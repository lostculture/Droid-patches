# MCN 1

Performance patch for the MCN Droid performance rack — a three-voice groove
machine with eight scenes.

| File | What it is |
|---|---|
| `droid.ini` | The patch. Copy to the root of the DROID SD card. |
| `gate-test.ini` | Diagnostic — blinks every G8 and X7 gate with no controllers or clock needed |
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
| `G1`–`G4` | Squid: kick / snare / hat / perc |
| `G5`–`G8` | Squid: mangle slots |
| `G9` | Clock out (X7 gate 1) |
| `G10` | Domino gate (X7 gate 2) |
| `G11` | Start of bar (X7 gate 3, spare) |
| `G12` | Multigrain trigger (X7 gate 4) |
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
4. Hold **B4.9**–**B4.12** for kit fills, **B4.13**–**B4.16** for mangle rolls.
   **B4.17**–**B4.24** finger-trigger the eight Squid channels.
5. **B1.5**–**B1.8** mute whole voices. The **S5.1**–**S5.8** per-channel mutes
   ship **disabled** — see below.
6. **B4.1**–**B4.8** switch scenes. Everything you change is stored into the
   current scene automatically — no save gesture. Long-press **B4.32** to reset
   the current scene.

## The P8S8 switches

DROID panel switches are 3-position and read 0.0 / 0.5 / 1.0, so a switch sitting
up reads 1 and would silently multiply its channel's gate to zero. The mutes
therefore ship disabled. Two constants near the top of `droid.ini` control them:

```ini
[copy]
    input = 0          # _SWITCH_MUTES: 0 = ignore switches, 1 = they mute
    output = _SWITCH_MUTES

[copy]
    input = 1          # _SWITCH_UP_MUTES: 1 = up mutes, 0 = down mutes
    output = _SWITCH_UP_MUTES
```

Once the patch is playing, set `_SWITCH_MUTES` to 1 and check that flipping S5.1
kills the kick. If it works the other way round, flip `_SWITCH_UP_MUTES` to 0.
The centre position never mutes either way.

The P8S8 sliders are always live and need no configuration — with the patch
running, push P5.1 up and the kick gets busier.

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
