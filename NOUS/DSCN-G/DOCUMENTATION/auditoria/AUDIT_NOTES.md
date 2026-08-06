# AUDIT_NOTES — DSCN-G v3 Paper Kit (2026-07-22)

Revisión de `verify_dscng_v3.py`, `nback_v5_grounded.py`, `generate_figure2.py`,
`analyze_results.py`, `README.md`, `paper_structure.md` y `claims_falsifiable.md`.
Todo el código se **ejecutó realmente** (no solo se leyó) en un entorno limpio,
a escala canónica (seeds=30, steps=2000 para el núcleo; n-back 1–15, 40 trials
por condición). Esta nota documenta qué estaba roto, qué se corrigió, y qué
número reclamado en la documentación se sostiene o no frente a una corrida real.

**Precedente:** esto repite el patrón encontrado en la revisión anterior del
compendio NOUS_Tecnico_v4 (Sección 14): código que, ejecutado tal cual, no
reproduce las cifras que el propio documento presenta como verificadas. Vale
la misma conclusión práctica: antes de escribir el paper con estos números,
hay que citar solo lo que la corrida real produjo.

---

## 1. Bugs que rompían el pipeline (arreglados)

### 1.1 `nback_v5_grounded.py` nunca guardaba resultados — CRÍTICO
`sweep()` calculaba todo correctamente y lo imprimía por consola, pero el
bloque `if __name__ == "__main__":` no guardaba nada en disco. `generate_figure2.py`
y `analyze_results.py` requieren `nback_v5_paper_ready.json` para poder correr.
Siguiendo el README tal cual estaba escrito ("`python nback_v5_grounded.py`"
y después "`python generate_figure2.py`"), el segundo paso fallaba siempre
con `FileNotFoundError`. El pipeline documentado, literalmente, no podía
completarse.

**Fix:** se agregó el guardado de `nback_v5_paper_ready.json` con el esquema
exacto que ya esperaban los dos scripts consumidores (`N_ss_mean`, `N_ss_std`,
`N_ss_estimates`, `n_back_results[].{n_back,bal_acc,bal_acc_std,dprime}`), más
un flag `--n-backs` para poder llegar hasta 15-back (el default original solo
llegaba a 10, pero el paper cita explícitamente `d'(15-back)`).

### 1.2 `analyze_results.py` — "desvío estándar" que no era tal
```python
print(f"  Mean ΔPLV: {c3['mean_delta_plv']:.3f} ± {np.std(c3['min_delta_plv']):.3f}")
```
`c3['min_delta_plv']` es un float único (el mínimo). `np.std()` de un solo
número siempre da 0 — el "± X" que imprimía no era un error real, aunque
tenía la forma de uno.

**Fix:** `verify_c3()` ahora también devuelve `std_delta_plv` (calculado
sobre todos los eventos) y la lista completa `all_delta_plv`; `analyze_results.py`
usa el valor real.

### 1.3 Acoplamiento de Kuramoto — no era una actualización sincrónica
```python
for i in self.nodes_active:
    ...
    for j in self.nodes_active:
        ...weight * np.sin(self.phi[j] - self.phi[i])...
    self.phi[i] = (...)   # ← escribe en el mismo array que lee `j`
```
Como la escritura de `self.phi[i]` ocurre dentro del mismo bucle exterior que
lee `self.phi[j]`, cualquier `j` que ya haya sido procesado como `i` en una
iteración anterior aporta su fase **ya actualizada**, no la fase que tenía al
empezar el step. Es un barrido tipo Gauss-Seidel, dependiente del orden de
`nodes_active` — no el step sincrónico de Kuramoto (`dφ_i/dt` evaluado sobre
`φ(t)` para todo `i` a la vez) que el modelo y el paper describen.

