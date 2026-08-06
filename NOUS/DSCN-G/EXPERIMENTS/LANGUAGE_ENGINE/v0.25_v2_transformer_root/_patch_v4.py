import io

PATH = "/data/user/0/com.hermesagent.android/files/home/NOUS_Tecnico_v4.md"
BAK  = PATH + ".bak2"

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

with open(BAK, "w", encoding="utf-8") as f:
    f.write(content)

reps = []

# --- PUNTO 4: T2 confunde distancia/coseno (lineas ~302-308) ---
reps.append(("T2_block", """**Verificación empírica (100 seeds × 2000 pasos):**
- Distancia final al óptimo: $\| \\boldsymbol{\\omega} - \\boldsymbol{\\omega}_{\\text{ideal}} \| = 0.612 \\pm 0.173$ (media ± std)
- **Factor de convergencia efectivo** $\\rho_{\\text{eff}} = 0.7001 \\pm 0.021$ (definido como razón de distancias consecutivas en fase estacionaria)
- Teórico para $\\beta=0.10$: $\\rho_{\\text{theory}} = 1-\\beta = 0.90$; observado menor debido a ruido de recompensa y acoplamiento de fase.
- **97% de las semillas** ($p_{\\text{conv}} = 0.97$) alcanzan fase estacionaria antes del paso 1500.

> **Nota:** El valor $\\rho_{\\text{eff}} = 0.7001$ indica convergencia **más rápida** que el límite teórico pesimista ($0.90$), atribuible a la señal de fase (Ecuación 3) que proporciona gradiente adicional.""",
"""**Verificación empírica (escala canónica, 30 seeds × 2000 pasos; datos de `CORE/VALIDATION/RESULTS/verification_results_v3.json`):**
- **Alignment final** $\\cos(\\boldsymbol{\\omega}, \\boldsymbol{\\omega}_{\\text{ideal}}) = 1.0000 \\pm 0.0000$ (no es una distancia euclídea; el valor $0.612$ citado antes era el parámetro de orden de fase $\\omega_{\\text{sim}}$ de T3, no una norma de vector).
- Acotamiento de norma: $\\max \\|\\boldsymbol{\\omega}\\| = 1.087 < 1.111$ (cota teórica $\\beta/(1-\\beta)\\cdot R_{\\max} + \\|\\boldsymbol{\\omega}(0)\\|$ con $\\beta=0.10$). **Nota:** la verificación canónica congelada usó $\\beta=0.20$, que da alignment 1.0000; el diseño de núcleo usa $\\beta=0.10$. Ambos convergen; la diferencia de $\\beta$ se declara explícitamente.
- **97% de las semillas** ($p_{\\text{conv}} = 0.97$) alcanzan fase estacionaria antes del paso 1500 (umbral de coseno $>0.5$, criterio laxo; ver T3 para el criterio estricto).

> **Nota:** El límite teórico de T2 es de norma vectorial, no de coseno. El sistema converge a vecindad $O(\\beta)$ del óptimo; el alignment medido (1.0000) refleja coseno, no distancia euclídea."""))

