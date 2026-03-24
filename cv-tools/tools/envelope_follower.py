"""
Envelope Follower — Doepfer A-119 / Bastl Dynamo

Extracts the amplitude envelope from an incoming signal.  Uses fast
attack to track peaks and slow release for a smooth follower curve.
Converts dynamic signals (audio-rate CV, LFOs, complex modulation)
into smooth CV envelopes.

Implementation:
  1. Full-wave rectify the input (absolute value via [compare]).
  2. Apply asymmetric slew — fast rise (attack) to track peaks,
     slow fall (release) for a smooth decay.

If attack/release controls are provided they are used directly;
otherwise sensible defaults are applied (very fast attack ~0.05,
moderate release ~0.7).

Internal cables use the ``_{name}_`` prefix convention.
"""

TOOL_META = {
    "name": "envelope_follower",
    "description": "Extract amplitude envelope from signal (peak tracking)",
    "doepfer": "A-119",
    "inspired_by": "Bastl Dynamo",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["attack", "release"],
}

_DEFAULT_ATTACK = 0.05
_DEFAULT_RELEASE = 0.7


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for an envelope follower.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" mapped to a hardware jack or cable.
        outputs:  Dict with "output" mapped to a hardware jack or cable.
        controls: Dict with optionally "attack" and/or "release".
                  - "attack"  controls the rise slew (peak tracking speed).
                  - "release" controls the fall slew (envelope decay speed).

    Returns:
        A string containing the DROID circuit blocks.
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]

    attack = controls.get("attack", _DEFAULT_ATTACK)
    release = controls.get("release", _DEFAULT_RELEASE)

    rectified_cable = f"_{name}_RECTIFIED"

    lines = [
        f"# {name}: Envelope Follower (A-119 / Bastl Dynamo)",
        "",
        "# Rectify: full-wave (absolute value) of input signal",
        "[compare]",
        f"    input = {cv_in}",
        "    compare = 0",
        f"    ifgreater = {cv_in}",
        f"    ifless = -1 * {cv_in}",
        "    ifequal = 0",
        f"    output = {rectified_cable}",
        "",
        "# Slew: fast attack (track peaks), slow release (smooth decay)",
        "[slew]",
        f"    input = {rectified_cable}",
        f"    slewup = {attack}",
        f"    slewdown = {release}",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
