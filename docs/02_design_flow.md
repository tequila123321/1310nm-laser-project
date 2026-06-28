# 02 - Design Flow

## Step 1 - Freeze the First Spec

Define wavelength, power, temperature range, modulation need, packaging path, and fabrication route.

Recommended first target:

```text
1310 nm CW DFB laser
InP substrate
InGaAsP/InP or AlGaInAs/InP MQW
Ridge waveguide
5-10 mW at 25 C
```

## Step 2 - Choose Active Region

Use an MQW active region designed for emission near 1310 nm.

Starting assumptions:

- Material: InGaAsP/InP or AlGaInAs/InP.
- Quantum wells: 5-8 wells.
- Emission target: slightly adjusted for temperature redshift.
- Strain: consider compressive strain for TE gain.

Core outputs:

- Gain peak wavelength.
- Differential gain.
- Transparency carrier density.
- Optical confinement factor.
- Estimated threshold gain.

## Step 3 - Design the Waveguide

Model the vertical stack and ridge geometry.

Sweep:

- Ridge width: 1.5, 2.0, 2.5, 3.0 um.
- Etch depth.
- SCH thickness.
- Metal distance from mode.

Outputs:

- Effective index.
- Fundamental mode confinement.
- Higher-order mode cutoff risk.
- Metal and free-carrier absorption.
- Far-field estimate.

## Step 4 - Design the DFB Grating

Use first-order Bragg condition:

```text
lambda_B = 2 * neff * Lambda
```

If `neff = 3.2`, the first estimate is:

```text
Lambda = 1310 nm / (2 * 3.2) = 204.7 nm
```

Then sweep:

- Grating period around the first estimate.
- Coupling coefficient.
- Cavity length.
- Duty cycle.
- Grating depth.
- Quarter-wave phase shift.

Use CMT/TMM for the full cavity. Use FDTD/FEM only to verify local grating coupling and scattering.

## Step 5 - Electro-Thermal Design

QCL thermal issues are severe, but 1310 nm DFB lasers still need careful thermal modeling.

Model:

- Junction heating.
- Current spreading.
- Series resistance.
- Contact resistance.
- Submount and solder.
- Heat sink boundary condition.

Outputs:

- Junction temperature rise.
- Thermal resistance.
- Safe operating current.
- Expected wavelength shift with current and temperature.

## Step 6 - Mask and Test Matrix

The first mask should be a learning vehicle.

Include:

- FP reference lasers.
- DFB period sweep.
- Ridge width sweep.
- Cavity length sweep.
- Grating strength sweep.
- TLM and sheet-resistance structures.
- Cleave and alignment marks.

## Step 7 - Test and Model Closure

Measure:

- L-I-V.
- Spectrum versus current.
- Spectrum versus temperature.
- SMSR.
- Far field.
- Polarization.
- Series resistance.
- Thermal rollover.

Use measurement to fit:

- Internal loss.
- Mirror loss.
- Grating coupling.
- Differential gain.
- Thermal resistance.
- Contact resistance.

