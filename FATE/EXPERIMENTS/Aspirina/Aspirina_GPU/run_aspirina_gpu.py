#!/usr/bin/env python3
"""4 Aspirina Runs GPU — FATE v6 + BRICS + DSCN-G (Pitcairn)

Runs:
- D=8 × balanced (25 seeds, budget=2000)
- D=8 × chem_first (25 seeds, budget=2000)
- D=16 × balanced (25 seeds, budget=2000)
- D=16 × chem_first (25 seeds, budget=2000)

Oracle: bench/oracles/smiles/oracle_smiles_dscng.py (GPU, batch mode)
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

BIN = Path(r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5_pipe.exe")
ORACLE = Path(r"C:\Users\lucas\repos\fate-v5-modular\bench\oracles\smiles\oracle_smiles_dscng_wrapper.py")  # wrapper: single-thread, no MP issues
OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\Aspirina_GPU")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

RUNS = [
    # (dim, seeds, budget, suffix)
    (8, 25, 2000, "D8"),
    (16, 25, 2000, "D16"),
]

print("=" * 60)
print("Aspirina GPU — 4 Runs (FATE v6 + BRICS + DSCN-G)")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Bin: {BIN}")
print(f"Oracle: {ORACLE}")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, seeds, budget, suffix in RUNS:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: D={dim}, seeds={seeds}, budget={budget}")
    print(f"  Output: {OUTPUT_DIR}")
    
    # Run 'seeds' times with different seeds (pipe mode doesn't have --seeds flag)
    for i in range(seeds):
        seed = 42 + i
        output_file = OUTPUT_DIR / f"aspirina_{suffix}_seed{seed}.jsonl"
        print(f"  [{i+1}/{seeds}] Seed {seed}...")
        
        # Command: main_v5_pipe --dim D --budget B --seed S --batch | oracle > output
        cmd = [
            str(BIN),
            "--dim", str(dim),
            "--budget", str(budget),
            "--seed", str(seed),
            "--batch",
        ]
        
        oracle_cmd = [sys.executable, str(ORACLE)]
        
        # Run piped
        try:
            # Set MSYS2 PATH for DLLs
            env = os.environ.copy()
            env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
            
            with open(output_file, "w") as f:
                # Start pipe process
                pipe_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                )
                
                # Start oracle process
                oracle_proc = subprocess.Popen(
                    oracle_cmd,
                    stdin=pipe_proc.stdout,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                
                # Close pipe_proc stdout so it can finish
                pipe_proc.stdout.close()
                
                # Wait for both
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