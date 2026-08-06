# DSCN-G v3 — Estado del Paper y Próximos Pasos

**Fecha:** 2026-07-20  
**Último commit:** `a7ff5b1`  
**Estado:** ✅ Verificación completa — Listo para escritura del draft

---

## ✅ Lo que está COMPLETADO y VERIFICADO

### 1. Arquitectura v3 (verify_dscng_v2.py)

| Componente | Implementación | Verificación |
|------------|----------------|--------------|
| **T1** (Homeostatic Fixed Point) | Pruning por vitalidad | N_ss* = 4 (α=5, θ_death=0.12) ✓ |
| **T2** (ω Alignment) | Broadcast neuromodulatorio | alignment = 1.0000 ✓ |
| **T3** (Phase Consensus) | Kuramoto all-to-all | R = 0.90 (η=0.025) ✓ |
| **C3** (Phase Hijacking) | η_kura dinámico (0.005→0.025) | ΔR = +0.46 ✓ |

**Claim clave:** `eta_kura` dinámico permite que T3 y C3 coexistan (análogoa atención neuromodulatoria).

---

### 2. N-back Validation (nback_v4_capacity.py)

**Resultado principal:**
- WM Capacity = N_ss* = **4 items**
- Accuracy 3-back: **59.3%**
- Accuracy 4-back: **49.5%** (chance)
- **Drop 3→4: 9.8%**

**Comparación con humanos:**
- Cowan (2001): 4 ± 1 items
- DSCN-G v3: 4 items (emergente, no hardcoded)

**Baseline comparison (baseline_comparison.py):**

| n-back | Random | Hopfield | DSCN-G v3 | Ideal |
|--------|--------|----------|-----------|-------|
| 1 | 50% | 59.5% | 58.1% | 100% |
| 2 | 50% | 59.0% | 59.2% | 100% |
| 3 | 50% | 59.3% | 59.3% | 100% |
| 4 | 50% | 49.7% | 49.5% ← drop | 100% |
| 5 | 50% | 50.0% | 49.5% | 100% |

---

## 📝 Lo que FALTA escribir (Paper Draft)

### Secciones Pendientes

1. **Abstract** (~200 palabras)
   - Problema: IIT/GWT limitaciones
   - Solución: DSCN-G unifica TD-learning + Kuramoto + homeostasis
   - Resultados: 4 teoremas verificados, capacity = 4 items
   - Claim: Primer framework con predicciones falsificables + simulador open-source

2. **Introduction** (~1000 palabras)
   - 1.1: Limitaciones de frameworks actuales (IIT: intratable, GWT: descriptivo)
   - 1.2: DSCN-G en una página (arquitectura unificada)
   - 1.3: Ontological position (NCC, no hard problem)
   - 1.4: Contributions (bullet points)
   - 1.5: Roadmap

3. **Computational Foundations** (~1500 palabras)
   - 2.1: Graph structure
   - 2.2: TD-learning (Eq.1)
   - 2.3: Information chains (Eq.2)
   - 2.4: Phase dynamics (Eqs.3-4) + **Kuramoto all-to-all** (nuevo v3)
   - 2.5: Autopoiesis (Eqs.5-6)
   - 2.6: Wave interference (Eq.7)
   - 2.7: **Dynamic eta_kura** (nuevo v3 — neuromodulatory attention)
   - Figura 1: Architecture diagram

4. **Formal Theorems** (~1500 palabras)
   - Theorem 1: Homeostatic fixed point + maximality (verificado)
   - Theorem 2: ω alignment convergence (verificado v3)
   - Theorem 3: Phase consensus (verificado v3, η=0.025)
   - Theorem 4: Dynamic eta_kura enables T3+C3 coexistence (nuevo)
   - C3 Conjecture: Phase hijacking (verificado, ΔR = +0.46)

5. **Working Memory Validation** (~800 palabras)
   - Methods: N-back task protocol
   - Results: capacity = 4 items, drop 3→4 = 9.8%
   - Comparison: Cowan (2001), Hopfield network
   - Figura 2: Accuracy vs. n-back (DSCN-G vs. Hopfield vs. random)

