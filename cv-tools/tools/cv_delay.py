"""
Clocked CV Delay Line — Chronoblob-inspired CV delay for DROID

Delays a control voltage signal by N clock steps, producing echo/canon
effects on pitch sequences, delayed modulation, and other time-shifted
CV patterns.  On each clock tick the output plays back the input value
from N steps ago.

DROID circuit: [delay]
"""

TOOL_META = {
    "name": "cv_delay",
    "description": "Clocked CV delay line (echo/canon for control voltages)",
    "doepfer": "N/A",
    "inspired_by": "Chronoblob concept for CV",
    "required_inputs": ["input", "clock"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["delay_steps"],
}

_DEFAULT_DELAY_STEPS = 4


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a clocked CV delay instance.

    Parameters
    ----------
    name : str
        Instance name, used to prefix internal signals.
    inputs : dict
        Must contain ``"input"`` (CV source) and ``"clock"`` (clock to
        advance the delay line).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable.
    controls : dict
        Optional keys: ``"delay_steps"`` — a pot or fixed value
        controlling how many clock steps the signal is delayed.  When a
        pot is provided its 0-1 range is scaled to 1-16 steps.  If
        omitted the delay defaults to 4 steps.

    Returns
    -------
    str
        DROID .ini text for the [delay] circuit.
    """
    input_sig = inputs["input"]
    clock_sig = inputs["clock"]
    output_sig = outputs["output"]
    delay_steps = controls.get("delay_steps")

    # Pot 0-1 maps to 1-16 steps: time = pot * 15 + 1
    # Without a pot, default to 4 steps.
    if delay_steps is not None:
        time_expr = f"{delay_steps} * 15 + 1"
    else:
        time_expr = str(_DEFAULT_DELAY_STEPS)

    lines = [
        f"# {name}: Clocked CV Delay",
        "[delay]",
        f"    input = {input_sig}",
        f"    clock = {clock_sig}",
        f"    time = {time_expr}",
        f"    output = {output_sig}",
    ]

    return "\n".join(lines)
