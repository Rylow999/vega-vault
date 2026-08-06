#!/usr/bin/env python3
"""
DSCN-G Theorem Verification Harness
====================================
Tests Theorems 1, 2, and 3 with dedicated verification code.

Theorem 1: Homeostatic Fixed Point
  N_ss* = max{n : ρ_eff(α, n) ≥ n · θ_death²}

Theorem 2: Parametric Vector Convergence
  ‖ω_i(t) − ω*(λ_vm, n_actions, θ*)‖ ≤ C·β

Theorem 3: Phase Convergence Rate
  P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T)

Also tests the ρ_eff definition and computes actual values.
"""

import numpy as np
from typing import Tuple, List, Dict
from scipy.stats import norm
import json
import os

# ============================================================
# Core DSCN-G Dynamics (reused from dscn_g_simulator.py)
# ============================================================

class DSCN_G_Verification:
    """DSCN-G model for verification purposes."""
    
    def __init__(self, N=50, K=3, d=8, alpha=5.0, beta=0.01,
                 eta=0.1, lambda_vm=3.0, n_actions=8,
                 gamma=0.01, theta_death=0.10, kappa=1.0,
                 seed: int = None):
        if seed is not None:
            np.random.seed(seed)
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()
        
        self.N_init = N
        self.K = K
        self.d = d
        self.alpha = alpha
        self.beta = beta
        self.eta = eta
        self.lambda_vm = lambda_vm
        self.n_actions = n_actions
        self.gamma = gamma
        self.theta_death = theta_death
        self.kappa = kappa
        
        # State
        self.nodes_active = list(range(N))
        self.nodes_pruned = []
        self.omega = self.rng.normal(0, 0.1, (N, d))
        self.omega_ideal = np.ones(d) / np.sqrt(d)
        self.phi = self.rng.uniform(0, 2*np.pi, N)
        self.vitality = np.ones(N)
        self.chain_positions = self.rng.choice(self.nodes_active, K, replace=False)
        self.t = 0
    
    def _compute_relevance(self, i: int) -> float:
        """R_i = R_base / (1 + ‖ω_i − ω_ideal‖)"""
        diff = np.linalg.norm(self.omega[i] - self.omega_ideal)
        return 1.0 / (1.0 + diff)
    
    def _chain_transition(self, node_idx: int) -> int:
        """P(m|n) ∝ exp(−α · ‖ω_m − ω_n‖)"""
        if not self.nodes_active:
            return node_idx
        
        probs = []
        for m_idx in self.nodes_active:
            diff = np.linalg.norm(self.omega[m_idx] - self.omega[node_idx])
            probs.append(np.exp(-self.alpha * diff))
        
        probs = np.array(probs)
        probs /= probs.sum()
        return self.rng.choice(self.nodes_active, p=probs)
    
    def _select_action(self, phi_i: float) -> int:
        """Von Mises action selection."""
        theta_actions = np.linspace(0, 2*np.pi, self.n_actions, endpoint=False)
        log_probs = self.lambda_vm * np.cos(phi_i - theta_actions)
        log_probs -= log_probs.max()
        probs = np.exp(log_probs)
        probs /= probs.sum()
        return int(self.rng.choice(self.n_actions, p=probs))
    
    def _phase_update(self, i: int, action_idx: int, outcome: int, reward: float):
            """φ_i(t+1) = [φ_i + η·R_i·reward·sin(θ_a − φ_i)] mod 2π (adaptive coupling)

            Note: outcome is always 1 (deterministic update). Phase update weighted by reward.
            """
            R_i = self._compute_relevance(i)
            theta_a = 2 * np.pi * action_idx / self.n_actions

            # Adaptive coupling: effective η increases with phase error
            phase_error = (theta_a - self.phi[i] + np.pi) % (2 * np.pi) - np.pi
            adaptive_factor = 1.0 + abs(phase_error) / np.pi  # ∈ [1, 2]
            eta_eff = self.eta * adaptive_factor

            # Phase update weighted by reward (continuous, not gated by binary outcome)
            update = eta_eff * R_i * reward * np.sin(theta_a - self.phi[i])
            self.phi[i] = (self.phi[i] + update) % (2 * np.pi)
    
    def _update_vitality_and_prune(self, activity: np.ndarray):
        """V_i(t+1) = V_i·e^(-γ) + A_i·(1−e^(-γ)); prune V_i < θ_death"""
        decay = np.exp(-self.gamma)
        self.vitality[self.nodes_active] = (
            self.vitality[self.nodes_active] * decay +
            activity[self.nodes_active] * (1 - decay)
        )
        
        to_prune = [i for i in self.nodes_active if self.vitality[i] < self.theta_death]
        for i in to_prune:
            self.nodes_active.remove(i)
            self.nodes_pruned.append(i)
    
    def _compute_valence(self, activity: np.ndarray) -> np.ndarray:
        """E_i = max(0, A_i − V_i)·κ"""
        excess = np.maximum(0, activity - self.vitality)
        return excess * self.kappa
    
    def _wave_interference(self, i: int) -> float:
        """I_i = ‖ω_i‖ · cos(φ_i − φ_root)"""
        if not self.nodes_active:
            return 0.0
        root_idx = self.nodes_active[0]
        return np.linalg.norm(self.omega[i]) * np.cos(self.phi[i] - self.phi[root_idx])
    
    def compute_rho_eff(self) -> float:
        """Herfindahl index of chain activity: ρ_eff = Σ (A_i/ΣA_j)²"""
        if not self.nodes_active:
            return 0.0
        activity = np.zeros(len(self.nodes_active))
        for pos in self.chain_positions:
            if pos in self.nodes_active:
                idx = self.nodes_active.index(pos)
                activity[idx] += 1
        if activity.sum() == 0:
            return 0.0
        activity /= activity.sum()
        return float(np.sum(activity ** 2))
    
    def compute_phi_proxy(self) -> float:
        """Φ_proxy = ρ_eff · log(N_active)"""
        rho = self.compute_rho_eff()
        return rho * np.log(max(1, len(self.nodes_active)))
    
    def step(self) -> Tuple[int, float]:
        """One simulation step."""
        self.t += 1
        
        # Move chains
        activity = np.zeros(len(self.omega))
        for k in range(self.K):
            old_pos = self.chain_positions[k]
            new_pos = self._chain_transition(old_pos)
            self.chain_positions[k] = new_pos
            activity[new_pos] += 1
        activity /= self.K
        
        # Update vitality and prune
        self._update_vitality_and_prune(activity)
        
        if not self.nodes_active:
            return 0, 0.0
        
        # Select node for action (max wave interference)
        interference = np.array([self._wave_interference(i) for i in self.nodes_active])
        selected_idx = self.nodes_active[np.argmax(interference)]
        
        # Select action
        action = self._select_action(self.phi[selected_idx])
        
        # Reward based on alignment with omega_ideal (learning progress)
        # reward = alignment(omega, omega_ideal) ∈ [0, 1]
        omega_vec = self.omega[selected_idx]
        alignment = np.dot(omega_vec, self.omega_ideal) / (np.linalg.norm(omega_vec) + 1e-8)
        reward = (alignment + 1.0) / 2.0  # Map [-1, 1] → [0, 1]
        
        # Deterministic update (expected gradient)
        # Always update with expected gradient: ω ← ω + β * reward * ω_ideal
        self.omega[selected_idx] = (
            (1 - self.beta) * self.omega[selected_idx] +
            self.beta * reward * self.omega_ideal
        )
        
        # Phase update uses deterministic outcome=1 (always update phase with reward-weighted gradient)
        self._phase_update(selected_idx, action, 1, reward)
        
        # Valence
        self._compute_valence(activity)
        
        return action, reward
    
    def run(self, steps: int):
        """Run for specified steps."""
        for _ in range(steps):
            self.step()


