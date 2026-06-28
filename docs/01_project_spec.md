# 01 - Project Specification

## Device Class

The baseline device is a 1310 nm InP-based interband semiconductor laser. The recommended first implementation is a DFB ridge-waveguide edge-emitting laser.

This is not a QCL project. QCLs use intersubband transitions and are normally used in mid-infrared or THz regimes. A 1310 nm telecom laser uses interband recombination in III-V quantum wells.

## Baseline Specifications

| Parameter | First-pass value | Notes |
|---|---:|---|
| Center wavelength | 1310 nm | Telecom O-band |
| Photon energy | about 0.947 eV | E = hc/lambda |
| Output power | 5-10 mW | First CW target |
| Threshold current | TBD | Extract after active/waveguide model |
| Cavity type | DFB | FP references should also be included |
| Cavity length | 300-800 um sweep | Do not freeze one value too early |
| Ridge width | 1.5-3.0 um sweep | Trade optical mode, heat, and current |
| Temperature | 25 C first, then 85 C | Product target may be wider |
| Modulation | CW first | Direct modulation can be added later |

## Open Product Questions

Answer these before detailed design:

- Is the product for datacom, sensing, seed laser, or lab source?
- Is single-longitudinal-mode operation mandatory?
- What SMSR is required?
- Is uncooled operation required?
- Is direct modulation required? If yes, target bitrate?
- Is fiber coupling required? If yes, what coupling loss target?
- Will fabrication use an InP foundry, university lab, or internal process?

