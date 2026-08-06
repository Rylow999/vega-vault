---
name: dscng-experiments
description: Procedimiento para correr experimentos del DSCN-G Language Engine (y del marco DSCN-G en general) en el entorno Android restringido de Hermes. Cubre acceso al vault vía su, python puro sin numpy, límites de stream, procesos background frágiles y la disciplina de validación incremental que usa Luciano. Trigger cuando el usuario pide "experimento v0.X", "probar si el grafo...", "language engine", o cualquier corrida medible sobre DSCN-G/nexus-vault.
---

# DSCN-G Experiments (entorno Android / Hermes CLI)

Procedimiento probado para llevar experimentos del Language Engine de DSCN-G
en el telefonito de Luciano. El objetivo es producir resultados MEDIDOS, no
afirmaciones. Cada salto se valida con un script que corre y escribe JSON.

## Restricciones del entorno (CRÍTICO, no olvidar)
- **Vault en /sdcard requiere `su -c`**. El usuario de la app (`u0_a471`) NO lee
  /sdcard. Para leer un archivo del vault: `su -c 'cat ...'` o copiarlo al home
  y luego `read_file`. `search_files` de Hermes NO recorre /sdcard bien — usar
  `find`/`su -c` por terminal.
- **Python puro, sin numpy, sin red para pip estable** en el terminal de Hermes
  (`/data/data/com.hermesagent.android/files/usr/bin/python3`, 3.13). Hay red
  para `urllib` (bajar corpus/PDF funciona) y `pip install` ocasional (pdfminer
  tardó; cryptography falló por timeout). Implementar todo en python stdlib.
- **Stream de write_file < ~8K tokens**. Archivos grandes (>8K) revientan el
  stream y el write NO se ejecuta (timeout silencioso). Dividir en write_file
  chicos + patch, o escribir el .py directo por terminal con write_file corto.
- **Procesos background: el session_id a veces desaparece** del tracker aunque el
  proc siga vivo. Para verificar si un experimento largo sigue corriendo, usar
  `pgrep -f run_vXX.py` por terminal, no confiar solo en process(poll). Si el
  log está vacío y no hay JSON, el proc pudo morir sin escribir — relanzar.
- **CPU compartida**: no lanzar 2 experimentos pesados a la vez si uno es O(N²)
  por paso (N=1000 tarda 20+ min). Validar con N chico (10-200) y pocos pasos
  PRIMERO; el N grande va en background aparte.

## Workflow estándar (validación incremental)
1. El usuario propone idea → la traduzco a hipótesis MEDIBLE (un número que suba
   o baje). Nunca "el grafo entiende" sin accuracy.
2. Escribo `run_v0X.py` en home (python puro, stdlib). Lo lanzo y espero JSON.
3. Si el resultado es "fallo", LO REPORTEO como hallazgo (no lo disfrazo). Los
   fallos de diseño (no de bug) son oro: dicen qué NO hacer. Ej. v0.7 contexto
   promediando ω empeoró porque aplastaba la señal; v0.6b dolor post-hoc no sirvió.
4. Si el usuario pide "de a poco", encadeno v0.X→v0.X+1 y no salto a la meta.
5. Al terminar, copio script + JSON al vault bajo
   `NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/v0.X_*/` con `su -c`, dueño
   `root:everybody`, perm 664.

## Anatomía de un experimento (template mental)
- Hipótesis explícita en el docstring.
- Parámetros en mayúsculas al tope (ALPHA, BETA, N_INIT, STEPS...).
- `main()` imprime ANTES y DESPUÉS de entrenar, y escribe `results_v0X.json`.
- Métrica honesta: accuracy de recuperación, tasa de inválidas, retención de
  masa, error de predicción. Comparar contra la versión previa (v0.6a 10.11%).

