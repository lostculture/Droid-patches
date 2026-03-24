"""
Sequential Switch — Doepfer A-151 Sequential Switch for DROID

A clock-driven switch that cycles through 2-4 inputs sequentially,
advancing to the next input on each clock pulse.  Can be reset via
an external trigger or a controller button.

DROID circuit: [switch]
"""

TOOL_META = {
    "name": "sequential_switch",
    "description": "Clock-driven sequential input selector (2-4 inputs)",
    "doepfer": "A-151",
    "required_inputs": ["clock", "input1", "input2"],
    "optional_inputs": ["input3", "input4", "reset"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["reset_btn", "reset_led"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a sequential switch instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"clock"``, ``"input1"``, and ``"input2"``.
        May also contain ``"input3"``, ``"input4"``, and ``"reset"``.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable.
    controls : dict
        Optional keys: ``"reset_btn"`` and ``"reset_led"``.
        When ``reset_btn`` is provided a [button] circuit is generated and
        its output is combined with any external reset input.

    Returns
    -------
    str
        DROID .ini circuit block(s).
    """
    clock = inputs["clock"]
    output = outputs["output"]

    reset_btn = controls.get("reset_btn")
    reset_led = controls.get("reset_led")
    external_reset = inputs.get("reset")

    lines = []

    # --- Optional reset button circuit ---
    if reset_btn:
        btn_cable = f"_{name}_RESET_BTN"
        lines.append(f"# {name}: reset button")
        lines.append("[button]")
        lines.append(f"    button = {reset_btn}")
        if reset_led:
            lines.append(f"    led = {reset_led}")
        lines.append("    states = 1")
        lines.append(f"    output = {btn_cable}")
        lines.append("")

    # Determine the combined reset signal
    if reset_btn and external_reset:
        reset_signal = f"_{name}_RESET_BTN + {external_reset}"
    elif reset_btn:
        reset_signal = f"_{name}_RESET_BTN"
    elif external_reset:
        reset_signal = external_reset
    else:
        reset_signal = None

    # --- Count how many inputs are wired ---
    input_count = 2
    if "input3" in inputs:
        input_count = 3
    if "input4" in inputs:
        input_count = 4

    # --- Sequential switch circuit ---
    lines.append(f"# {name}: Sequential Switch ({input_count} inputs)")
    lines.append("[switch]")
    for i in range(1, input_count + 1):
        lines.append(f"    input{i} = {inputs[f'input{i}']}")
    lines.append(f"    forward = {clock}")
    if reset_signal:
        lines.append(f"    reset = {reset_signal}")
    lines.append(f"    output1 = {output}")

    return "\n".join(lines)
