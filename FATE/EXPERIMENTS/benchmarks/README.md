# Experiments — Nexus Vault

Directorio raíz de todos los experimentos del programa FATE / Nexus.

## Estructura

```
experiments/
  FATE_v6_STATUS.md          ← Status actual (2026-07-19)
  FATE_v5_STATUS.md          ← Histórico v5 (2026-07-07)
  FATE_v4_*.md               ← Histórico v4
  
  EGFR_Drug_Discovery/       ← Drug discovery para EGFR (cáncer)
    00_Protocol.md           ← Protocolo completo
    01_PDB_Structures.md     ← Estructuras PDB disponibles
    oracle_egfr_v1.py        ← Oracle similarity-based (verificado)
    data/
      chembl_egfr_ic50_1000.json  ← 1000 compuestos ChEMBL con IC50
  
  Aspirina_GPU/              ← Corridas BRICS + DSCN-G en GPU
    run_aspirina_gpu.py      ← Script para 2 corridas (D=8, D=16)
    aspirina_*.jsonl         ← Resultados (en curso)
```

## Estado Actual (2026-07-19)

### ⚠️ IMPORTANTE: Corrección de Benchmarks

Algunos benchmarks anteriores (commits 1451af2, f53da18, 5aed4cd) usaban **random search** en vez de FATE real.
Ver `CORRECCION_RANDOM_SEARCH.md` para detalles completos.

**Benchmarks válidos con FATE real:**
- Commit `678f8ec`: EGFR Benchmark — 30 runs con FATE v6 real (pipe mode)
- Archivos: `egfr_fate_D*_budget*_seed*.csv` (incluyen "fate" en el nombre)

### FATE v6 ✅ PUSHED

**Repo:** https://github.com/Rylow999/fate-v6-modular  
**Commit:** `280d0ec` (README + benchmarks D=8-1024)

**Benchmarks:**
- Phase 1 ✅: 4 oráculos × 2-3 dims × 2 budgets × 5 seeds = 20 configs
- Phase 2 ✅ parcial: rastrigin D=128,256,512,1024 (D=2048 ❌ timeout >2h)
- **Hallazgo clave:** moving_peaks D=10 = 0.998 (mejora vs v5: 0.86-0.93)

**Límite práctico:** D=1024 (3 eval/s). D=2048 es impráctico con budget=3000.

### EGFR Drug Discovery 🧪 ORACLE VERIFIED

**Oracle:** `EGFR_Drug_Discovery/oracle_egfr_v1.py`  
**Datos:** 800 compuestos únicos (ChEMBL IC50 contra EGFR)  
**Throughput:** 380 eval/s (batch de 10)  
**Smoke test:** fitness=0.7943 (IC50=71nM, similarity=0.086)

**Pendientes:**
- Benchmark completo (D=64,128,256 × budget=500,3000 × 25 seeds)
- Top-50 candidates → docking validation

### Aspirina GPU ⏳ CORRIENDO

**Corridas:** 2 configs (D=8, D=16 × 25 seeds, budget=2000)  
**Oracle:** BRICS + DSCN-G coherence (GPU Pitcairn)  
**Tiempo estimado:** 1-1.5 horas totales  
**Output:** `Aspirina_GPU/aspirina_D8.jsonl`, `aspirina_D16.jsonl`

---

## Cómo ejecutar

### FATE v6 benchmarks

```bash
cd fate-v6-modular
bash build_v5.sh  # Compilar

# Benchmark estándar
cd bench
../bin/main_v5.exe --oracle rastrigin --dim 10 --budget 3000 --seed 42 --seeds 5

# Pipe mode con oracle externo
../bin/main_v5_pipe.exe --dim 64 --budget 500 --seed 42 --batch | python oracle_extern.py
```

### EGFR oracle

```bash
cd nexus-vault/experiments/EGFR_Drug_Discovery
python oracle_egfr_v1.py  # Test interactivo (pipe mode)
```

### Aspirina GPU

```bash
cd nexus-vault/experiments/Aspirina_GPU
python run_aspirina_gpu.py  # ~1-1.5 horas
```

---

**Última actualización:** 2026-07-19 ~06:30  
**Próximo hito:** Terminar corridas aspirina GPU, luego benchmark EGFR completo