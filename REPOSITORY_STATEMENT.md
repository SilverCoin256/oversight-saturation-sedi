# Repository Statement

**Repository:** https://github.com/SilverCoin256/oversight-saturation-sedi

---

## Contents

The repository contains all code, figures, and manuscript files needed to reproduce the results in "Institutional Observability Under Scaled AI Governance."

### Code (simulation/)
- monte_carlo_simulation.py — Main simulation (120 runs, 50 rho levels)
- figure_generation.py — Generates all 5 figures
- kingman_analysis.py — 2.71x saturation proof
- sedi_computation.py — SEDI index calculation
- depth_degradation.py — D(rho) degradation function
- utils.py — Shared utilities

### Figures (figures/)
All 5 figure PDFs from the paper.

### Manuscript (manuscript/)
Final manuscript PDF and cover letter PDF.

### Requirements
Python 3.10+, numpy, scipy, pandas, matplotlib.

### License
MIT — free to use, modify, and distribute with attribution.

---

## Reproducibility

To reproduce all results:
```bash
git clone https://github.com/SilverCoin256/oversight-saturation-sedi.git
cd oversight-saturation-sedi
pip install -r requirements.txt
python simulation/figure_generation.py
```

All figures will be regenerated in the figures/ directory.
