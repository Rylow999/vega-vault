# Notas sobre Datos de Benchmark

## ⚠️ Importante: Identificar FATE Real vs Random Search

Este documento clarifica qué datos corresponden a **FATE v6 real** y cuáles son **random search** (usados temporalmente mientras se arreglaba el pipe mode).

---

## Datos Válidos (FATE v6 Real)

### EGFR Benchmark — FATE Real ✅
- **Ubicación:** `experiments/EGFR_Benchmark/egfr_fate_*.csv`
- **Commit:** `678f8ec` (2026-07-19 ~20:30)
- **Cantidad:** 30 runs (D=64/128/256 × budget=500/3000 × 5 seeds)
- **Script:** `run_egfr_fate_real.py` + `pipe_intermediary.py`
- **Método:** FATE v6 real via pipe mode bidireccional
- **Resultados:** best=1.0000 en todas las configs (pIC50 ≥ 9.0)

**Estos son los únicos datos válidos para el paper de EGFR.**

---

## Datos NO Válidos (Random Search)

### EGFR Benchmark — Random Search ❌
- **Ubicación:** `experiments/EGFR_Benchmark/egfr_D*_budget*_seed*.csv` (sin "fate")
- **Commit:** `1451af2`
- **Cantidad:** 150 runs
- **Script:** `run_egfr_direct.py`
- **Método:** Generación aleatoria de phase vectors
- **Código:** `phase = rng.uniform(0, 2 * np.pi, dim)`
- **NO USAR** para análisis o comparaciones

### Aspirina GPU — Random Search ❌
- **Ubicación:** `experiments/Aspirina_GPU/aspirina_direct_*.csv`
- **Commit:** `f53da18`
- **Cantidad:** 50 runs
- **Script:** `run_aspirina_direct.py`
- **Método:** Random search con oracle BRICS+DSCN-G
- **NO USAR** para análisis o comparaciones

### Aspirina ChEMBL — Random Search ❌
- **Ubicación:** `experiments/Aspirina_GPU/aspirina_chembl_*.jsonl`
- **Commit:** `73c70a0`
- **Cantidad:** 50 runs
- **Script:** `run_aspirina_chembl.py`
- **Método:** Random search con oracle ChEMBL simple
- **NO USAR** para análisis o comparaciones

---

## Cómo Distinguir en el Futuro

1. **Nombre del archivo:**
   - Incluye "fate" → FATE real ✅
   - No incluye "fate" → Verificar script ❌

2. **Script usado:**
   - `run_egfr_fate_real.py` → FATE real ✅
   - `run_egfr_direct.py` → Random search ❌

3. **Metadata en el CSV:**
   - FATE real: primera línea es `eval,fitness`
   - Random search: misma estructura (¡cuidado!)

4. **Commit en Git:**
   - `678f8ec` → FATE real ✅
   - `1451af2`, `f53da18`, `5aed4cd` → Random search ❌

---

## Próximos Pasos

Para el paper, usar **exclusivamente**:
- Datos de `egfr_fate_*.csv` (commit `678f8ec`)
- Si se necesitan más datos, correr con `run_egfr_fate_real.py`
- Para comparativa vs CMA-ES/TPE: usar `main_v5.exe --samplers cma-es` (cuando esté implementado)

---

**Responsable:** Hermes Agent  
**Fecha:** 2026-07-19 ~20:35  
**Verificación:** Ver `CORRECCION_RANDOM_SEARCH.md` para más detalles

---

## Lección Aprendida

**Siempre especificar en el nombre del archivo:**
- El sampler usado (fate, cma-es, tpe, random)
- Dimensiones y budget
- Seed

**Ejemplo de buena convención:**
`egfr_fate_D64_budget500_seed42.csv` ✅

**Ejemplo a evitar:**
`egfr_D64_budget500_seed42.csv` ❌ (¿fate? ¿random? ¿cma-es?)