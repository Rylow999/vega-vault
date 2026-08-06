# Fase 2 — Inferencia Simbólica + Duda (Primer de Diseño)

## Componentes de Fase 2

### 1. Abducción XOR (exp_SGM_0004 → exp_SGM_0005)
- **Base**: Generative XOR (Ec. 8 del spec SGM v1.4)
- **Brute-force**: O(n²) — prueba todos los pares (A,B) y calcula cos(ω_XOR, ω_query)
- **PPR-guided**: O(K²) donde K << n — PPR desde ω_query encuentra top-K candidatos relevantes, luego XOR solo entre ellos
- **Trampa**: un distractor con cos(ω_distractor, ω_query) > cos(ω_n1, ω_query) pero sin salida (callejón)
  - Resonancia local (argmax 1 paso) → elige distractor → callejón → FALLA
  - PPR → fluye por la cadena → se acumula en target → PASS

### 2. Duda vs Contradicción (T-INF-04, T-INF-05)
- **Duda** (check_stagnation): "no avanzo, sin evidencia en contra"
  - Trigger: novelty < 0.30 (pocos nodos únicos en ventana) Y W(t) ya chico
  - Respuesta escalonada: (1) aflojar λ,α → (2) semilla nueva via HNSW → (3) marcar INCONCLUSA
- **Contradicción** (verify_contradiction): "me lastimé, evidencia en contra"
  - Trigger: Σ E_i en trayectoria > θ_refut (2.0)
  - Respuesta: marcar CONTRADICTORIA + relaunch con φ perturbado (φ+π) + cooldown 5 ticks
- **Clave**: NO se cruzan. Una es "no avanzo", la otra es "me lastimé".

### 3. PPR Routing (exp_SGM_0004)
- **Algoritmo**: Personalized PageRank con omega_query como semilla y Ec.2 como edge weight
- **Converge en ~100 iters** para grafos de miles de nodos
- **α (restart prob)**: 0.15 — 15% de volver a la semilla cada paso
- **No es similarity-NN**: es un random walk con restart, compatible con el grafo

### 4. Decaimiento de hit_count (idea EWC)
- hit_count actual no tiene decaimiento — un nodo inactivo desde hace 1000 ticks sigue con hit_count alto
- Agregar: hit_count(t) = hit_count(t-1) * exp(-γ_decay) + activación_actual
- Análogo a la "rigidez" de Fisher Information de EWC, pero más barato

### 5. Contradicción (exp_SGM_0014, T-INF-02) — IMPLEMENTADO 2026-08-02
- `verify_contradiction()`: Σ E_n en trayectoria > θ_refut (2.0) → marca CONTRADICTORIA, relanza
  cadena desde raíz con perturbación de fase (φ_root → φ* + π), cooldown 5 ticks.
- Dolor DEBE disparar DURANTE la trayectoria (online), no post-hoc (lección v0.6b/v0.9a del LE:
  dolor post-hoc no mejora nada). Evidencia empírica de dolor interno: v0.9c (G: 0.0→1.0).
- Negative controls: cadena con dolor bajo (1.0) y dolor cero NO disparan. PASS.
- Eq.6: E_i = max(0, A_i - V_i)*κappa. Eq.8: W(t) = W_base/(1 + κ_W·E_root).

### 6. Loop unificado (exp_SGM_0015, T-INF-05) — IMPLEMENTADO 2026-08-02
- Junta abducción (afinidad Eq.2) + duda (§2.3.2) + contradicción (§2.3.1) en un loop.
- Tres estados finales bien tipados, sin confusión:
  - A resuelve → DETERMINADO (llegada al target)
  - B dolor > 2.0 → CONTRADICTORIA (relanza φ+π)
  - C estancado (novelty baja + ventana contraída, SIN dolor) → INCONCLUSA vía handle_doubt escalonado
- **LECCIÓN DE HONESTIDAD (crítica):** el escenario C debe disparar de VERDAD handle_doubt hasta
  doubt_count≥3 (igual que 0013). Si dudás por timeout (doubt_count=0) el test no probó la duda.
  Para forzarlo en el test: trampa de pocos nodos (ω clusterizados) + ventana contraída por
  presión (window_pressure=0.3, NO por dolor — §2.3.2 dice "sin dolor asociado").
- Fase 2 QUEDA CERRADA con 0015. Siguiente: Fase 3 (SensorBridge).