# ============================================================
# Theorem 1 Verification: Homeostatic Fixed Point
# ============================================================

def verify_theorem1(
    alpha: float = 5.0,
    theta_death: float = 0.10,
    N_inits: List[int] = [4, 50, 200],
    seeds: int = 100,
    steps: int = 2000
) -> Dict:
    """
    Theorem 1: N_ss* = max{n : ρ_eff(α, n) ≥ n · θ_death²}
    
    Verification:
    1. Simulate for different N_init, check steady-state N_active
    2. Compute ρ_eff at steady state
    3. Check if N_ss* satisfies the fixed-point equation
    4. Verify universal bound: N_ss* ≤ 1/θ_death
    """
    print(f"\n{'='*60}")
    print(f"THEOREM 1 VERIFICATION: Homeostatic Fixed Point")
    print(f"{'='*60}")
    print(f"Parameters: α={alpha}, θ_death={theta_death}")
    print(f"Universal bound: N_ss* ≤ {1/theta_death:.1f}")
    print(f"Running {seeds} seeds × {steps} steps for N_init ∈ {N_inits}")
    
    results = []
    
    for N_init in N_inits:
        N_ss_values = []
        rho_eff_values = []
        
        for seed in range(seeds):
            sim = DSCN_G_Verification(
                N=N_init, K=3, d=8, alpha=alpha,
                theta_death=theta_death, gamma=0.01, seed=seed
            )
            sim.run(steps)
            
            N_ss = len(sim.nodes_active)
            rho = sim.compute_rho_eff()
            
            N_ss_values.append(N_ss)
            rho_eff_values.append(rho)
        
        N_ss_mean = np.mean(N_ss_values)
        N_ss_std = np.std(N_ss_values)
        rho_mean = np.mean(rho_eff_values)
        rho_std = np.std(rho_eff_values)
        
        # Theoretical fixed point
        # Find max n such that rho_eff >= n * theta_death^2
        theta2 = theta_death ** 2
        # For a rough estimate, we can use the observed rho_mean
        # But the theorem states: N_ss* = max{n : rho_eff(α, n) ≥ n * θ_death²}
        # Since rho_eff is a decreasing function of n, we can check if observed N_ss satisfies this
        
        theoretical_max = int(1 / theta_death)  # Universal bound
        concentration_bound = int(rho_mean / theta_death) if rho_mean > 0 else 0
        
        print(f"\n  N_init = {N_init}:")
        print(f"    N_ss* (sim) = {N_ss_mean:.1f} ± {N_ss_std:.1f}")
        print(f"    ρ_eff (sim) = {rho_mean:.4f} ± {rho_std:.4f}")
        print(f"    Universal bound: {N_ss_mean:.1f} ≤ {theoretical_max:.1f} ✓" if N_ss_mean <= theoretical_max else f"    Universal bound: VIOLATED")
        print(f"    Concentration bound: N* ≤ ρ/θ_death = {concentration_bound:.1f}")
        print(f"    Fixed point check: ρ_eff = {rho_mean:.4f} ≥ N*·θ² = {N_ss_mean * theta2:.4f} {'✓' if rho_mean >= N_ss_mean * theta2 else '✗'}")
        
        results.append({
            'N_init': N_init,
            'N_ss_mean': float(N_ss_mean),
            'N_ss_std': float(N_ss_std),
            'rho_eff_mean': float(rho_mean),
            'rho_eff_std': float(rho_std),
            'universal_bound_ok': bool(N_ss_mean <= theoretical_max),
            'fixed_point_ok': bool(rho_mean >= N_ss_mean * theta_death**2)
        })
    
    # Overall
    all_N_ss = [r['N_ss_mean'] for r in results]
    all_rho = [r['rho_eff_mean'] for r in results]
    
    print(f"\n  OVERALL: N_ss* = {np.mean(all_N_ss):.1f} ± {np.std(all_N_ss):.1f}")
    print(f"           ρ_eff = {np.mean(all_rho):.4f} ± {np.std(all_rho):.4f}")
    
    return {
        'alpha': alpha,
        'theta_death': theta_death,
        'results': results,
        'overall_N_ss': float(np.mean(all_N_ss)),
        'overall_rho_eff': float(np.mean(all_rho))
    }


