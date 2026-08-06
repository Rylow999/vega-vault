# DSCN-G v3 — Paper Kit

**Dual-State Cognitive Geometry**

Kit completo para reproducir simulaciones y escribir el paper sobre DSCN-G v3.

> ⚠️ **Auditado 2026-07-22** — ver `AUDIT_NOTES.md` antes de citar cualquier
> número de este README en el paper. Se encontraron y corrigieron dos bugs
> que rompían el pipeline (el N-back nunca guardaba resultados; el
> acoplamiento de Kuramoto no era sincrónico), y varios números "esperados"
> de más abajo no se reproducen con el código corregido — están marcados.

## 📋 Contenido

### Scripts principales

- **`verify_dscng_v3.py`** — Verifica los 4 teoremas del núcleo (T1, T2, T3, C3)
- **`nback_v5_grounded.py`** — N-back task grounded en el sustrato de vitalidad/omega
- **`generate_figure2.py`** — Genera la Figura 2 (degradación de d' vs n-back)
- **`analyze_results.py`** — Analiza resultados de verificación y N-back
- **`run_pipeline.sh`** — corre las cuatro etapas de punta a punta en un solo comando

### Documentación

- **`AUDIT_NOTES.md`** — auditoría 2026-07-22: bugs encontrados/corregidos y tabla reclamado-vs-reproducido
- **`paper_structure.md`** — Estructura completa del paper (con notas de auditoría inline)
- **`claims_falsifiable.md`** — Claims y criterios de falsificación (veredictos actualizados)

## 🚀 Uso

### Instalación

```bash
pip install numpy scipy matplotlib
```

### Ejecución rápida (~30 seg)

```bash
bash run_pipeline.sh --quick
```

### Ejecución completa / escala canónica (~4 min con el código corregido)

```bash
bash run_pipeline.sh
```

o paso a paso:

```bash
python verify_dscng_v3.py --seeds 30 --steps 2000
python nback_v5_grounded.py --n-backs 1 2 3 4 5 6 8 10 12 15 --n-trials 40
python generate_figure2.py
python analyze_results.py
```

> Antes de la auditoría esto tomaba ~1h20 (loop de Kuramoto no vectorizado)
> y el segundo paso fallaba siempre por falta del JSON de salida. Ambos
> problemas están corregidos — ver `AUDIT_NOTES.md`.

## 📊 Resultados reproducidos (escala canónica, código corregido, 2026-07-22)

### Verificación de teoremas

- **T1 (Homeostasis):** N_ss* converge a **~4.0–4.8 nodos** (no ~9-10 — esa
  cifra pertenece al modelo de N-back, un sistema distinto; ver tabla en
  `AUDIT_NOTES.md`). Cota universal y punto fijo: sólidos. Maximalidad: el
  test actual nunca la confirma (posible problema del test, no del teorema).
- **T2 (ω alignment):** alignment final = **1.0000 ± 0.0000** (≥ lo reclamado)
- **T3 (Phase consensus):** **100%** de corridas alcanzan consenso por el
  criterio del código, pero solo 23/30 cumplen el umbral R≥0.9 que el
  teorema define; 0/30 bimodal (no 7% como se decía antes)
- **C3 (Hijacking):** **no se reproduce** — solo 0.9% de los triggers
  muestran el aumento de PLV reclamado (no 100%); ΔPLV medio ≈ 0 (no −0.46)

### N-back (recurso continuo)

- **N_ss* empírico:** 9.50 ± 1.02 (se reproduce casi exacto)
- **d'(1-back):** 5.33 (se reproduce)
- **d'(10-back):** 3.92 (no 3.12 como se decía antes)
- **d'(15-back):** 3.90 (no 2.78 — la curva cae y **se aplana** a partir de
  ~5-back, no sigue bajando)
- **Patrón:** SIN escalón abrupto en ningún punto (esto sí se sostiene), pero
  la forma real es "caída y meseta", no una degradación continua hasta 2.78

## 📁 Archivos generados por el pipeline

- `verification_results_v3.json` — Datos de verificación (reales, escala canónica)
- `nback_v5_paper_ready.json` — Datos de N-back (reales)
- `figure2_nback_v5_paper.png` — Figura para el paper (regenerada con datos reales)

## 🔬 Claims principales

Ver `claims_falsifiable.md` para el detalle claim por claim con veredicto
actualizado. Resumen:

### Se sostienen tal como estaban reclamados

