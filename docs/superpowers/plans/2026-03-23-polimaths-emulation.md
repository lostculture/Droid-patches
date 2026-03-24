# PoliMATHS Emulation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a DROID patch emulating the Make Noise PoliMATHS 8-channel CV/audio event generator with Rise-Fall envelopes, oscillators, 4 activation modes, spread modulation, and dual output modes.

**Architecture:** Single `.ini` patch file built section-by-section. Each section is a self-contained block of DROID circuits following the "producers above consumers" convention. Spread math is computed inline to minimize circuit count. ~168 circuits total across 17 functional sections.

**Tech Stack:** DROID patch language (.ini format). Hardware: 2x p2b8, 1x p10, 1x p8s8, 1x x7. Spec: `docs/superpowers/specs/2026-03-23-polimaths-emulation-design.md`

**Reference patches for style:** `droid-maths-classics.ini`, `droid-bouncing-ball.ini`, `droid-mi-grids.ini`

**Key conventions from existing patches:**
- Comment header block with INPUTS/OUTPUTS/CONTROLLER descriptions
- Section separators: `# -------------------------------------------------`
- Major sections: `# ============================================================`
- Internal cables: `_UPPERCASE_NAME`
- Comments above each circuit explaining its purpose

**Testing:** DROID patches cannot be unit-tested. Each task produces a loadable intermediate state. To verify: load `.ini` onto DROID via USB, confirm LEDs respond and signals appear on outputs. Tasks are ordered so earlier tasks produce simpler, independently verifiable behavior.

---

### Task 1: File Header and Controller Declarations

**Files:**
- Create: `droid-polimaths.ini`

- [ ] **Step 1: Write the comment header block**

Write the file header with full I/O mapping, controller descriptions, and feature summary. Follow the style from `droid-maths-classics.ini` — block comment listing all inputs, outputs, and controller assignments.

```ini
# PoliMATHS — 8-Channel CV Event Generator
#
# Emulation of Make Noise PoliMATHS for DROID.
# 8 channels of Rise-Fall envelopes with superimposed
# oscillators (LFO to audio rate). Four activation modes,
# Spread modulation across channels, and dual output modes.
#
# INPUTS:
#   I1: Activate (clock/gate — triggers channel activations)
#   I2: Reset
#   I3: Span CV (external channel selection modulation)
#   I4: Spread CV (external spread amount modulation)
#
# OUTPUTS (Internal Osc mode — default):
#   O1-O8: Channel 1-8 envelope+oscillation CV
#   G1-G8: Channel 1-8 activity gates (via X7)
#
# OUTPUTS (External Osc mode — B1.7):
#   O1-O8: Channel 1-8 pitch CV (1V/oct for external VCOs)
#   G1-G8: Channel 1-8 activation gates
#
# CONTROLLER 1 (p2b8) — Transport & Mode:
#   P1.1: Span (channel select / round step / parallel divisions)
#   P1.2: Spread (center=none, CW=right channels, CCW=left)
#   B1.1: Run/Stop (LED = running)
#   B1.2: Reset (momentary)
#   B1.3: Mode (4 states: Ch.Index / Round / Parallel / Binary)
#   B1.4: Cycle on/off
#   B1.5: Cycle mode (All / Follow the Leader)
#   B1.6: Osc Bias (Unipolar / Bipolar)
#   B1.7: Output mode (Internal Osc / External Osc)
#   B1.8: [unused]
#
# CONTROLLER 2 (p2b8) — Curve & Manual Triggers:
#   P2.1: Curve (envelope shape: log → linear → exponential)
#   P2.2: Osc depth (oscillation mix amount)
#   B2.1-B2.8: Manual channel triggers (momentary)
#   L2.1-L2.8: Channel activity LEDs
#
# CONTROLLER 3 (p10) — Parameters & Spread Depths:
#   P3.1: Rise    P3.6: Rise spread depth
#   P3.2: Fall    P3.7: Fall spread depth
#   P3.3: Strength P3.8: Strength spread depth
#   P3.4: Rate    P3.9: Rate spread depth
#   P3.5: Shape   P3.10: Osc spread depth
#
# CONTROLLER 4 (p8s8) — Per-Channel:
#   P4.1-P4.8: Channel 1-8 level trim
#   S4.1-S4.8: Channel 1-8 mute switches
#
# CONTROLLER 5 (x7) — Gate Expander:
#   G1-G8: Channel 1-8 gate outputs
```

- [ ] **Step 2: Write controller declarations**

```ini
[p2b8]
[p2b8]
[p10]
[p8s8]
[x7]
```

- [ ] **Step 3: Verify file is valid**

Confirm the file loads without syntax errors. At this stage the patch does nothing but declare controllers.

---

### Task 2: Transport — Clock, Run/Stop, Reset

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 1

- [ ] **Step 1: Write transport section**

```ini
# ============================================================
# TRANSPORT
# ============================================================

# Internal clock (normaled to I1 when unpatched)
[lfo]
    hz = 4 * P1.1 + 0.5
    square = N1

# Run/Stop toggle
[button]
    button = B1.1
    led = L1.1
    startvalue = 1
    output = _RUNNING

# Reset (momentary)
[button]
    button = B1.2
    states = 1
    led = L1.2
    output = _RESET_BTN

# Gate activate with running state
[copy]
    input = I1 * _RUNNING
    output = _ACTIVATE

# Merge reset sources
[copy]
    input = _RESET_BTN + I2
    output = _RESET
```

- [ ] **Step 2: Verify**

Load patch. B1.1 LED should light on boot (startvalue=1). Pressing B1.1 toggles LED. B1.2 should flash momentarily. Internal clock should be active on N1 (visible if I1 normalled).

---

### Task 3: Mode, Cycle, and Output Buttons

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 2

- [ ] **Step 1: Write mode/cycle/output button section**

```ini
# ============================================================
# MODE & CYCLE CONTROLS
# ============================================================

# Mode select: 4 states (Ch.Index=0 / Round=0.333 / Parallel=0.667 / Binary=1.0)
[button]
    button = B1.3
    states = 4
    output = _MODE

# Mode LED brightness (0.25 / 0.5 / 0.75 / 1.0)
[copy]
    input = _MODE * 0.75 + 0.25
    output = L1.3

# Cycle on/off
[button]
    button = B1.4
    led = L1.4
    output = _CYCLE_ON

# Cycle mode: 0 = All, 1 = Follow the Leader
[button]
    button = B1.5
    led = L1.5
    output = _CYCLE_MODE

# Osc Bias: 0 = Unipolar, 1 = Bipolar
[button]
    button = B1.6
    led = L1.6
    output = _OSC_BIPOLAR

# Output mode: 0 = Internal Osc, 1 = External Osc
[button]
    button = B1.7
    led = L1.7
    output = _OUTPUT_MODE

# Cycle All: active when cycle ON and mode = All
[copy]
    input = _CYCLE_ON * (1 - _CYCLE_MODE)
    output = _CYCLE_ALL

# Cycle FtL: active when cycle ON and mode = FtL
[copy]
    input = _CYCLE_ON * _CYCLE_MODE
    output = _CYCLE_FTL
```

