"""
Sample & Hold / Track & Hold — Doepfer A-148

Captures the input voltage when triggered, holding the last sampled value
until the next trigger arrives.  In Track & Hold mode the output follows
the input while the gate is high and holds when the gate goes low.

DROID circuit: [sample]
"""

TOOL_META = {
    "name": "sample_hold",
    "description": "Sample & Hold / Track & Hold",
    "doepfer": "A-148",
    "required_inputs": ["signal", "trigger"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Return DROID .ini text for a [sample] circuit instance.

    Parameters
    ----------
    name : str
        Instance name, used for cable prefixes.
    inputs : dict
        Must contain ``"signal"`` and ``"trigger"`` mapped to hardware
        jacks or internal cables (e.g. ``{"signal": "I1", "trigger": "I2"}``).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable (e.g. ``{"output": "O1"}``).
    controls : dict
        Unused for this tool — kept for interface compatibility.

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    lines = [
        f"# {name}: Sample & Hold",
        "[sample]",
        f"    input = {inputs['signal']}",
        f"    trigger = {inputs['trigger']}",
        f"    output = {outputs['output']}",
    ]
    return "\n".join(lines)
