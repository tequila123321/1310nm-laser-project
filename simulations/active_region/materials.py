"""
InGaAsP lattice-matched to InP: composition, band gap, refractive index,
effective masses, band offset.

Only lattice-matched compositions are covered (In1-xGaxAsyP1-y with x tied to y).
Strained wells need the full quaternary parameter set - not in v0.

Sources
- Eg(y):            Nahory et al., Appl. Phys. Lett. 33, 659 (1978)
- x(y):             lattice match to InP
- n(y, lambda):     Broberg & Lindgren, J. Appl. Phys. 55, 3376 (1984) (Afromowitz model)
- masses:           linear interpolation InP -> In0.53Ga0.47As (Agrawal & Dutta, Ch. 3)
- band offset:      dEc/dEg = 0.40 for InGaAsP/InP (Forrest et al. 1984)
- dEg/dT:           ~ -3.3e-4 eV/K, matches the ~0.45 nm/K lasing shift seen at 1.3 um
"""
import numpy as np

HC = 1239.84193          # eV*nm
QC_INGAASP = 0.40        # conduction band share of the gap difference


def y_from_lambda_g(lambda_g_nm):
    """As fraction y whose lattice-matched band gap wavelength is lambda_g (nm).
    Solves 0.12 y^2 - 0.72 y + (1.35 - Eg) = 0 and takes the physical root."""
    Eg = HC / lambda_g_nm
    a, b, c = 0.12, -0.72, 1.35 - Eg
    return (-b - np.sqrt(b * b - 4 * a * c)) / (2 * a)


def x_from_y(y):
    """Ga fraction that keeps In1-xGaxAsyP1-y lattice-matched to InP."""
    return 0.1894 * y / (0.4184 - 0.013 * y)


def Eg(y, T=300.0):
    """Band gap in eV at temperature T (K)."""
    return 1.35 - 0.72 * y + 0.12 * y ** 2 - 3.3e-4 * (T - 300.0)


def lambda_g(y, T=300.0):
    """Band gap wavelength in nm."""
    return HC / Eg(y, T)


def n_index(y, lambda_nm):
    """Refractive index below the gap (Broberg-Lindgren single-oscillator fit).
    Returns nan when the photon energy is within 40 meV of the gap or above it:
    the model diverges there. Use a measured value (~3.5-3.55 for 1.3 um wells)."""
    E = HC / lambda_nm
    E0 = 3.391 - 1.652 * y + 0.863 * y ** 2 - 0.123 * y ** 3
    Ed = 28.91 - 9.278 * y + 5.626 * y ** 2
    Eg0 = 1.35 - 0.72 * y + 0.12 * y ** 2
    if E > Eg0 - 0.04:
        return np.nan
    eta = np.pi * Ed / (2 * E0 ** 3 * (E0 ** 2 - Eg0 ** 2))
    n2 = (1 + Ed / E0 + Ed * E ** 2 / E0 ** 3
          + eta * E ** 4 / np.pi * np.log((2 * E0 ** 2 - Eg0 ** 2 - E ** 2) / (Eg0 ** 2 - E ** 2)))
    return float(np.sqrt(n2))


def masses(y):
    """Effective masses in units of m0: (electron, heavy hole, light hole).
    Bulk values; used both for the growth direction and in-plane (parabolic model)."""
    me = 0.080 - 0.039 * y
    mhh = 0.56 - 0.10 * y
    mlh = 0.12 - 0.07 * y
    return me, mhh, mlh


def Ep(y):
    """Kane energy in eV (InP 20.7, In0.53Ga0.47As ~25.3; linear)."""
    return 20.7 + 4.6 * y


def describe(y):
    x = x_from_y(y)
    return f"In{1 - x:.2f}Ga{x:.2f}As{y:.2f}P{1 - y:.2f} (Q{lambda_g(y) / 1000:.2f})"


if __name__ == "__main__":
    print("check values at 1310 nm")
    for name, lg in [("InP", None), ("Q1.15", 1150), ("Q1.25", 1250), ("Q1.30", 1300), ("Q1.40", 1400)]:
        y = 0.0 if lg is None else y_from_lambda_g(lg)
        me, mhh, mlh = masses(y)
        print(f"{name:6s} y={y:.3f} x={x_from_y(y):.3f} Eg={Eg(y):.3f} eV  n(1310)={n_index(y, 1310):.3f}"
              f"  me={me:.4f} mhh={mhh:.3f} mlh={mlh:.3f}")
