# oversight-saturation-sedi

Simulation code for *Institutional Observability Under Scaled AI Governance: Deployment-Scale Capacity Degradation in Human Oversight Pipelines*, submitted to *Technology in Society*.

The model tests how review depth changes as workload approaches the capacity of a human review queue. The State-Estimation Degradation Index (SEDI) uses observable traces of the queue to estimate changes in review depth under the model’s assumptions.

## Repository contents

```
simulation/
  monte_carlo_simulation.py   <- the main simulation (120 runs)
  figure_generation.py        <- makes all 5 figures from the paper
  kingman_analysis.py         <- the 2.71x saturation proof
  sedi_computation.py         <- calculates SEDI values
  depth_degradation.py        <- the D(rho) function
  utils.py                    <- shared stuff

figures/                      <- all the output figures (pdf)
manuscript/                   <- the paper + cover letter (pdf)
requirements.txt              <- what you need to install
```

## Run the simulation

Use Python 3.10 or newer.

```bash
pip install -r requirements.txt
(cd simulation && python monte_carlo_simulation.py)
python simulation/figure_generation.py
python simulation/sedi_computation.py
```

The scripts write simulation results as CSV files and regenerate the figures.

## Simulation parameters

- μ₀ = 1.0 (service rate)
- ρc = 0.60 (the alert fatigue threshold — from Parasuraman & Riley 1997)
- k = 3.50 (how fast review quality drops)
- σ = 1.30 (log-normal spread for human review times)
- 120 monte carlo runs, 3000 cases each

## Citation

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

## License

The code is available under the [MIT License](LICENSE).

## Contact

shauryagupta042@gmail.com | [ORCID](https://orcid.org/0009-0001-7642-9247)
