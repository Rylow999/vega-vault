# EGFR — PDB Structures for Docking

**Status:** IDENTIFIED (2026-07-19)  
**Source:** RCSB PDB Search: "EGFR kinase human erlotinib"  
**Total matches:** 6 experimental structures

---

## §3.2 Estructuras PDB Disponibles

### Top Estructuras (por relevancia para docking)

| PDB ID | Resolución | Ligando | Mutación | Año | Usar para docking |
|--------|------------|---------|----------|-----|-------------------|
| **1M17** | ~2.5-3.0Å | Erlotinib | WT | 2000-2004 | ✅ Sí (clásica) |
| **4ZAU** | ~2.5-3.0Å | Osimertinib | T790M | 2010-2014 | ✅ Sí (resistencia) |
| Por completar | - | - | - | - | ⏳ Faltan 4 IDs |

**Nota:** La búsqueda mostró 6 estructuras pero necesito extraer los IDs específicos.

---

### Acciones Pendientes

1. **Extraer los 6 PDB IDs** de la página de resultados (hacer clic en cada uno o exportar tabla)
2. **Descargar estructuras** (.pdb files) para:
   - 1M17 (EGFR + Erlotinib, wild-type)
   - 4ZAU (EGFR + Osimertinib, T790M mutant)
3. **Verificar resolución** < 3.0Å (necesario para docking preciso)
4. **Identificar cadena relevante** (generalmente chain A es la quinasa domain)

---

### Criterios de Selección

Para docking confiable, priorizar:
- ✅ Resolución ≤ 3.0Å (ideal < 2.5Å)
- ✅ Ligando co-cristalizado conocido (Erlotinib, Gefitinib, Osimertinib)
- ✅ Wild-type o mutantes comunes (T790M, L858R)
- ❌ No usar estructuras con resolución > 4.0Å (demasiado ruido)

---

**Próximo paso:** Agente debe navegar a cada resultado para extraer PDB IDs específicos y descargar archivos.