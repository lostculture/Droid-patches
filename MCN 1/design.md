# MCN Droid Performance Rack — Patch Design

**Date:** 2026-09-12
**Patch file:** `MCN 1/droid.ini`
**Rack:** MCN Droid performance rack (ModularGrid #3087024)

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
| `G1`–`G4` | Squid: kick / snare / hat / perc |
| `G5`–`G8` | Squid: mangle slots (ratchets, stutters, chance one-shots) |
| `G9` | Clock out to the rack (X7 gate 1) |
| `G10` | Domino gate (X7 gate 2) |
| `G12` | Multigrain grain/slice trigger (X7 gate 4) |
| `O1` | Domino pitch (quantized, with slide) |
| `O2` | Domino accent |
| `O3` | Domino filter / mod |
| `O4`–`O5` | Spare CV — free for whatever the set needs |
| `O6` | Global filter macro (C4RBN / Dimension) |
| `O7` | Space macro (Aurora / FX AID) |
| `O8` | Accent bus |
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
| `B4.13`–`B4.16` | Rolls: G5 / G6 / G7 / G8 |
| `B4.17`–`B4.24` | Manual triggers for G1–G8 |
| `B4.25`–`B4.28` | Drum pattern banks A–D |
| `B4.29`–`B4.31` | Bass / lead / mangle pattern select |
| `B4.32` | SAVE (hold + scene = store) |

### Controller 5 (p8s8) — Per-channel Squid
| Control | Function |
|---|---|
| `P5.1`–`P5.8` | Per-channel density for G1–G8 |
| `S5.1`–`S5.8` | Per-channel mute for G1–G8 |

---

## 4. Voice engines

### Drums — Squid, `G1`–`G4`
Four `[algoquencer]` circuits, one per channel. This replaces the Grids-style
topographic engine the design originally proposed: `[algoquencer]` already has
fills, rolls, morphs, branches and — decisively — per-circuit presets, which is
what the scene system is built on. A Grids port would have needed its pattern
tables plus a parallel scene mechanism.

The map pots keep their meaning: `P3.2` (Map X) biases random beats towards
offbeats, `P3.3` (Map Y) towards the second half of the bar, and the joystick
adds a live offset to both, scaled by `P2.1`. `P3.1` sets global density and each
P8S8 slider biases its channel around it (centre = neutral).

### Mangle — Squid, `G5`–`G8`
Four `[euklid]` circuits at different rotations and lengths (16/16/12/16) so
they interlock rather than stack. `P3.9` sets how many beats land per cycle,
`P5.5`–`P5.8` bias each channel around it, and `B2.4` rerolls the rotation via a
`[random]`. Channel 7 passes through `[bernoulli]` so chaos thins it unevenly.
Roll buttons fire `[burst]` ratchets synced to the clock with `taptempo`.

### Bass — Domino, `G10` + `O1`–`O3`
Acid-style line: `[algoquencer]` with `dejavu = 1` for a remembered pattern,
`[minifonion]` quantizing to the global key/scale, `[slew]` for probabilistic
slide, and an accent bus that drives both `O2` and the filter CV `O3`.

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

3. **Preset behaviour on `[pot]`** — the intent is per-scene pot values with
   pickup. Confirm on the hardware that recalling a scene restores the stored
   value and the knob picks up rather than snapping.
4. **RAM** — six `[algoquencer]` circuits is the heaviest part of the patch.
   Check the memory readout in DROID Forge; if it is tight, the first cut is
   dropping the lead algoquencer to a `[euklid]` + `[random]` pitch pair.
5. **Joystick polarity** — `I3`/`I4` are treated as bipolar (±5 V) so the
   macros sit centred. If the Black Joystick 2 outputs 0–10 V, change
   `_MACRO_X` / `_MACRO_Y` to `(I3 - 0.5) * _MACRO_DEPTH`.

---

## 8. Sources

- Circuit parameter reference (auto-generated from the DROID `blue-6` manual):
  [Eising/droid-metapatch](https://github.com/Eising/droid-metapatch)
- G8 + X7 gate numbering in a working patch:
  [jpgsloan/supergrids](https://github.com/jpgsloan/supergrids)
- X7 specification (four gate outputs, MIDI DIN + USB):
  [Der Mann mit der Maschine X7](https://shop.dermannmitdermaschine.de/products/x7)
- Diagram and overlay generators: `lostculture/modular-patches`,
  `patch-sheets/generator.py` and `patch-sheets/droid_overlay.py`
