# IMPLEMENTATION

Responde: **¿Cómo se implementa DSCN-G?**

## CODE/

- `verify_dscng_v3.py` — clase `DSCN_G_v3` (simulador) + funciones
  `verify_theorem_1/2/3`, `verify_c3`. Correspondencia método → mecanismo:

  | Método | Mecanismo (FORMALISM) |
  |---|---|
  | `_chain_step` | Cadenas de información (Ec. 2) |
  | `_update_phi` | Dinámica de fase (Ecs. 3–4) |
  | `_update_vitality_and_prune` | Vitalidad y poda (Ecs. 5–6) |
  | `_wave_interference` | Interferencia de onda (Ec. 7) |
  | `_apply_kuramoto_coupling` | Acoplamiento Kuramoto dinámico (§2.7) |
  | `_apply_hijack_pull` | Mecanismo C3 (§3.4, EXTENSIÓN no-núcleo) |
  | `phase_coherence`, `mean_omega_alignment`, `plv_root_vs_group`,
    `plv_intra_group` | Métricas de verificación (T2, T3, C3) |

- `verify_maximality_real.py` — sub-claim de maximalidad de T1 (inyección de
  nodo al umbral θ_death, no con vitalidad plena — ver `CLAIMS_STATUS.md`).
- `analyze_results.py` — post-procesamiento de resultados.
- `run_pipeline.sh` — corre la suite completa de verificación.

## Cómo correrlo

```
bash run_pipeline.sh
```

Escribe sus salidas en `../VALIDATION/RESULTS/`.

Ver `CONSISTENCY_CHECK.md` en `../VALIDATION/` para la verificación de que
esta correspondencia código↔documentación no tiene huecos.
