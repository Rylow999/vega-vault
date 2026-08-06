# Protocolo de Validación Computacional para DSCN-G

**Motivo:** Validar DSCN-G sin necesidad de EEG/fMRI experimental, mediante predicciones computacionales falsificables y verificables.

**Fecha:** 2026-07-19  
**Autor:** Luciano Nieto

---

## Problema Actual

DSCN-G tiene:
- ✅ 3 teoremas formales verificados (homeostasis, convergencia, phase locking)
- ✅ Predicción C3 (Phase-Hijacking)
- ✅ Proxy de Φ_IIT (Theorem 7)

**Pero falta:**
- ❌ Validación en tareas cognitivas **reales** (no solo matemáticas)
- ❌ Comparación directa con modelos baseline (LSTM, Transformer, GNN)
- ❌ Predicciones cuantitativas específicas que puedan falsificarse

---

## Protocolo Propuesto: 4 Niveles de Validación

### Nivel 1: Validación Interna (Ya hecho ✅)

**Qué es:** Verificar que los teoremas se cumplen en simulación.

**Estado:**
- ✅ Theorem 1: N_ss* = 4.0 ± 0.0 (100 seeds)
- ✅ Theorem 2: ‖ω − ω*‖ ≤ 0.038 < β = 0.10
- ✅ Theorem 3: P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T), p_conv = 0.97

**Conclusión:** DSCN-G es **matemáticamente consistente**.

---

### Nivel 2: Validación en Tareas Sintéticas (Por hacer 🔲)

**Qué es:** Aplicar DSCN-G a tareas cognitivas sintéticas con ground truth conocido.

**Tareas propuestas:**

#### 2.1 Working Memory Task (N-back)

**Setup:**
- Input: Secuencia de estímulos S = [s₁, s₂, ..., s_T]
- Tarea: Detectar cuando s_t = s_{t-n} (n-back)
- Métrica: Accuracy % (chance = 10% para 10 estímulos)

**Predicción DSCN-G:**
- N_ss* ≈ 4 (por Theorem 1) → **mejor performance en 2-back y 3-back**
- Performance cae drásticamente en 4-back (límite de capacidad)
- **Falsificación:** Si accuracy > 80% en 4-back, el modelo está mal

**Baseline para comparar:**
- LSTM: ~85% en 3-back, ~60% en 4-back
- Transformer: ~90% en 3-back, ~75% en 4-back
- **DSCN-G debería:** ~85% en 3-back, ~50% en 4-back (por límite de 4 items)

#### 2.2 Decision-Making Task (Multi-Armed Bandit)

**Setup:**
- K = 8 acciones, cada una con reward probability p_k
- Agente debe maximizar reward acumulado
- Métricas: Regret acumulado, % de acciones óptimas

**Predicción DSCN-G:**
- Phase locking (Theorem 3) → converge a acción óptima en ~100-200 trials
- Valence signal (E_i) → detecta cambios en p_k (reversal learning)
- **Falsificación:** Si regret > UCB1 después de 500 trials, el modelo falla

**Baseline:**
- UCB1: Regret ~ O(log T)
- Thompson Sampling: Regret ~ O(√K·log T)
- **DSCN-G debería:** Regret similar a Thompson (~√K·log T)

#### 2.3 Pattern Completion (Hopfield-style)

**Setup:**
- Memorizar M patrones binarios {ξ^μ} de N bits
- Input: Patrón con ruido (10-50% bits flippeados)
- Output: Patrón recuperado
- Métrica: Accuracy de recuperación vs. ruido

**Predicción DSCN-G:**
- Capacidad: M ≈ 0.15·N (similar a Hopfield, por N_ss* ≈ 4)
- Recuperación en O(log N) pasos (por resonancia armónica)
- **Falsificación:** Si capacidad < 0.10·N, el modelo no escala bien

**Baseline:**
- Hopfield clásico: M ≈ 0.15·N
- Modern Hopfield (Krotov & Hopfield, 2016): M ≈ 0.50·N
- **DSCN-G debería:** M ≈ 0.15-0.25·N (intermedio)

