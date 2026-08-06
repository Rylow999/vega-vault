# Paper Status - DSCN-G

## Current Draft
- Main paper: `papers/DSCN_G/paper_main.md` (markdown) / `papers/DSCN_G/main.tex` (LaTeX)
- PDF compiled: `papers/DSCN_G/main.pdf`

## Theorem Status in Paper
| Theorem | Paper Label | Status | Note |
|---------|-------------|--------|------|
| Theorem 1 | Theorem 1 | ✅ Verified | Homeostatic fixed point |
| Theorem 2 | Theorem 2 | ⚠️ Verification pending | Vector convergence - known issue |
| Theorem 3 | Theorem 3 | ⚠️ Partial | Phase convergence - improved with adaptive coupling |
| Theorem 4 | Theorem 4 | ❌ Fails | Φ-proxy scale relation - marked "pending" |

## Removed Sections
- Former Theorems 4-6 (Impossibility theorems vs IIT/GWT/PP) - REMOVED
- Moved to "Future Work" section

## Paper Structure
1. Introduction
2. Computational Foundations (Eqs 1-7)
3. Formal Theorems (1-3, with 4 marked pending)
4. Working Memory Validation (Section 4)
5. Prediction C3: Phase-Hijacking (Section 5)
6. Theorem 4: Φ-proxy Scale Relation (Section 6, pending)
7. Discussion & Future Work

## Figures
- Fig 1: Architecture diagram
- Fig 2: Theorem 1 verification (N_ss* vs N_init)
- Fig 3: Theorem 3 verification (phase convergence)
- Fig 4: WM capacity curve (d' vs n-back)
- Fig 5: C3 Phase-Hijacking schematic

## Status
- Ready for submission with honest framing of Theorem 2/3/4 status
- All code reproducible via `papers/DSCN_G/code/verify_theorems.py`
- CHANGES.md documents all corrections from review