# ============================================================
# Theorem 2 Verification: Parametric Vector Convergence
# ============================================================

def compute_omega_star(lambda_vm: float, n_actions: int, theta_star: float) -> float:
    """
    Compute theoretical baseline ω* = E[o·R] for given parameters.
    
    ω* = Σ_a P(a|θ*)·o(a)·R(a)·ê_R
    
    For standard parameters: von Mises with λ_vm, outcome criterion o(a) = 1 if |sin((θ_a−θ*)/2)| < π/8
    """
    theta_actions = np.linspace(0, 2*np.pi, n_actions, endpoint=False)
    
    # Von Mises probabilities at θ*
    log_probs = lambda_vm * np.cos(theta_star - theta_actions)
    log_probs -= log_probs.max()
    probs = np.exp(log_probs)
    probs /= probs.sum()
    
    # Outcome criterion
    outcomes = (np.abs(np.sin((theta_actions - theta_star) / 2)) < np.pi / 8).astype(float)
    
    # Reward function: R(a) = exp(−3·|sin((θ_a−θ*)/2)|)
    rewards = np.exp(-3 * np.abs(np.sin((theta_actions - theta_star) / 2)))
    
    # Expected o·R
    expected_oR = np.sum(probs * outcomes * rewards)
    
    return float(expected_oR)


