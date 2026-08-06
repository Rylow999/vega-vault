# SensorBridge (Fase 3) — Literature & Design Map

Companion to `sgm-core-dev` for the next SGM experiment (exp_SGM_0019, Fase 3 SensorBridge).
Maps the papers ALREADY in the vault (`lit/papers/`, excluded from GitHub via `.gitignore`) to the
Fase 3 tasks, and sketches an honest synthetic design. Built 2026-08-02 from roadmap §Fase 3.

## Fase 3 objective (from SGM_ROADMAP.md, dated 2026-08-02)
- Proyección de señales sensoriales → ω + interocepción.
- `sensor_bridge()` para audio, visual, térmico, propioceptivo.
- `ω_root_intero` (PHS, T_eff, ρ(t), latencia, page faults).
- Política de emergencia (E_root > 0.8 → reducir K=3, W_base=4).
- Tests T-SEN-01 / T-SEN-02.
- **Nota:** sin hardware real, testear con señales SINTÉTICAS. No inventar datos de sensores.

## Vault papers → Fase 3 task mapping
| Paper (lit/papers/) | Rol en SensorBridge |
|---|---|
| `kanerva_hdc_2009_0903.4547.pdf` (Kanerva HDC) | **MECANISMO BASE.** Hyperdimensional Computing proyecta señal de ANY-dimensionalidad a un vector denso (ω) vía bundling + permutación (binding). Implementa `sensor_bridge()` directamente. |
| `vsa_survey_2022_2111.06077.pdf` (VSA survey) | Unifica HDC + TPR; referencia de operaciones (bind, bundle, permute, unbind, cosine similarity). La "biblia" de proyección sensor→espacio. |
| `plate_tensor_product_2003_cs0308022.pdf` (TPR) | Tensor Product Representations: binding alternativo de señales en vectores. Complementa HDC. |
| `hipporag_arxiv_2405.14831.pdf` (HippoRAG PPR) | Personalized PageRank sobre Knowledge Graph. El ruteo por afinidad (Eq.2) YA es PPR; relevante para RECUPERAR la señal proyectada desde ω (round-trip). |
| `titans_arxiv_2501.00663.pdf` (Titans) | Long-term memory + test-time learning; memoria persistente de la señal proyectada. |
| `snap_2024.pdf` (SNAP) | Catastrophic forgetting en Hebbian. CUIDADO: proyectar señal nueva NO debe machacar memoria existente (relevante también Fase 4 trauma). |
| `kirkpatrick_ewc_2017.pdf` (EWC) | Preservar memoria en aprendizaje continuo al incorporar señal nueva. |
| `kope_arxiv_2604.07904.pdf` | ID 2604 es futuro/raro — confirmar con PyPDF2 antes de citar; no asumir. |

## Suggested exp_SGM_0019 design (synthetic, honest)
1. Generar señal sintética: p.ej. "audio" = vector de amplitudes; "visual" = matriz aplanada.
2. Proyectar a ω vía HDC binding (permutación + bundling) — el mecanismo de Kanerva/Plate.
3. **Test de INYECTIVIDAD:** señales distintas → ω distintos (coseno(ω_a, ω_b) < umbral). Si colapsan, la proyección no sirve.
4. **Test de ROUND-TRIP:** desde ω recuperar la señal (unbind) con error < tol. Demuestra que el grafo puede "sentir" y "recordar" la señal.
5. Conectar a `ω_root_intero`: la señal proyectada modula ρ(t) / latencia; política de emergencia si E_root > 0.8.
6. NO usar hardware real; todo sintético. NO inventar métricas de sensores.

## Trazability note
Fase 3 es orthogonal a Fase 1 (modos, 0016) y al loop escalado (0017) y self-mod (0018). Keep it a
SINGLE experiment (proyección + round-trip + interocepción), do NOT bundle SensorBridge with
Planificación (Fase 4) — split per the trazability rule learned on 0016/0017.