# --- PUNTO 4: resumen tabla (334-343) ---
reps.append(("resumen_tbl", """### Resumen de Valores Verificados (100 Seeds × 2000 Pasos)

| Métrica | Valor | IC 95% | Teorema |
|---------|-------|--------|---------|
| $\\rho_{\\text{eff}}$ (factor convergencia) | 0.7001 | [0.679, 0.721] | Teorema 2 |
| $\\omega_{\\text{sim}}$ (similitud coseno final) | 0.612 | [0.578, 0.646] | Teorema 2 |
| $p_{\\text{conv}}$ (convergencia <1500 pasos) | 0.97 | [0.92, 1.00] | Teorema 2 |
| $T_{\\text{lock}}$ (bloqueo fase) | 187 pasos | [144, 230] | Teorema 3 |
| Error fase final | 0.18 rad | [0.14, 0.22] | Teorema 3 |
| $V_{\\min}$ / $V_{\\max}$ | 0.000 / 1.000 | — | Teorema 1 |""",
"""### Resumen de Valores Verificados

> **Escala:** la verificación canónica congelada (`CORE/VALIDATION/RESULTS/`) usó 30 seeds × 2000 steps (Ronda 4). Las filas marcadas «ref code» provienen del reference implementation de la Sección 14 a 100 seeds; son consistentes cualitativamente pero no son el freeze.

| Métrica | Valor | IC 95% | Teorema | Escala |
|---------|-------|--------|---------|--------|
| alignment $\\cos(\\boldsymbol{\\omega},\\boldsymbol{\\omega}_{\\text{ideal}})$ | 1.0000 | [1.0000, 1.0000] | T2 | 30 seeds (freeze) |
| $\\max\\,\\|\\boldsymbol{\\omega}\\|$ (cota norma) | 1.087 | < 1.111 | T2 | 100 seeds (ref code) |
| $\\omega_{\\text{sim}}$ (orden de fase) | 0.612 | [0.567, 0.657] | T3 | 30 seeds (freeze) |
| consensus estricto T3 (R≥0.9) | 76.7% | 23/30 | T3 | 30 seeds (freeze) |
| $p_{\\text{conv}}$ (convergencia <1500 pasos) | 0.97 | [0.92, 1.00] | T2 | 100 seeds (ref code) |
| $T_{\\text{lock}}$ (bloqueo fase) | 187 pasos | [144, 230] | T3 | 100 seeds (ref code) |
| Error fase final | 0.18 rad | [0.14, 0.22] | T3 | 100 seeds (ref code) |
| $V_{\\min}$ / $V_{\\max}$ | 0.000 / 1.000 | — | T1 | 100 seeds (ref code) |"""))

# --- PUNTO 7: T1 metrica en 13.1 ---
reps.append(("T1_metric", """- **Resultado**: 100/100 semillas convergen ($\\rho_{\\text{eff}} = 0.7001 \\pm 0.002$)
- Error medio final: $2.3 \\times 10^{-4} \\pm 1.1 \\times 10^{-4}$""",
"""- **Resultado**: 100/100 semillas convergen (error medio final $|V_i(T)-V_i^*| = 2.3 \\times 10^{-4} \\pm 1.1 \\times 10^{-4} < \\epsilon=0.01$). La métrica de convergencia de T1 es el error de vitalidad, **no** $\\rho$ (que es la densidad contextual de T2, ver Sección 13.5)."""))

# --- PUNTO 5: 13.4 tabla T1/T3 ---
reps.append(("T13_4", """| **T1: Vitalidad** | 100 / 100 | $\\rho_{\\text{eff}}$ | > 0.65 | **0.7001** ± 0.002 |
| **T2: Norma $\\omega$** | 100 / 100 | max $\\|\\omega\\|$ | < 1.111 | **1.087** |
| **T3: Fase** | 97 / 100 | $\\omega_{\\text{sim}}$ | > 0.5 | **0.612** ± 0.045 |""",
"""| **T1: Vitalidad** | 100 / 100 | error $|V_i(T)-V_i^*|$ | < 0.01 | **2.3e-4** ± 1.1e-4 |
| **T2: Norma $\\omega$** | 100 / 100 | max $\\|\\omega\\|$ | < 1.111 | **1.087** |
| **T3: Fase (criterio laxo $\\omega_{\\text{sim}}>0.5$)** | 30 / 30 | $\\omega_{\\text{sim}}$ | > 0.5 | **0.612** ± 0.045 |
| **T3: Fase (criterio estricto R≥0.9)** | 23 / 30 | consenso unimodal | > 0.9 | **76.7%** |"""))

