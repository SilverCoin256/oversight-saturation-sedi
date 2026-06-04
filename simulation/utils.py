#!/usr/bin/env python3
"""shared functions used across all the simulation scripts"""

import numpy as np

def D_rho(rho, rho_c=0.60, k=3.50, Dmax=1.0):
    """review depth degradation (equation 2 from the paper)"""
    return Dmax * np.exp(-k * np.maximum(rho - rho_c, 0))

def kingman_E_L(rho, Ca2=1.0, sigma=1.30):
    """kingman heavy-traffic bound for expected queue length"""
    Cs2 = np.exp(sigma**2) - 1
    multiplier = (Ca2 + Cs2) / 2
    rho_safe = np.clip(rho, 0.001, 0.999)
    return (rho_safe / (1 - rho_safe)) * multiplier

def compute_sedi(rho, rho_baseline=0.10, rho_c=0.60, k=3.50):
    """calculate SEDI for a given utilization level"""
    d = D_rho(rho, rho_c, k)
    d0 = D_rho(rho_baseline, rho_c, k)
    var_eps = (1 - d)**2 * 0.8 + 0.05
    var_eps_0 = (1 - d0)**2 * 0.8 + 0.05
    return max(0, min(1, 1 - var_eps / var_eps_0))

# params from table 1
CANONICAL_PARAMS = {
    'mu0': 1.0,
    'rho_c': 0.60,
    'k': 3.50,
    'Dmax': 1.0,
    'sigma': 1.30,
    'N_MC': 120,
    'N_sim': 3000,
}
