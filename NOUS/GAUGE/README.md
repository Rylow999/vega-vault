# GAUGE — Confinamiento No-Abeliano en Circulantes Fractales

Extension gauge del sustrato DSCN-G: teoria de gauge SU(2) en reticulado
sobre el grafo circulante fractal C_N(S), S = {1, 2, 4, ..., N/2}, con
plaquettes triangulares. Laboratorio discreto para estudiar un analogo
estructural del confinamiento — declarado honestamente como **modelo de
juguete**: NO constituye prueba del problema del Milenio de Yang-Mills.

**Paper:** [`PAPER/DSCN_G_Gauge.md`](PAPER/DSCN_G_Gauge.md)
**Verificacion:** [`verification/`](verification/) — outputs del Monte Carlo
**Licencia:** MIT · **Autor:** Luciano Benjamin Nieto (ORCID 0009-0000-8766-7243)

---

## Que hay en este repositorio

| Ruta | Contenido |
|---|---|
| `PAPER/` | El paper (con conjeturas G1-G4 etiquetadas como abiertas) |
| `gauge_mc.py` | Monte Carlo Metropolis SU(2) original (Appendix A del paper) — **sin corregir, conservado como referencia historica** |
| `gauge_instrument.py` | Instrumento corregido: geometria de loops, clasificacion, A_min por BFS |
| `gauge_sim.py` | Simulacion y estadistica del instrumento corregido |
| `run_gauge_instrument.py` | Runner con hipotesis, negative controls y criterios PASS/FAIL |
| `verify.py` | Chequea los numeros contra los artefactos en disco |
| `verification/` | Artefactos de corridas |
| `results/` | Resultados del instrumento corregido (JSON con config completa) |
| `CHANGELOG.md` | Historial de cambios y auditorias |

---

## Estado de la auditoria 2026-10-29

Una auditoria independiente (y la propia revision interna) encontro **defectos
en el instrumento original** que invalidaban la lectura "no area law" de las
corridas previas. Los defectos y su estado:

### 1. Clasificacion de los Wilson loops (CORREGIDO)

El `gauge_mc.py` original reportaba `W(1,1), W(1,2), W(1,3), W(2,2), W(2,3),
W(3,3)` como si todos fueran observables comparables. No lo son. Con
`d1=1, d2=2` (el default del script original):

- **TIPO-E** — el path contiene una arista invertida *consecutiva*, de modo
  que el factor `U . Udag` aparece contiguo y la holonomia vale
  **identicamente 1**. Verificado: `W = 1.0000000000` con desviacion
  `2.7e-15` (machine precision).
- **TIPO-V** — el path repite un vertice. El loop no es simple: no encierra
  una region de manera canonica y su "area minima" no esta definida de
  forma univoca.
- **SIMPLE** — path simple, el unico tipo comparable entre si.

La deteccion usa **reduccion de palabra** (stack-reduction de pares
consecutivos `(a,b),(b,a)`), no conteo de aristas repetidas: las matrices
SU(2) no conmutan, asi que una arista invertida *no consecutiva* NO cancela
(`A . B . C . A^-1 != I`). Verificado numericamente: con `d1=1,d2=2` el loop
`(2,2)` invierte la arista `(2,4)` en los pasos 2 y 6 (no contiguos) y da
`W = -0.749`, no 1.

Con `d1=1, d2=4` (generadores linealmente independientes) **todos** los
loops usados son SIMPLE.

### 2. Generadores degenerados (CORREGIDO)

`d1=1, d2=2` no genera un "rectangulo": en `Z_N`, `+2 = 2*(+1)`, los dos
generadores son colineales. El instrumento usa por defecto `d1=1, d2=4`.

### 3. Estadistica (CORREGIDO)

El error del script original era `std / sqrt(n)`, que ignora la correlacion
temporal. Con `tau_int` ~ 15-25, el error real es ~5-6x mayor. El
instrumento reporta:

- error por **bloques** (16 bloques),
- `tau_int` por autocorrelacion truncada,
- `N_eff` (muestras efectivas),
- z-score de cada observable contra 0.

Ademas reporta `W` (con signo) y `|W|` (sin signo): con signo hay
cancelacion entre superficies de orientaciones opuestas; `|W|` es el
observable de area law.

### 4. Area minima por BFS (NUEVO)

El "area" de la Definicion 2.7 del paper se computa ahora por BFS exacto
sobre el 2-complejo: `A_min(C)` = minimo numero de triangulos `S` con
`borde(S) = C` (mod 2). El BFS usa toggle (agregar o quitar triangulos) y
arranca desde los triangulos incidentes a `C` (el estado vacio tiene borde
vacio y no se puede expandir).

