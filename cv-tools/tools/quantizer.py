"""
Quantizer — Doepfer A-156 Dual Quantizer

Quantizes a continuous CV input to musical scale degrees using the DROID
[minifonion] circuit.  Supports root note selection (C through B) and
multiple scale types including major, minor, modes, pentatonic, and blues.

Root and scale can be set by pots (scaled from 0-1 to the valid integer
range) or left at defaults (root = C, scale = Major).  An optional trigger
input gates when quantization occurs — without it, the input is quantized
continuously.

Scale degree reference (minifonion):
    0 = Chromatic        1 = Major           2 = Dorian
    3 = Phrygian         4 = Lydian          5 = Mixolydian
    6 = Minor            7 = Locrian         8 = Whole Tone
   11 = Minor Blues     12 = Minor Penta    13 = Major Penta
   14 = Harmonic Minor  15 = Melodic Minor

DROID circuit: [minifonion]
"""

TOOL_META = {
    "name": "quantizer",
    "description": "Musical scale quantizer with root and scale selection",
    "doepfer": "A-156",
    "required_inputs": ["input"],
    "optional_inputs": ["trigger"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["root", "scale"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a musical scale quantizer.

    Parameters
    ----------
    name : str
        Instance name, used for cable prefixes.
    inputs : dict
        Must contain ``"input"`` mapped to a hardware jack or internal cable.
        Optionally ``"trigger"`` to gate when quantization happens.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal cable.
    controls : dict
        Optionally ``"root"`` (pot selecting root note, 0-1 mapped to 0-11)
        and/or ``"scale"`` (pot selecting scale type, 0-1 mapped to 0-15).

    Returns
    -------
    str
        DROID .ini circuit block.
    """
    cv_in = inputs["input"]
    trigger = inputs.get("trigger")
    cv_out = outputs["output"]

    root_pot = controls.get("root")
    scale_pot = controls.get("scale")

    # Build root expression: pot 0-1 scaled to 0-11, or default 0 (C)
    root_expr = f"{root_pot} * 11" if root_pot else "0"

    # Build degree expression: pot 0-1 scaled to 0-15, or default 1 (Major)
    degree_expr = f"{scale_pot} * 15" if scale_pot else "1"

    lines = [
        f"# {name}: Quantizer (A-156)",
    ]

    if root_pot and scale_pot:
        lines.append(f"# Root: {root_pot} (0-11), Scale: {scale_pot} (0-15)")
    elif root_pot:
        lines.append(f"# Root: {root_pot} (0-11), Scale: Major (fixed)")
    elif scale_pot:
        lines.append(f"# Root: C (fixed), Scale: {scale_pot} (0-15)")
    else:
        lines.append("# Root: C (fixed), Scale: Major (fixed)")

    lines += [
        "",
        "[minifonion]",
        f"    input = {cv_in}",
    ]

    if trigger:
        lines.append(f"    trigger = {trigger}")

    lines += [
        f"    root = {root_expr}",
        f"    degree = {degree_expr}",
        "    select1 = 1",
        "    select3 = 1",
        "    select5 = 1",
        "    select7 = 1",
        "    select9 = 1",
        "    select11 = 1",
        "    select13 = 1",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
