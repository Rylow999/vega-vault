# SCOPE — DSCN-G v1.0

## ¿Qué es DSCN-G?

**DSCN-G = Dual-State Cognitive Geometry.** Un marco teórico que propone que
los sistemas cognitivos pueden entenderse como sistemas dinámicos
autoorganizados: mantienen estabilidad interna, coordinan procesos
distribuidos, se adaptan al entorno y reorganizan su dinámica según demanda —
sin depender de una representación fija de información.

**Problema que intenta resolver:** cómo modelar memoria de trabajo y
regulación cognitiva como recursos *continuos* emergentes de principios
homeostáticos, en vez de como slots discretos fijos.

**Principios fundamentales:** regulación dinámica (homeostasis
computacional), coordinación temporal (sincronización de fase), recursos
cognitivos dinámicos (memoria/atención variables), aprendizaje adaptativo
(TD-learning). Detalle en `THEORY/00_Core_Definition.md` §2.

**Límites actuales:** verificado por simulación computacional (30 seeds,
2000 steps); sin validación contra datos biológicos (EEG/fMRI, future work);
comparado solo contra un RNN vainilla, no contra LSTM/GRU/Transformer.

## ¿Qué pertenece al CORE?

**Incluido:**
- Los 4 principios fundamentales (regulación, coordinación temporal, recursos
  dinámicos, aprendizaje adaptativo).
- Arquitectura mínima: regulación interna, coordinación temporal, memoria
  dinámica, mecanismo adaptativo.
- Formalismo: Ecs. 1–7 del paper (TD-learning, cadenas de información,
  dinámica de fase, vitalidad/poda, interferencia de onda, Kuramoto).
- Teoremas T1 (punto fijo homeostático + maximalidad), T2 (convergencia de
  ω), T3 (consenso de fase — con matiz, ver `CLAIMS_STATUS.md`).
- Resultados verificados: N-back v6 occurrence-aware (N_ss*=9.50±1.02),
  comparación contra RNN vainilla.

## ¿Qué NO pertenece al CORE?

- **C3 / Face Hijacking** — hipótesis experimental, no sostenida a los
  parámetros de diseño originales. Extensión, no núcleo.
- **Φ_proxy (escalado O(log N))** — evidencia preliminar no concluyente, dos
  definiciones probadas, ninguna sostiene la predicción. Extensión.
- **Conciencia emergente / DSCN-G como NCC formalmente completo** — claim
  especulativo, explícitamente no se puede afirmar "DSCN-G es consciente" ni
  "resuelve el hard problem".
- **Dinámica discreta** — relación con el núcleo aún sin determinar.
- Extensiones ontológicas y modelos futuros (línea NOUS: Quantum, Gauge,
  Cosmos).

## ¿Qué queda pendiente?

- Dinámica discreta: determinar si es extensión formal o línea aparte
  (`EXTENSIONS/DISCRETE_DYNAMICS/`, vacío por ahora).
- Nuevas extensiones matemáticas y capacidades cognitivas: fuera de alcance
  de v1.0 por diseño — ver `CORE_RULES.md` para el criterio de admisión.
- Validación EEG/fMRI, ablation studies, sensibilidad a parámetros, baseline
  LSTM/GRU/Transformer (declarado como trabajo futuro en el paper §5.5).

Ver `../CLAIMS_STATUS.md` para el estado claim-por-claim y
`../../ROADMAP.md` para el checklist de congelación completo.
