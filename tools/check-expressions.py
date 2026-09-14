"""Flag DROID parameter values that exceed the allowed A*B+C form.

A DROID parameter accepts one multiplication and one offset — the manual calls
it "Multiply and Add, Attenuation and Offset", computing A x B + C, where B and
C may themselves be cables. Anything richer (parentheses, a second product, a
third term) is not a valid expression, and the result is a parameter that never
evaluates: a gate that silently never fires, an LED that never lights.

Nothing in the patch file looks wrong, so this is worth running over any patch
that is mysteriously silent.

    python tools/check-expressions.py path/to/droid.ini

Use extra circuits to build up anything more complex: [copy] to precompute a
product, [logic] with "and" / "or" to combine three or more gates.

The check is deliberately conservative: it flags anything beyond the documented
A x B + C form. Confirmed to fail on real hardware are parentheses and products
of three or more terms. A sum of two products (a * b + c * d) is flagged too but
has been observed working, so treat those hits as worth checking rather than as
certain faults.
"""
import re, sys, pathlib

TOKEN = r"(?:-?\d*\.?\d+|_[A-Z][A-Z0-9_]*|[A-Z]\d+(?:\.\d+)?)"
ALLOWED = [
    rf"^{TOKEN}$",                                  # plain value
    rf"^{TOKEN}\s*\*\s*{TOKEN}$",                   # A * B
    rf"^{TOKEN}\s*\*\s*{TOKEN}\s*\+\s*{TOKEN}$",    # A * B + C
    rf"^{TOKEN}\s*\+\s*{TOKEN}$",                   # A + C
    rf"^{TOKEN}\s*-\s*{TOKEN}$",                    # A - C
]

path = pathlib.Path(sys.argv[1])
bad = []
circuit = None
for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
    line = raw.split("#")[0].rstrip()
    if not line.strip():
        continue
    if m := re.match(r"^\[(\w+)\]$", line.strip()):
        circuit = m.group(1)
        continue
    if m := re.match(r"^\s+(\w+)\s*=\s*(.+)$", line):
        param, value = m.group(1), m.group(2).strip()
        if not any(re.match(p, value) for p in ALLOWED):
            bad.append((n, circuit, param, value))

print(f"{path.name}: {len(bad)} parameter(s) exceed A*B+C\n")
for n, c, p, v in bad:
    print(f"  line {n:>4}  [{c}] {p} = {v}")