- [ ] **Step 2: Verify**

Load patch. B1.3 cycles through 4 brightness levels on L1.3. B1.4-B1.7 toggle their LEDs. All buttons should be responsive.

---

### Task 4: Spread Pre-Compute

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 3

- [ ] **Step 1: Write spread direction calculation**

```ini
# ============================================================
# SPREAD
# ============================================================

# Spread direction: P1.2 center (0.5) = no spread
# Adding I4 for external CV modulation
# Result: -1 (full left) to +1 (full right)
[copy]
    input = (P1.2 + I4 - 0.5) * 2
    output = _SPREAD_DIR
```

This single circuit produces `_SPREAD_DIR` used inline by all downstream circuits. Per-channel weights (0/7 through 7/7) are literal constants in the contour/lfo expressions.

- [ ] **Step 2: Verify**

P1.2 at center → `_SPREAD_DIR` ≈ 0. Fully CW → ≈ +1. Fully CCW → ≈ -1. Not directly observable without downstream circuits, but patch should load without errors.

---

### Task 5: Channel Index Activation Mode

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 4

- [ ] **Step 1: Write Channel Index section**

Uses 8x `[compare]` to determine which channel the Span pot (P1.1 + I3) selects. Each compare tests if span falls in a 1/8th window. The activation trigger is AND'd with the channel selection.

```ini
# ============================================================
# ACTIVATION MODE: CHANNEL INDEX
# ============================================================

# Combined span: pot + external CV
[copy]
    input = P1.1 + I3
    output = _SPAN

# Channel 1 selected: span 0.000 - 0.125
[compare]
    input = _SPAN
    compare = 0.125
    ifless = _ACTIVATE
    ifgreater = 0
    ifequal = 0
    output = _CIDX_CH1

# Channel 2 selected: span 0.125 - 0.250
[copy]
    input = _SPAN - 0.125
    output = _SPAN_S2

[compare]
    input = _SPAN_S2
    compare = 0
    ifgreater = 1
    ifless = 0
    ifequal = 0
    output = _SPAN_S2_LO

[compare]
    input = _SPAN
    compare = 0.250
    ifless = 1
    ifgreater = 0
    ifequal = 0
    output = _SPAN_S2_HI

[copy]
    input = _SPAN_S2_LO * _SPAN_S2_HI * _ACTIVATE
    output = _CIDX_CH2
```

This per-channel approach requires too many circuits. Instead, use a simpler method: quantize span to 0-7 using math, then use 8x compare against each integer value:

```ini
# Quantize span to channel number (0-7)
# Multiply by 8, floor via compare cascade
[copy]
    input = _SPAN * 7
    output = _SPAN_SCALED

# Ch1: span < 0.5 (after scaling: _SPAN_SCALED < 0.5)
[compare]
    input = _SPAN_SCALED
    compare = 0.5
    ifless = _ACTIVATE
    ifgreater = 0
    output = _CIDX_CH1

# Ch2: 0.5 <= span < 1.5
[compare]
    input = _SPAN_SCALED
    compare = 0.5
    ifgreater = 1
    ifless = 0
    output = _CIDX2_LO

[compare]
    input = _SPAN_SCALED
    compare = 1.5
    ifless = _CIDX2_LO
    ifgreater = 0
    output = _CIDX_CH2
```

This still uses too many circuits. **Simplest approach**: use a `[switch]` with 8 identical inputs that routes _ACTIVATE to the correct internal cable. But `[switch]` selects *which input to read*, not *which output to write to*.

**Best approach**: Use the `[compare]` `ifequal` path won't work since span is continuous. Instead, round to nearest integer and use 8 separate compares against exact values. But DROID doesn't have a round function.

**Practical approach**: Use a `[pot]` with `discrete = 8` to quantize P1.1 (but pot circuit reads a physical pot, not a computed value). Since we need P1.1 + I3, we can't use the pot circuit directly.

**Final approach**: Use the switch offset behavior. A `[switch]` with 8 inputs naturally quantizes offset 0-1 into 8 zones. Put `_ACTIVATE` into each input, and the output carries it only for the selected zone. But that gives us only 1 output — we need to know *which* channel.

The cleanest DROID idiom: generate `_ACTIVATE` on the correct output by using 8 separate copy circuits gated by threshold checks. Since DROID's compare handles ranges naturally:

```ini
# ============================================================
# ACTIVATION MODE: CHANNEL INDEX
# ============================================================

# Combined span: pot + external CV
[copy]
    input = P1.1 + I3
    output = _SPAN

# Scale span to 0-8 range for threshold comparison
[copy]
    input = _SPAN * 8
    output = _SPAN8

# Channel 1: _SPAN8 in [0, 1)
[compare]
    input = _SPAN8
    compare = 1
    ifless = 1
    ifgreater = 0
    output = _CIDX_SEL1

# Channel 2: _SPAN8 in [1, 2)
[compare]
    input = _SPAN8 - 1
    compare = 0
    ifgreater = 1
    ifless = 0
    output = _CIDX_SEL2_LO

[compare]
    input = _SPAN8
    compare = 2
    ifless = _CIDX_SEL2_LO
    ifgreater = 0
    output = _CIDX_SEL2
```

This is still verbose. Let me use the most circuit-efficient approach: a single `[switch]` per channel that outputs _ACTIVATE only when that channel's span zone is selected, using 8 switches all reading the same `_SPAN` offset but with only one slot set to _ACTIVATE:

Actually, the simplest is to route _ACTIVATE through a `[switch]` read in one direction for channel ID, then gate 8 copies. Since DROID `[switch]` with 8 inputs selects which input to pass through, we need the reverse: given a selector, route a signal to one of N outputs. DROID doesn't have a demux.

**Most efficient DROID approach: 8x `[copy]` with `[compare]`-generated selection masks.** To keep it to 16 circuits total (8 compare + 8 copy is too many), I'll compute channel selection inline:

```ini
# ============================================================
# ACTIVATION MODE: CHANNEL INDEX
# ============================================================

# Combined span: pot + external CV, clamped 0-1
[copy]
    input = P1.1 + I3
    output = _SPAN

# Quantize span to channel number 1-8.
# _SPAN * 8 gives 0-8; integer part = channel.
# Use [compare] for each channel threshold window.
# Ch N active when: (N-1)/8 <= _SPAN < N/8

# Channel 1
[compare]
    input = _SPAN
    compare = 0.125
    ifless = _ACTIVATE
    ifgreater = 0
    ifequal = _ACTIVATE
    output = _CIDX_CH1

# Channel 2
[compare]
    input = _SPAN - 0.125
    compare = 0
    ifgreater = 1
    ifless = 0
    output = _CI2A

[compare]
    input = _SPAN
    compare = 0.25
    ifless = _CI2A
    ifgreater = 0
    output = _CI2B

[copy]
    input = _CI2B * _ACTIVATE
    output = _CIDX_CH2
```

