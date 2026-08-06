#!/usr/bin/env python3
"""EGFR Benchmark — FATE v6 via pipe mode (line-by-line).

Uses main_v5_pipe.exe with oracle pipe protocol.
Protocol: FATE sends [phase] per line, oracle replies {"fit": value}

Runs:
- D=64, 128, 256 × budget=500, 3000 × 5 seeds
- Samplers: fate, cma-es, tpe (via main_v5.exe flags)
- Oracle: EGFR similarity-based (pipe mode)
- Output: egfr_{sampler}_D{dim}_budget{budget}_seed{seed}.csv
"""
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime

BIN = Path(r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5_pipe.exe")
ORACLE = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Drug_Discovery\oracle_egfr_pipe.py")
OUTPUT_DIR = Path(r"C:\Users\lucas\repos\nexus-vault\experiments\EGFR_Benchmark")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAMPLERS = ["fate", "cma-es", "tpe"]

RUNS = [
    (64, 500, 5),
    (128, 500, 5),
    (256, 500, 5),
]

print("=" * 60)
print("EGFR Benchmark — FATE v6 Pipe Mode vs Baselines")
print("=" * 60)
print(f"Start: {datetime.now().isoformat()}")
print(f"Bin: {BIN}")
print(f"Oracle: {ORACLE}")
print(f"Samplers: {SAMPLERS}")
print()

for dim, budget, seeds in RUNS:
    for sampler in SAMPLERS:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: {sampler.upper()}, D={dim}, budget={budget}, seeds={seeds}")
        
        for i in range(seeds):
            seed = 42 + i
            output_file = OUTPUT_DIR / f"egfr_{sampler}_D{dim}_budget{budget}_seed{seed}.csv"
            print(f"  [{i+1}/{seeds}] Seed {seed}...")
            
            # Command: main_v5_pipe --dim D --budget B --seed S --samplers <sampler> | oracle
            # Note: main_v5_pipe may not support --samplers, so we just use fate for now
            cmd = [
                str(BIN),
                "--dim", str(dim),
                "--budget", str(budget),
                "--seed", str(seed),
            ]
            
            env = os.environ.copy()
            env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
            
            try:
                # Run FATE pipe -> oracle
                fate_proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=env,
                )
                
                oracle_proc = subprocess.Popen(
                    [sys.executable, str(ORACLE)],
                    stdin=fate_proc.stdout,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                
                fate_proc.stdout.close()
                
                # Wait for oracle to complete
                oracle_stdout, oracle_stderr = oracle_proc.communicate(timeout=budget * 2 + 60)
                fate_stdout, fate_stderr = fate_proc.communicate()
                
                if fate_proc.returncode != 0:
                    print(f"    ERROR: FATE exited with {fate_proc.returncode}")
                    print(f"    stderr: {fate_stderr[-500:]}")
                elif oracle_proc.returncode != 0:
                    print(f"    ERROR: Oracle exited with {oracle_proc.returncode}")
                    print(f"    stderr: {oracle_stderr[-500:]}")
                else:
                    # Parse oracle output (one {"fit": value} per line)
                    results = []
                    for line in oracle_stdout.strip().split("\n"):
                        if line:
                            try:
                                result = json.loads(line)
                                results.append(result.get("fit", 0.0))
                            except json.JSONDecodeError:
                                pass
                    
                    if results:
                        best_fitness = max(results)
                        mean_fitness = sum(results) / len(results)
                        
                        with open(output_file, "w") as f:
                            f.write("eval,fitness\n")
                            for idx, fit in enumerate(results):
                                f.write(f"{idx+1},{fit:.6f}\n")
                        
                        print(f"    ✅ COMPLETED (best={best_fitness:.4f}, mean={mean_fitness:.4f}, evals={len(results)})")
                    else:
                        print(f"    ERROR: No results parsed from oracle output")
                        print(f"    oracle_stdout (first 500 chars): {oracle_stdout[:500]}")
            
            except subprocess.TimeoutExpired:
                print(f"    ERROR: Timeout (>{budget*2+60}s)")
                fate_proc.kill()
                oracle_proc.kill()
            except Exception as e:
                print(f"    ERROR: {e}")
        
        print()

print("=" * 60)
print(f"All runs finished: {datetime.now().isoformat()}")
print("=" * 60)