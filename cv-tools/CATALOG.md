# CV Tool Catalog — Eurorack Utility Module Survey

A comprehensive catalog of CV utility functions found across the Eurorack
ecosystem, mapped to DROID feasibility. Sources: Doepfer A-100, Mutable
Instruments, Befaco, Joranalogue, Noise Engineering, Bastl, Music Thing
Modular, Intellijel, and ModularGrid community.

## Status Key

- **DONE** — Already in our library
- **NEW** — Not yet implemented, feasible in DROID
- **SKIP** — Not feasible (audio-rate only, needs hardware, or redundant)

---

## Already Implemented (20 tools)

| Tool | Inspired By | DROID Circuit | Status |
|------|-------------|---------------|--------|
| attenuverter | Doepfer A-133, MI Shades | `[copy]` | DONE |
| slew_limiter | Doepfer A-170, Joranalogue Contour 1 | `[slew]` | DONE |
| sample_hold | Doepfer A-148, MI Kinks S&H | `[sample]` | DONE |
| clock_divider | Doepfer A-160 | `[clocktool]` | DONE |
| comparator | Doepfer A-167 | `[compare]` | DONE |
| logic | Doepfer A-166, MI Kinks Logic | `[logic]` | DONE |
| trigger_delay | Doepfer A-162, NE Jam Jam | `[triggerdelay]` | DONE |
| vc_switch | Doepfer A-150 | `[switch]` | DONE |
| sequential_switch | Doepfer A-151, Befaco Muxlicer | `[switch]` | DONE |
| trigger_modifier | Doepfer A-165 | `[gatetool]` | DONE |
| precision_adder | Doepfer A-185 | `[mixer]` | DONE |
| crossfader | Doepfer A-134 | `[crossfader]` | DONE |
| min_max | Doepfer A-172, Rampage logic | `[compare]` | DONE |
| random_voltage | Doepfer A-149 | `[random]`+`[slew]` | DONE |
| quantizer | Doepfer A-156, Intellijel Scales | `[minifonion]` | DONE |
| quad_lfo | Doepfer A-143-9 | `[lfo]`+`[copy]` | DONE |
| quad_decay | Doepfer A-142-4 | `[contour]` | DONE |
| vc_mixer | Doepfer A-135 | `[mixer]` | DONE |
| addressed_switch | Doepfer A-152 | `[switch]` | DONE |
| pwm_generator | Doepfer A-168 | `[lfo]` | DONE |

---

## Batch 1 — Simple New Tools (1-2 circuits each)

| Function | Inspired By | DROID Approach | Complexity |
|----------|-------------|----------------|------------|
| **rectifier** | MI Kinks Sign section | `[compare]` — full-wave: `abs(x)`, half-wave: `max(x,0)` | Very simple |
| **flip_flop** | General utility | `[flipflop]` — toggle on trigger | Very simple |
| **bernoulli_gate** | MI Branches, DROID native | `[bernoulli]` — probabilistic gate router | Very simple |
| **burst_generator** | Rampage, various | `[burst]` — N triggers after input trigger | Very simple |
| **clock_multiplier** | Doepfer A-160-5 | `[clocktool]` with multiply param | Very simple |
| **cv_delay** | Chronoblob concept | `[delay]` — delay CV by N clock steps | Simple |
| **envelope_follower** | Doepfer A-119, Bastl Dynamo | `[slew]` with fast attack on rectified input | Simple |

### Rectifier (MI Kinks — Sign Section)
Full-wave rectification folds negative voltages positive (frequency doubler for
audio, absolute value for CV). Half-wave clips negative to zero. These are
fundamental waveshaping operations. In DROID: compare against 0, output
`input` or `-1 * input` accordingly.

### Flip-Flop / Toggle
Converts trigger pairs into alternating on/off gate. Every other trigger
toggles the output state. Essential for clock-synced binary switching. DROID
has a native `[flipflop]` circuit — this tool wraps it.

### Bernoulli Gate (MI Branches)
A probabilistic gate router: each incoming gate is randomly sent to output A
or output B based on a probability control. At 50% it's a coin flip. DROID's
`[bernoulli]` circuit does this natively.

### Burst Generator
After receiving a single trigger, outputs a configurable number of rapid
triggers. Useful for ratcheting, drum fills, and generative rhythms. DROID's
`[burst]` circuit handles this.

### Clock Multiplier (Doepfer A-160-5)
Multiplies incoming clock rate by a selectable factor (×2 to ×16). Complements
the clock_divider tool. Uses `[clocktool]` with the `multiply` parameter.

