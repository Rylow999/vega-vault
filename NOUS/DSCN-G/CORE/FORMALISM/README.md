# FORMALISM

Responde: **¿Cómo se describe DSCN-G formalmente?**

DSCN-G v3 es un único paper auditado (6 rondas, 2026-07-22/24); las ecuaciones y
teoremas viven ahí, no se fragmentaron en archivos sueltos para no arriesgar
inconsistencias entre una copia y el original. Este directorio es el índice de
dónde está cada pieza formal dentro de
[`../01_DSCN-G_Paper.md`](../01_DSCN-G_Paper.md):

## Ecuaciones (§2 — Fundamentos Computacionales)

| Ec. | Mecanismo | Sección |
|---|---|---|
| 1 | Aprendizaje por diferencia temporal (TD-learning) | §2.2 |
| 2 | Cadenas de información | §2.3 |
| 3–4 | Dinámica de fase y selección de acción | §2.4 |
| 5–6 | Vitalidad y poda (autopoiesis) | §2.5 |
| 7 | Interferencia de onda | §2.6 |
| — | Acoplamiento Kuramoto dinámico (mecanismo nuevo v3) | §2.7 |

## Teoremas formales (§3 — Teoremas Formales y Verificación)

| Teorema | Enunciado | Sección | Estado |
|---|---|---|---|
| T1 | Punto fijo homeostático (+ maximalidad) | §3.1 | ✅ verificado, ver `CLAIMS_STATUS.md` |
| T2 | Convergencia del vector semántico ω | §3.2 | ✅ verificado |
| T3 | Consenso de fase | §3.3 | ⚠️ verificado con matiz (reporte estricto) |
| C3 | Sincronización patológica ("hijacking") | §3.4 | ❌ no sostenido a params originales — es EXTENSIÓN, no núcleo |

La correspondencia formalismo → código está en `../IMPLEMENTATION/`; la
correspondencia formalismo → evidencia numérica está en `../VALIDATION/`.
