"""
Window Comparator — Joranalogue Compare 2

Two thresholds define a voltage window.  The main output gate is HIGH only
when the input falls *between* the low and high thresholds.  More expressive
than a single comparator — can detect specific voltage ranges, creating
bandpass-like behaviour for gates.

Optional outputs signal when the input is above the window (``above``) or
below it (``below``), giving three mutually-exclusive zones.

Two parameter modes:
  1. **Low/High thresholds** — set ``low_threshold`` and/or ``high_threshold``
     directly.  Defaults: 0.25 and 0.75.
  2. **Center/Width** — set ``center`` and ``width``; these are converted to
     low = center - width/2, high = center + width/2.  If both modes are
     supplied, low/high thresholds take priority.

DROID circuits: [compare], [logic], [copy]
"""

TOOL_META = {
    "name": "window_comparator",
    "description": "Gate high when input is within a voltage window (low-high range)",
    "doepfer": "N/A",
    "inspired_by": "Joranalogue Compare 2",
    "required_inputs": ["input"],
    "optional_inputs": [],
    "required_outputs": ["in_window"],
    "optional_outputs": ["above", "below"],
    "required_controls": [],
    "optional_controls": ["low_threshold", "high_threshold", "center", "width"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a window comparator instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"input"`` mapped to a hardware jack or internal cable.
    outputs : dict
        Must contain ``"in_window"``.  May contain ``"above"`` (gate when
        input > high threshold) and/or ``"below"`` (gate when input < low
        threshold).
    controls : dict
        May contain ``"low_threshold"`` and ``"high_threshold"`` for direct
        threshold control, or ``"center"`` and ``"width"`` as an alternative
        parameterisation.  If neither is given, defaults are 0.25 / 0.75.

    Returns
    -------
    str
        DROID .ini circuit text.
    """
    cv_in = inputs["input"]
    in_window_out = outputs["in_window"]
    above_out = outputs.get("above")
    below_out = outputs.get("below")

    prefix = f"_{name}_"

    # --- Resolve thresholds ------------------------------------------
    low_threshold = controls.get("low_threshold")
    high_threshold = controls.get("high_threshold")
    center = controls.get("center")
    width = controls.get("width")

    # Center/width mode: only used when explicit low/high are absent
    if center and width and not low_threshold and not high_threshold:
        # DROID cannot compute inline arithmetic across two pots, so we
        # materialise the thresholds via [copy] math blocks.
        low_cable = f"{prefix}LOW_THRESH"
        high_cable = f"{prefix}HIGH_THRESH"
        use_computed = True
    else:
        low_cable = low_threshold or "0.25"
        high_cable = high_threshold or "0.75"
        use_computed = False

    above_low_cable = f"{prefix}ABOVE_LOW"
    below_high_cable = f"{prefix}BELOW_HIGH"

    lines = [
        f"# {name}: Window Comparator (Joranalogue Compare 2)",
    ]

    # --- Optional: centre/width -> low/high conversion ---------------
    if use_computed:
        lines += [
            f"# Compute low threshold = center - width/2",
            "[copy]",
            f"    input = {center} - {width} * 0.5",
            f"    output = {low_cable}",
            "",
            f"# Compute high threshold = center + width/2",
            "[copy]",
            f"    input = {center} + {width} * 0.5",
            f"    output = {high_cable}",
            "",
        ]

    # --- Compare: input > low threshold? -----------------------------
    lines += [
        f"# Check if input >= low threshold",
        "[compare]",
        f"    input = {cv_in}",
        f"    compare = {low_cable}",
        "    ifgreater = 1",
        "    ifless = 0",
        "    ifequal = 1",
        f"    output = {above_low_cable}",
    ]

    # --- Compare: input < high threshold? ----------------------------
    lines += [
        "",
        f"# Check if input <= high threshold",
        "[compare]",
        f"    input = {cv_in}",
        f"    compare = {high_cable}",
        "    ifgreater = 0",
        "    ifless = 1",
        "    ifequal = 1",
        f"    output = {below_high_cable}",
    ]

    # --- AND: both conditions = within window ------------------------
    lines += [
        "",
        f"# AND: both conditions met = input is within window",
        "[logic]",
        f"    input1 = {above_low_cable}",
        f"    input2 = {below_high_cable}",
        f"    and = {in_window_out}",
    ]

    # --- Optional output: above (input > high threshold) -------------
    if above_out:
        lines += [
            "",
            f"# Above window: gate when input > high threshold",
            "[copy]",
            f"    input = -1 * {below_high_cable} + 1",
            f"    output = {above_out}",
        ]

    # --- Optional output: below (input < low threshold) --------------
    if below_out:
        lines += [
            "",
            f"# Below window: gate when input < low threshold",
            "[copy]",
            f"    input = -1 * {above_low_cable} + 1",
            f"    output = {below_out}",
        ]

    return "\n".join(lines)
