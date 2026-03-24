"""
Voltage-Controlled Mixer — Doepfer A-135 VC Mixer for DROID

Mix 2-4 CV inputs with individual voltage-controlled levels into a
single output.  Each input's amplitude can be attenuated by a
corresponding level control (pot, CV, or expression).

Level behaviour per input:
  - If a level control is provided (e.g. "level1" for "input1"), the
    input is multiplied inline:  ``input1 = I1 * P1.1``
  - If no level control is provided, the input passes at full level
    with no multiplication.

Only inputs that are actually supplied are rendered — input3 and input4
are fully optional.

DROID circuit: [mixer]
"""

TOOL_META = {
    "name": "vc_mixer",
    "description": "CV mixer with voltage-controlled levels per input",
    "doepfer": "A-135",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": ["input3", "input4"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["level1", "level2", "level3", "level4"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a voltage-controlled mixer.

    Parameters
    ----------
    name : str
        Instance name, used in the comment header.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"``; may also contain
        ``"input3"`` and/or ``"input4"``.  Values are hardware jacks or
        internal cables (e.g. ``{"input1": "I1", "input2": "I2"}``).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable (e.g. ``{"output": "O1"}``).
    controls : dict
        Optionally ``"level1"`` through ``"level4"`` — each a pot, CV
        jack, or expression that scales the corresponding input.

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    cv_out = outputs["output"]

    # Collect provided inputs in canonical order
    input_keys = ["input1", "input2", "input3", "input4"]
    level_keys = ["level1", "level2", "level3", "level4"]

    active = [
        (ikey, inputs[ikey], controls.get(lkey))
        for ikey, lkey in zip(input_keys, level_keys)
        if ikey in inputs
    ]

    count = len(active)
    controlled = sum(1 for _, _, lvl in active if lvl)

    # Header comment
    lines = [f"# {name}: VC Mixer (A-135) — {count} inputs"]
    if controlled:
        level_summary = ", ".join(
            f"{ikey}*{lvl}" for ikey, _, lvl in active if lvl
        )
        lines.append(f"# Level controls: {level_summary}")

    lines += ["", "[mixer]"]

    for ikey, value, level in active:
        if level:
            lines.append(f"    {ikey} = {value} * {level}")
        else:
            lines.append(f"    {ikey} = {value}")

    lines.append(f"    output = {cv_out}")

    return "\n".join(lines)
