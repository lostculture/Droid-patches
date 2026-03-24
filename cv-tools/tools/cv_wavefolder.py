"""
CV Wavefolder — Intellijel uFold / Joranalogue Fold 6 (CV domain)

Fold a CV signal back on itself for complex waveshaping.  A wavefolder
"reflects" a signal when it exceeds a threshold — instead of clipping or
wrapping, the value bounces back, creating complex shapes from simple
inputs.  Multiple folds create increasingly intricate modulation patterns
from a single LFO or envelope.

**fold_amount** controls how much the input is amplified before folding.
Higher values push the signal further past the fold boundaries, producing
more bounces.  The pot range 0–1 is mapped to 1x–5x gain:
    gain = fold_amount * 4 + 1

If no fold_amount control is provided, a default gain of 2 is applied
(one fold for a full-range signal).

**symmetry** adds a DC offset before folding, shifting the fold centre
so the positive and negative halves of the waveform fold at different
points.  The offset can come from a CV input (``symmetry``), a pot
(``symmetry_knob``), or both summed together.

Implementation uses two DROID circuits:

1. ``[copy]`` — scales the input by the fold gain and adds any symmetry
   offset, writing the result to an internal cable.
2. ``[fold]`` — folds the amplified signal between ``low = 0`` and
   ``high = 1``.  When the value exceeds 1 it bounces back toward 0,
   and when it drops below 0 it bounces back toward 1, exactly like a
   hardware wavefolder.
"""

TOOL_META = {
    "name": "cv_wavefolder",
    "description": "Fold CV signal back on itself for complex waveshaping",
    "doepfer": "N/A",
    "inspired_by": "Intellijel uFold, Joranalogue Fold 6",
    "required_inputs": ["input"],
    "optional_inputs": ["symmetry"],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["fold_amount", "symmetry_knob"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for a CV wavefolder.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" mapped to a jack or cable.
                  May also contain "symmetry" (CV offset input).
        outputs:  Dict with "output" mapped to a jack or cable.
        controls: Dict with optionally "fold_amount" (pot/CV for gain)
                  and/or "symmetry_knob" (pot for DC offset).

    Returns:
        A string containing the DROID circuit blocks.
    """
    cv_in = inputs["input"]
    cv_out = outputs["output"]
    symmetry_cv = inputs.get("symmetry")
    fold_amount = controls.get("fold_amount")
    symmetry_knob = controls.get("symmetry_knob")

    # --- Build the gain expression ---
    # fold_amount pot 0-1 maps to gain 1x-5x: fold_amount * 4 + 1
    # No fold_amount defaults to gain 2 (one fold for full-range signal)
    if fold_amount:
        gain_expr = f"{cv_in} * ({fold_amount} * 4 + 1)"
    else:
        gain_expr = f"{cv_in} * 2"

    # --- Build the symmetry offset expression ---
    # Combine CV input and knob if both present, or use whichever is provided
    if symmetry_cv and symmetry_knob:
        offset_expr = f"{symmetry_cv} + {symmetry_knob}"
    elif symmetry_cv:
        offset_expr = symmetry_cv
    elif symmetry_knob:
        offset_expr = symmetry_knob
    else:
        offset_expr = None

    # --- Combine gain and offset into the amplified expression ---
    if offset_expr:
        amplified_expr = f"{gain_expr} + {offset_expr}"
    else:
        amplified_expr = gain_expr

    # Internal cable for the amplified/offset signal
    amplified_cable = f"_{name}_AMPLIFIED"

    # --- Build the header comment ---
    lines = [f"# {name}: CV Wavefolder (uFold / Fold 6)"]

    if fold_amount:
        lines.append(f"# Fold amount: {fold_amount} (0=clean, 1=heavy folding)")
    else:
        lines.append("# Fold amount: fixed gain 2x (default)")

    if symmetry_cv and symmetry_knob:
        lines.append(f"# Symmetry offset: {symmetry_cv} + {symmetry_knob}")
    elif symmetry_cv:
        lines.append(f"# Symmetry offset: CV via {symmetry_cv}")
    elif symmetry_knob:
        lines.append(f"# Symmetry offset: knob via {symmetry_knob}")

    # --- Amplify input (more gain = more folds) ---
    lines += [
        "",
        "# Amplify input — higher gain pushes signal past fold boundaries",
        "[copy]",
        f"    input = {amplified_expr}",
        f"    output = {amplified_cable}",
    ]

    # --- Fold the amplified signal between 0 and 1 ---
    lines += [
        "",
        "# Fold between 0 and 1 — signal bounces back at boundaries",
        "[fold]",
        f"    input = {amplified_cable}",
        "    low = 0",
        "    high = 1",
        f"    output = {cv_out}",
    ]

    return "\n".join(lines)
