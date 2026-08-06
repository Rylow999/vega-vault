#!/usr/bin/env python3
"""EGFR Benchmark — FATE v6 via pipe mode.

Runs:
- D=64, 128, 256 × budget=500, 3000 × 25 seeds
- FATE v6 (fate-engine) vs CMA-ES vs TPE
- Oracle: similarity-based (oracle_egfr_v1.py)
- Output: egfr_{sampler}_D{dim}_budget{budget}_seed{seed}.csv
"""
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime

BIN = Path(r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5.exe")
ORACLE = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Drug_Discovery\oracle_egfr_v1.py")
OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Benchmark")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Samplers: fate, cma-es, tpe
SAMPLERS = ["fate", "cma-es", "tpe"]

RUNS = [
    # (dim, budget, seeds)
    (64, 500, 5),   # Reduced seeds for speed
    (128, 500, 5),
    (256, 500, 5),
]

print("=" * 60)
print("EGFR Drug Discovery Benchmark — FATE v6 vs Baselines")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Bin: {BIN}")
print(f"Oracle: {ORACLE}")
print(f"Samplers: {SAMPLERS}")
print(f"Output: {OUTPUT_DIR}")
print()

for dim, budget, seeds in RUNS:
    for sampler in SAMPLERS:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: {sampler}, D={dim}, budget={budget}, seeds={seeds}")
        
        for i in range(seeds):
            seed = 42 + i
            output_file = OUTPUT_DIR / f"egfr_{sampler}_D{dim}_budget{budget}_seed{seed}.csv"
            print(f"  [{i+1}/{seeds}] Seed {seed}...")
            
            # Command: main_v5 --oracle pipe --dim D --budget B --seed S --samplers <sampler> | oracle
            cmd = [
                str(BIN),
                "--oracle", "pipe",
                "--dim", str(dim),
                "--budget", str(budget),
                "--seed", str(seed),
                "--samplers", sampler,
            ]
            
            env = os.environ.copy()
            env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
            
            try:
                # Start FATE process
                fate_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                    bufsize=1,  # Line buffered
                )
                
                # Start oracle process
                oracle_proc = subprocess.Popen(
                    [sys.executable, str(ORACLE)],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                )
                
                # Pipe FATE stdout -> oracle stdin line by line
                results = []
                fate_stderr = []
                
                # Read FATE stderr in a thread
                import threading
                def read_stderr():
                    for line in fate_proc.stderr:
                        fate_stderr.append(line)
                
                stderr_thread = threading.Thread(target=read_stderr)
                stderr_thread.start()
                
                # Send phases to oracle, collect fitness
                for line in fate_proc.stdout:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        # Send to oracle
                        oracle_proc.stdin.write(line + "\n")
                        oracle_proc.stdin.flush()
                        
                        # Read fitness from oracle
                        oracle_output = oracle_proc.stdout.readline()
                        if oracle_output:
                            result = json.loads(oracle_output)
                            fitness = result.get("fit", 0.0)
                            results.append(fitness)
                            
                            # Send fitness back to FATE
                            fate_proc.stdin.write(f"{fitness}\n")
                            fate_proc.stdin.flush()
                    except (json.JSONDecodeError, BrokenPipeError) as e:
                        print(f"    ERROR: {e}")
                        break
                
                # Close oracle stdin and wait
                oracle_proc.stdin.close()
                oracle_proc.wait()
                fate_proc.wait()
                stderr_thread.join()
                
                if fate_proc.returncode != 0:
                    print(f"    ERROR: FATE exited with {fate_proc.returncode}")
                    print(f"    stderr: {''.join(fate_stderr[-5:])}")
                elif oracle_proc.returncode != 0:
                    print(f"    ERROR: Oracle exited with {oracle_proc.returncode}")
                else:
                    # Save results
                    best_fitness = max(results) if results else 0.0
                    with open(output_file, "w") as f:
                        f.write("eval,fitness\n")
                        for idx, fit in enumerate(results):
                            f.write(f"{idx+1},{fit:.6f}\n")
                    
                    print(f"    ✅ COMPLETED (best={best_fitness:.4f}, evals={len(results)})")
            
            except Exception as e:
                print(f"    ERROR: {e}")
        
        print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)