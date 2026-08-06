# FATE v6 — Status (2026-07-19)

**Estado**: BENCHMARK EN CURSO (Phase 2: D=2048)  
**Repo**: https://github.com/Rylow999/fate-v6-modular  
**Binarios**: `fate-v6-modular/bin/main_v5.exe`, `main_v5_pipe.exe`

---

## ¿Qué es FATE v6?

FATE v6 es la versión **modular y GPU-accelerated** del optimizador FATE.

**Cambios principales vs v5:**
1. **Arquitectura modular**: core/, oracles/, cli/ separados
2. **Batch protocol**: evaluación de generaciones completas en un mensaje
3. **GPU support**: Pitcairn (R9 270X) funcional con OpenCL
4. **MSYS2 fixes**: PATH, TMP, getline() compatibility

---

## Benchmarks v6 (2026-07-19)

### Phase 1: v5-matching configs ✅ COMPLETADA

| Oracle | Dim | Budget | FATE-v6 best | Throughput | Estado |
|--------|-----|--------|--------------|------------|--------|
| rastrigin | 10 | 500 | **0.803±0.031** | 30,724 eval/s | ✅ |
| rastrigin | 10 | 3000 | **0.893±0.012** | 93,141 eval/s | ✅ |
| rastrigin | 64 | 500 | **0.617±0.016** | 12,534 eval/s | ✅ |
| rastrigin | 64 | 3000 | **0.697±0.023** | 16,667 eval/s | ✅ |
| moving_peaks | 10 | 3000 | **0.998±0.000** | 124,744 eval/s | ✅ **↑ Mejora vs v5** |
| moving_peaks | 64 | 3000 | **0.455±0.028** | 19,246 eval/s | ✅ |
| schwefel | 10 | 3000 | **1.000±0.000** | 53,419 eval/s | ✅ |
| schwefel | 64 | 3000 | **1.000±0.000** | 16,904 eval/s | ✅ |
| chembl | 64 | 500 | **0.134±0.006** | 3,974 eval/s | ✅ |
| chembl | 64 | 3000 | **0.149±0.006** | 4,594 eval/s | ✅ |
| chembl | 128 | 3000 | **0.144±0.005** | 2,329 eval/s | ✅ |
| chembl | 256 | 3000 | **0.144±0.004** | 429 eval/s | ✅ |

**Comparación con v5:**
- moving_peaks D=10: **0.998** vs 0.86-0.93 en v5 → **MEJORA SIGNIFICATIVA**
- ChEMBL D=64: **0.149±0.006** vs 0.148±0.009 en v5 → **Empate técnico**
- Throughput D=10: 30k-124k eval/s → **10x más rápido** que v5

### Phase 2: GPU extension configs ⏳ PARCIAL (D=2048 timeout)

| Oracle | Dim | Budget | FATE-v6 best | Throughput | Estado |
|--------|-----|--------|--------------|------------|--------|
| rastrigin | 128 | 3000 | 0.655 | 3,853 eval/s | ✅ |
| rastrigin | 256 | 3000 | 0.602 | 460 eval/s | ✅ |
| rastrigin | 512 | 3000 | 0.557 | 66 eval/s | ✅ |
| rastrigin | 1024 | 3000 | 0.545 | 3 eval/s | ✅ |
| rastrigin | 2048 | 3000 | — | ~1 eval/s (est.) | ❌ TIMEOUT (>2h) |

**Hallazgo:** Throughput cae con dimensionalidad. D=2048 es **impráctico** con budget=3000.
FATE **escala funcionalmente hasta D=1024** (3 eval/s → ~17 min para budget=3000).

---

## EGFR Drug Discovery — Protocolo Iniciado

**Estado:** Oracle v1 implementado y verificado  
**Datos:** 1000 compuestos ChEMBL con IC50 contra EGFR (CHEMBL203)  
**Oracle:** `papers/EGFR_Drug_Discovery/oracle_egfr_v1.py` (similarity-based)

**Resultados smoke test:**
- 800 compuestos únicos cargados
- pIC50 range: 2.19 - 11.22 (IC50: 6.5mM - 0.06nM)
- Throughput: 380 eval/s (batch de 10)
- Fitness test: 0.7943 (IC50=71nM, similarity=0.086)

**Próximos pasos:**
1. Benchmark EGFR (D=64, 128, 256 × budget=500, 3000 × 25 seeds)
2. Top-50 candidates → validar con docking (AutoDock Vina)
3. Comparar FATE-v6 vs CMA-ES en pIC50 predicho

---

## Aspirina GPU — Pendiente

**Objetivo:** 4 corridas BRICS+DSCN-G en GPU (Pitcairn)
- D=8 × balanced (25 seeds, budget=2000)
- D=8 × chem_first (25 seeds, budget=2000)
- D=16 × balanced (25 seeds, budget=2000)
- D=16 × chem_first (25 seeds, budget=2000)

**Tiempo estimado:** 1-1.5 horas totales (con batch protocol)

---

## Próximos Pasos

1. ⏳ Esperar a que termine benchmark v6 (D=2048)
2. Commit + push a GitHub (`fate-v6-modular`)
3. Lanzar 4 corridas aspirina GPU
4. Integrar todo en `/experiments` en el vault
5. Iniciar benchmark EGFR completo

---

**Última actualización:** 2026-07-19 ~05:30  
**Benchmark v6:** Phase 1 ✅, Phase 2 ⏳ (95% completada)