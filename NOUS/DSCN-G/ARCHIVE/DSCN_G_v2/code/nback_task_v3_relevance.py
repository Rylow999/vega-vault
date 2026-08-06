#!/usr/bin/env python3
"""
DSCN-G v3 — N-back Task (v2: relevance-based matching)

Key insight: WM recognition is based on ______________________.
When a stimulus repeats, the relevance pattern across nodes should match.
"""
from verify_dscng_v2 import DSCN_G_v2
import numpy as np
from numpy.random import default_rng

class NBackTaskV2:
    """N-back using relevance patterns (R_i = 1/(1+||ω_i - ω_ideal||))."""
    
    def __init__(self, n_stimuli=10, d=8, seed=None):
        self.n_stimuli = n_stimuli
        self.d = d
        self.rng = default_rng(seed)
        
        #Each stimulus maps to a target ω pattern (different direction in R^d)
        self.stim_targets = self._generate_orthogonal_targets()
    
    def _generate_orthogonal_targets(self):
        """Generate ~orthogonal target vectors for each stimulus."""
        targets = []
        for s in range(self.n_stimuli):
            # Random direction, normalized
            v = self.rng.normal(size=self.d)
            v /= np.linalg.norm(v)
            targets.append(v)
        return targets
    
    def run_trial(self, n_back, sequence_length=100, match_prob=0.2, sim_kwargs=None):
        """
        Run single N-back trial with mixture of match/non-match trials.
        """
        if sim_kwargs is None:
            sim_kwargs = {}
        
        # Generate sequence with controlled matches
        sequence = []
        is_match_list = []
        for t in range(sequence_length):
            if t >= n_back and self.rng.random() < match_prob:
                # Force match
                stim = sequence[t - n_back]
                is_match = True
            else:
                stim = self.rng.integers(0, self.n_stimuli)
                is_match = False
            sequence.append(stim)
            is_match_list.append(is_match if t >= n_back else None)
        
        sequence = np.array(sequence)
        
        # Initialize simulator
        sim = DSCN_G_v2(N=50, K=3, **sim_kwargs)
        
        # WM storage: list of relevance patterns at encoding
        wm = []
        results = []
        
        for t, stim in enumerate(sequence):
            # Encode stimulus: temporarily bias ω_ideal toward target
            # This is a "soft" encoding - doesn't change learning, just phase dynamics
            original_omega_ideal = sim.omega_ideal.copy()
            target = self.stim_targets[stim]
            
            # Blend current ω_ideal with stimulus target (attention mechanism)
            sim.omega_ideal = 0.7 * original_omega_ideal + 0.3 * target
            sim.omega_ideal /= np.linalg.norm(sim.omega_ideal)
            
            # Run dynamics
            sim.step()
            
            # Record relevance pattern: R_i for active nodes
            relevance_pattern = np.array([sim._relevance(i) for i in sim.nodes_active])
            wm.append((stim, relevance_pattern.copy()))
            
            # Restore original ω_ideal
            sim.omega_ideal = original_omega_ideal
            
            # Query at t >= n_back
            if t >= n_back:
                is_match = (stim == sequence[t - n_back])
                _, stored_pattern = wm[t - n_back]
                
                # Compare relevance patterns
                similarity = np.corrcoef(relevance_pattern, stored_pattern)[0, 1]
                if np.isnan(similarity):
                    similarity = 0.0
                
                # Decision
                threshold = 0.1  # Tuned
                response = (similarity > threshold)
                
                correct = (response == is_match)
                results.append((is_match, response, correct, similarity))
        
        return results


def run_nback_validation_v2(n_backs=[1, 2, 3, 4, 5, 6], n_trials=20, 
                            sequence_length=100, match_prob=0.2, seed=42, **sim_kwargs):
    """Run N-back validation across loads."""
    task = NBackTaskV2(n_stimuli=10, d=8, seed=seed)
    results = {}
    
    print("=" * 70)
    print("DSCN-G v3 — N-back Validation (v2: relevance matching)")
    print("=" * 70)
    print(f"Config: {sim_kwargs}")
    print(f"Trials={n_trials}, Length={sequence_length}, MatchProb={match_prob}")
    print()
    
    for n_back in n_backs:
        all_correct = []
        
        for trial in range(n_trials):
            trial_results = task.run_trial(
                n_back=n_back,
                sequence_length=sequence_length,
                match_prob=match_prob,
                sim_kwargs={**sim_kwargs, 'seed': seed + trial}
            )
            
            for is_match, response, correct, similarity in trial_results:
                all_correct.append(correct)
        
        accuracy = np.mean(all_correct)
        std_err = np.std(all_correct) / np.sqrt(len(all_correct))
        results[n_back] = {'accuracy': accuracy, 'std_err': std_err, 'n_samples': len(all_correct)}
        
        print(f"{n_back}-back: {accuracy*100:.1f}% ± {std_err*100:.1f}% (n={len(all_correct)})")
    
    print()
    if 4 in results and 5 in results:
        drop = results[4]['accuracy'] - results[5]['accuracy']
        print(f"Drop 4→5: {drop*100:.1f}%")
        if results[4]['accuracy'] > 0.6 and drop > 0.1:
            print("✓ Capacity limit near 4 items")
        else:
            print("⚠ No clear capacity limit")
    
    return results


if __name__ == "__main__":
    base_cfg = {
        'alpha': 5.0, 'theta_death': 0.10, 'beta': 0.20,
        'eta_kura': 0.005, 'eta_kura_high': 0.025, 'hijack_steps': 20,
    }
    
    results = run_nback_validation_v2(**base_cfg)
    
    import json
    with open("nback_results_v3_relevance.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to nback_results_v3_relevance.json")