# --- PUNTO 3: 13.5 renombrar + aclarar rho ---
reps.append(("T13_5", """### 13.5 Distribución de $\\rho_{\\text{eff}}$ (Tiempo Subjetivo Efectivo)

La **densidad contextual efectiva** promedio sobre 100 semillas:
$$
\\rho_{\\text{eff}} = \\frac{1}{T} \\sum_{t=1}^T \\rho(t) \\cdot (1 + \\rho(t))
$$
- Media: **0.7001**
- Desvío: **0.002**
- Rango: [0.695, 0.705]
- Interpretación: El sistema opera consistentemente en **Fase 3 (Comprensión Profunda)** donde $\\rho > 0.7$ y $\\beta_{\\text{eff}} \\approx 0.20$ (duplicando tasa base)""",
"""### 13.5 Densidad Contextual Efectiva $\\rho(t)$ (Tiempo Subjetivo)

La **densidad contextual** $\\rho(t) \\in [0,1]$ (Ecuación 9) promedio sobre 100 semillas:
$$
\\bar{\\rho} = \\frac{1}{T} \\sum_{t=1}^T \\rho(t)
$$
- Media: **0.7001**
- Desvío: **0.002**
- Rango: [0.695, 0.705]
- Interpretación: El sistema opera consistentemente en **Fase 3 (Comprensión Profunda)** donde $\\rho > 0.7$ y $\\beta_{\\text{eff}} \\approx 0.20$ (duplicando tasa base).

> **Aclaración de notación:** $\\rho$ aquí es la densidad contextual de la Ecuación 9, **distinta** de la $\\rho_{\\text{mean}} \\approx 0.44\\text{–}0.49$ reportada como métrica de consenso de T1 en los datos congelados (`verification_results_v3.json`). Son dos cantidades diferentes; no deben confundirse."""))

# --- PUNTO 5: 15.2 T3 numeros ---
reps.append(("T15_2", """### 15.2 Sincronización de Fase (Parámetro de Orden ω_sim)

- **Media**: 0.612 ± 0.045 (últimas 500 ticks)
- **Semillas convergidas**: 97/100 (ω_sim > 0.5)
- **Semillas antipodales**: 3/100 (ω_sim ∈ [0.42, 0.48]) — estructura de doble atractor confirmada""",
"""### 15.2 Sincronización de Fase (Parámetro de Orden ω_sim)

- **Media (criterio laxo ω_sim > 0.5)**: 0.612 ± 0.045 (últimas 500 ticks) → 30/30 semillas (100%) por el criterio del código.
- **Criterio estricto (R ≥ 0.9, consenso unimodal)**: 23/30 = **76.7%** (7/30 solo pasan el respaldo laxo R ≥ 0.5, «weak_unimodal»; 0/30 bimodales). Reportar 76.7% como consensus rate real de T3.
- **Semillas antipodales**: 3/100 (ω_sim ∈ [0.42, 0.48]) — estructura de doble atractor confirmada."""))

# --- PUNTO 1/7: 15.4 N_ss* ---
reps.append(("T15_4", """| Nodos activos | 4.0 ± 0.0 | Teorema 1: N* = 4 (ρ_eff/θ_death = 7.00, bound 10) |""",
"""| Nodos activos (N*) | 4.0 ± 0.0 | Teorema 1: punto fijo homeostático. Datos congelados T1: N_init 4→4.0, 50→4.8±0.4, 200→4.2±0.5 (cota 1/θ_death=10 respetada). N_ss*≈4–5, **no** 9–10 (ese valor es del N-back v6). |"""))

# --- PUNTO 2: 15.5 C3 retirada ---
reps.append(("T15_5", """### 15.5 Activación C3 (Phase-Hijacking)

- **Ticks con C3 activo**: 28.6% ± 3.1%
- **Semillas con ≥1 evento C3**: 67/100
- **Correlación E_root → phase error**: r = 0.73 (p < 0.001)
- **Direccionalidad**: 94% de hijackings hacia antipodal (φ* + π)""",
"""### 15.5 Activación C3 (Phase-Hijacking) — ❌ RETIRADA (ver `EXTENSIONS/C3_Face_Hijacking/STATUS.md`)

La telemetría anterior (28.6% ticks con C3, r=0.73, 94% antipodal) **no se sostiene** a los parámetros de diseño originales y se retira del v4.0:
- Verificación real (30 seeds × 2000 steps): 2237 triggers (3.73% de steps); solo **20/2237 (0.9%)** muestran ΔPLV < −0.3; mean ΔPLV = −0.007 ± 0.061 (≈ 0).
- Rediseño (θ_death=0.01, hijack_steps=150, η=0.80) sube a 30.2%, pero esos parámetros son ~10× los de diseño y no alcanzan «la norma».
- C3 queda como **extensión retirada**, no como claim del núcleo. El núcleo (T1/T2/T3) no depende de C3."""))

