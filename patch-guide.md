# DROID Patch Guide

## Patches

| File | Description |
|------|-------------|
| `droid-4track-sequencer.ini` | 4-track generative sequencer (base patch) |
| `droid-4track-plainbob.ini` | 4-track sequencer with Plain Bob pitch rotation |
| `tintinnalogia-8bell-plainbob.ini` | 8-bell change ringing sequencer (3 methods) |
| `droid-shift-register.ini` | 6-stage CV shift register (port of disting NT) |
| `droid-quad-bernoulli.ini` | 4-channel probabilistic gate (port of disting NT) |
| `droid-clep-disting.ini` | Multi-mode CV generator: step/random/LFO (port of disting NT) |
| `droid-random-stepped-voltage.ini` | Random stepped voltage with freeze/auto-randomize (port of disting NT) |
| `droid-quad-snh.ini` | Quad sample & hold at staggered clock divisions (inspired by disting NT) |
| `droid-no-control.ini` | Variable-timing self-clocking trigger sequencer (port of disting NT) |
| `droid-sync-latch.ini` | Musical boundary transport sync (port of disting NT) |
| `droid-bouncing-ball.ini` | Classic bouncing ball trigger generator with decay and gravity |
| `droid-maths-classics.ini` | Multi-function utility: quadrature LFO, arcade trill, VC slew, pulse delay, clock divider |
| `droid-zularic-repetitor.ini` | Multi Repetitor — 3-bank rhythmic gate generator (ZR / Numeric / Euclidean) |
| `droid-mi-grids.ini` | MI Grids clone — topographic drum sequencer with XY morphing, density, and chaos |
| `droid-cv-recorder.ini` | Dual-channel CV recorder / looper (inspired by Bishop's Miscellany) |

---

## droid-4track-sequencer.ini

A 4-track algorithmic sequencer using `[algoquencer]` circuits. Each track generates independent pitch, gate, and accent patterns with per-track controls via a P10 overlay.

### Hardware

4 controllers: p2b8, p2b8, p10, b32

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | External Clock | Normaled to internal LFO when unpatched |
| I2 | External Reset | Combined with B1.2 button |

### Outputs

| Jack | Signal |
|------|--------|
| O1-O4 | Track 1-4 Pitch CV (quantized to scale) |
| O5-O8 | Track 1-4 Accent CV |
| G1-G4 | Track 1-4 Gates |

### Controls

**Controller 1 (p2b8) — Transport**

| Control | Function |
|---------|----------|
| P1.1 | Tempo (internal LFO rate) |
| P1.2 | *unused* |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Reroll all patterns (momentary) |
| B1.4 | *unused* |
| B1.5-B1.8 | Mute Track 1-4 (LED on = unmuted) |

**Controller 2 (p2b8) — Performance**

| Control | Function |
|---------|----------|
| P2.1 | Root Note (12 semitones, notched) |
| P2.2 | Scale Type (16 scales, notched) |
| B2.1-B2.4 | Fill Track 1-4 (momentary, forces all gates on) |
| B2.5-B2.8 | Select Track 1-4 (for P10 overlay) |

**Controller 3 (p10) — Per-Track Parameters (overlaid by track select)**

| Control | Function | Default |
|---------|----------|---------|
| P3.1 | Activity (pattern density) | 50% |
| P3.2 | Variation (pattern randomness) | 30% |
| P3.3 | Steps (1-8, notched) | 8 |
| P3.4 | Gate Length | 50% |
| P3.5 | Dejavu (pattern memory) | 50% |
| P3.6 | Morphs (gradual pattern change) | 30% |
| P3.7 | Rolls (global, all tracks) | — |

**Controller 4 (b32) — Step Buttons**

| Buttons | Track |
|---------|-------|
| B4.1-B4.8 | Track 1 step toggles + position LEDs |
| B4.9-B4.16 | Track 2 |
| B4.17-B4.24 | Track 3 |
| B4.25-B4.32 | Track 4 |

---

## droid-4track-plainbob.ini

Same as above, plus **Plain Bob Minimus** pitch rotation. The 4 melodic lines weave between outputs following the change ringing algorithm, while gates and accents stay on their original tracks.

### Additional Controls

| Control | Function |
|---------|----------|
| P1.2 | Permutation Rate — how many clock steps between swaps (4 to 32, notched in 8 positions) |
| B1.4 | Plain Bob On/Off (LED = active) |

### How It Works

- When **B1.4 is off**: outputs route normally (Track 1 pitch to O1, etc.)
- When **B1.4 is on**: every N clock steps (set by P1.2), adjacent pitch outputs swap following the Plain Bob pattern
- **Reset** (B1.2) returns to identity routing (each track on its own output)
- The rotation freezes when B1.4 is toggled off, preserving the current permutation

### Plain Bob Minimus Pattern

12 changes per lead, 24 changes (2 leads) for a full course back to identity:

```
Cross:    swap (1,2) and (3,4)
14:       keep 1 & 4, swap (2,3)
Lead-end: keep 1 & 2, swap (3,4)

Sequence: cross, 14, cross, 14, cross, 14,
          cross, 14, cross, 14, cross, lead-end
          (repeat)
```

### Outputs (same jacks, different routing)

| Jack | Signal |
|------|--------|
| O1-O4 | **Permuted** pitch CV — which track plays here changes over time |
| O5-O8 | Track 1-4 Accent CV (always on original track) |
| G1-G4 | Track 1-4 Gates (always on original track) |

---

## tintinnalogia-8bell-plainbob.ini

A change ringing sequencer that plays 8 bells in sequence, permuting their order according to traditional English bell-ringing methods. Three methods available: Plain Hunt, Grandsire, and Plain Bob.

### Hardware

4 controllers: p2b8, p2b8, p10, b32

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | External Clock | Normaled to internal LFO when unpatched |
| I2 | Reset to Rounds | Returns bells to natural order (1-2-3-4-5-6-7-8) |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Pitch CV — current bell, quantized to selected scale |
| O2 | Row Marker — trigger at start of each new row |
| O3 | Combined Gate — all bell strikes |
| G1-G8 | Individual bell triggers (G1 = bell 1/treble, G8 = bell 8/tenor) |

### Controls

**Controller 1 (p2b8) — Transport**

| Control | Function |
|---------|----------|
| P1.1 | Tempo |
| P1.2 | Root Note (12 semitones, notched) |
| B1.1 | Run/Stop |
| B1.2 | Reset to Rounds |
| B1.3 | Start/Stop Changes (toggle — bells ring in current order until enabled) |

**Controller 2 (p2b8) — Method & Scale**

| Control | Function |
|---------|----------|
| P2.1 | Scale Type (16 scales, notched) |
| B2.1 | Plain Hunt (method select, default) |
| B2.2 | Grandsire (method select) |
| B2.3 | Plain Bob (method select) |

**Controller 4 (b32) — Visualization**

| LEDs | Function |
|------|----------|
| L4.1-L4.8 | Bell order — brightness shows which bell is at each position (bright = treble, dim = tenor) |
| L4.9-L4.16 | Bell strikes — flash when each bell sounds (L4.9 = bell 1 through L4.16 = bell 8) |

### Methods

**Plain Hunt** — 16-change cycle
- Odd rows: swap pairs (1,2), (3,4), (5,6), (7,8)
- Even rows: swap pairs (2,3), (4,5), (6,7); positions 1 & 8 stay

**Grandsire** — 3-state cycle on 7 bells (bell 8/tenor fixed)
- State "3": swap (1,2), keep 3, swap (4,5), (6,7)
- State "1": keep 1, swap (2,3), (4,5), (6,7)
- State "N": swap (1,2), (3,4), (5,6), keep 7

**Plain Bob Major** — 12-change lead, 7 leads = 84 changes for full course
- Cross: swap all pairs (1,2), (3,4), (5,6), (7,8)
- 1N: keep 1 & 8, swap (2,3), (4,5), (6,7)
- Lead end: keep 1 & 2, swap (3,4), (5,6), (7,8)
- Pattern: cross, 1N, cross, 1N, ..., cross, **lead-end** (repeat)

### Usage Tips

1. Start with B1.3 off — bells ring rounds (1-2-3-4-5-6-7-8 repeating)
2. Select a method with B2.1/B2.2/B2.3
3. Press B1.3 to start changes — bell order begins permuting
4. Watch the B32 LEDs: row 1 shows current order, row 2 shows strike pattern
5. Press B1.2 (reset) to return to rounds at any time
6. Always reset after switching methods to clear the state

---

## droid-shift-register.ini

A 6-stage CV shift register ported from the disting NT `shift_register.lua` by Thorinside. On each trigger, the input CV shifts down through 6 stages. Internal random CV and clock are normaled when inputs are unpatched, making it immediately usable standalone. Optional feedback loops stage 6 back to the input for repeating patterns.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | CV Input | Normaled to internal random (range set by P1.2) |
| I2 | Trigger Input | Normaled to internal clock (rate set by P1.1) |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Stage 1 (newest value) |
| O2 | Stage 2 |
| O3 | Stage 3 |
| O4 | Stage 4 |
| O5 | Stage 5 |
| O6 | Stage 6 (oldest value) |
| O7 | Trigger pass-through |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate (internal clock speed) |
| P1.2 | Random Range (0 = silent, full = 10 octaves) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (clear all stages to 0) |
| B1.3 | Feedback (LED on = stage 6 loops back to input) |

### Usage Tips

1. **Standalone generative**: Leave inputs unpatched. Random CV feeds stage 1, internal clock shifts values down. Patch O1-O6 through quantizers to VCOs for 6-voice evolving melody.
2. **External CV processing**: Patch a pitch CV to I1 and a clock/trigger to I2. The register creates delayed copies of the input, great for canons or echo effects.
3. **Feedback loops**: Toggle B1.3 on — stage 6 feeds back to stage 1, creating a 6-step repeating loop. New values stop entering; the pattern circulates indefinitely.
4. **Frozen snapshots**: Stop the clock (B1.1 off) to freeze all 6 stages at their current values. Useful for holding a chord or a set of CVs.

### Technical Notes

Stages are processed in reverse order (6 first, 1 last) so each stage latches the previous stage's old value before it gets updated in the same frame. This is a standard DROID technique for shift registers using `[sample]` circuits.

---

## droid-quad-bernoulli.ini

A 4-channel probabilistic gate processor ported from the disting NT `quad_bernoulli.lua` by Thorinside. Each incoming gate is randomly passed or blocked based on a global probability setting. Normaled to polyrhythmic clock divisions when inputs are unpatched.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Gate 1 | Normaled to internal clock |
| I2 | Gate 2 | Normaled to clock /2 |
| I3 | Gate 3 | Normaled to clock /3 |
| I4 | Gate 4 | Normaled to clock /4 |

### Outputs

| Jack | Signal |
|------|--------|
| O1-O4 | Passed gates (probability check succeeded) |
| O5-O8 | Rejected gates (complement of O1-O4) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate (internal clock, for normalization) |
| P1.2 | Probability (0% = block all, 100% = pass all) |
| B1.1-B1.4 | Bypass Ch 1-4 (LED on = always passes, ignores probability) |
| L1.5-L1.8 | Output activity Ch 1-4 (LED flashes when gate passes) |

### Usage Tips

1. **Standalone rhythm generator**: Leave inputs unpatched. The 4 channels get polyrhythmic divisions (x1, /2, /3, /4) of the internal clock. Turn P1.2 to thin out the pattern. Patch O1-O4 to drum triggers.
2. **Probability filter**: Patch your sequencer's gates to I1-I4. Sweep P1.2 to gradually drop notes. At 50%, roughly half the gates pass through.
3. **Complementary outputs**: O5-O8 get the gates that O1-O4 reject. Patch both to different sound sources for call-and-response textures.
4. **Per-channel bypass**: Toggle B1.1-B1.4 to force specific channels to always pass, keeping a steady kick while other parts thin out.
5. **Chain with shift register**: Use the shift register's trigger output (O7) as a clock source, and its stage outputs as CV while the bernoulli gates decide which notes sound

---

## droid-clep-disting.ini

A multi-mode clocked CV generator ported from the disting NT `clep_disting.lua` by Thorinside. Three switchable modes — algorithmic step sequence, pure random, and stepped sine LFO — with optional scale quantization.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Clock | Normaled to internal LFO (rate set by P1.1) |
| I2 | Reset | Returns to step 1 |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | CV Output (selected mode, optionally quantized) |
| O2 | Gate (step mode = rhythmic pattern, random/LFO = every step) |
| O3 | BOC Trigger (beginning of cycle, once per N steps) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate |
| P1.2 | Steps (1-8, notched) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Mode: Step (default) |
| B1.4 | Mode: Random |
| B1.5 | Mode: LFO |
| B1.6 | Reroll (randomize step sequence) |
| B1.7 | Quantize On/Off (LED on = quantized to Locrian scale) |

### Modes

**Step** — Algorithmic sequence (algoquencer). Generates a random pitch pattern that it remembers (dejavu = 1). Press B1.6 (Reroll) to generate a new pattern. Activity is set to 70%, so the gate output has rhythmic variety. The P1.2 step count sets sequence length.

**Random** — Pure random CV on each clock step. Every step generates a completely new value. Gate fires on every step. Good for chaotic generative textures.

**LFO** — 8-point stepped sine wave. The step count (P1.2) determines how many points of the sine play: 8 steps = full cycle, 4 steps = positive half only, fewer steps = partial wave fragments. Gate fires on every step.

### Usage Tips

1. **Quick generative melody**: Select Step mode (B1.3), set 8 steps (P1.2 full), quantize on (B1.7). Patch O1 to a VCO and O2 to a VCA gate. Hit B1.6 to reroll until you like the sequence.
2. **Evolving random**: Select Random mode (B1.4). Every clock step is a surprise. Quantize on keeps it musical.
3. **Stepped modulation**: Select LFO mode (B1.5), quantize off (B1.7). Patch O1 to filter cutoff or other modulation targets. Adjust step count for sine resolution.
4. **BOC sync**: Patch O3 to another module's reset input to sync sequence lengths. The BOC trigger fires once per cycle (every N steps).
5. **External clock**: Patch a clock source to I1 for tempo-synced CV generation. Use I2 for phrase-aligned resets

---

## droid-random-stepped-voltage.ini

A remembered random CV sequence ported from the disting NT `ae_random_stepped_voltage.lua` by Andras Eichstaedt / Thorinside. The sequence repeats until rerolled. Freeze pauses the sequence in place without stopping the clock. Auto-randomize generates a fresh pattern each cycle. Slew smooths transitions between steps.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Clock | Normaled to internal LFO (rate set by P1.1) |
| I2 | Reset | Returns to step 1 |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | CV Output (quantized to scale, optionally slewed) |
| O2 | Gate (fires every step) |
| O3 | BOC Trigger (beginning of cycle) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate |
| P1.2 | Steps (1-8, notched) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Freeze (LED on = sequence paused in place) |
| B1.4 | Reroll (new random sequence) |
| B1.5 | Auto-randomize (LED on = new pattern each cycle) |
| B1.6 | Slew (LED on = smooth transitions between steps) |

### Usage Tips

1. **Repeating random melody**: Set steps (P1.2), let it run. The sequence repeats the same random pattern. Hit B1.4 to reroll until you like it.
2. **Freeze for performance**: Toggle B1.3 to freeze the sequence mid-phrase. The clock keeps running but the CV holds at the current step. Unfreeze to resume from where you left off.
3. **Evolving sequences**: Toggle B1.5 (auto-randomize) on. Every time the sequence loops back to step 1, it generates a completely new pattern. Creates ever-changing melodies.
4. **Smooth vs stepped**: Toggle B1.6 to switch between sharp staircase transitions (off) and smooth portamento glides (on). Slew mode is great for modulation targets like filter cutoff.
5. **Pairs well with quad bernoulli**: Patch O2 (gate) through the bernoulli to thin out the rhythmic pattern while the pitch sequence stays intact on O1

---

## droid-quad-snh.ini

Four sample & hold channels sampling the same CV input at staggered clock divisions (/1, /2, /3, /4). Inspired by the disting NT `sextuplet.lua` by Thorinside, adapted from 6 channels to 4 to fit DROID's 8-output architecture. With internal random normalization, produces 4 correlated-but-different melodic lines from a single source. Optional scale quantization is applied before sampling so all channels receive scale-correct notes.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | CV Source | Normaled to internal random |
| I2 | Clock | Normaled to internal LFO (rate set by P1.1) |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | S&H Channel 1 (samples every clock) |
| O2 | S&H Channel 2 (samples every 2 clocks) |
| O3 | S&H Channel 3 (samples every 3 clocks) |
| O4 | S&H Channel 4 (samples every 4 clocks) |
| O5 | Clock /1 trigger pass-through |
| O6 | Clock /2 trigger |
| O7 | Clock /3 trigger |
| O8 | Clock /4 trigger |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate (internal LFO speed) |
| P1.2 | Scale (attenuate all S&H outputs, 0-100%) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Freeze (LED on = hold all channels, clock blocked) |
| B1.4 | Quantize (LED on = CV quantized to Locrian scale before sampling) |

### Usage Tips

1. **4-voice generative melody**: Leave inputs unpatched. Random CV is sampled at 4 different rates, creating related but divergent melodies. Patch O1-O4 to four VCOs through quantizers for instant polyrhythmic counterpoint.
2. **Correlated modulation**: Patch a slow LFO to I1. Each channel captures the LFO at a different moment, producing 4 phase-shifted staircase versions of the same wave. Great for filter cutoffs or waveshaping.
3. **Freeze for performance**: Toggle B1.3 to hold all 4 channels at their current values. The clock stops reaching the S&H circuits, but the clock division outputs (O5-O8) also freeze, making it a full performance pause.
4. **Scale control**: P1.2 attenuates all 4 CV outputs simultaneously. At 50%, the output range is halved. Useful for keeping melodies within a smaller interval or creating subtle modulation.
5. **Quantize before sampling**: Toggle B1.4 on to quantize the input CV to a scale before it reaches any S&H channel. This ensures all 4 outputs are always on scale degrees, even with random input.
6. **Clock output chaining**: O5-O8 output the divided clocks, useful for triggering envelopes, syncing other modules, or driving the quad bernoulli's gate inputs for polyrhythmic probability filtering.
7. **External clock + CV**: Patch a sequencer pitch CV to I1 and its clock to I2. Each channel captures pitch at different divisions — channel 1 tracks every note, channel 4 only updates every 4th note, creating a natural delay/echo effect in pitch space.

---

## droid-no-control.ini

A variable-timing self-clocking trigger sequencer ported from the disting NT `no_control.lua` by Expert Sleepers. Each step in the sequence has a different random duration — slow steps linger, fast steps rush by. The sequencer generates its own clock internally, with the speed changing per step. The duration values double as pitch CV, creating melodies where rhythm and pitch are intrinsically linked.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Reset | Returns to step 1 |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Trigger (fires every step change) |
| O2 | Gate (algorithmic pattern, ~80% density) |
| O3 | Pitch CV (step duration value, optionally quantized) |
| O4 | BOC Trigger (beginning of cycle) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Speed Range — at 0 all steps are uniformly slow (~2 sec); at full, fast steps reach ~60ms while slow steps stay long |
| P1.2 | Steps (1-8, notched) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Reroll (new random timing pattern) |
| B1.4 | Freeze (LED on = holds current step indefinitely) |
| B1.5 | Quantize (LED on = pitch CV quantized to Locrian scale) |

### How It Works

Unlike conventional sequencers that advance on an external clock, this patch generates its own clock using an internal LFO. The LFO's speed is controlled by the current step's CV value — each step literally determines how long it lasts. When the LFO fires, the algoquencer advances to the next step, which outputs a new duration CV, changing the LFO speed for the next interval.

The algoquencer remembers its pattern (dejavu = 1), so the same irregular rhythm repeats each cycle. Press Reroll (B1.3) to generate a completely new timing pattern.

### Usage Tips

1. **Organic trigger source**: Patch O1 to a drum module for irregular, human-feeling rhythms. The variable timing creates natural-sounding patterns that fixed-clock sequencers can't achieve.
2. **Linked pitch and rhythm**: Patch O3 to a VCO and O2 to a VCA gate. Fast steps are high-pitched, slow steps are low-pitched (or vice versa), creating an intrinsic connection between melody and rhythm.
3. **Speed Range as expression**: Sweep P1.1 during performance. At 0, the sequence crawls uniformly. Turn it up and the timing starts swinging — some steps zip by while others drag. Creates dramatic tension and release.
4. **Freeze for emphasis**: Toggle B1.4 to freeze on the current step. The LFO stops, holding the current note/trigger indefinitely. Unfreeze to resume the sequence from where it left off.
5. **Reroll for variety**: Each press of B1.3 generates a completely new random timing pattern. The rhythm changes but the structure (step count, density) stays the same.
6. **BOC sync**: Patch O4 to another module's reset to sync phrase lengths. The BOC trigger fires once per complete cycle through all steps.
7. **Pair with quad bernoulli**: Feed O1 into the bernoulli's gate input for probability-filtered irregular triggers — doubly unpredictable rhythms.

---

## droid-sync-latch.ini

A musical boundary transport sync ported from the disting NT `sync_latch.lua` by Sleepwalk Cinema (original concept from the Mutable Instruments MIDIpal). Defers transport changes to musically precise loop boundaries. Arm the latch, and the slave run gate toggles at the next end-of-loop — ensuring you never start or stop a sequencer mid-phrase.

Simplified from the original: assumes 4/4 time (4 beats per bar), beat-rate clock (no PPQN), and uses the armed state as the fill indicator.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Clock | Normaled to internal LFO (rate set by P1.1). One pulse per beat. |
| I2 | Arm | Trigger toggles arm state (same as B1.3) |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Slave Run gate (high = running, toggles at loop boundaries) |
| O2 | Armed/Fill gate (high from arm press until latch fires) |
| O3 | End of Bar trigger (every 4 beats) |
| O4 | End of Loop trigger (every N bars) |
| O5 | Gated Clock (clock passed only while slave is running) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Clock Rate (internal LFO speed) |
| P1.2 | Bars per Loop (1-8, notched; 4 beats per bar = 4 to 32 beat loops) |
| B1.1 | Run/Stop — master clock (LED = running) |
| B1.2 | Reset (momentary — clears all state, slave returns to idle) |
| B1.3 | Arm (toggle, LED on = armed. Auto-clears when latch fires at loop end) |
| B1.4 | Direct Slave Toggle (immediate start/stop, bypasses latch. LED = slave running) |

### How It Works

1. The clock counts beats. Every 4 beats, an end-of-bar trigger fires (O3). Every N bars (set by P1.2), an end-of-loop trigger fires (O4).
2. Press **B1.3** (Arm) to queue a transport change. The armed LED (L1.3) lights up and O2 goes high.
3. At the next end-of-loop, the latch fires: the slave run gate (O1) toggles and the armed state auto-clears.
4. The slave starts idle after reset. The first arm+latch starts it, the second stops it, and so on.
5. **B1.4** (Direct Toggle) bypasses the latch mechanism entirely, toggling the slave immediately. Use this when you don't need boundary-aligned changes.

### Usage Tips

1. **Start a drum machine on the downbeat**: Patch O5 (gated clock) to your drum sequencer's clock input. Arm the latch (B1.3). At the next loop boundary, the gated clock starts flowing, beginning the drums exactly on beat 1.
2. **Stop on a phrase boundary**: While the slave is running, press B1.3 to arm. The slave continues until the loop ends, then stops cleanly — no mid-bar cutoffs.
3. **Fill indicator**: O2 goes high the moment you arm. Patch it to a drum fill trigger, an LED, or a mixer CV to signal "a change is coming." It stays high until the latch fires.
4. **External clock sync**: Patch your master clock to I1. The sync latch counts beats from the external source, ensuring boundaries align with your master tempo.
5. **Remote arm**: Patch a trigger from another module (e.g., a foot pedal, button press, or sequencer gate) to I2 to arm the latch hands-free.
6. **Quick start/stop**: Use B1.4 for immediate transport control when you don't care about boundary alignment. The LED shows the current slave state.
7. **Chain with other patches**: Patch O4 (EOL) to the reset input of another sequencer to sync phrase lengths. Patch O3 (EOB) to trigger bar-aligned events like filter sweeps or envelope resets.

---

## droid-bouncing-ball.ini

A classic bouncing ball trigger generator. A trigger starts a sequence of increasingly rapid bounces that decay in amplitude — like a ball dropped onto a hard surface. Uses a decaying energy envelope that inversely controls an LFO's speed: as energy drains, the LFO accelerates, producing the signature bouncing-ball pattern of closer-and-closer triggers with fading amplitude.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Trigger | Start a bounce sequence |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Bounce triggers (amplitude-gated, naturally tapers off) |
| O2 | Bounce velocity CV (staircase of decreasing values, one per bounce) |
| O3 | Energy envelope (continuous decay curve, 1→0) |
| O4 | Accelerating clock (raw LFO, full amplitude, keeps running) |
| O5 | Sequence active gate (high while bouncing, low when at rest) |
| O6 | Inverted envelope (0→1 rising, for upward modulation) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Speed — initial bounce rate and overall tempo. Low = slow first bounce, high = fast |
| P1.2 | Decay — how long the sequence lasts. Low = short ping, high = long dramatic bounce |
| B1.1 | Trigger (manual bounce start. LED brightness = envelope activity) |
| B1.2 | Loop (LED on = sequence auto-repeats when it ends) |
| B1.3 | Gravity (3 states: light / medium / heavy. Controls how dramatically bounces accelerate) |

### How It Works

1. A trigger fires a one-shot AD envelope (the "energy" of the ball).
2. The envelope starts at 1 (full energy) and decays toward 0 (at rest).
3. An LFO generates the bounce triggers. Its speed is: `base + gravity * (1 - envelope)`.
4. At the start (envelope = 1): LFO is slow → first bounces are widely spaced.
5. As envelope decays toward 0: LFO speeds up → bounces get closer together.
6. The bounce trigger amplitude is multiplied by the envelope, so late bounces are quieter. When the amplitude drops below the gate threshold, bounces naturally stop.
7. In loop mode, the contour auto-restarts, creating repeating bounce sequences.

### Gravity Settings

| State | Acceleration | Character |
|-------|-------------|-----------|
| Light | 8 Hz range | Gentle, moon-like. Bounces slowly converge. |
| Medium | 20 Hz range | Natural feel. Good all-around default. |
| Heavy | 32 Hz range | Dramatic, Jupiter-like. Bounces rush to silence. |

### Usage Tips

1. **Percussion trigger**: Patch O1 to a drum module trigger input. Each press of B1.1 fires a bouncing ball rhythm. Adjust P1.2 for short taps vs long rolls.
2. **Velocity-sensitive drums**: Patch O2 to the drum module's velocity/accent input alongside O1 to the trigger. Early bounces hit hard, late bounces are soft.
3. **Bouncing pitch**: Patch O2 (velocity CV) through a quantizer to a VCO. Each bounce hits a lower note, creating a descending melodic figure.
4. **Rising modulation**: Patch O6 (inverted envelope) to filter cutoff. As the ball bounces, the filter opens — creating a brightening texture that intensifies as bounces accelerate.
5. **Accelerating clock**: Patch O4 to any clock input for a clock that starts slow and speeds up. Useful for accelerating arpeggios, tape-speed-up effects, or tension-building transitions.
6. **Gated processing**: Use O5 (sequence active) to enable/disable other modules only while the ball is bouncing. Patch to a VCA CV or a circuit's `select` input.
7. **Loop for texture**: Toggle B1.2 on for continuous bouncing. The sequence restarts automatically, creating a rhythmic texture. Adjust P1.2 to control the cycle time.
8. **External trigger**: Patch a gate from a sequencer to I1 for rhythmically-timed bouncing ball bursts. Each gate edge starts a new sequence.

---

## droid-maths-classics.ini

Five iconic Make Noise MATHS patches combined into a single DROID utility module. Inspired by the MATHS Classic Patches manual — quadrature LFO, arcade trill, voltage-controlled slew, pulse delay, and clock divider — each function available simultaneously from one p2b8 controller.

### Hardware

1 controller: p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | CV Input | Source for VC slew / portamento |
| I2 | Trigger/Clock | Source for pulse delay + clock divider |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Quadrature 0° (sine-like LFO) |
| O2 | Quadrature 90° |
| O3 | Quadrature 180° (inverted 0°) |
| O4 | Quadrature 270° (inverted 90°) |
| O5 | Arcade Trill (self-modulating FM) |
| O6 | Slewed CV (portamento on I1) |
| O7 | Delayed trigger (pulse delay on I2) |
| O8 | Divided clock (from I2) |

### Controls

| Control | Function |
|---------|----------|
| P1.1 | Rate — quad LFO speed and trill base frequency |
| P1.2 | Modifier — slew time (O6) and delay time (O7) |
| B1.1 | Run/Stop (LED = running). Gates the quadrature LFO only; other functions run independently |
| B1.2 | Reset (momentary). Resets quadrature sequencers to step 1 |
| B1.3 | Trill Depth (3 states: subtle / medium / wild). Controls self-modulation feedback amount |
| B1.4 | Clock Divide (4 states: /2 /4 /8 /16). Sets division ratio for O8 |
| B1.5 | Quad Shape (LED on = smooth sine, off = stepped staircase) |

### Functions

**Quadrature LFO (O1–O4)** — Two 8-step sequencers hold pre-baked sine lookup values (8 samples per cycle). The second sequencer is offset by 2 steps to produce a 90° phase shift. An internal LFO clocks both at 8× the visible rate. Optional slew smoothing (B1.5) interpolates between steps for a rounder waveform. 180° and 270° are derived by inverting the 0° and 90° outputs.

**Arcade Trill (O5)** — A self-modulating LFO whose triangle output feeds back into its own frequency input. DROID's one-frame processing delay keeps this stable (same technique as droid-no-control.ini). The feedback depth (B1.3) ranges from subtle warble to wild FM tones. P1.1 sets the base pitch.

**VC Slew / Portamento (O6)** — A simple slew limiter on I1. P1.2 controls the slew time for both rising and falling edges. Patch a pitch CV to I1 for classic portamento, or any CV for smoothing.

**Pulse Delay (O7)** — Delays triggers arriving at I2 by a variable amount. P1.2 scales the delay from 0 to 2 seconds. Useful for creating flamming, echo triggers, or offset timing.

**Clock Divider (O8)** — Divides the clock at I2 by a ratio selected with B1.4. Four ratios available: /2, /4, /8, /16. Use alongside pulse delay for polyrhythmic trigger processing.

### Techniques

- **Wavetable-style LFO**: The quadrature uses sequencer-based waveform lookup rather than a native LFO waveform. This allows arbitrary waveshapes — the sine values could be replaced with any 8-point waveform.
- **Self-modulating feedback**: The arcade trill exploits DROID's deterministic processing order. The LFO reads its own output from the previous frame, creating stable FM without explicit delay circuits.
- **Shared pot, dual function**: P1.2 simultaneously controls slew time and delay time. Both are modifier parameters that benefit from the same 0–1 knob range.

### Usage Tips

1. **Quadrature modulation**: Patch O1–O4 to four VCA CV inputs or filter cutoffs for swirling phase-shifted modulation. Classic analog polysynth animation.
2. **Ring mod textures**: Patch O5 (trill) to a VCA CV input with an audio signal. Sweep P1.1 for metallic, bell-like tones. Cycle B1.3 for varying aggression.
3. **Smooth portamento**: Patch a keyboard or sequencer pitch CV to I1. O6 produces gliding pitch transitions. P1.2 at noon gives a medium glide; full CW gives slow dramatic slides.
4. **Trigger echo**: Patch a drum trigger to I2. O7 produces a delayed copy — instant flam or echo effect. O8 simultaneously divides the same clock for polyrhythmic layering.
5. **Stepped vs smooth**: Toggle B1.5 to switch the quadrature between a staircase waveform (good for stepped modulation, sample-and-hold textures) and a smooth sine approximation (good for continuous modulation).
6. **Combined clocking**: Use the quadrature outputs as slow modulation while I2 handles fast clock division — the two systems share P1.1 for correlated rates but operate independently.
7. **Trill as audio**: At high P1.1 settings the trill enters audio range. Patch O5 to a mixer for crude but characterful FM synthesis directly from DROID.

---

## droid-zularic-repetitor.ini

A 3-bank rhythmic gate generator inspired by the Noise Engineering Zularic Repetitor and Multi Repetitor modules. Generates 4 simultaneous gate outputs (mother + 3 children) from a library of world music rhythms, algorithmic numeric patterns, and Euclidean rhythms. Three banks selectable via P2.1: Zularic (8 stored patterns from African and world music traditions), Numeric Repetitor (2 algorithmically-derived 16-step patterns), and Euclidean (variable-density rhythms with 4 phase-offset outputs).

### Hardware

2 controllers: p2b8, p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Beat (clock) | Normaled to internal LFO (rate set by P1.1) |
| I2 | Measure (reset) | Combined with B1.2 button |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Mother gate (Row 1) |
| O2 | Child 1 gate (Row 2) |
| O3 | Child 2 gate (Row 3) |
| O4 | Child 3 gate (Row 4) |

### Controls

**Controller 1 (p2b8) — Transport & Pattern**

| Control | Function |
|---------|----------|
| P1.1 | Clock rate (internal LFO speed) |
| P1.2 | Pattern select (8 notched positions — function depends on bank) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| L1.4-L1.6 | Pattern number indicator (3-bit binary) |

**Controller 2 (p2b8) — Bank & Display**

| Control | Function |
|---------|----------|
| P2.1 | Bank select (3 positions: ZR / NR / Euclidean) |
| L2.1-L2.4 | Beat indicator LEDs (Mother, Child 1, Child 2, Child 3 — flash on gate) |
| L2.5-L2.6 | Bank indicator (off/off = ZR, on/off = NR, on/on = Euclidean) |

### Banks

**Bank 1: Zularic (ZR)** — 8 stored patterns, P1.2 selects 1–8

Patterns extracted from the Noise Engineering Zularic Repetitor manual. Each pattern has 4 rows: a mother rhythm and 3 children derived from it. Patterns 1–4 are Old World (12-step, 12/8 feel — African and Middle Eastern rhythms). Patterns 5–8 are New World (16-step, 4/4 feel — Funk and Rock derived).

| Position | Origin | Steps | Character |
|----------|--------|-------|-----------|
| 1 | Old World 1 | 12 | Dense polyrhythmic (26 beats) |
| 2 | Old World 3 | 12 | Medium density (22 beats) |
| 3 | Old World 5 | 12 | Very dense (27 beats) |
| 4 | Old World 6 | 12 | Sparse (18 beats) |
| 5 | New World 7 | 16 | Medium funk (24 beats) |
| 6 | New World 8 | 16 | Dense funk (29 beats) |
| 7 | New World 9 | 16 | Very dense (33 beats) |
| 8 | New World 10 | 16 | Medium groove (28 beats) |

The 12-step patterns create a 12/8 compound time feel; the 16-step patterns play in straight 4/4. The page-flip mechanism handles this automatically — the `_HALF_LEN` cable switches between 6 (for 12-step) and 8 (for 16-step) based on the selected pattern.

**Bank 2: Numeric Repetitor (NR)** — 2 stored patterns, P1.2 positions 1–4 = NR1, 5–8 = NR2

Algorithmically curated 16-step patterns from the Multi Repetitor's Numeric bank. Each mother rhythm was selected from 65,536 possible 16-step patterns using the criteria: fewer than 8 beats per measure, balanced density across all rotations. Children are derived via binary multiplication.

| Selection | Mother Pattern | Beats | Character |
|-----------|---------------|-------|-----------|
| NR1 | `X...X...X...X...` | 4 | Four on the floor — universal dance rhythm |
| NR13 | `X..X..X.X..X..X.` | 6 | Triplet feel — 3+3+2+3+3+2 grouping |

NR1's children thin out progressively: R2 has 4 beats offset by 2 steps, R3 has 2 beats (downbeat + midpoint), R4 has only the downbeat. NR13's children maintain the triplet feel with increasing sparsity.

**Bank 3: Euclidean** — Algorithmic, P1.2 controls beat density

Uses DROID's native `[euklid]` circuit to generate Euclidean rhythms in real time — no pattern storage needed. The 8 pot positions map to beat counts: 1, 2, 3, 5, 7, 9, 11, 13 beats distributed as evenly as possible across 16 steps.

All 4 outputs use the same beat count but with phase offsets for polyrhythmic interaction:

| Output | Offset | Effect |
|--------|--------|--------|
| O1 (Mother) | 0 | Base Euclidean pattern |
| O2 (Child 1) | 3 | Shifted by 3 steps |
| O3 (Child 2) | 7 | Nearly half-rotation |
| O4 (Child 3) | 11 | Counter-phase |

At low beat counts (1–3), the offsets create widely spaced trigger cascades. At higher counts (9–13), the four outputs interlock into dense polyrhythmic textures where beats fill in the gaps between each other.

### Architecture

The patch uses a page-flip mechanism to handle patterns longer than 8 steps (DROID's `[sequencer]` maximum). Two 8-step sequencers per row are clocked alternately via a `[clocktool]` divider and `[flipflop]`:

```
_CLOCK → [clocktool] ÷ _HALF_LEN → [flipflop] → _SEQ_PAGE
                                                    │
              Page A clock ← _CLOCK * (1 - page)   │
              Page B clock ← _CLOCK * page ─────────┘
```

Pattern selection uses 8-input `[switch]` circuits (one per row per page half), and page merge switches combine the two halves. A final bank mux layer (3-input switches) selects between ZR, NR, and Euclidean outputs.

Total: 138 circuits, ~9.5 KB estimated RAM (within 10 KB budget).

### Usage Tips

1. **Quick start**: Leave inputs unpatched, press B1.1 to start. Turn P1.1 for tempo, P1.2 for pattern. Patch O1–O4 to four different drum/percussion modules.
2. **Bank exploration**: Turn P2.1 to switch banks. ZR for organic world rhythms, NR for precise algorithmic patterns, Euclidean for evenly-spaced geometric rhythms. Watch L2.5/L2.6 for current bank.
3. **12/8 vs 4/4**: ZR patterns 1–4 are 12-step (compound time). Use these with a clock at dotted-eighth speed for authentic 12/8 grooves. Patterns 5–8 are 16-step straight time.
4. **Euclidean density sweep**: In Euclidean bank, slowly turn P1.2 from left to right during performance. The rhythm builds from a single downbeat (1 beat) through sparse polyrhythm (3–5 beats) to dense interlocking patterns (11–13 beats).
5. **Phase-offset polyrhythm**: In Euclidean mode with 5 or 7 beats, the four phase-offset outputs create complex interlocking patterns. Patch each to a different percussion sound for instant polyrhythmic drumming.
6. **External clock**: Patch a clock to I1 for tempo sync. Patch a reset/downbeat trigger to I2 to align phrase boundaries with your master sequencer.
7. **Selective gating**: Use only O1 (mother) for the main rhythm and patch O2–O4 through VCAs or a bernoulli gate for occasional ghost notes and fills.
8. **Four on the floor anchor**: Select NR bank, positions 1–4 (NR1). O1 gives a solid `X...X...X...X...` kick pattern while O2–O4 provide progressively sparser complementary rhythms — instant techno foundation.

---

## droid-mi-grids.ini

A DROID clone of Mutable Instruments Grids, the "topographic drum sequencer." Generates rhythmic gate patterns for 3 drum channels (BD, SD, HH) that morph continuously across an X/Y map of rhythmic styles, with density control, accent outputs, and per-step chaos. Pattern data from the original Grids firmware by Emilie Gillet (GPL v3+).

### How It Works

Grids stores rhythmic patterns as per-step "level" values (0-255) across a 2D map. This implementation uses the 4 corner nodes from the original 5x5 grid, giving a simplified but musically effective 2x2 map:

| | X=0 (Left) | X=1 (Right) |
|---|---|---|
| **Y=0 (Top)** | Node 0: Four-on-the-floor, clean backbeat, steady 8ths | Node 4: Busy rolling, backbeat + fills, active HH |
| **Y=1 (Bottom)** | Node 20: Syncopated Afro-Cuban, polyrhythmic, sparse HH | Node 24: Dense fine-resolution, sparse w/ rolls, rapid-fire HH |

The X and Y pots continuously interpolate between these four corners using bilinear crossfading. Each step produces a "level" for each channel. The density knob sets a threshold — steps whose level exceeds (1 - density) fire a gate. At low density only the strongest beats fire; at full density nearly everything triggers.

Accents fire when a step's level exceeds 0.753 (192/255), matching the original Grids behavior. Chaos adds a random offset (+/-15%) to each step's level, introducing variation.

### Hardware

2 controllers: p2b8, p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Clock | Normaled to internal LFO (rate set by P1.1) |
| I2 | Reset | Returns to step 1 |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | BD gate |
| O2 | SD gate |
| O3 | HH gate |
| O4 | BD accent |
| O5 | SD accent |
| O6 | HH accent |
| O7 | Clock thru |

### Controls

**Controller 1 (p2b8) — Transport & Map**

| Control | Function |
|---------|----------|
| P1.1 | Clock rate (internal LFO speed) |
| P1.2 | Map X — morph left/right between rhythmic styles |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Chaos on/off (LED = active) |

**Controller 2 (p2b8) — Map Y, Density & Mutes**

| Control | Function |
|---------|----------|
| P2.1 | Map Y — morph top/bottom between rhythmic styles |
| P2.2 | Density (0 = sparse, only strongest beats; 1 = full, nearly all steps fire) |
| B2.1 | BD mute (LED on = unmuted) |
| B2.2 | SD mute (LED on = unmuted) |
| B2.3 | HH mute (LED on = unmuted) |

### Architecture

The patch uses 79 circuits (~6.3 KB) organized in 10 sections:

1. **Transport** — Internal LFO normaled to I1, run/stop, reset merge
2. **Page-flip** — 16-step sequencing via 2x8-step pages (clocktool /8 + flipflop)
3. **Pattern data** — 24 sequencers (4 nodes x 3 channels x 2 pages) storing level values
4. **Page merge** — 12 switches combining page A/B into one output per node/channel
5. **Bilinear interpolation** — 9 crossfaders (3 per channel: top row, bottom row, vertical)
6. **Chaos** — 1 random generator + 3 copies adding offset when enabled
7. **Density threshold** — 3 compares (level > 1-density = gate)
8. **Accent threshold** — 3 compares (level > 0.753 = accent)
9. **Mutes & outputs** — 3 mute toggles + 6 output copies
10. **Controls** — 3 pots (Map X, Map Y, Density)

### Usage Tips

1. **Quick start**: Patch O1-O3 to three drum modules (kick, snare, hi-hat). Press B1.1 to start. Turn P1.1 for tempo. Both X and Y pots at noon gives a blend of all four corner patterns.
2. **Explore the map**: Sweep P1.2 (X) and P2.1 (Y) slowly. Top-left is classic four-on-the-floor rock. Top-right gets busy and rolling. Bottom-left goes Afro-Cuban syncopated. Bottom-right is dense and rapid-fire.
3. **Density as build-up**: Start with P2.2 low — only the strongest beats fire. Gradually increase for fills and build-ups. At full density, nearly every step triggers.
4. **Accent for dynamics**: Patch O4-O6 to accent/velocity inputs on your drum modules for dynamic variation. Accented steps are the strongest beats in each pattern.
5. **Chaos for humanization**: Toggle B1.3 to add +/-15% random variation to each step's level. This pushes some borderline steps over or under the density threshold, creating subtle per-repeat variation.
6. **Channel mutes for arrangement**: Use B2.1-B2.3 to drop channels in and out during performance. All three start unmuted (LED on).
7. **External clock**: Patch your master clock to I1 and a reset/downbeat to I2 for tempo sync. O7 passes the gated clock through for chaining.
8. **Pair with accent envelopes**: Route accent outputs through separate envelope generators with shorter decay for snappy accented hits alongside longer-decay normal gates.

### Pattern Data Credits

Pattern data extracted from Mutable Instruments Grids by Emilie Gillet, licensed under GPL v3+. The 4 corner nodes (0, 4, 20, 24) from the original 5x5 topographic map provide the rhythmic material. 16 steps per channel extracted from 32-byte patterns using max-pair reduction to capture both even and odd-index values.

---

## droid-cv-recorder.ini

A dual-channel CV recorder / looper inspired by Shakmat's Bishop's Miscellany. Record knob movements to tape and play them back as loops or one-shot sequences. Features variable playback speed, reverse, scrub, pause, and SD card save/load. Both channels share transport and playback controls but record independently.

Uses the DROID `[recorder]` circuit (1,712 bytes RAM each) which provides full transport controls, clock-synced recording, and SD card persistence. Two `[recorder]` instances share the same tape memory pool.

### Hardware

2 controllers: p2b8, p2b8

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Clock | Normaled to internal LFO (rate set by P1.1) |
| I2 | Play trigger | Starts playback on both channels (combine with B1.5) |

### Outputs

| Jack | Signal |
|------|--------|
| O1 | Ch1 CV out (recorded knob movement) |
| O2 | Ch2 CV out |
| O3 | Ch1 gate out |
| O4 | Ch2 gate out |
| O5 | Clock thru (gated by Run/Stop) |

### Controls

**Controller 1 (p2b8) — Transport & Speed**

| Control | Function |
|---------|----------|
| P1.1 | Clock rate (internal LFO speed, 0.5-8.5 Hz) |
| P1.2 | Playback speed (0-2x, center = 1x) / Scrub position (when scrub enabled) |
| B1.1 | Run/Stop (LED = running, default on) |
| B1.2 | Reset clock phase (momentary) |
| B1.3 | Record Ch1 (LED = recording, handled by recorder) |
| B1.4 | Record Ch2 (LED = recording, handled by recorder) |
| B1.5 | Play (LED = Ch1 playing, handled by recorder) |
| B1.6 | Stop (LED = Ch2 playing, stops recording and playback) |
| B1.7 | Loop on/off (LED = loop mode active) |
| B1.8 | Reverse on/off (LED = reverse playback) |

**Controller 2 (p2b8) — Recording & File Management**

| Control | Function |
|---------|----------|
| P2.1 | Ch1 recording knob — turn while recording to capture CV movement |
| P2.2 | Ch2 recording knob |
| B2.1 | Pause (LED = paused, freezes playback position) |
| B2.2 | Scrub enable (LED = on, P1.2 controls tape position instead of speed) |
| B2.3 | Save to SD card (momentary, LED flash) |
| B2.4 | Load from SD card (momentary, LED flash) |
| B2.5 | File number select (cycles 0-9, LED brightness shows position) |
| L2.6 | Tape overflow warning (lights if either channel exceeds tape memory) |

### Recording Workflow

1. Press **B1.1** (Run/Stop) to start the clock — LED lights, default is on at startup
2. Press **B1.3** (Record Ch1) — L1.3 lights, recording begins
3. **Turn P2.1** — the knob's CV (0-1V) is captured to tape, one sample per clock tick
4. Press **B1.3** again (or B1.6 Stop) — recording stops
5. Press **B1.5** (Play) — recorded CV loops out on O1, L1.5 lights
6. Adjust **P1.2** for playback speed (center = normal, CW = 2x faster)
7. Toggle **B1.8** for reverse playback
8. Toggle **B1.7** for loop on/off (off = one-shot)
9. Press **B2.3** to save to SD card; **B2.4** to load

### One-Shot Trigger Mode

When Loop is OFF (B1.7), sending a trigger to **I2** (or pressing B1.5) plays the recording once from start to end, then stops. This is the "via trigger" playback mode — useful for firing recorded CV gestures from a sequencer or foot pedal.

### Scrub Mode

Toggle **B2.2** to enable scrub. Now P1.2 controls the tape position directly (0 = start, 1 = end) instead of playback speed. Turn the pot to manually scrub through the recording. Useful for finding specific moments or for manual "scratching" performance effects.

### File Management

Press **B2.5** to cycle through file numbers 0-9 (LED brightness indicates position). Ch1 saves to files 0-9, Ch2 saves to files 10-19 (offset by 10 to prevent conflicts). Press **B2.3** to save both channels; **B2.4** to load. Files persist on the SD card as `tape####.bin`.

### Architecture

20 circuits, ~4.8 KB estimated RAM:

| Section | Circuits | Purpose |
|---------|----------|---------|
| Transport | 5 | LFO clock, Run/Stop, Reset, gated clock, clock thru |
| CV Sources | 2 | Pot helpers for recording knobs |
| Shared Controls | 5 | Play trigger merge, Loop, Reverse, Pause, Scrub toggles |
| Playback Speed | 2 | Speed scaling (0-2x) and reverse negation |
| Save/Load/File | 3 | Save, Load buttons with LED flash, 10-state file selector |
| Recorder x2 | 2 | Independent CV/gate recorders sharing transport state |
| LED Indicators | 1 | Overflow warning merge |

### Usage Tips

1. **Basic recording**: Start the clock (B1.1), hit record (B1.3), wiggle the knob (P2.1), stop recording, press play (B1.5). Instant CV loop on O1.
2. **Dual-channel**: Record both channels independently. Ch1 records from P2.1, Ch2 from P2.2. Both play back simultaneously with shared speed/reverse/loop controls.
3. **Speed performance**: Sweep P1.2 during playback for varispeed effects. Full CCW = frozen, center = normal, full CW = double speed. Toggle B1.8 for instant reverse.
4. **One-shot riffs**: Turn loop off (B1.7), patch a trigger source to I2. Each trigger plays the recorded CV gesture once — instant "riff on demand" from any trigger source.
5. **Scrub DJ mode**: Enable scrub (B2.2), then manually position the tape head with P1.2. Great for finding sweet spots in a recording or for performative scratching.
6. **Pause for freeze**: Toggle B2.1 to freeze playback at the current position. The CV output holds its current value. Unpause to resume from where you left off.
7. **SD card presets**: Save favorite recordings to different file slots (B2.5 cycles 0-9). Load them back anytime — great for a library of pre-recorded CV gestures.
8. **External clock sync**: Patch a clock to I1 for tempo-synced recording. The recorder captures one CV sample per clock tick, so the playback stays in time with your system.
9. **Pair with quantizer**: Patch O1 through a `[minifonion]` for pitch-quantized CV playback. Record free-form knob movements, play back as musical melodies.
10. **Gate outputs**: O3/O4 output gates recorded alongside the CV. With `gatein1 = 1`, the gate is always high during recording, producing a continuous gate during playback. Useful for driving VCAs or envelopes.


---

## droid-polimaths.ini

An 8-channel CV event generator emulating the Make Noise PoliMATHS. Each channel runs an independent Rise-Fall envelope with a superimposed oscillator (LFO to audio rate). Four activation modes determine which channels fire on each trigger input. Spread modulation applies staggered parameter offsets across channels for automatic timbral differentiation. Two output modes: Internal Osc (envelope × oscillator CV) and External Osc (pitch CV for driving external VCOs).

### Hardware

5 controllers: p2b8, p2b8, p10, p8s8, x7

### Inputs

| Jack | Signal | Notes |
|------|--------|-------|
| I1 | Activate | Clock or gate — triggers channel activations |
| I2 | Reset | Returns all channels to idle |
| I3 | Span CV | External channel selection modulation |
| I4 | Spread CV | External spread amount modulation |

### Outputs

**Internal Osc mode (default — B1.7 off):**

| Jack | Signal |
|------|--------|
| O1–O8 | Channel 1–8 envelope × oscillator CV |
| G1–G8 | Channel 1–8 activity gates (via x7) |

**External Osc mode (B1.7 on):**

| Jack | Signal |
|------|--------|
| O1–O8 | Channel 1–8 pitch CV (1V/oct for external VCOs) |
| G1–G8 | Channel 1–8 activation gates |

### Controls

**Controller 1 (p2b8) — Transport & Mode**

| Control | Function |
|---------|----------|
| P1.1 | Span (channel select for Ch.Index; round step position for Round; parallel divisions for Parallel) |
| P1.2 | Spread (center = none; CW = right channels offset up; CCW = left channels offset up) |
| B1.1 | Run/Stop (LED = running) |
| B1.2 | Reset (momentary) |
| B1.3 | Mode (4 states: Ch.Index / Round / Parallel / Binary) |
| B1.4 | Cycle on/off (LED = active) |
| B1.5 | Cycle mode (2 states: All / Follow the Leader) |
| B1.6 | Osc Bias (2 states: Unipolar / Bipolar) |
| B1.7 | Output mode (2 states: Internal Osc / External Osc) |
| B1.8 | *unused* |

**Controller 2 (p2b8) — Curve & Manual Triggers**

| Control | Function |
|---------|----------|
| P2.1 | Curve (envelope shape: full CCW = logarithmic; noon = linear; full CW = exponential) |
| P2.2 | Osc Depth (oscillation mix: 0 = envelope only; full = full oscillator depth) |
| B2.1–B2.8 | Manual channel triggers Ch 1–8 (momentary) |
| L2.1–L2.8 | Channel activity LEDs (brightness tracks envelope level) |

**Controller 3 (p10) — Parameters & Spread Depths**

| Control | Function |
|---------|----------|
| P3.1 | Rise (envelope attack time) |
| P3.2 | Fall (envelope release time) |
| P3.3 | Strength (envelope peak level) |
| P3.4 | Rate (oscillator frequency) |
| P3.5 | Shape (oscillator waveshape) |
| P3.6 | Rise Spread Depth |
| P3.7 | Fall Spread Depth |
| P3.8 | Strength Spread Depth |
| P3.9 | Rate Spread Depth |
| P3.10 | Osc Spread Depth |

**Controller 4 (p8s8) — Per-Channel**

| Control | Function |
|---------|----------|
| P4.1–P4.8 | Channel 1–8 level trim (attenuate individual channel output) |
| S4.1–S4.8 | Channel 1–8 mute switches |

**Controller 5 (x7) — Gate Expander**

| Jack | Function |
|------|----------|
| G1–G8 | Channel 1–8 gate outputs |

### Activation Modes

Four modes select which channels are activated on each trigger at I1. Cycle through with **B1.3**:

**Ch.Index** — Span pot (P1.1 + I3 CV) selects a single channel. Only that channel fires. Useful for playing channels as individual voice sources via CV.

**Round** — A sequencer steps through channels 1→2→...→8→1. Each trigger advances to the next channel. Span pot sets the starting position within the sequence.

**Parallel** — All channels fire simultaneously. Span pot selects a clock division count (1–8) so each trigger fires a different number of channels at once.

**Binary** — A binary counter advances on each trigger (0–255). The 8-bit output maps to 8 channel gates — each channel fires when its corresponding bit is set. Creates rhythmic gate patterns that cycle through all 256 binary states.

### Cycle Modes

When **Cycle** is on (B1.4), channels re-trigger automatically after their envelope completes. Two sub-modes via **B1.5**:

**All** — All active channels cycle independently. Each channel detects its own envelope end-of-cycle and retriggers itself, regardless of other channels.

**Follow the Leader** — Channels form a chain. When channel N's envelope reaches zero, it triggers channel N+1. Channel 8 wraps back to channel 1. This creates a cascading ripple effect: trigger channel 1 once and the envelope passes sequentially through all 8 channels indefinitely.

### Spread

Spread distributes parameter offsets across the 8 channels. The amount of offset applied to each channel is proportional to its position and the spread depth knobs (P3.6–P3.10).

- **P1.2 center**: no spread — all channels receive identical parameters
- **P1.2 CW**: right-side channels (5–8) get higher offsets; left-side (1–4) get lower
- **P1.2 CCW**: reversed — left channels get higher offsets
- **P3.6–P3.10**: individual depth controls per parameter (Rise, Fall, Strength, Rate, Osc)
- **I4**: external CV modulates spread amount

When spread is applied, each channel's Rise, Fall, Strength, oscillator Rate, and oscillator depth all shift by a scaled offset, making each channel's envelope slightly different. At maximum spread depths, channel 8 may have substantially longer rise times, higher strength, and faster oscillator than channel 1.

### Architecture

194 circuits across 15 functional sections.

| Section | Circuits |
|---------|----------|
| Transport | 6 |
| Mode/cycle buttons | 9 |
| Spread pre-compute | 1 |
| Channel Index | 17 |
| Round | 19 |
| Parallel | 15 |
| Binary counter | 23 |
| Mode mux | 9 |
| Trigger merge | 9 |
| Envelopes | 8 |
| Oscillators + shape | 16 |
| Output mixing + routing | 24 |
| Gate outputs | 16 |
| Follow the Leader | 24 |
| LEDs + channel index | 9 |

### Usage Tips

1. **Instant polyrhythm**: Select Parallel mode (B1.3 state 3). Sweep P1.1 to step through different numbers of simultaneously-firing channels. Patch O1–O8 to separate sound modules — each trigger fires a changing cluster of channels.
2. **Cascading envelopes**: Select Ch.Index mode (B1.3 state 1). Enable Cycle (B1.4) and set Follow the Leader (B1.5 state 2). Trigger channel 1 (B2.1) — the envelope cascades 1→2→...→8→1 indefinitely. Adjust Rise/Fall (P3.1/P3.2) for cascade speed.
3. **Spread for timbral variation**: Set all spread depth knobs (P3.6–P3.10) to noon. Sweep P1.2 from center outward. The channels develop increasingly differentiated envelope shapes — channel 1 gets short/quiet, channel 8 gets long/loud (or vice versa).
4. **Binary counter rhythms**: Select Binary mode (B1.3 state 4). Connect a steady clock to I1. Each clock tick advances the binary counter — the 8 channel gates fire in a mathematically determined pattern cycling through 256 states before repeating.
5. **External VCO pitch**: Enable External Osc mode (B1.7 on). O1–O8 now output pitch CVs. Patch to 8 VCOs and use G1–G8 to gate their VCAs. Each channel fires at a pitch determined by the Spread-modulated Rate and Strength values.
6. **Voltage-controlled spread**: Patch a slow LFO or envelope to I4 (Spread CV). The spread distribution across channels slowly opens and closes, animating the timbral differences between channels.
7. **Manual voice triggering**: B2.1–B2.8 manually trigger each channel regardless of the current activation mode. Use these for direct performance control — play individual channels like keys. Combine with Cycle modes for sustained ringing.
8. **Mutes for arrangement**: S4.1–S4.8 mute individual channels. Drop and add channels during performance for dynamic arrangement. Level trim (P4.1–P4.8) balances output levels per channel before muting.
9. **Oscillator as drone**: Set Rise and Fall long (P3.1/P3.2 full CW), enable Bipolar Osc (B1.6), increase Osc Depth (P2.2). Channels sustain long envelopes with the oscillator creating a continuous drone. Rate spread (P3.9) detunes channels apart.
10. **CV-select specific channels**: Patch a sequencer CV to I3 (Span CV) in Ch.Index mode. The CV selects which channel fires on each trigger — instant CV-controlled channel addressing.
