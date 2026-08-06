---
name: dscn-g-lab
description: Experimentos controlados, auditoría honesta y publicación incremental para el motor DSCN-G. Usar cuando se diseñen experimentos online/offline, se evalúe señal real, se publique incremental, o se eviten anti-patrones conocidos.
---

# DSCN-G Lab

## Reglas duras
- Offline antes de online: k-means silhouette/inertia sobre contextos reales antes de correr mecanismos online.
- Nunca afirmar inyección, seguridad o separación de sentido sin evidencia directa (grep/test mono-sémicas).
- Cuando un experimento empeora el baseline, cerrar honestamente; recién ahí cambiar diseño.
- Documentar en `_README_ENGINE.md` con precisión: señal vs artefacto, baseline, métricas reales.
- Generalización mínima: si un mecanismo mejora el baseline para una palabra polisémica, hay que validarlo en al menos otra antes de declarar ganador. Un acierto en una palabra puede ser artefacto del template o del lexicón.
- Métrica preferida para lenguaje no es clasificación interna A/B, sino coherencia externa de dominio: generación o respuesta coherente con el dominio dado, evaluada por overlap semántico/consistencia, no por accuracy de sentido interna.

## Corpus y sustrato
- Wikipedia español suele bloquear descargas automáticas (`403`). Tatoeba/Tatoeba-style suele no estar disponible para español (`404`). No iterar en infinito sobre downloads.
- Corpus real accesible usable: `donquijote.txt`. Elegir palabras con ocurrencias suficientes para extraer contextos no triviales.
- Si no hay corpus real procesable, usar corpus sintético controlado A/B con ground truth explícito, documentando esa condición.
- Succinto embeddings reales: skip-gram Python puro sobre el corpus sí es viable para clasificación, pero la generación por similitud coseno no salió funcional en experimentos previos. Para generación, preferir modelo de transición explícito (bigramas/trigramas por sentido) sobre embeddings densos en este régimen.
- Sustrato restringido: entrenar skip-gram sobre TODO el libro puede volverse inviable en este entorno en tiempo razonable. Usar primero subcorpus por ventanas locales alrededor de la palabra focal; si hace falta, usar epoch/batch mínimos y medir densidad real antes de escalar.

## SGM vault location (CORREGIDO 2026-08-02 — SGM y LE SEPARADOS)

SGM y el DSCN-G Language Engine son pilares SEPARADOS. Solo referencias cruzadas, NUNCA
mezclar archivos. Full layout/push flow: `references/sgm_vault_layout.md` (nexus-vault-ops).
- SGM canonical: `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`
- LE canonical:  `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`
- PandoraOS (otro proyecto): `/sdcard/Hermes/nexus-vault/SHARED/PandoraOS/`
Cuando el usuario pregunta por SGM, mirar en el vault SGM (arriba) — NO en `rizoma_docs/`
(espejo de trabajo en el home del agente, invisible para el usuario) y NO en `engine_export/`
(es el LE v0.1→v0.25). En SGM/README.md va SOLO SGM + linea de cross-reference a LE;
los docs de LE (README LE, CHANGELOG, EXPLICACION_CRIOLO, RESUMEN_NOCHE) y PandoraOS docx
NO van dentro de SGM (fueron sacados el 2026-08-02).

### Estructura real SGM (as of 2026-08-02, 74 archivos en vault)

```
NOUS/DSCN-G/EXPERIMENTS/SGM/
├── README.md              ← índice maestro (separación SGM/LE al tope, SOLO SGM)
├── README_SGM.md          ← índice técnico de experimentos
├── results/experiment_registry.json  ← registry (14 entradas: 0001-0013 + 0003 stress)
├── docs/                  ← spec v1.4, roadmap, protocolo, literature_index (SOLO SGM)
├── experiments/           ← scripts (puros .py stdlib)
├── results/               ← JSON de resultados
├── phases/phase0_substrato/ , phases/phase2_inferencia/
└── lit/papers/            ← PDFs (KoPE, EWC, HippoRAG, Titans, Kanerva, VSA, Plate)
```
NOUS/DSCN-G/EXPERIMENTS/SGM/ es la FUENTE DE VERDAD. `rizoma_docs/` y `~/EXPERIMENTOS/SGM/`
son espejos en el home del agente (invisibles para el usuario) — no usarlos como ubicación
canónica. `motor/`, `decoder/`, `phase1/phase3..6/`, `tests/` del roadmap son ASPIRACIONALES
(hoy SGM es scripts en experiments/ + phases/).

