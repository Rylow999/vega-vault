# Theorem 2: Parametric Vector Convergence

## Statement
For DSCN-G with parameters (λ_vm, n_actions, θ*, β), the sequence {ω_i(t)} converges with probability 1 to the set:

A = {ω : ‖ω − ω*(λ_vm, n_actions, θ*)‖ ≤ C · β}

where ω*(λ_vm, n_actions, θ*) = Σ_a P(a|θ*)·o(a)·R(a)·ê_R is the parametric fixed point and C = σ²_ξ/(2−β) with σ²_ξ the stochastic gradient variance.

## Current Status
⚠️ **KNOWN ISSUE** - Architectural disconnect between ω learning and phase-based reward

## Verification Results
- Theoretical ω* (alignment-based reward): 0.5 (scalar projection onto ω_ideal)
- Observed convergence: ω_proj → 1.0 (max alignment)
- Distance ‖ω_proj − ω*‖ = 0.47 > β=0.1 (C ≈ 4.75, not O(1))

## Root Cause
Architectural disconnect:
- ω learns via TD-learning toward ω_ideal (alignment-based reward)
- Reward in original paper depends on phase alignment (phase-based, not vector-based)
- Phase convergence (Theorem 3) is prerequisite for vector convergence
- Current verification uses 2000 steps; phase convergence needs ~5000+ steps

## Proposed Fixes (Future Work)
1. **Align reward structure**: Make reward depend on ω alignment (done - alignment-based reward)
2. **Extend verification time**: 50,000+ steps for phase convergence
3. **Alternative**: Initialize phases near θ* for faster convergence

## Code
Verified via `verify_theorems.py` Theorem 2 verification

## Paper Reference
Theorem 2 in main.tex / paper_main.md - marked "verification pending"

## Status
⚠️ KNOWN ISSUE - Documented in CHANGES.md, paper marks as "verification pending"