#!/usr/bin/env python3
"""RG-flow self-consistency check (DSCN-G-Quantum v9.1 sec 8.3 vs
DSCN-G-Cosmos v8.1 sec 4.3). Refits beta in  alpha = a0 (log2 N)^(-beta)
from the tables AS PRINTED IN THE PAPERS. Pure stdlib.

HONEST SCOPE (Metodo Integral): internal consistency check of the printed
tables against the stated functional form — NOT independent verification.

Audit finding (2026-10-15): the Quantum table yields beta ~ 0.26, NOT
2*pi/D ~ 2.094 as the paper claims; the Cosmos table DOES yield ~2.098
(0.16%). Quantum sec 8.3 flagged for revision.

Run:  python3 verify_rg_consistency.py   (no dependencies)
"""
import json, math

QUANTUM_TABLE = {6: 2.40e-2, 8: 2.29e-2, 10: 2.19e-2, 12: 2.10e-2, 20: 1.75e-2}
COSMOS_TABLE  = {6: 1.86e-3, 8: 1.02e-3, 10: 6.36e-4, 12: 4.34e-4, 20: 1.49e-4}

def fit_beta(table):
    """least squares: ln(alpha) = ln(a0) - beta * ln(log2 N)  (log2 N = m)"""
    ms = sorted(table)
    xs = [math.log(m) for m in ms]
    ys = [math.log(table[m]) for m in ms]
    n = len(xs)
    sx, sy = sum(xs), sum(ys)
    sxx = sum(x*x for x in xs)
    sxy = sum(x*y for x, y in zip(xs, ys))
    slope = (n*sxy - sx*sy) / (n*sxx - sx*sx)
    intercept = (sy - slope*sx) / n
    return -slope, math.exp(intercept)

beta_theory = 2 * math.pi / 3
out = {}
for name, table in [("quantum_sec_8_3", QUANTUM_TABLE), ("cosmos_sec_4_3", COSMOS_TABLE)]:
    b, a0 = fit_beta(table)
    out[name] = {"beta_fit": round(b, 4), "a0_fit": a0,
                 "beta_theory_2pi_over_D": round(beta_theory, 4),
                 "rel_err_percent": round(abs(b - beta_theory) / beta_theory * 100, 3)}
    print(f"{name}: beta_fit={b:.4f} vs 2pi/D={beta_theory:.4f} "
          f"(rel err {out[name]['rel_err_percent']}%)")
out["verdict"] = ("cosmos table CONSISTENT with the law (0.16%); quantum table "
                  "INCONSISTENT (87%) — flagged for revision")
out["HONEST_NOTE"] = ("internal consistency only: printed tables were generated "
                      "by the same law being fitted; independent verification "
                      "requires measuring alpha(N) from substrate dynamics "
                      "(simulation not present in the repo)")
with open("verification_rg.json", "w") as f:
    json.dump(out, f, indent=2)
