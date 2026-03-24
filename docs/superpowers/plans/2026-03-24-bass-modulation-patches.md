# Bass Modulation Engine — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 5 genre-specific DROID bass modulation patches that receive a trigger/gate and output complex multi-destination CV envelopes to drive the user's oscillators, filters, VCAs, and effects for signature bass sounds.

**Architecture:** Each patch is a self-contained `.ini` file for DROID. It receives trigger/gate on I1, optional clock on I2, and outputs genre-specific CVs on O1-O8 to control external audio modules (oscillator pitch, filter cutoff, VCA level, extra modulation). A p2b8 controller provides real-time tweakability of the key parameters that define each genre's character. The user preference is for longer, sustained, modulated bass notes rather than punchy/short ones.

**Tech Stack:** DROID patch language (.ini), circuits: `[contour]`, `[lfo]`, `[slew]`, `[copy]`, `[button]`, `[pot]`, `[switch]`, `[sample]`, `[compare]`

**Hardware target:** 1x p2b8 controller per patch (can share the same physical p2b8). DROID master I/O.

**User's audio modules for patching (see `docs/module-inventory.md`):**
- Oscillators: Furthrrrr Generator, Domino, Pizza, DIMENSION MK3, Troika
- Filters: C4RBN (SVF + wavefolding), A Filter of Crows, Ikarie, A-120
- VCAs: Aikido, Autodub, Javelin, 3x VCA
- Effects: Nautilus, Beads, Aurora, Chronoblob2, The Toad, Endless Processor
- Envelopes: MATHS, Zadar, Quadigy (but DROID replaces these for bass)
- Modulation: ochd, Triple Sloths, QV-L

---

## Shared Conventions

All bass patches follow these conventions:

### I/O Standard
```
INPUTS:
  I1: Gate/Trigger (note on/off)
  I2: Clock (for tempo-synced features, normaled to internal LFO)
  I3: Pitch CV (1V/oct from sequencer — passed through with modifications)
  I4: Accent/Velocity CV (optional, 0-1)

OUTPUTS:
  O1: Pitch CV (processed: slides, bends applied to I3)
  O2: Filter CV (envelope + modulation for filter cutoff)
  O3: VCA CV (amplitude envelope)
  O4: Mod CV (genre-specific: wobble LFO, detune, accent, etc.)
  O5: Resonance CV (filter resonance modulation)
  O6: Extra mod (wavefolder amount, delay send, phaser depth, etc.)
  O7: Sub level (for sub-bass layer mixing)
  O8: Gate out (processed gate, with legato/slide handling)
```

### Controller Standard (p2b8)
```
P1.1: Primary character param (genre-specific — the "one knob" control)
P1.2: Secondary character param
B1.1: Run/active (LED = active)
B1.2: Primary character modifier (genre-specific — may be mod intensity, LFO rate, etc.)
B1.3-B1.4: Genre-specific mode switches
B1.5-B1.8: Genre-specific toggles
```

### File Naming
`droid-bass-{genre}.ini` — e.g., `droid-bass-liquid.ini`

### Patch Guide
Each patch gets an entry in `patch-guide.md` with I/O tables and suggested module routings.

---

## Task 1: Liquid DnB Bass Modulation Engine

**Files:**
- Create: `droid-bass-liquid.ini`
- Modify: `patch-guide.md` (append)

**Character:** Slow, flowing filter sweeps that evolve over 2-4 bars. Long sustain, gentle modulation, minimal distortion. The bass "breathes" — filter opens slowly, closes slowly, with a very slow LFO adding organic drift. User prefers longer notes.

**CV Recipe:**
- **Filter env:** Attack 20ms, Decay 400ms, Sustain 30%, Release 600ms, depth ~2 octaves
- **VCA env:** Attack 5ms, Decay 0, Sustain 100%, Release 100ms
- **Slow LFO** (0.05-0.2 Hz) → filter cutoff at 15% depth (the "liquid" movement)
- **Very slow LFO** (0.01 Hz, 4-bar drift) → filter env depth (evolving brightness)
- **Pitch:** Clean pass-through, no slides

**Controls:**
- P1.1: Filter sweep depth (how far the filter opens on each note)
- P1.2: LFO rate (liquid movement speed, 0.05-0.5 Hz)
- B1.1: Active (LED)
- B1.2: Mod depth (3 states: subtle/medium/lush)
- B1.3: Sweep shape (2 states: smooth/punchy — changes filter env decay)
- B1.4: Drift toggle (enables/disables the very slow macro LFO)
- B1.5: Brightness base (2 states: dark/warm — shifts filter cutoff base)
- B1.6: Long release toggle (doubles all release times)

