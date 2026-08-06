# FATE v6 — Ruta del Programa de Investigación

**Documento**: `experiments/PROGRAMA_ROUTE.md`  
**Última actualización**: 2026-07-19  
**Estado**: EN EJECUCIÓN (Fase 1 y 2 en curso)

---

## Visión General

**Objetivo a 12 meses:** Establecer FATE v6 como framework de optimización competitivo en:
1. Optimización continua (benchmarks sintéticos)
2. Drug discovery (EGFR inhibitor design)
3. Sistemas complejos (DSCN-G coherence)

**Diferenciador clave:** Honestidad metodológica + reproducibilidad total. Separar claims verificables de hipótesis, reportar exitos Y fallos. Todo el código + datos + configs en `/experiments/` del vault.

---

## Fases del Programa

### Fase 1: FATE v6 como Optimizador General (2-4 semanas) ✅ EN CURSO

**Estado:** Benchmarks completados (D=8-1024), escritura del paper en preparación.

**Entregables:**
- ✅ FATE v6 modular (core/, oracles/, cli/)
- ✅ Batch protocol (2.4) para GPU acceleration
- ✅ Benchmarks: rastrigin, moving_peaks, schwefel, ChEMBL (D=8-1024)
- ✅ Hallazgo: moving_peaks D=10 = **0.998** (mejora vs v5: 0.86-0.93)
- ⏳ Paper draft (GECCO/NeurIPS 2026)

**Repos:**
- https://github.com/Rylow999/fate-v6-modular (commit `280d0ec`)
- https://github.com/Rylow999/nexus-vault (experiments/)

**Próximos pasos:**
1. Escritura paper Fase 1 (prioridad: semana 3-4)
2. Benchmark EGFR completo (similarity-based)
3. Análisis comparativo FATE-v6 vs CMA-ES vs TPE ( честный reporte)

---

### Fase 2: EGFR Drug Discovery (3-6 meses) 🧪 ORACLE VERIFIED

**Estado:** Oracle implementado y verificado (380 eval/s, 800 compuestos ChEMBL).

**Objetivo:** Optimización de inhibidores de EGFR (CHEMBL203) usando FATE v6.

**Entregables:**
- ✅ Oracle similarity-based (`oracle_egfr_v1.py`)
- ✅ 1000 compuestos ChEMBL descargados (800 únicos, pIC50 2.19-11.22)
- ✅ Protocolo documentado (`00_Protocol.md`)
- ✅ Estructuras PDB identificadas (`01_PDB_Structures.md`)
- ⏳ Benchmark completo (D=64,128,256 × budget=500,3000 × 25 seeds)
- ⏳ Top-50 candidates → docking validation (AutoDock Vina)
- ⏳ Paper Fase 2 (JCIM/Bioinformatics)

**Configuración del benchmark:**
```bash
cd nexus-vault/experiments/EGFR_Drug_Discovery
python oracle_egfr_v1.py  # test mode

# Benchmark completo (por crear)
./run_egfr_benchmark.py   # D=64,128,256 × 500,3000 × 25 seeds
```

**Métrica de éxito:** FATE-v6 encuentra candidatos con pIC50 > 7.0 (IC50 < 100nM) consistentemente mejor que CMA-ES.

**Riesgos:**
- Oracle similarity-based es "muy simple" → mitigación: validar con docking
- FATE no mejora vs CMA-ES → mitigación: honestidad en el paper (reportar ambos lados)

---

### Fase 3: Sistema Integrado "Nexus Drug Discovery" (6-12 meses) 🔧 EN SETUP

**Estado:** Oracle BRICS+DSCN-G funcional (wrapper single-thread).

**Objetivo:** Loop cerrado de diseño molecular: FATE + BRICS + DSCN-G + docking.

**Entregables:**
- ✅ Oracle BRICS+DSCN-G (`oracle_smiles_dscng_wrapper.py`, single-thread)
- ⏳ Corridas aspirina GPU (D=8/16 × 25 seeds, BRICS+DSCN-G)
- ⏳ Multi-objectivo: pIC50 + QED + SA + síntesis-realista
- ⏳ Paper Fase 3 (Scientific Reports o similar)

**Configuración:**
```bash
cd nexus-vault/experiments/Aspirina_GPU
python run_aspirina_gpu.py  # D=8/16 × 25 seeds, budget=2000
```

**Innovación:** DSCN-G coherence como regularizador de "viabilidad dinámica" en el espacio latente molecular.

---

## Infraestructura

### Estructura de `/experiments/`

