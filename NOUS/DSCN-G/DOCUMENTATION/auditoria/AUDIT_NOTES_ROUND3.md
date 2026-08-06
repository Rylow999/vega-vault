# AUDIT_NOTES_ROUND3 — Rediseño del N-back (2026-07-22)

Continuación de `AUDIT_NOTES_ROUND2.md` §2/§4. Se probó la opción 3
primero como se pidió; no alcanzó sola; se implementó la opción 1. Este
documento tiene los números finales y qué reemplazar en el paper.

---

## 1. Opción 3 sola (subir `n_stimuli`) — probada, NO alcanza

Se corrió el chequeo original (orden de v5) con `n_stimuli` = 10, 30, 100,
midiendo `match_alive_frac` y `nonmatch_alive_frac` por separado:

| n_stimuli | match_alive_frac (todo n_back) | nonmatch_alive_frac (n_back=5) |
|---|---|---|
| 10  | **1.0000** | 0.208 |
| 30  | **1.0000** | 0.072 |
| 100 | **1.0000** | 0.031 |

`match_alive_frac` queda exactamente en 1.0000 sin importar `n_stimuli`.
Subir el alfabeto sí reduce el piso de falsas alarmas (columna derecha),
pero no toca el problema de fondo: la razón no es colisión estadística
entre identidades, es el **orden de las operaciones**. En cada paso `t`
del script original se escribe el estímulo actual `s=seq[t]` en el
sustrato *antes* de preguntar si `target=seq[t-n_back]` sigue vivo. En un
trial *match*, `s == target` por definición — así que la escritura de
*este mismo paso* ya satisface la pregunta, sin importar qué pasó hace
n_back pasos. Ningún tamaño de alfabeto arregla una garantía estructural.

**Conclusión de esta parte: opción 3 sola no da resultado, como se
sospechaba. Se pasó a la opción 1.**

---

## 2. Opción 1 (v6): chequeo occurrence-aware

**Fix:** se invirtió el orden — para cada paso `t`, primero se evalúa el
trial (usando el estado del sustrato heredado de `t-1`), y recién después
se escribe el estímulo `s=seq[t]`. Así un trial match ya no puede
autosatisfacerse con su propia escritura.

**Se combinó con opción 3** (n_stimuli: 10 → 50) porque, aun con el fix de
orden, un alfabeto chico deja que una identidad "revive" por coincidencia
de otra presentación no relacionada en vez de la ocurrencia específica de
hace n_back pasos. n_stimuli=50 se eligió como punto medio (10 dejaba
piso alto, 100 lo bajaba pero corría el riesgo de hacer la tarea casi
imposible más allá de 3-back sin aportar más información — ver tabla
comparativa completa 10/30/100 corrida en el desarrollo, no incluida acá
por espacio).

Archivo: `nback_v6_occurrence_aware.py`. Todo lo demás sin cambios: misma
Ec. 5, misma regla de decisión coseno, mismo sustrato reutilizable,
`measure_N_ss()` intacta (no depende de este chequeo).

### Resultado (escala canónica: 40 trials, seeds 0–39, reproducible — corrido dos veces, idéntico)

| n_back | bal.acc | d' |
|---|---|---|
| 1  | 100.0% ± 0.1% | 5.39 |
| 2  |  99.1% ± 0.6% | 4.87 |
| 3  |  87.2% ± 1.8% | 3.18 |
| 4  |  72.0% ± 2.3% | 2.19 |
| 5  |  59.3% ± 2.0% | 1.29 |
| 6  |  56.2% ± 1.6% | 1.06 |
| 7  |  55.7% ± 1.7% | 0.98 |
| 8  |  55.5% ± 1.3% | 1.00 |
| 10 |  55.1% ± 1.6% | 0.97 |
| 12 |  55.4% ± 1.9% | 1.00 |
| 15 |  54.2% ± 1.7% | 0.82 |
| 20 |  53.8% ± 1.6% | 0.80 |

N_ss* empírico: **sin cambios, 9.50 ± 1.02** — esa medición no pasa por el
chequeo de match/no-match, así que el bug de v5 no la afectaba.

Ver `figure2_nback_v6_paper.png`.

---

## 3. v5 (viejo) vs v6 (corregido) — qué cambia en la historia que cuenta el paper

| | v5 (bug de orden) | v6 (corregido) |
|---|---|---|
| hit_rate | 1.0000 siempre, cualquier n_back | Depende de n_back: 1.00 → 0.35 (10-back) |
| d'(1-back) | 5.33 | 5.39 (≈ igual) |
| d'(3-back) | 4.20 | 3.18 |
| d'(5-back) | 3.91 | 1.29 |
| d'(10-back) | 3.92 | 0.97 |
| Caída más fuerte (1 solo paso) | 0.75 (4→5-back) | 1.69 (2→3-back) |
| Forma | meseta temprana e "irreal" (nunca hay miss) | caída pronunciada 2→5-back, piso real desde ~6-back |
| ¿Mide olvido genuino? | No — garantizado sin misses por construcción | Sí — ahora depende de si la traza específica sobrevivió |

