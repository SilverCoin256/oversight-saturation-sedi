#!/usr/bin/env python3
"""quick check of the D(rho) degradation curve"""

import numpy as np
from utils import D_rho

print("rho    D(rho)")
for rho in np.linspace(0, 1, 11):
    print(f"{rho:.2f}   {D_rho(rho):.4f}")

print(f"\nat rho=0.85: D = {D_rho(0.85):.4f}")
print(f"at rho=0.95: D = {D_rho(0.95):.4f}")
