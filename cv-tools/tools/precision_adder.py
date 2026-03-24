"""
Precision Adder — Doepfer A-185-2 Precision CV Adder

Sum 2-4 CV inputs together precisely.  Used for transposing pitch CVs,
combining modulation sources, stacking offsets, etc.  Each input is
summed at unity gain via a single [mixer] circuit.

Only the inputs that are actually provided are included in the rendered
block — input3 and input4 are fully optional.
"""

TOOL_META = {
    "name": "precision_adder",
    "description": "Sum 2-4 CV inputs precisely (transpose, offset)",
    "doepfer": "A-185",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": ["input3", "input4"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render a DROID .ini block for a precision CV adder.

    Args:
        name:     Instance name (unused by this circuit but kept for API
                  consistency with other tools).
        inputs:   Dict with "input1" and "input2" (required), plus
                  optionally "input3" and/or "input4".
        outputs:  Dict with "output" mapped to a jack or cable.
        controls: Dict (unused — no controls for a pure adder).

    Returns:
        A string containing the DROID [mixer] circuit block.
    """
    cv_out = outputs["output"]

    # Collect all provided inputs in canonical order
    input_keys = ["input1", "input2", "input3", "input4"]
    active_inputs = [
        (key, inputs[key]) for key in input_keys if key in inputs
    ]

    count = len(active_inputs)
    lines = [
        f"# Precision Adder: sum {count} CV inputs at unity gain",
        "",
        "[mixer]",
    ]

    for key, value in active_inputs:
        lines.append(f"    {key} = {value}")

    lines.append(f"    output = {cv_out}")

    return "\n".join(lines)