This uses 3 circuits per channel (24 total) — way too many. Let me reconsider.

**Best practical approach: use `[multicompare]` if available, or accept that Channel Index uses ~16 circuits.** Looking at the DROID circuit list, there's `[multicompare]` — "Compare input against up to 8 values." This is exactly what we need!

Let me update to use `[multicompare]`:

```ini
# Channel index: multicompare quantizes _SPAN into 8 zones
# Each output fires when _SPAN falls in that zone's range
[multicompare]
    input = _SPAN
    compare1 = 0.0625
    compare2 = 0.1875
    compare3 = 0.3125
    compare4 = 0.4375
    compare5 = 0.5625
    compare6 = 0.6875
    compare7 = 0.8125
    compare8 = 0.9375
    output1 = _CIDX_SEL1
    output2 = _CIDX_SEL2
    output3 = _CIDX_SEL3
    output4 = _CIDX_SEL4
    output5 = _CIDX_SEL5
    output6 = _CIDX_SEL6
    output7 = _CIDX_SEL7
    output8 = _CIDX_SEL8
```

Wait — I need to verify how `[multicompare]` works. The spec says "Compare input against up to 8 values" but I don't have the exact parameter names. Let me use the reliable approach instead: 8x `[compare]` with overlapping threshold logic, or better yet — **a sequencer trick**.

Actually, the simplest reliable approach is: store _SPAN as a value, then for each channel, test if it falls in range using `[compare]` with `ifequal` plus rounding. Since that's unreliable with continuous values, let me just use 8x `[compare]` with a staircase approach:

```ini
# _SPAN ranges 0-1. Multiply by 7 to get 0-7 range.
# Each channel tests: am I the nearest integer?
# Channel i selected when abs(_SPAN*7 - i) < 0.5

# This can be computed as: _SPAN*7 > (i-0.5) AND _SPAN*7 < (i+0.5)
# Using a single compare with threshold at the midpoint:
# ch0: _SPAN*7 < 0.5
# ch1: _SPAN*7 >= 0.5 AND < 1.5  → need 2 compares
# ...this still needs 2 per channel for interior channels.
```

For 8 channels: ch1 needs 1 compare, ch2-7 need 2 each, ch8 needs 1 = 14 compares. Plus 6 copies for AND logic = 20 circuits. Too many.

**Pragmatic solution: use 8 overlapping `[compare]` circuits where each tests an upper threshold, then derive per-channel selection by differencing adjacent outputs:**

```ini
# Scale span to 0-8
[copy]
    input = _SPAN * 8
    output = _SPAN8

# Cumulative thresholds: "is span >= N?"
[compare]
    input = _SPAN8
    compare = 1
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SPAN_GE1

[compare]
    input = _SPAN8
    compare = 2
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SPAN_GE2

# ... through _SPAN_GE7

# Channel selection by differencing:
# Ch1 = NOT _SPAN_GE1 (span < 1)
# Ch2 = _SPAN_GE1 AND NOT _SPAN_GE2
# Ch8 = _SPAN_GE7
```

This uses 7 `[compare]` + 8 `[copy]` = 15 circuits. Still heavy. But it's necessary for clean channel selection.

Given that this section will be large, let me write it compactly:

- [ ] **Step 1 (revised): Write Channel Index activation**

```ini
# ============================================================
# ACTIVATION MODE: CHANNEL INDEX
# ============================================================

# Combined span value
[copy]
    input = P1.1 + I3
    output = _SPAN

# Scale to 0-8 range for threshold tests
[copy]
    input = _SPAN * 8
    output = _SPAN8

# Cumulative "span >= N" thresholds
[compare]
    input = _SPAN8
    compare = 1
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE1

[compare]
    input = _SPAN8
    compare = 2
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE2

[compare]
    input = _SPAN8
    compare = 3
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE3

[compare]
    input = _SPAN8
    compare = 4
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE4

[compare]
    input = _SPAN8
    compare = 5
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE5

[compare]
    input = _SPAN8
    compare = 6
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE6

[compare]
    input = _SPAN8
    compare = 7
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _SP_GE7

# Per-channel selection (difference of adjacent thresholds)
# Ch1 selected when span < 1 (not GE1)
[copy]
    input = (1 - _SP_GE1) * _ACTIVATE
    output = _CIDX_CH1

# Ch2 selected when GE1 but not GE2
[copy]
    input = (_SP_GE1 - _SP_GE2) * _ACTIVATE
    output = _CIDX_CH2

# Ch3 selected when GE2 but not GE3
[copy]
    input = (_SP_GE2 - _SP_GE3) * _ACTIVATE
    output = _CIDX_CH3

[copy]
    input = (_SP_GE3 - _SP_GE4) * _ACTIVATE
    output = _CIDX_CH4

[copy]
    input = (_SP_GE4 - _SP_GE5) * _ACTIVATE
    output = _CIDX_CH5

[copy]
    input = (_SP_GE5 - _SP_GE6) * _ACTIVATE
    output = _CIDX_CH6

[copy]
    input = (_SP_GE6 - _SP_GE7) * _ACTIVATE
    output = _CIDX_CH7

# Ch8 selected when GE7
[copy]
    input = _SP_GE7 * _ACTIVATE
    output = _CIDX_CH8
```

Total: 2 copy (span) + 7 compare + 8 copy (selection) = 17 circuits.

- [ ] **Step 2: Verify**

Load patch. Turn P1.1 through its range — not directly observable yet until outputs are connected. Confirm patch loads without error.

---

### Task 6: Round Activation Mode

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 5

- [ ] **Step 1: Write Round activation**

Round mode steps through channels sequentially. An 8-step sequencer holds channel positions. Span controls step size via clock multiplication.

