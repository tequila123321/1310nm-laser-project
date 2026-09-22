"""
Step 1-3 baseline run: material check -> QW levels -> gain spectrum.

Baseline structure (placeholder, lattice-matched, to be replaced by the company's
epi or a literature structure):
    barrier Q1.15 InGaAsP, 15 nm each side
    well    Q1.40 InGaAsP, 6 nm
Outputs go to results/ (git-ignored).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import materials as mat
from qw_solver import single_well, solve_structure, build_profiles
from gain import gain_spectrum, peak_gain_sweep, fit_log_gain

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)

WELL_LG, BARRIER_LG, LW, T = 1400.0, 1150.0, 6.0, 300.0

# ---------- step 1: materials ----------
yw, yb = mat.y_from_lambda_g(WELL_LG), mat.y_from_lambda_g(BARRIER_LG)
print("== Step 1  materials (lattice-matched InGaAsP/InP) ==")
for tag, y in (("well", yw), ("barrier", yb), ("InP", 0.0)):
    me, mhh, mlh = mat.masses(y)
    print(f"  {tag:8s} {mat.describe(y):40s} Eg={mat.Eg(y, T):.3f} eV  n(1310)={mat.n_index(y, 1310):.3f}"
          f"  me={me:.4f} mhh={mhh:.3f} mlh={mlh:.3f}")
dEg = mat.Eg(yb, T) - mat.Eg(yw, T)
print(f"  dEg={dEg * 1000:.0f} meV  ->  dEc={mat.QC_INGAASP * dEg * 1000:.0f} meV, "
      f"dEv={(1 - mat.QC_INGAASP) * dEg * 1000:.0f} meV")

# ---------- step 2: quantum well ----------
qw = solve_structure(single_well(yw, yb, LW), T)
print("\n== Step 2  quantum-well levels (single well, meV above well edge) ==")
for band in ("c", "hh", "lh"):
    print(f"  {band:3s}: " + ", ".join(f"{e * 1000:.1f}" for e in qw[band]["E"]))
print(f"  c1-hh1 band edge: {qw['E_edge_c1hh1']:.4f} eV  ->  {qw['lambda_edge_nm']:.1f} nm")
if "E_edge_c1lh1" in qw:
    print(f"  c1-lh1 band edge: {qw['E_edge_c1lh1']:.4f} eV  ->  {mat.HC / qw['E_edge_c1lh1']:.1f} nm")

print("\n  well width sweep (band edge):")
lws = np.array([5.0, 5.5, 6.0, 6.5, 7.0])
lam = np.array([solve_structure(single_well(yw, yb, l), T)["lambda_edge_nm"] for l in lws])
for l, la in zip(lws, lam):
    print(f"    Lw={l:.1f} nm -> {la:.1f} nm")
print(f"  d(lambda)/d(Lw) ~ {np.polyfit(lws, lam, 1)[0]:.1f} nm per nm of well width")

lam_T = [solve_structure(single_well(yw, yb, LW), Tk)["lambda_edge_nm"] for Tk in (300.0, 358.0)]
print(f"  band edge 25 C -> 85 C: {lam_T[0]:.1f} -> {lam_T[1]:.1f} nm  ({(lam_T[1] - lam_T[0]) / 58:.2f} nm/K)")

fig, ax = plt.subplots(figsize=(6, 4))
z = qw["z"]
_, Vc, _ = build_profiles(qw["layers"], "c", T)
_, Vv, _ = build_profiles(qw["layers"], "hh", T)
ax.plot(z, Vc + qw["Eg_well"], "k")
ax.plot(z, -Vv, "k")
for e, p in zip(qw["c"]["E"], qw["c"]["psi"]):
    ax.plot(z, qw["Eg_well"] + e + 0.02 * p / np.abs(p).max(), label=f"c {e * 1000:.0f} meV")
for e, p in zip(qw["hh"]["E"], qw["hh"]["psi"]):
    ax.plot(z, -e + 0.02 * p / np.abs(p).max(), "--", label=f"hh {e * 1000:.0f} meV")
ax.set_xlabel("z (nm)")
ax.set_ylabel("energy (eV)")
ax.legend(fontsize=7)
ax.set_title(f"Q1.40/Q1.15 well {LW:.0f} nm, edge {qw['lambda_edge_nm']:.0f} nm")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "band_diagram.png"), dpi=150)

# ---------- step 3: gain ----------
print("\n== Step 3  TE material gain, per well ==")
E_ph = np.linspace(0.85, 1.05, 2001)
N_list = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]) * 1e18
fig, ax = plt.subplots(figsize=(6, 4))
for N in N_list:
    g, info = gain_spectrum(qw, N, E_ph, T=T)
    k = np.argmax(g)
    print(f"  N={N / 1e18:.1f}e18  peak {g[k]:7.0f} cm^-1 at {mat.HC / E_ph[k]:.1f} nm"
          f"   Efc={info['Efc'] * 1000:.0f} meV Efv={info['Efv'] * 1000:.0f} meV")
    ax.plot(mat.HC / E_ph, g, label=f"{N / 1e18:.1f}e18")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlim(1200, 1420)
ax.set_xlabel("wavelength (nm)")
ax.set_ylabel("material gain (1/cm)")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "gain_spectra.png"), dpi=150)

N_fine = np.linspace(0.8e18, 6e18, 27)
gp, Epk = peak_gain_sweep(qw, N_fine, E_ph, T=T)
g0, Ntr, dgdN = fit_log_gain(N_fine, gp)
print(f"\n  fit g = g0 ln(N/Ntr):  g0={g0:.0f} cm^-1  Ntr={Ntr / 1e18:.2f}e18 cm^-3  "
      f"dg/dN(2Ntr)={dgdN:.2e} cm^2")
sel = gp > 0
print(f"  gain peak wavelength: {mat.HC / Epk[sel][0]:.1f} nm at N={N_fine[sel][0] / 1e18:.1f}e18"
      f"  ->  {mat.HC / Epk[-1]:.1f} nm at N={N_fine[-1] / 1e18:.1f}e18")
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot(N_fine / 1e18, gp, "o", ms=3, label="model")
ax.plot(N_fine / 1e18, g0 * np.log(N_fine / Ntr), "-",
        label=f"g0 ln(N/Ntr), g0={g0:.0f}, Ntr={Ntr / 1e18:.2f}e18")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("N (1e18 / cm^3)")
ax.set_ylabel("peak gain (1/cm)")
ax.legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "peak_gain_vs_N.png"), dpi=150)
print(f"\nplots in {OUT}")
