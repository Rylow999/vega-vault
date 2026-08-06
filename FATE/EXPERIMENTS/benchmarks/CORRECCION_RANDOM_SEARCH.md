# Corrección: Benchmarks "Direct Mode" son Random Search (NO FATE real)

**Fecha:** 2026-07-19  
**Motivo:** Aclarar que los benchmarks etiquetados como "direct mode" NO son FATE v6 real.

---

## Benchmarks afectados

### 1. EGFR Benchmark (1451af2)
- **Archivos:** `experiments/EGFR_Benchmark/egfr_D*_budget*_seed*.csv` (150 archivos)
- **Script:** `run_egfr_direct.py`
- **Lo que dice el commit:** "150 runs completed"
- **Realidad:** **Random search** (generación aleatoria de phase vectors)
- **Código relevante:**
  ```python
  # Genera phase vector aleatorio
  phase = rng.uniform(0, 2 * np.pi, dim)
  ```
- **NO es:** FATE v6, CMA-ES, ni ningún optimizador

### 2. Aspirina GPU Direct (f53da18)
- **Archivos:** `experiments/Aspirina_GPU/aspirina_direct_D*_seed*.csv` (50 archivos)
- **Script:** `run_aspirina_direct.py`
- **Lo que dice el commit:** "50 runs completed (BRICS+DSCN-G)"
- **Realidad:** **Random search** con oracle BRICS+DSCN-G
- **Código relevante:**
  ```python
  phase = rng.uniform(0, 2 * np.pi, dim).tolist()
  ```
- **NO es:** FATE v6 ni pipe mode

### 3. Benchmarks Direct Mode (5aed4cd)
- **Scripts:** `run_egfr_direct.py`, `run_aspirina_direct.py`
- **Motivo original:** Pipe mode con `main_v5_pipe.exe` tenía problemas de comunicación bidireccional
- **Decisión tomada:** Usar random search temporalmente para "tener datos"
- **Esto fue un error:** Se commiteó y pusheado como si fuera un benchmark válido

---

## ¿Por qué es un problema?

1. **Confusión en los resultados:** Los archivos CSV tienen nombres que no distinguen entre FATE real y random search
2. **Afirmaciones potencialmente engañosas:** Los commits dicen "completed" sin aclarar que es random search
3. **Dificulta el análisis:** Si alguien analiza los datos sin leer el código, asume que es FATE

---

## Solución aplicada

### Commit correcto (678f8ec)
- **Título:** "EGFR Benchmark: FATE v6 REAL — 30 runs completed"
- **Contenido:** Usa `pipe_intermediary.py` para conectar FATE real con oracle
- **Archivos:** `egfr_fate_D*_budget*_seed*.csv` (30 archivos)
- **Distingue claramente:** Los archivos con "fate" en el nombre son FATE real

### Este commit de corrección
- Agrega este `CORRECCION_RANDOM_SEARCH.md` para documentar explícitamente
- No modifica los commits anteriores (ya están pusheados)
- Sirve como referencia para cualquiera que analice los datos

---

## Cómo distinguir los datos

| Patrón de archivo | ¿Es FATE real? | Script | Commit |
|-------------------|----------------|--------|--------|
| `egfr_fate_D*_budget*_seed*.csv` | ✅ SÍ | `run_egfr_fate_real.py` | 678f8ec |
| `egfr_D*_budget*_seed*.csv` (sin "fate") | ❌ NO (random) | `run_egfr_direct.py` | 1451af2 |
| `aspirina_direct_D*_seed*.csv` | ❌ NO (random) | `run_aspirina_direct.py` | f53da18 |
| `aspirina_chembl_D*_seed*.jsonl` | ❌ NO (random) | `run_aspirina_chembl.py` | 73c70a0 |

---

## Lección aprendida

**Nunca commitear "datos de benchmark" sin especificar explícitamente:**
1. ¿Qué optimizador se usó? (FATE, CMA-ES, random search, etc.)
2. ¿El código del optimizador es real o es un placeholder?
3. ¿Los resultados son comparables con otros benchmarks?

En el futuro:
- Usar nombres de archivos que incluyan el sampler: `egfr_{sampler}_D{dim}_...`
- Agregar metadata en el CSV: `# sampler=FATE-v6` o `# sampler=random`
- Verificar el código antes de commitear resultados

---

**Responsable:** Hermes Agent (asistente de Luciano Nieto)  
**Fecha de corrección:** 2026-07-19 ~20:30