#!/usr/bin/env python3
"""Lint a DROID patch for faults that load silently or upset DROID Forge.

Four checks, all of which have bitten real patches in this repo:

1. A x B + C
   A DROID parameter has exactly three columns - value, factor, offset - and
   computes A x B + C (manual section 2.6). Parentheses, a second product or a
   third term cannot be stored, so the parameter never evaluates. No error, no
   symptom: a gate simply never fires. Build anything richer from [logic] and
   [copy] circuits.

2. Duplicate parameters
   Setting the same parameter twice in one circuit silently keeps the last one.

3. Brackets in prose comments
   Forge reads "#  O1: [Label] description" as a jack label. A bracket anywhere
   else in a comment is a parse error in Forge. Keep circuit names out of prose.

4. Non-Forge section dividers
   Forge sections are three lines: divider, title, divider. A block that also
   ends with a divider opens a second, untitled section.

    python tools/check-patch.py path/to/droid.ini
"""

import re
import sys
import pathlib

TOKEN = r"(?:-?\d*\.?\d+|_[A-Z][A-Z0-9_]*|[A-Z]\d+(?:\.\d+)?)"
ALLOWED = [
    rf"^{TOKEN}$",
    rf"^{TOKEN}\s*\*\s*{TOKEN}$",
    rf"^{TOKEN}\s*\*\s*{TOKEN}\s*\+\s*{TOKEN}$",
    rf"^{TOKEN}\s*\+\s*{TOKEN}$",
    rf"^{TOKEN}\s*-\s*{TOKEN}$",
]
LABEL = re.compile(r"^#\s+[A-Z]\d+(?:\.\d+)?:\s*\[[^\]]*\]")


def lint(path: pathlib.Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    expr, dupes, brackets, dividers = [], [], [], []
    circuit, start, seen, in_circuits = None, 0, {}, False

    for n, raw in enumerate(lines, 1):
        stripped = raw.strip()

        if stripped.startswith("#"):
            if in_circuits and ("[" in stripped or "]" in stripped):
                brackets.append((n, stripped))
            elif not in_circuits and ("[" in stripped or "]" in stripped) and not LABEL.match(raw):
                brackets.append((n, stripped))
            if re.match(r"^#\s*[=_]{5,}$", stripped):
                dividers.append((n, stripped))
            continue

        line = raw.split("#")[0].rstrip()
        if not line.strip():
            continue

        if m := re.match(r"^\[(\w+)\]$", line.strip()):
            circuit, start, seen, in_circuits = m.group(1), n, {}, True
            continue

        if m := re.match(r"^\s+(\w+)\s*=\s*(.+)$", line):
            param, value = m.group(1), m.group(2).strip()
            if param in seen:
                dupes.append((circuit, param, seen[param], n))
            seen[param] = n
            if not any(re.match(p, value) for p in ALLOWED):
                expr.append((n, circuit, param, value))

    total = len(expr) + len(dupes) + len(brackets) + len(dividers)
    print(f"{path.name}: {total} issue(s)")

    if expr:
        print(f"\n  {len(expr)} parameter(s) exceed A x B + C — these never evaluate:")
        for n, c, p, v in expr:
            print(f"    line {n:>5}  [{c}] {p} = {v}")
    if dupes:
        print(f"\n  {len(dupes)} duplicate parameter(s) — the later value wins:")
        for c, p, first, second in dupes:
            print(f"    [{c}] '{p}' set at line {first}, overridden at line {second}")
    if brackets:
        print(f"\n  {len(brackets)} comment(s) with brackets — Forge reads these as jack labels:")
        for n, text in brackets:
            print(f"    line {n:>5}  {text[:70]}")
    if dividers:
        print(f"\n  {len(dividers)} non-Forge divider(s) — use '# ---' title '# ---', no trailing divider:")
        for n, text in dividers:
            print(f"    line {n:>5}  {text[:40]}")

    return total


if __name__ == "__main__":
    sys.exit(1 if lint(pathlib.Path(sys.argv[1])) else 0)
