"""
Quad Decay — Doepfer A-142-4 Quad Decay Envelope for DROID

Four independent decay envelope generators, each triggered by its own
gate input.  Each produces a simple attack=0, decay envelope.  Useful
for percussion, trigger-to-CV conversion, and as simple envelopes.

DROID circuit: [contour] (one per active channel)
"""

TOOL_META = {
    "name": "quad_decay",
    "description": "Four independent decay envelope generators",
    "doepfer": "A-142-4",
    "required_inputs": ["trigger1"],
    "optional_inputs": ["trigger2", "trigger3", "trigger4"],
    "required_outputs": ["env1"],
    "optional_outputs": ["env2", "env3", "env4"],
    "required_controls": [],
    "optional_controls": ["decay1", "decay2", "decay3", "decay4", "decay_all"],
}

_DEFAULT_DECAY = 0.5
_CHANNELS = [1, 2, 3, 4]


def render(name, inputs, outputs, controls):
    """Render DROID .ini text for a quad decay envelope instance.

    Parameters
    ----------
    name : str
        Instance name, used as a prefix for internal cable names.
    inputs : dict
        Must contain ``"trigger1"``.  May also contain ``"trigger2"``,
        ``"trigger3"``, ``"trigger4"`` for additional channels.
    outputs : dict
        Must contain ``"env1"``.  May also contain ``"env2"``, ``"env3"``,
        ``"env4"`` for additional channels.
    controls : dict
        Optional keys:

        - ``"decay1"`` .. ``"decay4"`` — per-channel decay time (pot or
          fixed value).
        - ``"decay_all"`` — shared decay time applied to any channel
          that lacks an individual control.

        If neither an individual nor a shared control is provided for a
        channel, the decay defaults to 0.5.

    Returns
    -------
    str
        DROID .ini text containing one ``[contour]`` circuit per active
        trigger/envelope pair.
    """
    decay_all = controls.get("decay_all")
    blocks = []

    for ch in _CHANNELS:
        trigger_key = f"trigger{ch}"
        env_key = f"env{ch}"

        trigger = inputs.get(trigger_key)
        env = outputs.get(env_key)

        # Only emit a contour block when both trigger and output are assigned
        if trigger is None or env is None:
            continue

        # Resolve decay value: per-channel > shared > default
        decay = controls.get(f"decay{ch}", decay_all if decay_all is not None else _DEFAULT_DECAY)

        blocks.append(
            "\n".join([
                f"# {name}: decay envelope ch{ch}",
                "[contour]",
                f"    gate = {trigger}",
                "    attack = 0",
                f"    decay = {decay}",
                "    sustain = 0",
                "    release = 0.001",
                f"    output = {env}",
            ])
        )

    return "\n\n".join(blocks)
