#!/usr/bin/env python3
"""
DROID CV Tool: Clock Multiplier (Doepfer A-160-5)

Multiplies an incoming clock rate by a selectable factor (x2 to x16).
Complements the clock_divider tool for creating faster subdivisions.

Uses the DROID [clocktool] circuit with the 'multiply' parameter.
"""

TOOL_META = {
    "name": "clock_multiplier",
    "description": "Clock multiplier with selectable ratio (x2 to x16)",
    "doepfer": "A-160-5",
    "required_inputs": ["clock"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["ratio"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a clock multiplier instance.

    Parameters
    ----------
    name : str
        Instance name, used to prefix internal signals.
    inputs : dict
        Must contain "clock".
    outputs : dict
        Must contain "output".
    controls : dict
        May contain "ratio" (pot) — maps 0-1 to multiply 1-16.

    Returns
    -------
    str
        DROID .ini circuit text.
    """
    lines = []

    clock = inputs["clock"]
    output = outputs["output"]

    ratio_pot = controls.get("ratio")

    # --- Multiply ratio ---
    # Pot 0-1 maps to multiply 1-16: multiply = pot * 15 + 1
    # Without a pot, default to multiply by 2.
    if ratio_pot:
        multiply_expr = f"{ratio_pot} * 15 + 1"
    else:
        multiply_expr = "2"

    # --- Clock multiplier circuit ---
    lines.append(f"# {name}: clock multiplier (A-160-5)")
    lines.append("[clocktool]")
    lines.append(f"    clock = {clock}")
    lines.append(f"    multiply = {multiply_expr}")
    lines.append(f"    output = {output}")

    return "\n".join(lines)