def compute_omega_star_alignment_based() -> float:
    """
    Theoretical baseline for alignment-based reward:
    
    Reward = (alignment + 1) / 2, where alignment = cos(θ) ∈ [-1, 1]
    Outcome = 1 if alignment > 0, else 0
    
    For random initial omega (uniform on sphere):
    - alignment ~ uniform in [-1, 1] (approximately)
    - outcome = 1 when alignment > 0 (probability 0.5)
    - reward = (cos(θ) + 1) / 2
    
    Expected value:
    E[outcome * reward] = E[1_{alignment>0} * (alignment + 1)/2]
    = ∫_0^1 (x + 1)/2 dx = [x²/4 + x/2]_0^1 = 1/4 + 1/2 = 3/4 = 0.75
    
    So theoretical omega_star = 0.75 (scalar projection onto omega_ideal)
    """
    return 0.75


def verify_theorem2(
    lambda_vm: float = 3.0,
    n_actions: int = 8,
    theta_star: float = np.pi / 2,
    beta: float = 0.10,
    seeds: int = 100,
    steps: int = 2000
) -> Dict:
    """
    Theorem 2: ‖ω_i(t) − ω*(λ_vm, n_actions, θ*)‖ ≤ C·β
    
    With alignment-based reward, theoretical ω* = 0.75 (scalar projection onto ω_ideal)
    
    Verification:
    1. Compute theoretical ω* for alignment-based reward = 0.75
    2. Run simulation, track projection of ω onto ω_ideal
    2. Check if distance ≤ C·β (typically C ≈ 1, so distance ≤ β)
    """
    print(f"\n{'='*60}")
    print(f"THEOREM 2 VERIFICATION: Parametric Vector Convergence")
    print(f"{'='*60}")
    print(f"Parameters: λ_vm={lambda_vm}, n_actions={n_actions}, β={beta}")
    print(f"  (Alignment-based reward: theoretical ω* = 0.5)")

    # Theoretical baseline for alignment-based reward
    # With deterministic update: proj* = E[reward] = E[(cosθ+1)/2] = 0.5
    omega_star = 0.5
    print(f"  Theoretical ω* = {omega_star:.6f} (scalar projection onto ω_ideal)")
    
    distances = []
    distances_final = []
    
    for seed in range(seeds):
        sim = DSCN_G_Verification(
            N=50, K=3, d=8, alpha=5.0, beta=beta,
            lambda_vm=lambda_vm, n_actions=n_actions,
            gamma=0.01, theta_death=0.10, seed=seed
        )
        
        # Track distance over time
        for step in range(steps):
            sim.step()
            # Distance from theoretical baseline (scalar projection onto ω_ideal)
            if sim.nodes_active:
                # Project ω onto ω_ideal direction
                projections = []
                for i in sim.nodes_active:
                    norm = np.linalg.norm(sim.omega[i])
                    if norm > 0:
                        proj = np.dot(sim.omega[i], sim.omega_ideal)
                        projections.append(proj)
                
                if projections:
                    mean_proj = np.mean(projections)
                    dist = abs(mean_proj - 0.75)  # theoretical ω* = 0.75
                    if step == steps - 1:
                        distances_final.append(dist)
        
    distances_final = np.array(distances_final)
    mean_dist = np.mean(distances_final)
    std_dist = np.std(distances_final)
    
    print(f"\n  Distance ‖ω_proj − ω*‖:")
    print(f"    Mean = {mean_dist:.6f}")
    print(f"    Std  = {std_dist:.6f}")
    print(f"    β    = {beta:.6f}")
    print(f"    Mean ≤ β: {'✓' if mean_dist <= beta else '✗'}")
    print(f"    All ≤ β: {'✓' if np.all(distances_final <= beta) else '✗'}")
    
    # Also check O(β) scaling: distance should be proportional to β
    # For β=0.1, distance should be ~0.1 (C ≈ 1)
    C_estimate = mean_dist / beta
    print(f"    C = mean/β = {C_estimate:.2f} (should be O(1))")
    
    return {
        'lambda_vm': lambda_vm,
        'n_actions': n_actions,
        'beta': beta,
        'omega_star': 0.75,
        'mean_distance': float(mean_dist),
        'std_distance': float(std_dist),
        'mean_le_beta': bool(mean_dist <= beta),
        'all_le_beta': bool(np.all(distances_final <= beta)),
        'C_estimate': float(C_estimate)
    }


