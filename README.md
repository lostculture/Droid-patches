# DROID Patches

A collection of patches for the [DROID](https://shop.dermannmitdermaschine.de) modular eurorack system by Der Mann mit der Maschine. All patches are `.ini` files that can be loaded directly in DROID Forge.

## Patches

### Sequencers

| Patch | Description | Controllers |
|-------|-------------|-------------|
| [droid-4track-sequencer.ini](droid-4track-sequencer.ini) | 4-track algorithmic sequencer with per-track activity, variation, gate length, and fill controls. Step editing via b32. | p2b8 p2b8 p10 b32 |
| [droid-4track-plainbob.ini](droid-4track-plainbob.ini) | 4-track sequencer with Plain Bob Minimus pitch rotation — melodic lines weave between outputs following change ringing permutation rules. | p2b8 p2b8 p10 b32 |
| [tintinnalogia-8bell-plainbob.ini](tintinnalogia-8bell-plainbob.ini) | 8-bell change ringing sequencer implementing Plain Hunt, Grandsire, and Plain Bob Major methods. Permutes pitched bells according to traditional English ringing rules. | p2b8 p2b8 p10 b32 |
| [droid-tb303-acid.ini](droid-tb303-acid.ini) | TB-303 acid bass line generator with generative and fixed pattern modes, b32 step editing, probabilistic slide, accent envelopes, and 4 embedded classic acid patterns. | p2b8 p2b8 b32 |

### Rhythm Generators

| Patch | Description | Controllers |
|-------|-------------|-------------|
| [droid-zularic-repetitor.ini](droid-zularic-repetitor.ini) | Multi Repetitor — 3-bank rhythmic gate generator with 4 outputs. Bank 1 (ZR): 8 Zularic patterns (African & world rhythms). Bank 2 (NR): 2 Numeric Repetitor patterns (algorithmic). Bank 3: Euclidean rhythms (1-13 beats, 4 phase-offset outputs). | p2b8 p2b8 |

### Disting NT Ports

Ports of algorithms from the Expert Sleepers disting NT to DROID hardware.

| Patch | Origin | Description | Controllers |
|-------|--------|-------------|-------------|
| [droid-clep-disting.ini](droid-clep-disting.ini) | clep_disting.lua | Three switchable modes: algorithmic step sequence, pure random, and stepped sine LFO with optional scale quantization. | p2b8 |
| [droid-no-control.ini](droid-no-control.ini) | no_control.lua | Self-clocking sequencer where each step's duration is random, creating organic irregular rhythms. Step durations double as pitch CV. | p2b8 |
| [droid-quad-bernoulli.ini](droid-quad-bernoulli.ini) | quad_bernoulli.lua | Four gate inputs probabilistically passed or blocked. Normaled to polyrhythmic clock divisions when unpatched. | p2b8 |
| [droid-quad-snh.ini](droid-quad-snh.ini) | sextuplet.lua | Four S&H channels sample the same CV at staggered clock divisions (/1 /2 /3 /4), producing correlated but diverging melodic lines. | p2b8 |
| [droid-random-stepped-voltage.ini](droid-random-stepped-voltage.ini) | ae_random_stepped_voltage.lua | Remembered random CV sequence that repeats until rerolled, with freeze, auto-randomize, and optional slew. | p2b8 |
| [droid-shift-register.ini](droid-shift-register.ini) | shift_register.lua | 6-stage CV shift register with optional feedback that loops stage 6 back to input for repeating patterns. | p2b8 |
| [droid-sync-latch.ini](droid-sync-latch.ini) | sync_latch.lua | Defers transport start/stop to loop boundaries so slave sequencers only change state on musical downbeats. | p2b8 |

### Utilities

| Patch | Description | Controllers |
|-------|-------------|-------------|
| [droid-bouncing-ball.ini](droid-bouncing-ball.ini) | Bouncing ball trigger generator — a decaying envelope inversely controls LFO speed, producing accelerating triggers that fade like a dropped ball. | p2b8 |
| [droid-maths-classics.ini](droid-maths-classics.ini) | Five Make Noise MATHS classic patches in one: quadrature LFO, self-modulating arcade trill, voltage-controlled slew, pulse delay, and clock divider. | p2b8 |

## TB-303 Pattern Library

[tb303-pattern-library.json](tb303-pattern-library.json) contains 70 CC BY-SA acid bass patterns from [acid-tabs.com](https://www.acid-tabs.com/) (credit: J.McConaghy). Each pattern has 16 steps with note, octave, gate type, accent, and slide data. Four curated patterns are embedded directly in the TB-303 patch as fixed playback patterns.

## Multi Repetitor Pattern Libraries

- [zr-patterns.json](zr-patterns.json) — 29 Zularic Repetitor patterns extracted from the [ZR manual](https://manuals.noiseengineering.us/zr/), including Old World (African/12-step) and New World (Funk/Rock/16-step) banks with 4 rows each (mother + 3 children).
- [mr-patterns.json](mr-patterns.json) — 52 Multi Repetitor patterns extracted from the [MR manual](https://manuals.noiseengineering.us/mr/): 16 Numeric (algorithmic prime rhythms), 16 Zularic (world music), and 20 Euclidean (generalized Euclidean). All 16-step, 4 rows per pattern.

## Documentation

- [patch-guide.md](patch-guide.md) — Detailed reference for all patches: hardware requirements, I/O mappings, control layouts, and usage tips
- [TB303 style acid patten generator.md](TB303%20style%20acid%20patten%20generator.md) — Design spec for the TB-303 patch

## License

Pattern library data is CC BY-SA (attribution: J.McConaghy / Acid-Tabs.com). Patches are provided as-is for personal use.
