#!/usr/bin/env python3
"""
DROID CV Tool: Clock Divider (Doepfer A-160)

Divides an incoming clock by a selectable ratio (1-16).
Provides a reset input to sync the division phase.

Uses the DROID [clocktool] circuit with the 'divide' parameter.
"""

TOOL_META = {
    "name": "clock_divider",
    "description": "Clock divider with selectable ratio and reset",
    "doepfer": "A-160",
    "required_inputs": ["clock"],
    "optional_inputs": ["reset"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["ratio", "reset_btn", "reset_led"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a clock divider instance.

    Parameters
    ----------
    name : str
        Instance name, used to prefix internal signals.
    inputs : dict
        Must contain "clock". May contain "reset".
    outputs : dict
        Must contain "output".
    controls : dict
        May contain "ratio" (pot), "reset_btn" (button),
        "reset_led" (LED for the reset button).

    Returns
    -------
    str
        DROID .ini circuit text.
    """
    lines = []
    prefix = f"_{name.upper()}"

    clock = inputs["clock"]
    output = outputs["output"]

    reset_input = inputs.get("reset")
    ratio_pot = controls.get("ratio")
    reset_btn = controls.get("reset_btn")
    reset_led = controls.get("reset_led")

    # --- Reset button (if provided) ---
    has_reset_btn = reset_btn is not None
    if has_reset_btn:
        lines.append(f"# {name}: reset button")
        lines.append("[button]")
        lines.append(f"    button = {reset_btn}")
        lines.append("    states = 1")
        if reset_led:
            lines.append(f"    led = {reset_led}")
        lines.append(f"    output = {prefix}_RESET_BTN")
        lines.append("")

    # --- Combine reset sources ---
    # Build a combined reset signal from external reset input and button
    has_reset_input = reset_input is not None
    if has_reset_btn and has_reset_input:
        lines.append(f"# {name}: merge reset sources")
        lines.append("[copy]")
        lines.append(f"    input = {reset_input} + {prefix}_RESET_BTN")
        lines.append(f"    output = {prefix}_RESET")
        lines.append("")
        reset_signal = f"{prefix}_RESET"
    elif has_reset_btn:
        reset_signal = f"{prefix}_RESET_BTN"
    elif has_reset_input:
        reset_signal = reset_input
    else:
        reset_signal = None

    # --- Divide ratio ---
    # Pot 0-1 maps to divide 1-16: divide = pot * 15 + 1
    # Without a pot, default to divide by 2.
    if ratio_pot:
        divide_expr = f"{ratio_pot} * 15 + 1"
    else:
        divide_expr = "2"

    # --- Clock divider circuit ---
    lines.append(f"# {name}: clock divider (A-160)")
    lines.append("[clocktool]")
    lines.append(f"    clock = {clock}")
    if reset_signal:
        lines.append(f"    reset = {reset_signal}")
    lines.append(f"    divide = {divide_expr}")
    lines.append(f"    output = {output}")

    return "\n".join(lines)
