# Layout

Put mask layout source files here.

Suggested structure:

- `klayout/` for KLayout macros and DRC scripts.
- `gdsfactory/` or `nazca/` for parameterized layout generation.
- `gds/` for exported GDS files when needed.

The first layout should include a test matrix: FP references, DFB period sweep, ridge width sweep, cavity length sweep, TLM, sheet-resistance structures, alignment marks, and cleave marks.

