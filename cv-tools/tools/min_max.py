"""
Minimum/Maximum Selector — Doepfer A-172 Maximum/Minimum Selector

Takes two CV inputs and outputs the higher (maximum) and/or lower (minimum)
of the two.  Useful for CV limiting, waveshaping, and creating complex
modulation.

DROID doesn't have a dedicated min/max circuit, so we implement it using
[compare]:

  - MAX: compare input1 against input2 — pass whichever is greater.
  - MIN: compare input1 against input2 — pass whichever is lesser.

Only the circuits for outputs that are actually assigned are emitted.
At least one of ``max_out`` or ``min_out`` must be provided.
"""

TOOL_META = {
    "name": "min_max",
    "description": "Output the min and/or max of two CV inputs",
    "doepfer": "A-172",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": [],
    "required_outputs": [],
    "optional_outputs": ["max_out", "min_out"],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a min/max selector.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input1" and "input2" mapped to jacks or cables.
        outputs:  Dict with optionally "max_out" and/or "min_out".
        controls: Dict (unused — no controls for this tool).

    Returns:
        A string containing the DROID circuit blocks.

    Raises:
        ValueError: If neither max_out nor min_out is provided.
    """
    in1 = inputs["input1"]
    in2 = inputs["input2"]
    max_out = outputs.get("max_out")
    min_out = outputs.get("min_out")

    if not max_out and not min_out:
        raise ValueError(
            f"{name}: at least one of 'max_out' or 'min_out' must be assigned"
        )

    lines = [f"# {name}: Min/Max Selector (A-172)"]

    if max_out:
        lines += [
            "",
            "# Maximum: output whichever input is greater",
            "[compare]",
            f"    input = {in1}",
            f"    compare = {in2}",
            f"    ifgreater = {in1}",
            f"    ifless = {in2}",
            f"    ifequal = {in1}",
            f"    output = {max_out}",
        ]

    if min_out:
        lines += [
            "",
            "# Minimum: output whichever input is lesser",
            "[compare]",
            f"    input = {in1}",
            f"    compare = {in2}",
            f"    ifgreater = {in2}",
            f"    ifless = {in1}",
            f"    ifequal = {in1}",
            f"    output = {min_out}",
        ]

    return "\n".join(lines)
