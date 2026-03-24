"""
Attenuverter — Doepfer A-133 Dual VC Polarizer

Attenuate, invert, and offset a CV signal using a single [copy] circuit.
The amount control is bipolar: center = silence, CW = full positive,
CCW = fully inverted.
"""

TOOL_META = {
    "name": "attenuverter",
    "description": "Attenuate, invert, and offset CV signals",
    "doepfer": "A-133",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": ["amount"],
    "optional_controls": ["offset"],
}


def render(name, inputs, outputs, controls):
    """Render a DROID .ini block for a bipolar attenuverter.

    Args:
        name:     Instance name, used as cable prefix.
        inputs:   Dict with at least "input" mapped to a jack or cable.
        outputs:  Dict with at least "output" mapped to a jack or cable.
        controls: Dict with "amount" (required) and optionally "offset".

    Returns:
        A string containing the DROID [copy] circuit block.
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]
    amount = controls["amount"]
    offset = controls.get("offset")

    # Build the input expression:
    #   input * (2 * amount_pot - 1)        — bipolar scaling
    #   ... + offset                        — optional DC offset
    expr = f"{cv_in} * (2 * {amount} - 1)"
    if offset:
        expr += f" + {offset}"

    lines = [
        "# Attenuverter: scale input from -1x to +1x with optional offset",
        "# amount pot center = zero, CW = positive, CCW = inverted",
        "",
        "[copy]",
        f"    input = {expr}",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
