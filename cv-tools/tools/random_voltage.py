"""
Random Voltage Source — Doepfer A-149

Generates random CV voltages in two modes:

1. **Stepped random** — produces a new random value on each trigger,
   equivalent to a sample-and-hold on a noise source.
2. **Smooth random** — a continuously fluctuating random CV created by
   slewing a random source, giving organic, slowly-drifting modulation.

DROID circuits: [random] (stepped and raw smooth), [slew] (smooth output)
"""

TOOL_META = {
    "name": "random_voltage",
    "description": "Stepped and smooth random CV generator",
    "doepfer": "A-149",
    "required_inputs": [],
    "optional_inputs": ["trigger"],
    "required_outputs": [],
    "optional_outputs": ["stepped", "smooth"],
    "required_controls": [],
    "optional_controls": ["rate", "range"],
}

_DEFAULT_RATE = 0.3
_DEFAULT_RANGE = 1
_DEFAULT_SLEW = 0.5


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a random voltage source.

    Parameters
    ----------
    name : str
        Instance name, used to prefix internal cable names.
    inputs : dict
        May contain ``"trigger"`` mapped to a hardware jack or internal
        cable.  When provided, the stepped random circuit fires on each
        trigger edge.
    outputs : dict
        May contain ``"stepped"`` and/or ``"smooth"``, each mapped to a
        hardware jack or internal cable.  Only circuits required for the
        requested outputs are emitted.
    controls : dict
        Optional keys:

        - ``"rate"`` — pot or CV controlling the smooth random's
          fluctuation speed (also used as internal clock rate for the
          stepped random when no trigger is supplied).
        - ``"range"`` — pot or CV controlling the maximum output voltage
          (minimum is always 0).

    Returns
    -------
    str
        DROID .ini circuit blocks for the requested random outputs.
    """
    prefix = f"_{name.upper()}"
    lines = []

    trigger = inputs.get("trigger")
    stepped_out = outputs.get("stepped")
    smooth_out = outputs.get("smooth")

    rate = controls.get("rate")
    range_ctrl = controls.get("range")

    maximum = range_ctrl if range_ctrl else _DEFAULT_RANGE

    # --- Stepped random output ---
    if stepped_out:
        lines.append(f"# {name}: stepped random (A-149)")
        lines.append("[random]")
        if trigger:
            lines.append(f"    trigger = {trigger}")
            lines.append(f"    clock = {trigger}")
        lines.append(f"    minimum = 0")
        lines.append(f"    maximum = {maximum}")
        lines.append(f"    output = {stepped_out}")

    # --- Smooth random output ---
    if smooth_out:
        if lines:
            lines.append("")
        raw_cable = f"{prefix}_RAND_RAW"
        rate_value = rate if rate else _DEFAULT_RATE

        lines.append(f"# {name}: smooth random source (A-149)")
        lines.append("[random]")
        lines.append(f"    rate = {rate_value}")
        lines.append(f"    minimum = 0")
        lines.append(f"    maximum = {maximum}")
        lines.append(f"    output = {raw_cable}")
        lines.append("")
        lines.append(f"# {name}: slew for smooth random")
        lines.append("[slew]")
        lines.append(f"    input = {raw_cable}")
        lines.append(f"    slewup = {_DEFAULT_SLEW}")
        lines.append(f"    slewdown = {_DEFAULT_SLEW}")
        lines.append(f"    output = {smooth_out}")

    return "\n".join(lines)