### Key files by category

**Specs & docs** (in `docs/` — SOLO SGM, NO docs de LE ni PandoraOS):
- `SGM_v1_4_Especificacion_Corregida.md` — full spec (§2.3 separa duda/contradicción)
- `SGM_ROADMAP.md` — 6-phase roadmap (+ Fase 0)
- `SGM_README.md` — master index with validation status
- `Arquitectura_Pure_L2_Pandora.md` — unified SGM+NOUS+DSCN-BIO architecture
- `RIZOMA_Vision_Futuro_SGM.md` — long-term vision (speculative)
- `SGM_experiment_protocol.md` — experiment protocol
- `SGM_literature_index.md` — literature index

**Experiment results** (in `results/` + `phases/`):
- `experiment_registry.json` — central registry (14 entries: SGM_0001–0013 + 0003 stress)
- `results_exp_SGM_0002..0013.json` — individual results (phases/ duplica algunos)
- `baseline_snapshots_exp_SGM_0003_nodecore_equiv_teorica.json` — NodeCore baseline

**Scripts** (in `experiments/`):
- `run_abduce_*.py` (7 scripts: D dimensionalidad, phase dynamics v1/v2/v3, PPR, decay, XOR)
- `run_nodecore_*.py` (2 scripts: smoke test, memory benchmark)
- `run_ppr_routing.py`
- `run_doubt_stagnation.py` (exp_SGM_0013, duda)
- `t_inf_06_*.py` (3 scripts: equivalence, NodeCore port, stress test)

**Literature** (in `lit/papers/`):
- `kope_arxiv_2604.07904.pdf` — KoPE (Xiao et al., Microsoft Research Asia, April 2026)
- `hipporag_arxiv_2404.10501.pdf` — HippoRAG (NeurIPS 2024)  [nota: hay wrong_id/ con IDs malos]
- `kanerva_hdc_1988_*.pdf`, `plate_tensor_product_2003_*.pdf`, `vsa_survey_2022_*.pdf`, `titans_*.pdf`, `kirkpatrick_ewc_2017.pdf`

### SGM experiment results summary (as of 2026-08-02, 14 registry entries)

| ID | Name | Result | Key finding |
|---|---|---|---|
| SGM_0001 | nodecore_smoke_test | PASS | Grafo construido, 100 ticks sin errores |
| SGM_0002 | nodecore_memoria_benchmark | FAIL | NodeCore NO ahorra memoria en Python (1.02x), 2x lento |
| SGM_0003 | nodecore_equiv_teorica | PASS | NodeCore reproduce SGMNode sin degradación |
| SGM_0003_stress | nodecore_equiv_teorica_stress | PASS | 5000 ticks f16, sin degradación |
| SGM_0004 | ppr_multipath_routing | PASS | PPR routing acc=1.0 vs local=0.0 |
| SGM_0005 | abduce_ppr | PASS | PPR encuentra par correcto score=1.0 |
| SGM_0006 | abduce_decay | PASS | Decay mejora score 0.797→1.0 |
| SGM_0007 | abduce_xor_dimensionality | PASS | D=32 mejora pair_accuracy vs D=16 (0.0→0.1) |
| SGM_0008 | abduce_xor_phase_dynamics | FAIL | Fase v1 (cos Δφ) anula/invierte binding |
| SGM_0009 | abduce_xor_phase_dynamics_v2 | FAIL | \|cos Δφ\|: sync 0.96 pero pair_acc 0.0 |
| SGM_0010 | abduce_xor_phase_bias | FAIL | Sesgo relacional re-pondera pero no compensa D=32 |
| SGM_0011 | abduce_xor_D128 | PASS | Mejor global: D=128 + sesgo fase (score 0.354) |
| SGM_0012 | abduce_xor_phase_sigmoid | FAIL | Sigmoid no mejora, ruido D=32 es el cuello |
| SGM_0013 | doubt_stagnation_mechanism | PASS | Novelty 0.25 dispara tick 24; escala INCONCLUSA |

**Próximo (pendiente 2026-08-02):** exp_SGM_0014 (T-INF-02 `verify_contradiction`, dolor
Σ E_n > θ_refut=2.0 → CONTRADICTORIA). Luego exp_SGM_0015 (T-INF-05 integración).

### SGM experiment results summary (as of 2026-08-02, 14 registry entries)