## Pitfalls reales de esta sesión (no repetir)
- **SMOKE TEST obligatorio antes de background** (especialmente para archivos
  escritos en partes con write_file + patch). Después de escribir un .py en
  partes, SIEMPRE correr: `python3 -c "import py_compile; py_compile.compile(
  'run_vXX.py', doraise=True); import run_vXX as m; <llamar cada funcion con
  datos minimos>"`. Esto detecta NameError (funciones borradas por patch),
  globals indefinidos, y desalineaciones antes de lanzar background. En esta
  sesion detecte 3 bugs asi (decode sin cuerpo, load_dq sin return, focus_trace
  desalineado) antes de perder tiempo. NUNCA lanzar background sin smoke test.
- **Reutilizar funciones entre experimentos con `exec()`**: para heredar
  transformer/corpus de un experimento anterior, usar
  `exec(open("run_vXXc.py").read().split("def main")[0])`. Importa todas las
  funciones/constantes SIN ejecutar main(). Evita reescibir codigo y mantiene
  consistencia. NO usar `import` (falla por guiones en el nombre del archivo).
- **Google Tatoeba 404 + Wikipedia 403 (v0.25 session).** Tatoeba `spa_sentences.tsv.gz` returned HTML 404; Wikipedia `es.wikipedia.org` returned HTML 403 instead of JSON. If retrying later, inspect bytes before decompressing. Fallback: synthetic realistic corpus with explicit sense labels worked for v0.25 v7b onward and is preferable when external corpora are unavailable.
- **OFFLINE-BEFORE-ONLINE POLYSEMY PROBE (v0.25 v7/v7b).** Before any online mechanism, run k-means silhouette/inertia on real contexts (k=2 vs k=1). If k=2 does not beat k=1, stop: no real bimodal signal for that word. Don Quijote is monosemic for most candidates; use a synthetic labeled corpus when the real one lacks structure. Seed omega0 from k-means centers; seeding helps start but does not guarantee online refinement in current config.
- **LOCAL-CONTEXT WINDOW HARD LIMIT (v0.25 v5/v6).** Averaging W neighbors or selective attention over local W cannot detect sense transitions in short/interleaved text (acc<0.50 with mixed blocks). It only works in long pure blocks, and still cannot detect A→B boundaries because W does not observe mixed transitions. Do not iterate on local W for disambiguation; the real path is long-context transformer.
- **DECODER BY EMBEDDING SIMILARITY IS NON-FUNCTIONAL; EXPLICIT TRANSITION MODEL WORKS (v0.25 v12-v13b).** Nearest-neighbor decoder over D=16 skip-gram embeddings: top1=0.020, top5=0.095, incoherent output. Bigrams on the same corpus: top1=0.630, top5=0.940, coherent generation. LECCIÓN: in small corpora with fixed templates, explicit transition models capture what dense embeddings without sequential training cannot. Next step: connect sense-conditioned generation to the sense-routing loop, not revert to embeddings for decoding.
- **SENSE-CONDITIONED GENERATION WORKS (v0.25 v14-v15).** Per-sense bigram models generate text that respects the target sense's vocabulary in this regime. A linear classifier over skip-gram + context reached acc=0.938 on test. NEXT PROBE: route sense -> delta temperature in conditioned model -> evaluate purity and human coherence, not just accuracy.
- **Loop cerrado no robusto sin baseline fuerte (v0.25 v8-v11).** El ciclo integrador puede destruir señal aunque los embeddings la tengan: baseline con skip-gram + clasificador lineal dio 0.766 en test, pero el loop cayó a 0.490. Una variante conservadora mejoró sobre su baseline débil original (0.328→0.500→0.697), pero NO generalizó a otra palabra (baseline 1.000, loop 0.500/0.447). REGLA PRÁCTICA: medir baseline con método supervisado fuerte sobre mismos embeddings antes de introducir loop; cualquier loop que empeore baseline débil es concluyente solo si mejora consistente; exigir generalización a ≥2 palabras antes de declarar mecanismo válido.
- **MODULARIZACION OBLIGATORIA DESDE v0.25 (v2_core).** Extraer `dscng_core.py` con `MetricLogger`, `SimpleTransformer`, `SkipGram`, `RootMemory`, `LinearSenseClassifier`, `build_polysemy_corpus`. Antes de extraer, backup de scripts+JSON+README en `backups_previos/`. Reescribir cada experimento como wrapper de <30 lineas importando del core. Validar con script de regresión tolerancia 5% contra resultados previos.
- **MetricLogger obligatorio desde v0.25 (v2_core).** Todo experimento nuevo debe loguear por paso `acc_pred`, `acc_gt`, `dolor`, `foco_acc`, `W_actual` y escribir `results_v0X.json` con `summary + rows`. Eso habilita comparación honesta entre versiones sin reescribir prints.
- **Smoke test con ejecutable alternativo (v0.25 v2_core).** `execute_code` puede usar intérprete con depends perdidas; para tests unitarios usar `terminal` con `python3 - <<PY` si falla linking del ejecutable de Hermes.
- **Corpus sintético expandible con augment desde v0.25 (dscng_core).** `build_polysemy_corpus` soporta `n_per_sense>=1000` y augmentación por swap de keyword aleatoria del sentido con prob 0.7. Mantiene ground truth por construcción. SEMILLA FIJA `random.Random(0)` para reproducibilidad.
- **Contracción de ventana Ecu.8 desde v0.25 (dscng_core).** Implementada en `RootMemory.contraer_ventana(W_base, kappa)=int(max(2, W_base/(1+κ·dolor)))`. Queda lista para medir si la contracción mejora recuperación post-duda; no habilitar por defecto hasta evaluar.
- **Semillas omega0 desde k-means offline (v0.25 v7b, dispositivo 8c/8d).** Offline k-means: si `silhouette/k=2 >> k=1`, portar centros como `omega0` en vez de gauss. Seeding ayuda el arranque, pero NO garantiza refinamiento online; diferenciar "falta señal en corpus" de "el mecanismo no refina".

