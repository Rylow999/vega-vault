#!/usr/bin/env python3
"""Aspirina GPU Benchmark — Direct oracle mode (no pipe).

Runs:
- D=8, 16 × 25 seeds, budget=2000
- Oracle: BRICS + DSCN-G coherence (single-thread)
- Output: aspirina_direct_D{dim}_seed{seed}.csv
"""
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Import oracle directly
import sys
sys.path.insert(0, r"C:\Users\lucas\repos\fate-v5-modular\bench\oracles\smiles")
from oracle_smiles_dscng_wrapper import evaluate as smiles_evaluate

OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\Aspirina_GPU")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUNS = [
    (8, 25, 2000, "D8"),
    (16, 25, 2000, "D16"),
]

print("=" * 60)
print("Aspirina GPU Benchmark — Direct Oracle Mode")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Oracle: BRICS + DSCN-G (oracle_smiles_dscng_wrapper.py)")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, seeds, budget, suffix in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, seeds={seeds}, budget={budget}")
    
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"aspirina_direct_{suffix}_seed{seed}.csv"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Initialize RNG
        rng = np.random.default_rng(seed)
        
        # Run optimization (random search for now)
        results = []
        best_fitness = 0.0
        best_detail = None
        
        for eval_num in range(budget):
            # Generate random phase vector
            phase = rng.uniform(0, 2 * np.pi, dim).tolist()
            
            # Evaluate (wrapper returns fit, chem, dyn)
            try:
                fit, chem, dyn = smiles_evaluate(phase)
            except Exception as e:
                fit = 0.0
                chem = 0.0
                dyn = 0.0
            
            results.append((fit, chem, dyn))
            
            if fit > best_fitness:
                best_fitness = fit
                best_detail = (chem, dyn)
            
            # Progress log every 100 evals
            if (eval_num + 1) % 100 == 0:
                print(f"    Eval {eval_num+1}/{budget}, best={best_fitness:.4f}, chem={best_detail[0] if best_detail else 0:.3f}, dyn={best_detail[1] if best_detail else 0:.3f}")
        
        # Save results
        with open(output_file, "w") as f:
            f.write("eval,fitness,chem,dyn\n")
            for idx, (fit, chem, dyn) in enumerate(results):
                f.write(f"{idx+1},{fit:.6f},{chem:.6f},{dyn:.6f}\n")
        
        print(f"    ✅ COMPLETED (best={best_fitness:.4f})")
    
    print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)