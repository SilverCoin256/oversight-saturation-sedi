#!/usr/bin/env python3
"""Depth degradation function analysis."""

import numpy as np
from utils import D_rho

rho_vals = np.linspace(0, 1, 100)
print("ρ\tD(ρ)")
for rho in rho_vals[::10]:
    print(f"{rho:.2f}\t{D_rho(rho):.4f}")

# R² check above ρc
rho_above = np.linspace(0.60, 0.97, 50)
D_analytical = D_rho(rho_above)
print(f"\nD(ρ) at ρ=0.85: {D_rho(0.85):.4f}")
print(f"D(ρ) at ρ=0.95: {D_rho(0.95):.4f}")
