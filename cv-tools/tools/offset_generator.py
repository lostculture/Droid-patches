"""
Offset Generator — Doepfer A-183-2 Offset Generator

Add a fixed or controllable DC voltage offset to a CV signal.

When an input is connected the offset is summed with it — useful for
biasing signals, shifting pitch CVs up/down by a fixed interval, or
moving a bipolar LFO into unipolar territory.

When no input is connected the module acts as a standalone voltage
source, outputting just the offset value — handy for providing a fixed
reference voltage or manual CV anywhere in a patch.

The offset amount defaults to 0.5 (mid-range) when no pot or external
control is assigned.
"""

TOOL_META = {
    "name": "offset_generator",
    "description": "Add voltage offset to CV signal (or generate fixed voltage)",
    "doepfer": "A-183-2",
    "required_inputs": [],
    "optional_inputs": ["input"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["offset"],
}


def render(name, inputs, outputs, controls):
    """Render a DROID .ini block for a CV offset generator.

    Args:
        name:     Instance name, used as cable prefix.
        inputs:   Dict optionally containing "input" mapped to a jack or cable.
        outputs:  Dict with "output" mapped to a jack or cable.
        controls: Dict optionally containing "offset" (pot or CV source).
                  Defaults to 0.5 when not provided.

    Returns:
        A string containing the DROID [copy] circuit block.
    """
    cv_in = inputs.get("input")
    cv_out = outputs["output"]
    offset = controls.get("offset", "0.5")

    # Build the input expression:
    #   (input or 0) + (offset or 0.5)
    if cv_in:
        expr = f"{cv_in} + {offset}"
    else:
        expr = str(offset)

    if cv_in:
        comment = "# Offset Generator: add DC offset to input signal"
    else:
        comment = "# Offset Generator: standalone voltage source"

    lines = [
        comment,
        "",
        "[copy]",
        f"    input = {expr}",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