**Fix:** se toma una foto (`snapshot`) de φ antes de escribir nada, y todas
las actualizaciones se calculan sobre esa foto. De paso se vectorizó
(numpy broadcasting en vez de doble loop en Python): **~12x más rápido**
(216 s → 18 s en el smoke test), lo cual permitió correr la escala canónica
completa (30 seeds × 2000 steps) en ~3 minutos en vez de la ~1h30 estimada
con el código original.

---

## 2. Reclamado vs. reproducido (escala canónica, código corregido)

| Claim | Documento dice | Corrida real (30 seeds, 2000 steps) | Veredicto |
|---|---|---|---|
| **T1 — N_ss\*** | README: "~9-10 nodos". paper_structure abstract: "9.5±1.0". | **N_ss\* ≈ 4.0–4.8** según N_init (4.0/4.8/4.2) | ❌ El "9-10" / "9.5±1.0" del abstract y el README **no es el número de T1** — es el N_ss\* del modelo de N-back (otro sistema, otro θ_death, otro N). El propio `claims_falsifiable.md` ya tenía la tabla correcta (4.0/5.0/5.0) pero el resto de los documentos no la usa. |
| **T1 — cota universal y punto fijo** | ✓ verificado | ✓ se sostiene en los 3 N_init | ✅ |
| **T1 — maximalidad (iii)** | ✓ verificado | Falla ("✗ suspicious") en **los 3 N_init, siempre** | ⚠️ No es evidencia de que el teorema sea falso — es que el test en sí no es una prueba real: en vez de simular N_init=N\*+1, aproxima ρ con una fórmula (`K/n`). Nunca puede pasar como está escrito. Hay que simular la condición real o quitar la afirmación de "verificado". |
| **T2 — ω alignment** | 0.9998 | **1.0000 ± 0.0000** | ✅ Se sostiene, incluso mejor de lo reclamado. |
| **T3 — consensus rate** | "90% (27/30), 83% unimodal, 7% bimodal" | **100% (30/30)**, pero 23/30 son R≥0.9 real y 7/30 solo pasan un criterio más laxo (R≥0.5, rama "weak_unimodal"). **0/30 bimodal.** | ⚠️ El número final es "mejor" pero por una razón incorrecta: el código acepta como "consenso" un umbral más bajo que el que el propio teorema define (R≥0.9). La cifra "7% bimodal" no aparece en ninguna corrida. |
| **C3 — hijacking** | "1874 triggers (9.37% steps), **100%** de triggers con ΔPLV<−0.3, media ΔPLV=−0.462±0.089" | **2237 triggers (3.73% steps), solo 0.9% de triggers (20/2237) con ΔPLV<−0.3, media ΔPLV=−0.007±0.061** | ❌ **No se reproduce.** En promedio el mecanismo de hijacking, tal como está implementado, no aumenta el phase-locking del grupo — la media está esencialmente en cero, no en −0.46. Esta es la claim central del paper que menos se sostiene. |
| **N-back — N_ss\* empírico** | 9.5 ± 1.0 | **9.50 ± 1.02** | ✅ Se reproduce casi exacto. |
| **N-back — d'(1-back)** | 5.30 | **5.33** | ✅ |
| **N-back — d'(10-back)** | 3.12 | **3.92** | ❌ |
| **N-back — d'(15-back)** | 2.78 | **3.90** | ❌ (y el default original del script ni siquiera llegaba a 15-back — había que extender `n_backs` a mano) |
| **N-back — forma de la curva** | "degradación suave" continua hasta 15-back | Cae de 5.33→~3.9 hasta el 5-back, y **de ahí en más queda plana** (3.89–3.95 incluso extendiendo a 20-back) | ⚠️ Sigue siendo cierto que NO hay escalón abrupto (la afirmación cualitativa central — "recurso continuo, no slots discretos" — se sostiene), pero la forma real es "caída y meseta", no una caída continua hasta 2.78. Ver `figure2_nback_v5_paper.png` (regenerada con datos reales). |

---

## 3. Por qué C3 probablemente no se sostiene (hipótesis, no verificado)

