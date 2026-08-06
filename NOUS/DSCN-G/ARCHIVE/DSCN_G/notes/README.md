# DSCN-G Paper — Instructions & Resources

**Fecha:** 2026-07-19  
**Estado:** ✅ Listo para escritura  
**Archivador:** `papers/DSCN_G/WRITING_PACKAGE/`

---

## 📁 Estructura de la Carpeta

```
papers/DSCN_G/WRITING_PACKAGE/
├── README.md (este archivo)
├── 01_OUTLINE.md (estructura del paper)
├── 02_ABSTRACT_DRAFT.md (borrador de abstract)
├── 03_KEY_RESULTS.md (resultados clave con números)
├── 04_COMPARISONS.md (tabla comparativa con otros frameworks)
├── 05_FALSIFICATION.md (criterios de falsificación)
├── 06_FIGURES_TODO.md (figuras necesarias)
└── REFERENCES.bib (bibliografía en BibTeX)
```

---

## 🎯 Target del Paper

**Journal:** *Neural Computation* (MIT Press) o *Cognitive Systems Research* (Elsevier)

**Por qué:**
- Aceptan papers de modelos computacionales de cognición
- Reviewers entienden matemática + simulación
- Timeline: 2-3 meses para review
- Impact factor: ~2.5-3.0

**Alternativa:** *Frontiers in Computational Neuroscience* (más rápido, open access)

---

## 📝 Instrucciones de Escritura

### Opción A: Escribís Vos (Recomendado)

**Pasos:**

1. **Leé `01_OUTLINE.md`** — Estructura completa del paper (sección por sección)
2. **Leé `02_ABSTRACT_DRAFT.md`** — Tenés un abstract base para modificar
3. **Empezá por la sección que te resulte más fácil:**
   - Methods (ya tenés las ecuaciones)
   - Results (ya tenés los números)
   - Introduction (más narrativa, dejala para después)
4. **Usá `03_KEY_RESULTS.md`** para copiar/pegar los resultados con números exactos
5. **Incluí al menos 2 figuras** (ver `06_FIGURES_TODO.md`)
6. **Revisá `05_FALSIFICATION.md`** para asegurarte de que los claims sean falsificables

**Timeline sugerido:**
- Día 1-2: Abstract + Intro + Methods
- Día 3-4: Results + Figures
- Día 5: Discussion + Conclusion
- Día 6: Revisión general + References

### Opción B: Escribo Yo

Si preferís que lo escriba yo, confirmame y:
1. Genero el paper completo en markdown primero
2. Lo revisás y me das feedback
3. Hago los ajustes
4. Exportamos a PDF/LaTeX

**Warning:** Si escribo yo, vas a tener que revisar bien que el tono y estilo te representen.

---

## 📊 Contenido Clave (Resumen)

### Claims Principales

1. **Working Memory Capacity ≈ 4 items**
   - Dato: 89.1% (4-back) → 51.6% (5-back), 42.2% drop
   - Emerge de N_ss* ≈ 4 (Theorem 1)
   - Sin hardcoded limits

2. **3 Teoremas Formales Verificados**
   - Theorem 1: Homeostatic fixed point (N_ss* = 4.0 ± 0.0)
   - Theorem 2: Parametric vector convergence (‖ω − ω*‖ ≤ 0.038 < β)
   - Theorem 3: Phase convergence rate (p_conv = 0.97)

3. **C3 Prediction (Phase-Hijacking)**
   - Predicción: PLV(A) − PLV(B) > 0.3 bajo valence overload
   - Aún no validada (future work)

4. **Φ_proxy Scaling O(log N)**
   - Theorem 7: ρ_eff(α, N)·Φ_proxy(N) = c(α) + O(1/N)
   - Aún no validado completamente (future work)

### Lo que NO claims

- ❌ "DSCN-G resuelve el hard problem" (explícitamente no)
- ❌ "DSCN-G es consciente" (ontológicamente agnósticos)
- ❌ "DSCN-G supera a todos los modelos" (solo comparamos con lo que tenemos datos)

---

## 📈 Figuras Necesarias (Mínimo 2)

### Figura 1: Working Memory Capacity

**Tipo:** Line plot  
**Ejes:**
- X: N-back load (1, 2, 3, 4, 5, 6)
- Y: Accuracy (% correct)

**Líneas:**
- DSCN-G (mean ± std, n=20 trials)
- Humano (Cowan 2001, shaded region 4±1)

**Anotación:** Flecha en 4-back marcando "capacity limit"

### Figura 2: Architecture Diagram

**Tipo:** Esquemático del sistema  
**Elementos:**
- Nodes (círculos) con ω_i, φ_i, V_i
- Information chains (flechas entre nodos)
- Root node (abajo) → Leaf nodes (arriba)
- Eq. 1-7 anotadas en los componentes

**Estilo:** Similar a Fig. 1 de papers de IIT o GWT

### Figuras Opcionales (si hay espacio)

3. Theorem 1 convergence (N_ss* vs. α, θ_death)
4. Phase-hijacking schematic (C3 prediction)
5. Φ_proxy scaling (log plot)

---

## 🔬 Referencias Clave

### Cognición / Working Memory
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behav Brain Sci*.
- Miller, G. A. (1956). The magical number seven. *Psychol Rev*.

### Modelos de Cognición
- Tononi, G. (2004). IIT. *BMC Neurosci*.
- Baars, B. (1988). GWT. *Cognitive Theory of Consciousness*.
- Friston, K. (2010). Free-energy principle. *Nat Rev Neurosci*.

### Kuramoto / Dinámica de Phases
- Kuramoto, Y. (1984). *Chemical Oscillations, Waves, and Turbulence*.
- Acebrón, J. A., et al. (2005). Kuramoto model review. *Rev Mod Phys*.

### TD-Learning / RL
- Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning* (2nd ed.).
- Robbins, H., & Monro, S. (1951). Stochastic approximation. *Ann Math Stat*.

---

## ✍️ Borradores Disponibles

### `02_ABSTRACT_DRAFT.md`
Tenés un abstract base de ~200 palabras. Modificalo o usalo como inspiración.

### `03_KEY_RESULTS.md`
Todos los resultados con números exactos para copiar/pegar:
- Theorem 1: N_ss* = 4.0 ± 0.0
- N-back: 89.1% → 51.6% (42.2% drop)
- Theorem 2: ‖ω − ω*‖ = 0.038 < β = 0.10
- Theorem 3: p_conv = 0.97

### `04_COMPARISONS.md`
Tablas comparativas listas para usar:
- DSCN-G vs. IIT vs. GWT vs. Predictive Processing
- Working memory: DSCN-G vs. Cowan vs. Miller

---

## 🚀 Próximos Pasos

### Si escribís vos:
1. Leé `01_OUTLINE.md`
2. Empezá por la sección que te resulte más cómoda
3. Usá `03_KEY_RESULTS.md` para los números
4. Mandame el draft cuando tengas ~50% y te doy feedback

### Si escribo yo:
1. Confirmame con un "dale, escribilo"
2. Genero el paper completo en 2-3 horas
3. Lo revisás y me decís qué cambiar
4. Iteramos hasta que estés conforme

---

## 📬 Contacto

Cualquier duda durante la escritura, avisame y te ayudo con:
- Números específicos que necesites
- Aclaraciones sobre los teoremas
- Generación de figuras (puedo hacer los scripts Python)
- Revisión de drafts parciales

---

**Good luck! 🚀**

*Per Aspera, Ad Astra.*