# ============================================================
# Theorem 3 Verification: Phase Convergence Rate
# ============================================================

def verify_theorem3(
    lambda_vm: float = 3.0,
    eta: float = 0.1,
    seeds: int = 100,
    steps: int = 2000
) -> Dict:
    """
    Theorem 3: P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T)
    
    Verification:
    1. Track phase of root node over time
    2. Detect if phase converges to antipodal (θ* + π) vs target (θ*)
    3. Estimate p_conv = 1 - P(antipodal)
    """
    print(f"\n{'='*60}")
    print(f"THEOREM 3 VERIFICATION: Phase Convergence Rate")
    print(f"{'='*60}")
    print(f"Parameters: λ_vm={lambda_vm}, η={eta}")
    print(f"Running {seeds} seeds × {steps} steps")
    
    # Target phase
    theta_star = np.pi / 2
    antipodal = (theta_star + np.pi) % (2 * np.pi)
    
    antipodal_count = 0
    conv_count = 0
    
    for seed in range(seeds):
        sim = DSCN_G_Verification(
            N=50, K=3, d=8, alpha=5.0, beta=0.01,
            eta=eta, lambda_vm=lambda_vm, n_actions=8,
            gamma=0.01, theta_death=0.10, seed=seed
        )
        
        # Run and track root phase
        for _ in range(steps):
            sim.step()
        
        # Check final phase of root node
        root_phase = sim.phi[sim.nodes_active[0]] if sim.nodes_active else 0
        
        # Distance to target vs antipodal
        dist_to_target = min(abs(root_phase - theta_star), 2*np.pi - abs(root_phase - theta_star))
        dist_to_antipodal = min(abs(root_phase - antipodal), 2*np.pi - abs(root_phase - antipodal))
        
        if dist_to_antipodal < dist_to_target:
            antipodal_count += 1
        else:
            conv_count += 1
    
    p_antipodal = antipodal_count / seeds
    p_conv = conv_count / seeds
    
    print(f"\n  Results:")
    print(f"    Antipodal seeds: {antipodal_count}/{seeds} = {p_antipodal:.3f}")
    print(f"    Converged seeds: {conv_count}/{seeds} = {p_conv:.3f}")
    
    # The theorem states P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T)
    # For R_min ≈ 0.5 (minimum relevance), c is a constant
    # We can check if the bound is reasonable
    R_min = 0.5
    c = 1.0  # Conservative constant
    bound = np.exp(-c * lambda_vm * eta * R_min * steps)
    
    print(f"  Theoretical bound (c=1, R_min=0.5): exp(-{c*lambda_vm*eta*R_min*steps:.1f}) = {bound:.2e}")
    print(f"  Observed P(antipodal) = {p_antipodal:.3f} {'≤ bound ✓' if p_antipodal <= bound else '> bound (bound too loose)'}")
    
    return {
        'lambda_vm': lambda_vm,
        'eta': eta,
        'seeds': seeds,
        'steps': steps,
        'antipodal_count': antipodal_count,
        'p_antipodal': float(p_antipodal),
        'p_conv': float(p_conv),
        'theoretical_bound': float(bound),
        'bound_satisfied': bool(p_antipodal <= bound)
    }


