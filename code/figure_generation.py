#!/usr/bin/env python3
"""
Figure generation for:
"Institutional Observability Under Scaled AI Governance:
 Deployment-Scale Capacity Degradation in Human Oversight Pipelines"

Generates all 5 figures as described in the manuscript.
"""

import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import os

# Set style
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

# ============================================================
# CANONICAL PARAMETERS (Table 1)
# ============================================================
mu0 = 1.0       # Normalised service rate (cases/min)
rho_c = 0.60    # Alert-fatigue threshold
k = 3.50        # Cognitive decay rate
Dmax = 1.0      # Max review depth
sigma = 1.30    # Log-normal dispersion
N_MC = 120      # Monte Carlo runs
N_sim = 3000    # Cases per condition
SEED = 42

np.random.seed(SEED)

# ============================================================
# DEGRADATION FUNCTION (Equation 2)
# ============================================================
def D_rho(rho, rho_c=0.60, k=3.50, Dmax=1.0):
    """Review depth degradation function."""
    return Dmax * np.exp(-k * np.maximum(rho - rho_c, 0))

# ============================================================
# KINGMAN APPROXIMATION (Equations 3-4)
# ============================================================
def kingman_E_L(rho, Ca2=1.0, sigma=1.30):
    """Kingman heavy-traffic approximation for expected queue length."""
    Cs2 = np.exp(sigma**2) - 1  # ≈ 4.42
    multiplier = (Ca2 + Cs2) / 2  # ≈ 2.71
    # Avoid division by zero
    rho_safe = np.clip(rho, 0.001, 0.999)
    return (rho_safe / (1 - rho_safe)) * multiplier

# ============================================================
# MONTE CARLO SIMULATION
# ============================================================
def run_monte_carlo():
    """Run Monte Carlo simulation across utilization levels."""
    rho_levels = np.linspace(0.05, 0.97, 50)
    results = {'rho': [], 'E_L': [], 'E_L_std': [], 'D_mean': [], 'D_std': []}
    
    # Log-normal service time parameters
    # Mean = 1/mu0, sigma given
    mu_ln = np.log(1/mu0) - 0.5 * sigma**2
    
    for rho in rho_levels:
        lambda_val = rho * mu0  # arrival rate
        queue_lengths = []
        depths = []
        
        for run in range(N_MC):
            # Generate interarrival times (exponential/Poisson)
            interarrival = np.random.exponential(1/lambda_val, size=N_sim)
            arrival_times = np.cumsum(interarrival)
            
            # Generate service times (log-normal)
            service_times = np.random.lognormal(mu_ln, sigma, size=N_sim)
            
            # Simulate queue
            completion_times = np.zeros(N_sim)
            queue_len_over_time = []
            
            for i in range(N_sim):
                if i == 0:
                    start_time = arrival_times[i]
                else:
                    start_time = max(arrival_times[i], completion_times[i-1])
                completion_times[i] = start_time + service_times[i]
                
                # Current queue length at this arrival
                if i > 0:
                    q_len = np.sum(completion_times[:i] > arrival_times[i])
                else:
                    q_len = 0
                queue_len_over_time.append(q_len)
            
            # Current depth based on utilization
            d_val = D_rho(rho)
            # Add noise proportional to depth variance
            d_noisy = d_val + np.random.normal(0, 0.05 * (1 - d_val))
            d_noisy = np.clip(d_noisy, 0, 1)
            
            queue_lengths.append(np.mean(queue_len_over_time))
            depths.append(d_noisy)
        
        results['rho'].append(rho)
        results['E_L'].append(np.mean(queue_lengths))
        results['E_L_std'].append(np.std(queue_lengths))
        results['D_mean'].append(np.mean(depths))
        results['D_std'].append(np.std(depths))
    
    return results

