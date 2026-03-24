"""
Trigger Delay — Doepfer A-162 Dual Trigger Delay for DROID

Delays incoming triggers/gates by a configurable amount of time.
When a clock input is provided, the delay parameter acts as clock
divisions (e.g. 0.25 = one quarter-note delay).  Without a clock,
delay is a free-running time in seconds.

DROID circuit: [triggerdelay]
"""

TOOL_META = {
    "name": "trigger_delay",
    "description": "Delay triggers by time or clock divisions",
    "doepfer": "A-162",
    "required_inputs": ["input"],
    "optional_inputs": ["clock"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["delay_time"],
}

_DEFAULT_DELAY = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a trigger delay instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input"`` mapped to a hardware jack or internal cable.
        Optionally contains ``"clock"`` to sync the delay to an external clock.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable.
    controls : dict
        Optional keys: ``"delay_time"`` — a pot or fixed value controlling the
        delay amount.  If omitted, defaults to 0.5.

    Returns
    -------
    str
        DROID .ini text for the [triggerdelay] circuit.
    """
    input_sig = inputs["input"]
    output_sig = outputs["output"]
    clock = inputs.get("clock")
    delay = controls.get("delay_time", _DEFAULT_DELAY)

    lines = [
        f"# {name}: Trigger Delay",
        "[triggerdelay]",
        f"    input = {input_sig}",
    ]

    if clock:
        lines.append(f"    clock = {clock}")

    lines += [
        f"    delay = {delay}",
        f"    output = {output_sig}",
    ]

    return "\n".join(lines)
