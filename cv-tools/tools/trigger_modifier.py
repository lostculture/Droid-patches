"""
Trigger Modifier — Doepfer A-165 Dual Trigger Modifier for DROID

Converts between gates and triggers, and modifies gate length.  Can turn
a short trigger into a longer gate, or turn a long gate into a short
trigger.  When a gate_length control (pot) is provided, it sets the
output gate duration dynamically; otherwise a fixed default of 0.5 is
used.

DROID circuit: [gatetool]
"""

TOOL_META = {
    "name": "trigger_modifier",
    "description": "Gate/trigger conversion and gate length modifier",
    "doepfer": "A-165",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["gate_length"],
}

_DEFAULT_GATE_LENGTH = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a trigger modifier instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input"`` mapped to a hardware jack or internal cable.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable.
    controls : dict
        Optional keys: ``"gate_length"`` — a pot or fixed value controlling
        the output gate duration.  If omitted, defaults to 0.5.

    Returns
    -------
    str
        DROID .ini text for the [gatetool] circuit.
    """
    input_sig = inputs["input"]
    output_sig = outputs["output"]
    gate_length = controls.get("gate_length", _DEFAULT_GATE_LENGTH)

    lines = [
        f"# {name}: Trigger Modifier",
        "[gatetool]",
        f"    inputgate = {input_sig}",
        f"    gatelength = {gate_length}",
        f"    output = {output_sig}",
    ]

    return "\n".join(lines)
