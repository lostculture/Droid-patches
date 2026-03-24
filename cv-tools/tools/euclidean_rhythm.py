"""
Euclidean Rhythm Generator — Distribute N hits evenly across M steps

Uses the Bjorklund/Euclidean algorithm to space active beats as evenly
as possible within a pattern of a given length.  For example, 3 hits in
8 steps produces the classic tresillo pattern [x..x..x.].

When a *hits* control (pot) is provided, the 0-1 range is mapped to
1-16 via ``hits * 15 + 1``.  The same scaling applies to the *steps*
control.  The *rotation* control is passed through directly (the
[euklid] circuit interprets 0-1 as a fractional offset).

A reset button is handled identically to the clock_divider module:
a [button] circuit is created and its output is merged with any
external reset input using [copy].

DROID circuit: [euklid]
"""

TOOL_META = {
    "name": "euclidean_rhythm",
    "description": "Euclidean rhythm generator (N hits in M steps)",
    "doepfer": "N/A",
    "inspired_by": "Various Euclid modules, NE Numeric Repetitor",
    "required_inputs": ["clock"],
    "optional_inputs": ["reset"],
    "required_outputs": ["gate"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["hits", "steps", "rotation", "reset_btn", "reset_led"],
}

_DEFAULT_BEATS = 3
_DEFAULT_LENGTH = 8
_DEFAULT_OFFSET = 0


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a Euclidean rhythm generator instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"clock"`` mapped to a hardware jack or internal
        cable.  May contain ``"reset"`` for an external reset signal.
    outputs : dict
        Must contain ``"gate"`` mapped to a hardware jack or internal
        cable.
    controls : dict
        Optional keys:

        - ``"hits"`` — a pot or fixed value controlling active beats.
          When a pot (0-1 range) is provided, the value is scaled via
          ``hits * 15 + 1`` to map the full range to 1-16 beats.
          If omitted, defaults to 3.
        - ``"steps"`` — a pot or fixed value controlling the pattern
          length.  When a pot (0-1 range) is provided, the value is
          scaled via ``steps * 15 + 1`` to map the full range to 1-16
          steps.  If omitted, defaults to 8.
        - ``"rotation"`` — a pot or fixed value controlling pattern
          rotation / offset.  Passed directly to the circuit.
          If omitted, defaults to 0.
        - ``"reset_btn"`` — a button jack for manual reset.
        - ``"reset_led"`` — an LED jack for the reset button.

    Returns
    -------
    str
        DROID .ini text for the [euklid] circuit (and any supporting
        circuits for reset handling).
    """
    lines = []
    prefix = f"_{name.upper()}"

    clock = inputs["clock"]
    gate = outputs["gate"]

    reset_input = inputs.get("reset")
    hits_ctrl = controls.get("hits")
    steps_ctrl = controls.get("steps")
    rotation_ctrl = controls.get("rotation")
    reset_btn = controls.get("reset_btn")
    reset_led = controls.get("reset_led")

    # --- Reset button (if provided) ---
    has_reset_btn = reset_btn is not None
    if has_reset_btn:
        lines.append(f"# {name}: reset button")
        lines.append("[button]")
        lines.append(f"    button = {reset_btn}")
        lines.append("    states = 1")
        if reset_led:
            lines.append(f"    led = {reset_led}")
        lines.append(f"    output = {prefix}_RESET_BTN")
        lines.append("")

    # --- Combine reset sources ---
    has_reset_input = reset_input is not None
    if has_reset_btn and has_reset_input:
        lines.append(f"# {name}: merge reset sources")
        lines.append("[copy]")
        lines.append(f"    input = {reset_input} + {prefix}_RESET_BTN")
        lines.append(f"    output = {prefix}_RESET")
        lines.append("")
        reset_signal = f"{prefix}_RESET"
    elif has_reset_btn:
        reset_signal = f"{prefix}_RESET_BTN"
    elif has_reset_input:
        reset_signal = reset_input
    else:
        reset_signal = None

    # --- Hits (beats) ---
    # Pot 0-1 maps to 1-16: beats = pot * 15 + 1
    if hits_ctrl is not None:
        beats_expr = f"{hits_ctrl} * 15 + 1"
    else:
        beats_expr = _DEFAULT_BEATS

    # --- Steps (length) ---
    # Pot 0-1 maps to 1-16: length = pot * 15 + 1
    if steps_ctrl is not None:
        length_expr = f"{steps_ctrl} * 15 + 1"
    else:
        length_expr = _DEFAULT_LENGTH

    # --- Rotation (offset) ---
    # Passed directly; the circuit interprets 0-1 as fractional offset.
    if rotation_ctrl is not None:
        offset_expr = rotation_ctrl
    else:
        offset_expr = _DEFAULT_OFFSET

    # --- Euclidean rhythm circuit ---
    lines.append(f"# {name}: Euclidean rhythm generator")
    lines.append("[euklid]")
    lines.append(f"    clock = {clock}")
    if reset_signal:
        lines.append(f"    reset = {reset_signal}")
    lines.append(f"    beats = {beats_expr}")
    lines.append(f"    length = {length_expr}")
    lines.append(f"    offset = {offset_expr}")
    lines.append(f"    output = {gate}")

    return "\n".join(lines)
