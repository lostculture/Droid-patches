"""
Voltage-Controlled Switch — Doepfer A-150 Dual VC Switch for DROID

Routes one of two inputs to the output based on a gate/CV control signal.
When the gate is low (0), input1 passes through; when high (1), input2
passes through.

The switching source is determined by priority:
  1. If a ``gate`` control is provided, it drives the offset directly.
  2. If a ``switch_btn`` button is provided, a [button] toggle circuit is
     created and its output drives the offset via an internal cable.
  3. If neither is provided, a default internal cable fixed at 0 is used
     (input1 always selected).

DROID circuit: [switch]
"""

TOOL_META = {
    "name": "vc_switch",
    "description": "Voltage-controlled 2-input signal switch",
    "doepfer": "A-150",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["gate", "switch_btn", "switch_led"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a voltage-controlled switch instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"`` mapped to hardware jacks
        or internal cables (e.g. ``{"input1": "I1", "input2": "I2"}``).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable
        (e.g. ``{"output": "O1"}``).
    controls : dict
        Optional keys:
        - ``"gate"``: External CV/gate jack that selects the active input.
        - ``"switch_btn"``: Button that toggles between inputs via a
          [button] circuit.
        - ``"switch_led"``: LED indicator for the toggle state (only used
          when ``switch_btn`` is provided).

    Returns
    -------
    str
        DROID .ini circuit block(s).
    """
    in1 = inputs["input1"]
    in2 = inputs["input2"]
    out = outputs["output"]

    gate = controls.get("gate")
    switch_btn = controls.get("switch_btn")
    switch_led = controls.get("switch_led")

    lines = [f"# {name}: Voltage-Controlled Switch (A-150)"]

    # Determine the offset source by priority
    if gate:
        # Direct CV/gate control
        gate_source = gate
    elif switch_btn:
        # Toggle button — create a [button] circuit first
        gate_cable = f"_{name}_GATE"
        btn_lines = [
            "[button]",
            f"    button = {switch_btn}",
        ]
        if switch_led:
            btn_lines.append(f"    led = {switch_led}")
        btn_lines.append(f"    output = {gate_cable}")
        lines.append("")
        lines.extend(btn_lines)
        gate_source = gate_cable
    else:
        # No control provided — default to input1 (offset = 0)
        gate_source = f"_{name}_SELECT"
        lines.append("")
        lines.append(f"# No gate or button provided; {gate_source} defaults to 0")
        lines.append("[copy]")
        lines.append(f"    input = 0")
        lines.append(f"    output = {gate_source}")

    # Main switch circuit
    lines.append("")
    lines.append("[switch]")
    lines.append(f"    input1 = {in1}")
    lines.append(f"    input2 = {in2}")
    lines.append(f"    offset = {gate_source}")
    lines.append(f"    output1 = {out}")

    return "\n".join(lines)
