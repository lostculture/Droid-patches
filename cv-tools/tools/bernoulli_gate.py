"""
Bernoulli Gate — Probabilistic Gate Router for DROID

Inspired by Mutable Instruments Branches, this module randomly routes each
incoming gate to one of two outputs based on a probability control.

At probability 0.0 all gates go to output A. At 1.0 all gates go to output B.
At 0.5 (the default) it is a fair coin flip.

DROID circuit: [bernoulli]
"""

TOOL_META = {
    "name": "bernoulli_gate",
    "description": "Probabilistic gate router (coin-flip gate splitter)",
    "doepfer": "N/A",
    "inspired_by": "MI Branches",
    "required_inputs": ["gate"],
    "optional_inputs": [],
    "required_outputs": ["output_a"],
    "optional_outputs": ["output_b"],
    "required_controls": [],
    "optional_controls": ["probability"],
}

_DEFAULT_PROBABILITY = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a Bernoulli gate instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for comment labels.
    inputs : dict
        Must contain ``"gate"`` mapped to a hardware jack or internal cable
        (e.g. ``{"gate": "I1"}``).
    outputs : dict
        Must contain ``"output_a"`` mapped to a hardware jack or internal
        cable.  May optionally contain ``"output_b"`` for the second output
        channel.
    controls : dict
        Optional keys:

        - ``"probability"`` — pot or CV controlling the routing probability.
          0.0 sends all gates to output A, 1.0 sends all gates to output B,
          0.5 (default) is a fair coin flip.

    Returns
    -------
    str
        DROID .ini circuit block for the Bernoulli gate.
    """
    gate = inputs["gate"]
    output_a = outputs["output_a"]
    output_b = outputs.get("output_b")
    probability = controls.get("probability", _DEFAULT_PROBABILITY)

    lines = [f"# {name}: Bernoulli Gate (MI Branches)"]
    lines.append("[bernoulli]")
    lines.append(f"    input = {gate}")
    lines.append(f"    distribution = {probability}")
    lines.append(f"    output1 = {output_a}")

    if output_b:
        lines.append(f"    output2 = {output_b}")

    return "\n".join(lines)