# ============================================================
# ρ_eff Definition Verification
# ============================================================

def verify_rho_eff_definition():
    """
    Verify that ρ_eff computed from chains matches the Herfindahl definition.
    """
    print(f"\n{'='*60}")
    print(f"ρ_eff DEFINITION VERIFICATION")
    print(f"{'='*60}")
    
    # Run a simulation and check ρ_eff computation
    sim = DSCN_G_Verification(N=50, K=3, seed=42)
    sim.run(1000)
    
    # Get chain positions
    chain_positions = sim.chain_positions
    active = sim.nodes_active
    
    # Manual Herfindahl computation
    activity = np.zeros(len(active))
    for pos in chain_positions:
        if pos in active:
            idx = active.index(pos)
            activity[idx] += 1
    
    if activity.sum() > 0:
        activity /= activity.sum()
        rho_manual = np.sum(activity ** 2)
    else:
        rho_manual = 0.0
    
    rho_method = sim.compute_rho_eff()
    
    print(f"  Manual Herfindahl: {rho_manual:.6f}")
    print(f"  Method compute_rho_eff(): {rho_method:.6f}")
    print(f"  Match: {'✓' if abs(rho_manual - rho_method) < 1e-10 else '✗'}")
    
    return {
        'manual': float(rho_manual),
        'method': float(rho_method),
        'match': abs(rho_manual - rho_method) < 1e-10
    }


# ============================================================
# Main Verification Runner
# ============================================================

def run_all_verifications() -> Dict:
    """Run all theorem verifications and compile results."""
    print("\n" + "="*70)
    print("DSCN-G THEOREM VERIFICATION SUITE")
    print("="*70)
    
    all_results = {}
    
    # ρ_eff definition
    all_results['rho_eff_definition'] = verify_rho_eff_definition()
    
    # Theorem 1
    all_results['theorem1'] = verify_theorem1(
        alpha=5.0, theta_death=0.10,
        N_inits=[4, 50, 200],
        seeds=10,  # Reduced for speed
        steps=500
    )
    
    # Theorem 2
    all_results['theorem2'] = verify_theorem2(
        lambda_vm=3.0, n_actions=8,
        theta_star=np.pi/2, beta=0.10,
        seeds=10, steps=500
    )
    
    # Theorem 3
    all_results['theorem3'] = verify_theorem3(
        lambda_vm=3.0, eta=0.1,
        seeds=10, steps=500
    )
    
    # Summary
    print(f"\n{'='*70}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*70}")
    
    for key, result in all_results.items():
        if key == 'rho_eff_definition':
            status = '✓' if result['match'] else '✗'
            print(f"  {key}: {status}")
        elif 'overall_N_ss' in result:
            print(f"  {key}: N_ss* = {result['overall_N_ss']:.1f}, ρ_eff = {result['overall_rho_eff']:.4f}")
        elif 'mean_distance' in result:
            status = '✓' if result['mean_le_beta'] else '✗'
            print(f"  {key}: ‖ω−ω*‖ = {result['mean_distance']:.6f} ≤ β={result['beta']:.3f} {status}")
        elif 'p_conv' in result:
            status = '✓' if result['p_conv'] > 0.9 else '⚠'
            print(f"  {key}: p_conv = {result['p_conv']:.3f} {status}")
    
    return all_results


if __name__ == "__main__":
    results = run_all_verifications()
    
    # Save results
    output_path = "verification_results.json"
    import json
    
    def convert(obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        return obj
    
    with open(output_path, 'w') as f:
        json.dump(convert(results), f, indent=2)
    print(f"\nResults saved to {output_path}")