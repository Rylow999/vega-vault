#!/usr/bin/env python3
"""Aspirina Runs — FATE v6 + ChEMBL Oracle (simple, sin BRICS/GPU)

Runs:
- D=8 (25 seeds, budget=2000)
- D=16 (25 seeds, budget=2000)

Oracle: ChEMBL neighbors (compilado en main_v5, sin dependencias externas)
Output: aspirina_chembl_D{dim}_seed{seed}.jsonl
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

BIN = Path(r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5.exe")
OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\Aspirina_GPU")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUNS = [
    # (dim, seeds, budget, suffix)
    (8, 25, 2000, "D8"),
    (16, 25, 2000, "D16"),
]

print("=" * 60)
print("Aspirina ChEMBL — FATE v6 (25 seeds c/ dim)")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Bin: {BIN}")
print(f"Oracle: chembl (compile-time, sin dependencias)")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, seeds, budget, suffix in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, seeds={seeds}, budget={budget}")
    
    # Run 'seeds' times with different seeds
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"aspirina_chembl_{suffix}_seed{seed}.jsonl"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Command: main_v5 --oracle chembl --dim D --budget B --seed S --samplers fate
        cmd = [
            str(BIN),
            "--oracle", "chembl",
            "--dim", str(dim),
            "--budget", str(budget),
            "--seed", str(seed),
            "--samplers", "fate",
        ]
        
        # Set MSYS2 PATH for DLLs
        env = os.environ.copy()
        env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
        
        try:
            with open(output_file, "w") as f:
                # Change to bench directory so chembl_fps.bin is found
                result = subprocess.run(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                    timeout=600,
                    cwd=r"C:\Users\lucas\repos\fate-v5-modular\bench",
                )
            
            if result.returncode != 0:
                print(f"    ERROR: exited with {result.returncode}")
                print(f"    stderr: {result.stderr[:500]}")
            else:
                print(f"    ✅ COMPLETED")
        
        except subprocess.TimeoutExpired:
            print(f"    ⏱ TIMEOUT (>10 min)")
        except Exception as e:
            print(f"    ERROR: {e}")
    
    print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)