# --- PUNTO 2: 16.1 C3 bloque ---
reps.append(("T16_1_C3", """#### **C3 — Phase-Hijacking por Valencia** (RETIRADO en Ronda 6, 2026-07-24 — NO SOSTENIDO a parámetros originales: 0.9% triggers, ΔPLV≈0; rediseño llega a 30.2%, lejos de "la norma". Se mantiene como Predicción histórica, no como claim activo)
- **Enunciado**: Cuando $E_{\\text{root}} > \\theta_{\\text{emerg}} = 0.30$, la fase root $\\phi_{\\text{root}}$ es perturbada direccionalmente hacia el atractor antipodal $\\phi^* + \\pi$.
- **Métrica**: Correlación $E_{\\text{root}}$ vs error de fase = 0.73; 94% direccionalidad antipodal.
- **Falsación**: Si eventos de alta valencia ($E > 0.30$) producen resets de fase uniformes/bidireccionales.""",
"""#### **C3 — Phase-Hijacking por Valencia** (❌ RETIRADA en Ronda 6, 2026-07-24 — NO SOSTENIDA a parámetros originales)
- **Enunciado**: Cuando $E_{\\text{root}} > \\theta_{\\text{emerg}} = 0.30$, la fase root $\\phi_{\\text{root}}$ es perturbada direccionalmente hacia el atractor antipodal $\\phi^* + \\pi$.
- **Métrica real (30 seeds × 2000 steps)**: 2237 triggers (3.73% steps); solo 20/2237 (0.9%) con ΔPLV < −0.3; mean ΔPLV = −0.007 ± 0.061 ≈ 0. La correlación $E_{\\text{root}}$ vs error de fase **no** es 0.73 (ese valor era de un borrador previo y se retira).
- **Rediseño**: sube a 30.2% con parámetros ~10× los de diseño, lejos de «la norma».
- **Estado**: Extensión retirada (`EXTENSIONS/C3_Face_Hijacking/`). No es claim del núcleo.
- **Falsación**: Si eventos de alta valencia ($E > 0.30$) producen resets de fase uniformes/bidireccionales."""))

# --- PUNTO 6: 16.1 P6/P7 procedencia ---
reps.append(("T16_1_P8", """#### **P8 — Contracción de Ventana Contextual**
- **Enunciado**: $W(t) = 50 / (1 + 2.0 \\cdot E_{\\text{root}})$ → ventana se contrae bajo valencia.
- **Evidencia sim**: Correlación $W$ vs $E_{\\text{root}}$ = -0.91 (p<0.001).
- **Falsación**: Ventana estable o expansiva bajo alta valencia.""",
"""#### **P8 — Contracción de Ventana Contextual**
- **Enunciado**: $W(t) = 50 / (1 + 2.0 \\cdot E_{\\text{root}})$ → ventana se contrae bajo valencia.
- **Evidencia sim**: Correlación $W$ vs $E_{\\text{root}}$ = -0.91 (p<0.001).
- **Falsación**: Ventana estable o expansiva bajo alta valencia.

> **Procedencia de P6/P7**: Las métricas de herencia (P6: drift padre-hijo 0.098±0.012; P7: XOR 94/100) provienen de simulaciones de extensión con grafo en crecimiento, **no** del código de referencia de la Sección 14, que corre con 4 raíces fijas (N*≈4–5, ver Telemetría 15.4) y no implementa el XOR ni la cascada. P6/P7 son válidas como comportamiento de la dinámica de herencia, pero no se verifican con el núcleo de 4 nodos. La cascada (Ec. 12) en el reference code es un placeholder (`pass`)."""))

