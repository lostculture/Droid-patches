# DROID CV Tool Library

A modular library of CV utility tools inspired by the Doepfer A-100 series,
implemented as DROID patch building blocks.

## Quick Start

```bash
python cv-tools/builder.py cv-tools/examples/utility-rack.yaml
```

## How It Works

1. **Tools** are self-contained Python modules in `cv-tools/tools/` — each
   implements one classic CV utility function (attenuverter, slew, S&H, etc.)
2. **Patch configs** are YAML files that list which tools you want and how
   they connect
3. **The builder** allocates physical I/O, controller controls, and internal
   cables, then renders a complete DROID `.ini` patch

## Patch Config Format

```yaml
name: "My Utility Rack"
description: "Clock + S&H + Quantizer"

controllers:
  - p2b8    # Controller 1
  - p2b8    # Controller 2

tools:
  - tool: clock_divider
    name: clkdiv
    inputs:
      clock: I1
    outputs:
      div_out: O1
    controls:
      ratio: P1.1
      reset_btn: B1.1
      reset_led: L1.1

  - tool: sample_hold
    name: sh1
    inputs:
      signal: I2
      trigger: _clkdiv_div_out   # internal cable from clock divider
    outputs:
      out: O2

  - tool: quantizer
    name: quant
    inputs:
      pitch: _sh1_out
    outputs:
      quantized: O3
    controls:
      root: P1.2
      scale: P2.1
```

## Available Tools

### Priority 1 — Fundamental CV Utilities
| Tool | Inspired By | Description |
|------|-------------|-------------|
| `attenuverter` | A-133 | Attenuate, invert, offset CV |
| `slew_limiter` | A-170 | Slew/portamento with separate rise/fall |
| `sample_hold` | A-148 | Sample & Hold / Track & Hold |
| `clock_divider` | A-160 | Clock divider with selectable ratio |
| `comparator` | A-167 | Compare two CVs, output gate |
| `logic` | A-166 | Boolean logic (AND/OR/XOR/NAND/NOR) |
| `trigger_delay` | A-162 | Delay triggers by time or clock |
| `vc_switch` | A-150 | Voltage-controlled signal switch |
| `sequential_switch` | A-151 | Clock-driven sequential routing |

### Priority 2 — Extended Utilities
| Tool | Inspired By | Description |
|------|-------------|-------------|
| `trigger_modifier` | A-165 | Gate↔trigger conversion, gate length |
| `precision_adder` | A-185 | Sum/transpose CVs precisely |
| `crossfader` | A-134 | Fade between two CV sources |
| `min_max` | A-172 | Output min or max of two CVs |
| `random_voltage` | A-149 | Triggered/fluctuating random CV |
| `quantizer` | A-156 | Musical scale quantizer |

### Priority 3 — Advanced
| Tool | Inspired By | Description |
|------|-------------|-------------|
| `quad_lfo` | A-143-9 | Quadrature LFO (4 phases) |
| `quad_decay` | A-142-4 | Four independent decay envelopes |
| `vc_mixer` | A-135 | Voltage-controlled CV mixer |
| `addressed_switch` | A-152 | CV-addressed switch + shift register |
| `pwm_generator` | A-168 | Variable pulse width generator |
