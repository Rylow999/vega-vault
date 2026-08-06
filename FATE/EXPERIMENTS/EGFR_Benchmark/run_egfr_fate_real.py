#!/usr/bin/env python3
"""EGFR Benchmark — FATE v6 REAL (via pipe intermediary).

Runs:
- D=64, 128, 256 × budget=500, 3000 × 5 seeds
- FATE v6 (fate-engine real, no random search)
- Oracle: EGFR similarity-based
- Output: egfr_fate_D{dim}_budget{budget}_seed{seed}.csv
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

INTERMEDIARY = Path(__file__).parent / "pipe_intermediary.py"
OUTPUT_DIR = Path(__file__).parent

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUNS = [
    # (dim, budget, seeds)
    (64, 500, 5),
    (64, 3000, 5),
    (128, 500, 5),
    (128, 3000, 5),
    (256, 500, 5),
    (256, 3000, 5),
]

print("=" * 60)
print("EGFR Benchmark — FATE v6 REAL (pipe mode)")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Intermediary: {INTERMEDIARY}")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, budget, seeds in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, budget={budget}, seeds={seeds}")
    
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"egfr_fate_D{dim}_budget{budget}_seed{seed}.csv"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Run intermediary (which launches FATE)
        try:
            result = subprocess.run(
                [sys.executable, str(INTERMEDIARY),
                 "--dim", str(dim),
                 "--budget", str(budget),
                 "--seed", str(seed),
                 "--output", str(output_file)],
                capture_output=True,
                text=True,
                timeout=budget * 3,  # generous timeout
            )
            
            # Parse stderr for best fitness
            best_fitness = 0.0
            for line in result.stderr.split('\n'):
                if 'best=' in line:
                    try:
                        best_fitness = float(line.split('best=')[1].strip().split(',')[0])
                    except:
                        pass
            
            if result.returncode == 0:
                print(f"    ✅ COMPLETED (best={best_fitness:.4f})")
            else:
                print(f"    ERROR: Intermediary exited with {result.returncode}")
                print(f"    stderr: {result.stderr[-300:]}")
        
        except subprocess.TimeoutExpired:
            print(f"    ERROR: Timeout (>{budget*3}s)")
        except Exception as e:
            print(f"    ERROR: {e}")
    
    print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)