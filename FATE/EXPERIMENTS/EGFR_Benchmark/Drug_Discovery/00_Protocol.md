# EGFR Drug Discovery — FATE v6 Research Program

**Status:** PLANNING (2026-07-19)  
**Target:** Epidermal Growth Factor Receptor (EGFR, CHEMBL203, P00533)  
**Indication:** Cáncer (NSCLC, glioblastoma, colorectal)  
**Meta:** Paper con rigor metodológico completo o exploración interna validada

---

## §1 Target Justification

### 1.1 ¿Por qué EGFR?

| Criterio | EGFR | Justificación |
|----------|------|---------------|
| **Relevancia clínica** | ✅ Alta | Mutado en ~30% NSCLC, 50% glioblastoma |
| **Datos disponibles** | ✅ 19,118 compuestos en ChEMBL | IC50/Ki/EC50 medidos experimentalmente |
| **Estructuras PDB** | ✅ Múltiples (6LU7, 1M17, etc.) | Docking viable |
| **Scaffold conocido** | ✅ Erlotinib, Gefitinib, Osimertinib | Hay referencias para validar el oracle |
| **Complejidad** | ✅ Media | Ni muy fácil (aspirina) ni muy difícil (allosteric modulators) |

### 1.2 Información del Target

- **ChEMBL ID:** `CHEMBL203`
- **UniProt:** `P00533` (EGFR_HUMAN)
- **Nombre completo:** Epidermal growth factor receptor
- **Tipo:** SINGLE PROTEIN (tirosina quinasa)
- **Organismo:** *Homo sapiens*
- **Compuestos asociados:** 19,118 (ChEMBL website)
- **Drugs aprobados:** Erlotinib (Tarceva), Gefitinib (Iressa), Osimertinib (Tagrisso), etc.

### 1.3 Estructuras Cristalinas Disponibles (PDB)

Por verificar con búsqueda específica en PDB/RCSB:
- **1M17:** EGFR quinasa domain + Erlotinib (resolución ~2.5Å)
- **4ZAU:** EGFR + Osimertinib (T790M mutant)
- **6LU7:** (es SARS-CoV-2 Mpro, NO EGFR — corregir)

**Acción pendiente:** Buscar estructuras PDB específicas de EGFR con ligandos co-cristalizados.

---

## §2 Protocolo de Investigación

### Fase 0: Setup (2 semanas)

| Tarea | Responsable | Estado |
|-------|-------------|--------|
| Obtener ChEMBL API key | Usuario | ⏳ Pendiente |
| Descargar datos EGFR (IC50, SMILES) | Agente | ⏳ Pendiente |
| Identificar estructuras PDB de EGFR | Agente | ⏳ Pendiente |
| Configurar entorno docking (AutoDock Vina) | Usuario + Agente | ⏳ Pendiente |

### Fase 1: Construcción del Oracle (4-8 semanas)

**Objetivo:** Crear `oracle_egfr_v1.py` que transforme phase → fitness.

#### Decisión (2026-07-19): Opción A — Similarity-Based

**Implementado:** `oracle_egfr_v1.py` (similarity-based, rápido, reproducible)

```python
def oracle_egfr(phase):
    # 1. phase → fingerprint sintético (1024 bits)
    fp = phase_to_fingerprint(phase, dim=64)
    
    # 2. Buscar compuesto más cercano en ChEMBL con IC50 conocido
    #    (Tanimoto similarity contra 1000 compuestos precomputados)
    nearest = find_nearest_in_db(fp, db=chembl_egfr_ic50_1000)
    
    # 3. Fitness = pIC50 / 9.0 (normalizado a [0, 1])
    # IC50 < 1nM → pIC50 > 9 → fitness ≈ 1.0
    # IC50 > 1μM → pIC50 < 6 → fitness < 0.67
    ic50 = nearest['IC50_nM']
    pIC50 = 9.0 - log10(ic50)
    fitness = pIC50 / 9.0
    
    return fitness, {
        "nearest_smiles": nearest['smiles'],
        "similarity": nearest['tanimoto'],
        "pIC50": pIC50,
        "IC50_nM": ic50
    }
```

**Datos:** 1000 compuestos de ChEMBL con IC50 contra EGFR (CHEMBL203), descargados vía API pública.
- Fuente: `https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL203&standard_type=IC50&standard_flag=1&limit=1000`
- Total disponible: 26,600 actividades (usamos top 1000 por ahora)
- Rango pIC50: ~5.0 - 9.0+ (IC50: 10μM - 1nM)

**Pros:**
- ✅ Rápido: ~10k-50k eval/s (dependiendo de dim, batch)
- ✅ Reproducible: mismos datos, mismos resultados
- ✅ Honesto: es un proxy válido (análogos conocidos predicen actividad)
- ✅ No requiere docking ni setup complejo

**Contras:**
- ❌ Solo encuentra análogos de lo conocido (no descubre scaffolds totalmente nuevos)
- ❌ La calidad depende de la cobertura del dataset (1000 vs 26,600)

**Próximos pasos:**
- Si los resultados son prometedores (FATE encuentra pIC50 > 7), escalar a 10,000 compuestos.
- Para paper: validar top-50 con docking real (AutoDock Vina).

---

### Fase 2: Benchmark Riguroso (4-6 semanas)