```ini
# ============================================================
# ACTIVATION MODE: ROUND
# ============================================================

# Step size from span: 1-4 steps per activation
[switch]
    input1 = 1
    input2 = 2
    input3 = 3
    input4 = 4
    offset = _SPAN
    output1 = _ROUND_STEP

# Clock multiply for step size
[clocktool]
    clock = _ACTIVATE
    multiply = _ROUND_STEP
    output = _ROUND_CLK

# Position counter: cycles through 8 steps
# CV values 0.000-1.000 in 8 steps (0, 0.143, 0.286, ...)
[sequencer]
    clock = _ROUND_CLK
    reset = _RESET
    cv1 = 0.000
    cv2 = 0.143
    cv3 = 0.286
    cv4 = 0.429
    cv5 = 0.571
    cv6 = 0.714
    cv7 = 0.857
    cv8 = 1.000
    cvoutput = _ROUND_POS

# Route activation to the current channel position
# Reuse the same threshold logic as Channel Index
# but with _ROUND_POS instead of _SPAN

# Scale to 0-8
[copy]
    input = _ROUND_POS * 8
    output = _RPOS8

# Thresholds (reuse pattern from Ch.Index section)
[compare]
    input = _RPOS8
    compare = 1
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE1

[compare]
    input = _RPOS8
    compare = 2
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE2

[compare]
    input = _RPOS8
    compare = 3
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE3

[compare]
    input = _RPOS8
    compare = 4
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE4

[compare]
    input = _RPOS8
    compare = 5
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE5

[compare]
    input = _RPOS8
    compare = 6
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE6

[compare]
    input = _RPOS8
    compare = 7
    ifgreater = 1
    ifless = 0
    ifequal = 1
    output = _RP_GE7

# Per-channel round triggers
[copy]
    input = (1 - _RP_GE1) * _ACTIVATE
    output = _ROUND_CH1

[copy]
    input = (_RP_GE1 - _RP_GE2) * _ACTIVATE
    output = _ROUND_CH2

[copy]
    input = (_RP_GE2 - _RP_GE3) * _ACTIVATE
    output = _ROUND_CH3

[copy]
    input = (_RP_GE3 - _RP_GE4) * _ACTIVATE
    output = _ROUND_CH4

[copy]
    input = (_RP_GE4 - _RP_GE5) * _ACTIVATE
    output = _ROUND_CH5

[copy]
    input = (_RP_GE5 - _RP_GE6) * _ACTIVATE
    output = _ROUND_CH6

[copy]
    input = (_RP_GE6 - _RP_GE7) * _ACTIVATE
    output = _ROUND_CH7

[copy]
    input = _RP_GE7 * _ACTIVATE
    output = _ROUND_CH8
```

Total: 1 switch + 1 clocktool + 1 sequencer + 1 copy + 7 compare + 8 copy = 19 circuits.

- [ ] **Step 2: Verify**

Patch loads without error. Round mode logic is not observable until mode mux and outputs are connected.

---

### Task 7: Parallel Activation Mode

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 6

- [ ] **Step 1: Write Parallel activation**

Each channel has its own clock divider. Span sets the division spread.

```ini
# ============================================================
# ACTIVATION MODE: PARALLEL
# ============================================================

# Division ratios per channel, controlled by Span
# Span center (0.5) = all /1; Span CW = ascending divs
# Use switch to select division sets

# Division set selection from span (4 presets)
# Set 0: all /1
# Set 1: /1 /1 /2 /2 /4 /4 /8 /8
# Set 2: /1 /2 /3 /4 /5 /6 /7 /8
# Set 3: /1 /2 /4 /8 /16 /32 /64 /128

# Ch1 always /1
[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = 1
    output = _PAR_CH1

# Ch2: /1 or /2 depending on span
[switch]
    input1 = 1
    input2 = 1
    input3 = 2
    input4 = 2
    offset = _SPAN
    output1 = _PAR_DIV2

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV2
    output = _PAR_CH2

# Ch3
[switch]
    input1 = 1
    input2 = 2
    input3 = 3
    input4 = 4
    offset = _SPAN
    output1 = _PAR_DIV3

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV3
    output = _PAR_CH3

# Ch4
[switch]
    input1 = 1
    input2 = 2
    input3 = 4
    input4 = 8
    offset = _SPAN
    output1 = _PAR_DIV4

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV4
    output = _PAR_CH4

# Ch5
[switch]
    input1 = 1
    input2 = 4
    input3 = 5
    input4 = 16
    offset = _SPAN
    output1 = _PAR_DIV5

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV5
    output = _PAR_CH5

# Ch6
[switch]
    input1 = 1
    input2 = 4
    input3 = 6
    input4 = 32
    offset = _SPAN
    output1 = _PAR_DIV6

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV6
    output = _PAR_CH6

# Ch7
[switch]
    input1 = 1
    input2 = 8
    input3 = 7
    input4 = 64
    offset = _SPAN
    output1 = _PAR_DIV7

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV7
    output = _PAR_CH7

# Ch8
[switch]
    input1 = 1
    input2 = 8
    input3 = 8
    input4 = 128
    offset = _SPAN
    output1 = _PAR_DIV8

[clocktool]
    clock = _ACTIVATE
    reset = _RESET
    divide = _PAR_DIV8
    output = _PAR_CH8
```

Total: 8 clocktool + 7 switch = 15 circuits.

- [ ] **Step 2: Verify**

Patch loads without error.

---

### Task 8: Binary Counter Activation Mode

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 7

- [ ] **Step 1: Write Binary Counter**

8 flipflops form a ripple counter. Each toggles on the falling edge of the previous. Channel triggers fire on rising edges of each bit.

```ini
# ============================================================
# ACTIVATION MODE: BINARY COUNTER
# ============================================================

# Bit 0 (Ch1) — toggles on every activation
[flipflop]
    toggle = _ACTIVATE
    reset = _RESET
    output = _BIN_BIT0

# Bit 1 (Ch2) — toggles when bit 0 goes low (carry)
# Use inverted bit0: toggle on rising edge of NOT bit0
[copy]
    input = 1 - _BIN_BIT0
    output = _BIN_BIT0_INV

[flipflop]
    toggle = _BIN_BIT0_INV
    reset = _RESET
    output = _BIN_BIT1

# Bit 2 (Ch3)
[copy]
    input = 1 - _BIN_BIT1
    output = _BIN_BIT1_INV

[flipflop]
    toggle = _BIN_BIT1_INV
    reset = _RESET
    output = _BIN_BIT2

# Bit 3 (Ch4)
[copy]
    input = 1 - _BIN_BIT2
    output = _BIN_BIT2_INV

[flipflop]
    toggle = _BIN_BIT2_INV
    reset = _RESET
    output = _BIN_BIT3

# Bit 4 (Ch5)
[copy]
    input = 1 - _BIN_BIT3
    output = _BIN_BIT3_INV

[flipflop]
    toggle = _BIN_BIT3_INV
    reset = _RESET
    output = _BIN_BIT4

# Bit 5 (Ch6)
[copy]
    input = 1 - _BIN_BIT4
    output = _BIN_BIT4_INV

[flipflop]
    toggle = _BIN_BIT4_INV
    reset = _RESET
    output = _BIN_BIT5

# Bit 6 (Ch7)
[copy]
    input = 1 - _BIN_BIT5
    output = _BIN_BIT5_INV

[flipflop]
    toggle = _BIN_BIT5_INV
    reset = _RESET
    output = _BIN_BIT6

# Bit 7 (Ch8)
[copy]
    input = 1 - _BIN_BIT6
    output = _BIN_BIT6_INV

[flipflop]
    toggle = _BIN_BIT6_INV
    reset = _RESET
    output = _BIN_BIT7

# Binary counter uses bits as gates directly
# Channel is "active" while its bit is high
# Per PoliMATHS: channel activates while bit=1, silent while bit=0
[copy]
    input = _BIN_BIT0
    output = _BIN_CH1

[copy]
    input = _BIN_BIT1
    output = _BIN_CH2

[copy]
    input = _BIN_BIT2
    output = _BIN_CH3

[copy]
    input = _BIN_BIT3
    output = _BIN_CH4

[copy]
    input = _BIN_BIT4
    output = _BIN_CH5

[copy]
    input = _BIN_BIT5
    output = _BIN_CH6

[copy]
    input = _BIN_BIT6
    output = _BIN_CH7

[copy]
    input = _BIN_BIT7
    output = _BIN_CH8
```