```
experiments/
├── README.md                    # Índice maestro
├── PROGRAMA_ROUTE.md            # Este documento
├── FATE_v6_STATUS.md            # Status actualizado (2026-07-19)
├── FATE_v5_STATUS.md            # Histórico v5
│
├── Aspirina_GPU/                # Corridas BRICS+DSCN-G + ChEMBL
│   ├── run_aspirina_gpu.py      # Oracle SMILES (BRICS+DSCN-G)
│   ├── run_aspirina_chembl.py   # Oracle ChEMBL simple
│   ├── aspirina_chembl_D*_seed*.jsonl   # 50 runs completados ✅
│   └── aspirina_D*_seed*.jsonl  # Por correr (BRICS+GPU)
│
├── EGFR_Drug_Discovery/         # Drug discovery específico
│   ├── 00_Protocol.md           # Protocolo completo (fases 0-3)
│   ├── 01_PDB_Structures.md     # Estructuras PDB (6 matches)
│   ├── oracle_egfr_v1.py        # Oracle similarity-based ✅ VERIFIED
│   └── data/chembl_egfr_ic50_1000.json
│
└── ...                          # Futuros experiments
```

### Convenciones

- **Cada experimento** tiene: script + configs + raw outputs + análisis
- **Scripts** son self-contained y reproducibles (paths absolutos o relativos al vault)
- **Outputs** son JSONL parseables (fácil post-procesamiento)
- **Documentación** en español, código en inglés

---

## Timeline Estimado

| Semana | Hito | Estado |
|--------|------|--------|
| 1 (2026-07-19) | FATE v6 benchmarks + push | ✅ COMPLETADO |
| 1-2 | Fix BRICS+GPU + aspirina GPU runs | ⏳ EN CURSO |
| 2-3 | Benchmark EGFR completo | 🔲 PENDIENTE |
| 3-4 | Paper draft Fase 1 (FATE general) | 🔲 PENDIENTE |
| 4-8 | Docking validation (top-50 EGFR) | 🔲 PENDIENTE |
| 8-12 | Paper Fase 2 (EGFR drug discovery) | 🔲 PENDIENTE |
| 12-24 | Sistema multi-objectivo + Fase 3 | 🔲 PENDIENTE |

---

## Criterios de Éxito

### Paper Fase 1 (FATE v6 general)
- [ ] 4+ benchmarks sintéticos (rastrigin, moving_peaks, schwefel, ChEMBL)
- [ ] D=8-1024, 25 seeds c/u
- [ ] Comparativa FATE-v6 vs CMA-ES vs TPE ( честный)
- [ ] Batch protocol + GPU como contribución principal
- [ ] Submit: GECCO/NeurIPS 2026

### Paper Fase 2 (EGFR)
- [ ] FATE mejora vs CMA-ES en pIC50 (estadísticamente significativo, p<0.05)
- [ ] Top-50 candidates con docking scores
- [ ] Al menos 1-2 candidatos con IC50 predicho < 100nM
- [ ] Submit: JCIM o Bioinformatics

### Paper Fase 3 (Nexus)
- [ ] Loop cerrado FATE+BRICS+DSCN-G+docking
- [ ] Multi-objectivo: ≥2 objetivos (ej: pIC50 + QED)
- [ ] Síntesis-realista (fragmentos BRICS válidos)
- [ ] Submit: Scientific Reports o similar

---

## Honestidad Metodológica

**Principio:** "No hay nada que demostrarle a nadie, pero siempre con honestidad."

- Separar **claims verificables** de **hipótesis**
- Reportar **cuándo FATE pierde** también, no solo cuando gana
- Si un baseline gana, documentarlo (es información valiosa)
- Datos + código + configs **siempre públicos** (o al menos reproducibles internamente)

---

## Próximos Pasos Inmediatos (esta semana)

1. ✅ Fix oracle BRICS+GPU (wrapper single-thread)
2. ⏳ Correr aspirina GPU (D=8/16 × 25 seeds, BRICS+DSCN-G)
3. 🔲 Benchmark EGFR completo (D=64,128,256 × 25 seeds)
4. 🔲 Empezar paper draft Fase 1

---

**Notas:**
- Aspirina ChEMBL (50 runs) ya están completas y pusheadas (commit `73c70a0`)
- Oracle EGFR similarity-based verificado (380 eval/s, 800 compuestos)
- BRICS+GPU wrapper single-thread funcional (más lento pero estable)

**Última revisión:** 2026-07-19 ~17:00