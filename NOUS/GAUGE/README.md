# GAUGE — Confinamiento No-Abeliano en Circulantes Fractales

Extension gauge del sustrato DSCN-G: teoria de gauge SU(2) en reticulado
sobre el grafo circulante fractal C_N(S), S = {1, 2, 4, ..., N/2}, con
plaquettes triangulares. Laboratorio discreto para estudiar un analogo
estructural del confinamiento — declarado honestamente como **modelo de
juguete**: NO constituye prueba del problema del Milenio de Yang-Mills.

**Paper:** [`PAPER/DSCN_G_Gauge.md`](PAPER/DSCN_G_Gauge.md) (ingles)
**Verificacion:** [`verification/`](verification/) — output del Monte Carlo
**Licencia:** MIT · **Autor:** Luciano Benjamin Nieto (ORCID 0009-0000-8766-7243)

---

## Que hay en este repositorio

| Ruta | Contenido |
|---|---|
| `PAPER/` | El paper (con conjeturas G1-G4 etiquetadas como abiertas) |
| `gauge_mc.py` | Monte Carlo Metropolis SU(2) (extraido del Apendice A del paper) |
| `verification/gauge_mc_output_2026-10-15.txt` | Output de la corrida de verificacion |
| `CHANGELOG.md` | Historial de cambios y auditorias |

## Resultados principales

Monte Carlo Metropolis en tres corridas independientes: N=16 x2 (Arch
2026-10-11; Windows 2026-10-15) y N=64 (Arch 2026-10-25, seed 42, 500+500
sweeps, 11 betas). Todas reproducen el mismo comportamiento cualitativo
(N=64: plaquette 0.029 -> 0.863, saturacion ~0.86 en beta=10). Tabla N=16:

| beta | plaquette (norm.) | W(1,1) | W(2,2) |
|---|---|---|---|
| 0.1 | 0.033 | 0.062 | -0.025 |
| 1.0 | 0.235 | 0.037 | 0.051 |
| 2.0 | 0.462 | 0.213 | 0.155 |
| 5.0 | 0.742 | 0.492 | 0.481 |
| 10.0 | 0.869 | 0.739 | 0.750 |

Lectura: la plaquette sube de ~0 a ~0.87 con beta (regimen de acoplamiento
debil / fase de Coulomb del juguete) y los loops de Wilson crecen
monotonamente. Es la estructura cualitativa que el paper declara; **el
resultado es PRELIMINAR** (N=16 es muy chico).

## Que falta (priorizado)

1. **N=64 Metropolis: HECHO (2026-10-25)** — misma estructura que N=16 y sin
   area law en el rango medido. Falta heat bath Kennedy-Pendleton + ratios de
   Creutz con errores < 5% en el lado fuerte (beta < beta_c) para cuantificar
   G1 (ley de area) y extraer sigma(beta).
2. **Extraccion de sigma(beta)** via ratios de Creutz con errores < 5%
   (mas sweeps; corrida actual sin error estadistico reportado).
3. **Cuidado con G1 en beta alto:** en esta implementacion la plaquette
   satura ~0.87 en beta=10 (no ~1); los loops NO decaen con el area en este
   rango. La señal de confinamiento (area law) queda DEMOSTRADA SOLO en los
   regimenes asintoticos del paper (character expansion / gaussiana); el MC
   actual no la establece.

## Verificacion (reproducir)

```bash
python3 gauge_mc.py    # numpy requerido; ~1 min en N=16
```

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
