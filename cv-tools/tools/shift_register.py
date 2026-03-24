"""
Clocked CV Shift Register — Music Thing Turing Machine inspired

A chain of four sample-and-hold stages.  On each clock tick every stage
passes its value to the next stage, and the first stage samples a new
input.  Creates delay/canon effects for CV sequences.

When a feedback control (pot) is provided, the first stage input is a
crossfade between the new external input and the last stage output:

    input_expression = input * (1 - feedback) + stage4 * feedback

At 0 % feedback the register acts as a pure delay line.  At 100 % the
chain loops on itself (Turing Machine "locked" mode), producing an
evolving pattern of fixed length.

The stages are processed in **reverse order** so that each one latches
the previous stage's *old* value before that stage updates.

DROID circuit: [sample] (x4)
"""

TOOL_META = {
    "name": "shift_register",
    "description": "Clocked CV shift register with optional feedback (Turing Machine style)",
    "doepfer": "N/A",
    "inspired_by": "Music Thing Turing Machine",
    "required_inputs": ["input", "clock"],
    "optional_inputs": ["reset"],
    "required_outputs": ["output"],
    "optional_outputs": ["stage1", "stage2", "stage3", "stage4"],
    "required_controls": [],
    "optional_controls": ["feedback"],
}

_NUM_STAGES = 4


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a 4-stage clocked CV shift register.

    Parameters
    ----------
    name : str
        Instance name, used to prefix all internal cables.
    inputs : dict
        Must contain ``"input"`` (CV source) and ``"clock"`` (advance
        trigger).  May contain ``"reset"`` — a trigger that is OR-ed
        with the clock so all stages re-latch simultaneously.
    outputs : dict
        Must contain ``"output"`` (connected to the end of the chain,
        stage 4).  May contain any of ``"stage1"`` .. ``"stage4"``
        mapped to hardware jacks or internal cables.
    controls : dict
        May contain ``"feedback"`` — a pot (0-1) that crossfades the
        first stage's input between the external signal (0) and the
        last stage output (1).  When omitted the external input is
        used directly.

    Returns
    -------
    str
        DROID .ini circuit blocks for the shift register.
    """
    prefix = f"_{name}"

    input_sig = inputs["input"]
    clock_sig = inputs["clock"]
    reset_sig = inputs.get("reset")
    feedback = controls.get("feedback")

    # Build trigger expression (clock, optionally OR-ed with reset)
    if reset_sig is not None:
        trigger = f"{clock_sig} + {reset_sig}"
    else:
        trigger = clock_sig

    # Build stage-1 input expression (with optional feedback crossfade)
    if feedback is not None:
        stage1_input = (
            f"{input_sig} * (1 - {feedback}) + {prefix}_STAGE4 * {feedback}"
        )
    else:
        stage1_input = input_sig

    lines = [
        f"# {name}: CV Shift Register (Turing Machine style)",
        f"# 4-stage clocked S&H chain — processed in reverse order",
    ]

    # --- Stage 4 (last) — latches stage 3's value ---
    lines += [
        "",
        f"# Stage 4 — latches stage 3",
        "[sample]",
        f"    input = {prefix}_STAGE3",
        f"    trigger = {trigger}",
        f"    output = {prefix}_STAGE4",
    ]

    # --- Stage 3 — latches stage 2's value ---
    lines += [
        "",
        f"# Stage 3 — latches stage 2",
        "[sample]",
        f"    input = {prefix}_STAGE2",
        f"    trigger = {trigger}",
        f"    output = {prefix}_STAGE3",
    ]

    # --- Stage 2 — latches stage 1's value ---
    lines += [
        "",
        f"# Stage 2 — latches stage 1",
        "[sample]",
        f"    input = {prefix}_STAGE1",
        f"    trigger = {trigger}",
        f"    output = {prefix}_STAGE2",
    ]

    # --- Stage 1 — latches new input (or feedback mix) ---
    lines += [
        "",
        f"# Stage 1 — latches new input",
        "[sample]",
        f"    input = {stage1_input}",
        f"    trigger = {trigger}",
        f"    output = {prefix}_STAGE1",
    ]

    # --- Main output: end of chain (stage 4) ---
    lines += [
        "",
        f"# Main output (end of chain)",
        "[copy]",
        f"    input = {prefix}_STAGE4",
        f"    output = {outputs['output']}",
    ]

    # --- Optional per-stage outputs ---
    stage_map = {
        "stage1": f"{prefix}_STAGE1",
        "stage2": f"{prefix}_STAGE2",
        "stage3": f"{prefix}_STAGE3",
        "stage4": f"{prefix}_STAGE4",
    }

    for stage_name, cable in stage_map.items():
        stage_out = outputs.get(stage_name)
        if stage_out is not None:
            lines += [
                "",
                f"# {stage_name} tap output",
                "[copy]",
                f"    input = {cable}",
                f"    output = {stage_out}",
            ]

    return "\n".join(lines)
