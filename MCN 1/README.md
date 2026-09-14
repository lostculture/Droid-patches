# MCN 1

Performance patch for the MCN Droid performance rack — a three-voice groove
machine with eight scenes.

**Requires DROID firmware blue-7.** The P8S8 is a late-2024 controller; older
firmware lights it up on boot but never addresses it, which silently kills every
channel whose density reads a `P5` jack — the drums and three of the four mangle
slots — while the bass, lead and Multigrain carry on as if nothing were wrong.

| File | What it is |
|---|---|
| `droid.ini` | The patch. Copy to the root of the DROID SD card. |
|||||| `diagnostics/` | Five test patches that bisect a silent patch — see below |
| `design.md` | Full design: routing, control map, voice engines, scene system |
| `overlay-print.pdf` | Printable controller overlay (A4 landscape) |
| `routing-print.pdf` | Printable routing + audio path sheets |
| `images/` | The same diagrams as PNGs, embedded in `design.md` |
| `patch-sheets/` | YAML sources for the diagrams |

## Load it

Copy `droid.ini` to the SD card root and power-cycle, or open it in DROID Forge
and upload.

## Patch it

Gates are numbered continuously across the expanders — G8 first, then X7:

| Jack | To |
|---|---|
| `G1` | Squid: kick |
| `G2` | Squid: left blank on purpose |
| `G3`–`G5` | Squid: snare / hat / perc |
| `G6`–`G8` | Squid: mangle slots |
| `G9` | Clock out (X7 gate 1) |
| `G10` | Domino gate (X7 gate 2) |
| `G11` | Start of bar (X7 gate 3, spare) |
| `G12` | Multigrain — mangle engine 4 (X7 gate 4) |
| `O1`–`O3` | Domino pitch / accent / filter |
| `O6`–`O7` | Filter macro, space macro |
| `O8` | Accent bus |
| MIDI TRS ch.1 | Dimension MK3 |
| `I1`/`I2` | Clock / reset in — leave unpatched to use the internal clock |
| `I3`/`I4` | Joystick X/Y (stacked; the joystick also goes straight to Multigrain) |

`O4` and `O5` are free.

## Output levels

| Output | Level |
|---|---|
| `G1`–`G8` (G8 expander → Squid) | 0 V / 5 V, fixed in hardware, not adjustable |
| `G9`–`G12` (X7) | gate/trigger at modular level |
| `O1`–`O8` (CV) | 0–10 V, where a patch value of 1.0 = 10 V |

The gate jacks are binary: any non-zero value from the patch comes out as a full
5 V gate, so gate levels need nothing done to them. The CV outputs are the ones
to watch — if a destination wants 0–5 V rather than 0–10 V, halve the value on
the way out, e.g. `input = _BASS_ACC * _BASS_ACCENT * 0.5`.

## Play it

1. Press **B1.1** to run. **P1.1** is tempo, **P1.2** swing.
2. **P3.1** drum density, **P3.2/P3.3** map X/Y — these are the main "move the
   groove" knobs. The joystick offsets both, scaled by **P2.1**.
3. **P2.2** chaos: turns deja-vu down and morphing up across every sequencer.
4. Hold **B4.9**–**B4.12** for kit fills, **B4.13**–**B4.16** for mangle rolls
   (the fourth rolls the Multigrain). **B4.17**–**B4.24** finger-trigger the
   Squid channels; **B4.18** is the blank channel 2.
5. **B1.5**–**B1.8** switch whole voices on and off — **LED lit = playing**, and
   all four start on. The **S5.1**–**S5.8** per-channel mutes ship **disabled**
   — see below.
6. **B4.1**–**B4.8** switch scenes. Everything you change is stored into the
   current scene automatically — no save gesture. Long-press **B4.32** to reset
   the current scene.

## The P8S8

The faders scale their own channel's density, 40% fully down to 100% fully up.
If the P8S8 ever stops responding, one constant near the top of `droid.ini`
takes it out of the signal path entirely and the patch keeps playing:

```ini
[copy]
    input = 1          # _USE_P8S8: 1 = faders scale channels, 0 = ignore them
    output = _USE_P8S8
```

`controller-test.ini` checks the controller itself: push each fader and the
matching Squid gate G1–G8 should go high, with the fader's own LED following it.
If every other controller responds but the P8S8 does not, suspect the firmware
first, then the ribbon chain order (rack position is irrelevant — only the
daisy-chain order counts).

## The P8S8 switches

