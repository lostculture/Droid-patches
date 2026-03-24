# PoliMATHS Emulation — DROID Patch Design Spec

## Overview

Emulate Make Noise PoliMATHS — an 8-channel CV and audio event generator — as a DROID patch. Each channel generates a Rise-Fall envelope with a superimposed variable-rate oscillator (LFO through audio range). Channels are activated via multiple modes (Channel Index, Round, Parallel, Binary Counter) and parameters can be spread across channels for complex, evolving modulation.

Two output modes are switchable at runtime:
- **Internal Osc mode**: O1-O8 carry envelope+oscillation CVs, G1-G8 carry activity gates
- **External Osc mode**: O1-O8 carry 1V/oct pitch CVs (for driving external VCOs), G1-G8 carry activation gates (for triggering external envelopes/VCAs)

**Hardware constraint**: DROID has 8 continuous CV outputs (O1-O8). The X7 expander provides gate-only outputs (G1-G8). All design decisions respect this limit.

## Hardware

```
Controllers: [p2b8] [p2b8] [p10] [p8s8] [x7]
              C1      C2     C3    C4      C5
```

### I/O

| Jack | Function |
|------|----------|
| I1 | Activate (clock/gate — triggers channel activations) |
| I2 | Reset |
| I3 | Span CV (external modulation of channel selection) |
| I4 | Spread CV (external modulation of spread amount/direction) |
| O1-O8 | Channel 1-8 CV outputs (mode-dependent, see below) |
| G1-G8 | Channel 1-8 gates (via X7, mode-dependent, see below) |

Note: X7 gate outputs are addressed as `G1` through `G8` in DROID syntax (first X7 expander).

**Output modes (switched by B1.7):**

| Mode | O1-O8 | G1-G8 |
|------|-------|-------|
| Internal Osc | Envelope + oscillation mixed CV | Activity gates (high while envelope > 0) |
| External Osc | 1V/oct pitch CV per channel | Activation gates (trigger external envelopes) |

### Controller Mapping

**C1 (p2b8) — Transport & Mode:**

