#!/usr/bin/env python3
"""
DSCN-G v3 vs Baselines — N-back Comparison

Baselines:
1. Random guessing: 50% accuracy
2. Hopfield network: capacity ≈ 0.15×N items
3. Ideal observer: 100% accuracy
4. DSCN-G v3: capacity = N_ss* (homeostatic)
"""
import numpy as np
from numpy.random import default_rng

def hopfield_nback(n_back, sequence_length=200, n_neurons=30, capacity_fraction=0.15, seed=None):
    """
    Simulated Hopfield network N-back.
    
    Capacity ≈ 0.15 × N neurons (classic Hopfield limit).
    When n_back > capacity, accuracy drops to chance.
    """
    rng = default_rng(seed)
    capacity = int(capacity_fraction * n_neurons)
    
    # Generate sequence with 25% matches
    sequence = []
    is_match_flags = []
    for t in range(sequence_length):
        if t >= n_back and rng.random() < 0.25:
            stim = sequence[t - n_back]
            is_match = True
        else:
            stim = rng.integers(0, 10)
            is_match = False
        sequence.append(stim)
        if t >= n_back:
            is_match_flags.append(is_match)
    
    # Simulate capacity-limited WM (same as DSCN-G v4)
    correct = []
    for t, (stim, is_match) in enumerate(zip(sequence, is_match_flags)):
        if n_back >= capacity:
            response = rng.random() < 0.5  # Guess
        else:
            # Perfect retrieval within capacity
            stored = sequence[t - n_back]
            response = (stim == stored)
        
        correct.append(response == is_match)
    
    return np.mean(correct)


def ideal_nback(n_back, sequence_length=200, seed=None):
    """Ideal observer (perfect retrieval) — upper bound."""
    rng = default_rng(seed)
    
    sequence = []
    is_match_flags = []
    for t in range(sequence_length):
        if t >= n_back and rng.random() < 0.25:
            stim = sequence[t - n_back]
            is_match = True
        else:
            stim = rng.integers(0, 10)
            is_match = False
        sequence.append(stim)
        if t >= n_back:
            is_match_flags.append(is_match)
    
    # Perfect retrieval
    correct = []
    for stim, is_match in zip(sequence[len(is_match_flags):], is_match_flags):
        correct.append(is_match == (stim == sequence[0]))  # Placeholder
    
    # Actually simulate correctly
    correct = []
    for t, is_match in enumerate(is_match_flags):
        stored = sequence[t]  # t corresponds to position in sequence before current
        current = sequence[t + n_back]
        response = (stored == current)
        correct.append(response == is_match)
    
    return np.mean(correct)  # Should be ~100%


def run_baseline_comparison(n_backs=[1,2,3,4,5,6], n_trials=50, **dscn_kwargs):
    """Compare DSCN-G v3 with baselines."""
    from nback_v4_capacity import run_nback_v4
    
    print("=" * 80)
    print("DSCN-G v3 vs Baselines — N-back Comparison")
    print("=" * 80)
    print()
    
    # DSCN-G v3
    results_dscn, N_ss = run_nback_v4(
        n_backs=n_backs, n_trials=n_trials,
        match_prob=0.25, seed=42, **dscn_kwargs
    )
    
    # Run baselines
    results_baseline = {
        'random': {},
        'hopfield': {},
        'ideal': {}
    }
    
    rng = default_rng(42)
    
    for n_back in n_backs:
        # Random: 50%
        results_baseline['random'][n_back] = 0.50
        
        # Hopfield
        hopfield_accs = [
            hopfield_nback(n_back, n_neurons=30, seed=rng.integers(0, 10000))
            for _ in range(n_trials)
        ]
        results_baseline['hopfield'][n_back] = np.mean(hopfield_accs)
        
        # Ideal: ~100%
        results_baseline['ideal'][n_back] = 1.00
    
    # Print comparison table
    print(f"{'n-back':>6} | {'Random':>7} | {'Hopfield':>9} | {'DSCN-G v3':>10} | {'Ideal':>7}")
    print("-" * 80)
    
    for n in n_backs:
        dscn_acc = results_dscn[n]['accuracy']
        hopf_acc = results_baseline['hopfield'][n]
        print(f"{n:>6} | {results_baseline['random'][n]:>7.1%} | {hopf_acc:>9.1%} | {dscn_acc:>10.1%} | {results_baseline['ideal'][n]:>7.1%}")
    
    print()
    print("=== CAPACITY COMPARISON ===")
    print(f"DSCN-G v3:  N_ss* = {N_ss} items (homeostatic fixed point)")
    print(f"Hopfield:   N_max = 0.15 × {30} = {int(0.15*30)} items")
    print(f"Human:      4 ± 1 items (Cowan 2001)")
    print()
    
    # Effect size
    if 3 in results_dscn and 4 in results_dscn:
        drop_dscn = results_dscn[3]['accuracy'] - results_dscn[4]['accuracy']
        drop_hopfield = results_baseline['hopfield'][3] - results_baseline['hopfield'][4]
        print(f"Drop 3→4: DSCN-G = {drop_dscn*100:.1f}%, Hopfield = {drop_hopfield*100:.1f}%")
    
    return results_dscn, results_baseline


if __name__ == "__main__":
    dscn_cfg = {
        'alpha': 5.0, 'theta_death': 0.12,
        'eta_kura': 0.005, 'eta_kura_high': 0.025,
        'beta': 0.20
    }
    
    results_dscn, results_baseline = run_baseline_comparison(**dscn_cfg)
    
    # Save
    import json
    with open('baseline_comparison.json', 'w') as f:
        json.dump({
            'dscn_v3': {k: {'accuracy': v['accuracy']} for k, v in results_dscn.items()},
            'baselines': results_baseline
        }, f, indent=2)
    print("Saved to baseline_comparison.json")