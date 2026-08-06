#!/usr/bin/env python3
"""EGFR Drug Discovery Benchmark — FATE v6 + similarity-based oracle.

Runs:
- D=64, 128, 256 × budget=500, 3000 × 25 seeds
- Oracle: EGFR similarity-based (oracle_egfr_v1.py)
- Output: egfr_D{dim}_budget{budget}_seed{seed}.jsonl

Protocolo: FATE vs CMA-ES vs TPE en pIC50 predicho (ChEMBL IC50 data).
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

ORACLE = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Drug_Discovery\oracle_egfr_v1.py")
BIN = Path(r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5_pipe.exe")
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
print("EGFR Drug Discovery Benchmark — FATE v6")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Oracle: {ORACLE}")
print(f"Bin: {BIN}")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, budget, seeds in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, budget={budget}, seeds={seeds}")
    
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"egfr_D{dim}_budget{budget}_seed{seed}.jsonl"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Command: main_v5_pipe --dim D --budget B --seed S --batch | oracle > output
        cmd = [
            str(BIN),
            "--dim", str(dim),
            "--budget", str(budget),
            "--seed", str(seed),
            "--batch",
        ]
        
        env = os.environ.copy()
        env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
        
        try:
            with open(output_file, "w") as f:
                pipe_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                )
                
                oracle_proc = subprocess.Popen(
                    [sys.executable, str(ORACLE)],
                    stdin=pipe_proc.stdout,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                
                pipe_proc.stdout.close()
                pipe_stdout, pipe_stderr = pipe_proc.communicate()
                oracle_stdout, oracle_stderr = oracle_proc.communicate()
                
                if pipe_proc.returncode != 0:
                    print(f"    ERROR: pipe exited with {pipe_proc.returncode}")
                    print(f"    stderr: {pipe_stderr[:500]}")
                elif oracle_proc.returncode != 0:
                    print(f"    ERROR: oracle exited with {oracle_proc.returncode}")
                    print(f"    stderr: {oracle_stderr[:500]}")
                else:
                    print(f"    ✅ COMPLETED")
        
        except Exception as e:
            print(f"    ERROR: {e}")
    
    print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)