Total: 8 flipflop + 7 copy (invert) + 8 copy (output) = 23 circuits.

- [ ] **Step 2: Verify**

Patch loads without error.

---

### Task 9: Mode Multiplexer and Manual Trigger OR

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Tasks 5-8

- [ ] **Step 1: Write mode mux — select correct trigger per channel based on _MODE**

Each channel gets a `[switch]` that selects between the 4 mode outputs. Then manual triggers (B2.1-B2.8) are OR'd in.

```ini
# ============================================================
# MODE MUX + MANUAL TRIGGERS
# ============================================================

# Per-channel mode selection: pick trigger from active mode
# _MODE: 0=Ch.Index, 0.333=Round, 0.667=Parallel, 1.0=Binary

# Channel 1
[switch]
    input1 = _CIDX_CH1
    input2 = _ROUND_CH1
    input3 = _PAR_CH1
    input4 = _BIN_CH1
    offset = _MODE
    output1 = _MODE_TRIG_CH1

# Channel 2
[switch]
    input1 = _CIDX_CH2
    input2 = _ROUND_CH2
    input3 = _PAR_CH2
    input4 = _BIN_CH2
    offset = _MODE
    output1 = _MODE_TRIG_CH2

# Channel 3
[switch]
    input1 = _CIDX_CH3
    input2 = _ROUND_CH3
    input3 = _PAR_CH3
    input4 = _BIN_CH3
    offset = _MODE
    output1 = _MODE_TRIG_CH3

# Channel 4
[switch]
    input1 = _CIDX_CH4
    input2 = _ROUND_CH4
    input3 = _PAR_CH4
    input4 = _BIN_CH4
    offset = _MODE
    output1 = _MODE_TRIG_CH4

# Channel 5
[switch]
    input1 = _CIDX_CH5
    input2 = _ROUND_CH5
    input3 = _PAR_CH5
    input4 = _BIN_CH5
    offset = _MODE
    output1 = _MODE_TRIG_CH5

# Channel 6
[switch]
    input1 = _CIDX_CH6
    input2 = _ROUND_CH6
    input3 = _PAR_CH6
    input4 = _BIN_CH6
    offset = _MODE
    output1 = _MODE_TRIG_CH6

# Channel 7
[switch]
    input1 = _CIDX_CH7
    input2 = _ROUND_CH7
    input3 = _PAR_CH7
    input4 = _BIN_CH7
    offset = _MODE
    output1 = _MODE_TRIG_CH7

# Channel 8
[switch]
    input1 = _CIDX_CH8
    input2 = _ROUND_CH8
    input3 = _PAR_CH8
    input4 = _BIN_CH8
    offset = _MODE
    output1 = _MODE_TRIG_CH8

# OR manual triggers (B2.1-B2.8) and FtL triggers with mode triggers
# _FTL_TRIG_CHx cables are defined in Task 14; DROID treats undefined cables as 0
[copy]
    input = _MODE_TRIG_CH1 + B2.1 + _FTL_TRIG_CH1
    output = _TRIG_CH1

[copy]
    input = _MODE_TRIG_CH2 + B2.2 + _FTL_TRIG_CH2
    output = _TRIG_CH2

[copy]
    input = _MODE_TRIG_CH3 + B2.3 + _FTL_TRIG_CH3
    output = _TRIG_CH3

[copy]
    input = _MODE_TRIG_CH4 + B2.4 + _FTL_TRIG_CH4
    output = _TRIG_CH4

[copy]
    input = _MODE_TRIG_CH5 + B2.5 + _FTL_TRIG_CH5
    output = _TRIG_CH5

[copy]
    input = _MODE_TRIG_CH6 + B2.6 + _FTL_TRIG_CH6
    output = _TRIG_CH6

[copy]
    input = _MODE_TRIG_CH7 + B2.7 + _FTL_TRIG_CH7
    output = _TRIG_CH7

[copy]
    input = _MODE_TRIG_CH8 + B2.8 + _FTL_TRIG_CH8
    output = _TRIG_CH8
```

Total: 8 switch + 8 copy = 16 circuits.

- [ ] **Step 2: Verify**

Patch loads. Pressing B2.1-B2.8 should now produce _TRIG_CH signals (not yet observable on outputs).

---

### Task 10: Envelopes — 8x Contour

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 9

- [ ] **Step 1: Write 8 contour circuits with spread math inline**

Spread weights per channel: 0.000, 0.143, 0.286, 0.429, 0.571, 0.714, 0.857, 1.000.

```ini
# ============================================================
# ENVELOPES (8x Rise-Fall)
# ============================================================

# Channel 1 (spread weight = 0.000 — no spread effect)
[contour]
    gate = _TRIG_CH1
    attack = P3.1
    decay = P3.2
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH1

# Channel 2 (spread weight = 0.143)
[contour]
    gate = _TRIG_CH2
    attack = P3.1 + 0.143 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.143 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH2

# Channel 3 (spread weight = 0.286)
[contour]
    gate = _TRIG_CH3
    attack = P3.1 + 0.286 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.286 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH3

# Channel 4 (spread weight = 0.429)
[contour]
    gate = _TRIG_CH4
    attack = P3.1 + 0.429 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.429 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH4

# Channel 5 (spread weight = 0.571)
[contour]
    gate = _TRIG_CH5
    attack = P3.1 + 0.571 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.571 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH5

# Channel 6 (spread weight = 0.714)
[contour]
    gate = _TRIG_CH6
    attack = P3.1 + 0.714 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.714 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH6

# Channel 7 (spread weight = 0.857)
[contour]
    gate = _TRIG_CH7
    attack = P3.1 + 0.857 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 0.857 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH7

# Channel 8 (spread weight = 1.000)
[contour]
    gate = _TRIG_CH8
    attack = P3.1 + 1.000 * (P3.6 - 0.5) * _SPREAD_DIR
    decay = P3.2 + 1.000 * (P3.7 - 0.5) * _SPREAD_DIR
    sustain = 0
    release = 0.001
    shape = (P2.1 - 0.5) * 2
    loop = _CYCLE_ALL
    retrigger = 1
    output = _ENV_CH8
```

Total: 8 contour circuits.

- [ ] **Step 2: Verify**

Patch loads. Manual triggers (B2.1-B2.8) should now generate envelopes on `_ENV_CH` cables. Not yet on physical outputs.

---

### Task 11: Oscillators — 8x LFO + Shape Switch

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 10

- [ ] **Step 1: Write 8 LFO circuits with spread on rate**

