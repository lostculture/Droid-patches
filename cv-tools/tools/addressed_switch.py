"""
Addressed Switch — Doepfer A-152 Voltage Addressed Switch for DROID

A switch where the active input/output is selected by a CV address voltage
(0–1).  Unlike the sequential switch which steps through inputs on clock
pulses, this one jumps directly to the input addressed by the CV.  Can also
function as an analog shift register (ASR) when combined with an external
clock.

Address mapping:
  - 2 inputs: 0 = input1, 1 = input2
  - 3 inputs: 0 = input1, 0.5 = input2, 1 = input3
  - 4 inputs: 0, 0.333, 0.667, 1.0

The address source is determined by what is provided:
  1. Both ``address`` input and ``address_knob`` control → summed.
  2. Only ``address`` input → used directly.
  3. Only ``address_knob`` control → used directly.
  4. Neither → offset defaults to 0 (input1 always selected).

DROID circuit: [switch]
"""

TOOL_META = {
    "name": "addressed_switch",
    "description": "CV-addressed input selector (1-of-4) with optional ASR mode",
    "doepfer": "A-152",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": ["input3", "input4", "address"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["address_knob"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a CV-addressed switch instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"`` mapped to hardware jacks
        or internal cables.  May also contain ``"input3"``, ``"input4"``,
        and ``"address"`` (a CV source that selects the active input).
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable.
    controls : dict
        Optional keys:
        - ``"address_knob"``: A pot/encoder that sets or offsets the
          address position (e.g. ``"P1.1"``).

    Returns
    -------
    str
        DROID .ini circuit block(s).
    """
    output = outputs["output"]

    address_cv = inputs.get("address")
    address_knob = controls.get("address_knob")

    # --- Count how many inputs are wired ---
    input_count = 2
    if "input3" in inputs:
        input_count = 3
    if "input4" in inputs:
        input_count = 4

    # --- Determine offset source ---
    if address_cv and address_knob:
        offset = f"{address_cv} + {address_knob}"
    elif address_cv:
        offset = address_cv
    elif address_knob:
        offset = address_knob
    else:
        offset = "0"

    # --- Addressed switch circuit ---
    lines = [f"# {name}: Addressed Switch ({input_count} inputs, A-152)"]
    lines.append("[switch]")
    for i in range(1, input_count + 1):
        lines.append(f"    input{i} = {inputs[f'input{i}']}")
    lines.append(f"    offset = {offset}")
    lines.append(f"    output1 = {output}")

    return "\n".join(lines)
