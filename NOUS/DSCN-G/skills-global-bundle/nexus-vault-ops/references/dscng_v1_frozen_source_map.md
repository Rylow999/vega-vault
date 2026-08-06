# DSCN-G v1.0 FROZEN — Authoritative Source Map

> Use this when the user says "use the frozen v1.0 data" or when NOUS_Tecnico_v4.md
> disagrees with a claim. The v4 doc LAGS the frozen data; the frozen DSCN-G dir is the
> SOURCE OF TRUTH. Build path: /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/ (needs `su`).

## What "v1.0 congelada" means (critical disambiguation)
- "DSCN-G v1.0 congelada" = the NOUS/DSCN-G/ DIRECTORY, frozen for FORM/structure
  (see FREEZE_CHECKLIST.md at vault root: folders, CORE/EXTENSION split, claims table).
- It is NOT a scientific freeze — C3 / Φ_proxy / discrete-dynamics are left OPEN as content
  decisions. "Congelado" (frozen structure) ≠ "validado" (validated science).
- It is NOT the NOUS_Tecnico_v4.md document. The v4 is a downstream compendium that the user
  edits separately and which, in practice, drifts behind the frozen data.

## File → claim map (verified 2026-07-25)

| Frozen file | Proves / corrects | Used to fix v4 section |
|---|---|---|
| `CLAIMS_STATUS.md` | Master claim table: T1/T2/T3 state, N_ss*≈4–5 (T1) vs 9.5±1.0 (N-back), C3 ❌, Φ_proxy ⚠️ | All claim rows; §19 |
| `DOCUMENTATION/auditoria/claims_falsifiable.md` | Per-claim falsification criteria + auditoría Ronda 4–6. The honesty manifesto (principles 1–6: "correr el código y confrontar los números"). | §19 "Limitaciones Honestas" |
| `EXTENSIONS/C3_Face_Hijacking/STATUS.md` | C3 a params originales: 2237 triggers, 0.9% with ΔPLV<−0.3, mean ΔPLV=−0.007±0.061. Rediseño 30.2%. hub_boost retirado. | §15.5 (delete r=0.73), §16.1 |
| `EXTENSIONS/C3_Face_Hijacking/README.md` | C3 is a CORE operating mode, not a separate module; retirado a params orig. | §16.1 framing |
| `CORE/VALIDATION/RESULTS/verification_results_v3.json` | T1: N_ss*=4.0/4.8/4.2 for N_init 4/50/200. T2: β=0.20, alignment=1.0000. T3: η=0.50, 30/30 "consensus" but 23 unimodal + 7 weak_unimodal. | §13.x params vs stated β=0.10/η=0.05 |
| `CORE/VALIDATION/RESULTS/maximality_real_results.json` | T1 maximalidad CONDITIONAL: full_vitality injection → maximal_real=FALSE (3–77% pruned); boundary injection (V=θ_death) → 100% pruned, TRUE. | T1 maximalidad row |
| `EXPERIMENTS/N_BACK/nback_v6_corrected/nback_v6_paper_ready.json` | N_ss*=9.5±1.02 (10 seeds). d'(10-back)=3.92, d'(15-back)=3.90 (NOT 3.12/2.78). Curve drops then plateaus ~3.9. | §3.1, T1 note (N_ss*≈4–5) |

## Key catches when patching v4 FROM this source
1. PARAM MISMATCH: frozen T2 used β=0.20, T3 used η=0.50. The v4 states β=0.10, η=0.05 as
   "Tabla 3.1". Either the v4's verification block is wrong, or the frozen runs used different
   params. Report the frozen params explicitly; don't silently pretend they match.
2. T1 maximalidad is TRUE only under boundary injection. Flat "✅ Validado" overclaims.
3. T2 real result is alignment=1.0000 — the v4's own "distancia 0.612" is doubly wrong
   (wrong metric AND shadows the real 1.0000).
4. T3 strict consensus = 23/30 = 76.7% (R≥0.9). The "97/100 (ω_sim>0.5)" in the v4 is the soft
   criterion; report both, don't let the loose one stand as the corrected value.
5. C3 must be shown RETIRED everywhere: delete §15.5's "28.6% ticks, r=0.73, 94% antipodal" —
   that number is from a pre-audit draft and is contradicted by the frozen STATUS (mean ΔPLV≈0).

## Verify an edit actually landed
Before telling the user a doc is "corregido", run:
  su -c 'stat -c "%y %s" <file>'
and diff against a known-good pre-edit copy. A byte-identical, unchanged-mtime file means the
edit did NOT land (this happened 2026-07-25: user claimed v4 fixes, vault v4 was unchanged).
