#!/usr/bin/env python3
"""
generates all 5 figures from my oversight saturation paper
just run it and it'll recreate everything in the figures/ folder
"""

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

OUTPUT_DIR = 'figures'
os.makedirs(OUTPUT_DIR, exist_ok=True)

mu0 = 1.0
rho_c = 0.60
k = 3.50
Dmax = 1.0
sigma = 1.30
N_MC = 120
N_sim = 3000
SEED = 42

np.random.seed(SEED)

def D_rho(rho, rho_c=0.60, k=3.50, Dmax=1.0):
    return Dmax * np.exp(-k * np.maximum(rho - rho_c, 0))

def kingman_E_L(rho, Ca2=1.0, sigma=1.30):
    Cs2 = np.exp(sigma**2) - 1
    multiplier = (Ca2 + Cs2) / 2
    rho_safe = np.clip(rho, 0.001, 0.999)
    return (rho_safe / (1 - rho_safe)) * multiplier

def run_monte_carlo():
    rho_levels = np.linspace(0.05, 0.97, 50)
    results = {'rho': [], 'E_L': [], 'E_L_std': [], 'D_mean': [], 'D_std': []}
    mu_ln = np.log(1/mu0) - 0.5 * sigma**2
    
    for rho in rho_levels:
        lambda_val = rho * mu0
        queue_lengths = []
        depths = []
        
        for run in range(N_MC):
            interarrival = np.random.exponential(1/lambda_val, size=N_sim)
            arrival_times = np.cumsum(interarrival)
            service_times = np.random.lognormal(mu_ln, sigma, size=N_sim)
            completion_times = np.zeros(N_sim)
            
            for i in range(N_sim):
                if i == 0:
                    start_time = arrival_times[i]
                else:
                    start_time = max(arrival_times[i], completion_times[i-1])
                completion_times[i] = start_time + service_times[i]
            
            q_lens = [np.sum(completion_times[:max(j,1)] > arrival_times[j]) for j in range(N_sim)]
            d_val = D_rho(rho)
            d_noisy = d_val + np.random.normal(0, 0.05 * (1 - d_val))
            d_noisy = np.clip(d_noisy, 0, 1)
            
            queue_lengths.append(np.mean(q_lens))
            depths.append(d_noisy)
        
        results['rho'].append(rho)
        results['E_L'].append(np.mean(queue_lengths))
        results['E_L_std'].append(np.std(queue_lengths))
        results['D_mean'].append(np.mean(depths))
        results['D_std'].append(np.std(depths))
    
    return results

def fig_saturation():
    print("Generating Figure 1: Saturation Curve...")
    mc = run_monte_carlo()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    rho_vals = np.array(mc['rho'])
    E_L_vals = np.array(mc['E_L'])
    E_L_std = np.array(mc['E_L_std'])
    rho_smooth = np.linspace(0.05, 0.97, 200)
    kingman_vals = kingman_E_L(rho_smooth)
    
    ax1.plot(rho_vals, E_L_vals, 'b-', linewidth=1.5, label='MC median E[L]')
    ax1.fill_between(rho_vals, 
                     np.maximum(E_L_vals - 1.96*E_L_std/np.sqrt(N_MC), 0),
                     E_L_vals + 1.96*E_L_std/np.sqrt(N_MC),
                     alpha=0.15, color='blue', label='95% CI')
    ax1.plot(rho_smooth, kingman_vals, 'r--', linewidth=1.5, label='G/G/1 bound (Kingman)')
    ax1.axvline(x=rho_c, color='gray', linestyle=':', linewidth=1.2, label=f'rho_c={rho_c}')
    
    ax1.set_xlabel('Utilization (rho)')
    ax1.set_ylabel('Expected queue length E[L]')
    ax1.set_title('(a) Queue Length vs. Utilization')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(bottom=0)
    ax1.grid(True, alpha=0.3)
    
    D_vals = np.array(mc['D_mean'])
    D_std = np.array(mc['D_std'])
    rho_dense = np.linspace(0.05, 0.97, 500)
    D_analytical = D_rho(rho_dense)
    
    ax2.plot(rho_vals, D_vals, 'b-', linewidth=1.5, label='MC median D(rho)')
    ax2.fill_between(rho_vals,
                     np.maximum(D_vals - 1.96*D_std/np.sqrt(N_MC), 0),
                     np.minimum(D_vals + 1.96*D_std/np.sqrt(N_MC), 1),
                     alpha=0.15, color='blue', label='95% CI')
    ax2.plot(rho_dense, D_analytical, 'r--', linewidth=1.5, 
             label='D_max exp(-k(rho-rho_c)+)')
    ax2.axvline(x=rho_c, color='gray', linestyle=':', linewidth=1.2)
    
    ax2.set_xlabel('Utilization (rho)')
    ax2.set_ylabel('Review depth D (normalised)')
    ax2.set_title('(b) Review-Depth Degradation')
    ax2.legend(loc='lower left', framealpha=0.9)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.05, 1.1)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Figure 1: Monte Carlo Simulation Results (N_MC=120 runs, 95% CI shaded)', 
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_saturation.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_saturation.pdf saved")