| ID | Name | Result | Key finding |
|---|---|---|---|
| SGM_0001 | nodecore_smoke_test | PASS | Grafo construido, 100 ticks sin errores |
| SGM_0002 | nodecore_memoria_benchmark | FAIL | NodeCore NO ahorra memoria en Python (1.02x), 2x lento |
| SGM_0003 | nodecore_equiv_teorica | PASS | NodeCore reproduce SGMNode sin degradación |
| SGM_0003_stress | nodecore_equiv_teorica_stress | PASS | 5000 ticks f16, sin degradación |
| SGM_0004 | ppr_multipath_routing | PASS | PPR routing acc=1.0 vs local=0.0 |
| SGM_0005 | abduce_ppr | PASS | PPR encuentra par correcto score=1.0 |
| SGM_0006 | abduce_decay | PASS | Decay mejora score 0.797→1.0 |
| SGM_0007 | abduce_xor_dimensionality | PASS | D=32 mejora pair_accuracy vs D=16 (0.0→0.1) |
| SGM_0008 | abduce_xor_phase_dynamics | FAIL | Fase v1 (cos Δφ) anula/invierte binding |
| SGM_0009 | abduce_xor_phase_dynamics_v2 | FAIL | |cos Δφ|: sync 0.96 pero pair_acc 0.0 |
| SGM_0010 | abduce_xor_phase_bias | FAIL | Sesgo relacional re-pondera pero no compensa D=32 |
| SGM_0011 | abduce_xor_D128 | PASS | Mejor global: D=128 + sesgo fase (score 0.354) |
| SGM_0012 | abduce_xor_phase_sigmoid | FAIL | Sigmoid no mejora, ruido D=32 es el cuello |
| SGM_0013 | doubt_stagnation_mechanism | PASS | Novelty 0.25 dispara tick 24; escala INCONCLUSA |

**Key conclusion from phase series (SGM_0008–0012):** Dynamic phase as multiplier or bias of XOR binding does NOT work in this setup. Pure XOR binding (no phase) is superior. D=128 is the optimal point found. The bottleneck is noise in element-wise XOR binding, not lack of phase synchronization.

**exp_SGM_0013 (T-INF-04 duda, PASS):** `check_stagnation` (novelty = nodos únicos/ventana,
NUNCA promediar ω) detecta cadena atrapada (novelty 0.25) en tick 24; control negativo
(novelty 0.50) no dispara. `handle_doubt` escala relax→relaunch→abandon como INCONCLUSA
(NO CONTRADICTORIA). Duda y contradicción son mecanismos SEPARADOS (§2.3.1 vs §2.3.2).

**Próximo (pendiente):** exp_SGM_0014 (T-INF-02 `verify_contradiction`, dolor Σ E_n > θ_refut=2.0
→ CONTRADICTORIA, relanzar con φ_root→φ*+π, cooldown 5 ticks). Luego exp_SGM_0015 (T-INF-05).


### Phase dynamics lessons (from SGM_0008–0012, KoPE-informed)

- **Phase as binding multiplier is always wrong.** When Δφ≈π, cos(Δφ)≈-1 inverts the binding. When Δφ≈π/2, |cos(Δφ)|≈0 nullifies it. When Δφ≈0, |cos(Δφ)|≈1 gives same as static. No gain in any regime.
- **Phase as attention modulation (KoPE style) is the correct pattern.** KoPE uses phase to modulate softmax attention weights, not to multiply binding values. SGM should follow the same pattern: phase modulates attention/selection, not the binding product.
- **D dimensionalidad matters more than phase for XOR binding.** D=128 with phase-as-bias (SGM_0011) scored 0.354 vs D=32 static 0.341 — the D increase was the real driver, phase was a minor bonus.
- **Synchronization converges fast with proper params** (α=0.5, K=1.0, 2000 ticks → Δφ=0.12 rad, 93% convergence), but convergence alone doesn't improve binding if the modulation mechanism is wrong.

### KoPE paper (2604.07904) — key insight for SGM

KoPE (Xiao et al., Microsoft Research Asia, April 2026) uses Kuramoto oscillator phase synchronization as an attention mechanism in Vision Transformers. The phase modulates softmax attention weights, NOT binding values. This is the pattern SGM should follow for relational composition: phase as a soft selection mechanism in attention, not as a multiplier on the binding product.

## SGM experiment protocol (from vault)

