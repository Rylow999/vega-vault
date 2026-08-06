#!/usr/bin/env python3
"""
DSCN-G v3 — N-back Task (v3: working memory via activity trace)

Key insight: WM is maintained by ______________________ activity traces.
Each node has a trace that decays over time. Matching stimulus reactivates the trace.
"""
from verify_dscng_v2 import DSCN_G_v2
import numpy as np
from numpy.random import default_rng

class DSCN_G_v3_WM(DSCN_G_v2):
    """DSCN-G v3 with working memory traces."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Activity trace per node (exponential decay)
        self.trace = np.zeros(self.N)
        self.trace_decay = 0.95  # decay factor per step
    
    def step_with_trace(self, stimulus=None):
        """Step with optional stimulus encoding."""
        self.t += 1
        
        # Decay traces
        self.trace *= self.trace_decay
        
        # If stimulus is presented, activate corresponding nodes
        if stimulus is not None:
            # Activate nodes with high relevance to stimulus direction
            # Use stimulus ID to select a subset of nodes (hash-like)
            np.random.seed(int(stimulus * 1000 + self.t))
            active_subset = np.random.choice(self.nodes_active, 
                                             size=max(1, len(self.nodes_active)//3),
                                             replace=False)
            self.trace[active_subset] = 1.0
        
        # Run normal DSCN-G dynamics
        super().step()
        
        return self.trace.copy()


class NBackTaskV3:
    """N-back using WM traces."""
    
    def __init__(self, n_stimuli=10, seed=None):
        self.n_stimuli = n_stimuli
        self.rng = default_rng(seed)
    
    def run_trial(self, n_back, sequence_length=100, match_prob=0.3, sim_kwargs=None):
        """Run N-back trial with match/non-match balanced."""
        if sim_kwargs is None:
            sim_kwargs = {}
        
        # Generate balanced sequence
        sequence = []
        is_match_list = []
        for t in range(sequence_length):
            if t >= n_back and self.rng.random() < match_prob:
                stim = sequence[t - n_back]
                is_match = True
            else:
                stim = self.rng.integers(0, self.n_stimuli)
                is_match = False
            sequence.append(stim)
            if t >= n_back:
                is_match_list.append(is_match)
        
        # Initialize WM simulator
        sim = DSCN_G_v3_WM(N=50, K=3, **sim_kwargs)
        
        # Store trace patterns
        wm_traces = []
        results = []
        
        for t, stim in enumerate(sequence):
            trace = sim.step_with_trace(stimulus=stim)
            wm_traces.append(trace.copy())
            
            if t >= n_back:
                is_match = (stim == sequence[t - n_back])
                
                # Compare current trace with stored trace
                stored_trace = wm_traces[t - n_back]
                
                # Correlation between traces
                similarity = np.corrcoef(trace, stored_trace)[0, 1]
                if np.isnan(similarity):
                    similarity = 0.0
                
                # Decision
                threshold = 0.0
                response = (similarity > threshold)
                
                correct = (response == is_match)
                results.append((is_match, response, correct, similarity))
        
        return results


def run_nback_v3(n_backs=[1,2,3,4,5,6], n_trials=20, sequence_length=100, 
                 match_prob=0.3, seed=42, **sim_kwargs):
    """Run N-back validation."""
    task = NBackTaskV3(n_stimuli=10, seed=seed)
    results = {}
    
    print("=" * 70)
    print("DSCN-G v3 — N-back (v3: WM traces)")
    print("=" * 70)
    print()
    
    for n_back in n_backs:
        all_correct = []
        all_similarity = []
        
        for trial in range(n_trials):
            trial_results = task.run_trial(
                n_back=n_back,
                sequence_length=sequence_length,
                match_prob=match_prob,
                sim_kwargs={**sim_kwargs, 'seed': seed + trial}
            )
            
            for is_match, response, correct, sim_val in trial_results:
                all_correct.append(correct)
                all_similarity.append((is_match, sim_val))
        
        accuracy = np.mean(all_correct)
        std_err = np.std(all_correct) / np.sqrt(len(all_correct))
        results[n_back] = {'accuracy': accuracy, 'std_err': std_err, 'n': len(all_correct)}
        
        # Also compute d-prime
        hits = sum(1 for m, r, c, s in [(m,r,c,s) for (_,r,c,s) in []] if False)  # placeholder
        
        print(f"{n_back}-back: {accuracy*100:.1f}% ± {std_err*100:.1f}%")
    
    print()
    if 4 in results and 5 in results:
        drop = results[4]['accuracy'] - results[5]['accuracy']
        print(f"Drop 4→5: {drop*100:.1f}%")
    
    return results


if __name__ == "__main__":
    base_cfg = {
        'alpha': 5.0, 'theta_death': 0.10,
        'eta_kura': 0.005, 'eta_kura_high': 0.025,
    }
    
    results = run_nback_v3(**base_cfg)
    
    import json
    with open("nback_v3_traces.json", "w") as f:
        json.dump(results, f, indent=2)