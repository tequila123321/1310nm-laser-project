"""
1D finite-difference Schrodinger solver for a layered heterostructure
(BenDaniel-Duke form, position-dependent effective mass, no strain, no k.p mixing).

    -(hbar^2/2) d/dz [ (1/m(z)) d psi/dz ] + V(z) psi = E psi

Units: nm, eV, masses in m0.  hbar^2/(2 m0) = 0.0380998 eV nm^2.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal

import materials as mat

H2_2M0 = 0.0380998  # eV nm^2


class Layer:
    def __init__(self, y, thickness_nm, label=""):
        self.y = y
        self.t = thickness_nm
        self.label = label or mat.describe(y)


def build_profiles(layers, band, T=300.0, dz=0.02, qc=mat.QC_INGAASP):
    """Return z, V(z), m(z) for band in {'c','hh','lh'}.
    V is measured from the lowest band edge in the stack (well), positive upward for
    electrons and positive *into the valence band* for holes."""
    eg = np.array([mat.Eg(l.y, T) for l in layers])
    eg_min = eg.min()
    share = qc if band == "c" else (1.0 - qc)
    z_edges = np.concatenate([[0.0], np.cumsum([l.t for l in layers])])
    z = np.arange(dz / 2, z_edges[-1], dz)
    V = np.zeros_like(z)
    m = np.zeros_like(z)
    for i, l in enumerate(layers):
        sel = (z >= z_edges[i]) & (z < z_edges[i + 1])
        V[sel] = share * (eg[i] - eg_min)
        me, mhh, mlh = mat.masses(l.y)
        m[sel] = {"c": me, "hh": mhh, "lh": mlh}[band]
    return z, V, m


def solve_band(layers, band, T=300.0, dz=0.02, max_states=6):
    """Bound states of one band. Returns (energies [eV], wavefunctions [n_states, nz], z).
    Energies are relative to the well band edge (positive)."""
    z, V, m = build_profiles(layers, band, T, dz)
    nz = z.size
    # masses at half points
    m_half = 0.5 * (m[:-1] + m[1:])
    c = H2_2M0 / dz ** 2
    diag = V.copy()
    diag[:-1] += c / m_half
    diag[1:] += c / m_half
    off = -c / m_half
    vmax = V.max()
    E, psi = eigh_tridiagonal(diag, off, select="v", select_range=(-1.0, vmax - 1e-6))
    E, psi = E[:max_states], psi[:, :max_states].T
    # normalise: sum |psi|^2 dz = 1
    psi = psi / np.sqrt((psi ** 2).sum(axis=1, keepdims=True) * dz)
    return E, psi, z


def solve_structure(layers, T=300.0, dz=0.02):
    """Solve c, hh, lh bands. Returns dict with levels, wavefunctions, well gap and
    the band-edge transition wavelength (c1-hh1)."""
    out = {"T": T, "layers": layers}
    for band in ("c", "hh", "lh"):
        E, psi, z = solve_band(layers, band, T, dz)
        out[band] = {"E": E, "psi": psi}
    out["z"] = z
    well_y = min(layers, key=lambda l: mat.Eg(l.y, T)).y
    out["well_y"] = well_y
    out["Eg_well"] = mat.Eg(well_y, T)
    Ec1, Ehh1 = out["c"]["E"][0], out["hh"]["E"][0]
    out["E_edge_c1hh1"] = out["Eg_well"] + Ec1 + Ehh1
    out["lambda_edge_nm"] = mat.HC / out["E_edge_c1hh1"]
    if out["lh"]["E"].size:
        out["E_edge_c1lh1"] = out["Eg_well"] + Ec1 + out["lh"]["E"][0]
    return out


def overlap(psi_a, psi_b, dz):
    """|<psi_a|psi_b>|^2 matrix between two sets of wavefunctions."""
    return (psi_a @ psi_b.T * dz) ** 2


def single_well(well_y, barrier_y, Lw, Lb=15.0):
    """Convenience: one well between two barriers (thick enough to hold the tails)."""
    return [Layer(barrier_y, Lb, "barrier"), Layer(well_y, Lw, "well"), Layer(barrier_y, Lb, "barrier")]
