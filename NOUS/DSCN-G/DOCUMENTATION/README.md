# DSCN-G v3 — Paper Kit Auditado (Ronda 6, 2026-07-22/24)

**DSCN-G = Dual-State Cognitive Geometry.** Nombre canónico único; ver
`00_Core_Definition.md` para la nota de resolución de nombre.

## Orden de lectura

1. **`00_Core_Definition.md`** — portada conceptual, lenguaje llano, sin cifras.
2. **`01_DSCN-G_Paper.md`** — el paper técnico. Teoremas, verificación computacional,
   resultados de N-back, discusión. Léelo para cualquier cifra o claim preciso.
3. **`02_Design_Notes/`** — notas de diseño de Ronda 5 (histórico, llevó al v3).
4. **`03_Estado_Auditoria/`** — mapa ejecutivo de qué está listo, qué necesita ajuste de
   texto, y qué se retiró — cierre de Ronda 6.
5. **`auditoria/`** — las 6 rondas de auditoría completas, veredicto por claim
   (`claims_falsifiable.md`), outline anotado (`paper_structure.md`), y la revisión
   científica externa (`REVIEW_RECOMMENDATIONS.md`).
6. **`codigo/`** — todo el código y datos crudos que sustentan cada cifra del paper.

## Estado de las claims formales del núcleo (resumen)

| Claim | Estado |
|---|---|
| T2 — convergencia de ω | ✅ alignment = 1.0000 |
| T1 — punto fijo homeostático (+ maximalidad) | ✅ N_ss\*≈4–5, maximalidad verificada con simulación real |
| T3 — consenso de fase | ⚠️ 100% (criterio operacional) / 76.7% (criterio estricto R≥0.9) |
| C3 — hijacking (sincronización patológica) | ❌ no se sostiene (0.9% de triggers muestra el efecto) |
| Φ_proxy O(log N) | ❌ no se sostiene con ninguna de las dos métricas probadas |
| Baseline RNN vainilla (N-back) | ✅ DSCN-G retiene piso d′≈0.8–1.0 hasta 20-back; RNN colapsa desde 7-back |

Detalle completo en `01_DSCN-G_Paper.md` §3–5 y `03_Estado_Auditoria/`.

## Reproducibilidad

```
bash codigo/run_pipeline.sh
python3 codigo/nback_v6_corrected/nback_v6_occurrence_aware.py
```

## Nota sobre `papers/DSCN_G_v3/` (carpeta existente del repo)

`PAPER_TODO.md` en esa carpeta todavía reporta C3 como verificado (ΔR=+0.46 ✓), cifra
retractada por la auditoría de este paquete (ver §3.4 del paper y `CORRIGENDUM.md`
adjunto). Aplicar ese corrigendum antes de considerar `DSCN_G_v3` vigente.