---

### Nivel 3: Predictions Cuantitativas Específicas (Por hacer 🔲)

**Qué es:** Hacer 3-5 predicciones numéricas específicas que puedan falsificarse.

#### Predicción 1: Capacidad de Working Memory

**Claim:** "DSCN-G tiene capacidad máxima de 4 ± 1 items en working memory."

**Test:**
- Correr N-back task con n = 1, 2, 3, 4, 5, 6
- Medir accuracy para cada n
- **Predicción específica:**
  - 1-back: 95-100%
  - 2-back: 85-95%
  - 3-back: 70-85%
  - 4-back: 40-60% (drop drástico)
  - 5-back: 20-40%
  - 6-back: 10-25% (chance)

**Falsificación:** Si accuracy en 4-back > 70%, la predicción es falsa.

#### Predicción 2: Phase-Hijacking (C3) bajo Valence Overload

**Claim:** "Bajo valence overload (E_i > threshold), las fases se perturban direccionalmente hacia el estímulo sobreactivante."

**Test:**
- Crear escenario con 2 estímulos competidores A y B
- A tiene valencia alta (reward = 1.0), B tiene valencia neutral (reward = 0.5)
- Medir PLV (Phase Locking Value) entre nodos antes y después de valence overload

**Predicción específica:**
- PLV(A) − PLV(B) > 0.3 después de 50 trials con valence overload
- Dirección de perturbación: Δφ → φ_A (no aleatorio)

**Falsificación:** Si PLV(A) − PLV(B) < 0.1 después de 100 trials, C3 es falsa.

#### Predicción 3: Scaling Law para Φ_proxy

**Claim:** "Φ_proxy escala como O(K) para fractal circulant graphs."

**Test:**
-Generar graphs con N = {10, 50, 100, 500, 1000} nodos
- Medir tiempo de cómputo de Φ_proxy vs. N
- **Predicción específica:**
  - t(N) = c · log(N) + O(1) para K fijo
  - t(N) = c · K · log(N) para K variable

**Falsificación:** Si t(N) > N^1.5 para N=1000, el scaling no es O(log N).

---

### Nivel 4: Comparación con Modelos Baseline (Por hacer 🔲)

**Qué es:** Comparar DSCN-G contra modelos establecidos en las mismas tareas.

**Baselines propuestos:**

| Tarea | Baseline 1 | Baseline 2 | Baseline 3 |
|-------|-----------|-----------|-----------|
| N-back | LSTM (128 units) | GRU (128 units) | Transformer (2 layers) |
| Bandit | UCB1 | Thompson Sampling | UCB2 |
| Pattern Completion | Hopfield clásico | Modern Hopfield | GNN (GraphSAGE) |

**Métricas de comparación:**
1. **Accuracy/Performance:** ¿DSCN-G es competitivo?
2. **Sample Efficiency:** ¿Cuántos trials necesita para converger?
3. **Interpretability:** ¿Se puede entender por qué tomó esa decisión?
4. **Scalability:** ¿Cómo escala con N?

**Criterio de éxito:**
- DSCN-G no necesita superar a todos los baselines en todo
- Pero debería ser **mejor en al menos 2 aspectos**:
  - Ej: Sample efficiency + interpretability
  - Ej: Scalability + phase-hijacking (único de DSCN-G)

---

## Protocolo de Implementación

### Paso 1: Simulador DSCN-G (2-3 semanas)

**Qué hacer:**
- Crear `dscn_g_simulator.py` con todas las ecuaciones (1-7)
- Implementar:
  - `step()`: Un paso de simulación
  - `run_episode()`: Ejecutar una tarea completa
  - `compute_phi_proxy()`: Calcular Φ_proxy
  - `compute_plv()`: Calcular Phase Locking Value

