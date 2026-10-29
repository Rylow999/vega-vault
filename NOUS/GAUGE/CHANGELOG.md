# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [2026-10-29] — Auditoria del instrumento: loops no comparables, estadistica subestimada, area no canonica

### Agregado
- `gauge_instrument.py` — geometria corregida del sustrato:
  - `classify_loop()`: clasifica cada loop como SIMPLE / TIPO-E / TIPO-V.
    TIPO-E = la holonomia vale 1 identicamente (arista invertida
    *consecutiva*, detectada por reduccion de palabra). TIPO-V = el path
    repite un vertice. Solo los SIMPLE son comparables entre si.
  - `area_min_bfs()`: `A_min(C)` por BFS exacto sobre el 2-complejo, con
    toggle y arranque desde los triangulos incidentes a C.
- `gauge_sim.py` — simulacion y estadistica: errores por bloques (16),
  `tau_int` por autocorrelacion truncada, `N_eff`, z-score, y observacion
  dual `W` / `|W|`.
- `run_gauge_instrument.py` — runner con hipotesis pre-registradas, negative
  controls y criterios PASS/FAIL explicitos.
- `verify.py` — chequea los numeros contra los artefactos en disco, con
  exit code. Portable.
- `results/` — resultados JSON con config completa, geometria por loop,
  errores, tau_int, N_eff y veredictos de los checks.

### Corregido
- **Clasificacion de loops.** El `gauge_mc.py` original promediaba
  observables NO COMPARABLES. Correccion importante: la deteccion por
  "arista repetida" (primera version) era incorrecta — con `d1=1,d2=2` los
  loops `(2,2)` y `(3,1)` NO repiten ninguna arista; repiten vertices. Y la
  deteccion por "arista invertida" tampoco basta: las matrices SU(2) no
  conmutan, asi que una arista invertida NO consecutiva no cancela
  (`A.B.C.A^-1 != I`). Verificado: `(2,2)` con `d1=1,d2=2` invierte la
  arista `(2,4)` en los pasos 2 y 6 (no contiguos) y da `W = -0.749`.
  La deteccion correcta es por reduccion de palabra.
- **Generadores.** `d1=1, d2=2` son colineales en `Z_N` (`+2 = 2*(+1)`): el
  "rectangulo" no es un rectangulo. El instrumento usa `d1=1, d2=4`.
- **Errores estadisticos.** El original reportaba `std/sqrt(n)`, que ignora
  la correlacion temporal. Con `tau_int` ~ 15-25 el error real es ~5-6x
  mayor. Ahora: bloques + tau_int + N_eff reportados.
- **Area.** Se computa `A_min` real por BFS en vez de asumir `R*T`.

### Verificado (sin cambios)
- **Teorema 4.1**: la constante del paper es CORRECTA. Integracion exacta
  sobre la superficie minima: coeficiente leader medido = `(1/2)^A`
  (1.0022, 1.0113, 0.9503 para A=2,4,6), luego
  `<W> = (1/2)^A . (beta/2)^A = (beta/4)^A`. Confirmado por MC en la red
  completa: `<plaq>` vs `beta/4` con z = +0.67, +1.03, -0.53 en
  beta=0.1, 0.05, 0.01.
- **Grafo**: `|edges|` y `|triangulos|` exactos para N=16 y N=64.
- **Clasificacion**: 16 loops TIPO-E testeados, todos con `W = 1` exacto
  (desviacion maxima `2.7e-15`).

### Nota honesta (correccion de un hallazgo previo)
- Una version anterior de esta auditoria afirmaba que el Teorema 4.1 tenia
  la constante mal (factor `2^A`). **Era un error aritmetico del auditor**:
  el coeficiente leader `c` multiplica a `(beta/2)^A`, no a `beta^A`, y se
  habia comparado contra `(1/4)^A` (unidades distintas). Corregido: el
  Teorema 4.1 es correcto.

### Pendiente (defecto real, no corregido)
- **Paso 5 del Teorema 4.1**: la derivacion escrita tiene un factor `2^A`
  perdido en la ultima linea. El conteo del Paso 4 (`A-1` links internos,
  verificado: `E_int = 1, 3, 5` para `A = 2, 4, 6`) es correcto; la
  combinacion final
  `(beta/2)^A . (1/2)^{A-1} . 2/2 = (beta/4)^A` no cierra (da `2^A` veces
  mas). El *resultado* afirmado es correcto; la *algebra escrita* no.
  Correccion de un renglón, pendiente de aplicar al paper.
- **Teorema 4.2 (weak coupling)**: el coeficiente de `1/beta` medido en la
  plaqueta es **1.287** (estable en beta=10,20,40,80), el paper predice
  `3*C_F = 2.25` con `C_F=3/4`. No reproduce.
