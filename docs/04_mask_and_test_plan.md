# 04 - Mask and Test Plan

## First Mask Philosophy

The first wafer should answer process and model questions. It should not contain only one "best guess" laser.

## Suggested Test Matrix

| Variable | Suggested values |
|---|---|
| Ridge width | 1.5, 2.0, 2.5, 3.0 um |
| Cavity length | 300, 500, 700, 800 um |
| DFB period | Center value plus wavelength sweep |
| Grating strength | Multiple etch depths or duty cycles |
| Facet coating | FP references plus DFB coating variants if available |

## Include Passive and Electrical Test Structures

- TLM for p-contact and n-contact resistance.
- Sheet resistance structures.
- Van der Pauw structures.
- Etch-depth monitor patterns.
- Grating SEM monitor areas.
- Alignment marks.
- Cleave marks.

## Measurement Plan

### Wafer or Bar Level

- Probe I-V.
- Pulsed L-I if available.
- Quick spectrum check.
- Contact resistance and sheet resistance.

### Chip/Submount Level

- CW L-I-V at controlled temperature.
- Spectrum versus current.
- Spectrum versus temperature.
- SMSR.
- Far-field pattern.
- Polarization.
- Thermal rollover.
- Lifetime screen if productization is planned.

## Data to Feed Back Into Models

- Threshold current.
- Slope efficiency.
- Series resistance.
- Wavelength offset from target.
- Temperature tuning coefficient.
- Current tuning coefficient.
- Internal loss estimate.
- Differential efficiency.
- Thermal resistance.
- DFB yield and mode-hop behavior.

