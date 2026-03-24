"""
Voltage Scaler / Range Mapper — Doepfer A-183-4 Quad Level Shifter

Map a CV signal from one voltage range to another.  For example, map a
0–1 V input to 0.2–0.8 V output, or expand a narrow range to full 0–1 V.
Essential for adapting signals between modules that use different ranges.

Mapping formula:
    output = (input - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

For the default case (in: 0–1, out: 0–1) this is a transparent pass-through.

Since DROID cannot perform division inline, the implementation assumes a
standard 0–1 V input range by default.  With that assumption the formula
simplifies to:

    output = input * (out_max - out_min) + out_min

When in_min / in_max controls are also provided, the input is first
normalised to 0–1 via a preceding [copy] stage and then scaled:

    normalised = (input - in_min) / (in_max - in_min)

To approximate the division we pre-compute a reciprocal scaling factor.
However, if the input range is dynamic (pots), true runtime division is
impossible in a single DROID expression.  The recommended workflow is to
set in_min and in_max as fixed literals so the builder can fold them.

If only out_min and out_max are given, input is assumed 0–1 and no
normalisation stage is emitted — this is the most common use-case
(two pots controlling the output window).
"""

TOOL_META = {
    "name": "voltage_scaler",
    "description": "Map CV from one voltage range to another (scale and shift)",
    "doepfer": "A-183-4",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["in_min", "in_max", "out_min", "out_max"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a voltage range scaler / mapper.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" mapped to a jack or cable.
        outputs:  Dict with "output" mapped to a jack or cable.
        controls: Dict with optionally "in_min", "in_max", "out_min",
                  "out_max".  Controls may be pot references, CV jacks,
                  or numeric literals.

    Returns:
        A string containing the DROID circuit block(s).
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]

    in_min = controls.get("in_min")
    in_max = controls.get("in_max")
    out_min = controls.get("out_min")
    out_max = controls.get("out_max")

    # Apply defaults — full 0-1 pass-through when nothing is specified
    if out_min is None:
        out_min = "0"
    if out_max is None:
        out_max = "1"

    lines = [f"# {name}: Voltage Scaler / Range Mapper (A-183-4)"]

    # --- Input normalisation stage ---
    # When an explicit input range is given, normalise to 0-1 first.
    if in_min is not None or in_max is not None:
        # Default missing boundaries to the standard range
        if in_min is None:
            in_min = "0"
        if in_max is None:
            in_max = "1"

        # Internal cable carries the normalised value
        norm_cable = f"_{name}_NORM"

        lines += [
            f"# Normalise input from [{in_min} .. {in_max}] to 0-1",
            "",
            "# norm = (input - in_min) / (in_max - in_min)",
            "# We split this into: subtract in_min, then multiply by",
            "# 1 / (in_max - in_min).  The denominator must be a fixed",
            "# literal for the reciprocal to be computed at build time.",
            "[copy]",
            f"    input = ({cv_in} - {in_min}) / ({in_max} - {in_min})",
            f"    output = {norm_cable}",
        ]

        # The scaling stage reads the normalised signal
        scale_input = norm_cable
    else:
        # No input-range controls — assume 0-1 input directly
        scale_input = cv_in

    # --- Output scaling stage ---
    # output = normalised_input * (out_max - out_min) + out_min
    # Special-case: if out_min=0 and out_max=1, just pass through.
    is_passthrough = (out_min == "0" and out_max == "1")

    if is_passthrough and scale_input == cv_in:
        # Total pass-through — emit a trivial copy
        lines += [
            "# Pass-through (default 0-1 -> 0-1)",
            "",
            "[copy]",
            f"    input = {cv_in}",
            f"    output = {cv_out}",
        ]
    else:
        lines += [
            f"# Scale to output range [{out_min} .. {out_max}]",
            "",
            "[copy]",
            f"    input = {scale_input} * ({out_max} - {out_min}) + {out_min}",
            f"    output = {cv_out}",
        ]

    return "\n".join(lines)