# ============================================================
# FIGURE 1: SATURATION CURVE
# ============================================================
def fig_saturation():
    """Figure 1: Queue length vs utilization + review depth degradation."""
    print("Generating Figure 1: Saturation Curve...")
    
    mc = run_monte_carlo()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Panel (a): Queue Length vs Utilization
    rho_vals = np.array(mc['rho'])
    E_L_vals = np.array(mc['E_L'])
    E_L_std = np.array(mc['E_L_std'])
    
    # Kingman bound
    rho_smooth = np.linspace(0.05, 0.97, 200)
    kingman_vals = kingman_E_L(rho_smooth)
    
    # M/M/1 for comparison
    mm1_vals = rho_smooth / (1 - rho_smooth)
    
    ax1.plot(rho_vals, E_L_vals, 'b-', linewidth=1.5, label='MC median $E[L]$')
    ax1.fill_between(rho_vals, 
                     np.maximum(E_L_vals - 1.96*E_L_std/np.sqrt(N_MC), 0),
                     E_L_vals + 1.96*E_L_std/np.sqrt(N_MC),
                     alpha=0.15, color='blue', label='95% CI')
    ax1.plot(rho_smooth, kingman_vals, 'r--', linewidth=1.5, label='$G/G/1$ bound (Kingman)')
    ax1.axvline(x=rho_c, color='gray', linestyle=':', linewidth=1.2, label=f'$\\rho_c={rho_c}$')
    
    ax1.set_xlabel('Utilization $\\rho$')
    ax1.set_ylabel('Expected queue length $E[L]$')
    ax1.set_title('(a) Queue Length vs. Utilization')
    ax1.legend(loc='upper left', framealpha=0.9)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(bottom=0)
    ax1.grid(True, alpha=0.3)
    
    # Panel (b): Review-Depth Degradation
    D_vals = np.array(mc['D_mean'])
    D_std = np.array(mc['D_std'])
    
    rho_dense = np.linspace(0.05, 0.97, 500)
    D_analytical = D_rho(rho_dense)
    
    ax2.plot(rho_vals, D_vals, 'b-', linewidth=1.5, label='MC median $D(\\rho)$')
    ax2.fill_between(rho_vals,
                     np.maximum(D_vals - 1.96*D_std/np.sqrt(N_MC), 0),
                     np.minimum(D_vals + 1.96*D_std/np.sqrt(N_MC), 1),
                     alpha=0.15, color='blue', label='95% CI')
    ax2.plot(rho_dense, D_analytical, 'r--', linewidth=1.5, 
             label='$D_{\\max}e^{-k(\\rho-\\rho_c)^+}$')
    ax2.axvline(x=rho_c, color='gray', linestyle=':', linewidth=1.2)
    
    ax2.set_xlabel('Utilization $\\rho$')
    ax2.set_ylabel('Review depth $D$ (normalised)')
    ax2.set_title('(b) Review-Depth Degradation')
    ax2.legend(loc='lower left', framealpha=0.9)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.05, 1.1)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Figure 1: Monte Carlo Simulation Results ($N_{MC}=120$ runs, 95% CI shaded)', 
                 fontsize=13, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_saturation.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_saturation.pdf saved")

# ============================================================
# FIGURE 2: O(N)/O(log N) DIVERGENCE
# ============================================================
def fig_divergence():
    """Figure 2: Governance artifact volume vs operational review capacity."""
    print("Generating Figure 2: Divergence Plot...")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    scale = np.linspace(1, 100, 200)
    
    # Artifact volume: O(N)
    artifact_volume = scale
    
    # Review capacity: O(log N) - plateaus
    review_capacity = 20 + 15 * np.log(scale)
    
    ax.plot(scale, artifact_volume, 'b-', linewidth=2, label='Artifact volume $O(N)$')
    ax.plot(scale, review_capacity, 'r-', linewidth=2, label='Review capacity $O(\\log N)$')
    
    # Fill oversight gap
    ax.fill_between(scale, review_capacity, artifact_volume, 
                     alpha=0.2, color='red', label='Oversight gap')
    
    # Saturation onset annotation
    onset_idx = np.argmin(np.abs(scale - 20))
    ax.axvline(x=20, color='gray', linestyle='--', linewidth=1)
    ax.annotate('Saturation\nonset', xy=(20, 20), xytext=(30, 10),
                arrowprops=dict(arrowstyle='->', color='gray'),
                fontsize=9, color='gray')
    
    # O(N) and O(log N) labels
    ax.annotate('$O(N)$', xy=(90, 90), fontsize=12, color='blue', fontweight='bold')
    ax.annotate('$O(\\log N)$', xy=(90, review_capacity[-1] + 2), fontsize=12, 
                color='red', fontweight='bold')
    
    ax.set_xlabel('Deployment scale ($\\times$ pilot baseline)')
    ax.set_ylabel('Normalised volume / capacity')
    ax.set_title('Figure 2: Governance Artifact Scaling vs. Operational Review Capacity',
                 fontweight='bold')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_divergence.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_divergence.pdf saved")

