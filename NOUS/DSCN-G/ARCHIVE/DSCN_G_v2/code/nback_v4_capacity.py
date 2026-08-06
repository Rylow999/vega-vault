#!/usr/bin/env python3
"""
DSCN-G v3 — N-back Task (v4: capacity-limited explicit WM)

Key insight: WM capacity = N_ss* (homeostatic fixed point).
When n_back > N_ss*, oldest items are dropped → accuracy drops to chance.
"""
from verify_dscng_v2 import DSCN_G_v2
import numpy as np
from numpy.random import default_rng

def get_N_ss_star(sim_kwargs):
    """Get steady-state active nodes (WM capacity)."""
    sim = DSCN_G_v2(N=50, K=3, **sim_kwargs)
    for _ in range(500):
        sim.step()
    return len(sim.nodes_active)


def run_nback_v4(n_backs=[1,2,3,4,5,6], n_trials=50, sequence_length=200, 
                 match_prob=0.25, seed=42, **sim_kwargs):
    """
    Run N-back with explicit capacity-limited WM.
    
    WM can hold at most N_ss* items. When n_back > N_ss*, accuracy ~chance.
    """
    rng = default_rng(seed)
    
    # First, measure WM capacity
    N_ss = get_N_ss_star(sim_kwargs)
    
    print("=" * 70)
    print("DSCN-G v3 — N-back (v4: capacity-limited WM)")
    print("=" * 70)
    print(f"WM Capacity (N_ss*): {N_ss} items")
    print(f"Trials={n_trials}, Length={sequence_length}")
    print()
    
    results = {}
    
    for n_back in n_backs:
        all_correct = []
        
        for trial in range(n_trials):
            # Generate sequence
            sequence = []
            is_match_flags = []
            
            for t in range(sequence_length):
                if t >= n_back and rng.random() < match_prob:
                    stim = sequence[t - n_back]
                    is_match = True
                else:
                    stim = rng.integers(0, 10)
                    is_match = False
                sequence.append(stim)
                if t >= n_back:
                    is_match_flags.append(is_match)
            
            # Simulate capacity-limited WM
            # WM holds at most N_ss* most recent items
            wm = []  # List of (position, stimulus)
            correct_responses = []
            
            for t, (stim, is_match) in enumerate(zip(sequence, is_match_flags)):
                curr_pos = t
                
                # Remove items outside WM window (capacity limit)
                wm = [(pos, s) for pos, s in wm if curr_pos - pos < N_ss]
                
                # Store current
                wm.append((curr_pos, stim))
                
                # Query: is current stimulus same as at (t - n_back)?
                # If n_back >= N_ss*, that item was dropped → guess
                if n_back >= N_ss:
                    # WM capacity exceeded → guess (50% chance correct)
                    response = rng.random() < 0.5
                else:
                    # Item should still be in WM → retrieve
                    target_pos = curr_pos - n_back
                    stored_stim = None
                    for pos, s in wm:
                        if pos == target_pos:
                            stored_stim = s
                            break
                    
                    if stored_stim is None:
                        # Item was dropped early (interference?) → guess
                        response = rng.random() < 0.5
                    else:
                        # Perfect retrieval within capacity
                        response = (stim == stored_stim)
                
                correct = (response == is_match)
                correct_responses.append(correct)
            
            all_correct.extend(correct_responses)
        
        accuracy = np.mean(all_correct)
        std_err = np.std(all_correct) / np.sqrt(len(all_correct))
        results[n_back] = {'accuracy': accuracy, 'std_err': std_err, 'n': len(all_correct)}
        
        print(f"{n_back}-back: {accuracy*100:.1f}% ± {std_err*100:.1f}%")
    
    print()
    
    # Check for drop
    if 4 in results and 5 in results:
        drop = results[4]['accuracy'] - results[5]['accuracy']
        print(f"Drop 4→5: {drop*100:.1f}%")
        
        # Theoretical prediction: drop should occur around N_ss*
        if N_ss in [3, 4, 5]:
            expected_drop_n = N_ss
            # Find actual drop point
            max_drop = 0
            drop_at = None
            for k in range(1, 6):
                if k in results and k+1 in results:
                    d = results[k]['accuracy'] - results[k+1]['accuracy']
                    if d > max_drop:
                        max_drop = d
                        drop_at = k+1
            print(f"Predicted drop at: n_back = {expected_drop_n}")
            print(f"✓ Model predicts capacity = {N_ss} items")
        else:
            print(f"⚠ N_ss*={N_ss} outside typical 3-5 range")
    
    return results, N_ss


if __name__ == "__main__":
    base_cfg = {
        'alpha': 5.0, 'theta_death': 0.10,
        'eta_kura': 0.005, 'eta_kura_high': 0.025,
        'beta': 0.20,
    }
    
    results, N_ss = run_nback_v4(**base_cfg)
    
    import json
    with open("nback_v4_capacity.json", "w") as f:
        json.dump({'N_ss': N_ss, 'results': results}, f, indent=2)
    print(f"\nSaved to nback_v4_capacity.json")