Verificado para `N=16, d1=1, d2=2`: `A_min(1,1)=2`, `A_min(1,2)=4`,
`A_min(1,3)=6`. Con `d1=1, d2=4`: `A_min(1,1)=6`, `A_min(2,1)=4`,
`A_min(2,2)=6`, `A_min(3,1)=6`.

### 5. Lo que NO se cambio

- El **Teorema 4.1** (`<W(C)> = (beta/4)^A`) se verifico por integracion
  exacta sobre la superficie minima: el coeficiente leader medido es
  `(1/2)^A` (1.0022, 1.0113, 0.9503 para A=2,4,6), luego
  `<W> = (1/2)^A . (beta/2)^A = (beta/4)^A`. **La constante del paper es
  correcta.**
- La derivacion escrita en el **Paso 5** tiene un factor `2^A` perdido en la
  ultima linea (el conteo de links internos `A-1` y la combinacion final no
  cierran). El *resultado* afirmado es correcto; la *algebra escrita* no.
  Ver `CHANGELOG.md`.

---

## Como correr

```bash
# smoke test rapido
python3 run_gauge_instrument.py --quick --seeds 1

# corrida completa
python3 run_gauge_instrument.py --seeds 2 --n-therm 1500 --n-meas 12000 \
    --out results/gauge_instrument_N16.json

# verificar todos los numeros contra los artefactos
python3 verify.py
```

Requisitos: `numpy`. `verify.py` devuelve exit code != 0 si algo falla.

---

## Resultados principales (instrumento corregido)

Ver `results/gauge_instrument_N16.json` para los numeros completos (config,
geometria por loop, errores por bloques, tau_int, N_eff, z-scores).

La estructura cualitativa se reproduce: la plaquette sube de ~0 a ~0.87 con
beta. Lo que cambia respecto de las corridas originales es **el error
real** (era ~6x subestimado) y **que solo se miden loops comparables**.

## Que falta (priorizado)

1. **G1 con la instrumentacion correcta**: extraer `sigma(beta)` de los loops
   SIMPLE usando `A_min` real, no `R*T`. El ajuste `log W = -sigma RT -
   alpha (R+T)` que propone el paper (§11.1) no puede funcionar: `R*T` no es
   el area, y el area minima depende de la orientacion del loop.
2. **Teorema 4.2 (weak coupling)**: el coeficiente de `1/beta` medido en la
   plaqueta es **1.287** (estable en beta=10,20,40,80), mientras el paper
   predice `3*C_F = 2.25` con `C_F=3/4`. No reproduce: recalibrar o marcar
   como no reproducido.
3. **Definicion 2.7**: el 2-complejo tiene `chi = N/2` (8 en N=16, 512 en
   N=1024), muy por encima de 2 — no-manifold. "Superficie minima con
   borde C" no tiene minimo canonico sin fijar la cadena (Z_2/R) y el
   embedido. Ver Lemoine, arXiv:2604.16252, para el marco correcto.
4. **Lemma 3.2**: el paper reporta `|P|/N = 1.25, 3.00, 4.00, 5.00`; la
   formula exacta es `|P_m| = N(m-1)`.
5. **Tabla 7.1**: regenerar desde los artefactos (el paper y el artefacto
   no son la misma corrida; hay diferencias de hasta 31% en plaquette).
6. **Conjetura G2 + Nair (arXiv:2608.10133)**: el puente espectral es
   genuino pero el espacio de Hilbert de `H_KS` sobre 56 aristas truncado a
   `j <= j_max` es `3^56`-dimensional. Es un problema formidable, no una
   linea de dos meses.

## Papers hermanos

- [`NOUS/QUANTUM`](../QUANTUM/) — sustrato base (Lemma 4.1: lambda2=4, heredado)
- [`NOUS/COSMOS`](../COSMOS/) — flujo RG logaritmico compartido
- [`Master-Document/Gap_G1_Derivation.md`](../../Master-Document/Gap_G1_Derivation.md) — derivacion del gap G1

## Cita

```bibtex
@misc{nieto2026gauge,
  author = {Nieto, Luciano Benjam{\'i}n},
  title  = {DSCN-G-Gauge: Non-Abelian Confinement on Fractal Circulant
            Graphs as a Discrete Yang-Mills Analog},
  year   = {2026},
  url    = {https://github.com/Rylow999/vega-vault/tree/main/NOUS/GAUGE}
}
```