**Código mínimo:**
```python
class DSCN_G:
    def __init__(self, N=50, K=3, alpha=5.0, beta=0.01, ...):
        # Inicializar nodos, edges, parameters
        pass
    
    def step(self, stimulus):
        # Eq. 1: Update vectors
        # Eq. 2: Chain transitions
        # Eq. 3-4: Phase dynamics + action selection
        # Eq. 5-6: Vitality pruning + valence
        # Eq. 7: Wave interference
        return action, reward
    
    def run_nback(self, n, sequence):
        # Implementar N-back task
        pass
    
    def run_bandit(self, probs, n_trials):
        # Implementar multi-armed bandit
        pass
```

### Paso 2: Correr Experimentos (1-2 semanas)

**Qué hacer:**
- Para cada tarea (N-back, Bandit, Pattern Completion):
  - Correr 100 seeds independientes
  - Variar parámetros clave (λ_vm, α, K)
  - Guardar resultados en CSV/JSON

**Output esperado:**
- `results/nback_accuracy_vs_n.csv`
- `results/bandit_regret_vs_trials.csv`
- `results/pattern_completion_accuracy_vs_noise.csv`

### Paso 3: Análisis y Visualización (1 semana)

**Qué hacer:**
- Plotear curvas de aprendizaje
- Comparar con baselines
- Calcular estadísticas (mean ± std, p-values)

**Figuras clave:**
1. N-back: Accuracy vs. n (con línea en n=4 marcando el drop)
2. Bandit: Regret vs. trials (DSCN-G vs. UCB1 vs. Thompson)
3. Pattern completion: Accuracy vs. noise level
4. Phase-hijacking: PLV(A) − PLV(B) vs. trials

### Paso 4: Redacción del Paper (2-3 semanas)

**Estructura:**
1. Intro: DSCN-G + motivación
2. Methods: Ecuaciones + tareas
3. Results: Nivel 2 + Nivel 3 (todos los experimentos)
4. Discussion: ¿Qué predicen los resultados?
5. Conclusion: Claims validados vs. falsificados

---

## Timeline Estimado

| Semana | Tarea | Deliverable |
|--------|-------|-------------|
| 1-2 | Simulador DSCN-G | `dscn_g_simulator.py` funcional |
| 3-4 | Experimentos Nivel 2 | CSVs con resultados |
| 5 | Análisis y plots | 4-6 figuras clave |
| 6-8 | Redacción paper | Draft completo |

**Total:** 6-8 semanas para tener un paper completo de DSCN-G.

---

## Criterios de Éxito (Go/No-Go)

### ✅ Go (publicar) si:

1. **Working Memory:** Accuracy en 3-back ≥ 80%, drop en 4-back < 60%
2. **Bandit:** Regret después de 500 trials ≤ 1.5× Thompson Sampling
3. **Pattern Completion:** Capacidad ≥ 0.15·N con 10% noise
4. **Phase-Hijacking:** PLV(A) − PLV(B) > 0.2 después de 50 trials

### ❌ No-Go (revisar modelo) si:

1. **Working Memory:** Accuracy en 3-back < 60% (no aprende)
2. **Bandit:** Regret >> UCB1 (peor que random)
3. **Pattern Completion:** Capacidad < 0.10·N (no escala)
4. **Phase-Hijacking:** PLV(A) − PLV(B) ≈ 0 (sin efecto)

---

## Claim Final Validable

**Si todos los criterios Go se cumplen:**

> "DSCN-G es un modelo computacional de cognición que:
> (1) respeta límites biológicos (working memory ~4 items),
> (2) aprende eficientemente en tasks de decisión (regret similar a Thompson Sampling),
> (3) generaliza en tasks de pattern completion (capacidad ~0.15·N),
> (4) predice un fenómeno nuevo (phase-hijacking) que puede testearse experimentalmente con EEG/fMRI.
>
> **Falsificación:** Si alguno de estos 4 claims falla en simulación, el modelo debe revisarse."

---

**Responsable:** Luciano Nieto  
**Próximo paso:** Empezar `dscn_g_simulator.py` esta semana.