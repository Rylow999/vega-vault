# Estructura del Paper DSCN-G

**Target:** *Neural Computation* (MIT Press) o *Cognitive Systems Research* (Elsevier)  
**Longitud objetivo:** 8000-10000 palabras (sin references)  
**Figuras:** 2-3 mínimo

---

## Estructura Principal

### Abstract (~200-250 palabras)

**Estructura:**
1. **Problema:** Frameworks actuales (IIT, GWT) tienen limitaciones (intratabilidad, falta predicciones)
2. **Solución:** Presentamos DSCN-G (arquitectura unificada)
3. **Método:** 3 teoremas formales + verificación computacional (200k evaluaciones)
4. **Resultados clave:**
   - Theorem 1: N_ss* = 4.0 ± 0.0 (working memory capacity)
   - N-back validation: 89.1% → 51.6% drop (4→5 back)
   - Theorem 2-3: Convergencia verificada
5. **Contribución unique:** Primer framework con predicciones falsificables + simulador open-source
6. **Claim ontológico:** NCC (no resolvemos hard problem)

**Ver:** `02_ABSTRACT_DRAFT.md` para borrador completo.

---

### 1. Introduction (~1000-1200 palabras)

**1.1 Problema (2 párrafos)**
- IIT: cuantitativo pero intratable (Φ exponencial)
- GWT: descriptivo pero sin especificidad matemática
- Predictive Processing: unificador pero sin predicciones direccionales
- **Gap:** Falta framework con (a) prediccciones falsificables, (b) simulador open-source

**1.2 DSCN-G en una página (2 párrafos)**
- Unifica: TD-learning + Kuramoto + plasticidad + valence
- 3 teoremas formales verificados
- **Claim fuerte:** Working memory capacity ≈ 4 items (Cowan 2001)

**1.3 Ontological Position (1 párrafo)**
- No resolvemos hard problem (Chalmers 1995)
- Claim: NCC más completo formalmente
- Agnósticos sobre experiencia subjetiva

**1.4 Contributions (bullet points)**
1. 3 teoremas + verificación computacional
2. Predicción C3 (phase-hijacking) falsificable
3. Φ_proxy scaling O(log N)
4. Simulador open-source

**1.5 Roadmap (1 párrafo)**
- Section 2: Computational foundations (Eqs. 1-7)
- Section 3: Formal theorems + verification
- Section 4: Working memory validation (N-back)
- Section 5: Discussion (C3, Φ_proxy, future work)
- Section 6: Conclusion

---

### 2. Computational Foundations (~1500-1800 palabras)

**2.1 Graph Structure (300 palabras)**
- Directed hierarchical graph G = (N, E)
- Depth d(n), root/intermediate/leaf nodes
- Global state S(t) = (ω, φ, V, chains)

**2.2 State Vectors + TD-Learning (Eq. 1) (300 palabras)**
- ω_i(t+1) = (1−β)·ω_i(t) + β·o(t)·R(t)·ê_R
- Stochastic gradient, Robbins-Monro conditions
- Baseline ω*(λ_vm, n_actions, θ*) computable

**2.3 Information Chains (Eq. 2) (200 palabras)**
- P(m|n) ∝ exp(−α·‖ω_m − ω_n‖)
- K independent chains, XOR integration
- Analogía: coincidence detection en dendritas

**2.4 Phase Dynamics (Eqs. 3-4) (400 palabras)**
- Kuramoto bounded: φ_i(t+1) = [φ_i + η·R_i·sign(o)·sin(θ_a − φ_i)] mod 2π
- Von Mises action selection: P(a|φ)
- Bounded relevance R_i (Definition 1)

**2.5 Autopoiesis (Eqs. 5-6) (300 palabras)**
- Vitality: V_i(t+1) = V_i·e^(−γ) + A_i·(1 − e^(−γ))
- Pruning: V_i < θ_death → eliminar
- Valence: E_i = max(0, A_i − V_i)·κ

**2.6 Wave Interference (Eq. 7) (200 palabras)**
- I_i = ‖ω_i‖·cos(φ_i − φ_root)
- Cognitive relevance threshold θ_interf = 0.70
- Attention sin mecanismo externo

**Figura 2:** Architecture diagram con todas las ecuaciones anotadas.

---

### 3. Formal Theorems (~1800-2000 palabras)

**Theorem 1 — Homeostatic Fixed Point (500 palabras)**
- Statement: N_ss* = max{n : ρ_eff ≥ n·θ_death²}
- Properties: (i) universal bound ≤ 1/θ_death, (ii) concentration, (iii) uniqueness
- Proof sketch
- **Verification:** N_ss* = 4.0 ± 0.0 (α=5.0, θ_death=0.10)
- **Trailer:** Corresponde a Cowan (2001) 4±1 items

