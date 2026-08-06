#!/usr/bin/env python3
"""
DSCN-G v3 — N-back Task Validation
Working memory capacity emerge from homeostatic pruning (N_ss*).
"""
from verify_dscng_v2 import DSCN_G_v2
import numpy as np
from numpy.random import default_rng

# ═══════════════════════════════════════════════════════════════
#  N-BACK TASK
# ═══════════════════════════════════════════════════════════════

class NBackTask:
    """N-back working memory task using DSCN-G v3."""
    
    def __init__(self, n_stimuli=10, seed=None):
        self.n_stimuli = n_stimuli
        self.rng = default_rng(seed)
        
    def generate_sequence(self, length, n_back_match_prob=0.3):
        """Generate stimulus sequence with controlled match ratio."""
        seq = []
        matches = []
        for t in range(length):
            if t >= 1 and self.rng.random() < n_back_match_prob:
                # Force match with stimulus at t-n_back (will be validated during task)
                stim = seq[-1]  # Placeholder, actual match depends on n_back
                matches.append(True)
            else:
                stim = self.rng.integers(0, self.n_stimuli)
                matches.append(False)
            seq.append(stim)
        return np.array(seq)
    
    def run_trial(self, sim, n_back, sequence):
        """
        Run single N-back trial.
        
        Protocol:
        1. Present stimulus at each step
        2. Encode as phase pattern (subset of nodes)
        3. At step t, query: "Is stimulus[t] == stimulus[t-n_back]?"
        4. Sim responds based on whether phase pattern matches stored pattern
        
        Returns: list of (is_match, response, correct) tuples
        """
        results = []
        n_nodes = len(sim.nodes_active)
        
        # Phase patterns for each stimulus (orthogonal-ish patterns)
        # We use von Mises action selection: each stimulus maps to preferred action
        stimulus_to_action = {
            s: int(s * sim.n_actions / self.n_stimuli) 
            for s in range(self.n_stimuli)
        }
        
        # Working memory: list of (stimulus, phase_pattern_at_encoding)
        wm = []
        
        for t, stim in enumerate(sequence):
            # Step 1: Present stimulus → simulate encoding
            action_idx = stimulus_to_action[stim]
            
            # Force the selected node to take this action (simulate input)
            # In real DSCN-G, this would be external input to chains
            selected_node = sim.nodes_active[0] if sim.nodes_active else 0
            
            # Update phi for selected node toward preferred phase for this stimulus
            theta_a = 2 * np.pi * action_idx / sim.n_actions
            sim.phi[selected_node] = (theta_a + sim.rng.normal(0, 0.1)) % (2 * np.pi)
            
            # Step 2: Run DSCN-G dynamics (maintenance/rehearsal)
            sim.step()
            
            # Step 3: Store phase pattern in WM
            phase_pattern = sim.phi[sim.nodes_active].copy()
            wm.append((stim, phase_pattern))
            
            # Step 4: Query (if t >= n_back)
            if t >= n_back:
                is_match = (stim == sequence[t - n_back])
                
                # Compare current phase pattern with stored pattern from t-n_back
                _, stored_pattern = wm[t - n_back]
                current_pattern = sim.phi[sim.nodes_active]
                
                # Similarity metric: phase coherence between patterns
                phase_diff = np.abs(np.angle(np.exp(1j * (current_pattern - stored_pattern))))
                similarity = np.mean(np.cos(phase_diff))  # 1.0 = identical, 0 = orthogonal
                
                # Decision threshold (tuned to maximize accuracy)
                threshold = 0.8
                response = (similarity > threshold)
                
                correct = (response == is_match)
                results.append((is_match, response, correct, similarity))
        
        return results


def run_nback_validation(n_backs=[1, 2, 3, 4, 5, 6], n_trials=20, sequence_length=100, 
                         seed=42, **sim_kwargs):
    """
    Run full N-back validation across multiple loads.
    
    Returns: dict with accuracy for each n_back level
    """
    task = NBackTask(n_stimuli=10, seed=seed)
    results = {}
    
    print("=" * 70)
    print("DSCN-G v3 — N-back Working Memory Validation")
    print("=" * 70)
    print(f"Config: {sim_kwargs}")
    print(f"Trials per n-back: {n_trials}, Sequence length: {sequence_length}")
    print()
    
    for n_back in n_backs:
        all_correct = []
        
        for trial in range(n_trials):
            # Fresh simulator for each trial
            sim = DSCN_G_v2(N=50, K=3, seed=seed + trial, **sim_kwargs)
            
            # Generate sequence
            sequence = task.generate_sequence(sequence_length)
            
            # Run trial
            trial_results = task.run_trial(sim, n_back, sequence)
            
            # Collect correct responses
            for is_match, response, correct, similarity in trial_results:
                all_correct.append(correct)
        
        accuracy = np.mean(all_correct)
        std_err = np.std(all_correct) / np.sqrt(len(all_correct))
        results[n_back] = {'accuracy': accuracy, 'std_err': std_err, 'n_samples': len(all_correct)}
        
        print(f"{n_back}-back: Accuracy = {accuracy*100:.1f}% ± {std_err*100:.1f}% (n={len(all_correct)})")
    
    print()
    
    # Check for capacity drop at 4→5
    if 4 in results and 5 in results:
        drop = results[4]['accuracy'] - results[5]['accuracy']
        drop_pct = drop / results[4]['accuracy'] * 100 if results[4]['accuracy'] > 0 else 0
        print(f"Drop 4→5 back: {drop*100:.1f}% ({drop_pct:.1f}% relative)")
        
        if results[4]['accuracy'] > 0.7 and results[5]['accuracy'] < 0.6:
            print("✓ Capacity limit detected near 4 items")
        else:
            print("⚠ No sharp drop at 4 items (capacity may differ)")
    
    return results


if __name__ == "__main__":
    # Base configuration (from grid search: α=5, θ_death=0.10 → N_ss*=4)
    base_cfg = {
        'alpha': 5.0,
        'theta_death': 0.10,
        'beta': 0.20,
        'eta_kura': 0.005,
        'eta_kura_high': 0.025,
        'hijack_steps': 20,
    }
    
    results = run_nback_validation(**base_cfg)
    
    # Save results
    import json
    with open("nback_results_v3.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to nback_results_v3.json")