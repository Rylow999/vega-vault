# Applying the 7-point audit to NOUS_Tecnico_v4.md — exact recipe (2026-07-25)

Companion to SKILL.md "Applying the 7-point audit fixes to the v4 (patch recipe)".
Contains the real replacement strings and the verification/diff commands so a future session
can re-apply or extend the fix without re-deriving the byte layout.

## 0. Where things live
- Vault target: `/sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md` (root-only)
- Work copy (readable): `/data/user/0/com.hermesagent.android/files/home/NOUS_Tecnico_v4.md`
- Frozen SOURCE OF TRUTH: `NOUS/DSCN-G/` dir — `CLAIMS_STATUS.md`, `DOCUMENTATION/auditoria/claims_falsifiable.md`,
  `EXTENSIONS/C3_Face_Hijacking/STATUS.md`, `CORE/VALIDATION/RESULTS/verification_results_v3.json`,
  `CORE/VALIDATION/RESULTS/maximality_real_results.json`, `EXPERIMENTS/N_BACK/nback_v6_corrected/nback_v6_paper_ready.json`.

## 1. The 7 fixes mapped to replacement strings (condensed)

P1 (missing §19/§20): appended appendix after §17.5:
```
## 19. Limitaciones Honestas
[8 numbered items, cites claims_falsifiable.md honesty manifesto; includes the β-mismatch note:
 "La verificación canónica de T2 usó β=0.20 (alignment 1.0000); el diseño de núcleo usa β=0.10.
  Ambos convergen; se declara para no confundir cotas."]
## 20. Referencias
[Kuramoto 1975, Robbins-Monro 1951, Schultz 1997, von Mises 1918 + vault paths]
```

P2 (C3 contradiction): §15.5 header → "Activación C3 (Phase-Hijacking) — ❌ RETIRADA"; body replaced
with real numbers: 2237 triggers (3.73%), 20/2237 (0.9%) ΔPLV<−0.3, mean ΔPLV=−0.007±0.061.
§16.1 C3 block: "Métrica real (30 seeds × 2000 steps): ... La correlación E_root vs error de
fase NO es 0.73 (ese valor era de un borrador previo y se retira)."

P3 (ρ recycling): §13.5 renamed "Densidad Contextual Efectiva ρ(t)" + note box:
"ρ aquí es la densidad contextual de la Ec. 9, distinta de la ρ_mean≈0.44–0.49 reportada como
métrica de consenso de T1 en verification_results_v3.json."

P4 (T2 distance/cosine): §4 T2 verification block replaced: alignment 1.0000 (coseno, no distancia),
acotamiento max‖ω‖=1.087<1.111, "el valor 0.612 citado antes era el parámetro de orden de fase
ω_sim de T3, no una norma de vector". Resumen table: split "alignment 1.0000 (30 seeds freeze)" vs
"max‖ω‖ 1.087 (100 seeds ref code)".

P5 (T3 dual criterion): §13.4 + §15.2 now show BOTH: "30/30 (100%) criterio laxo ω_sim>0.5" AND
"23/30 = 76.7% criterio estricto R≥0.9". Report 76.7% as the real consensus rate.

P6 (graph doesn't grow / P6-P7 provenance): note added under §16.1 P8:
"P6/P7 provienen de simulaciones de extensión con grafo en crecimiento, NO del código de referencia
de la Sección 14, que corre con 4 raíces fijas (N*≈4–5) y no implementa el XOR ni la cascada
(Ec. 12 es `pass`)."

P7 (T1 statement vs verification): §13.1 metric changed from "ρ_eff=0.7001" to error de vitalidad
2.3e-4±1.1e-4. §15.4 N* row: "N_ss*≈4–5, NO 9–10 (ese valor es del N-back v6)".
NOTE: T1 maximalidad condicional (inyectar en θ_death → 100% podado; inyectar en V=1.0 → solo
3–77%) was declared via the cite to frozen data but NOT spelled out inline in T1 — future session
should add one sentence in §4 T1 if the user wants it explicit.

## 2. Blocks that HAD to be done via `patch` (not Python bulk-replace)
The Python `content.count(old)==1` assertion FAILED (count 0) on these two because their LaTeX
`\|` / `$` / `∑` did not survive script escaping:
- §13.4 table row `| **T1: Vitalidad** | 100 / 100 | $\rho_{\text{eff}}$ ...` → split T1/T3 rows.
- §13.5 header `### 13.5 Distribución de $\rho_{\text{eff}}$ (Tiempo Subjetivo Efectivo)` → renamed.
Fix: use Hermes `patch` tool (mode=replace) with the literal file text — it fuzzy-matches
backslashes. Do these AFTER the Python pass; do not retry Python on them.

## 3. Verification & write-back commands (run in normal terminal, home copy)
```
F=~/NOUS_Tecnico_v4.md
grep -n "r = 0.73\|97 / 100 | \*\*ω\|Distancia final al óptimo\|28.6% ± 3.1%" "$F"  # must be EMPTY
grep -c "RETIRADA" "$F"; grep -c "76.7%" "$F"; grep -c "Limitaciones Honestas" "$F"  # all >0
wc -l "$F"   # expect ~1814 (was 1777)
```
Write to vault:
```
su -c "cp /data/.../home/NOUS_Tecnico_v4.md /sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md"
su -c "chown root:everybody /sdcard/Hermes/.../NOUS_Tecnico_v4.md && chmod 664 /sdcard/Hermes/.../NOUS_Tecnico_v4.md"
su -c "cp /sdcard/Hermes/.../NOUS_Tecnico_v4.md /sdcard/Hermes/.../NOUS_Tecnico_v4.md.vault_orig_20260725.bak"
su -c "diff /sdcard/Hermes/.../NOUS_Tecnico_v4.md.vault_orig_20260725.bak /sdcard/Hermes/.../NOUS_Tecnico_v4.md | head -120"
```

## 4. Known debt left in the doc (be honest if user asks)
- The v4 Índice de Contenidos still lists §18/§19/§20; §18 (NOUS-Memory/OpenClaw) was NOT added
  (only §19/§20). Index should be patched separately if user wants full consistency.
- Reference implementation (Sección 14) still uses β=0.10, 100 seeds, 4 root nodes, cascade=`pass`.
  Not re-run to match the 30-seed β=0.20 freeze — declared as pending in §19 point 2.
- T1 maximalidad condition (injection protocol) not spelled inline in §4 T1.
