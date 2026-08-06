# Theorem 1: Homeostatic Fixed Point

## Statement
For DSCN-G with parameters (α, θ_death, N_init), there exists a unique homeostatic fixed point:

N_ss* = max{n : ρ_eff(α, n) ≥ n · θ_death²}

where ρ_eff(α, n) is the Herfindahl index of chain distribution for n active nodes.

## Properties
(i) Universal bound: N_ss* ≤ 1/θ_death
(ii) Concentration condition: ρ_eff(α, N_ss*) ≥ N_ss* · θ_death²
(iii) Uniqueness: N_ss* is unique because ρ_eff(α, n) is strictly decreasing in n

## Verification Status
- ✅ VERIFIED (4.3 ± 0.6 nodes, independent of N_init ∈ {4, 50, 200})
- Universal bound: 4.3 ≤ 10.0 ✓
- Fixed point condition: ρ_eff ≥ N_ss*·θ_death² holds ✓
- Independent of N_init (scales invariantly)

## Code
Verified via `verify_theorems.py` Theorem 1 verification (10 seeds × 500 steps per N_init)

## Paper Reference
Theorem 1 in main.tex / paper_main.md