1. **ω alignment convergence** (T2) — alignment = 1.0000
2. **N_ss\* empírico del N-back** = 9.5 ± 1.0 nodos
3. **WM sin escalón abrupto** (forma cualitativa, no los valores puntuales de d')

### Necesitan corrección antes de citarse

4. **N_ss\* de T1** — es ~4-5, no ~9-10 (esa cifra era del modelo de N-back)
5. **Consenso de fase (T3)** — 100% por un criterio más laxo que R≥0.9; sin casos bimodales
6. **d'(10-back) y d'(15-back)** — la curva se aplana en ~3.9, no sigue cayendo a 2.78

### No se sostienen — requieren rediseño o hay que retirarlas

7. **Phase hijacking (C3)** — el mecanismo, tal como está implementado, no
   produce en promedio el aumento de sincronización patológica que describe
   (ver hipótesis en `AUDIT_NOTES.md` §3 sobre por qué)

### Pendientes de validación experimental (sin cambios)

- Validación EEG/fMRI de predicciones
- Scaling de Φ_proxy (O(log N))
- Drug discovery connection

## ⚠️ Honestidad epistémica

### Lo que PODEMOS claimar (verificado con la corrida real)

- ✅ ω alignment convergence (1.0000)
- ✅ N_ss* empírico del N-back = 9.5 ± 1.0
- ✅ WM sin escalón abrupto (forma cualitativa)
- ✅ T1: cota universal y condición de punto fijo

### Lo que hay que corregir o quitar antes de publicar

- ❌ "N_ss* = 9-10 nodos" para T1 → es ~4-5
- ❌ "C3 verificado (100% triggers, ΔPLV=-0.46)" → no se reproduce
- ❌ "d'(10-back)=3.12, d'(15-back)=2.78" → son 3.92 y 3.90
- ⚠️ "90% consensus, 7% bimodal" para T3 → es 100%/0% con el criterio del código, pero el criterio mismo es más laxo que la definición del teorema

### Lo que NO PODEMOS claimar (sin cambios respecto de antes)

- ❌ "DSCN-G resuelve el hard problem" (explícitamente NO)
- ❌ "Supera a todos los modelos" (solo comparamos con modelos de slots)
- ❌ Validación experimental (EEG/fMRI) — future work
- ❌ Φ_proxy scaling O(log N) — pendiente verificar

## 📚 Referencias clave

- Cowan (2001): The magical number 4 in short-term memory
- Miller (1956): The magical number 7, plus or minus 2
- Bays & Husain (2008): Resources and errors in working memory
- van den Berg et al. (2014): A resource-rational analysis of working memory
- Kuramoto (1984): Chemical oscillations, waves, and turbulence
- Tononi (2004): An information integration theory of consciousness
- Baars (1988): A cognitive theory of consciousness

## 🎯 Próximos pasos

1. Leer `AUDIT_NOTES.md` completo
2. Decidir qué hacer con C3 (rediseñar el trigger / correr con más nodos activos / retirar la claim)
3. Escribir Abstract + Introduction con los números corregidos
4. Escribir Results (N-back) con la forma real de la curva ("caída y meseta")
5. Generar Figura 1 (architecture diagram)
6. Escribir Discussion + Conclusion, ajustando la sección 5.3 (C3 como predicción falsificable) a lo que realmente se sostiene

## 📝 Notas importantes

### N-back v5 vs v4

La versión v5 es **grounded** en el sustrato real de DSCN-G:
- Sin cap explícito ni rama condicionada a n_back
- Misma regla de decisión (similitud coseno) para todo n_back
- Usa el espacio omega real de la arquitectura
- Sustrato reutilizable (vitalidad decae sobre todo el pool)
- (Auditoría 2026-07-22) ahora además guarda sus resultados a disco — antes no lo hacía

### Nota metodológica

El N-back aplica Eq. 5 a los N nodos completos (sin pruning permanente), mientras que el núcleo original usa pruning definitivo. Esta desviación es **deliberada y declarada**, no escondida.

### Nota metodológica adicional (auditoría 2026-07-22)

La meseta de d'≈3.9 a partir de ~5-back (en vez de seguir cayendo) es
consistente con un efecto de piso: solo hay `n_stimuli=10` vectores canónicos
en un espacio de 8 dimensiones, así que incluso cuando la traza específica
del estímulo consultado ya murió, comparar contra "lo que sea que esté vivo"
en el sustrato da una tasa de acierto por encima del azar por pura
coincidencia de un espacio de estímulos finito — no necesariamente por
retención genuina de memoria de trabajo. Vale la pena discutirlo en
Limitations si se usa esta curva en el paper.

## 🌟 Per Aspera, Ad Astra

**Open-source:** Todo el código es tuyo para usar, modificar y compartir.

**Falsificable:** Cada claim tiene criterios de falsificación claros.

**Honesto:** Separamos VERIFIED de HYPOTHESIZED de SPECULATED — y, después
de esta auditoría, también de "reclamado pero no reproducido".
