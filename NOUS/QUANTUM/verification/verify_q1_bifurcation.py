#!/usr/bin/env python3
"""Q1 classical part (DSCN-G-Quantum v9.1 sec 6.1), pure stdlib:
H_phase = -(eta*R/2) cos(dphi)  =>  d2H/ddphi2 = (eta*R/2) cos(dphi),
so the restoring stiffness vanishes exactly at dphi = pi/2
(saddle-node bifurcation). The quantum Gamma_dec ~ sin^2(dphi) remains a
POSTULATED mechanism (Appendix H.2 not included in the markdown).

Run:  python3 verify_q1_bifurcation.py   (no dependencies)
"""
import json, math

# scan cos around pi/2 with dense grid
best = None
for i in range(100001):
    phi = math.pi * i / 100000
    val = abs(math.cos(phi))
    if best is None or val < best[1]:
        best = (phi, val)
res = {"stiffness_zero_at": round(best[0], 6),
       "expected_pi_over_2": round(math.pi / 2, 6),
       "ok": bool(abs(best[0] - math.pi / 2) < 1e-4),
       "lindblad_gamma_dec": "NOT_REPRODUCIBLE_FROM_TEXT (operator L_k absent)"}
with open("verification_q1.json", "w") as f:
    json.dump(res, f, indent=2)
print(res)