### CV Delay
Delays a CV signal by N clock steps — a clocked digital delay line for control
voltages. Creates echo/canon effects on pitch sequences. DROID's `[delay]`
circuit does this directly.

### Envelope Follower (Doepfer A-119, Bastl Dynamo)
Extracts the amplitude envelope from an incoming signal. Fast attack tracks
peaks, slow release creates a smooth follower curve. In DROID: rectify the
input (compare+copy), then slew with asymmetric rise/fall.

---

## Batch 2 — Medium Tools (3-5 circuits each)

| Function | Inspired By | DROID Approach | Complexity |
|----------|-------------|----------------|------------|
| **window_comparator** | Joranalogue Compare 2 | 2× `[compare]` + `[logic]` AND | Medium |
| **slope_detector** | Befaco Rampage | `[sample]` + `[compare]` on delayed vs current | Medium |
| **voltage_clamp** | General utility | 2× `[compare]` for min/max bounds | Medium |
| **euclidean_rhythm** | Various, DROID native | `[euklid]` — Euclidean rhythm generator | Medium |
| **shift_register** | Music Thing Turing Machine | `[sample]` chain with feedback | Medium |

### Window Comparator (Joranalogue Compare 2)
Two thresholds define a voltage window. Gate is high only when input falls
BETWEEN the low and high thresholds. More expressive than a single comparator.
Needs two comparisons ANDed together.

### Slope Detector (Befaco Rampage)
Detects whether an incoming CV is rising or falling and outputs separate gates
for each direction. Uses a one-sample delay (sample & hold on clock) to compare
current value against previous value.

### Voltage Clamp / Limiter
Constrains a CV signal to a defined range — anything above the ceiling is
clipped to ceiling, anything below the floor is clipped to floor. Two cascaded
compare operations.

### Euclidean Rhythm Generator
Distributes N hits evenly across M steps using the Euclidean algorithm. Classic
generative rhythm tool. DROID's `[euklid]` circuit is purpose-built for this.

### Shift Register (Music Thing Turing Machine)
A clocked shift register with controllable feedback probability. Creates
evolving/looping random sequences. Uses a chain of `[sample]` circuits with
configurable feedback from the last stage.

---

## Batch 3 — Complex Tools (future)

| Function | Inspired By | DROID Approach | Complexity |
|----------|-------------|----------------|------------|
| **function_generator** | Befaco Rampage, Make Noise MATHS | `[contour]`+`[lfo]` with EOC trigger | Complex |
| **chaos_generator** | Nonlinear Labs, Lorenz | Multiple `[slew]`+`[math]` feedback | Complex |
| **turing_machine** | Music Thing Turing Machine | Full shift register + lock/probability | Complex |
| **matrix_mixer** | Toppobrillo Matrixplexer | `[matrixmixer]` | Complex |
| **poly_voice_alloc** | Intellijel Polaris concept | `[polytool]` | Complex |

---

## Functions Skipped (not feasible or redundant)

| Function | Reason |
|----------|--------|
| Audio-rate wavefolder | DROID processes at CV rate, not audio |
| Ring modulator (audio) | Audio domain only |
| Physical interfaces | Joystick, ribbon, theremin — need hardware |
| MIDI conversion | DROID has dedicated MIDI circuits, not a "tool" |
| BBD / DSP effects | Audio processing, not CV utility |
| Buffered multiples | Trivial in DROID — just reference the same cable |
| Manual CV source | Pots/faders are already direct CV sources in DROID |

---

## Sources

- [Doepfer A-100 Catalog](https://doepfer.de/a100.htm)
- [Mutable Instruments Kinks](https://modulargrid.net/e/mutable-instruments-kinks)
- [Befaco Rampage](https://www.perfectcircuit.com/befaco-rampage.html)
- [Joranalogue Compare 2](https://joranalogue.com/products/compare-2)
- [Joranalogue Select 2](https://joranalogue.com/products/select-2)
- [Noise Engineering: Lesser-Known Utilities](https://noiseengineering.us/blogs/loquelic-literitas-the-blog/lesser-known-utilities/)
- [Music Thing Modular Turing Machine](https://www.musicthing.co.uk/Turing-Machine/)
- [Befaco Muxlicer](https://www.befaco.org/muxlicer-2/)
- [ModularGrid CV Utility Modules](https://modulargrid.net/e/tags/view/15)
- [MusicRadar Best Eurorack Modules](https://www.musicradar.com/news/the-best-eurorack-modules-in-the-world)
