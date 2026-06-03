#!/usr/bin/env python3
"""
monte carlo sim for the oversight saturation model
runs 120 independent simulations across 50 utilization levels
"""

import numpy as np
import pandas as pd
import os

# from table 1 in the paper
mu0 = 1.0        # cases per minute
rho_c = 0.60     # alert fatigue kicks in here
k = 3.50         # how steep the drop is
Dmax = 1.0       # best possible review depth
sigma = 1.30     # how much human review times vary
N_MC = 120       # monte carlo runs
N_sim = 3000     # cases per run
SEED = 42

np.random.seed(SEED)

def D_rho(rho):
    """review depth at a given utilization (equation 2)"""
    return Dmax * np.exp(-k * np.maximum(rho - rho_c, 0))

def run_simulation():
    rho_levels = np.linspace(0.05, 0.97, 50)
    mu_ln = np.log(1/mu0) - 0.5 * sigma**2
    
    rows = []
    for rho in rho_levels:
        lambda_val = rho * mu0
        for run in range(N_MC):
            # poisson arrivals + log-normal service times
            interarrival = np.random.exponential(1/lambda_val, size=N_sim)
            arrival_times = np.cumsum(interarrival)
            service_times = np.random.lognormal(mu_ln, sigma, size=N_sim)
            completion_times = np.zeros(N_sim)
            
            for i in range(N_sim):
                start = arrival_times[i] if i == 0 else max(arrival_times[i], completion_times[i-1])
                completion_times[i] = start + service_times[i]
            
            # track queue length at each arrival
            q_lens = [np.sum(completion_times[:max(i,1)] > arrival_times[i]) for i in range(N_sim)]
            d_val = D_rho(rho)
            d_noisy = np.clip(d_val + np.random.normal(0, 0.05*(1-d_val)), 0, 1)
            
            rows.append({
                'rho': rho, 'run': run,
                'mean_queue_length': np.mean(q_lens),
                'review_depth': d_noisy
            })
    
    df = pd.DataFrame(rows)
    os.makedirs('../data/simulation_outputs', exist_ok=True)
    df.to_csv('../data/simulation_outputs/queue_lengths.csv', index=False)
    
    summary = df.groupby('rho').agg(
        E_L_mean=('mean_queue_length', 'mean'),
        E_L_std=('mean_queue_length', 'std'),
        D_mean=('review_depth', 'mean'),
        D_std=('review_depth', 'std')
    ).reset_index()
    summary.to_csv('../data/simulation_outputs/review_depths.csv', index=False)
    
    print(f"done! {len(rows)} rows across {len(rho_levels)} rho levels")
    return summary

if __name__ == '__main__':
    run_simulation()
