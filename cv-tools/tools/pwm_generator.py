"""
PWM Generator — Doepfer A-168 PWM Module for DROID

Generates a pulse/square wave with variable pulse width.  The pulse width
can be modulated by a CV input, creating classic PWM effects.  Useful as
a modulation source or for generating gates with specific duty cycles.

DROID circuit: [lfo] with the ``pulsewidth`` parameter controlling the
duty cycle of the square output (0.5 = standard square, lower = narrower
pulse, higher = wider pulse).
"""

TOOL_META = {
    "name": "pwm_generator",
    "description": "Variable pulse width generator with CV modulation",
    "doepfer": "A-168",
    "required_inputs": [],
    "optional_inputs": ["pw_cv"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["rate", "pulse_width"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a PWM generator instance.

    Parameters
    ----------
    name : str
        Instance name, used in the comment header.
    inputs : dict
        May contain ``"pw_cv"`` mapped to a hardware jack or internal
        cable that modulates the pulse width.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable that receives the pulse/square wave.
    controls : dict
        May contain ``"rate"`` (a pot or CV source) to set the LFO
        frequency (scaled as ``rate * 10 + 0.1`` Hz; defaults to 1 Hz),
        and ``"pulse_width"`` (a pot or CV source) for the base duty
        cycle (defaults to 0.5 = standard square).

    Returns
    -------
    str
        DROID .ini circuit block for the PWM generator.
    """
    pw_cv = inputs.get("pw_cv")
    output = outputs["output"]
    rate = controls.get("rate")
    pulse_width = controls.get("pulse_width")

    # Determine hz expression
    if rate:
        hz_expr = f"{rate} * 10 + 0.1"
    else:
        hz_expr = "1"

    # Determine pulsewidth expression
    if pulse_width and pw_cv:
        pw_expr = f"{pulse_width} + {pw_cv}"
    elif pulse_width:
        pw_expr = pulse_width
    elif pw_cv:
        pw_expr = f"0.5 + {pw_cv}"
    else:
        pw_expr = "0.5"

    lines = [
        f"# {name}: PWM Generator (A-168)",
        f"# pulsewidth 0.5 = square, <0.5 = narrow, >0.5 = wide",
        "",
        "[lfo]",
        f"    hz = {hz_expr}",
        f"    pulsewidth = {pw_expr}",
        f"    square = {output}",
    ]

    return "\n".join(lines)