6. **Discussion** (~1000 palabras)
   - 6.1: Comparison with IIT/GWT/PP
   - 6.2: C3 as falsifiable prediction (EEG: gamma PLV increase during overload)
   - 6.3: Limitations (simplified N-back, no experimental validation yet)
   - 6.4: Future work (EEG/fMRI, large-scale sims, drug discovery connection)

7. **Conclusion** (~300 palabras)
   - Claims principales
   - Framing como NCC
   - Impacto: falsificable + open-source

8. **References** (~40-50 items)
   - Cowan (2001), Miller (1956)
   - Kuramoto (1984), Acebrón et al. (2005)
   - Tononi (2004), Baars (1988), Friston (2010)
   - Dehaene & Changeux (GNW ignition)
   - Sutton & Barto (RL)

---

## 🎯 Próximos Pasos (Orden de Prioridad)

### Alta Prioridad (bloqueantes)

1. **Escribir Abstract + Introduction** — Define el framing del paper
2. **Escribir Results (N-back)** — claim central
3. **Generar Figura 2** — accuracy vs. n-back plot

### Media Prioridad (fortalecen)

4. **Escribir Computational Foundations** — detalles técnicos
5. **Escribir Theorems** — formalismo
6. **Generar Figura 1** — architecture diagram

### Baja Prioridad (nice-to-have)

7. **Escribir Discussion** — depende de reviewer feedback
8. **Φ_proxy scaling experiment** — Theorem 7 pendiente
9. **EEG prediction details** — protocol específico

---

## 📁 Archivos Clave

### Código (completado)
- `verify_dscng_v2.py` — simulador v3
- `nback_v4_capacity.py` — N-back task
- `baseline_comparison.py` — comparativas

### Datos (generados)
- `nback_paper_ready.json` — resultados N-back
- `baseline_comparison.json` — baselines

### Documentación (pendiente)
- `main.tex` o `paper.md` — draft completo
- `figures/` — arquitectura + N-back plot

---

## 🧠 Claims Honestos (para el paper)

### Lo que podemos claimar (verificado)
- ✅ WM capacity ≈ 4 items (N_ss* = 4)
- ✅ Drop en 3→4 back (9.8%)
- ✅ Comparable a Cowan (2001) "4±1"
- ✅ Mecanismo emergente (homeostatic pruning)
- ✅ T2 + T3 + C3 verificados simultáneamente (con η dinámico)

### Lo que NO podemos claimar (aún)
- ❌ "DSCN-G resuelve el hard problem" (explícitamente no)
- ❌ "Supera a todos los modelos" (solo comparamos con Hopfield)
- ❌ Validación experimental (EEG/fMRI) — future work
- ❌ Φ_proxy scaling O(log N) — pendiente

---

## 💡 Notas para la Escritura

### Estilo
- **Honestidad epistémica:** Separar VERIFIED de HYPOTHESIZED de SPECULATED
- **Falsificabilidad:** Cada claim debe tener criterio de falsificación
- **Open-source:** Simulador disponible en GitHub (nexus-vault)

### Analogías Biológicas (úsar con cuidado)
- **η_kura dinámico:** Análogo a acetilcolina/noradrenalina (atención/arousal)
- **Hijacking (C3):** Análogo a epilepsia focal / GNW ignition
- **Homeostasis:** Análogo a pruning sináptico + vitalidad neuronal

### Evitar
- "Descubre fármacos" → "Encuentra análogos con pIC50 predicho X"
- "Es consciente" → "NCC formalmente completo"
- "Demuestra" → "Verifica computacionalmente"

---

## 🚀 Checklist Final

- [ ] Abstract
- [ ] Introduction
- [ ] Computational Foundations
- [ ] Formal Theorems
- [ ] Working Memory Results
- [ ] Discussion
- [ ] Conclusion
- [ ] References
- [ ] Figura 1 (arquitectura)
- [ ] Figura 2 (N-back accuracy)
- [ ] Supplementary material (código, datos)

---

**Próximo paso inmediato:** Escribir Abstract + Introduction (define el tono del paper).

**Good luck! 🚀**

*Per Aspera, Ad Astra.*