| Control | Function |
|---------|----------|
| P1.1 | Span (channel select / round step / parallel spread) |
| P1.2 | Spread amount + direction (center = none, CW = right channels, CCW = left channels) |
| B1.1 | Run/Stop toggle (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Mode select (4 states: Ch.Index / Round / Parallel / Binary Counter) |
| B1.4 | Cycle on/off toggle |
| B1.5 | Cycle mode (2 states: All / Follow the Leader) |
| B1.6 | Osc Bias (2 states: Unipolar / Bipolar) |
| B1.7 | Output mode (2 states: Internal Osc / External Osc) |
| B1.8 | (spare) |
| L1.3 | Mode indicator (brightness encodes mode: 0.25/0.5/0.75/1.0) |
| L1.4 | Cycle indicator |
| L1.5 | Cycle mode indicator |
| L1.6 | Osc bias indicator |
| L1.7 | Output mode indicator (off = internal, on = external) |

**C2 (p2b8) — Curve, Osc Mix & Manual Triggers:**

| Control | Function |
|---------|----------|
| P2.1 | Curve (envelope shape: log → linear → exponential) |
| P2.2 | Osc depth (oscillation mix into envelope, 0 = pure envelope) |
| B2.1-B2.8 | Manual trigger for channels 1-8 (momentary, OR'd with mode triggers) |
| L2.1-L2.8 | Channel activity LEDs (brightness = envelope level) |

**C3 (p10) — Main Parameters + Spread Depths:**

| Control | Function |
|---------|----------|
| P3.1 | Rise time (attack) |
| P3.2 | Fall time (decay/release) |
| P3.3 | Strength (amplitude + polarity: CCW = negative, center = zero, CW = positive) |
| P3.4 | Rate (oscillation frequency: ~0.1 Hz to ~2 kHz) / Pitch (0-5V in external mode) |
| P3.5 | Shape (oscillation waveform: saw / triangle / ramp — hard-switched at 3 positions) |
| P3.6 | Rise spread depth (attenuverter: center = no spread) |
| P3.7 | Fall spread depth (attenuverter: center = no spread) |
| P3.8 | Strength spread depth |
| P3.9 | Rate/Pitch spread depth |
| P3.10 | Osc depth spread depth |

**C4 (p8s8) — Per-Channel Controls:**

| Control | Function |
|---------|----------|
| P4.1-P4.8 | Per-channel level trim (fine amplitude adjust) |
| S4.1-S4.8 | Per-channel mute switches (up = active, down = muted) |

## Signal Flow

### 1. Transport & Clock

```
Internal LFO ──► N1 (normaled to I1 when I1 unpatched)
I1 (Activate) ──► gated by _RUNNING ──► _ACTIVATE
I2 (Reset) + B1.2 ──► OR ──► _RESET
```

Circuits: 1x `[lfo]` (internal clock → N1), 1x `[button]` (B1.1 → _RUNNING), 1x `[button]` (B1.2 momentary → _RESET_BTN), 2x `[copy]` (gate clock, merge reset).

### 2. Activation Modes

Mode selected by B1.3 (4 states, cycling through modes). Mode state stored via `[button]` with `states = 4`, output `_MODE` (0, 0.333, 0.667, 1.0).

Each mode generates per-channel trigger signals `_MODE_TRIG_CH1` through `_MODE_TRIG_CH8`. These are OR'd with manual triggers (B2.1-B2.8) to produce final `_TRIG_CH{i}`:

```
_TRIG_CH{i} = _MODE_TRIG_CH{i} + B2.{i}
```

This requires 8x `[copy]` circuits (one per channel) for the OR merge.

**Channel Index (Mode 0):**
- Combined span: `_SPAN = P1.1 + I3 * _SPAN_ATTEN` (where _SPAN_ATTEN is the Span CV attenuverter — uses P1.1 range directly since no separate attenuverter pot is available; I3 is additive)
- Quantized to 8 zones using a `[switch]` with 8 outputs, or 7x `[compare]` thresholds
- Implementation: `[pot]` with `discrete = 8` on P1.1 gives clean 8-position quantization; combined with I3 via `[copy]` before the pot circuit
- Each activation trigger fires only the selected channel
- Generates `_MODE_TRIG_CH{i}` = `_ACTIVATE * _CH{i}_SELECTED`

**Round (Mode 1):**
- 8-step `[sequencer]` acts as position counter, clocked by `_ACTIVATE`
- Step values encode channel number (cv1=1, cv2=2, ... cv8=8), output feeds channel selection
- Span pot controls step size by clocking the sequencer multiple times (via `[clocktool]` multiply) or by using a variable-step approach
- Simplified: Span selects which of several pre-defined step patterns to use (1,2,3,4 step sizes via `[switch]`)
- Reset returns to step 1

**Parallel (Mode 2):**
- 8x `[clocktool]` circuits, each dividing `_ACTIVATE` by a different ratio
- Division ratios set by Span pot via `[switch]`:
  - Center: all /1
  - CW: Ch1=/1, Ch2=/1, Ch3=/2, Ch4=/2, Ch5=/4, Ch6=/4, Ch7=/8, Ch8=/8
  - Full CW: Ch1=/1, Ch2=/2, Ch3=/3, Ch4=/4, Ch5=/5, Ch6=/6, Ch7=/7, Ch8=/8
- Reset resyncs all dividers

**Binary Counter (Mode 3):**
- Uses a chain of 8x `[flipflop]` circuits to create an 8-bit binary counter
- Ch1 flipflop toggles on every `_ACTIVATE` trigger
- Ch2 flipflop toggles when Ch1 transitions high→low (carry bit)
- Ch3 flipflop toggles on Ch2's carry, etc.
- Each flipflop's rising edge (0→1 transition) generates the channel trigger
- Rising edge detection: `[compare]` on each flipflop output minus its previous-frame value, or simpler: use the flipflop output directly as a gate (channel is "active" while bit is high)
- Reset zeroes all flipflops
- Total: 8x `[flipflop]`, 8x edge detection circuits (~16 circuits)

**Mode multiplexing:**
- 4x `[switch]` per channel selects between the 4 mode outputs based on `_MODE`
- Or: 8x `[switch]` with 4 inputs each (one per mode's trigger for that channel)
- Total: 8x `[switch]` for mode mux + 8x `[copy]` for manual trigger OR = 16 circuits

### 3. Spread Calculation

Spread modulates 5 parameters differently per channel based on channel position.

```
# Spread direction from pot + CV input
_SPREAD_RAW = P1.2 + I4          # P1.2 center = 0.5 = no spread; I4 adds modulation
_SPREAD_DIR = (_SPREAD_RAW - 0.5) * 2    # Normalize to -1 to +1

# Per-channel weight (constants, computed inline):
#   Channel 0: weight = 0/7 = 0.000
#   Channel 1: weight = 1/7 = 0.143
#   Channel 2: weight = 2/7 = 0.286
#   ...
#   Channel 7: weight = 7/7 = 1.000
#
# When _SPREAD_DIR > 0: rightmost channels (high weight) get most spread
# When _SPREAD_DIR < 0: leftmost channels get most spread (weight inverted)
#
# Effective weight for channel i:
#   if _SPREAD_DIR >= 0: eff_weight = i/7
#   if _SPREAD_DIR <  0: eff_weight = (7-i)/7
#
# Simplified inline formula (works for both directions):
#   spread_offset = abs(_SPREAD_DIR) * eff_weight * depth_attenuverter

# For each spreadable parameter, per channel:
rise_ch[i]     = P3.1 + (i/7) * (P3.6 - 0.5) * _SPREAD_DIR
fall_ch[i]     = P3.2 + (i/7) * (P3.7 - 0.5) * _SPREAD_DIR
strength_ch[i] = P3.3 + (i/7) * (P3.8 - 0.5) * _SPREAD_DIR
rate_ch[i]     = P3.4 + (i/7) * (P3.9 - 0.5) * _SPREAD_DIR
osc_ch[i]      = P2.2 + (i/7) * (P3.10 - 0.5) * _SPREAD_DIR
```

The `(i/7)` factor is a constant per channel (0.000, 0.143, 0.286, 0.429, 0.571, 0.714, 0.857, 1.000). When `_SPREAD_DIR` is positive, higher-numbered channels get more offset. When negative, the multiplication naturally inverts: channel 7 gets the largest negative offset, effectively spreading leftward.

The depth attenuverters (P3.6-P3.10) are bipolar around center (0.5). At center, `(depth - 0.5) = 0`, so no spread occurs for that parameter regardless of _SPREAD_DIR.

Spread math is computed inline within contour/lfo parameter expressions — no separate circuits needed. One `[copy]` circuit pre-computes `_SPREAD_DIR` from P1.2 + I4.

### 4. Per-Channel Envelope

8x `[contour]` circuits configured as Rise-Fall (AR) envelopes:

```ini
[contour]
    gate = _TRIG_CH{i}                              # From mode router + manual OR
    attack = P3.1 + {i/7} * (P3.6 - 0.5) * _SPREAD_DIR   # Rise + spread
    decay = P3.2 + {i/7} * (P3.7 - 0.5) * _SPREAD_DIR    # Fall + spread
    sustain = 0                                       # No sustain = immediate fall
    release = 0.001                                   # Near-instant release
    shape = (P2.1 - 0.5) * 2                         # Curve: bipolar mapping (log↔exp)
    loop = _CYCLE_ALL                                 # Self-retrigger in Cycle All mode
    retrigger = 1                                     # Allow retrigger during envelope
    output = _ENV_CH{i}
```

**Cycle logic for `_CYCLE_ALL`:**
```
_CYCLE_ON = B1.4 output (toggle)
_CYCLE_MODE = B1.5 output (0 = All, 1 = FtL)
_CYCLE_ALL = _CYCLE_ON * (1 - _CYCLE_MODE)     # Only active when Cycle ON and mode = All
```
This requires 2x `[button]` + 1x `[copy]`.

### 5. Per-Channel Oscillator (Internal Osc Mode)

8x `[lfo]` circuits with audio-rate capability:

```ini
[lfo]
    hz = 0.1 + (P3.4 + {i/7} * (P3.9 - 0.5) * _SPREAD_DIR) * (P3.4 + ...) * 2000
    bipolar = _OSC_BIPOLAR
    triangle = _OSC_CH{i}
```

**Rate scaling:** Quadratic response `hz = 0.1 + rate^2 * 2000` gives ~0.1 Hz to ~2 kHz. Bipolar mode (B1.6) doubles the range.

**Shape selection:** P3.5 hard-switches between 3 waveforms using a `[switch]` per channel:
```ini
[switch]
    input1 = _OSC_SAW_CH{i}     # P3.5 < 0.33
    input2 = _OSC_TRI_CH{i}     # P3.5 0.33-0.67
    input3 = _OSC_RAMP_CH{i}    # P3.5 > 0.67
    offset = P3.5
    output1 = _OSC_SHAPED_CH{i}
```

However, to save circuits we can output only `triangle` from each LFO and use the `[fold]` or inline math to approximate shape morphing. Or: output all three waveforms from each LFO and switch. Since LFO can output multiple waveforms simultaneously at no extra circuit cost, the switch approach costs only 8 `[switch]` circuits.

**Trade-off note:** 8 LFOs at audio rate run continuously even when their channel's envelope is at zero. This is an accepted CPU trade-off — the DROID handles this load in practice, but it should be tested. The LFO output is gated by the envelope in the mix stage, so inaudible channels produce no output.

### 6. Per-Channel Pitch CV (External Osc Mode)

In External Osc mode, P3.4 becomes base pitch and Rate Spread (P3.9) creates per-channel intervals:

```
pitch_ch[i] = (P3.4 + {i/7} * (P3.9 - 0.5) * _SPREAD_DIR) * 5
```

Range: 0-5V (5 octaves). Spread on Rate creates chord voicings or detuning.

Computed by 8x `[copy]` circuits.

### 7. Output Routing (Mode Switch)

B1.7 selects between output configurations via `_OUTPUT_MODE` (0 = internal, 1 = external).

**Internal Osc mode (_OUTPUT_MODE = 0):**
```
_INTERNAL_CH{i} = (_ENV_CH{i} + _OSC_SHAPED_CH{i} * _ENV_CH{i} * osc_ch[i]) * strength_ch[i] * S4.{i} * P4.{i}
```

The oscillation is amplitude-modulated by the envelope (envelope gates the osc), matching PoliMATHS where oscillation exists within the envelope shape.

**External Osc mode (_OUTPUT_MODE = 1):**
```
_EXTERNAL_CH{i} = pitch_ch[i] * S4.{i}
```

**Output switch (8x `[switch]`):**
```ini
[switch]
    input1 = _INTERNAL_CH{i}
    input2 = _EXTERNAL_CH{i}
    offset = _OUTPUT_MODE
    output1 = O{i}
```

**Gate outputs (8x `[copy]` or `[compare]`):**
```ini
# Internal mode: activity gate (envelope > threshold)
# External mode: raw activation trigger passthrough
[switch]
    input1 = _ENV_GATE_CH{i}       # compare: _ENV_CH{i} > 0.01
    input2 = _TRIG_CH{i}           # raw trigger
    offset = _OUTPUT_MODE
    output1 = G{i}
```

Total: 8x `[switch]` (CV output), 8x `[compare]` (envelope gate detection), 8x `[switch]` (gate output) = 24 circuits. Can be reduced by computing envelope gates inline.

### 8. Cycle Modes

**Cycle All:**
- `_CYCLE_ALL` signal (computed in Section 4) enables `loop` on all contours
- Each channel self-retriggers on envelope completion
- All 8 channels cycle independently at their own Rise+Fall rates
- Spread on Rise/Fall creates polyrhythmic cycling across channels

**Follow the Leader:**
- When cycle is ON and mode = FtL: channel N's envelope completing triggers channel N+1
- EOC detection: `[compare]` checks `_ENV_CH{i} < 0.01` while `_WAS_ACTIVE_CH{i} = 1`
- "Was active" tracked by `[flipflop]`: set when triggered, reset when envelope falls below threshold
- Channel 8 wraps to channel 1
- Implementation per channel:

```ini
# Track "was active" state
[flipflop]
    set = _TRIG_CH{i}
    reset = _EOC_CH{i}
    output = _WAS_ACTIVE_CH{i}

# Detect end-of-cycle (envelope near zero AND was active)
[compare]
    input = _ENV_CH{i}
    compare = 0.01
    ifless = _WAS_ACTIVE_CH{i}     # Only fire if was active
    ifgreater = 0
    output = _EOC_CH{i}

# EOC triggers next channel (only in FtL mode)
# _FTL_TRIG_CH{i+1} = _EOC_CH{i} * _CYCLE_FTL
```

`_CYCLE_FTL = _CYCLE_ON * _CYCLE_MODE` (active when Cycle ON and mode = FtL).

FtL triggers are OR'd into each channel's trigger chain. Total: 8x `[flipflop]` + 8x `[compare]` + 8x `[copy]` = 24 circuits.

### 9. Activity LEDs

```ini
[copy]
    input = _ENV_CH{i}
    output = L2.{i}           # Brightness tracks envelope level
```

8x `[copy]` circuits.

### 10. Channel Index Output

Internal signal `_CHANNEL_INDEX_CV` represents the most recently activated channel as a voltage (0.125V per channel: Ch1=0.125, Ch2=0.25, ... Ch8=1.0).

This is an internal cable only — no spare CV output jack is available. Can be used for internal routing or future expansion.

Computed by 1x `[copy]` that updates on each activation.

## Feature Comparison

| PoliMATHS Feature | DROID Implementation | Fidelity |
|-------------------|---------------------|----------|
| 8 Rise-Fall envelopes | 8x contour (AR mode) | High |
| Per-channel oscillators (LFO to audio) | 8x lfo with quadratic rate scaling | High |
| External VCO control (1V/oct) | Switchable pitch CV mode on O1-O8 | High |
| Envelope * Oscillation mix | Inline math per channel | High |
| Strength (bipolar amplitude) | Bipolar math on output | High |
| Spread modulation (5 params x 8 ch) | Inline math with constant channel weights | High |
| Spread CV input | I4 added to P1.2 in spread formula | High |
| Channel Index activation | Discrete pot quantization + compare | High |
| Round activation | Sequencer counter with variable step | High |
| Parallel activation (clock divs) | 8x clocktool with span-selected ratios | High |
| Binary Counter activation | 8x flipflop cascade | High |
| Cycle All | contour loop parameter | Exact |
| Follow the Leader | compare + flipflop EOC chain | Approximate |
| Curve control | contour shape with bipolar mapping | High |
| Osc Shape (saw/tri/ramp) | Hard-switch between 3 LFO outputs | Medium |
| Osc Bias (uni/bipolar) | lfo bipolar parameter | Exact |
| Per-channel mutes | p8s8 toggle switches | High |
| Per-channel trim | p8s8 pots | High |
| Channel activity LEDs | p2b8 LED brightness = envelope level | High |
| Activity/trigger gates | X7 gate outputs (mode-dependent) | High |
| Manual channel triggers | B2.1-B2.8 OR'd with mode triggers | High |
| Span CV input | I3 summed with Span pot | High |
| Modulation Dissemination | Not implemented (v2 candidate) | None |
| Accumulate | Not implemented (v2 candidate) | None |
| Submixing | Not implemented (v2 candidate) | None |

## Estimated Circuit Count

| Section | Count | Types |
|---------|-------|-------|
| Controller declarations | 5 | p2b8, p2b8, p10, p8s8, x7 |
| Transport (clock, run, reset) | 5 | lfo, button x2, copy x2 |
| Mode + cycle buttons | 7 | button x5, copy x2 (_CYCLE_ALL, _CYCLE_FTL) |
| Spread pre-compute | 1 | copy (_SPREAD_DIR from P1.2 + I4) |
| Channel Index routing | 9 | pot (discrete), compare x8 |
| Round counter | 4 | sequencer, clocktool, switch, copy |
| Parallel dividers | 8 | clocktool x8 |
| Binary counter | 16 | flipflop x8, compare/copy x8 (edge detect) |
| Mode mux + manual OR | 16 | switch x8 (mode select), copy x8 (manual OR) |
| Envelopes | 8 | contour x8 |
| Oscillators | 8 | lfo x8 |
| Shape switch | 8 | switch x8 |
| Pitch CV (external) | 8 | copy x8 |
| Internal mix | 8 | copy x8 |
| Output mode switch | 16 | switch x8 (CV), switch x8 (gate) |
| Envelope gate detect | 8 | compare x8 |
| FtL cycle chain | 24 | flipflop x8, compare x8, copy x8 |
| Activity LEDs | 8 | copy x8 |
| Channel index CV | 1 | copy |
| **Total** | **~168** | |

**RAM optimization opportunities:**
- FtL cycle chain (24 circuits) could be deferred to v2 if count is too high, saving ~24
- Binary counter (16 circuits) could be dropped to 3 modes, saving ~16
- With both deferred: ~128 circuits (comfortable)
- Shape switch could use inline expressions instead of separate circuits in some cases

## Omitted Features (v2 Candidates)

- **Modulation Dissemination**: Would require 5x `[sample]` per channel (40 total) to capture CV at activation time. Powerful but pushes circuit count very high.
- **Accumulate**: Requires per-channel gate buffering with coordinated release. Complex state management.
- **Submixing**: Would need conditional signal routing based on which outputs are patched. DROID cannot detect patching state.
- **Smooth shape morphing**: Replace 8x hard-switch with 16x crossfader for smooth saw↔tri↔ramp transitions.
