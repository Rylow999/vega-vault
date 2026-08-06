#!/usr/bin/env python3
"""Pipe intermediary: connects main_v5_pipe.exe to EGFR oracle.

Protocol:
  FATE stdout -> {"req":[p1,p2,...,pD]}
  Intermediary evaluates with oracle
  Intermediary stdin to FATE -> {"fit":score}

Usage:
  python pipe_intermediary.py | main_v5_pipe --dim 8 --budget 100 --seed 42
  
O más simple (el intermediario lanza FATE):
  python pipe_intermediary.py --dim 8 --budget 100 --seed 42
"""
import subprocess
import sys
import json
import numpy as np
from pathlib import Path
import argparse

# Silence RDKit warnings
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

# Import oracle
EGFR_DIR = Path(__file__).parent.parent / "EGFR_Drug_Discovery"
sys.path.insert(0, str(EGFR_DIR))
from oracle_egfr_v1 import EGFROracle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dim', type=int, required=True)
    parser.add_argument('--budget', type=int, default=500)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--bin', type=str, default=r"C:\Users\lucas\repos\fate-v5-modular\bin\main_v5_pipe.exe")
    parser.add_argument('--output', type=str, default=None, help='Save fitness history to CSV')
    args = parser.parse_args()
    
    # Load oracle once
    print(f"[Intermediary] Loading EGFR oracle...", file=sys.stderr)
    oracle = EGFROracle()
    print(f"[Intermediary] Loaded {len(oracle.compounds)} compounds", file=sys.stderr)
    
    # Launch FATE
    env = dict(os.environ)
    env["PATH"] = r"C:\msys64\mingw64\bin;C:\msys64\usr\bin;" + env.get("PATH", "")
    
    fate_cmd = [
        args.bin,
        "--dim", str(args.dim),
        "--budget", str(args.budget),
        "--seed", str(args.seed),
        "--oracle", "pipe",
        "--quiet",  # Suppress FATE's own output
    ]
    
    print(f"[Intermediary] Launching FATE: {' '.join(fate_cmd)}", file=sys.stderr)
    
    # Launch FATE with pipes for stdin/stdout
    fate_proc = subprocess.Popen(
        fate_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
    )
    
    eval_count = 0
    best_fitness = 0.0
    fitness_history = []  # Track all fitness values
    
    try:
        # Read FATE's stdout line by line
        for line in fate_proc.stdout:
            line = line.strip()
            if not line:
                continue
            
            try:
                # Parse {"req":[p1,p2,...,pD]}
                obj = json.loads(line)
                phase_list = obj.get("req", [])
                phase = np.array(phase_list)
                
                # Evaluate
                fit, info = oracle.evaluate(phase)
                eval_count += 1
                fitness_history.append(float(fit))
                
                if fit > best_fitness:
                    best_fitness = float(fit)
                
                # Send fitness back to FATE's stdin (convert numpy types to native)
                response = json.dumps({"fit": float(fit)}) + "\n"
                fate_proc.stdin.write(response)
                fate_proc.stdin.flush()
                
                # Progress every 100 evals
                if eval_count % 100 == 0:
                    print(f"[Intermediary] Eval {eval_count}, best={best_fitness:.4f}", file=sys.stderr)
                
            except (json.JSONDecodeError, KeyError, Exception) as e:
                # On error, send 0.0
                fate_proc.stdin.write('{"fit": 0.0}\n')
                fate_proc.stdin.flush()
                fitness_history.append(0.0)
                print(f"[Intermediary] Error: {e}", file=sys.stderr)
        
        # Wait for FATE to complete
        fate_proc.stdin.close()
        fate_stderr = fate_proc.stderr.read()
        fate_proc.wait()
        
        print(f"[Intermediary] DONE: {eval_count} evals, best={best_fitness:.4f}", file=sys.stderr)
        
        # Save fitness history if output specified
        if args.output and fitness_history:
            with open(args.output, "w") as f:
                f.write("eval,fitness\n")
                for idx, fit in enumerate(fitness_history):
                    f.write(f"{idx+1},{fit:.6f}\n")
            print(f"[Intermediary] Saved {len(fitness_history)} evals to {args.output}", file=sys.stderr)
        
        if fate_proc.returncode != 0:
            print(f"[Intermediary] FATE exited with {fate_proc.returncode}", file=sys.stderr)
            print(f"[Intermediary] stderr: {fate_stderr[-500:]}", file=sys.stderr)
        
    except BrokenPipeError:
        print(f"[Intermediary] Broken pipe (FATE closed stdout early)", file=sys.stderr)
        fate_proc.kill()
    except Exception as e:
        print(f"[Intermediary] Fatal error: {e}", file=sys.stderr)
        fate_proc.kill()
        raise

if __name__ == "__main__":
    import os
    main()