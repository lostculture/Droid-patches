"""
Burst Generator — Rapid trigger burst from a single input trigger

Receives a single trigger and outputs a configurable number of rapid
triggers (2-16).  Useful for ratcheting effects, drum fills, and
generative rhythms.  The burst count and speed can be CV-controlled.

When a count control (pot) is provided, the 0-1 range is mapped to
1-16 triggers via ``count * 15 + 1``.  When a rate control is provided,
it is passed directly to set the burst speed.

DROID circuit: [burst]
"""

TOOL_META = {
    "name": "burst_generator",
    "description": "Generate burst of rapid triggers from single input trigger",
    "doepfer": "N/A",
    "inspired_by": "Befaco Rampage, general utility",
    "required_inputs": ["trigger"],
    "optional_inputs": [],
    "required_outputs": ["output"],
    "optional_outputs": [],
    "required_controls": [],
    "optional_controls": ["count", "rate"],
}

_DEFAULT_COUNT = 4
_DEFAULT_RATE = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a burst generator instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"trigger"`` mapped to a hardware jack or internal
        cable.
    outputs : dict
        Must contain ``"output"`` mapped to a hardware jack or internal
        cable.
    controls : dict
        Optional keys:

        - ``"count"`` — a pot or fixed value controlling how many triggers
          are emitted per burst.  When a pot (0-1 range) is provided, the
          value is scaled via ``count * 15 + 1`` to map the full pot range
          to 1-16 triggers.  If omitted, defaults to 4 triggers.
        - ``"rate"`` — a pot or fixed value controlling the speed of the
          burst triggers.  If omitted, defaults to 0.5.

    Returns
    -------
    str
        DROID .ini text for the [burst] circuit.
    """
    trigger_sig = inputs["trigger"]
    output_sig = outputs["output"]

    count_ctrl = controls.get("count")
    rate_ctrl = controls.get("rate")

    # Build the count expression: scale pot 0-1 to 1-16 if a control is
    # provided, otherwise use the fixed default.
    if count_ctrl is not None:
        count_value = f"{count_ctrl} * 15 + 1"
    else:
        count_value = _DEFAULT_COUNT

    rate_value = rate_ctrl if rate_ctrl is not None else _DEFAULT_RATE

    lines = [
        f"# {name}: Burst Generator",
        "[burst]",
        f"    trigger = {trigger_sig}",
        f"    count = {count_value}",
        f"    rate = {rate_value}",
        f"    output = {output_sig}",
    ]

    return "\n".join(lines)
