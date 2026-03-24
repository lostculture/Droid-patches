"""
CV Inverter — Doepfer A-175 Dual Inverter

Invert a CV signal around a configurable center point.  The default
center is 0.5, so an input of 0 outputs 1 and an input of 1 outputs 0
(standard unipolar inversion).

Mathematically: ``output = -1 * (input - center) + center``
which simplifies to: ``output = -input + 2 * center``

With the default center of 0.5 this becomes: ``output = -input + 1``

Simpler and more explicit than patching an attenuverter set to -1 with
an offset.  The adjustable center point lets you invert around any
reference voltage — useful for bipolar signals (center = 0) or signals
with non-standard ranges.
"""

TOOL_META = {
    "name": "cv_inverter",
    "description": "Invert CV signal around a center point",
    "doepfer": "A-175",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["center"],
}


def render(name, inputs, outputs, controls):
    """Render a DROID .ini block for a CV inverter.

    Args:
        name:     Instance name, used as cable prefix.
        inputs:   Dict with at least "input" mapped to a jack or cable.
        outputs:  Dict with at least "output" mapped to a jack or cable.
        controls: Dict with optionally "center" (default 0.5).

    Returns:
        A string containing the DROID [copy] circuit block.
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]
    center = controls.get("center")

    if center:
        # Variable center: output = -input + 2 * center
        expr = f"-1 * {cv_in} + 2 * {center}"
        comment_detail = f"# Center point controlled by {center}"
    else:
        # Default center 0.5: output = -input + 1
        expr = f"-1 * {cv_in} + 1"
        comment_detail = "# Center = 0.5 (default): 0 -> 1, 1 -> 0"

    lines = [
        f"# {name}: CV Inverter (A-175 style)",
        comment_detail,
        "",
        "[copy]",
        f"    input = {expr}",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