- **Definicion 2.7**: el 2-complejo tiene `chi = N/2` (no-manifold), asi que
  "superficie minima con borde C" no tiene minimo canonico. Requiere fijar
  cadena y embedido; ver Lemoine arXiv:2604.16252.
- **Lemma 3.2**: el paper reporta `|P|/N = 1.25, 3.00, 4.00, 5.00`; la
  formula exacta es `|P_m| = N(m-1)`.
- **Tabla 7.1**: el paper y los artefactos no son la misma corrida
  (diferencias de hasta 31% en plaquette).
- **Ajuste §11.1 item 3**: `log W = -sigma RT - alpha(R+T)` no puede
  funcionar: `R*T` no es el area, y `A_min` depende de la orientacion del
  loop.

### Contexto externo (verificado)
- **Lemoine, arXiv:2604.16252** — "Universal dualities for Wilson loops in
  lattice Yang-Mills". Expansion gauge/cadena sobre *decorated spanning
  surfaces`; es el marco correcto para reparar la Definicion 2.7.
- **Nair, arXiv:2608.10133** — "Towards a Proof of Mass Gap in 3d Yang-Mills
  Theory". El puente con G2 (`Delta_gauge >= c sqrt(lambda_2)`) es
  conceptual, pero el paper mismo admite que son objetos distintos.
- **arXiv:2506.00284** — es de **D.C. Jacobsen** (no "Serafini et al.").
- **Auditoria externa (Qwen)**: su claim central — que la discrepancia de
  ~100x en acoplamiento fuerte es "entropia de superficies" publicable —
  **no se sostiene**. Con `n_meas=6000` y errores por bloques, `W(1,1)` en
  beta=0.1 da `+0.01395 +- 0.01412` (z=0.99): indistinguible de cero. El
  "0.062" citado venia de 500 muestras con error naive; ademas los dos
  artefactos del vault dan **signos opuestos** para el mismo beta=0.1
  (N=16: +0.0621; N=64: -0.0089).

## [2026-10-25] — N=64: primera corrida a mayor tamano

### Agregado
- `verification/gauge_mc_N64_output_2026-10-25.txt` — MC Metropolis en N=64
  (|S|=6, 352 aristas, 320 plaquettes), seed 42, 500 termalizacion + 500
  medicion, 11 betas 0.1-10 (fino cerca de beta_c~2.5). Reproduce la
  estructura cualitativa de N=16: plaquette 0.029 -> 0.863, loops crecientes,
  saturacion ~0.86 en beta=10.

### Nota honesta
- El area law SIGUE sin establecerse por MC: en beta=10 la plaquette satura
  0.863 (no ~1) y W(2,2) ~ W(1,1) (los loops NO decaen con el area en este
  rango). La senal de confinamiento queda demostrada solo en los regimenes
  asintoticos del paper (character expansion / gaussiana). Pendiente:
  heat bath Kennedy-Pendleton y ratios de Creutz con errores < 5% en el
  lado de acoplamiento fuerte (beta < beta_c), donde la extraccion de
  sigma(beta) es viable.
- **Nota retrospectiva (2026-10-29):** esta conclusion queda MATIZADA. Los
  loops comparados eran solo dos (`W(1,1)` y `W(2,2)`), y `W(2,2)` con
  `d1=1,d2=2` es TIPO-V (no simple). Ademas los errores no se reportaron.
  El "no area law" era, en parte, un artefacto de instrumento.

## [2026-10-15] — Reproduccion cruzada del Monte Carlo

### Agregado
- `verification/gauge_mc_output_2026-10-15.txt` — segunda corrida
  independiente del `gauge_mc.py` original (sin modificaciones), en otro
  host: plaquette -0.02 -> 0.87 con beta, Wilson loops crecientes.
  Reproduce la corrida del 2026-10-11 (misma estructura cualitativa).

### Corregido
- README: explicitado que el MC actual NO establece area law (la plaquette
  satura ~0.87 en beta=10 y los loops no decaen con el area en este rango);
  la senal de confinamiento queda demostrada solo en los regimenes
  asintoticos del paper (character expansion / aproximacion gaussiana).

## [2026-10-11] — Auditoria Metodo Integral + primer run real

### Agregado
- `gauge_mc.py` extraido del Apendice A del paper (antes vivia solo como
  texto dentro del markdown) y EJECUTADO por primera vez.

## [2026-06] — Paper original

### Agregado
- Formulacion SU(2) sobre C_N(S); conjeturas G1-G3; teoremas 4.1/4.4.2 en
  regimenes asintoticos; taxonomia de tres regimenes (Tipo I/II/III).
