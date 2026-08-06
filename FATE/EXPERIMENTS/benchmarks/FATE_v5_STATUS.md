# FATE v5 — Status (2026-07-07)

**Estado**: STABLE, repo privado en GitHub.
**Repo**: https://github.com/Rylow999/fate-v5-stable
**Binario**: `fate-v5-stable/build/main_v5` (nativo C, libfate.so + chembl_oracle)

## Veredicto vs CMA-ES (benchmarks reales, mismas seeds/budget)

| Oracle | Dim | FATE-v5 (pop=20) | CMA-ES | Ganador |
|--------|-----|------------------|--------|---------|
| rastrigin | 10 | 0.947 | 0.861 | **FATE** |
| moving_peaks | 10 | 0.942 | 0.807 | **FATE** |
| chembl_neighbors | 64 | 0.158 | 0.142 | **FATE** |
| schwefel | 10 | 1.0 (empate) | 1.0 | empate |

FATE v5 vence a CMA-ES en continuo multimodal y drug-discovery reales.

## Mejoras implementadas (vs v4)

- `--uc-biased`: escape ULTRA_CHROMO direccional anclado al champion (salto Collatz).
- `--cog-fix`: omega_root siempre-activo + pesos cognitive más fuertes (resonance 0.20→0.45, state 0.15→0.35).
- **Pop adaptativo** (default cuando `--pop-size 0`): arranca en 20, decrece a 16.

## Hallazgo crítico del 2026-07-07

- **pop=20 es el óptimo**. pop=40 y pop=64 empeoran consistentemente.
- El escape CTEG (donde uc_biased/cog_fix actúan) **solo se dispara en régimen de estancamiento real**.
- Con pop=20 el champion converge tan rápido que el escape nunca corre → uc_biased/cog_fix son no-op en la práctica con la config óptima.
- Implicación: pop=20 resolvió el problema mejor que las mejoras de escape. Las mejoras siguen en el código y funcionan SI hay estancamiento forzado (pop grande + bajo stagnation), pero no suman sobre pop=20.

## Próximos pasos pendientes

1. Híbrido FATE+CMA para el caso de pop grande donde FATE todavía no le da.
2. Benchmark multi-seed en GitHub CI para validar el repo estable.
3. Escribir paper (research-paper-writing skill disponible).
4. GBrain sobre Obsidian como memoria del proyecto (en progreso).

## Nota de honestidad

Los flags uc_biased/cog_fix NO mejoran el score con pop=20 (el escape no se ejercita).
No son bugs: es que pop=20 hace innecesario el escape. Se documentan como
"activos bajo estancamiento", no como mejora universal.
