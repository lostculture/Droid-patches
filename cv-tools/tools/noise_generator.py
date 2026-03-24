"""
Noise Generator — Continuous Random CV Source

Generates a continuously varying random noise CV output.  Unlike the
random_voltage tool (which produces stepped or smoothed random values on
triggers), this provides a free-running noise source — an always-moving
random signal suitable for injecting organic variation into patches.

DROID circuit: [random] in free-running mode (no trigger / clock).

Inspired by the Doepfer A-118 Noise / Random Voltage generator.
"""

TOOL_META = {
    "name": "noise_generator",
    "description": "Continuous random noise CV source",
    "doepfer": "N/A",
    "inspired_by": "Doepfer A-118 Noise, general utility",
    "required_inputs": [],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["rate", "range"],
}

_DEFAULT_RATE = 1
_DEFAULT_RANGE = 1


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a continuous noise generator.

    Parameters
    ----------
    name : str
        Instance name, used in the comment header.
    inputs : dict
        Not used — the noise generator has no inputs.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable that receives the continuous random CV.
    controls : dict
        Optional keys:

        - ``"rate"`` — pot or CV controlling the fluctuation speed of the
          random output.  Higher values produce faster movement.
          Defaults to 1.
        - ``"range"`` — pot or CV controlling the maximum output voltage
          (minimum is always 0).  Defaults to 1.

    Returns
    -------
    str
        DROID .ini circuit block for the noise generator.
    """
    output = outputs["output"]
    rate = controls.get("rate", _DEFAULT_RATE)
    range_ctrl = controls.get("range", _DEFAULT_RANGE)

    lines = [
        f"# {name}: continuous noise generator (A-118 style)",
        "",
        "[random]",
        f"    rate = {rate}",
        f"    minimum = 0",
        f"    maximum = {range_ctrl}",
        f"    output = {output}",
    ]

    return "\n".join(lines)
