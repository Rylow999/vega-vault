#!/usr/bin/env python3
"""Lemma 4.1 (DSCN-G-Quantum v9.1): exact spectral gap lambda_2 = 4
of the fractal circulant C_N(S), S = {1, 2, 4, ..., N/2}, N = 2^m.

Method: exact spectral formula for circulant Laplacians,
  lambda_j = k_bar - sum_{d in S} w_d * cos(2*pi*j*d / N)
where w_d = 2 for d < N/2 (pair +/(-d)) and w_{N/2} = 1 (self-inverse).

Run:  python3 verify_lambda2.py
Output: verification_lambda2.json
Author: Luciano Benjamin Nieto. License: MIT.
"""
import json, math

def lambda2_and_kbar(m):
    N = 2 ** m
    S = [2 ** k for k in range(m)]
    vals = []
    for j in range(N):
        a = 0.0
        for d in S:
            w = 1 if d == N // 2 else 2
            a += w * math.cos(2 * math.pi * j * d / N)
        vals.append((2 * m - 1) - a)
    vals.sort()
    return 2 * m - 1, vals[1]

rows, ok_all = [], True
for m in range(3, 17):
    N = 2 ** m
    kbar, l2 = lambda2_and_kbar(m)
    err = abs(l2 - 4.0)
    ok = err < 1e-9
    ok_all &= ok
    rows.append({"m": m, "N": N, "k_bar": kbar,
                 "lambda2": round(l2, 12), "abs_err": err, "ok": ok})

res = {"lemma": "4.1 (iii): lambda_2(L) = 4 for all m >= 3",
       "method": "exact circulant Laplacian eigenvalues",
       "rows": rows, "all_ok": ok_all}
with open("verification_lambda2.json", "w") as f:
    json.dump(res, f, indent=2)
for r in rows:
    print(f"m={r['m']:2d} N={r['N']:6d} k_bar={r['k_bar']:5.1f} "
          f"lambda2={r['lambda2']:.12f} err={r['abs_err']:.1e} "
          f"{'OK' if r['ok'] else 'FAIL'}")
print("ALL OK" if ok_all else "SOME FAILED")
