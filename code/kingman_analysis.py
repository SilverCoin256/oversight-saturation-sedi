#!/usr/bin/env python3
"""kingman heavy-traffic analysis — proves the 2.71x saturation multiplier"""

import numpy as np

sigma = 1.30
Cs2 = np.exp(sigma**2) - 1     # ≈ 4.42 for human review times
Ca2 = 1.0                       # poisson arrivals
variance_multiplier = (Ca2 + Cs2) / 2   # ≈ 2.71

print(f"Cs^2 = {Cs2:.2f}")
print(f"variance multiplier = {variance_multiplier:.2f}")
print(f"so human pipelines saturate {variance_multiplier:.2f}x faster than M/M/1 predicts\n")

for rho in [0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]:
    mm1 = rho / (1 - rho)
    g_g_1 = mm1 * variance_multiplier
    print(f"  rho={rho:.2f}:  M/M/1 = {mm1:.1f}  |  G/G/1 = {g_g_1:.1f}")
