# 1310 nm Semiconductor Laser Project

This repo tracks the design of a 1310 nm InP-based semiconductor laser. The default starting point is a ridge-waveguide DFB edge-emitting laser for CW single-mode operation.

Important correction: a 1310 nm telecom laser is normally an interband InP/InGaAsP or InP/AlGaInAs device, not a QCL. QCL design tools and workflows are not the main path for this project.

## Baseline Target

| Item | Initial target |
|---|---|
| Wavelength | 1310 nm |
| Device type | DFB edge-emitting laser |
| Material platform | InP with InGaAsP or AlGaInAs MQW |
| Operation | CW first, direct modulation later if needed |
| Output power | 5-10 mW first-pass target |
| Temperature | Start at 25 C, then evaluate up to 85 C |
| Waveguide | Ridge waveguide |
| Cavity | First-order DFB grating with optional quarter-wave phase shift |
| First tapeout goal | Test matrix, not one single design |

## Recommended Software Stack

Minimum practical stack:

- Python or MATLAB for analytical models, parameter sweeps, and fitting.
- Lumerical MODE/FDTD or COMSOL Wave Optics for optical modes and grating checks.
- COMSOL Multiphysics for electro-thermal and package-level first models.
- KLayout with Python, gdsfactory, or Nazca for GDS layout.

Expanded engineering stack:

- Crosslight LASTIP/PICS3D, Synopsys Sentaurus, or Silvaco for laser TCAD.
- GenISys BEAMER for e-beam or mask data preparation.
- Ansys Icepak or Simcenter Flotherm for package thermal simulation.
- Zemax OpticStudio for coupling, collimation, and optical packaging.
- Keysight ADS/HFSS/SIwave for high-speed driver and package parasitics.

## Repo Structure

```text
docs/          Project specs, design flow, simulation plan, mask plan
simulations/   Scripts and model inputs
layout/        KLayout/gdsfactory/Nazca layout sources
experiments/   Measurement plans and test data
references/    Papers, vendor notes, design references
tasks.md       Near-term execution checklist
```

## First Milestone

Create a defensible first-pass DFB design:

1. Freeze initial device spec.
2. Choose material system and MQW starting structure.
3. Build optical waveguide model.
4. Estimate DFB grating period and coupling strength.
5. Build thermal/electrical first model.
6. Create mask test matrix.
7. Prepare measurement plan for L-I-V, spectrum, thermal rollover, and SMSR.

