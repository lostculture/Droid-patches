# Bass Modulation Engine — Module Routing Guide

How to patch the DROID bass modulation outputs to your eurorack modules.
All 5 patches share the same output standard — learn it once, swap genres
by loading a different `.ini`.

## Output Standard (all 5 patches)

| Output | Signal | What It Controls |
|--------|--------|------------------|
| O1 | Pitch CV | Oscillator pitch (1V/oct, with genre-specific processing) |
| O2 | Filter CV | Filter cutoff (envelope + modulation combined) |
| O3 | VCA CV | Amplitude envelope (note volume shape) |
| O4 | Mod CV | Genre-specific: extra LFO, accent env, 2nd pitch, etc. |
| O5 | Resonance CV | Filter resonance level |
| O6 | Extra Mod | Wavefolder depth, phaser, delay send, etc. |
| O7 | Sub Level | Sub-bass layer level (mostly static) |
| O8 | Gate Out | Processed gate signal |

## Input Standard (all 5 patches)

| Input | Signal | Source |
|-------|--------|--------|
| I1 | Gate/Trigger | Sequencer gate out, keyboard gate, or MIDI-CV |
| I2 | Clock | Quarter-note clock (required for wobble, optional for others) |
| I3 | Pitch CV | 1V/oct pitch from sequencer or keyboard |
| I4 | Accent CV | 0-1V accent/velocity (optional, >0.5 = accent for acid) |

---

## Genre-Specific Routing

### Liquid DnB (`droid-bass-liquid.ini`)

**Sound goal:** Warm, flowing, evolving bass with slow filter movement.

```
DROID O1 ──→ Furthrrrr Generator V/Oct    (or any saw/triangle VCO)
DROID O2 ──→ C4RBN Cutoff CV              (24dB LP, saturation adds warmth)
DROID O3 ──→ Aikido Ch.1 CV               (VCA for amplitude)
DROID O4 ──→ Ikarie CV                    (second filter for stereo movement)
DROID O5 ──→ C4RBN Resonance CV           (low resonance, 10-25%)
DROID O6 ──→ Toad Phase Depth CV          (slow phaser adds liquid shimmer)
DROID O7 ──→ Aikido Ch.2 CV              (sub VCA — mix a sine sub underneath)
DROID O8 ──→ [gate to envelope/sequencer]
```

**Key module roles:**
- **C4RBN** as main filter — its input saturation adds warmth without harsh distortion
- **Ikarie** as secondary filter — dual peaks create formant-like movement from O4's LFO
- **Toad** phaser on the output — 12-stage phaser adds the "liquid" shimmer
- **Furthrrrr** as VCO — complex waveforms give the filter something to sweep through

**Alternative VCOs:** Domino (bassline module, simpler), Troika (analog warmth), Pizza (FM for metallic liquid)

---

### Acid Bass (`droid-bass-acid.ini`)

**Sound goal:** Squelchy, resonant, with accent peaks and pitch slides.

```
DROID O1 ──→ C4RBN V/Oct                  (pitch WITH slide applied)
DROID O2 ──→ C4RBN Cutoff CV              (filter envelope + accent)
DROID O3 ──→ Aikido Ch.1 CV               (VCA with accent peak)
DROID O4 ──→ [spare — accent env for extra destination]
DROID O5 ──→ C4RBN Resonance CV           (HIGH — 50-85%, the squelch)
DROID O6 ──→ [spare — raw accent for triggering effects]
DROID O7 ──→ Aikido Ch.2 CV              (inverted filter env for sub ducking)
DROID O8 ──→ [gate out]
```

**Key module roles:**
- **C4RBN** does EVERYTHING for acid — pitch input, filter, resonance, AND its
  built-in output wavefolding adds the gritty overtones that define acid
- **Single VCO through single filter** — acid is a simple signal path, the
  envelope/accent/slide interaction creates the complexity

**Why C4RBN for acid:**
The C4RBN has input saturation (soft clipping before the filter) and output
wavefolding (harmonic addition after the filter). Combined with high resonance,
this creates the screaming, squelchy, harmonically rich acid tone that a clean
filter can't achieve. The 4-pole mode gives the steep 24dB rolloff that
defines the 303 sound.

**Alternative filters:** A-120 (Moog ladder, classic but cleaner), A Filter of Crows (overdrive character)

---

### Dub/Reggae Bass (`droid-bass-dub.ini`)

**Sound goal:** Deep, heavy, minimal. Physical pressure from sub frequencies.

```
DROID O1 ──→ A-110 V/Oct                  (or Domino — pure clean VCO)
DROID O2 ──→ A-120 Cutoff CV              (24dB Moog ladder for steep rolloff)
DROID O3 ──→ Autodub VCA CV               (the Autodub IS dub)
DROID O4 ──→ Analog Delay Send CV         (dub siren LFO → delay for dub echo)
DROID O5 ──→ [not needed — no resonance in dub bass]
DROID O6 ──→ Autodub Send Level           (space switch controls reverb send)
DROID O7 ──→ Aikido Ch.1 CV              (sub level — keep high and steady)
DROID O8 ──→ [gate out]
```

**Key module roles:**
- **A-110** (Doepfer VCO) for the purest possible sine/triangle sub tone — no
  harmonics means no mud. Set to triangle or sine output.
- **A-120** (Moog ladder filter) for steep 24dB/oct rolloff — cuts everything
  above ~200Hz cleanly. The transistor ladder adds subtle warmth.
- **Autodub** is literally designed for dub — stereo VCA with built-in
  send/return for delay/reverb effects. O3 drives the main VCA level,
  O6 drives the effect send.