- [ ] **Step 1: Create patch header and controller**
  Write the file header with I/O documentation, controller declaration, and transport section (gate input handling, clock normalization).

- [ ] **Step 2: Build filter envelope**
  `[contour]` with attack=0.02, decay controlled by P1.1, sustain=0.3, release=0.6. Output scaled by sweep depth to O2. Include sweep shape button to switch between smooth (decay=0.4) and punchy (decay=0.15) via `[switch]`.

- [ ] **Step 3: Build VCA envelope**
  `[contour]` with near-instant attack, full sustain, moderate release. Long release toggle doubles release time. Output to O3.

- [ ] **Step 4: Build liquid LFO modulation**
  `[lfo]` with rate from P1.2 (0.05-0.5 Hz range), triangle wave. Output mixed into filter CV (O2) at depth controlled by B1.2 mod intensity switch.

- [ ] **Step 5: Build macro drift LFO**
  Very slow `[lfo]` at ~0.01 Hz modulating the filter envelope depth. Enabled/disabled by B1.4 drift toggle. Creates the multi-bar evolving brightness.

- [ ] **Step 6: Build resonance and extra mod outputs**
  O4: Copy of the slow filter LFO (from Step 4) for routing to a second filter destination (e.g., Ikarie). O5: Static resonance level (low, 10-25%, set by brightness base switch). O6: Slow triangle for subtle wavefolder/phaser modulation. O7: Sub level (inverted VCA envelope slightly for sub emphasis during sustain).

- [ ] **Step 7: Wire pitch pass-through and gate**
  O1: Copy I3 (pitch) directly (no slides for liquid). O8: Gate output from I1.

- [ ] **Step 8: Add patch guide entry**
  Document I/O, controls, and suggest routing: O1→Furthrrrr pitch, O2→C4RBN cutoff, O3→Aikido VCA, O4→Ikarie CV, O6→Toad depth.

- [ ] **Step 9: Commit**
  `git add droid-bass-liquid.ini patch-guide.md && git commit -m "Add liquid DnB bass modulation engine"`

---

## Task 2: Acid Bass (303-Style) Modulation Engine

**Files:**
- Create: `droid-bass-acid.ini`
- Modify: `patch-guide.md` (append)

**Character:** Fast-decaying filter envelope with high resonance, accent system that boosts filter cutoff on marked steps, exponential slide (portamento) between notes. The interplay of accent + slide + resonance is the acid signature. Note: we already have `droid-tb303-acid.ini` which is a full sequencer — this is different: it's a pure modulation engine that receives external triggers/pitch and outputs 303-style envelope CVs.

