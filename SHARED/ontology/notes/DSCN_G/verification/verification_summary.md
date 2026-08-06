# DSCN-G Verification Summary

## Overview
All verification code in `papers/DSCN_G/code/verify_theorems.py`

## Theorem Status

| Theorem | Status | Key Metrics |
|---------|--------|-------------|
| Theorem 1: Homeostatic Fixed Point | ✅ PASS | N_ss* = 4.3 ± 0.6, universal bound ✓ |
| Theorem 2: Parametric Vector Convergence | ⚠️ KNOWN ISSUE | Distance 0.47 > β=0.1 (C≈4.75) |
| Theorem 3: Phase Convergence Rate | ⚠️ PARTIAL | p_conv=0.80, adaptive coupling helps |
| Theorem 4: Φ-proxy Scale Relation | ❌ FAILS | ρ_eff·Φ_proxy rises with N, not constant |

## Key Findings

### Theorem 1: PASS
- N_ss* = 4.3 ± 0.6 (independent of N_init)
- Universal bound N_ss* ≤ 1/θ_death = 10 ✓
- Fixed-point condition ρ_eff ≥ N_ss*·θ_death² holds

### Theorem 2: KNOWN ISSUE
- Distance ‖ω−ω*‖ = 0.47 > β=0.1 (C≈4.75)
- Root cause: reward structure incentivizes MAXIMIZATION (→1.0) not matching expectation (0.5)
- Converges to max alignment (1.0), not E[reward] (0.5)

### Theorem 3: PARTIAL (Improved with Adaptive Coupling)
- Fixed η=0.1: p_conv = 0.60-0.70 (30-40% antipodal)
- Adaptive coupling: p_conv = 0.80-1.00 (10-0% antipodal)
- Bound exp(-cληR_minT) still loose (2.7e-33 vs observed 0.1-0.2)

### Theorem 4: FAILS
- ρ_eff·Φ_proxy rises monotonically with N (0.65→0.68)
- Insensitive to α (same at α=1 and α=5)
- Marked "verification pending" in paper

## Claims for Paper
| Claim | Paper Status | Verification |
|-------|--------------|--------------|
| Homeostatic fixed point N_ss* ≈ 4 | Theorem 1 | ✅ Verified |
| WM capacity ≈ 4 items | Section 4 | ✅ Empirically supported |
| Vector convergence ‖ω−ω*‖ ≤ Cβ | Theorem 2 | ⚠️ Known issue |
| Phase convergence exponential | Theorem 3 | ⚠️ Partial (80%) |
| Φ-proxy scale relation | Theorem 4 | ❌ Fails (pending) |
| Phase-hijacking (C3) | Section 5 | 🔮 Conjecture |

## Code Locations
- Main simulator: `papers/DSCN_G/code/dscn_g_simulator.py`
- Verification: `papers/DSCN_G/code/verify_theorems.py`
- WM validation: `papers/DSCN_G/code/dscn_g_wm_emergent.py`
- Results: `data/verification_results.json`