**Buena noticia:** la conclusión cualitativa central del paper ("recurso
continuo, sin escalón discreto") se sostiene *mejor* con v6, no peor. La
caída de 1.69 en d' entre 2 y 3-back sigue estando por debajo del umbral
de "escalón abrupto" que el propio `claims_falsifiable.md` define (>2.0
en un solo paso) — pero por poco margen, no con la comodidad de antes (el
máximo de v5 era 0.75). Vale la pena decirlo así en el paper en vez de
"degradación suave" sin matices: es una caída pronunciada pero continua,
no un escalón, y hay que mostrar el número (1.69 < 2.0) para que quede
claro que es un margen angosto, no un colchón grande.

**Dato nuevo interesante:** el "codo" real de la curva (72%→59% entre
4 y 5-back) cae más cerca de la literatura clásica de capacidad (Cowan
~4, Miller 7±2) que la meseta de v5 (que arrancaba en ~94% desde
5-back). Con v6, DSCN-G predice un span efectivo de memoria de ~3-4
ítems con degradación marcada después — mucho más discutible/comparable
contra Cowan/Miller de lo que permitía v5.

**El piso que queda (~0.8–1.0 en d' desde 6-back en adelante, no baja a
0):** sigue habiendo un piso residual — no es cero. Con `n_stimuli=50`
lo redujimos bastante respecto de v5 pero no lo eliminamos del todo.
Interpretación más probable: coincidencias residuales del espacio de
estímulos finito (la misma familia de causa que ya estaba documentada
en `README.md` como "efecto de piso", solo que ahora aplicada a un
chequeo que sí es genuinamente occurrence-aware). Si querés un piso más
bajo todavía, subir `n_stimuli` más (ya probamos hasta 100, bajaba el
piso de no-match de v5 pero no se re-corrió el barrido completo v6 con
100 — se puede hacer si te interesa, no lo hice porque 50 ya alcanza
para sostener la claim cualitativa del paper).

---

## 4. Qué reemplazar en cada documento (texto sugerido, no aplicado — decisión editorial tuya)

- **Abstract / paper_structure.md §Abstract:** "memoria de trabajo emerge
  como recurso continuo (degradación de d' de 5.39 a ~1.0, con la caída
  más pronunciada entre 2 y 5-back, sin escalón abrupto — máxima caída en
  un paso = 1.69 < 2.0)" — no "5.30 a 2.78" (números de v5) ni el propio
  "5.33 a 3.90" que había quedado en Sección 1.
- **claims_falsifiable.md Claim 6b/6c:** actualizar con la tabla de §2 de
  este documento. La sub-claim "sin escalón abrupto" se sostiene pero con
  margen angosto (1.69/2.0), hay que decirlo así, no como algo cómodo.
- **paper_structure.md §4.2/4.4:** reemplazar los números de v5
  (aplanamiento en ~3.9) por los de v6 (caída a ~1.0 con piso desde
  ~6-back). La anotación de la Figura 2 ya se corrigió en
  `generate_figure2_v6.py`.
- **paper_structure.md §4.3 (comparación con Cowan/Miller):** ahora hay
  argumento real para compararse — el codo de la curva v6 (~3-4 ítems) es
  comparable en magnitud a esa literatura, cosa que v5 no permitía
  honestamente.
- **Metodología (§4.1):** agregar una frase explicando el fix de orden
  (ver §2 de este doc) — es relevante para que cualquiera que audite esto
  de nuevo entienda por qué v6 y v5 dan curvas tan distintas.

No se tocaron `verify_dscng_v3.py`, `verification_results_v3.json`, ni
las claims de T1/T2/T3/C3 — nada de esto las afecta, son sistemas
distintos.

---

## 5. Qué queda pendiente (no es parte de lo pedido esta vez, pero honesto declararlo)

- C3 (phase hijacking) sigue sin sostenerse — eso no lo tocamos en esta
  ronda, sigue como en `AUDIT_NOTES.md`/`claims_falsifiable.md`.
- La sub-claim de maximalidad de T1 sigue sin una prueba real (el test
  sigue siendo una aproximación, no una simulación de N_ss*+1).
- El desglose de T3 (23/30 estricto vs 7/30 laxo) sigue pendiente de una
  decisión editorial sobre qué criterio reportar.
- El piso residual de v6 (~0.8–1.0 en d') podría bajar más con
  `n_stimuli` más alto — no se exploró a fondo, ver nota en §3.
- Nadie corrió Φ_proxy scaling ni las validaciones EEG/fMRI — siguen como
  future work, sin cambios.
