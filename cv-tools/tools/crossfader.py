"""
Crossfader — Doepfer A-134 Voltage Controlled Crossfader

Smoothly fade between two CV inputs using a mix control.  At mix = 0 the
output is fully input1, at mix = 1 fully input2, and at 0.5 an equal blend
of both.  The mix parameter can come from a pot, an external CV, or both.

Mix source priority:
  1. "mix" pot AND "cv_mix" CV — combined: mix + cv_mix
  2. "mix" pot only            — manual crossfade
  3. "cv_mix" CV only          — voltage-controlled crossfade
  4. Neither provided          — fixed equal mix at 0.5

DROID circuit: [crossfader]
"""

TOOL_META = {
    "name": "crossfader",
    "description": "Fade between two CV sources",
    "doepfer": "A-134",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["mix", "cv_mix"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a voltage-controlled crossfader.

    Parameters
    ----------
    name : str
        Instance name, used for cable prefixes.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"`` mapped to hardware jacks
        or internal cables (e.g. ``{"input1": "I1", "input2": "I2"}``).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable (e.g. ``{"output": "O1"}``).
    controls : dict
        Optionally ``"mix"`` (a pot for manual crossfade) and/or
        ``"cv_mix"`` (an input jack for CV modulation of the mix).

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    input1 = inputs["input1"]
    input2 = inputs["input2"]
    cv_out = outputs["output"]

    mix_pot = controls.get("mix")
    cv_mix = controls.get("cv_mix")

    # Determine the mix expression (priority: both > pot > cv > 0.5)
    if mix_pot and cv_mix:
        mix_value = f"{mix_pot} + {cv_mix}"
    elif mix_pot:
        mix_value = mix_pot
    elif cv_mix:
        mix_value = cv_mix
    else:
        mix_value = "0.5"

    lines = [
        f"# {name}: Crossfader (A-134)",
    ]

    if mix_pot and cv_mix:
        lines.append(f"# Mix: pot {mix_pot} + CV {cv_mix}")
    elif mix_pot:
        lines.append(f"# Mix: manual via {mix_pot}")
    elif cv_mix:
        lines.append(f"# Mix: CV controlled via {cv_mix}")
    else:
        lines.append("# Mix: fixed at 0.5 (equal blend)")

    lines += [
        "",
        "[crossfader]",
        f"    input1 = {input1}",
        f"    input2 = {input2}",
        f"    mix = {mix_value}",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
