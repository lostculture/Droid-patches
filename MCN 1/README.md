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
| `gate-test.ini` | Diagnostic — blinks every G8 and X7 gate with no controllers or clock needed |
| `drum-test.ini` | Diagnostic — runs the drum engine alone, with a non-sequenced control gate on G11 |
| `controller-test.ini` | Diagnostic — proves which controllers the master is actually addressing |
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

The switches are 3-position, reading 0.0 / 0.5 / 1.0. **Pulling a switch fully
down mutes its channel**; centre and up both play, so a channel is never
silenced by a switch you have not deliberately moved. If that feels backwards:

```ini
[copy]
    input = 0          # _SWITCH_UP_MUTES: 0 = down mutes, 1 = up mutes
    output = _SWITCH_UP_MUTES
```

Set `_SWITCH_MUTES` to 0 to ignore the switches altogether.

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
