"""
Slope Detector — Befaco Rampage Slope Detector Section

Detects whether an incoming CV is rising or falling and outputs separate
gates for each direction.  Useful for extracting rhythm from modulation,
detecting envelope phases, triggering events on direction changes, etc.

The input is sampled on each clock tick to capture a "previous" value.
Between ticks, the live input is compared against that held value:

- **Rising gate** goes high when the current input is greater than the
  previous sample.
- **Falling gate** goes high when the current input is less than the
  previous sample.

Only the ``[compare]`` circuits for outputs that are actually assigned
are emitted.  At least one of ``rising`` or ``falling`` must be provided.

DROID circuits: [sample], [compare]
"""

TOOL_META = {
    "name": "slope_detector",
    "description": "Detect rising/falling CV slopes, output separate gates",
    "doepfer": "N/A",
    "inspired_by": "Befaco Rampage slope detector",
    "required_inputs": ["input", "clock"],
    "optional_inputs": [],
    "required_outputs": [],
    "optional_outputs": ["rising", "falling"],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a slope detector.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" and "clock" mapped to jacks or cables.
        outputs:  Dict with optionally "rising" and/or "falling".
        controls: Dict (unused — no controls for this tool).

    Returns:
        A string containing the DROID circuit blocks.

    Raises:
        ValueError: If neither rising nor falling is provided.
    """
    cv_in = inputs["input"]
    clock = inputs["clock"]
    rising = outputs.get("rising")
    falling = outputs.get("falling")

    if not rising and not falling:
        raise ValueError(
            f"{name}: at least one of 'rising' or 'falling' must be assigned"
        )

    prefix = f"_{name}_"
    prev_cable = f"{prefix}PREV"

    lines = [
        f"# {name}: Slope Detector (Befaco Rampage)",
        "",
        "# Capture previous value on each clock tick",
        "[sample]",
        f"    input = {cv_in}",
        f"    trigger = {clock}",
        f"    output = {prev_cable}",
    ]

    if rising:
        lines += [
            "",
            "# Rising: gate high when current input > previous sample",
            "[compare]",
            f"    input = {cv_in}",
            f"    compare = {prev_cable}",
            "    ifgreater = 1",
            "    ifless = 0",
            "    ifequal = 0",
            f"    output = {rising}",
        ]

    if falling:
        lines += [
            "",
            "# Falling: gate high when current input < previous sample",
            "[compare]",
            f"    input = {cv_in}",
            f"    compare = {prev_cable}",
            "    ifgreater = 0",
            "    ifless = 1",
            "    ifequal = 0",
            f"    output = {falling}",
        ]

    return "\n".join(lines)
