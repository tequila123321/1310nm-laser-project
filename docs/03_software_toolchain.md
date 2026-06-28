# 03 - Software Toolchain

## Recommended Starting Stack

| Function | Recommended tools |
|---|---|
| Active region and gain | Python/MATLAB, nextnano, Crosslight, Sentaurus, Silvaco |
| Optical waveguide | Lumerical MODE, COMSOL Wave Optics, RSoft, Photon Design |
| DFB cavity | Python CMT/TMM, Lumerical, RSoft, Photon Design |
| Electro-thermal | COMSOL, Crosslight PICS3D, Sentaurus, Silvaco |
| Layout | KLayout, gdsfactory, Nazca |
| Mask prep | GenISys BEAMER, mask-shop flow |
| Package thermal | Ansys Icepak, Simcenter Flotherm, COMSOL |
| Optical package | Zemax OpticStudio |
| Driver/package electrical | Keysight ADS, HFSS, SIwave |

## Minimum Budget Stack

```text
Python/MATLAB
Lumerical MODE or COMSOL Wave Optics
COMSOL Heat Transfer/AC/DC
KLayout
```

## Serious First-Tapeout Stack

```text
Crosslight LASTIP/PICS3D or Sentaurus/Silvaco
Lumerical MODE/FDTD
COMSOL
KLayout + gdsfactory/Nazca
GenISys BEAMER if e-beam or mask data prep is needed
```

## Productization Stack

```text
Icepak or Flotherm
Zemax OpticStudio
ADS/HFSS/SIwave
Calibre if formal signoff is required
```

## Notes

- Use QCL-specific NEGF workflows only for QCLs. A 1310 nm telecom laser is an interband MQW laser.
- Do not use full-cavity FDTD for a millimeter-class laser unless there is a very specific reason.
- Do not buy a full PIC EDA stack before the fabrication route and PDK are clear.
- KLayout is enough for early masks and internal pre-checks. Calibre becomes important for foundry signoff.