Each LFO outputs sawtooth, triangle, and ramp as native waveform outputs. Shape switch selects between them.

Note: DROID LFO has native `sawtooth` and `ramp` outputs — no copy/inversion needed.

```ini
# ============================================================
# OSCILLATORS (8x LFO) + SHAPE SWITCH
# ============================================================

# Channel 1 (spread weight = 0.000)
[lfo]
    hz = 0.1 + P3.4 * P3.4 * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH1
    triangle = _OSC_TRI_CH1
    ramp = _OSC_RAMP_CH1

[switch]
    input1 = _OSC_SAW_CH1
    input2 = _OSC_TRI_CH1
    input3 = _OSC_RAMP_CH1
    offset = P3.5
    output1 = _OSC_CH1

# Channel 2 (spread weight = 0.143)
[lfo]
    hz = 0.1 + (P3.4 + 0.143 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.143 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH2
    triangle = _OSC_TRI_CH2
    ramp = _OSC_RAMP_CH2

[switch]
    input1 = _OSC_SAW_CH2
    input2 = _OSC_TRI_CH2
    input3 = _OSC_RAMP_CH2
    offset = P3.5
    output1 = _OSC_CH2

# Channel 3 (spread weight = 0.286)
[lfo]
    hz = 0.1 + (P3.4 + 0.286 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.286 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH3
    triangle = _OSC_TRI_CH3
    ramp = _OSC_RAMP_CH3

[switch]
    input1 = _OSC_SAW_CH3
    input2 = _OSC_TRI_CH3
    input3 = _OSC_RAMP_CH3
    offset = P3.5
    output1 = _OSC_CH3

# Channel 4 (spread weight = 0.429)
[lfo]
    hz = 0.1 + (P3.4 + 0.429 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.429 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH4
    triangle = _OSC_TRI_CH4
    ramp = _OSC_RAMP_CH4

[switch]
    input1 = _OSC_SAW_CH4
    input2 = _OSC_TRI_CH4
    input3 = _OSC_RAMP_CH4
    offset = P3.5
    output1 = _OSC_CH4

# Channel 5 (spread weight = 0.571)
[lfo]
    hz = 0.1 + (P3.4 + 0.571 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.571 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH5
    triangle = _OSC_TRI_CH5
    ramp = _OSC_RAMP_CH5

[switch]
    input1 = _OSC_SAW_CH5
    input2 = _OSC_TRI_CH5
    input3 = _OSC_RAMP_CH5
    offset = P3.5
    output1 = _OSC_CH5

# Channel 6 (spread weight = 0.714)
[lfo]
    hz = 0.1 + (P3.4 + 0.714 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.714 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH6
    triangle = _OSC_TRI_CH6
    ramp = _OSC_RAMP_CH6

[switch]
    input1 = _OSC_SAW_CH6
    input2 = _OSC_TRI_CH6
    input3 = _OSC_RAMP_CH6
    offset = P3.5
    output1 = _OSC_CH6

# Channel 7 (spread weight = 0.857)
[lfo]
    hz = 0.1 + (P3.4 + 0.857 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 0.857 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH7
    triangle = _OSC_TRI_CH7
    ramp = _OSC_RAMP_CH7

[switch]
    input1 = _OSC_SAW_CH7
    input2 = _OSC_TRI_CH7
    input3 = _OSC_RAMP_CH7
    offset = P3.5
    output1 = _OSC_CH7

# Channel 8 (spread weight = 1.000)
[lfo]
    hz = 0.1 + (P3.4 + 1.000 * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + 1.000 * (P3.9 - 0.5) * _SPREAD_DIR) * 2000
    bipolar = _OSC_BIPOLAR
    sawtooth = _OSC_SAW_CH8
    triangle = _OSC_TRI_CH8
    ramp = _OSC_RAMP_CH8

[switch]
    input1 = _OSC_SAW_CH8
    input2 = _OSC_TRI_CH8
    input3 = _OSC_RAMP_CH8
    offset = P3.5
    output1 = _OSC_CH8
```

Total: 8 lfo + 8 switch (shape) = 16 circuits.

- [ ] **Step 2: Verify**

Patch loads without error.

---

### Task 12: Internal Mix + Pitch CV + Output Routing

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Tasks 10, 11

- [ ] **Step 1: Write internal mix, pitch CV, and output switch for all 8 channels**

Internal mix formula: `(env + osc * env * osc_depth) * strength * mute * trim`

Strength is bipolar (P3.3 center = zero). Osc depth spread uses weight * depth attenuverter.

```ini
# ============================================================
# OUTPUT MIXING + ROUTING
# ============================================================

# ----- Channel 1 (spread weight = 0.000) -----

# Internal: envelope + AM oscillation
[copy]
    input = (_ENV_CH1 + _OSC_CH1 * _ENV_CH1 * P2.2) * (P3.3 - 0.5) * 2 * S4.1 * P4.1
    output = _INT_CH1

# External: pitch CV
[copy]
    input = P3.4 * 5 * S4.1
    output = _EXT_CH1

# Output mode switch
[switch]
    input1 = _INT_CH1
    input2 = _EXT_CH1
    offset = _OUTPUT_MODE
    output1 = O1

# ----- Channel 2 (spread weight = 0.143) -----
[copy]
    input = (_ENV_CH2 + _OSC_CH2 * _ENV_CH2 * (P2.2 + 0.143 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.143 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.2 * P4.2
    output = _INT_CH2

[copy]
    input = (P3.4 + 0.143 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.2
    output = _EXT_CH2

[switch]
    input1 = _INT_CH2
    input2 = _EXT_CH2
    offset = _OUTPUT_MODE
    output1 = O2

# ----- Channel 3 (spread weight = 0.286) -----
[copy]
    input = (_ENV_CH3 + _OSC_CH3 * _ENV_CH3 * (P2.2 + 0.286 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.286 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.3 * P4.3
    output = _INT_CH3

[copy]
    input = (P3.4 + 0.286 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.3
    output = _EXT_CH3

[switch]
    input1 = _INT_CH3
    input2 = _EXT_CH3
    offset = _OUTPUT_MODE
    output1 = O3

# ----- Channel 4 (spread weight = 0.429) -----
[copy]
    input = (_ENV_CH4 + _OSC_CH4 * _ENV_CH4 * (P2.2 + 0.429 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.429 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.4 * P4.4
    output = _INT_CH4

[copy]
    input = (P3.4 + 0.429 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.4
    output = _EXT_CH4

[switch]
    input1 = _INT_CH4
    input2 = _EXT_CH4
    offset = _OUTPUT_MODE
    output1 = O4

# ----- Channel 5 (spread weight = 0.571) -----
[copy]
    input = (_ENV_CH5 + _OSC_CH5 * _ENV_CH5 * (P2.2 + 0.571 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.571 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.5 * P4.5
    output = _INT_CH5

[copy]
    input = (P3.4 + 0.571 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.5
    output = _EXT_CH5

[switch]
    input1 = _INT_CH5
    input2 = _EXT_CH5
    offset = _OUTPUT_MODE
    output1 = O5

# ----- Channel 6 (spread weight = 0.714) -----
[copy]
    input = (_ENV_CH6 + _OSC_CH6 * _ENV_CH6 * (P2.2 + 0.714 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.714 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.6 * P4.6
    output = _INT_CH6

[copy]
    input = (P3.4 + 0.714 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.6
    output = _EXT_CH6

[switch]
    input1 = _INT_CH6
    input2 = _EXT_CH6
    offset = _OUTPUT_MODE
    output1 = O6

# ----- Channel 7 (spread weight = 0.857) -----
[copy]
    input = (_ENV_CH7 + _OSC_CH7 * _ENV_CH7 * (P2.2 + 0.857 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 0.857 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.7 * P4.7
    output = _INT_CH7

[copy]
    input = (P3.4 + 0.857 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.7
    output = _EXT_CH7

[switch]
    input1 = _INT_CH7
    input2 = _EXT_CH7
    offset = _OUTPUT_MODE
    output1 = O7

# ----- Channel 8 (spread weight = 1.000) -----
[copy]
    input = (_ENV_CH8 + _OSC_CH8 * _ENV_CH8 * (P2.2 + 1.000 * (P3.10 - 0.5) * _SPREAD_DIR)) * ((P3.3 + 1.000 * (P3.8 - 0.5) * _SPREAD_DIR) - 0.5) * 2 * S4.8 * P4.8
    output = _INT_CH8

[copy]
    input = (P3.4 + 1.000 * (P3.9 - 0.5) * _SPREAD_DIR) * 5 * S4.8
    output = _EXT_CH8

[switch]
    input1 = _INT_CH8
    input2 = _EXT_CH8
    offset = _OUTPUT_MODE
    output1 = O8
```

