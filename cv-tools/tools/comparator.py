"""
Comparator — Doepfer A-167 Analog Comparator

Compare two CV signals (or one signal against a threshold).  Outputs a
gate (1 V) when input A is greater than input B, and 0 V otherwise.
An optional inverted output provides the logical complement.

Comparison source priority:
  1. "compare" input jack — compare against another signal
  2. "threshold" pot       — compare against a manual threshold
  3. Neither provided      — compare against a fixed 0.5 V default
"""

TOOL_META = {
    "name": "comparator",
    "description": "Compare two CVs, output gate when A > B",
    "doepfer": "A-167",
    "required_inputs": ["input"],
    "optional_inputs": ["compare"],
    "required_outputs": ["gate"],
    "optional_outputs": ["inverted"],
    "required_controls": [],
    "optional_controls": ["threshold"],
}


def render(name, inputs, outputs, controls):
    """Render DROID .ini blocks for an analog comparator.

    Args:
        name:     Instance name, used as internal cable prefix.
        inputs:   Dict with "input" (required) and optionally "compare".
        outputs:  Dict with "gate" (required) and optionally "inverted".
        controls: Dict with optionally "threshold".

    Returns:
        A string containing the DROID circuit blocks.
    """
    cv_in = inputs["input"]
    gate_out = outputs["gate"]
    inverted_out = outputs.get("inverted")

    compare_input = inputs.get("compare")
    threshold = controls.get("threshold")

    # Determine what to compare against (priority: compare jack > pot > 0.5)
    if compare_input:
        compare_value = compare_input
    elif threshold:
        compare_value = threshold
    else:
        compare_value = "0.5"

    # Internal cable for the gate value, used when we also need the inverse
    gate_cable = f"_{name}_gate"
    gate_target = gate_cable if inverted_out else gate_out

    lines = [
        f"# Comparator: gate high when input > reference",
    ]

    if compare_input:
        lines.append(f"# Comparing {cv_in} against signal {compare_input}")
    elif threshold:
        lines.append(f"# Comparing {cv_in} against threshold pot {threshold}")
    else:
        lines.append(f"# Comparing {cv_in} against fixed 0.5")

    lines += [
        "",
        "[compare]",
        f"    input = {cv_in}",
        f"    compare = {compare_value}",
        "    ifgreater = 1",
        "    ifless = 0",
        "    ifequal = 0",
        f"    output = {gate_target}",
    ]

    if inverted_out:
        # Copy the internal gate to the actual gate output
        lines += [
            "",
            f"# Gate output",
            "[copy]",
            f"    input = {gate_cable}",
            f"    output = {gate_out}",
            "",
            f"# Inverted gate: HIGH when input <= reference",
            "[copy]",
            f"    input = -1 * {gate_cable} + 1",
            f"    output = {inverted_out}",
        ]

    return "\n".join(lines)