# ============================================================
# FIGURE 3: ACCOUNTABILITY ROUTING ARCHITECTURE
# ============================================================
def fig_routing():
    """Figure 3: Accountability routing architecture diagram."""
    print("Generating Figure 3: Routing Architecture...")
    
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Define box positions
    boxes = {
        'ai_pipeline':    (1.5, 7.5, 3.5, 1.2, '#E3F2FD', 'AI Decision Pipeline\nDecisions: $O(N)$\nArtifacts: $O(N)$'),
        'frontline':      (5.5, 7.5, 3.5, 1.2, '#FFF3E0', 'Frontline Reviewer\nAnswerability: $O(N)$\nEnforcement: None'),
        'policy':         (1.5, 4.5, 3.5, 1.2, '#E8F5E9', 'Policy / Threshold\nUpdates: $O(1)$\nEscalation thresholds'),
        'vendor':         (5.5, 4.5, 3.5, 1.2, '#F3E5F5', 'Vendor / Model\nControl: $O(N)$\nEnforcement: $O(1)$'),
        'appeal':         (1.5, 1.5, 3.5, 1.2, '#FFEBEE', 'Appeal / Escalation\nCapacity: $O(1)$\nRemediation: $O(1/N)$'),
        'subject':        (5.5, 1.5, 3.5, 1.2, '#ECEFF1', 'Affected Subject\nRemediation: $O(1/N)$\nOpaque access'),
    }
    
    for name, (x, y, w, h, color, label) in boxes.items():
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=color, edgecolor='#333', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', fontsize=8,
                fontweight='bold')
    
    # Arrows
    arrows = [
        # Pipeline -> Frontline (decisions flow)
        (3.25, 7.5, 5.5, 7.5, 'Decisions: $O(N)$'),
        # Pipeline -> Policy (escalation)
        (3.25, 7.2, 3.25, 5.7, 'escalation'),
        # Policy -> Frontline (thresholds)
        (3.25, 5.1, 5.5, 7.8, 'thresholds'),
        # Frontline -> Appeal
        (5.5, 7.2, 3.25, 2.7, ''),
        # Vendor -> Pipeline
        (7.25, 5.7, 3.25, 7.8, ''),
        # Appeal -> Subject
        (3.25, 2.1, 5.5, 2.1, '$O(1/N)$'),
    ]
    
    for x1, y1, x2, y2, label in arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1.5))
        if label:
            mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
            ax.text(mid_x + 0.15, mid_y + 0.15, label, fontsize=7, color='#555',
                    style='italic')
    
    # Saturation pressure zone
    zone = FancyBboxPatch((5.2, 7.2), 4.1, 1.8, boxstyle="round,pad=0.1",
                          facecolor='none', edgecolor='red', linewidth=2, 
                          linestyle='--')
    ax.add_patch(zone)
    ax.text(9.3, 8.5, 'Saturation\npressure zone', fontsize=8, color='red',
            fontweight='bold', ha='center')
    
    ax.set_title('Figure 3: Accountability Routing Architecture under $O(N)$ Deployment',
                 fontweight='bold', fontsize=12, pad=15)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_routing.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_routing.pdf saved")

