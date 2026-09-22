"""
Material gain spectrum of a quantum well: parabolic subbands, 2D density of states,
k-selection, TE polarisation, Lorentzian intraband broadening, optional band-gap
renormalisation. Follows Coldren & Corzine, "Diode Lasers and Photonic Integrated
Circuits", Ch. 4. Per-well material gain (cm^-1); multiply by the confinement factor
per well from the mode solver to get modal gain.

Limits of v0 (state them when quoting numbers):
- bulk heavy-hole mass used in-plane -> hole DOS too large, N_tr somewhat high
- no strain, no valence-band mixing
- Lorentzian tails give a little artificial absorption below the band edge
"""
import numpy as np
from scipy.optimize import brentq
from scipy import signal as sig

import materials as mat
from qw_solver import overlap

Q = 1.602176634e-19
HBAR = 1.054571817e-34
M0 = 9.1093837e-31
EPS0 = 8.8541878128e-12
C = 2.99792458e8
KB = 8.617333262e-5  # eV/K


def sheet_density_2d(m, kT, Ef, E_sub):
    """2D carrier sheet density (m^-2) summed over subbands E_sub (eV, above edge)."""
    dos = m * M0 * (kT * Q) / (np.pi * HBAR ** 2)      # states per m^2 per (kT)
    x = np.clip((Ef - E_sub) / kT, -700, 700)
    return dos * np.sum(np.log1p(np.exp(x)))


def quasi_fermi_levels(N_cm3, Lw_nm, T, me, mhh, mlh, Ec, Ehh, Elh):
    """Electron and hole quasi-Fermi levels (eV) for well carrier density N (cm^-3).
    Electron level measured from the well CB edge upward; hole level measured from
    the well VB edge into the band (hole-energy convention)."""
    kT = KB * T
    ns = N_cm3 * 1e6 * Lw_nm * 1e-9                       # m^-2
    fe = lambda Ef: sheet_density_2d(me, kT, Ef, Ec) - ns
    fh = lambda Ef: sheet_density_2d(mhh, kT, Ef, Ehh) + sheet_density_2d(mlh, kT, Ef, Elh) - ns
    Efc = brentq(fe, -2.0, 2.0)
    Efv = brentq(fh, -2.0, 2.0)
    return Efc, Efv


def gain_spectrum(qw, N_cm3, E_ph, T=300.0, n_well=3.52, tau_in_ps=0.1,
                  bgr_coeff=1.6e-8, polarisation="TE"):
    """Material gain (cm^-1) versus photon energy array E_ph (eV) at density N.
    qw is the dict from qw_solver.solve_structure.
    bgr_coeff: band-gap renormalisation dEg = -bgr_coeff * N^(1/3) [eV, N in cm^-3];
    1.6e-8 gives about -20 meV at 2e18. Set 0 to switch off."""
    y = qw["well_y"]
    Lw = [l.t for l in qw["layers"] if l.label == "well"][0]
    me, mhh, mlh = mat.masses(y)
    Ec, Ehh, Elh = qw["c"]["E"], qw["hh"]["E"], qw["lh"]["E"]
    dz = qw["z"][1] - qw["z"][0]
    Eg_w = qw["Eg_well"] - bgr_coeff * N_cm3 ** (1.0 / 3.0)
    kT = KB * T
    Efc, Efv = quasi_fermi_levels(N_cm3, Lw, T, me, mhh, mlh, Ec, Ehh, Elh)

    Ep_J = mat.Ep(y) * Q
    Mb2 = M0 * Ep_J / 6.0                                  # bulk |M|^2 (kg J)
    E_J = E_ph * Q
    C0 = np.pi * Q ** 2 * HBAR / (n_well * C * EPS0 * M0 ** 2 * E_J)
    Lw_m = Lw * 1e-9

    g = np.zeros_like(E_ph)
    for hole_band, Ev, mh, kind in (("hh", Ehh, mhh, "hh"), ("lh", Elh, mlh, "lh")):
        if Ev.size == 0:
            continue
        ov = overlap(qw["c"]["psi"], qw[hole_band]["psi"], dz)   # [n_c, n_v]
        mr = me * mh / (me + mh)
        rho_r = mr * M0 / (np.pi * HBAR ** 2 * Lw_m)             # per J per m^3
        for i, Eci in enumerate(Ec):
            for j, Evj in enumerate(Ev):
                if ov[i, j] < 1e-3:
                    continue
                E_ij = Eg_w + Eci + Evj
                Et = E_ph - E_ij                                 # transverse kinetic energy
                on = Et >= 0
                Et_on = Et[on]
                Ee = Eci + Et_on * mr / me                       # electron energy above CB edge
                Eh = Evj + Et_on * mr / mh                       # hole energy into VB
                fc = 1.0 / (1.0 + np.exp(np.clip((Ee - Efc) / kT, -700, 700)))
                fh = 1.0 / (1.0 + np.exp(np.clip((Eh - Efv) / kT, -700, 700)))
                cos2 = Eci / (Eci + Et_on * mr / me + 1e-12)
                if polarisation == "TE":
                    ang = 0.75 * (1 + cos2) if kind == "hh" else (1.25 - 0.75 * cos2)
                else:  # TM
                    ang = 1.5 * (1 - cos2) if kind == "hh" else (0.5 + 1.5 * cos2)
                g[on] += C0[on] * Mb2 * ang * ov[i, j] * rho_r * (fc + fh - 1.0)
    g_cm = g / 100.0                                           # m^-1 -> cm^-1

    # Lorentzian broadening, HWHM = hbar / tau_in
    gamma = HBAR / (tau_in_ps * 1e-12) / Q                     # eV
    dE = E_ph[1] - E_ph[0]
    kern_E = np.arange(-30 * gamma, 30 * gamma + dE, dE)
    kern = (gamma / np.pi) / (kern_E ** 2 + gamma ** 2) * dE
    g_b = sig.convolve(g_cm, kern, mode="same")             # output length = len(g_cm)
    return g_b, {"Efc": Efc, "Efv": Efv, "Eg_well_renorm": Eg_w}


def peak_gain_sweep(qw, N_list, E_ph, **kw):
    """Peak gain and peak photon energy for each N. Returns two arrays."""
    gp, Epk = [], []
    for N in N_list:
        g, _ = gain_spectrum(qw, N, E_ph, **kw)
        k = np.argmax(g)
        gp.append(g[k])
        Epk.append(E_ph[k])
    return np.array(gp), np.array(Epk)


def fit_log_gain(N, gp):
    """Fit g_peak = g0 ln(N / N_tr) using points with g_peak > 0.
    Returns g0 (cm^-1), N_tr (cm^-3), differential gain dg/dN at 2 N_tr (cm^2)."""
    sel = gp > 0
    A = np.vstack([np.log(N[sel]), np.ones(sel.sum())]).T
    g0, b = np.linalg.lstsq(A, gp[sel], rcond=None)[0]
    Ntr = np.exp(-b / g0)
    dgdN = g0 / (2 * Ntr)
    return g0, Ntr, dgdN