Total: 16 copy + 8 switch = 24 circuits.

- [ ] **Step 2: First hardware test milestone**

Load patch. This is the first fully testable state:
- Set mode to Ch.Index (B1.3 first state)
- Turn P1.1 to select a channel
- Press B2.1-B2.8 manual triggers
- Observe CV on O1-O8 with oscilloscope or through a VCA
- Adjust Rise (P3.1), Fall (P3.2), Curve (P2.1) — should change envelope shape
- Adjust Rate (P3.4), Shape (P3.5), Osc depth (P2.2) — should add oscillation
- Toggle Spread (P1.2) and spread depths (P3.6-P3.10) — should create channel variation
- Toggle B1.7 for external osc mode — O1-O8 should output pitch CVs
- S4.1-S4.8 mute switches should silence individual channels

---

### Task 13: Gate Outputs (X7)

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 12

- [ ] **Step 1: Write gate outputs — envelope activity detection + mode switch**

```ini
# ============================================================
# GATE OUTPUTS (X7)
# ============================================================

# Envelope activity detection (internal mode: high while envelope active)
[compare]
    input = _ENV_CH1
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH1

[compare]
    input = _ENV_CH2
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH2

[compare]
    input = _ENV_CH3
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH3

[compare]
    input = _ENV_CH4
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH4

[compare]
    input = _ENV_CH5
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH5

[compare]
    input = _ENV_CH6
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH6

[compare]
    input = _ENV_CH7
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH7

[compare]
    input = _ENV_CH8
    compare = 0.01
    ifgreater = 1
    ifless = 0
    output = _ENV_GATE_CH8

# Gate output switch: internal=activity gate, external=trigger passthrough
[switch]
    input1 = _ENV_GATE_CH1
    input2 = _TRIG_CH1
    offset = _OUTPUT_MODE
    output1 = G1

[switch]
    input1 = _ENV_GATE_CH2
    input2 = _TRIG_CH2
    offset = _OUTPUT_MODE
    output1 = G2

[switch]
    input1 = _ENV_GATE_CH3
    input2 = _TRIG_CH3
    offset = _OUTPUT_MODE
    output1 = G3

[switch]
    input1 = _ENV_GATE_CH4
    input2 = _TRIG_CH4
    offset = _OUTPUT_MODE
    output1 = G4

[switch]
    input1 = _ENV_GATE_CH5
    input2 = _TRIG_CH5
    offset = _OUTPUT_MODE
    output1 = G5

[switch]
    input1 = _ENV_GATE_CH6
    input2 = _TRIG_CH6
    offset = _OUTPUT_MODE
    output1 = G6

[switch]
    input1 = _ENV_GATE_CH7
    input2 = _TRIG_CH7
    offset = _OUTPUT_MODE
    output1 = G7

[switch]
    input1 = _ENV_GATE_CH8
    input2 = _TRIG_CH8
    offset = _OUTPUT_MODE
    output1 = G8
```

Total: 8 compare + 8 switch = 16 circuits.

- [ ] **Step 2: Verify**

G1-G8 on X7 should go high when corresponding channels are active (internal mode) or when triggered (external mode).

---

### Task 14: Follow the Leader Cycle Chain

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 13 (needs _ENV_GATE_CH signals)

- [ ] **Step 1: Write FtL EOC detection and trigger chain**

Each channel detects when its envelope drops to zero (after being active), then triggers the next channel. Channel 8 wraps to channel 1.

