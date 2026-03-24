"""
Voltage Clamp / Limiter — General Utility

Constrain a CV signal to a defined range by clipping values that exceed a
ceiling or drop below a floor.  Anything above the ceiling outputs the ceiling
value; anything below the floor outputs the floor value.  Values within the
range pass through unchanged.

Essential for protecting downstream modules from out-of-range CVs, or for
hard-limiting modulation signals to a safe window.

Implementation uses two cascaded [compare] circuits:
  1. Clamp to ceiling — if input > ceiling, output ceiling; else pass through.
  2. Clamp to floor   — if result < floor, output floor; else pass through.

If only one boundary is provided, only that clamp is emitted.
If neither is provided, defaults to the standard 0–1 V range (floor=0,
ceiling=1).
"""

TOOL_META = {
    "name": "voltage_clamp",
    "description": "Constrain CV to a min/max range (clip/limit)",
    "doepfer": "N/A",
    "inspired_by": "General utility",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["floor", "ceiling"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a voltage clamp / limiter.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" mapped to a jack or cable.
        outputs:  Dict with "output" mapped to a jack or cable.
        controls: Dict with optionally "floor" and/or "ceiling".

    Returns:
        A string containing the DROID circuit blocks.
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]
    floor_val = controls.get("floor")
    ceiling_val = controls.get("ceiling")

    # Apply defaults when neither boundary is supplied
    if floor_val is None and ceiling_val is None:
        floor_val = "0"
        ceiling_val = "1"

    has_ceiling = ceiling_val is not None
    has_floor = floor_val is not None

    lines = [f"# {name}: Voltage Clamp / Limiter"]

    if has_ceiling and has_floor:
        # Both boundaries — two cascaded compares with internal cable
        clamped_high = f"_{name}_CLAMPED_HIGH"

        lines += [
            "",
            f"# Clamp to ceiling: if input > {ceiling_val}, output {ceiling_val}",
            "[compare]",
            f"    input = {cv_in}",
            f"    compare = {ceiling_val}",
            f"    ifgreater = {ceiling_val}",
            f"    ifless = {cv_in}",
            f"    ifequal = {cv_in}",
            f"    output = {clamped_high}",
            "",
            f"# Clamp to floor: if clamped < {floor_val}, output {floor_val}",
            "[compare]",
            f"    input = {clamped_high}",
            f"    compare = {floor_val}",
            f"    ifgreater = {clamped_high}",
            f"    ifless = {floor_val}",
            f"    ifequal = {clamped_high}",
            f"    output = {cv_out}",
        ]

    elif has_ceiling:
        # Ceiling only — single compare
        lines += [
            "",
            f"# Clamp to ceiling: if input > {ceiling_val}, output {ceiling_val}",
            "[compare]",
            f"    input = {cv_in}",
            f"    compare = {ceiling_val}",
            f"    ifgreater = {ceiling_val}",
            f"    ifless = {cv_in}",
            f"    ifequal = {cv_in}",
            f"    output = {cv_out}",
        ]

    elif has_floor:
        # Floor only — single compare
        lines += [
            "",
            f"# Clamp to floor: if input < {floor_val}, output {floor_val}",
            "[compare]",
            f"    input = {cv_in}",
            f"    compare = {floor_val}",
            f"    ifgreater = {cv_in}",
            f"    ifless = {floor_val}",
            f"    ifequal = {cv_in}",
            f"    output = {cv_out}",
        ]

    return "\n".join(lines)
