# NOUS_Tecnico_v4.md — Internal-Consistency Audit (2026-07-25)

Deep read of `/sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md`
(1777 lines, 91KB). 7 real defects found. Use as the fix list before any edit/submission.
Companion to the SKILL.md "Document-consistency audit" 7-point checklist (same numbering).

## F1 — Index promises sections that do not exist (checklist #1)
Índice lists §18 (NOUS-Memory/OpenClaw), §19 (Limitaciones Honestas), §20 (Referencias).
File ends at §17.5 (line 1777). Missing ~1/3 of promised doc, INCLUDING "Limitaciones
Honestas" — the first thing a reviewer asks for.
FIX: either write §18–20 or trim the Índice to match the body.

## F2 — C3 RETIRED in status but LIVE in body (checklist #2)
Index + §16.1: C3 RETIRADO (Ronda 6: 0.9% triggers at original params, ΔPLV≈0).
BUT §15.5: "28.6%±3.1% ticks with C3 active, r(E_root→phase error)=0.73, 94% antipodal",
and §16.1's own C3 statement repeats "r=0.73; 94% direccionalidad antipodal".
A doc cannot say "retired (0.9%)" and "r=0.73, 94% antipodal" on the same pages.
FIX: state explicitly which params produce the 0.9% (original) vs the 28.6%/r=0.73 (some
other config), or drop §15.5's C3 evidence if it is from the redesigned/non-original run.

## F3 — ρ_eff notation recycled for two different quantities (checklist #3)
- T1 / §13.1: "ρ_eff = 0.7001" = vitality CONVERGENCE FACTOR.
- §13.5 / §15.3: "ρ_eff = 0.7001" = densidad contextual promedio ρ(t) ∈ [0,1].
Different variables, coincidentally identical number.
FIX: rename one (e.g. convergence factor → ρ_conv; keep ρ_eff for contextual density).

## F4 — T2 reports a cosine as a "distance" (checklist #4)
Line 303: "Distancia final al óptimo ‖ω−ω_ideal‖ = 0.612 ± 0.173". This is cosine similarity,
confirmed by §13.3 where ω_sim = 0.612 is the phase-order/cosine parameter. The real T2 bound
(§13.2/§13.4) uses max ‖ω‖ = 1.087 < 1.111.
FIX: relabel 0.612 as cosine; keep the norm-bound (1.087) as the T2 verification metric.

## F5 — T3 dual criteria not unified in body (checklist #5)
§13.4: "97/100 semillas (ω_sim > 0.5)" (soft). Index already corrected to "76.7% estricto
(R≥0.9)". Body still leads with 97% without flagging the strict value.
FIX: report both: 97% at cos>0.5 (soft) AND 76.7% at R≥0.9 (strict). Don't leave 97% standing
as if it were the corrected figure.

## F6 — Graph does not grow, but P6/P7 need a growing graph (checklist #6)
Telemetry §15.4: "Nodos activos = 4.0 ± 0.0" — sim runs on the 4 fixed roots, graph never
grows. But P6 (inheritance drift, "dist padre-hijo 0.098±0.012") and P7 (XOR abstraction,
"94/100 formaciones correctas") require node creation. The reference code step_12 leaves
cascade as `pass` and XOR is not implemented at all. So P6/P7 metrics do NOT come from the
quoted §14 reference code.
FIX: name the actual simulation that produces P6/P7 (or note they are from a separate/extension
script), or downgrade their verification status.

## F7 — T1 statement ≠ verification (checklist #7)
Theorem 1 (line 267) is just "0 ≤ V_i ≤ 1" — identical to Invariante 7.1 (already proven by
induction). §13.1 renames it "Convergencia de Vitalidad" with a NEW enunciado
(V_i* = Ā_i/(1−e^−γ)) and verifies it by measuring ρ (densidad contextual), not vitality
convergence. Statement and verification measure different things.
FIX: align §13.1's verification to the renamed enunciado (track |V_i(T)−V_i*|), or restore T1
to its literal 0≤V≤1 statement and move the density discussion to its own place.

## Notes for editing
- Core DSCN-G paper is FROZEN (Ronda 6, 2026-07-24) — see freeze-safe recipe in
  references/updating_nous_from_triada.md. The v4.0 compendium is NOT core; these are doc-hygiene
  fixes, not core-claim changes. But coordinate with CORE claims (T1/T2/T3 numbers) so the
  compendium does not contradict the frozen paper's reported values.
- Verify claims against ANALISIS_ESTADO_2026-07-24.md + claims_falsifiable.md (authoritative
  post-Ronda-6 status) before re-citing any T1/T2/T3/C3 figure.
