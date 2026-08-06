# Consistency Check — DOCUMENTACIÓN ↔ IMPLEMENTACIÓN ↔ EXPERIMENTOS

> Chequeo estructural hecho el 2026-07-25 al reorganizar CORE en
> THEORY/FORMALISM/IMPLEMENTATION/VALIDATION. No reemplaza la auditoría
> científica de 6 rondas (`../../DOCUMENTATION/auditoria/`); verifica que la
> reubicación de archivos no rompió ninguna referencia y que el mapa
> documentación→código→experimentos sigue siendo correcto.

## 1. Código implementa lo que dice la documentación

| Mecanismo (paper §2 / FORMALISM) | Método en `verify_dscng_v3.py` | ¿Presente? |
|---|---|---|
| Cadenas de información (Ec. 2) | `_chain_step` | ✅ |
| Dinámica de fase / acción (Ecs. 3–4) | `_update_phi`, `_von_mises_action` | ✅ |
| Vitalidad y poda (Ecs. 5–6) | `_update_vitality_and_prune` | ✅ |
| Interferencia de onda (Ec. 7) | `_wave_interference` | ✅ |
| Acoplamiento Kuramoto dinámico (§2.7) | `_apply_kuramoto_coupling` | ✅ |
| Mecanismo C3 / hijacking (§3.4) | `_apply_hijack_pull` | ✅ (vive en el mismo archivo que el núcleo — ver nota abajo) |
| T1 (§3.1) | `verify_theorem_1`, `verify_maximality_real.py` | ✅ |
| T2 (§3.2) | `verify_theorem_2` | ✅ |
| T3 (§3.3) | `verify_theorem_3` | ✅ |

**Nota sobre C3:** el mecanismo vive en la misma clase `DSCN_G_v3` que el
núcleo (no está separado a nivel de código), aunque documentalmente es
EXTENSIÓN, no CORE. Esto es coherente con el propio Core_Definition
(§5: "C3 debe considerarse... no es necesario para definir el núcleo"),
pero significa que **la separación THEORY/CORE vs EXTENSIONS es documental,
no está reflejada en la arquitectura del código**. No es un error — el
diseño experimental necesita el mismo simulador para probar ambas cosas —
pero se anota aquí para que quede explícito.

## 2. Los experimentos prueban lo que dicen probar

Verificado por muestreo: `verify_theorem_1/2/3` y `verify_c3` escriben a
`verification_results_v3.json`; los parámetros por defecto del código
(`theta_death=0.10`, `hijack_steps=15`, `eta_hijack=0.15`, `seeds=30`,
`steps=2000`) coinciden con los "parámetros de diseño originales" citados en
`../../DOCUMENTATION/auditoria/claims_falsifiable.md`. Sin discrepancias.

## 3. Referencias cruzadas rotas

Se revisaron los paths citados entre comillas invertidas en
`CORE/THEORY/00_Core_Definition.md` tras la reubicación de archivos
(00_Core_Definition.md se movió a THEORY/, CODE/ se dividió en
IMPLEMENTATION/CODE/ y VALIDATION/RESULTS/). **Pendiente:** ese documento
referencia `01_DSCN-G_Paper.md` y `03_Estado_Auditoria/...` con paths
relativos que asumían la ubicación vieja (`CORE/`, no `CORE/THEORY/`) — hay
que actualizarlos a `../01_DSCN-G_Paper.md` y
`../../DOCUMENTATION/03_Estado_Auditoria/...`. Ver siguiente commit.

## 3b. Hallazgo — `run_pipeline.sh` corre el N-back equivocado (preexistente, no causado por la reorg de hoy)

`CORE/IMPLEMENTATION/CODE/run_pipeline.sh` (pasos 2–4) llama a
`nback_v5_grounded.py` y `generate_figure2.py` por path relativo, asumiendo
que están en el mismo directorio. **No están ahí** — viven en
`../../../EXPERIMENTS/N_BACK/nback_v5_legacy_flawed/`, la versión que
`REVIEW_PENDING.md` marca explícitamente como "bug legacy, conservado por
transparencia. NO usar sus números". La versión que el paper realmente cita
(N_ss*=9.50±1.02, occurrence-aware) es
`EXPERIMENTS/N_BACK/nback_v6_corrected/nback_v6_occurrence_aware.py` +
`generate_figure2_v6.py`.

**Consecuencia:** correr `run_pipeline.sh` tal como está hoy, de punta a
punta, falla (los scripts v5 no existen en ese directorio) o, si se
copiaran ahí por error, reproduciría los números v5 legacy — no los del
paper. Esto es un problema real de reproducibilidad, no cosmético.

**No corregido en esta pasada** (es un cambio de contenido/script, no de
organización — corresponde a quien mantiene el pipeline decidir si se
actualiza el script para apuntar a v6 o se documenta como pipeline
desactualizado). Anotado para que no se pierda.

## 4. Documentos que describen módulos inexistentes

No se encontraron. `EXTENSIONS/DISCRETE_DYNAMICS/` está documentalmente
referenciada (ROADMAP, REVIEW_PENDING) pero la carpeta está vacía — no es un
módulo fantasma, es una extensión pendiente de contenido, marcada como tal
en su propio README (ver `../../EXTENSIONS/DISCRETE_DYNAMICS/README.md`).

## Veredicto

Un path relativo corregido (punto 3, ya aplicado). Un problema real de
reproducibilidad encontrado y **no corregido** (punto 3b —
`run_pipeline.sh` apunta al N-back v5 legacy, no al v6 que cita el paper) —
requiere decisión de contenido, se deja anotado en `FREEZE_CHECKLIST.md`.
La separación CORE/EXTENSIONS es rigurosa a nivel documental; a nivel de
código, C3 comparte clase con el núcleo — anotado, no bloqueante para el
freeze.
