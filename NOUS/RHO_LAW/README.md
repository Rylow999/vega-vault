# RHO_LAW — La ley de rho como principio trans-dominio

**Tesis:** la ley de rho (colapso del observador cuando n_codevectors ~
dimension) no es un fenomeno de VSA. Es un miembro de una FAMILIA de
singularidades por "saturacion del observador" que aparece en dominios
distintos.

**Formalizacion completa:** [`docs/ESTRUCTURA_TRES_CAPAS.md`](docs/ESTRUCTURA_TRES_CAPAS.md) —
la estructura de tres capas (sustrato / observador / instrumento), los
teoremas de la capa 1 por dominio, el hueco ensemble-orbita, los mecanismos
de autorregulacion y el punto irreducible.

**Nota de estructura (2026-10-15):** este directorio vivia como referencia
rota (submodulo sin entrada en .gitmodules) y quedaba vacio en el vault.
Se inlineo el contenido del repositorio canonico
[`Rylow999/rho-law`](https://github.com/Rylow999/rho-law) para que la carpeta
sea autocontenida. El repo canonico sigue siendo la fuente de verdad.

## Estructura

- `domains/` — una carpeta por dominio con su manifestacion de la ley
- `experiments/` — codigo corriendo cada manifestacion (+ JSON de resultados)
- `data/` — datos de los experimentos Collatz / turbulencia / VSA
- `figures/` — figuras generadas por los experimentos
- `docs/` — analisis y referencias cruzadas

## Los dominios (con datos en disco)

| Dominio | Parametro admisible | Umbral | Tipo de transicion | Estado |
|---|---|---|---|---|
| VSA/HRR | rho = n_cv/dim | kappa* ~ 5.8e3 (banda [1e3,1e4]) | puntual (ancho cero) | con datos (repo fhrr-rho-collapse) |
| HRR real | rho | idem (anti-resonancia) | puntual | con datos |
| BSC binario | rho | idem (gram 0.28 vs puro 1.0) | puntual | con datos |
| LiDAR | clusters/voxel | rho>1 colapsa (gram 1.0 -> 0.33) | puntual | con datos |
| SDDF (turbulencia) | kappa del corte | banda ~1e3-1e4 | no-monotona (oscilante) | con datos (repo sddf) |
| Collatz | f_P = visitas_P/N | f_P* = 0.7075 = log4(8/3), cond. LEH | gradual (rampa) | con datos (`data/`, `experiments/`) |

## El hallazgo clave de Collatz

- El null correcto (P=1/3 + racimos geometricos, la misma estructura del
  mapa) SI cancela la desviacion como predice CLT (b = -0.472 ~ -0.5).
- Collatz cancela MAS LENTO: b = -0.264. GAP +0.21: acumula mas desviacion
  que el azar equivalente — hay sustrato real, no solo azar.
- La cola existe: 135/100.000 orbitas con |f_P - 1/3| > 0.15, todas
  convergen (hasta n = 2e6).

**El teorema a buscar (formulacion corregida):** la acumulacion sobre el
azar es sustrato real; lo que falta es la ACOTACION
|f_P - 1/3| <= C para toda orbita, con C < f_P* - 1/3 = 0.374.
Esa acotacion (si es cierta) + el umbral condicional = la conjetura cae
como corolario. Es un enunciado de teoria ergodica estandar, mas debil que
LEH y mas atacable. Trabajo formal actual:
[`Rylow999/collatz-last-theorem`](https://github.com/Rylow999/collatz-last-theorem)
(A1-A8 probados; cierre condicional a [H]; A6 formalizado en Lean 4 con
Mathlib — 9 teoremas sin sorry tras la correccion de 2026-10-15).

## La tesis filosofica

Tres capas: **sustrato irreducible** -> **observador** (f_P, decoders, G[u])
-> **instrumento** (grilla, kappa, forzado). El colapso vive en las capas
2-3; la capa 1 es invariante. Un resultado negativo ("la senal no contiene
esa informacion") puede ser un artefacto de las capas 2-3: antes de
publicarlo, probar al menos dos clases de observadores.

## Experimentos cruzados

- `experiments/exp_ns_multi_observer.py` — 20 espectros SDDF x 5 observadores
- `experiments/exp_collatz_multi_observer.py` — 161 orbitas x 3 observadores
- `experiments/exp_collatz_forzado.py` — el forzado de observador NO genera
  divergencia real (termination 1.00 en todos los epsilon)

## Cita

```bibtex
@misc{nieto2026rholaw,
  author = {Nieto, Luciano Benjam{\'i}n},
  title  = {RHO_LAW: The rho Law as a Trans-Domain Principle},
  year   = {2026},
  url    = {https://github.com/Rylow999/rho-law}
}
```
