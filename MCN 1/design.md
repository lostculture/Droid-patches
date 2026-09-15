# MCN Droid Performance Rack — Patch Design

**Date:** 2026-09-12
**Patch file:** `MCN 1/droid.ini`
**Rack:** MCN Droid performance rack (ModularGrid #3087024)
**Firmware:** DROID blue-7 or later (required — see §1)

A three-voice performance groove machine driven entirely from one DROID master:
drums and sample mangling on the Squid Salmple, bass on the Domino, and a
melodic lead sent over MIDI to the Ziqal Dimension MK3.

---

## 1. Hardware

### Controllers (chain order = addressing order)

| # | Controller | Role |
|---|---|---|
| 1 | `p2b8` | Transport & mutes |
| 2 | `p2b8` | Morph & reroll |
| 3 | `p10` | Live parameters (2 large + 8 small pots) |
| 4 | `b32` | Scenes, fills, manual triggers |
| 5 | `p8s8` | Per-channel Squid sliders + mute switches |

Declaration order in the `.ini` must match the physical left-to-right chain, as
laid out in the rack (P2B8 at col 1, P2B8 at col 6, P10 at col 11, B32 at col
16, P8S8 at col 26).

### Firmware

The patch requires **blue-7**. The P8S8 shipped in late 2024, and firmware
without support for it lights the controller on boot but never addresses it.
Because a missing controller takes down only the circuits that read its jacks,
the failure is deeply misleading: the drums and three mangle channels go silent
while the bass, lead and Multigrain — none of which read a `P5` jack — play
normally, which reads as a broken drum engine rather than a missing controller.
`controller-test.ini` in this folder isolates it in seconds.

Two blue-7 changes were checked against this patch and neither requires action:
`[algoquencer]` now always starts unmuted when no mute button is wired (helpful
here, since none is), and `[midiout]` rounds `cc1`–`cc8` to the nearest MIDI
value instead of truncating.

### Expanders

Verified against a working G8 + X7 patch and the `blue-6` circuit reference:

- **Expanders are not declared.** Only controllers get `[...]` blocks. A
  reference patch using both a G8 and X7 (for `[midiin]`) declares only its
  `p2b8` controllers. Note `droid-polimaths.ini` in this repo declares `[x7]`,
  which does not follow that convention.
- **Gate outputs are numbered continuously across expanders**, G8 first:
  `G1`–`G8` on the G8, then `G9`–`G12` on the X7 (the X7 has four gate outs).

So the physical wiring maps as:

| Physical | Address |
|---|---|
| G8 gates 1–8 → Squid | `G1`–`G8` |
| X7 gate 1 → clock out | `G9` |
| X7 gate 2 → Domino | `G10` |
| X7 gate 3 → (spare) | `G11` |
| X7 gate 4 → Multigrain | `G12` |

---

## 2. Routing

![Gates, CV and MIDI routing](images/routing.png)

| Jack | Destination |
|---|---|
| `G1` | Squid: kick |
| `G2` | Squid: left blank on purpose |
| `G3`–`G5` | Squid: snare / hat / perc |
| `G6`–`G8` | Squid: mangle slots (ratchets, stutters, chance one-shots) |
| `G9` | Clock out to the rack (X7 gate 1) |
| `G10` | Domino gate (X7 gate 2) |
| `G11` | PIZZA trigger / gate (X7 gate 3) |
| `G12` | Multigrain — mangle engine 4 (X7 gate 4) |
| `O1` | Domino pitch (quantized, with slide) |
| `O2` | Domino accent |
| `O3` | Domino filter / mod |
| `O4` | General purpose LFO — rate, level, waveform on page 2 |
| `O5` | PIZZA pitch (1V/oct) |
| `O6` | PIZZA timbre / FM index (envelope + LFO) |
| `O7` | PIZZA fold / second modulation (LFO + timbre macro + joystick) |
| `O8` | PIZZA ADSR envelope |
| MIDI TRS ch.1 | Dimension MK3: pitch + gate + velocity, CC1/CC2 |
| `I1` / `I2` | External clock / reset (internal LFO normalled when unpatched) |
| `I3` / `I4` | Joystick X / Y in — stacked; the joystick also feeds Multigrain directly |

### Audio path

![Audio path](images/audio-path.png)

The audio side is patched by hand and is shown for reference only — the DROID
touches it solely through the `O6` / `O7` macros.

### Joystick

The joystick goes to Multigrain **directly** on stacked cables; the DROID does
not pass it through. `I3` / `I4` are read only as macro *inputs*, offsetting the
drum map and timbre internally (scaled by `P2.1` macro depth). That leaves `O4`
and `O5` free — candidates are a second Domino mod CV, a Dimension CV, or a
sequenced offset for whatever the set needs.

---

## 3. Control surface

![DROID control overlay](images/overlay.png)

Printable version: `modular-patches/patch-sheets/examples/mcn-droid-performance-overlay.yaml`
(render with `python droid_overlay.py examples/mcn-droid-performance-overlay.yaml`).

### Controller 1 (p2b8) — Transport & mutes
| Control | Function |
|---|---|
| `P1.1` | Tempo |
| `P1.2` | Swing |
| `B1.1` | Run / Stop (LED = running, `startvalue = 1`) |
| `B1.2` | Reset (momentary) |
| `B1.3` | Clock divide (multi-state) |
| `B1.4` | Scene save — hold, then press a scene button |
| `B1.5`–`B1.8` | Mute drums / bass / lead / mangle |

### Controller 2 (p2b8) — Morph & reroll
| Control | Function |
|---|---|
| `P2.1` | Macro depth (how far the joystick moves things) |
| `P2.2` | Chaos |
| `B2.1`–`B2.4` | Reroll drums / bass / lead / mangle |
| `B2.5`–`B2.6` | Fill drums / fill mangle (momentary) |
| `B2.7`–`B2.8` | Lead octave / bass octave |

### Controller 3 (p10) — Live parameters
| Control | Function |
|---|---|
| `P3.1` | Drum density |
| `P3.2` / `P3.3` | Map X / Map Y (drum engine morph) |
| `P3.4` | Gate length |
| `P3.5` / `P3.6` | Bass density / bass accent |
| `P3.7` / `P3.8` | Lead density / lead register |
| `P3.9` | Mangle amount |
| `P3.10` | Timbre macro |

### Controller 4 (b32) — Scenes, fills, triggers
Row-major, 4 columns × 8 rows:

| Buttons | Function |
|---|---|
| `B4.1`–`B4.8` | Scenes 1–8 |
| `B4.9`–`B4.12` | Fills: kick / snare / hat / perc |
| `B4.13`–`B4.16` | Rolls: mangle 1–4 (G6 / G7 / G8 / Multigrain) |
| `B4.17`–`B4.24` | Manual triggers for G1–G8 (`B4.18` = blank channel 2) |
| `B4.25`–`B4.28` | Drum pattern banks A–D |
| `B4.29`–`B4.31` | Bass / lead / mangle pattern select |
| `B4.32` | Clear current scene (long press) |

### Controller 5 (p8s8) — Per-channel Squid
| Control | Function |
|---|---|
| `P5.1`–`P5.8` | Per-channel density by Squid channel — `P5.2` free (blank channel) |
| `S5.1`–`S5.8` | Per-channel mute by Squid channel — off by default, see below |

---

## 4. Voice engines

### Drums — Squid, `G1` and `G3`–`G5`
Four `[algoquencer]` circuits, one per channel. This replaces the Grids-style
topographic engine the design originally proposed: `[algoquencer]` already has
fills, rolls, morphs, branches and — decisively — per-circuit presets, which is
what the scene system is built on. A Grids port would have needed its pattern
tables plus a parallel scene mechanism.

The map pots keep their meaning: `P3.2` (Map X) biases random beats towards
offbeats, `P3.3` (Map Y) towards the second half of the bar, and the joystick
adds a live offset to both, scaled by `P2.1`. `P3.1` sets global density and each
P8S8 slider biases its channel around it (centre = neutral).

### Mangle — Squid `G6`–`G8`, plus Multigrain
Four `[euklid]` circuits at different rotations and lengths (16/16/12/16) so
they interlock rather than stack. Three drive Squid channels `G6`–`G8`; the
fourth has no Squid channel left after the shift, so it drives the Multigrain on
`G12` with its own rhythm rather than a mix of the others. `P3.9` sets how many
beats land per cycle, `P5.6`–`P5.8` bias the three Squid channels around it, and
`B2.4` rerolls the rotation via a `[random]`. The third passes through
`[bernoulli]` so chaos thins it unevenly. Roll buttons fire `[burst]` ratchets
synced to the clock with `taptempo`.

### Bass — Domino, `G10` + `O1`–`O3`
Acid/303 line: `[algoquencer]` with `dejavu = 1` for a remembered pattern,
`[minifonion]` quantizing to the global key/scale, `[slew]` giving accented notes
a glide into pitch, and an accent that drives both `O2` and the filter envelope
on `O3`. Offbeat-leaning placement and occasional two-step ratchets give it the
303 push; `pitchresolution = 12` puts the raw line on a semitone grid before
quantizing.

**Pitch range** is the part that matters in this rack, because the line was
climbing out of bass register. `pitchlow` and `pitchhigh` are now driven:

    _BASS_SHIFT = _BASS_OCTAVE + _BASS_MASTER      bottom of the line
    _BASS_TOP   = _BASS_SHIFT  + _BASS_SPREAD      ceiling

so `P3.8` (master, bipolar ±1 oct) moves the whole line and `P3.7` (spread,
0–1 oct) sets how far it may travel upward — from one repeated note to an octave.

**Glide** is a base amount on every note (`P3.1`, page 3) summed in a `[mixer]`
with an accent-gated extra (`P3.10`), which is the 303 behaviour where accent and
slide travel together. **Length** is `P3.2`, 4–32 steps.

### PIZZA — Bastl oscillator, `O5` + `G11` + `O8`

Added when the Javelin came out of the rack, so the envelope and VCA shaping it
used to provide now come from the DROID. PIZZA has no sequencer of its own. A bank of `[switch]` circuits, all addressed
by one mode cable, points its pitch, gate, octave, glide and envelope character
at either of two personalities:

| | Sub bass (default) | Lead |
|---|---|---|
| Source | its own euclidean sub line | lead line |
| Octave | −1 | +1 |
| Glide | 0.1 | 0.02 |
| Attack scale | 0.1 | 1.0 |
| Release scale | 0.3 | 2.0 |

The envelope times are scaled rather than replaced, so the same four page-2 pots
stay meaningful in both characters — a snappy sub and a swelling lead from one
set of knobs. Time constants are borrowed from the bass modulation engines in
this repo (`droid-bass-wobble.ini` uses 0.016–0.04 for its 80–200 ms stages).

The mode lives on `B4.29` overlaid on page 2, with `startvalue = 0` and
`dontsave = 1`, so it is sub bass at every power-up and the state never persists.
Page 1 keeps `B4.29` as the bass pattern advance, routed through a `[select]` so
a press on page 2 does not also advance the pattern.

Reusing existing lines rather than adding a seventh `[algoquencer]` keeps the
whole voice to about a dozen small circuits.

### Sub bass line — PIZZA's own sequence

Kept separate from the acid line, because a sub doubling the bass line is not a
sub part. `[euklid]` gives the gate with independent length and density,
`[gatetool]` sets how long each note holds, and a 3-step `[random]` through
`[minifonion]` picks between root, fifth and octave. Four small circuits rather
than a seventh `[algoquencer]`.

Because the acid and sub lengths are independent (4–32 steps each), the two bass
parts drift in and out of phase, which is most of the interest in a sub part that
plays so few notes.

### Lead — Dimension MK3 over MIDI
`[midiout]` on channel 1, TRS. Confirmed parameter shapes from the blue-6
circuit reference:

- `pitch1` takes **1 V/oct**, not MIDI note numbers (range −2 V = note 0 to
  8.583 V = note 127), so the lead shares the same `[minifonion]` quantizer as
  everything else.
- `gate1` — positive edge is note-on, negative edge note-off.
- `velocity1` — 0.0 to 1.0, sampled at the note-on edge; driven from the accent
  bus.
- `cc1` / `ccnumber1` and `cc2` / `ccnumber2` — wavetable position from `P3.10`
  and joystick Y.

---

## 5. Scene system

Built on DROID's **native per-circuit presets**, not the hand-rolled
`[dac]`/`[sample]` bank the design first proposed. Most stateful circuits expose
`preset`, `loadpreset`, `savepreset` and `clear` jacks, and feeding the `preset`
input directly (no trigger) switches preset *and* stores edits into the current
one. That is far cheaper and it persists to SD automatically.

A `[buttongroup]` over `B4.1`–`B4.8` outputs `_SCENE` (values 0–7), which is
wired to `preset` on every sequencer, every state button and every macro pot. So
a scene recalls:

- all six sequencer patterns and their pattern-bank selections,
- voice mutes, root note, clock divide, octave and rotation buttons,
- the macro pot values — density, map X/Y, chaos, bass/lead density, mangle
  amount, timbre. Pots use pickup, so a scene change does not jump a value until
  you move the knob past it.

`B4.32` long-pressed fires `clear` on those circuits, resetting the current
scene to defaults.

Deliberately **not** scene-stored: the `S5.1`–`S5.8` mute switches (a physical
switch position must always be the truth), and tempo, swing, gate length,
accent, register and macro depth (live feel controls).

### Switch handling

DROID panel switches are 3-position, reading 0.0 / 0.5 / 1.0 — not a plain
on/off. Multiplying a gate by `(1 - S5.n)` therefore zeroes the gate when the
switch is up and *halves* it at centre. Each switch now runs through a
`[compare]` against 0.5, so only a hard up or down mutes and centre never does,
and two constants (`_SWITCH_MUTES`, `_SWITCH_UP_MUTES`) make the feature and its
polarity a one-line change. The mutes default to off so the patch plays
regardless of where the switches happen to sit.

---

## 6. Build order (completed)

1. Controller declarations, I/O header comment block, transport section
   (internal LFO normalled to `I1`, run/stop, reset, clock divide, `G9` clock out).
2. Drum engine → `G1`–`G4`, with P8S8 density and mutes.
3. Mangle engine → `G5`–`G8`, rolls and fills.
4. Bass engine → `G10`, `O1`–`O3`.
5. Lead engine → `[midiout]`.
6. Macro bus: joystick `I3`/`I4` → engine offsets and `O6`–`O8`.
7. Scene capture/recall.
8. Docs: `patch-guide.md` section and a README table row.

---

## 7. Open decisions

Recorded as assumptions — say the word and they change before the build:

Both of the original open decisions were resolved during the build, in favour of
what the circuits actually offer:

1. **Drum engine** — `[algoquencer]` per channel rather than a Grids port, for
   its native fills/rolls/morphs and, critically, its presets (see §4).
2. **Scene scope** — wider than planned. Native presets made it cheap to store
   every pattern, toggle and macro pot rather than 8 mutes + 4 macros (see §5).

Still open, for the hardware:

3. ~~**Preset behaviour on `[pot]`**~~ — resolved on the hardware. A
   preset-backed pot does recall a stored value and pick up the physical knob
   only once you sweep past it. The consequence is sharp: a stored zero on a
   density pot is silence with the knob sitting at maximum, and nothing on the
   panel explains it. Every preset-backed pot therefore now carries a musical
   `startvalue`.
4. ~~**RAM**~~ — measured in Forge: 170 circuits including six `[algoquencer]`
   use 24% of memory. Not a constraint.
   Check the memory readout in DROID Forge; if it is tight, the first cut is
   dropping the lead algoquencer to a `[euklid]` + `[random]` pitch pair.
5. **Joystick polarity** — `I3`/`I4` are treated as bipolar (±5 V) so the
   macros sit centred. If the Black Joystick 2 outputs 0–10 V, change
   `_MACRO_X` / `_MACRO_Y` to `(I3 - 0.5) * _MACRO_DEPTH`.

---

## 8. What silenced this patch, and why it was hard to see

Three separate faults, each with the same signature — an output silently
reduced to zero, with nothing on the panel to show which factor did it:

1. **Firmware.** The P8S8 is a late-2024 controller; firmware without support
   lit it on boot but never addressed it. A missing controller only takes down
   the circuits that read its jacks, so the drums and three mangle channels went
   silent while the bass, lead and Multigrain played on — which reads as a broken
   drum engine rather than a missing controller. Fixed by blue-7.
2. **A centred switch read as "down".** `[compare]` tests equality exactly
   unless given a `precision`, so a 3-way switch at centre reading 0.4999 fell
   through to the mute branch. Fixed with `precision = 0.25`.
3. **A density pot at zero**, made worse by preset pickup holding a stored zero
   while the knob sat elsewhere. Fixed with `startvalue` on every preset-backed
   pot.
4. **Invalid parameter expressions — the real cause of the silent drums.** A
   DROID input computes A x B + C: one multiplication, one offset. Every drum
   and mangle gate was written with three products and a bracket, so the
   parameter never evaluated and the gate never fired. This was present from the
   first version, which is why those channels never once worked while the bass,
   lead and Multigrain — whose expressions happened to fit the form — worked
   throughout. The gates are now built from `[logic]` circuits, and
   `tools/check-patch.py` catches the whole class.

The lasting fixes are structural, not one-off: the status row on B32 LEDs 9–12
shows each factor of the drum path live, the `_USE_P8S8` and `_SWITCH_MUTES`
constants take whole subsystems out of the signal path in one line, and the five
patches in `diagnostics/` bisect the rack from wiring up to sequencer.

## 9. DROID Forge conventions

Forge is stricter about comments than the master is, and two of its rules are
invisible until it complains:

- **Square brackets in a comment are jack-label syntax.** `#  O1: [Bass] Domino
  pitch` gives that jack a label in Forge. A bracket anywhere else in a comment
  is a parse error — so circuit names in prose must be written without them.
  The header of `droid.ini` now labels every jack and control this way, which is
  worth doing for its own sake: the labels show up on the controls in Forge.
- **A section is exactly three lines** — divider, title, divider — with any
  explanation following *after* it. A block that also ends with a divider opens a
  second section with no title, which Forge reports as "Untitled section".

RAM, for reference: this patch at 170 circuits with six `[algoquencer]` circuits
uses **24%** of the master's memory, so the earlier worry about size was
unfounded.

## 10. Sources

- Circuit parameter reference (auto-generated from the DROID `blue-6` manual):
  [Eising/droid-metapatch](https://github.com/Eising/droid-metapatch)
- G8 + X7 gate numbering in a working patch:
  [jpgsloan/supergrids](https://github.com/jpgsloan/supergrids)
- X7 specification (four gate outputs, MIDI DIN + USB):
  [Der Mann mit der Maschine X7](https://shop.dermannmitdermaschine.de/products/x7)
- Diagram and overlay generators: `lostculture/modular-patches`,
  `patch-sheets/generator.py` and `patch-sheets/droid_overlay.py`