**CV Recipe:**
- **Filter env (MEG):** Attack 3ms, Decay 200-2000ms (knob), Sustain 0%, Release=Decay
- **Accent env:** Separate envelope, attack 15ms, decay 300ms, adds to filter CV
- **Accent accumulation:** Consecutive accents stack (don't fully discharge between notes)
- **VCA env:** Instant attack, held during gate, instant release (except accent adds a percussive peak)
- **Slide:** 60ms exponential slew on pitch CV, enabled per-note via gate overlap detection
- **Resonance:** High base level (70-90%), accent doesn't change resonance

**Controls:**
- P1.1: Filter decay (the primary 303 "shape" knob, 200ms-2s)
- P1.2: Accent amount (how much accent boosts filter cutoff)
- B1.1: Active (LED)
- B1.2: Env mod depth (3 states: subtle/classic/screaming)
- B1.3: Slide time (2 states: short 40ms / long 80ms)
- B1.4: Accent accumulation toggle (consecutive accent stacking)
- B1.5: Resonance level (2 states: medium 50% / high 85%)
- B1.6: Filter base shift (2 states: deep/bright)

- [ ] **Step 1: Create patch header with 303-specific I/O docs**
  Note that I4 is accent CV (>0.5 = accented note), I3 is pitch. Gate overlap on I1 triggers slide behavior.

- [ ] **Step 2: Build main filter envelope (MEG)**
  `[contour]` with instant attack, decay from P1.1 scaled to 200ms-2s range, zero sustain. The main MEG decay stays at whatever P1.1 sets on both accented and non-accented notes — the accent system (Step 3) handles the extra filter boost independently.

- [ ] **Step 3: Build accent envelope and accumulation**
  Second `[contour]` triggered by accent CV threshold. Attack 15ms, decay 300ms. With accumulation toggle: use `[slew]` with slow decay on accent CV so consecutive accents build up. Mix accent envelope into filter CV.

- [ ] **Step 4: Build slide (portamento) on pitch CV**
  `[slew]` on pitch pass-through. Slew time from B1.3 switch (40ms or 80ms). Always active (external sequencer controls legato — when notes overlap, the slew creates the slide effect).

- [ ] **Step 5: Build VCA envelope with accent boost**
  `[contour]` for VCA. Base: instant attack, full sustain, instant release. Mix in accent envelope at ~30% for percussive accent peak.

- [ ] **Step 6: Build resonance and extra outputs**
  O5: Static high resonance from B1.5 switch. O6: Accent raw CV pass-through (for driving other modules). O7: Inverted filter env (for sub ducking during bright sweeps).

- [ ] **Step 7: Wire all outputs and scale**
  Combine MEG + accent into O2 (filter CV), scale by env mod depth switch. O1: Pitch with slide. O3: VCA. O4: Accent envelope (separate for VCA or other destination). O8: Gate.

- [ ] **Step 8: Patch guide entry**
  Suggest: O1→C4RBN pitch, O2→C4RBN cutoff, O3→Aikido VCA, O5→C4RBN resonance. The C4RBN's built-in saturation + wavefolding is perfect for acid.

- [ ] **Step 9: Commit**

---

## Task 3: Dub/Reggae Bass Modulation Engine

**Files:**
- Create: `droid-bass-dub.ini`
- Modify: `patch-guide.md` (append)

**Character:** Deep, heavy, minimal. Almost pure sub with very little upper harmonic content. Long sustain, controlled release, emphasis on the weight and space between notes. Very subtle modulation — the sound is about restraint. User's Autodub module is literally made for this.

**CV Recipe:**
- **Filter env:** Near-static. If any: attack 0, decay 400ms, sustain 10%, depth tiny (0.5 octave max)
- **VCA env:** Attack 10ms (slightly softened to avoid speaker pops), Sustain 100%, Release 300ms
- **Pitch drop:** Optional 1-semitone pitch envelope, 0 attack, 100ms decay (weight drop)
- **Slow LFO:** 0.05-0.1 Hz at 5-10% depth on filter (barely perceptible breathing)
- **Resonance:** Zero to near-zero

**Controls:**
- P1.1: Weight (filter cutoff base — lower = deeper sub, 100-300 Hz range)
- P1.2: Release time (how long the note rings, 100ms-1s)
- B1.1: Active (LED)
- B1.2: Sub style (3 states: pure sine / warm / roots — shifts filter character)
- B1.3: Pitch drop toggle (enables/disables the 1-semi pitch drop)
- B1.4: Dub siren toggle (enables a slow pitch wobble for dub siren effects)
- B1.5: Space (2 states: tight/wide — affects release and reverb send level)
- B1.6: Pressure toggle (adds very subtle LFO to VCA for physical pulsing)

- [ ] **Step 1: Create patch header with dub-specific docs**
  Emphasize: this patch outputs very controlled, quiet CVs. The subtlety is the point.

- [ ] **Step 2: Build VCA envelope**
  `[contour]` with softened attack (10ms), full sustain, release from P1.2. Space switch doubles release. Output to O3.

- [ ] **Step 3: Build filter CV (mostly static)**
  Base cutoff from P1.1 mapped to low range. Sub style switch shifts between 3 presets. Tiny filter envelope (optional) with very shallow depth. Output to O2.

- [ ] **Step 4: Build pitch drop envelope**
  `[contour]` with 0 attack, 100ms decay, 0 sustain. Scaled to 1 semitone (~0.083V). Enabled by B1.3 toggle. Subtracted from pitch CV. Output pitch on O1.

- [ ] **Step 5: Build dub siren and pressure mods**
  Dub siren: very slow `[lfo]` (0.07 Hz, ~14 second cycle) modulating pitch by ±2 semitones, enabled by B1.4. Pressure: very slow `[lfo]` (0.08 Hz) at tiny depth on VCA for subtle amplitude breathing, enabled by B1.6.

- [ ] **Step 6: Build remaining outputs**
  O4: Dub siren LFO (for routing to delay send on Autodub). O5: Near-zero resonance. O6: Space/reverb send level (from Space switch). O7: Sub level (high, mostly unmodulated).

- [ ] **Step 7: Patch guide entry**
  Suggest: O1→Domino pitch (or A-110 for pure sine sub), O2→A-120 cutoff (24dB ladder for steep rolloff), O3→Autodub VCA, O6→Autodub send, effects chain: Analog Delay → Spring Reverb.

- [ ] **Step 8: Commit**

---

## Task 4: Dubstep Wobble Bass Modulation Engine

**Files:**
- Create: `droid-bass-wobble.ini`
- Modify: `patch-guide.md` (append)

**Character:** The defining feature is a tempo-synced LFO modulating filter cutoff — the "wub wub". The LFO rate changes between note divisions (half, quarter, eighth, sixteenth) for rhythmic variety. Rich harmonics from the oscillator, deep filter sweeps.

**CV Recipe:**
- **Filter LFO (the wobble):** Tempo-synced, sine/triangle. Rate switchable between divisions
- **VCA env:** Instant attack, full sustain, short release
- **Filter base env:** Optional short attack transient (200ms decay) for initial brightness
- **LFO depth:** 30-70% of filter range, sweeping 2-4 octaves
- **Pitch:** Optional sub-octave drop at note start (50-100ms, 1 octave)
- **Resonance:** Moderate (25-40%)

**Controls:**
- P1.1: Wobble depth (how far the LFO sweeps the filter, 0-100%)
- P1.2: Filter base (where the wobble sits in the frequency range)
- B1.1: Active (LED)
- B1.2: LFO rate (4 states: half/quarter/eighth/sixteenth note)
- B1.3: LFO shape (3 states: sine/triangle/square)
- B1.4: Sub drop toggle (octave pitch drop at note start)
- B1.5: Growl toggle (adds second LFO at different rate for complex wobble)
- B1.6: Filter type hint (2 states: smooth/aggressive — shifts resonance)

**LFO Rate Calculation (at 140 BPM via I2 clock):**
Use `[clocktool]` to derive divisions from clock input:
- Half note: `[clocktool]` divide=2
- Quarter note: direct clock (pass through)
- Eighth note: `[clocktool]` multiply=2 (or use `[lfo]` at 2x clock Hz with clock reset)
- Sixteenth note: `[clocktool]` multiply=4 (or `[lfo]` at 4x Hz with reset)
Note: `[clocktool]` supports both `divide` and `multiply` parameters. For the LFO, use the divided/multiplied clock as `reset` input.

- [ ] **Step 1: Create patch header**
  Document tempo-sync requirement (I2 = clock at quarter note rate).

- [ ] **Step 2: Build clock division system**
  `[clocktool]` instances for each division. `[button]` with states=4 selects which division drives the wobble LFO via `[switch]`.

- [ ] **Step 3: Build wobble LFO**
  `[lfo]` with `reset` driven by the selected clock division pulse (from Step 2). The `[lfo]` cannot directly sync to a clock — instead, the divided clock pulse resets the LFO phase each cycle, effectively syncing it. Set `hz` to approximate the target rate (e.g., 2.3 Hz for quarter note at 140 BPM) — the reset keeps it locked even if hz drifts slightly. Shape switchable via B1.3 `[switch]` between sine/triangle/square waveforms. Output scaled by P1.1 depth. Mix with filter base from P1.2. Output to O2.

- [ ] **Step 4: Build growl (second LFO)**
  Second `[lfo]` at a different division (always one step faster or slower than primary). Enabled by B1.5 toggle. Mixed into filter CV at ~30% of primary depth. Creates the complex, shifting wobble.

- [ ] **Step 5: Build VCA envelope and pitch drop**
  VCA: instant attack, full sustain, short release. Pitch drop: `[contour]` 0 attack, 80ms decay, scaled to -1 octave, enabled by B1.4. Pitch output on O1.

- [ ] **Step 6: Build initial transient envelope**
  Short filter `[contour]` (0 attack, 200ms decay) that adds a brightness burst at note start, before the LFO takes over. Mixed into O2.

- [ ] **Step 7: Wire remaining outputs**
  O4: Wobble LFO raw (for driving other destinations — VCA, wavefolder, panning). O5: Resonance from B1.6 switch. O6: Growl LFO (separate output). O7: Static sub level.

- [ ] **Step 8: Patch guide entry**
  Suggest: O1→Furthrrrr pitch (rich harmonics needed), O2→C4RBN cutoff, O3→Aikido VCA, O4→Flamingo fold amount. The C4RBN's wavefolding on output adds extra grit between wobble peaks.

- [ ] **Step 9: Commit**

---

## Task 5: Reese Bass Modulation Engine

**Files:**
- Create: `droid-bass-reese.ini`
- Modify: `patch-guide.md` (append)

**Character:** Detuned sawtooth oscillators creating inherent phasing/beating. The "modulation" is built into the detune — DROID outputs two pitch CVs with controllable detune spread. Slow filter sweeps add movement on top of the inherent phasing. This is the foundational DnB/jungle bass sound.

**CV Recipe:**
- **Pitch 1 & 2:** Same base pitch + configurable detune (±5 to ±50 cents)
- **Filter env:** Attack 10ms, Decay 300ms, Sustain 20%, Release 400ms, ~1.5 octave depth
- **Slow LFO:** 0.05-0.2 Hz triangle on filter cutoff at 20% depth
- **VCA env:** Instant attack, full sustain, release 200ms
- **Detune modulation:** Optional very slow LFO modulating the detune amount

**Controls:**
- P1.1: Detune amount (±5 cents to ±50 cents)
- P1.2: Filter sweep depth
- B1.1: Active (LED)
- B1.2: Detune character (3 states: subtle 5-10 / classic 10-20 / aggressive 25-50 cents)
- B1.3: Filter movement (2 states: slow envelope / LFO pulsing)
- B1.4: Detune drift toggle (very slow LFO modulates detune amount)
- B1.5: Width (2 states: mono/spread — changes detune polarity for stereo)
- B1.6: DnB mode toggle (adds 1/8th note filter LFO for rhythmic Reese)

**Detune CV math:** 1 cent = 1/1200 of a volt in 1V/oct. 10 cents = 0.00833V.

- [ ] **Step 1: Create patch header**
  Two pitch outputs needed: O1 = osc1 pitch (base + detune), O4 = osc2 pitch (base − detune). O8 remains as gate out per shared convention. The patch guide must note that O1 and O4 are both absolute pitch CVs — no external precision adder needed.

- [ ] **Step 2: Build detune CV generation**
  P1.1 scaled by B1.2 character switch to set detune range. Output two pitch CVs: `I3 + detune` and `I3 - detune`. Width switch flips the second from `-detune` to same `+detune` (mono mode). Detune drift LFO optionally modulates the detune amount.

- [ ] **Step 3: Build filter envelope**
  `[contour]` with 10ms attack, 300ms decay, 20% sustain, 400ms release. Depth from P1.2. Output to O2.

- [ ] **Step 4: Build filter movement LFO**
  B1.3 switches between two modes: slow envelope-only (filter env carries the movement) or LFO pulse (adds 0.1 Hz triangle at 20% depth). B1.6 DnB mode overrides to 1/8th note synced LFO for rhythmic pulsing. Output mixed into O2.

- [ ] **Step 5: Build VCA envelope**
  Instant attack, full sustain, 200ms release. Output to O3.

- [ ] **Step 6: Wire remaining outputs**
  O4 is already assigned as osc2 pitch (Step 2). O5: Moderate resonance (~20%). O6: Slow triangle LFO for routing to phaser/chorus depth (enhances Reese phasing). O7: Sub level (unmodulated). O8: Gate out.

- [ ] **Step 7: Patch guide entry**
  Suggest: O1→Troika voice 1 pitch (+detune), O4→Troika voice 2 pitch (−detune), O2→C4RBN cutoff (or Ikarie for dual-peak character), O3→Aikido VCA, O6→Toad depth (phaser enhances Reese). Both O1 and O4 are absolute 1V/oct pitch CVs — no external adder needed.

- [ ] **Step 8: Commit**

---

## Task 6: Final Integration

**Files:**
- Modify: `README.md` (add bass patches section)
- Modify: `patch-guide.md` (review all entries)
- Create: `docs/bass-routing-guide.md` (suggested module patchings per genre)

- [ ] **Step 1: Update README with bass patch section**
  Add "Bass Modulation Engines" category with the 5 patches.

- [ ] **Step 2: Create bass routing guide**
  Document recommended physical patch cable routings from DROID outputs to the user's specific modules for each genre.

- [ ] **Step 3: Final commit and push**
  `git add -A && git commit -m "Add 5 bass modulation engine patches" && git push`
