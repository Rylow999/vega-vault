# AUDIT_NOTES_ROUND2 — DSCN-G v3 Paper Kit (segunda pasada, 2026-07-22)

Continuación de `AUDIT_NOTES.md`. Esta pasada tuvo dos partes:

1. **Reproducción independiente** de la primera auditoría, corriendo el
   pipeline completo desde cero en un entorno limpio distinto.
2. **Revisión adicional** de `nback_v5_grounded.py` buscando problemas que
   la primera pasada no haya cubierto (no se había mirado esa lógica en
   detalle, solo el bug de guardado de JSON).

---

## 1. Reproducción independiente de AUDIT_NOTES.md — CONFIRMADA

Se corrió `verify_dscng_v3.py --seeds 30 --steps 2000` y
`nback_v5_grounded.py --n-backs 1 2 3 4 5 6 8 10 12 15 --n-trials 40` desde
cero, en un entorno separado. Los JSON resultantes son **idénticos byte a
byte** a `verification_results_v3.json` y `nback_v5_paper_ready.json`
entregados (comparación por igualdad de diccionarios tras `json.load`,
no solo "cerca"). Esto es esperable porque la simulación es determinística
(seeds fijas) pero confirma que los números de `AUDIT_NOTES.md` no son
aspiracionales ni dependientes del entorno — son exactamente lo que el
código produce. La Figura 2 regenerada también coincide.

**Conclusión: la primera auditoría es confiable. Lo que sigue es nuevo.**

---

## 2. Hallazgo nuevo (importante): el N-back no mide lo que el nombre sugiere

**Método:** se instrumentó `run_trial()` para registrar, en cada trial,
si la traza del "target" (el estímulo de hace `n_back` pasos) seguía viva
en el momento de la consulta — separado por trials *match* y *non-match* —
y para qué n_back esto cambia. Rango probado: 1 a 80.

| n_back | target vivo en trials MATCH | target vivo en trials NON-MATCH |
|---|---|---|
| 1  | 100.0% | 97.9% |
| 5  | 100.0% | 20.9% |
| 10 | 100.0% | 21.6% |
| 15 | 100.0% | 21.5% |
| 20 | 100.0% | 19.9% |
| 30 | 100.0% | 18.9% |
| 50 | 100.0% | 23.0% |
| 80 | 100.0% | 19.9% |

**El problema:** en un trial *match*, la traza del target sigue viva el
**100% de las veces, para cualquier n_back probado hasta 80**. Esto pasa
porque el chequeo de "vivo" es *por identidad de estímulo* (`tag == target`),
no *por ocurrencia específica*. Con solo `n_stimuli=10` identidades
posibles reciclándose en una secuencia de 300 pasos, la identidad
`target` casi siempre fue reescrita por **alguna otra presentación más
reciente** de ese mismo estímulo (no la que el n-back está preguntando),
así que su traza nunca muere de verdad dentro del rango probado.

**Consecuencia directa:** `hit_rate = 1.0000` en el 100% de los 40 trials,
para los 4 n_back chequeados en detalle (1/5/10/15) — nunca hay un solo
miss. Esto ya se ve indirectamente en `nback_v5_paper_ready.json` (todas
las balanced accuracy son consistentes con `bal_acc = 1 − fa_rate/2`, es
decir, dependen solo de la tasa de falsas alarmas), pero no está señalado
en ningún documento del kit — README, claims_falsifiable.md y
paper_structure.md hablan de "degradación de d'" como si reflejara olvido
progresivo de la traza específica, y no es eso lo que está pasando.

**Lo que realmente genera la curva:** toda la caída de d' viene del lado
de falsas alarmas, y tiene una causa mecánica clara:
- En trials *non-match*, la probabilidad de que la identidad `target`
  siga viva cae de 97.9% (1-back) a ~20% (5-back) y **se estabiliza ahí**
  (18.9%–23.0% incluso a 80-back) — esto es lo que se aplana, no una
  propiedad de memoria de trabajo.
- Cuando la traza está viva, la tasa de falsa alarma es ~0% (los vectores
  canónicos de los 10 estímulos están bien separados: similitud coseno
  máxima entre pares = 0.80, por debajo del criterio 0.85 — verificado
  directamente).
- Cuando la traza murió, se compara contra un nodo aleatorio del sustrato,
  lo cual da una tasa de falsa alarma "piso" de ~13–17% (consistente con
  la nota metodológica que ya existe en `README.md` sobre efecto de piso,
  pero ahora medida directamente en vez de solo hipotetizada).
- El producto de estos dos factores (probabilidad de caer en la rama
  "muerta" × ~15% de falsa alarma en esa rama) reproduce la forma completa
  de la curva: sube rápido de 1 a 5-back y se aplana después, porque el
  primer factor se estabiliza ahí.

