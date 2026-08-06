#!/usr/bin/env python3
"""EGFR Oracle wrapper — batch mode for pipe protocol.

Reads: {"req": [[phase1], [phase2], ...]}
Writes: {"fit": [fit1, fit2, ...]}

Compatible with main_v5_pipe.exe --batch
"""
import sys
import json
import numpy as np
from pathlib import Path

# Import oracle
sys.path.insert(0, str(Path(__file__).parent))
from oracle_egfr_v1 import EGFROracle

# Load oracle once
print("[EGFR Batch Oracle] Loading...", file=sys.stderr)
oracle = EGFROracle()
print(f"[EGFR Batch Oracle] Loaded {len(oracle.compounds)} compounds", file=sys.stderr)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    
    if "req" not in obj:
        continue
    
    req = obj["req"]
    
    # Handle batch mode: req is [[phase1], [phase2], ...]
    if isinstance(req[0], list):
        phases = req
    else:
        phases = [req]
    
    # Evaluate all phases
    fitnesses = []
    for phase in phases:
        phase_array = np.array(phase)
        fit, info = oracle.evaluate(phase_array)
        fitnesses.append(fit)
    
    # Output in batch format
    if len(fitnesses) == 1:
        # Scalar mode
        print(json.dumps({"fit": fitnesses[0]}))
    else:
        # Batch mode
        print(json.dumps({"fit": fitnesses}))
    
    sys.stdout.flush()

print(f"[EGFR Batch Oracle] DONE", file=sys.stderr)