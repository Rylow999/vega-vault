# Corrigendum — papers/DSCN_G_v2/PAPER_TODO.md

**Colocar este archivo en `papers/DSCN_G_v2/` (o anexar su contenido al final de
`PAPER_TODO.md` de esa carpeta).**

`PAPER_TODO.md` (2026-07-20) reporta, en su tabla de arquitectura v3:

> **C3** (Phase Hijacking) | η_kura dinámico (0.005→0.025) | ΔR = +0.46 ✓

Esta cifra fue retractada por la auditoría de Ronda 6 del paquete `DSCN_G_v3`
(2026-07-22/24). Verificación real, 30 semillas × 2000 pasos:

- Solo **20 de 2237 eventos de disparo (0.9%)** muestran el aumento de sincronización
  reclamado (criterio: ΔPLV > 0.3).
- La media de ΔPLV sobre todos los eventos es **−0.007 ± 0.061**, prácticamente cero —
  no el +0.46/−0.46 reportado en borradores previos de este trabajo.

**Veredicto vigente:** C3, a los parámetros de diseño originales, **no se sostiene** y no
debe citarse como verificado. Ver `papers/DSCN_G_v3/01_DSCN-G_Paper.md` §3.4 y
`papers/DSCN_G_v3/03_Estado_Auditoria/ANALISIS_ESTADO_2026-07-24.md` para el detalle
completo, incluidas las dos decisiones pendientes sobre su rediseño.

Los demás valores de esa tabla (T1, T2) coinciden en orden de magnitud con `DSCN_G_v3`
pero usan parámetros ligeramente distintos (θ_death=0.12 vs. 0.10) — no son
contradictorios, solo de una corrida anterior. T3 en `PAPER_TODO.md` reporta R=0.90 sin
desglosar criterio estricto/laxo; `DSCN_G_v3` sí lo desglosa (76.7% estricto).
