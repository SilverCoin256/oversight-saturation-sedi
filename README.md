# oversight-saturation-sedi

hey! this is the code from my paper about AI governance and why human oversight breaks down when too many AI decisions pile up.

**paper:** "Institutional Observability Under Scaled AI Governance: Deployment-Scale Capacity Degradation in Human Oversight Pipelines" — submitted to Technology in Society (Elsevier)

## what this is about

basically, when companies/governments deploy AI at scale, they generate tons of compliance logs and audit trails. but the humans who are supposed to review all this stuff? they can't keep up. i called this "oversight saturation" and built a model to show how it happens.

the cool part is SEDI (State-Estimation Degradation Index) — it's a number you can calculate from public records to tell if an institution's oversight is actually working or just looks like it's working.

## what's in here

```
code/
  monte_carlo_simulation.py   <- the main simulation (120 runs)
  figure_generation.py        <- makes all 5 figures from the paper
  kingman_analysis.py         <- the 2.71x saturation proof
  sedi_computation.py         <- calculates SEDI values
  depth_degradation.py        <- the D(rho) function
  utils.py                    <- shared stuff

figures/                      <- all the output figures (pdf)
requirements.txt              <- what you need to install
```

## how to run it

you need python 3.10+ and then:

```bash
pip install -r requirements.txt
python code/monte_carlo_simulation.py
python code/figure_generation.py
python code/sedi_computation.py
```

the simulation takes like 30 seconds on a normal laptop. it'll spit out csv files with all the results and regenerate the figures.

## parameters i used

- μ₀ = 1.0 (service rate)
- ρc = 0.60 (the alert fatigue threshold — from Parasuraman & Riley 1997)
- k = 3.50 (how fast review quality drops)
- σ = 1.30 (log-normal spread for human review times)
- 120 monte carlo runs, 3000 cases each

## if you want to cite this

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

## license

MIT — do whatever you want with the code, just give credit.

## contact

shauryagupta042@gmail.com | [ORCID](https://orcid.org/0009-0001-7642-9247)