applied = []
for label, old, new in reps:
    n = content.count(old)
    if n == 1:
        content = content.replace(old, new, 1)
        applied.append(label)
    else:
        print(f"[FALLO] {label}: encontrados {n} (esperado 1)")

anchor = "## 19. Limitaciones Honestas"
if anchor not in content:
    appendix = r"""

---

## 19. Limitaciones Honestas

Este documento sigue el manifiesto de honestidad epistémica de `NOUS/DSCN-G/DOCUMENTATION/auditoria/claims_falsifiable.md` (principios 1–6: separar VERIFIED/HYPOTHESIZED/SPECULATED; cada claim con criterio de falsificación; declarar limitaciones; no overclaimar; lenguaje preciso; **correr el código y confrontar los números antes de marcar ✅**).

1. **C3 (Phase-Hijacking) retirada.** No sostenida a parámetros de diseño originales (0.9% triggers con ΔPLV<−0.3; mean ΔPLV≈0). La telemetría previa (r=0.73, 94% antipodal) se retira. No es claim del núcleo.
2. **Escala de verificación mixta.** La verificación canónica congelada usó 30 seeds × 2000 steps (Ronda 4, `verification_results_v3.json`). Las cifras a 100 seeds de este documento provienen del reference code de la Sección 14 y son consistentes cualitativamente, pero no son el freeze; la re-corrida a 100 seeds con los datos canónicos está pendiente.
3. **Desajuste de β.** La verificación canónica de T2 usó β=0.20 (alignment 1.0000); el diseño de núcleo usa β=0.10. Ambos convergen; se declara para no confundir cotas.
4. **Grafo fijo en el reference code.** El código de la Sección 14 corre con 4 raíces (N*≈4–5) y no implementa el XOR (abstracción) ni la cascada (Ec. 12 es `pass`). Las predicciones P6/P7 (herencia/XOR) se validan en simulaciones de extensión aparte, no con ese núcleo de 4 nodos.
5. **N_ss* de T1 ≈ 4–5, no 9–10.** El valor 9–10 pertenece al N-back v6 (Claim 6a), no a T1.
6. **T3: doble criterio.** 30/30 (100%) por criterio laxo del código (ω_sim>0.5); 23/30 (76.7%) por criterio estricto del teorema (R≥0.9). Reportar 76.7%.
7. **Sin validación experimental.** EEG/MEG (P2,P3) y fMRI 7T (P4,P5) son future work declarado, no verificado.
8. **Posición sobre consciencia.** DSCN-G es un NCC candidato («correlaciona con consciencia»), no «es consciente». El drug discovery (FATE) es «predice pIC50», no «descubre fármacos».

---

## 20. Referencias

- Nieto, L. B. (2026). *DSCN-G v7.2 — Compendio Teórico*. NOUS/DSCN-G (vault nexus-vault).
- Luconi, L. E. (colaboración conceptual).
- Datos canónicos de verificación: `NOUS/DSCN-G/CORE/VALIDATION/RESULTS/verification_results_v3.json`, `maximality_real_results.json`.
- Auditoría Ronda 4–6 (2026-07-22/24): `NOUS/DSCN-G/DOCUMENTATION/auditoria/`.
- Extensión C3 retirada: `NOUS/DSCN-G/EXTENSIONS/C3_Face_Hijacking/STATUS.md`.
- Kuramoto, Y. (1975). *Self-entrainment of a population of coupled nonlinear oscillators.*
- Robbins, H., Monro, S. (1951). *A stochastic approximation method.*
- Schultz, W., Dayan, P., Montague, P. R. (1997). *A neural substrate of prediction and reward.*
- von Mises, R. (1918). *Über die 'Ganzzahligkeit' der Energielevel...* (distribución von Mises).
"""
    content = content.rstrip() + appendix
    applied.append("appendix_19_20")
else:
    print("[SKIP] secciones 19/20 ya presentes")

with open(PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("Aplicados OK:", applied)
print("FALLARON:", [l for l, _, _ in reps if l not in applied])
print("Lineas:", content.count("\n") + 1, "| Bytes:", len(content.encode("utf-8")))
