"""
Quadrature LFO — Doepfer A-143-9 Quadrature LFO for DROID

Produces four LFO outputs at 0, 90, 180, and 270 degree phase offsets,
all sharing the same rate.  Useful for spatial effects, complex cross-
modulation, panning, and any scenario that benefits from smooth,
phase-shifted modulation sources.

DROID circuits: [lfo] (sine + cosine) and [copy] (inversion for 180/270).
The sine output gives 0 degrees, cosine gives 90 degrees, and their
inversions provide 180 and 270 degrees respectively.
"""

TOOL_META = {
    "name": "quad_lfo",
    "description": "Quadrature LFO with 4 phase-shifted outputs",
    "doepfer": "A-143-9",
    "required_inputs": [],
    "optional_inputs": ["sync"],
    "required_outputs": [],
    "optional_outputs": ["phase_0", "phase_90", "phase_180", "phase_270"],
    "required_controls": [],
    "optional_controls": ["rate"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a quadrature LFO instance.

    Parameters
    ----------
    name : str
        Instance name, used to prefix internal cable names.
    inputs : dict
        May contain ``"sync"`` mapped to a hardware jack or internal
        cable for hard-syncing the LFO phase.
    outputs : dict
        Any combination of ``"phase_0"``, ``"phase_90"``, ``"phase_180"``,
        and ``"phase_270"`` mapped to hardware jacks or internal cables.
    controls : dict
        May contain ``"rate"`` (a pot or CV source).  When provided the
        LFO frequency is ``rate * 5 + 0.1`` Hz.  When absent the LFO
        runs at a fixed 1 Hz.

    Returns
    -------
    str
        DROID .ini circuit blocks for the quadrature LFO.
    """
    prefix = f"_{name}"

    sync = inputs.get("sync")
    rate = controls.get("rate")

    phase_0_out = outputs.get("phase_0")
    phase_90_out = outputs.get("phase_90")
    phase_180_out = outputs.get("phase_180")
    phase_270_out = outputs.get("phase_270")

    # Determine hz expression
    if rate:
        hz_expr = f"{rate} * 5 + 0.1"
    else:
        hz_expr = "1"

    # --- LFO core: produces sine (0°) and cosine (90°) ---
    lines = [
        f"# {name}: Quadrature LFO (A-143-9)",
        f"# 0°=sine  90°=cosine  180°=-sine  270°=-cosine",
        "",
        "[lfo]",
        f"    hz = {hz_expr}",
    ]

    if sync:
        lines.append(f"    sync = {sync}")

    lines += [
        f"    sine = {prefix}_SIN",
        f"    cosine = {prefix}_COS",
    ]

    # --- Copy blocks for each requested output ---

    if phase_0_out:
        lines += [
            "",
            f"# 0° phase output (sine)",
            "[copy]",
            f"    input = {prefix}_SIN",
            f"    output = {phase_0_out}",
        ]

    if phase_90_out:
        lines += [
            "",
            f"# 90° phase output (cosine)",
            "[copy]",
            f"    input = {prefix}_COS",
            f"    output = {phase_90_out}",
        ]

    if phase_180_out:
        lines += [
            "",
            f"# 180° phase output (inverted sine)",
            "[copy]",
            f"    input = -1 * {prefix}_SIN + 1",
            f"    output = {phase_180_out}",
        ]

    if phase_270_out:
        lines += [
            "",
            f"# 270° phase output (inverted cosine)",
            "[copy]",
            f"    input = -1 * {prefix}_COS + 1",
            f"    output = {phase_270_out}",
        ]

    return "\n".join(lines)
