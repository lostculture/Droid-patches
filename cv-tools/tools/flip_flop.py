"""
Flip-Flop / Toggle — General Utility

Converts triggers into a toggling on/off gate.  Each trigger alternates the
output between high (1) and low (0).  Essential for creating clock-synced
binary switches, dividing a clock by 2, latching behaviour, etc.

An optional reset input forces the output back to low.  An optional inverted
output provides the logical complement of the main output.

DROID circuit: [flipflop]
"""

TOOL_META = {
    "name": "flip_flop",
    "description": "Toggle output on each trigger (divide-by-2, binary switch)",
    "doepfer": "N/A",
    "inspired_by": "General utility",
    "required_inputs": ["trigger"],
    "optional_inputs": ["reset"],
    "required_outputs": ["output"],
    "optional_outputs": ["inverted"],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a flip-flop / toggle instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"trigger"`` mapped to a hardware jack or internal
        cable.  May contain ``"reset"`` to force the output low.
    outputs : dict
        Must contain ``"output"``.  May contain ``"inverted"`` for the
        logical complement of the main output.
    controls : dict
        Unused for this tool — kept for interface compatibility.

    Returns
    -------
    str
        DROID .ini circuit text.
    """
    trigger = inputs["trigger"]
    reset = inputs.get("reset")
    output = outputs["output"]
    inverted = outputs.get("inverted")

    # When both output and inverted are needed, route through an internal
    # cable so we can derive both from a single [flipflop] circuit.
    prefix = f"_{name}_"
    if inverted:
        ff_output = f"{prefix}gate"
    else:
        ff_output = output

    lines = [
        f"# {name}: Flip-Flop / Toggle",
        "[flipflop]",
        f"    toggle = {trigger}",
    ]

    if reset:
        lines.append(f"    reset = {reset}")

    lines.append(f"    output = {ff_output}")

    if inverted:
        # Copy internal cable to the requested output jack
        lines += [
            "",
            f"# {name}: gate output",
            "[copy]",
            f"    input = {ff_output}",
            f"    output = {output}",
            "",
            f"# {name}: inverted output",
            "[copy]",
            f"    input = -1 * {ff_output} + 1",
            f"    output = {inverted}",
        ]

    return "\n".join(lines)
