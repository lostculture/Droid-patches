"""
Boolean Logic — Doepfer A-166 Dual Logic Module

Takes two gate/trigger inputs and performs boolean logic operations:
AND, OR, XOR.  All three outputs are available simultaneously; only
those actually wired up will appear in the rendered .ini block.

DROID circuit: [logic]
"""

TOOL_META = {
    "name": "logic",
    "description": "Boolean logic: AND, OR, XOR on two gate inputs",
    "doepfer": "A-166",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": [],
    "required_outputs": [],
    "optional_outputs": ["and_out", "or_out", "xor_out"],
    "required_controls": [],
    "optional_controls": [],
}

# Maps logical output names to DROID [logic] circuit parameter names.
_OUTPUT_MAP = {
    "and_out": "and",
    "or_out": "or",
    "xor_out": "xor",
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a boolean logic instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"`` mapped to hardware
        jacks or internal cables (e.g. ``{"input1": "I1", "input2": "I2"}``).
    outputs : dict
        Any subset of ``{"and_out", "or_out", "xor_out"}`` mapped to
        hardware jacks or internal cables.  Only assigned outputs are
        included in the rendered block.
    controls : dict
        Unused for this tool — kept for interface compatibility.

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    lines = [
        f"# {name}: Boolean logic (AND / OR / XOR)",
        "[logic]",
        f"    input1 = {inputs['input1']}",
        f"    input2 = {inputs['input2']}",
    ]

    for key, param in _OUTPUT_MAP.items():
        if key in outputs:
            lines.append(f"    {param} = {outputs[key]}")

    return "\n".join(lines)
