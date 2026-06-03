#!/usr/bin/env python3
"""SEDI index computation from simulation outputs."""

import numpy as np
import pandas as pd
import os

def D_rho(rho, rho_c=0.60, k=3.50, Dmax=1.0):
    return Dmax * np.exp(-k * np.maximum(rho - rho_c, 0))

stages = np.array([1, 5, 10, 20, 40, 80])
rho_by_stage = {1: 0.10, 5: 0.30, 10: 0.50, 20: 0.65, 40: 0.80, 80: 0.92}

sedi_values = []
for s in stages:
    rho = rho_by_stage[s]
    d = D_rho(rho)
    var_eps = (1 - d)**2 * 0.8 + 0.05
    var_eps_0 = (1 - D_rho(0.10))**2 * 0.8 + 0.05
    sedi = max(0, min(1, 1 - var_eps / var_eps_0))
    sedi_values.append({'stage': s, 'rho': rho, 'D': d, 'SEDI': sedi})
    print(f"Stage {s:3d}×: ρ={rho:.2f}, D={d:.3f}, SEDI={sedi:.3f}")

df = pd.DataFrame(sedi_values)
os.makedirs('../data/simulation_outputs', exist_ok=True)
df.to_csv('../data/simulation_outputs/sedi_values.csv', index=False)
print("\nSEDI values saved.")
