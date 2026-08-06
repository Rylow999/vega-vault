# Freeze Checklist — pre-congelación DSCN-G v1.0

> Generado 2026-07-25 aplicando la guía de corrección y estructuración.
> Detalle completo del estado científico en `ROADMAP.md`; esto es el
> checklist de forma (¿está todo en su lugar?), no de validación.

## DSCN-G

- [x] CORE definido — `NOUS/DSCN-G/CORE/SCOPE.md`.
- [x] CORE separado en THEORY / FORMALISM / IMPLEMENTATION / VALIDATION.
- [x] Extensiones separadas — `NOUS/DSCN-G/EXTENSIONS/`.
- [x] C3 aislado y documentado — `EXTENSIONS/C3_Face_Hijacking/README.md` +
      `STATUS.md`.
- [ ] Dinámica discreta documentada — `EXTENSIONS/DISCRETE_DYNAMICS/README.md`
      creado, pero como **placeholder honesto**: la relación con el núcleo
      sigue sin determinar. No se cierra este ítem, se deja explícito.
- [x] Código revisado — `CORE/VALIDATION/CONSISTENCY_CHECK.md` (sin
      inconsistencias sustantivas; un path relativo corregido).
- [x] Experimentos organizados — `EXPERIMENTS/N_BACK|COMPARISONS|
      SYNCHRONIZATION|ABLATIONS|STABILITY|OTHER` (ya existía de la reorg
      2026-07-25).
- [x] Documentación consistente — tabla de estado en `CLAIMS_STATUS.md`,
      reglas de evolución en `CORE_RULES.md`.
- [ ] **Abierto — hallazgo nuevo:** `CORE/IMPLEMENTATION/CODE/run_pipeline.sh`
      apunta al N-back v5 legacy (marcado "NO usar sus números" en
      `REVIEW_PENDING.md`), no al v6 que el paper realmente cita. Ver
      `CORE/VALIDATION/CONSISTENCY_CHECK.md` §3b. Reproducibilidad rota si
      se corre el pipeline tal cual hoy — requiere decisión de contenido.

## FATE

- [x] Dependencias claras — `FATE/DSCNG_INTERFACE/DSCNG_INTERFACE.md`.
- [x] Interfaz DSCN-G definida — mismo archivo, componentes usados/propios
      documentados.
- [ ] **Abierto:** discrepancia de versión — `Master-Document/` cita
      FATE v4/v5, la interfaz real documenta v6. No bloquea el freeze del
      núcleo DSCN-G (es un problema de FATE, no de DSCN-G), pero sí bloquea
      dar por cerrado el Master-Document. Ver caveat en
      `DSCNG_INTERFACE.md`.

## NOUS

- [x] Separación de investigación futura — QUANTUM / GAUGE / COSMOS aislados
      de DSCN-G, cada uno con PAPER/ + NOTES/ propios.
- [x] Ontología organizada — `NOUS/DOCUMENTATION/` (filosófico/técnico)
      separado del núcleo verificado.

## Veredicto

**DSCN-G v1.0 puede congelarse en el sentido de forma** (estructura,
separación núcleo/extensión, documentación de claims) — eso es lo que pedía
esta guía. La congelación *científica* depende de las decisiones abiertas
en `REVIEW_PENDING.md` (C3, Φ_proxy, dinámica discreta — Bloque B de
`ROADMAP.md`), que son decisiones de contenido, no de organización, y siguen
sin resolverse. Organización ≠ validación (regla de oro del `README.md`
raíz) — esto ordena, no decide.