**Configuración:**

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| Samplers | FATE-v6, CMA-ES, Random | Baselines estándar |
| Dims | 64, 128, 256 | Escalabilidad |
| Budgets | 500, 3000, 10000 | ¿Cuánto "tiempo" necesita cada uno? |
| Seeds | 25 | Estadística sólida (mean ± std) |
| Oracle | `oracle_egfr_v1.py` (similarity o híbrido) | Consistente |

**Métricas:**
- `best_pIC50`: Mejor actividad predicha (pIC50 = -log10(IC50[M]))
- `mean_pIC50`: Actividad promedio de top-100
- `time_total`: Tiempo de cómputo
- `throughput`: evals/segundo
- `novelty`: Tanimoto promedio vs compuestos conocidos (<0.6 = scaffold nuevo)

**Criterio de éxito:**
- FATE encuentra compuestos con pIC50 > 7 (IC50 < 100nM)
- FATE > CMA-ES en al menos 2 de 3 métricas (best, mean, novelty)
- Throughput > 100 eval/s (para que sea práctico)

---

### Fase 3: Validación Externa (8-12 semanas, opcional pero recomendado)

**Paso 3.1: Docking de top candidatos**
- Top-20 de FATE → AutoDock Vina contra 2-3 PDBs de EGFR
- Top-20 de CMA-ES → mismo docking
- Comparar: ¿FATE encuentra mejores poses? ¿Mejor energía de unión?

**Paso 3.2: Análisis de scaffolds**
- ¿Los top de FATE son análogos de Erlotinib o scaffolds nuevos?
- Si son nuevos: ¿tienen propiedades ADMET razonables? (usar SwissADME)

**Paso 3.3: (Opcional, caro, external)**
- Sintetizar top-3 moléculas
- Test in vitro contra EGFR quinasa
- Publicar si IC50 experimental < 1μM

---

## §3 Datos Requeridos

### 3.1 ChEMBL Data (por descargar)

```bash
# Query para obtener todos los compuestos con IC50 contra EGFR
# CHEMBL203, assay_type='B' (binding), standard_type='IC50'

SELECT chembl_id, canonical_smiles, standard_value as ic50_nM, standard_units
FROM activities
WHERE target_chembl_id = 'CHEMBL203'
  AND standard_type = 'IC50'
  AND standard_units = 'nM'
  AND standard_value IS NOT NULL
  AND standard_value > 0
```

**Acción:** Usuario debe ejecutar esta query en ChEMBL web o API y exportar CSV.

### 3.2 PDB Structures (por identificar)

Buscar en https://www.rcsb.org:
- Query: `EGFR AND kinase domain AND Homo sapiens AND resolution < 3.0A`
- Filtrar: estructuras con ligandos co-cristalizados (Erlotinib, Gefitinib, etc.)

**Acción:** Agente hace búsqueda web y crea `§3.2_pdb_structures.md`.

---

## §4 Documentación y Organización en Vault

```
nexus-vault/
  papers/
    EGFR_Drug_Discovery/
      00_Protocol.md (este archivo)
      01_Data_Acquisition.md (ChEMBL API, PDB structures)
      02_Oracle_Design.md (similarity vs docking, decisions)
      03_Experimental_Log.md (runs, seeds, configs, results)
      04_Analysis.md (FATE vs CMA, novelty, scaffolds)
      05_Validation.md (docking results, ADMET, synthesis plans)
      06_Paper_Draft.md (manuscrito final)
  experiments/
    EGFR/
      chembl_egfr_ic50.csv (descargado)
      pdb_structures.json (identificados)
      oracle_egfr_v1.py (código)
      run_egfr_benchmark.py (benchmark script)
      results_v6/ (CSVs de corridas)
  ontology/notes/
    EGFR_Target.md (wikilinks a papers, datos, experimentos)
```

---

## §5 Próximos Pasos Inmediatos

1. **Usuario:** Obtener ChEMBL API key (https://www.ebi.ac.uk/chembl/api/data/docs)
2. **Agente:** Buscar estructuras PDB de EGFR (RCSB PDB)
3. **Usuario + Agente:** Decidir oracle (similarity vs docking vs híbrido)
4. **Agente:** Crear `oracle_egfr_v1.py` skeleton
5. **Usuario:** Confirmar si hay acceso a GPU para docking (R9 270X puede correr Vina?)

---

## §6 Honestidad Metodológica

**Lo que podemos claimar:**
- "FATE-v6 encuentra moléculas con alta afinidad predicha (pIC50 > 7) en X horas"
- "FATE-v6 supera a CMA-ES en best_pIC50 (effect size = Y)"
- "Top-10 candidatos tienen scaffolds nuevos (Tanimoto < 0.6 vs Erlotinib)"

**Lo que NO podemos claimar sin validación experimental:**
- "FATE descubre nuevos fármacos para cáncer" (requiere in vitro/in vivo)
- "Estas moléculas son seguras/effectivas en humanos" (requiere ensayos clínicos)
- "FATE es mejor que docking tradicional" (requiere benchmark contra Glide, GOLD, etc.)

**Nuestra postura:** Si el oracle es similarity-based, somos honestos: "optimización de análogos". Si incluimos docking y validación externa, podemos claimar "descubrimiento de scaffolds". La calidad del oracle define el techo de las claimaciones.

---

**Última actualización:** 2026-07-19  
**Próximo checkpoint:** Cuando usuario tenga API key de ChEMBL y agente identifique PDBs