The switches are 3-position, reading 0.0 / 0.5 / 1.0. They ship **disabled**, so
no switch position can silence a channel:

```ini
[copy]
    input = 0          # _SWITCH_MUTES: 0 = ignore switches, 1 = down mutes
    output = _SWITCH_MUTES
```

Set it to 1 when you want per-channel mutes, and watch `L4.11` — that LED is the
channel 1 mute term and must stay lit with the switch centred or up. If it goes
dark with nothing muted, set the constant back to 0 and tell me.

The comparison uses plain numbers rather than a cable for its branches. With a
cable there, a centred switch was read as "down" and muted every channel, while
the identical comparison written with literals read the same switch correctly.

## Reading the status row

The four fill buttons on the B32 have no LEDs of their own, so LEDs 9–12 show
the state of the drum path instead. If the drums are silent, one of these is
dark and tells you why:

| LED | Means | If dark |
|---|---|---|
| `L4.9` | Drums voice on | Press `B1.5` |
| `L4.10` | Drum density (brightness = value) | Turn `P3.1` up |
| `L4.11` | Channel 1 not muted | `S5.1` is muting it |
| `L4.12` | Clock | Transport stopped — press `B1.1` |

## A DROID parameter is only A x B + C

The manual's "Multiply and Add, Attenuation and Offset" section is a hard limit,
not a style note: **one multiplication and one offset per input**, where the
factor and offset may themselves be cables. Anything richer — parentheses, a
second product, a third term — is not a valid expression, and the parameter
simply never evaluates. Nothing looks wrong in the file; a gate just never fires
and an LED never lights.

This silenced the drums and mangle channels from the very first version of this
patch, because every one of their gates was written as

```ini
input = _D1_TRIG * _DRUMS_ON * (-1 * _MUTE1 * _SWITCH_MUTES + 1) + B4.17
```

They are now built from `[logic]` instead — `and` to combine the trigger with
the voice and channel enables, `or` to fold in the manual trigger and rolls.

`tools/check-expressions.py` in the repo root catches this:

```bash
python tools/check-expressions.py "MCN 1/droid.ini"
```

## Diagnostics

Five patches in `diagnostics/`, each self-contained. Copy one to the SD card as
`droid.ini` to run it. In order of what they isolate:

| File | Proves |
|---|---|
| `gate-test.ini` | The G8 and X7 wiring — blinks G1–G12 with no controllers or clock |
| `controller-test.ini` | Which controllers the master is addressing — every control responds instantly |
| `drum-test.ini` | The drum engine alone, with a non-sequenced control gate on G11 |
| `stage1.ini` | The full drum path at 20 circuits instead of 111 |
| `stage2.ini` | Four algoquencers, one variable changed each, to bisect further |

Between them they have caught, in this rack: an outdated firmware that lit the
P8S8 on boot without ever addressing it, a centred 3-way switch being read as
"down", and a density pot sitting at zero.

## If the drums are silent

Run `drum-test.ini`. It plays four drum channels with fixed densities, no pots,
no buttons and no presets, plus a non-sequenced control gate on `G11`:

- **All of G1 G3 G4 G5 and G11 blink** → the engine is fine, so it is a
  parameter in `droid.ini`. Check `B1.5` is lit (dark = drums off), turn `P3.1`
  up, and long-press `B4.32` to clear the scene — voice states are stored per
  scene and survive a reboot.
- **Only G11 blinks** → `[algoquencer]` is producing nothing. Tell me; the drum
  engine would need replacing with `[euklid]`.
- **Nothing blinks** → the patch is not running at all.

## If the gates do not fire

Load `gate-test.ini` instead. It blinks G1–G12 on its own with no clock, no
controllers and no button presses, so it separates a wiring problem from a patch
problem. The header of that file lists what each outcome means.

Neither expander is ever declared in a patch — only controllers are. A single
G8's jacks are `G1`–`G8`; the X7's four gates follow at `G9`–`G12`. The X7 must
be the first module in the chain.

If the gates blink in the test but the main patch is quiet, it is almost always
density: `P3.1` (drums) and `P3.9` (mangle) at zero means silence by design, and
`B1.1` must be lit for the clock to run.

## Regenerate the diagrams

The YAML in `patch-sheets/` is rendered by the tools in the
[modular-patches](https://github.com/lostculture/modular-patches) repo:

```bash
cd modular-patches/patch-sheets
python droid_overlay.py path/to/overlay.yaml -o overlay.pdf
python generator.py path/to/routing.yaml -o routing.pdf
```
