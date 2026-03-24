"""
Gate Combiner — Doepfer A-186-1 Gate/Trigger Combiner

Merge 2-4 gate/trigger inputs into a single output using OR logic.
Output is high whenever ANY input is high.  Simpler than the full logic
tool — this is just a multi-input OR for combining gate signals.

Implementation: a [copy] circuit whose input is the sum of all active
gate inputs.  In DROID, adding gates works as OR because any non-zero
value is "high".  The output may exceed 1 when multiple gates overlap,
but that is perfectly fine for gate signals.

DROID circuit: [copy]
"""

TOOL_META = {
    "name": "gate_combiner",
    "description": "Merge 2-4 gates/triggers into one (OR combine)",
    "doepfer": "A-186-1",
    "required_inputs": ["input1", "input2"],
    "optional_inputs": ["input3", "input4"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": [],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a gate/trigger combiner.

    Parameters
    ----------
    name : str
        Instance name, used in the comment header.
    inputs : dict
        Must contain ``"input1"`` and ``"input2"`` mapped to hardware
        jacks or internal cables.  May contain ``"input3"`` and/or
        ``"input4"`` for additional gate sources.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable.
    controls : dict
        Unused for this tool — kept for interface compatibility.

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    gate_out = outputs["output"]

    # Collect all provided inputs in canonical order
    input_keys = ["input1", "input2", "input3", "input4"]
    active_inputs = [inputs[key] for key in input_keys if key in inputs]

    count = len(active_inputs)
    expression = " + ".join(active_inputs)

    lines = [
        f"# {name}: Gate Combiner — OR-merge {count} gate/trigger inputs",
        "[copy]",
        f"    input = {expression}",
        f"    output = {gate_out}",
    ]

    return "\n".join(lines)
