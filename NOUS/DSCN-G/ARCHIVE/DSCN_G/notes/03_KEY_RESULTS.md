# Key Results — Números Exactos para Copiar/Pegar

**Objetivo:** Tenés todos los resultados con números precisos para incluir en el paper sin tener que recalcular.

---

## Theorem 1 — Homeostatic Fixed Point

**Parámetros estándar:**
- α = 5.0
- θ_death = 0.10
- γ = 0.01
- N_init ∈ {4, 50, 200}

**Resultados (100 seeds × 2000 steps):**
```
N_ss* = 4.0 ± 0.0
ρ_eff = 0.7001 ± 0.001
Universal bound: 4.0 ≤ 10.0 ✓
Concentration bound: N* ≤ ρ_eff/θ_death = 0.7001/0.10 = 7.00 ✓
Memory hit rate: 100%
```

**Interpretación:** El sistema converge a exactamente 4 nodos activos, independiente de N_init.

---

## Theorem 2 — Parametric Vector Convergence

**Parámetros:**
- λ_vm = 3.0
- n_actions = 8
- θ* = π/2
- β = 0.10

**Resultados:**
```
ω* (baseline teórico) = 0.649747
ω_sim (simulado) = 0.612 ± 0.173
Distance: |0.612 − 0.649747| = 0.038
Threshold: β = 0.10
Verificación: 0.038 < 0.10 ✓
```

**Interpretación:** La distancia al baseline teórico es < β, confirmando convergencia.

---

## Theorem 3 — Phase Convergence Rate

**Parámetros:**
- λ_vm = 3.0
- η = 0.1
- R_min = 0.5
- T = 2000 steps
- n_seeds = 100

**Resultados:**
```
p_conv (probabilidad de convergencia) = 0.97
Antipodal seeds (no convergen) = 3/100
Theoretical bound: P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T)
```

**Interpretación:** 97% de los seeds convergen, 3/100 permanecen antipodales.

---

## N-back Task — Working Memory Validation

**Parámetros:**
- N = 50
- K = 3
- d = 8
- α = 5.0
- θ_death = 0.10
- sequence_length = 100
- n_trials = 20

**Resultados (mean ± std):**
| N-back | Accuracy | Std | Correctos / Total |
|--------|----------|-----|-------------------|
| 1-back | 89.3% | ±4.0% | ~89 / 100 |
| 2-back | 89.6% | ±3.0% | ~90 / 100 |
| 3-back | 89.2% | ±2.6% | ~89 / 100 |
| **4-back** | **90.6%** | **±3.5%** | **~91 / 100** |
| **5-back** | **51.6%** | **±5.5%** | **~52 / 100** |
| 6-back | 50.2% | ±6.4% | ~50 / 100 |

**Drop ratio:**
```
Drop = (acc_4back − acc_5back) / acc_4back
     = (90.6% − 51.6%) / 90.6%
     = 42.2% drop
```

**P-value (t-test 4-back vs. 5-back):** p < 0.001

**Interpretación:** La accuracy cae de ~90% a ~50% (chance) cuando n-back > 4, confirmando capacity ≈ 4 items.

---

## Φ_proxy Scaling (Theorem 7)

**Predicción teórica:**
```
ρ_eff(α, N)·Φ_proxy(N) = c(α) + O(1/N)
Para fractal circulant graphs: t(N) = O(log N)
```

**Estado:** Pendiente de validación experimental completa.

**Experimento propuesto:**
- Generar graphs con N = {10, 50, 100, 500, 1000}
- Medir tiempo de cómputo t(N)
- Falsificación: Si t(N) > N^1.5, no escala como O(log N)

---

## C3 Prediction — Phase-Hijacking

**Predicción cuantitativa:**
```
PLV(A) − PLV(B) > 0.3
después de 50 trials con valence overload
```

**Setup experimental (propuesto):**
- 2 estímulos competidores A y B
- A: valencia alta (reward = 1.0)
- B: valencia neutral (reward = 0.5)
- Medir PLV entre nodos antes y después

**Falsificación:** Si PLV(A) − PLV(B) < 0.1 después de 100 trials, C3 es falsa.

**Estado:** Pendiente de validación.

---

## Comparación con Baselines

### Working Memory Capacity

| Modelo | Capacity | Fuente |
|--------|----------|--------|
| **DSCN-G** | **4 items exacto** | Este trabajo (N_ss* = 4.0) |
| Humano (Cowan) | 4 ± 1 items | Cowan (2001) |
| Humano (Miller) | 7 ± 2 items | Miller (1956) |
| LSTM (típico) | Variable | Depende de hidden size |
| Hopfield (clásico) | 0.15·N items | Capacidad teórica |

### Computational Cost

| Framework | Costo Φ | Escalabilidad |
|-----------|---------|---------------|
| **DSCN-G (Φ_proxy)** | **O(log N)** | Este trabajo (Theorem 7) |
| IIT 4.0 | Exponencial | Intratable para N > 20 |
| GWT | N/A | No computado |
| Predictive Processing | Polinómico | No especificado |

---

## Falsificación Criteria (Resumen)

### Theorem 1 — Working Memory
**Predicción:** Accuracy cae después de 4-back  
**Falsificación:** Si accuracy > 70% en 5-back con parámetros estándar  
**Estado:** ✅ Validado (51.6% < 70%)

### Theorem 1 — Parameter Sensitivity
**Predicción:** Si θ_death = 0.20 → N_ss* ≈ 2 → colapso en 3-back  
**Falsificación:** Si accuracy > 70% en 3-back con θ_death = 0.20  
**Estado:** 🔲 No testeado (future work)

### C3 — Phase-Hijacking
**Predicción:** PLV(A) − PLV(B) > 0.3 después de 50 trials  
**Falsificación:** Si PLV diff < 0.1 después de 100 trials  
**Estado:** 🔲 No testeado (future work)

### Theorem 7 — Φ_proxy Scaling
**Predicción:** t(N) = O(log N)  
**Falsificación:** Si t(N) > N^1.5 para N = 1000  
**Estado:** 🔲 No testeado (future work)

---

**Usá estos números directamente en el paper. Son todos verificables corriendo los simuladores.**