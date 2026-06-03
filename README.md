# Oversight Saturation & SEDI — Reproducibility Package

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.0000000.svg)](https://doi.org/10.5281/zenodo.0000000)

This repository contains the complete reproducibility package for:

**"Institutional Observability Under Scaled AI Governance: Deployment-Scale Capacity Degradation in Human Oversight Pipelines"**

*Technology in Society (Elsevier), 2026*

**Author:** Shaurya Gupta (ORCID: 0009-0001-7642-9247)

---

## Abstract

Institutions deploying AI at scale accumulate governance artifacts at rates proportional to decision volume. Human interpretive capacity does not scale proportionally. This paper identifies the resulting failure mode, *oversight saturation*, as a structural consequence of deployment architecture. The repository contains all code to reproduce the Monte Carlo simulations, figures, and SEDI index computations.

---

## Repository Structure

```
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── code/
│   ├── monte_carlo_simulation.py    # Main MC simulation
│   ├── kingman_analysis.py          # Kingman heavy-traffic analysis
│   ├── depth_degradation.py         # D(rho) degradation function
│   ├── sedi_computation.py          # SEDI index calculation
│   ├── figure_generation.py         # All figure generation
│   └── utils.py                     # Shared utilities
├── data/
│   ├── simulation_outputs/          # CSV outputs from MC runs
│   └── calibration/                 # Calibration data references
├── supplementary/
│   ├── appendix_a_derivations.pdf   # Full mathematical derivations
│   ├── appendix_b_sensitivity.pdf   # Sensitivity analysis
│   └── appendix_c_scenarios.pdf     # Additional scenarios
└── manuscript/
    └── README.md                    # Link to published version
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/shauryagupta/oversight-saturation-sedi.git
cd oversight-saturation-sedi
pip install -r requirements.txt
```

### Reproduce All Results

```bash
# Run Monte Carlo simulation (120 runs, ~30 seconds)
python code/monte_carlo_simulation.py

# Generate all 5 figures
python code/figure_generation.py

# Compute SEDI values
python code/sedi_computation.py
```

### Expected Output

- `data/simulation_outputs/queue_lengths.csv` — Queue lengths across utilization levels
- `data/simulation_outputs/review_depths.csv` — Review depth values
- `data/simulation_outputs/sedi_values.csv` — SEDI index across deployment stages
- All figures regenerated in the `figures/` directory

---

## Key Parameters

| Symbol | Value | Description |
|---|---|---|
| μ₀ | 1.0 case/min | Normalised service rate |
| ρc | 0.60 | Alert-fatigue threshold |
| k | 3.50 | Cognitive decay rate |
| Dmax | 1.0 | Maximum review depth |
| σ | 1.30 | Log-normal dispersion |
| N_MC | 120 | Monte Carlo runs |

---

## Citation

If you use this code or data, please cite:

```bibtex
@article{gupta2026institutional,
  title={Institutional Observability Under Scaled AI Governance: 
         Deployment-Scale Capacity Degradation in Human Oversight Pipelines},
  author={Gupta, Shaurya},
  journal={Technology in Society},
  year={2026},
  publisher={Elsevier}
}
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Contact

Shaurya Gupta — shauryagupta042@gmail.com — [ORCID: 0009-0001-7642-9247](https://orcid.org/0009-0001-7642-9247)