T1 converge a un equilibrio de **~4-5 nodos activos** con los parámetros por
defecto (θ_death=0.10). `plv_intra_group()` calcula el order parameter sobre
`nodes_active[1:]` (todos menos la raíz) — con 4-5 nodos activos eso son
**3-4 nodos** para medir "consenso grupal". Es una población muy chica y
ruidosa para mostrar la sincronización patológica que C3 predice, y además
hay tensión directa con T1: el propio framework converge a un tamaño de
grupo que deja muy poco margen para que C3 se manifieste como se describe.
Esto es una hipótesis a partir de la estructura del código, no algo que se
haya verificado por separado — queda para quien continúe el trabajo decidir
si conviene rediseñar el trigger de hijacking, correrlo con más nodos
activos (relajando θ_death solo para ese experimento), o directamente
reportar C3 como no confirmado a estos parámetros.

---

## 4. Qué SÍ queda sólido después de esta auditoría

- El núcleo (`DSCN_G_v3`) corre sin errores, de punta a punta, a escala canónica.
- **T2 (ω alignment)** se reproduce limpiamente y hasta mejor de lo reclamado.
- **N_ss\* del N-back** (9.5±1.0) y **d'(1-back)** (5.33) se reproducen casi exactos.
- La conclusión cualitativa "memoria de trabajo como recurso continuo, sin
  escalón discreto" sigue siendo consistente con los datos reales — el
  gráfico no muestra ningún salto abrupto en ningún punto probado.
- **T1**, cota universal y condición de punto fijo: sólidas.
- El pipeline completo (núcleo → N-back → figura → análisis) ahora corre de
  punta a punta con un solo comando (`run_pipeline.sh`) en ~4 minutos.

## 5. Qué NO está listo para citarse tal cual en el paper

- El "N_ss\* ≈ 9-10" del abstract/README para T1 (es el número de otro modelo).
- La maximalidad de T1 (el test actual nunca la confirma).
- El desglose 90%/83%/7% de T3.
- **C3 completo** — la claim central de "phase hijacking" no se sostiene con
  los parámetros actuales.
- Los valores puntuales d'(10-back)=3.12 y d'(15-back)=2.78.

---

## 6. Archivos entregados

**Código corregido (ejecutado y verificado en este audit):**
- `verify_dscng_v3.py` — fix de sincronía de Kuramoto + vectorización + C3 devuelve std real
- `nback_v5_grounded.py` — fix del guardado de JSON faltante
- `generate_figure2.py` — sin cambios de lógica (solo backend headless para poder correr sin display)
- `analyze_results.py` — fix de la línea de "± std" falsa

**Orquestación:**
- `run_pipeline.sh` — corre las 4 etapas en orden con un solo comando (`--quick` para smoke test)

**Resultados reales de esta corrida (escala canónica, no aspiracionales):**
- `verification_results_v3.json`
- `nback_v5_paper_ready.json`
- `figure2_nback_v5_paper.png`

**Documentación corregida:**
- `README.md` — números de "Resultados esperados" y "Claims" actualizados a lo reproducido
- `claims_falsifiable.md` — veredictos de cada claim actualizados (verificado / no verificado / pendiente)
- `paper_structure.md` — se agregaron notas de auditoría inline en las secciones cuyos números hay que revisar antes de escribir prosa final (no se reescribió la estructura completa — esa decisión editorial queda para quien arme el paper)

## 7. Sugerencia para el agente que arma el paper

No copiar números de `paper_structure.md` / `claims_falsifiable.md` originales
sin cruzarlos primero contra `verification_results_v3.json` y
`nback_v5_paper_ready.json` de esta carpeta (son datos reales, no los
aspiracionales). Para C3 en particular, la sección 5.3 de `paper_structure.md`
("C3 as Falsifiable Prediction") necesita reescribirse o marcarse como no
soportada por el modelo actual antes de publicar nada.