```ini
# ============================================================
# FOLLOW THE LEADER CYCLE
# ============================================================

# Track "was active" state per channel and detect end-of-cycle.
# EOC triggers next channel, gated by _CYCLE_FTL.

# Ch1 → triggers Ch2
[flipflop]
    set = _TRIG_CH1
    reset = _FTL_EOC1
    output = _FTL_ACTIVE1

[compare]
    input = _ENV_CH1
    compare = 0.01
    ifless = _FTL_ACTIVE1
    ifgreater = 0
    output = _FTL_EOC1

[copy]
    input = _FTL_EOC1 * _CYCLE_FTL
    output = _FTL_TRIG_CH2

# Ch2 → triggers Ch3
[flipflop]
    set = _TRIG_CH2
    reset = _FTL_EOC2
    output = _FTL_ACTIVE2

[compare]
    input = _ENV_CH2
    compare = 0.01
    ifless = _FTL_ACTIVE2
    ifgreater = 0
    output = _FTL_EOC2

[copy]
    input = _FTL_EOC2 * _CYCLE_FTL
    output = _FTL_TRIG_CH3

# Ch3 → triggers Ch4
[flipflop]
    set = _TRIG_CH3
    reset = _FTL_EOC3
    output = _FTL_ACTIVE3

[compare]
    input = _ENV_CH3
    compare = 0.01
    ifless = _FTL_ACTIVE3
    ifgreater = 0
    output = _FTL_EOC3

[copy]
    input = _FTL_EOC3 * _CYCLE_FTL
    output = _FTL_TRIG_CH4

# Ch4 → triggers Ch5
[flipflop]
    set = _TRIG_CH4
    reset = _FTL_EOC4
    output = _FTL_ACTIVE4

[compare]
    input = _ENV_CH4
    compare = 0.01
    ifless = _FTL_ACTIVE4
    ifgreater = 0
    output = _FTL_EOC4

[copy]
    input = _FTL_EOC4 * _CYCLE_FTL
    output = _FTL_TRIG_CH5

# Ch5 → triggers Ch6
[flipflop]
    set = _TRIG_CH5
    reset = _FTL_EOC5
    output = _FTL_ACTIVE5

[compare]
    input = _ENV_CH5
    compare = 0.01
    ifless = _FTL_ACTIVE5
    ifgreater = 0
    output = _FTL_EOC5

[copy]
    input = _FTL_EOC5 * _CYCLE_FTL
    output = _FTL_TRIG_CH6

# Ch6 → triggers Ch7
[flipflop]
    set = _TRIG_CH6
    reset = _FTL_EOC6
    output = _FTL_ACTIVE6

[compare]
    input = _ENV_CH6
    compare = 0.01
    ifless = _FTL_ACTIVE6
    ifgreater = 0
    output = _FTL_EOC6

[copy]
    input = _FTL_EOC6 * _CYCLE_FTL
    output = _FTL_TRIG_CH7

# Ch7 → triggers Ch8
[flipflop]
    set = _TRIG_CH7
    reset = _FTL_EOC7
    output = _FTL_ACTIVE7

[compare]
    input = _ENV_CH7
    compare = 0.01
    ifless = _FTL_ACTIVE7
    ifgreater = 0
    output = _FTL_EOC7

[copy]
    input = _FTL_EOC7 * _CYCLE_FTL
    output = _FTL_TRIG_CH8

# Ch8 → wraps to Ch1
[flipflop]
    set = _TRIG_CH8
    reset = _FTL_EOC8
    output = _FTL_ACTIVE8

[compare]
    input = _ENV_CH8
    compare = 0.01
    ifless = _FTL_ACTIVE8
    ifgreater = 0
    output = _FTL_EOC8

[copy]
    input = _FTL_EOC8 * _CYCLE_FTL
    output = _FTL_TRIG_CH1
```

Total: 8 flipflop + 8 compare + 8 copy = 24 circuits.

- [ ] **Step 2: Verify**

Note: FtL triggers (`_FTL_TRIG_CHx`) are already wired into the trigger OR merge in Task 9. DROID treats undefined cables as 0, so they were inert until this task defined them.



Load patch. Enable Cycle (B1.4), set mode to FtL (B1.5). Trigger channel 1 (B2.1). Should see a cascade of envelopes rippling through channels 1→2→3→...→8→1.

---

### Task 15: Activity LEDs + Channel Index CV

**Files:**
- Modify: `droid-polimaths.ini`

**Depends on:** Task 14

- [ ] **Step 1: Write LED drivers and channel index CV**

```ini
# ============================================================
# ACTIVITY LEDs + CHANNEL INDEX
# ============================================================

# Channel activity LEDs (brightness = envelope level)
[copy]
    input = _ENV_CH1
    output = L2.1

[copy]
    input = _ENV_CH2
    output = L2.2

[copy]
    input = _ENV_CH3
    output = L2.3

[copy]
    input = _ENV_CH4
    output = L2.4

[copy]
    input = _ENV_CH5
    output = L2.5

[copy]
    input = _ENV_CH6
    output = L2.6

[copy]
    input = _ENV_CH7
    output = L2.7

[copy]
    input = _ENV_CH8
    output = L2.8

# Channel index CV (internal signal for future expansion)
# Encodes most recently triggered channel as 0.125V per channel
[copy]
    input = _ENV_GATE_CH1 * 0.125 + _ENV_GATE_CH2 * 0.250 + _ENV_GATE_CH3 * 0.375 + _ENV_GATE_CH4 * 0.500 + _ENV_GATE_CH5 * 0.625 + _ENV_GATE_CH6 * 0.750 + _ENV_GATE_CH7 * 0.875 + _ENV_GATE_CH8 * 1.000
    output = _CHANNEL_INDEX_CV
```

Total: 9 copy circuits.

- [ ] **Step 2: Final verification**

Load complete patch. All features should now be functional:
- L2.1-L2.8 should glow/pulse with envelope activity per channel
- All 4 activation modes should work via B1.3
- Cycle All (B1.4 + B1.5 state 0) should auto-cycle all channels
- Follow the Leader (B1.4 + B1.5 state 1) should cascade envelopes
- Spread (P1.2 + P3.6-P3.10) should create per-channel parameter variation
- Internal/External mode (B1.7) should switch between envelope+osc and pitch CV outputs
- Mutes (S4.1-S4.8) and trims (P4.1-P4.8) should work per channel

- [ ] **Step 3: Commit**

```bash
git add droid-polimaths.ini
git commit -m "Add PoliMATHS 8-channel CV event generator patch"
```

---

### Task 16: Update Patch Guide and README

**Files:**
- Modify: `patch-guide.md`
- Modify: `README.md`

**Depends on:** Task 15

- [ ] **Step 1: Add PoliMATHS entry to patch-guide.md**

Add a new section following the existing format with hardware requirements, I/O mapping, controls reference, and usage tips.

- [ ] **Step 2: Add PoliMATHS entry to README.md**

Add a one-line description to the patch list following existing format.

- [ ] **Step 3: Commit**

```bash
git add patch-guide.md README.md
git commit -m "Add PoliMATHS emulation to patch guide and README"
```

---

## Circuit Count Summary

| Task | Section | Circuits |
|------|---------|----------|
| 2 | Transport | 5 |
| 3 | Mode/cycle buttons | 9 |
| 4 | Spread pre-compute | 1 |
| 5 | Channel Index | 17 |
| 6 | Round | 19 |
| 7 | Parallel | 15 |
| 8 | Binary counter | 23 |
| 9 | Mode mux + manual OR | 16 |
| 10 | Envelopes | 8 |
| 11 | Oscillators + shape | 16 |
| 12 | Output mixing + routing | 24 |
| 13 | Gate outputs | 16 |
| 14 | Follow the Leader | 24 |
| 15 | LEDs + channel index | 9 |
| **Total** | | **194** |

**Note:** Exceeds the spec estimate of ~168 due to DROID lacking a demux circuit (threshold cascades needed for Channel Index and Round mode routing) and binary counter carry chain inversions.

**Optimization opportunities if circuit count is too high:**
1. **Drop Binary Counter mode** (-23 circuits, reduce mode switch to 3 inputs): saves 23
2. **Share demux between Ch.Index and Round** by routing both through a common span→channel converter: saves ~15
3. **Drop Follow the Leader** (-24 circuits): saves 24

With optimizations 1+2: ~156 circuits (comfortable).
With all optimizations: ~132 circuits (very comfortable).

The implementer should build Tasks 1-13 first (~170 circuits), test on hardware, then add Task 14 (FtL, +24 circuits) if circuit budget permits.