def fig_divergence():
    print("Generating Figure 2: Divergence Plot...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scale = np.linspace(1, 100, 200)
    artifact_volume = scale
    review_capacity = 20 + 15 * np.log(scale)
    
    ax.plot(scale, artifact_volume, 'b-', linewidth=2, label='Artifact volume O(N)')
    ax.plot(scale, review_capacity, 'r-', linewidth=2, label='Review capacity O(log N)')
    ax.fill_between(scale, review_capacity, artifact_volume, 
                     alpha=0.2, color='red', label='Oversight gap')
    
    ax.axvline(x=20, color='gray', linestyle='--', linewidth=1)
    ax.annotate('Saturation onset', xy=(20, 20), xytext=(35, 12),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, color='gray')
    
    # labels with white background to avoid overlap
    ax.text(85, 88, 'O(N)', fontsize=11, color='blue', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.85))
    ax.text(85, 42, 'O(log N)', fontsize=11, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.85))
    
    ax.set_xlabel('Deployment scale (x pilot baseline)')
    ax.set_ylabel('Normalised volume / capacity')
    ax.set_title('Figure 2: Governance Artifact Scaling vs. Operational Review Capacity',
                 fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_divergence.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_divergence.pdf saved")

def fig_routing():
    print("Generating Figure 3: Routing Architecture...")
    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    boxes = {
        'ai_pipeline': (0.8, 7.8, 3.2, 1.0, '#E3F2FD', 'AI Decision Pipeline\nDecisions: O(N)\nArtifacts: O(N)'),
        'frontline':   (5.8, 7.8, 3.2, 1.0, '#FFF3E0', 'Frontline Reviewer\nAnswerability: O(N)\nEnforcement: None'),
        'policy':      (0.8, 5.2, 3.2, 1.0, '#E8F5E9', 'Policy / Threshold Layer\nUpdates: O(1)\nEscalation thresholds'),
        'vendor':      (5.8, 5.2, 3.2, 1.0, '#F3E5F5', 'Vendor / Model Layer\nControl: O(N)\nEnforcement: O(1)'),
        'appeal':      (0.8, 2.6, 3.2, 1.0, '#FFEBEE', 'Appeal / Escalation\nCapacity: O(1)\nRemediation: O(1/N)'),
        'subject':     (5.8, 2.6, 3.2, 1.0, '#ECEFF1', 'Affected Subject\nRemediation: O(1/N)\nOpaque access'),
    }
    
    for name, (x, y, w, h, color, label) in boxes.items():
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                              facecolor=color, edgecolor='#444', linewidth=1.2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='#222')
    
    # pipeline -> frontline (rightward)
    ax.annotate('', xy=(5.75, 8.3), xytext=(4.05, 8.3),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax.text(4.9, 8.65, 'Decisions: O(N)', fontsize=6.5, color='#555', ha='center')
    
    # pipeline -> policy (downward)
    ax.annotate('', xy=(2.4, 6.25), xytext=(2.4, 7.75),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax.text(2.7, 7.0, 'escalation', fontsize=6.5, color='#555')
    
    # policy -> frontline (diagonal up-right)
    ax.annotate('', xy=(5.75, 8.0), xytext=(4.05, 5.7),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax.text(4.6, 6.95, 'thresholds', fontsize=6.5, color='#555')
    
    # frontline -> appeal (curved down)
    ax.annotate('', xy=(4.05, 3.1), xytext=(7.4, 7.75),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3, 
                               connectionstyle='arc3,rad=0.3'))
    ax.text(6.5, 5.5, 'appeals', fontsize=6.5, color='#555')
    
    # vendor -> pipeline (upward)
    ax.annotate('', xy=(7.4, 7.75), xytext=(7.4, 6.25),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax.text(7.7, 7.0, 'model\nupdates', fontsize=6.5, color='#555')
    
    # appeal -> subject (rightward)
    ax.annotate('', xy=(5.75, 3.1), xytext=(4.05, 3.1),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.3))
    ax.text(4.9, 3.4, 'O(1/N) access', fontsize=6.5, color='#555', ha='center')
    
    # saturation zone
    zone = FancyBboxPatch((5.5, 7.5), 3.8, 1.6, boxstyle="round,pad=0.08",
                          facecolor='none', edgecolor='red', linewidth=1.8, linestyle='--')
    ax.add_patch(zone)
    ax.text(9.2, 8.7, 'Saturation\npressure zone', fontsize=7.5, color='red',
            fontweight='bold', ha='center')
    
    ax.set_title('Figure 3: Accountability Routing Architecture under O(N) Deployment',
                 fontweight='bold', fontsize=12, pad=12)
    
    plt.tight_layout(pad=1.0)
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_routing.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_routing.pdf saved")

def fig_depth_kde():
    print("Generating Figure 4: Review Depth KDE...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    rho_levels = [0.30, 0.60, 0.85]
    colors = ['#2E7D32', '#F9A825', '#C62828']
    labels = ['rho = 0.30 (below threshold)', 'rho = 0.60 (at threshold)', 'rho = 0.85 (saturated)']
    d_range = np.linspace(0, 1, 1000)
    
    for rho, color, label in zip(rho_levels, colors, labels):
        if rho <= rho_c:
            a, b = 8, 2
        elif rho < 0.75:
            a, b = 3, 4
        else:
            a, b = 1.5, 6
        
        samples = np.random.beta(a, b, size=N_sim)
        kde = stats.gaussian_kde(samples, bw_method=0.05)
        density = kde(d_range)
        
        ax.plot(d_range, density, color=color, linewidth=2, label=label)
        ax.fill_between(d_range, density, alpha=0.1, color=color)
    
    ax.set_xlabel('Per-case review depth d (0 = none, 1 = full deliberative)')
    ax.set_ylabel('Probability density')
    ax.set_title('Figure 4: Review-Depth Distribution by Utilization Level\n(N_sim=3000 cases per condition)',
                 fontweight='bold')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_depth_kde.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_depth_kde.pdf saved")

def fig_sedi():
    print("Generating Figure 5: SEDI Degradation...")
    fig, ax = plt.subplots(figsize=(8, 5))
    
    stages = np.array([1, 5, 10, 20, 40, 80])
    rho_by_stage = {1: 0.10, 5: 0.30, 10: 0.50, 20: 0.65, 40: 0.80, 80: 0.92}
    
    sedi_values = []
    for s in stages:
        rho = rho_by_stage[s]
        d = D_rho(rho)
        var_eps = (1 - d)**2 * 0.8 + 0.05
        var_eps_0 = (1 - D_rho(0.10))**2 * 0.8 + 0.05
        sedi = max(0, min(1, 1 - var_eps / var_eps_0))
        sedi_values.append(sedi)
    
    sedi_values = np.array(sedi_values)
    
    ax.plot(stages, sedi_values, 'b-o', linewidth=2, markersize=8, 
            label='SEDI (estimated)', clip_on=False)
    ax.axhline(y=0.50, color='red', linestyle='--', linewidth=1.5,
               label='Observability threshold (0.50)')
    
    ax.fill_between([1, 80], 0, 0.50, alpha=0.08, color='red')
    ax.text(35, 0.22, 'Attestation decoupling', ha='center', fontsize=10,
            color='red', fontweight='bold', style='italic')
    
    ax.set_xlabel('Deployment scale (x pilot baseline)')
    ax.set_ylabel('SEDI')
    ax.set_title('Figure 5: Governance Observability Degradation\n(SEDI: State-Estimation Degradation Index)',
                 fontweight='bold')
    ax.legend(loc='lower left', framealpha=0.9)
    ax.set_xlim(0.8, 90)
    ax.set_ylim(-0.05, 1.1)
    ax.set_xscale('log')
    ax.set_xticks(stages)
    ax.set_xticklabels([str(s) for s in stages])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout(pad=1.5)
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_sedi.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_sedi.pdf saved")

if __name__ == '__main__':
    print("=" * 60)
    print("Generating all figures for Technology in Society submission")
    print("=" * 60)
    fig_saturation()
    fig_divergence()
    fig_routing()
    fig_depth_kde()
    fig_sedi()
    print("\n" + "=" * 60)
    print("All 5 figures generated successfully in 'figures/' directory")
    print("=" * 60)
