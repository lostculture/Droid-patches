"""
Slew Limiter — Doepfer A-170 Dual Slew Limiter for DROID

Smooths CV transitions with independent rise and fall times.
Use for portamento/glide, envelope smoothing, or converting gates
into simple attack-release envelopes.

DROID circuit: [slew]
"""

TOOL_META = {
    "name": "slew_limiter",
    "description": "Slew limiter with independent rise/fall times",
    "doepfer": "A-170",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["rise", "fall", "slew"],
}

_DEFAULT_SLEW = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a slew limiter instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain "input" mapped to a hardware jack or internal cable.
    outputs : dict
        Must contain "output" mapped to a hardware jack or internal cable.
    controls : dict
        Optional keys: "rise", "fall", "slew".
        - If "rise" and "fall" are both provided, they control ascent and
          descent independently.
        - If only "slew" is provided, it drives both slewup and slewdown.
        - If none are provided, both default to 0.5.

    Returns
    -------
    str
        DROID .ini text for the [slew] circuit.
    """
    input_sig = inputs["input"]
    output_sig = outputs["output"]

    has_rise = "rise" in controls
    has_fall = "fall" in controls
    has_slew = "slew" in controls

    # Determine slewup and slewdown values
    if has_rise and has_fall:
        slewup = controls["rise"]
        slewdown = controls["fall"]
    elif has_slew:
        slewup = controls["slew"]
        slewdown = controls["slew"]
    elif has_rise:
        # Only rise provided — use it for rise, default for fall
        slewup = controls["rise"]
        slewdown = _DEFAULT_SLEW
    elif has_fall:
        # Only fall provided — default for rise, use it for fall
        slewup = _DEFAULT_SLEW
        slewdown = controls["fall"]
    else:
        slewup = _DEFAULT_SLEW
        slewdown = _DEFAULT_SLEW

    lines = [
        f"[slew]",
        f"    input = {input_sig}",
        f"    slewup = {slewup}",
        f"    slewdown = {slewdown}",
        f"    output = {output_sig}",
    ]

    return "\n".join(lines)
