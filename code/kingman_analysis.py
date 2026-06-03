#!/usr/bin/env python3
"""Kingman heavy-traffic analysis for human-in-the-loop oversight pipelines."""

import numpy as np

sigma = 1.30
Cs2 = np.exp(sigma**2) - 1  # ≈ 4.42
Ca2 = 1.0  # Poisson arrivals
variance_multiplier = (Ca2 + Cs2) / 2  # ≈ 2.71

print(f"Cs² = {Cs2:.2f}")
print(f"Variance multiplier (Ca² + Cs²)/2 = {variance_multiplier:.2f}")
print(f"Human-in-the-loop pipelines saturate {variance_multiplier:.2f}× faster than M/M/1 models")

# Queue length comparison at various utilization levels
for rho in [0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]:
    mm1 = rho / (1 - rho)
    g_g_1 = mm1 * variance_multiplier
    print(f"  ρ={rho:.2f}: M/M/1 E[L]={mm1:.1f}, G/G/1 E[L]={g_g_1:.1f}")
