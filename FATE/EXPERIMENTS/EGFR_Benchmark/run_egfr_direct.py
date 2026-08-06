#!/usr/bin/env python3
"""EGFR Benchmark — Simple mode (no pipe, direct oracle calls).

Runs:
- D=64, 128, 256 × budget=500, 3000 × 25 seeds
- Direct oracle evaluation (no pipe mode)
- Output: egfr_D{dim}_budget{budget}_seed{seed}.csv
"""
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# Import oracle directly
import sys
sys.path.insert(0, r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Drug_Discovery")
from oracle_egfr_v1 import EGFROracle

OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Benchmark")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUNS = [
    # (dim, budget, seeds)
    (64, 500, 25),
    (64, 3000, 25),
    (128, 500, 25),
    (128, 3000, 25),
    (256, 500, 25),
    (256, 3000, 25),
]

print("=" * 60)
print("EGFR Drug Discovery Benchmark — Direct Oracle Mode")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Oracle: EGFROracle (oracle_egfr_v1.py)")
print(f"Output: {OUTPUT_DIR}")
print()

# Load oracle once
print("[Loading oracle...]")
oracle = EGFROracle()
print(f"[✓] Oracle loaded: {len(oracle.compounds)} compounds")
print()

for dim, budget, seeds in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, budget={budget}, seeds={seeds}")
    
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"egfr_D{dim}_budget{budget}_seed{seed}.csv"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Initialize RNG
        rng = np.random.default_rng(seed)
        
        # Run FATE-like optimization (simple random search for now)
        results = []
        best_fitness = 0.0
        best_info = None
        
        for eval_num in range(budget):
            # Generate random phase vector
            phase = rng.uniform(0, 2 * np.pi, dim)
            
            # Evaluate
            fitness, info = oracle.evaluate(phase)
            results.append((fitness, info))
            
            if fitness > best_fitness:
                best_fitness = fitness
                best_info = info
            
            # Progress log every 100 evals
            if (eval_num + 1) % 100 == 0:
                print(f"    Eval {eval_num+1}/{budget}, best={best_fitness:.4f}")
        
        # Save results
        with open(output_file, "w") as f:
            f.write("eval,fitness,similarity,pIC50,IC50_nM,nearest_smiles\n")
            for idx, (fit, info) in enumerate(results):
                smiles = info.get("nearest_smiles", "")[:50]  # truncate
                f.write(f"{idx+1},{fit:.6f},{info.get('similarity',0):.4f},{info.get('pIC50',0):.2f},{info.get('IC50_nM',0):.1f},{smiles}\n")
        
        print(f"    ✅ COMPLETED (best={best_fitness:.4f})")
    
    print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)