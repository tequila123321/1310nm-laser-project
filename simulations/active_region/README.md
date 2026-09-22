# Active region, steps 1-3 (v0, Python only)

```text
materials.py     InGaAsP/InP lattice-matched parameters (Eg, n, masses, offset)
qw_solver.py     1D finite-difference Schrodinger (BenDaniel-Duke), c / hh / lh levels
gain.py          2D parabolic-band TE gain spectrum, Lorentzian broadening, g0 ln(N/Ntr) fit
run_baseline.py  runs all three on the placeholder structure, writes results/*.png
```

Run: `python run_baseline.py` (needs numpy, scipy, matplotlib).

## Placeholder structure

Lattice-matched, no strain. Replace with the company's epi or a literature structure.

| Layer | Material | Thickness |
|---|---|---|
| barrier | Q1.15 InGaAsP (In0.81Ga0.19As0.40P0.60) | 15 nm each side |
| well | Q1.40 InGaAsP (In0.66Ga0.34As0.74P0.26) | 6 nm |

## Check values (2026-09-22)

Step 1, refractive index at 1310 nm: InP 3.207, Q1.15 3.375, Q1.25 3.447. Literature: 3.20-3.21, ~3.37, ~3.44.
The index model returns nan within 40 meV of the gap (Q1.30 and the well at 1310 nm). Use ~3.5-3.55 for the well in the mode solver.

Step 2, single 6 nm well: c1 = 41 meV, hh1 = 13 meV, lh1 = 44 meV, band offset 77 / 116 meV.
c1-hh1 band edge 1320 nm. Sensitivity 12 nm per nm of well width, 0.47 nm/K (25 to 85 C: 1320 -> 1348 nm).

Step 3, TE material gain per well: Ntr = 2.0e18 cm^-3, g0 = 2500-2600 cm^-1, dg/dN = 6e-16 cm^2 at 2 Ntr.
Gain peak at 1.5 Ntr: 1306 nm without band-gap renormalisation, 1339 nm with -20 meV at 2e18.
Treat the absolute gain-peak wavelength as +/- 15 nm until measured PL / lasing data pins the renormalisation.

## Known limits of v0

- Bulk heavy-hole mass used in-plane: hole DOS too high, Ntr on the high side, hole quasi-Fermi level sits in the gap below 5e18.
- No strain and no valence-band mixing. Real 1310 nm wells are usually 0.5-1.5 % compressively strained; that needs the full quaternary parameter set (next task).
- Band-gap renormalisation is a single tunable coefficient (`bgr_coeff`), not a calculation.
- Lorentzian broadening puts a small artificial absorption tail below the band edge.

## Next

1. Strained-well parameters (Pikus-Bir shifts) in `materials.py`, then re-run.
2. Mode solver (`../waveguide/`, femwell) to get neff and the per-well confinement factor.
3. Modal gain = Gamma_well x N_wells x material gain feeds the threshold model in step 5.
