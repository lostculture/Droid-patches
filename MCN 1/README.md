# MCN 1

Performance patch for the MCN Droid performance rack — a three-voice groove
machine with eight scenes.

| File | What it is |
|---|---|
| `droid.ini` | The patch. Copy to the root of the DROID SD card. |
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
5. **S5.1**–**S5.8** mute individual Squid channels; **B1.5**–**B1.8** mute
   whole voices.
6. **B4.1**–**B4.8** switch scenes. Everything you change is stored into the
   current scene automatically — no save gesture. Long-press **B4.32** to reset
   the current scene.

## Regenerate the diagrams

The YAML in `patch-sheets/` is rendered by the tools in the
[modular-patches](https://github.com/lostculture/modular-patches) repo:

```bash
cd modular-patches/patch-sheets
python droid_overlay.py path/to/overlay.yaml -o overlay.pdf
python generator.py path/to/routing.yaml -o routing.pdf
```
