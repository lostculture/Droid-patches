"""
Rectifier — MI Kinks Sign Section

Full-wave and half-wave CV rectification for bipolar signals.

- **Full-wave rectification** folds negative voltages positive (absolute
  value).  Useful as a frequency doubler or CV waveshaper — a triangle
  LFO becomes a double-speed triangle, a sine becomes a double-speed
  bump wave.

- **Half-wave rectification** clips negative voltages to zero and passes
  positive voltages unchanged.  Useful for converting bipolar modulation
  into unipolar, or gating a signal by its own polarity.

Both modes are implemented with a single [compare] circuit each,
testing the input against 0 and routing accordingly.

Only the circuits for outputs that are actually assigned are emitted.
At least one of ``full_wave`` or ``half_wave`` must be provided.
"""

TOOL_META = {
    "name": "rectifier",
    "description": "Full-wave and half-wave CV rectifier",
    "doepfer": "N/A",
    "inspired_by": "MI Kinks",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": [],
    "optional_outputs": ["full_wave", "half_wave"],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a CV rectifier.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" mapped to a jack or cable.
        outputs:  Dict with optionally "full_wave" and/or "half_wave".
        controls: Dict (unused — no controls for this tool).

    Returns:
        A string containing the DROID circuit blocks.

    Raises:
        ValueError: If neither full_wave nor half_wave is provided.
    """
    cv_in = inputs["input"]
    full_wave = outputs.get("full_wave")
    half_wave = outputs.get("half_wave")

    if not full_wave and not half_wave:
        raise ValueError(
            f"{name}: at least one of 'full_wave' or 'half_wave' must be assigned"
        )

    lines = [f"# {name}: CV Rectifier (MI Kinks)"]

    if full_wave:
        lines += [
            "",
            "# Full-wave rectification: fold negative to positive (abs)",
            "[compare]",
            f"    input = {cv_in}",
            "    compare = 0",
            f"    ifgreater = {cv_in}",
            f"    ifless = -1 * {cv_in}",
            "    ifequal = 0",
            f"    output = {full_wave}",
        ]

    if half_wave:
        lines += [
            "",
            "# Half-wave rectification: clip negative to zero",
            "[compare]",
            f"    input = {cv_in}",
            "    compare = 0",
            f"    ifgreater = {cv_in}",
            "    ifless = 0",
            "    ifequal = 0",
            f"    output = {half_wave}",
        ]

    return "\n".join(lines)