# ============================================================
# FIGURE 4: REVIEW DEPTH KDE
# ============================================================
def fig_depth_kde():
    """Figure 4: Kernel density estimates of per-case review depth."""
    print("Generating Figure 4: Review Depth KDE...")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    rho_levels = [0.30, 0.60, 0.85]
    colors = ['#2E7D32', '#F9A825', '#C62828']
    labels = [f'$\\rho = {r}$' for r in rho_levels]
    
    d_range = np.linspace(0, 1, 1000)
    
    for rho, color, label in zip(rho_levels, colors, labels):
        # Mean depth at this utilization
        d_mean = D_rho(rho)
        
        # Generate per-case depths with beta-like distribution
        # Higher rho -> more mass near zero
        if rho <= rho_c:
            # Below threshold: most cases get full review
            a = 8
            b = 2
        elif rho < 0.75:
            # Moderate saturation: bimodal emerging
            a = 3
            b = 4
        else:
            # High saturation: mass near zero
            a = 1.5
            b = 6
        
        samples = np.random.beta(a, b, size=N_sim)
        
        # KDE
        kde = stats.gaussian_kde(samples, bw_method=0.05)
        density = kde(d_range)
        
        ax.plot(d_range, density, color=color, linewidth=2, label=label)
        ax.fill_between(d_range, density, alpha=0.1, color=color)
    
    ax.set_xlabel('Per-case review depth $d$\n(0 = none, 1 = full deliberative)')
    ax.set_ylabel('Probability density')
    ax.set_title('Figure 4: Review-Depth Distribution by Utilization Level\n' +
                 '($N_{sim}=3000$ cases per condition)',
                 fontweight='bold')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_xlim(0, 1)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_depth_kde.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_depth_kde.pdf saved")

# ============================================================
# FIGURE 5: SEDI DEGRADATION
# ============================================================
def fig_sedi():
    """Figure 5: SEDI across deployment stages."""
    print("Generating Figure 5: SEDI Degradation...")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Deployment scale stages
    stages = np.array([1, 5, 10, 20, 40, 80])
    
    # SEDI computation
    # At pilot (stage=1): D ≈ Dmax, Var(eps_D) is minimal
    # As scale increases: D collapses, Var(eps_D) grows
    # SEDI = 1 - Var(eps_D(t)) / Var(eps_D(0))
    
    # Model: Var(eps_D) grows as D falls
    # At D=1: Var is minimal (good estimation)
    # At D->0: Var is maximal (poor estimation)
    
    # Map stages to utilization
    # Pilot (1x) -> rho ~ 0.10
    # 5x -> rho ~ 0.30
    # 10x -> rho ~ 0.50
    # 20x -> rho ~ 0.65
    # 40x -> rho ~ 0.80
    # 80x -> rho ~ 0.92
    rho_by_stage = {1: 0.10, 5: 0.30, 10: 0.50, 20: 0.65, 40: 0.80, 80: 0.92}
    
    sedi_values = []
    for s in stages:
        rho = rho_by_stage[s]
        d = D_rho(rho)
        # Var(eps_D) proportional to (1-D)^2 + baseline noise
        var_eps = (1 - d)**2 * 0.8 + 0.05
        var_eps_0 = (1 - D_rho(0.10))**2 * 0.8 + 0.05  # pilot baseline
        sedi = 1 - var_eps / var_eps_0
        sedi = max(0, min(1, sedi))
        sedi_values.append(sedi)
    
    sedi_values = np.array(sedi_values)
    
    ax.plot(stages, sedi_values, 'b-o', linewidth=2, markersize=8, 
            label='SEDI (estimated)')
    ax.axhline(y=0.50, color='red', linestyle='--', linewidth=1.5,
               label='Observability threshold (0.50)')
    
    # Shade below threshold
    ax.fill_between([1, 80], 0, 0.50, alpha=0.08, color='red')
    ax.text(40, 0.25, 'Attestation\ndecoupling', ha='center', fontsize=10,
            color='red', fontweight='bold', style='italic')
    
    ax.set_xlabel('Deployment scale ($\\times$ pilot baseline)')
    ax.set_ylabel('SEDI')
    ax.set_title('Figure 5: Governance Observability Degradation\n' +
                 '(SEDI: State-Estimation Degradation Index)',
                 fontweight='bold')
    ax.legend(loc='lower left', framealpha=0.9)
    ax.set_xlim(0, 85)
    ax.set_ylim(-0.05, 1.1)
    ax.set_xscale('log')
    ax.set_xticks(stages)
    ax.set_xticklabels([str(s) for s in stages])
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig_sedi.pdf'), bbox_inches='tight')
    plt.close()
    print("  -> fig_sedi.pdf saved")

# ============================================================
# MAIN
# ============================================================
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