## SGM vault location (CORREGIDO 2026-08-02 — user could not see files + SEPARACION LE)
Full corrected layout + separation rule + push flow: see `references/sgm_vault_layout.md` under nexus-vault-ops.
The CANONICAL SGM vault is `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`
(the user's real storage, opens in their file manager). `rizoma_docs/` in the agent
home (`/data/user/0/.../home/`) is ONLY a writable working mirror inside the Hermes
app sandbox — the user CANNOT open it, so never treat it as the deliverable location.
NOT `engine_export/` (DSCN-G v0.1→v0.25), NOT `~/EXPERIMENTOS/SGM/` (agent-home
sandbox, also invisible to the user). ALWAYS write the real deliverable into the
/sdcard vault using `su -c` + `chown root:everybody` so the user can see it.

SEPARATION RULE (user correction 2026-08-02): SGM and the DSCN-G Language Engine are
SEPARATE pillars. Their FILES must never be mixed — only cross-references in docs.
- SGM: `NOUS/DSCN-G/EXPERIMENTS/SGM/`  (spec v1.4, roadmap, protocolo, experiments 0001-0013)
- LE:  `NOUS/DSCN-G/EXPERIMENTS/LANGUAGE_ENGINE/`  (v0.x, polisemia, decoder, loop)
- PandoraOS: `SHARED/PandoraOS/`  (otro proyecto)
If LE docs (README LE, CHANGELOG, EXPLICACION_CRIOLO, RESUMEN_NOCHE) or PandoraOS docx
land inside SGM, MOVE them out (to LANGUAGE_ENGINE/ or SHARED/PandoraOS/) and leave only a
cross-reference line in SGM/README.md. This was enforced 2026-08-02 after a push had
leaked LE/PandoraOS/specs into SGM-CORE (fixed via DELETE API + vault MOVE).

Key SGM files in the vault `NOUS/DSCN-G/EXPERIMENTS/SGM/` (74 archivos, 2026-08-02):
- `README.md` — índice maestro (separación SGM/LE al tope, SOLO SGM + cross-ref LE)
- `README_SGM.md` — índice técnico de experimentos
- `docs/` — spec v1.4, roadmap, protocolo, literature_index (SOLO SGM; NO docs LE/PandoraOS)
- `experiments/` — scripts (run_abduce_*, run_nodecore_*, run_ppr_routing, run_doubt_stagnation, t_inf_06_*)
- `results/` + `phases/phase0_substrato/` + `phases/phase2_inferencia/` — JSON resultados
- `lit/papers/` — PDFs (KoPE, EWC, HippoRAG, Titans, Kanerva, VSA, Plate; wrong_id/ con IDs malos)
- `experiment_registry.json` — registry reconstruido 2026-08-02 a 14 entradas honestas
  (0001-0013 + 0003_stress). Tuvo duplicados (0008/0009) y faltaba el 0005; dedup + verificar.

The SGM README's target structure (`motor/`, `decoder/`, `phases/phase1_modos/`, etc.)
is aspirational — those directories do NOT exist yet (hoy SGM = scripts en experiments/ + phases/).

## SGM vault MIRROR convention (CORREGIDO 2026-08-02 — user could not see files)
The user CANNOT see anything in the agent home (`/data/user/0/.../home/`) — that
path is private to the Hermes app sandbox. The REAL vault is
`/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/`. Workflow per turn:
1. Edit/work in the agent-home working copy `rizoma_docs/` (writable by the app UID).
2. Sync to the vault with `su`:
   `su -c 'cp -r rizoma_docs/. /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/.'`
   then apply visibility:
   `su -c 'chown -R root:everybody <SGM vault path>; chmod -R u+rwX,g+rwX,o+rX <SGM vault path>'`
3. Push to GitHub SGM-CORE FROM THE VAULT (not the home mirror): `github_push_sgm.py`
   has `BASE="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM"`.
- `~/sync_vault.sh` performs steps 1-2 (home→vault, with chown). `~/EXPERIMENTOS/SGM/`
  is a REDUNDANT agent-home mirror the user cannot open — do not rely on it as the
  deliverable. Exact scripts: see references/sgm_vault_sync.md.

## Editing the experiment_registry.json under FUSE (IMPORTANT)
`write_file` / `patch` TOOLS fail with "Permission denied" on
`rizoma_docs/results/experiment_registry.json` (FUSE, root-owned path) — see
android-env-ops. To ADD or EDIT a registry entry, drive Python INSIDE `su -c`:
```sh
su -c 'LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib \
  PY=/data/data/com.hermesagent.android/files/usr/bin/python3; $PY - <<PYEOF
import json
p=".../rizoma_docs/results/experiment_registry.json"
d=json.load(open(p))
d.append(new_entry)   # or d[idx]["status"]="archived"
json.dump(d, open(p,"w"), indent=2)
print("ok", len(d))
PYEOF'
```
Never use the `patch`/`write_file` tools for this file. Same pattern for any
JSON under rizoma_docs/ on this host.

## SGM experiment protocol (from vault)

The SGM project has its own experiment protocol (in `NOUS/DSCN-G/EXPERIMENTS/SGM/docs/SGM_experiment_protocol.md`)
and uses a specific ID format: `exp_SGM_XXXX_<descriptor>` (4-digit sequential, no reuse).
Each run writes results to `experiment_registry.json` (in `NOUS/DSCN-G/EXPERIMENTS/SGM/results/`)
with config, seed, hypothesis, test_target, and links to baseline/variant.

**REGLA SEPARACIÓN (Luciano 2026-08-02):** SGM y LANGUAGE_ENGINE son pilares separados.
NUNCA mezclar archivos; solo cross-references en README.md. Si al limpiar encontrás
docs de LE (README LE, CHANGELOG, EXPLICACION_CRIOLO, RESUMEN_NOCHE) o PandoraOS docx
dentro de SGM, MOVÉLOS a `LANGUAGE_ENGINE/` o `SHARED/PandoraOS/` — no los borres ni los dejes.

Key SGM-specific methodology notes from the vault:
- **Test-first workflow**: write the test of equivalence/validation FIRST (e.g. T-INF-06),
  run it against baseline to capture snapshots, THEN implement the new component.
- **Smoke test before vault write**: `py_compile` + import + call every function with
  minimal data before syncing to vault. `grep "def X"` does NOT catch deleted bodies.
- **Experiment ID protocol**: globally unique IDs `exp_SGM_XXXX_<descriptor>`.
  No reusing IDs — if re-run, use `exp_SGM_XXXX_rev2`.
- **Results live in**: `phases/phase0_substrato/` or `phases/phase2_inferencia/` (y duplicados
  en `results/`). Registry: UNA entrada por experiment_id (dedup) + una por cada JSON que
  exista (verificar que el 0005 no falte al reconstruir).
- **Duda ≠ Contradicción** (§2.3.1 vs §2.3.2): estancamiento→INCONCLUSA (novelty conteo);
  dolor Σ E_n > θ_refut=2.0 → CONTRADICTORIA (perturbación de fase φ_root→φ*+π, cooldown 5).
  Mecanismos separados.
- Promedio local `W=8` mezcla sentidos en texto cort/intercalado.

## Auditoría de circularidad en mediciones de polisemia
Ver references/auditoria_circularidad_polisemia.md para el patrón completo:
regla de oro (ground truth + control monosémico + curva episodio), casos
documentados (v0.9c, v0.21 v8→v8f), y el veredicto de que el grafo rústico D=16
no separa sentido (acc_gt<=0.53, azar) mientras el root funciona como sistema
de duda (dolor_duda=0.841, W_contrae=0.982). PROTOCOLO OBLIGATORIO antes de
afirmar "separó sentidos": (1) GROUND TRUTH por ocurrencia; (2) NEGATIVE CONTROL
(monosémicas no deben repartirse); (3) BASELINE EN CONDICIONES IDÉNTICAS; (4)
CURVA ÉPOCA A ÉPOCA; (5) SMOKE TEST + RESULTS_JSON; (6) PERMUTACIÓN CONTROL
si es clustering. Ver references/audit_negative_control.md y references/audit_signal_removal.md.
- **Google Tatoeba 404 (v0.25 session).** `https://downloads.tatoeba.org/exports/sentences/spa_sentences.tsv.gz` returned HTML 404 in a 153-byte file with `.tsv.gz` extension, causing `gunzip` to fail. If retrying later, inspect bytes before gunzip. Practical fallback: synthetic realistic Spanish corpus with explicit sense labels worked for v0.25 v7b and is preferable when large corpora are unavailable.
- **Loop cerrado no robusto sin baseline fuerte (v0.25 v8-v11).** El ciclo integrador puede destruir señal aunque los embeddings la tengan: baseline con skip-gram + clasificador lineal dio 0.766 en test, pero el loop cayó a 0.490. Una variante conservadora (actualizar contexto, no omega focal; media móvil; umbral de foco) mejoró sobre su baseline débil (0.328→0.500) y llegó a 0.697, pero no generalizó a otra palabra con baseline 1.000 (cayó a 0.500/0.447). REGLA: calibrá el baseline ANTES del loop; loop sobre baseline débil es concluyente solo si mejora consistentemente; probá generalización a ≥2 palabras.
- **Decodificador por similitud de embeddings NO FUNCIONAL; modelo de transición explícito SÍ (v0.25 v12-v13b).** Decoder nearest-neighbor sobre embeddings D=16 arrojó top1=0.020, top5=0.095, generaciones sin coherencia. Bigramas en el mismo corpus dieron top1=0.630, top5=0.940 y generación coherente. LECCIÓN: en corpus chico con templates fijos, el modelo de transición explícito captura lo que embeddings locales sin entrenamiento secuencial no pueden.
- **Calibrar baseline FUERTE antes de medir loop (v0.25 v10-v11).** Baseline con embeddings skip-gram + clasificador lineal dio acc=0.766. El loop cayó a 0.490. Una variante conservadora mejoró sobre su baseline débil original (0.328→0.500→0.697), pero NO generalizó a otra palabra (baseline 1.000, loop 0.500/0.447). REGLA PRÁCTICA: medir baseline con método supervisado fuerte sobre mismos embeddings antes de introducir loop; cualquier loop que empeore baseline débil es concluyente solo si mejora consistente; exigir generalización a ≥2 palabras antes de declarar mecanismo válido.
- **Wikipedia/Tatoeba descentiable, fallback sintético válido (v0.25 v7b/v9/v11).** Wikipedia api.php devolvió HTML 403 en vez de JSON; Tatoeba spa_sentences.tsv.gz devolvió HTML 404. No reintentar ciegamente. Usar corpus sintético realista con etiquetas explícitas A/B y ground truth por construcción como reemplazo funcional para experimentos de polisemia cuando las fuentes externas fallan.
- **OFFLINE-BEFORE-ONLINE POLYSEMY PROBE (v0.25 v7/v7b, 2026-07-28).** Antes de lanzar un mecanismo online sobre una palabra candidata, correr k-means offline sobre sus contextos reales (silhouette/inertia k=2 vs k=1). Si k=2 NO le gana a k=1, detenerse: el corpus no tiene señal bimodal para esa palabra. Don Quijote es monosémico para la mayoría de candidatos (`banco`, `llave`, `mano`); usar corpus sintético con etiquetas explícitas si el real carece de estructura.
- **LOCAL-CONTEXT WINDOW HARD LIMIT (v0.25 v5/v6, 2026-07-28).** Promediar W vecinos o incluso atención selectiva sobre W local NO puede detectar cambio de sentido ni desambiguar en texto corto/intercalado. Verificado experimentalmente: acc<0.50 con bloques mezclados. Solo funciona en bloques largos puros, pero aún así no detecta la frontera A→B porque W no observa transiciones mezcladas. No iterar más sobre W local para desambiguación; el camino es transformer sobre contexto largo.
  lanzar un mecanismo online sobre una palabra candidata, correr k-means offline
  sobre sus contextos reales (silhouette/inertia k=2 vs k=1). Si k=2 NO le gana
  a k=1, detenerse: el corpus no tiene señal bimodal para esa palabra, ningún
  mecanismo online la encontrará. Si k=2 SÍ gana, portar los centros como semilla
  omega0 en vez de gauss(0,1). IMPORTANTE: semillar ayuda a arrancar, pero no
  garantiza refinamiento online en config actual (v7b: seeded online colapsó en
  `banco`, quedó flat en `llave`/`cabo`). El offline probe NO garantiza éxito online;
  solo separa "falta señal en el corpus" de "el mecanismo no refina la señal".
- LOCAL-CONTEXT WINDOW HARD LIMIT (v0.25 v5/v6, 2026-07-28): promediar W vecinos
  o even atención selectiva sobre W local NO puede detectar cambio de sentido ni
  disambiguar en texto corto/intercalado. Verificado experimentalmente: acc<0.50
  con bloques mezclados. Solo funciona en bloques LARGOS PUROS (A-only, luego B-only),
  pero aún así no detecta la FRONTERA A->B porque W no observa transiciones mezcladas.
  No iterar más sobre W local; el camino real es transformer sobre contexto largo.

## Estilo (de MEMORY, aplica acá)
Responder en criollo, directo, sin academicismo. Distinguir saber / hipotetizar /
no saber. Cerrar con resumen. El usuario valora rigor honesto sobre ambición de claims.
