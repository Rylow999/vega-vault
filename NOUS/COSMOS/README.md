# COSMOS — EFT de Materia y Energia Oscura (DSCN-G)

Formalizacion cosmologica del sustrato DSCN-G: la ecuacion de reaccion-difusion
de la vitalidad topologica mapea a un campo de Klein-Gordon con friccion de
Hubble. En el limite local genera halos de materia oscura (Yukawa-Poisson);
en el limite cosmologico, energia oscura (quintaesencia slow-roll).

**Paper:** [`PAPER/dscn_g_cosmos_v8_1_paper.md`](PAPER/dscn_g_cosmos_v8_1_paper.md) (v8.1, ingles)
**Verificacion:** [`verification/`](verification/) — scripts reproducibles + outputs + JSON
**Licencia:** MIT · **Autor:** Luciano Benjamin Nieto (ORCID 0009-0000-8766-7243)

---

## Que hay en este repositorio

| Ruta | Contenido |
|---|---|
| `PAPER/` | El paper (v8.1) con etiquetas de estado por claim |
| `verification/verify_predictions.py` | Reproduccion aritmetica de las predicciones (a)-(d) + refit del exponente RG |
| `verification/verification_predictions.json` | Resultados del run de verificacion |
| `verification/verify_predictions_output.txt` | Output literal del run |
| `CHANGELOG.md` | Historial de cambios y auditorias |

## Resultados principales

Las cuatro predicciones del paper, con su estado tras la auditoria
(Metodo Integral: "verificado" solo con artefacto reproducible):

| Prediccion | Valor del modelo | Observacion | Compatibilidad | Estado |
|---|---|---|---|---|
| (a) Anisotropia dH0/H0 | 3.49% (z=0.10) | 4.1% +/- 0.9% (CosmicFlows-4) | 0.68 sigma | OK reproducido (`verification/`) |
| (b) Decaimiento monotono dH(z) | exp(-z/z_tau) | — | — | OK demostracion analitica + grilla |
| (c) Escala angular theta(0.65) | 0.777 grados | 0.78 (DESI DR9) | 0.40% error | OK reproducido |
| (d) H0 local | 73.13 | 73.04 +/- 1.04 (SH0ES) | 0.09 sigma | OK reproducido |
| Flujo RG beta = 2pi/D | tabla 4.3 | fit beta=2.0977 vs 2.0944 | 0.16% | ATENCION consistencia interna (ver abajo) |
| Monte Carlo n=50.000 (sec 7) | tabla declarada | — | — | FALTA no reproducible del texto (modelo estocastico no especificado) |

## Verificacion (reproducir)

```bash
cd verification
python3 verify_predictions.py        # stdlib puro, sin dependencias
```

Salida esperada: `pred_a ... ok: True`, `pred_c error_percent 0.398`,
`pred_d ok: True` (sigma=0.087), y el MC sec 7 etiquetado `NOT_REPRODUCIBLE_FROM_TEXT`.

### Nota honesta sobre el flujo RG

El refit de la tabla alpha(m) impresa en 4.3 da beta=2.0977 frente a 2pi/D=2.0944
(0.16%). Es una **consistencia interna**: la tabla fue generada por la misma
ley que se ajusta. La verificacion independiente (medir alpha(N) desde la dinamica
del sustrato) requiere la simulacion MC citada, todavia ausente — ver
`CHANGELOG.md` y `verification/verification_predictions.json`.

## Literatura de contraste (verificada 2026-10-11)

- **DESI DR2 (2025-2026):** evidencia 3.2-3.4 sigma de energia oscura dinamica
  (w0waCDM favorecido, cruce phantom-quintessence "Quintom").
- **Tension H0:** Planck 67.40+/-0.50 vs SH0ES 73.04+/-1.04; H0DN 2026 la situa
  en ~7.1 sigma.
- **k-essence (dilaton/tachyon):** alivia la tension a 0.14-0.69 sigma — la familia
  fenomenologicamente mas exitosa publicada. El contraste cuantitativo del
  flujo RG logaritmico de este paper contra w0waCDM/k-essence es **el
  experimento que falta**.

## Papers hermanos

- [`NOUS/QUANTUM`](../QUANTUM/) — sustrato cuantico (Lemma 4.1, lambda2=4)
- [`NOUS/GAUGE`](../GAUGE/) — confinamiento SU(2) en el circulante
- [`Master-Document/Gap_G3_Derivation.md`](../../Master-Document/Gap_G3_Derivation.md) — derivacion de alpha0 y test w>=-1

## Cita

```bibtex
@misc{nieto2026cosmos,
  author = {Nieto, Luciano Benjam{\'i}n},
  title  = {DSCN-G-Cosmos v8.1: Emergent Quantum Gravity -- EFT Unification
            of Dark Matter and Dark Energy},
  year   = {2026},
  url    = {https://github.com/Rylow999/vega-vault/tree/main/NOUS/COSMOS}
}
```
