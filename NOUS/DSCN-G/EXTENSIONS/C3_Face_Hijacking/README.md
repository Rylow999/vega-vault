# C3 / Face Hijacking

## Propósito

C3 ("Phase Hijacking") es la hipótesis de que, cuando la vitalidad del nodo
raíz supera un umbral (`V_root > θ_emerg`), el sistema entra en un modo de
sincronización patológica: la raíz "secuestra" la fase del resto de los
nodos activos, aumentando artificialmente el phase-locking (PLV) del grupo.
La analogía biológica original es epilepsia focal / GNW ignition — usar con
cautela, ver `../../CORE/THEORY/00_Core_Definition.md` §5.6.

## Relación con DSCN-G

C3 usa el mismo simulador (`DSCN_G_v3`) y el mismo mecanismo de acoplamiento
Kuramoto que el núcleo — no es un módulo de código aparte, es un modo de
operación del núcleo bajo ciertas condiciones. Por eso podría *parecer*
núcleo, pero documentalmente no lo es: no es necesario para definir ni para
que funcionen T1/T2/T3.

## Estado actual

Ver `STATUS.md` para el detalle numérico completo. Resumen:

- **Demostrado:** el mecanismo dispara (2237 triggers en 30 seeds, 3.73% de
  los steps) y responde en la dirección predicha bajo parámetros más
  agresivos (rise_rate sube de 0.7% a 30.2%).
- **No sostenido a los parámetros de diseño originales:** solo 0.9% de los
  triggers muestran el efecto reclamado (ΔPLV<−0.3); ΔPLV medio ≈ 0
  (−0.007±0.061), no el −0.46 de borradores previos.
- **Hipotético / retirado:** la analogía de privilegio estructural
  ("hub_boost", tálamo) se probó y se retiró formalmente (Ronda 6) — no
  tuvo efecto medible por saturación de la métrica, no porque el mecanismo
  esté mal implementado.

## Condiciones para integración futura al CORE

Por `../../CORE_RULES.md`: necesitaría (1) evidencia que sostenga el efecto
a parámetros cercanos a los de diseño (no 10x más agresivos), (2) una
métrica de PLV que no sature con poblaciones pequeñas (3–4 seguidores a
N*≈4–5), y (3) reformular la predicción cuantitativa (¿qué % de triggers
se espera, y por qué?) antes de volver a intentar validarla.