The SGM project has its own experiment protocol (in `NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_experiment_protocol.md`)
and uses a specific ID format: `exp_SGM_XXXX_<descriptor>` (4-digit sequential, no reuse).
Each run writes results to `experiment_registry.json` (in `NOUS/DSCN-G/EXPERIMENTS/SGM/results/`)
with config, seed, hypothesis, test_target, and links to baseline/variant.

**REGLA DE UBICACIÓN (Luciano 2026-08-02):** todo SGM vive en
`NOUS/DSCN-G/EXPERIMENTS/SGM/` del vault (sdcard). NUNCA mezclar con LANGUAGE_ENGINE
(`NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`) ni con PandoraOS (`SHARED/PandoraOS/`).
Solo referencias cruzadas en README.md. Si al limpiar encontrás docs de LE/PandoraOS dentro
de SGM, MOVÉLOS a su lugar (no los borres, no los dejes).

Key SGM-specific methodology notes from the vault:
- **Test-first workflow**: write the test of equivalence/validation FIRST (e.g. T-INF-06),
  run it against baseline to capture snapshots, THEN implement the new component.
- **Smoke test before vault write**: `py_compile` + import + call every function with
  minimal data before syncing to vault. `grep "def X"` does NOT catch deleted bodies.
- **Experiment ID protocol**: globally unique IDs `exp_SGM_XXXX_<descriptor>`.
  No reusing IDs — if re-run, use `exp_SGM_XXXX_rev2`.
- **Results live in**: `phases/phase0_substrato/` or `phases/phase2_inferencia/` (y duplicados
  en `results/`). El registry central debe tener UNA entrada por experiment_id (dedup) y
  una entrada por cada JSON de resultado que exista (verificar que el 0005 no falte).
- **Duda ≠ Contradicción** (§2.3.1 vs §2.3.2): estancamiento→INCONCLUSA (novelty conteo);
  dolor acumulado > θ_refut→CONTRADICTORIA (perturbación de fase). Mecanismos separados.
- Promedio local `W=8` mezcla sentidos en texto cort/intercalado.
- Repulsión sibling incondicional produce divergencia técnica sin sentido real.
- Semillas aleatorias sin señal offline no descubren estructura real.
- Actualizar `omega` focal en cada paso del loop destruye señal incluso si los embeddings la contienen.
- Decodificador generativo por top-k similitud coseno sobre embeddings densos: no garantiza coherencia; requiere transición aprendida.
- En Don Quijote, palabras como “cabo” pueden separarse por forma gramatical/frase (“al cabo de”, “de cabo a cabo”), no por sentido polisémico. Ese clustering es artefacto de superficie; validar con generación o tokens característicos por cluster antes de declarar sentido diferenciado.
- **NO asumir que llegar a ideas parecidas a papers publicados cuenta como mejora**. La única forma de saberlo es correr tus números contra los benchmarks publicados en la misma tarea (ej. WebNLG para graph-to-text, ARC-AGI para razonamiento abstracto). Guardar la comparación de benchmarks para el experimento de auditoría (exp_SGM_0010), no darla por sentada antes.
- **KoPE (Xiao et al., arxiv 2604.07904, abril 2026)**: sincronización de fase Kuramoto como mecanismo de composición relacional en transformers. Superó ViT en ARC-AGI (+3.75 pp promedio) con la misma cantidad de parámetros. Para SGM: la fase dinámica de ω puede ser más efectiva que aumentar la dimensionalidad D sola. KoPE usa coupling data-adaptive J = softmax(q·k^T / √d) para sincronizar fases — análogo a la atención de tu DSCN-G pero con dinámica de fase explícita.

## Próximo paso típico
- Si offline no hay señal: cambiar corpus/palabra.
- Si offline hay señal y online colapsa: cambiar parametrización online antes de rediseñar arquitectura.
- Para generación: clasificador de sentido + modelo de transición explícito por sentido antes que decoder por similitud densa.
- Si el loop cerrado empeora el baseline, probar primero ruteo por sentido + memoria competitiva antes de reintentar omega focal updates.

## Workflow push incremental
- Base de push: `~/engine_export`
- Copiar primero desde `$HOME` a `engine_export/`, verificar existencia.
- `github_push_inc.py` requiere token como argumento; no está persistido en el repositorio ni en `.env`. Pedirlo al usuario solo cuando vaya a ejecutar el push, no almacenarlo en archivos de proyecto.
- Luego actualizar README/vault/nexus-vault cuando el push cierre.