**Effects chain (critical for dub):**
```
Autodub Send ──→ Analog Delay Unit ──→ Spring Reverb ──→ Autodub Return
                      ↑                      ↑
              DROID O4 (siren)     DROID O6 (space level)
```

The dub siren LFO (O4) patched to the delay time or feedback creates the
classic dub echo effect. The Spring Reverb adds the vintage character.

**Alternative VCOs:** Domino (dedicated bassline module, built for this), Furthrrrr (set to sine, triangle only)

---

### Dubstep Wobble (`droid-bass-wobble.ini`)

**Sound goal:** Rhythmic "wub wub" filter modulation, aggressive, heavy.

```
DROID O1 ──→ Furthrrrr Generator V/Oct    (rich harmonics for filter to sweep)
DROID O2 ──→ C4RBN Cutoff CV              (the wobble sweeps this)
DROID O3 ──→ Aikido Ch.1 CV               (VCA)
DROID O4 ──→ Flamingo Fold Amount CV       (wavefolding between wobble peaks)
DROID O5 ──→ C4RBN Resonance CV           (moderate, adds character to sweep)
DROID O6 ──→ Toad Phase Depth CV          (growl LFO → phaser for extra texture)
DROID O7 ──→ Aikido Ch.2 CV              (clean sub layer, unmodulated)
DROID O8 ──→ [gate out]
```

**Key module roles:**
- **Furthrrrr Generator** as VCO — you NEED rich harmonics for the wobble filter
  to sweep through. Saw or complex waveforms. A sine has nothing to sweep.
- **C4RBN** with output wavefolding ON — between the wobble peaks (when the
  filter is briefly open), the wavefolding adds extra grit and harmonics
- **Flamingo** wavefolder driven by O4 (raw wobble LFO) — the fold amount
  follows the wobble rhythm, creating harmonic richness that pulses in sync

**Clock requirement:** Patch a quarter-note clock to I2. The wobble LFO syncs
to this via clock-reset. Without I2, the wobble free-runs (still works, just
not tempo-locked).

**Performance tip:** Switch B1.2 between divisions during a performance —
changing from half-note to sixteenth-note wobble mid-phrase is a classic
dubstep arrangement technique.

**Alternative VCOs:** Chord v2 (polyphonic, thick), QUADNIC (digital, harsh), Orgone Accumulator (wavetable, complex)

---

### Reese Bass (`droid-bass-reese.ini`)

**Sound goal:** Thick detuned phasing, slow organic movement. THE DnB bass.

```
DROID O1 ──→ Troika Voice 1 V/Oct         (saw, tuned SHARP by detune amount)
DROID O4 ──→ Troika Voice 2 V/Oct         (saw, tuned FLAT by detune amount)
DROID O2 ──→ C4RBN Cutoff CV              (filter envelope + slow movement)
DROID O3 ──→ Aikido Ch.1 CV               (VCA)
DROID O5 ──→ C4RBN Resonance CV           (moderate ~20%)
DROID O6 ──→ Toad Phase Depth CV          (phaser enhances the beating)
DROID O7 ──→ Aikido Ch.2 CV              (clean sub layer)
DROID O8 ──→ [gate out]
```

**CRITICAL: Two pitch outputs.** O1 and O4 are both absolute 1V/oct pitch CVs.
O1 = base pitch + detune, O4 = base pitch - detune. No precision adder needed.
Patch each to a separate VCO voice set to sawtooth.

**Key module roles:**
- **Troika** is ideal — it's a 3-voice analog oscillator. Use voices 1 and 2
  for the detuned pair, voice 3 as a sub oscillator one octave down.
- **Toad** phaser on the mixed output — the 12-stage phaser interacts with
  the inherent beating to create rich, shifting textures
- **C4RBN** or **Ikarie** as filter — Ikarie's dual-peak character adds
  formant-like qualities to the Reese

**Alternative setups:**
- **Furthrrrr Generator** (dual VCO in one module) — patch O1 to carrier, O4 to modulator
- **Two separate VCOs** (A-110 + any other) — one per pitch output
- **Chord v2** — use unison mode with O1 as base, manually detune one voice

**Width switch (B1.5):** In "spread" mode (default), one osc goes sharp, one goes
flat — classic Reese. In "mono" mode, both go sharp — collapses the stereo
image but creates a different beating character (useful for mono playback).

---

## Quick Reference Card

```
                    LIQUID    ACID      DUB       WOBBLE    REESE
──────────────────────────────────────────────────────────────────
O1 Pitch     →    Furthrrrr  C4RBN     A-110     Furthrrrr  Troika v1
O2 Filter    →    C4RBN      C4RBN     A-120     C4RBN      C4RBN
O3 VCA       →    Aikido     Aikido    Autodub   Aikido     Aikido
O4 Mod       →    Ikarie     [spare]   Delay     Flamingo   Troika v2
O5 Resonance →    C4RBN      C4RBN     [none]    C4RBN      C4RBN
O6 Extra     →    Toad       [spare]   Autodub   Toad       Toad
O7 Sub       →    Aikido     Aikido    Aikido    Aikido     Aikido
O8 Gate      →    [gate]     [gate]    [gate]    [gate]     [gate]
──────────────────────────────────────────────────────────────────
Clock (I2)        optional   no        no        REQUIRED   optional
Accent (I4)       optional   REQUIRED  optional  optional   optional
```

## Getting Started

1. Load one of the `droid-bass-*.ini` files onto your DROID
2. Patch I1 to a gate source (sequencer, keyboard, MIDI-CV)
3. Patch I3 to a pitch CV source
4. Patch O1-O8 to your modules following the genre routing above
5. Tweak the p2b8 controls — the sweet-spot tuning means most useful
   sounds are in the center of each pot's range