**Theorem 2 — Parametric Vector Convergence (500 palabras)**
- Statement: ‖ω − ω*(λ_vm, n_actions, θ*)‖ ≤ O(β)
- Proof: Stochastic contraction mapping (Robbins-Siegmund)
- **Verification:** ‖ω − ω*‖ = 0.038 < β = 0.10
- Parametric sensitivity: ω* varía con λ_vm

**Theorem 3 — Phase Convergence Rate (500 palabras)**
- Statement: P(antipodal) ≤ exp(−c·λ_vm·η·R_min·T)
- Proof: Concentration bound
- **Verification:** p_conv = 0.97 (3/100 antipodal seeds)

**Theorem 7 — Φ_proxy Scaling (300 palabras)**
- Statement: ρ_eff(α, N)·Φ_proxy(N) = c(α) + O(1/N)
- Proof sketch (fractal circulant graphs)
- **Verificación futura:** t(N) = O(log N)

---

### 4. Working Memory Validation (~1200-1500 palabras) ⭐ SECCIÓN CLAVE

**4.1 Motivación (150 palabras)**
- Theorem 1 predice N_ss* ≈ 4
- ¿Se traduce en working memory capacity?
- Predicción: accuracy cae en n > 4

**4.2 Methods (300 palabras)**
- Task: N-back (n = 1-6)
- Simulator: dscn_g_simulator_wm.py
- Parámetros: N=50, K=3, α=5.0, θ_death=0.10
- Trials: 20 independientes, sequence_length=100
- Métrica: Accuracy (% correct)

**4.3 Results (400 palabras)**
- **Tabla:** Accuracy vs. n-back
- **Figura 1:** Line plot con drop en 4→5
- 1-back: 89.3%, 2-back: 89.6%, 3-back: 89.2%, 4-back: 90.6%
- **5-back: 51.6% (chance)**, 6-back: 50.2%
- **Drop:** 42.2% (p < 0.001)

**4.4 Comparison with Human Data (200 palabras)**
- Cowan (2001): 4±1 items
- Miller (1956): 7±2 items (over-estimado)
- **DSCN-G:** 4 items exacto (emerge de homeostasis)

**4.5 Falsification Criteria (150 palabras)**
- Si θ_death = 0.20 → N_ss* ≈ 2 → debería colapsar en 3-back
- Si θ_death = 0.05 → N_ss* ≈ 8 → debería colapsar en 9-back
- Experimento propuesto: variar θ_death sistemáticamente

---

### 5. Discussion (~1200-1500 palabras)

**5.1 Comparison with Existing Frameworks (400 palabras)**
- IIT: intratable, no predice capacity
- GWT: descriptivo, sin matemática
- Predictive Processing: muy general
- **DSCN-G:** predicciones falsificables + simulador

**5.2 C3 Prediction: Phase-Hijacking (300 palabras)**
- Claim: PLV(A) − PLV(B) > 0.3 bajo valence overload
- Sugerencia: testear con EEG (gamma-band PLV en S1-aPFC)
- **Falsificación:** Si PLV diff < 0.1, C3 es falsa
- Status: future work

**5.3 Φ_proxy Scaling (200 palabras)**
- Theorem 7: O(log N) para fractal circulant graphs
- Ventaja: O(K) computable vs. exponencial de IIT
- **Falsificación:** Si t(N) > N^1.5, no escala
- Status: future work

**5.4 Limitations (200 palabras)**
- No validado en datos experimentales (EEG/fMRI)
- working memory model es simplificado (phase patterns)
- Faltan comparaciones con baselines (LSTM, Hopfield)

**5.5 Future Work (200 palabras)**
- EEG/fMRI validation de C3
- Large-scale simulations (N=1000+)
- Application a drug discovery (FATE v6 connection)
- Baseline comparisons

---

### 6. Conclusion (~300-400 palabras)

**Párrafo 1: Resume claims principales**
- 3 teoremas verificados
- Working memory capacity ≈ 4 items (validado en N-back)
- Simulador open-source

**Párrafo 2: Framing como NCC**
- No resolvemos hard problem
- Claim: NCC más completo formalmente disponible

**Párrafo 3:Impacto**
- Primer framework con predicciones falsificables específicas
- Cualquiera puede bajar el simulador y validar

**Párrafo 4: Cierra con "Per Aspera, Ad Astra"**

---

## References

**Cantidad objetivo:** 40-50 referencias  
**Gestión:** Usar Zotero o BibTeX (`REFERENCES.bib`)

**Ver:** `REFERENCES.bib` para lista completa ya armada.

---

## Supplementary Materials

**Online-only:**
- `dscn_g_simulator.py`: Código fuente
- `dscn_g_simulator_wm.py`: Working memory simulation
- `VALIDATION_PROTOCOL_COMPUTATIONAL.md`: Protocolo
- `results/`: CSVs con datos brutos

**Link al repo:** https://github.com/Rylow999/nexus-vault/tree/main/papers/DSCN_G

---

**Timeline:** 5-7 días para primer draft completo  
**Iteraciones:** 2-3 rondas de feedback

💪 **Vamos con todo!**