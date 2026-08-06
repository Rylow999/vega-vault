#!/usr/bin/env python3
"""EGFR Oracle — pipe mode (line-by-line).

Protocol:
  stdin:  [p1,p2,...,pD]  (one phase vector per line, JSON array)
  stdout: {"fit": value}  (one fitness per line)

Compatible with main_v5_pipe.exe (no batch needed)
"""
import sys
import json
import numpy as np
from pathlib import Path

# Silence RDKit warnings
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')

# Import oracle
sys.path.insert(0, str(Path(__file__).parent))
from oracle_egfr_v1 import EGFROracle

# Load oracle once
print("[EGFR Pipe Oracle] Loading...", file=sys.stderr)
oracle = EGFROracle()
print(f"[EGFR Pipe Oracle] Loaded {len(oracle.compounds)} compounds", file=sys.stderr)

eval_count = 0

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        # Parse JSON object: {"req": [p1, p2, ..., pD]}
        obj = json.loads(line)
        phase_list = obj.get("req", [])
        phase = np.array(phase_list)
        
        # Evaluate
        fit, info = oracle.evaluate(phase)
        eval_count += 1
        
        # Output fitness
        print(json.dumps({"fit": fit}))
        sys.stdout.flush()
        
    except (json.JSONDecodeError, KeyError, Exception) as e:
        # On error, output 0.0 fitness
        print(json.dumps({"fit": 0.0}))
        sys.stdout.flush()

print(f"[EGFR Pipe Oracle] DONE: {eval_count} evaluations", file=sys.stderr)