**Por qué importa para el paper:** la sección 4 (Working Memory as
Emergent Continuous Resource) y la Figura 2 se presentan como evidencia de
que la memoria de trabajo decae como recurso continuo con la carga
(n_back). Lo que el experimento realmente mide es: *¿sigue "vigente" en
algún lugar del sustrato compartido la identidad de un estímulo, dado que
solo hay 10 identidades posibles reciclándose todo el tiempo?* — una
cantidad relacionada con el diseño del alfabeto de estímulos, no con la
distancia temporal n_back específica que se le pregunta al modelo. La nota
de "efecto de piso" que ya existe en `README.md` apuntaba en esta
dirección pero la trataba como una salvedad menor sobre la meseta final;
esto muestra que el mismo mecanismo explica **toda la curva**, no solo la
cola.

**No se tocó el código de la lógica experimental** — esto es una cuestión
de diseño (qué significa "vivo" para el chequeo de match), no un bug con
una corrección única y obvia. Ver §4 para las opciones.

---

## 3. Hallazgos menores (sí corregidos en el código adjunto)

### 3.1 `nback_v5_grounded.py` importa `DSCN_G_v3` pero nunca lo usa

El docstring del archivo dice "grounded directly in DSCN_G_v3's own
vitality/omega substrate". El código nunca instancia `DSCN_G_v3` — reimplementa
a mano la Ec. 5 (decaimiento de vitalidad) y la representación ω
d-dimensional, con parámetros propios (`gamma=0.20, theta_death=0.15`,
distintos de los defaults del núcleo). Es una reimplementación paralela
de la misma ecuación, no una corrida sobre la instancia compartida. Esto
ya estaba parcialmente declarado en la nota metodológica del README
("misma fórmula... aplicada aparte"), pero el título del docstring y el
README overclaimean "grounded ... en el sustrato" de un modo que sugiere
integración directa. Corregido: se sacó el import no usado y se ajustó el
docstring para describir con precisión qué comparte (la ecuación, la
representación) y qué no (la instancia, el pruning permanente — esto
último ya estaba declarado).

### 3.2 Corrección de d' usa el denominador equivocado para la tasa de falsas alarmas

```python
def z(p):
    p = min(max(p, 1.0 / (2 * n_match)), 1 - 1.0 / (2 * n_match))
    return norm.ppf(p)
dprime = z(hit_rate) - z(fa_rate)
```

La corrección log-lineal estándar (Hautus, 1995) para evitar z(0)/z(1)
debería usar el N de *cada* condición: `n_match` para `hit_rate`,
`n_nonmatch` para `fa_rate`. El código usa `n_match` para ambas. Corregido
en el archivo adjunto. **Impacto medido:** máximo +0.009 en d'(1-back),
0.000 en 5/10/15-back (40 trials, seeds 0–39) — no cambia ninguna
conclusión ni justifica re-correr el pipeline completo, pero vale
corregirlo para no arrastrarlo.

---

## 4. Decisión pendiente (para vos, no la tomé por mi cuenta)

El hallazgo de §2 es más de fondo que los del audit anterior porque toca
la validez de constructo del experimento central de la Sección 4 del
paper, no solo un número puntual. Veo tres caminos, sin inclinarme por
ninguno porque implica una decisión de diseño experimental:

1. **Rediseñar el chequeo de "vivo" para que sea por ocurrencia, no por
   identidad** — ej. taggear con `(t, estímulo)` en vez de solo
   `estímulo`, o usar `n_stimuli` mucho más grande que `n_back` máximo
   para que el reciclado de identidades no enmascare el olvido de la
   ocurrencia específica. Esto SÍ mediría decaimiento temporal genuino,
   pero cambia el experimento y hay que volver a correr y reescribir la
   Sección 4 con números nuevos.
2. **Mantener el experimento tal cual pero reencuadrar honestamente qué
   mide** — no "memoria de trabajo con carga n_back", sino algo como
   "discriminabilidad de identidad en un sustrato compartido con alfabeto
   finito", y mover la interpretación fuerte de "recurso continuo" a
   Limitations. Más rápido, pero es una claim bastante más débil que la
   que el paper quiere hacer.
3. **Aumentar `n_stimuli`** (ya que con 10 identidades y 300 pasos el
   reciclado es casi inevitable) y ver si con, digamos, 50–100 estímulos
   posibles el `nonmatch_alive_frac` deja de saturar en ~20% y empieza a
   depender de n_back de un modo más limpio — la corrección más barata de
   probar antes de rediseñar todo.

Puedo implementar cualquiera de las tres si me decís cuál preferís — la
2 no requiere tocar código; la 1 y la 3 sí, y ambas van a dar números
distintos a los que ya están en `nback_v5_paper_ready.json` y Figura 2,
así que no las corrí sin que decidas primero.

---

## 5. Archivos entregados en esta pasada

- `nback_v5_grounded.py` — import no usado sacado, docstring corregido,
  fix del denominador de corrección de d' (§3.1, §3.2). **Sin cambios en
  la lógica experimental** — los números publicados en
  `nback_v5_paper_ready.json` siguen siendo válidos tal como están.
- Este archivo (`AUDIT_NOTES_ROUND2.md`).

No se tocaron `verify_dscng_v3.py`, `generate_figure2.py`,
`analyze_results.py`, `run_pipeline.sh`, ni los JSON/PNG de resultados —
no encontré nada más que corregir en ellos en esta pasada.
