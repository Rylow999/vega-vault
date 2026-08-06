# STATUS — C3 / Face Hijacking

> Extraído y organizado de `../../DOCUMENTATION/auditoria/claims_falsifiable.md`
> (Claim 5). Ese archivo es la fuente completa; esto es el resumen operativo
> de esta extensión.

## Parámetros de diseño originales
`θ_death=0.10`, `hijack_steps=15`, `η_hijack=0.15` (defaults de
`../C3_Face_Hijacking/../../CORE/IMPLEMENTATION/CODE/verify_dscng_v3.py`).

## Resultado a params originales — ❌ NO sostenido
- 2237 hijack triggers en 30 seeds, 2000 steps (3.73% de los steps).
- Solo 20/2237 triggers (0.9%) muestran ΔPLV < −0.3.
- Mean ΔPLV = −0.007 ± 0.061 (no −0.462 ± 0.089 como se afirmaba antes).
- Max ΔPLV (caso más extremo) = −0.918 — existen casos extremos, pero no
  son la norma.

**Diagnóstico:** T1 converge a ~4–5 nodos activos; `plv_intra_group()` mide
consenso sobre `nodes_active[1:]` (excluye la raíz) — con N*≈4–5 eso son
3–4 seguidores, población insuficiente para que el pull de hijacking
produzca sincronización medible y estable frente al ruido.

## Rediseño (Ronda 4) — mejora real, sigue sin llegar a "la norma"
Bajando `θ_death` (más nodos sobreviven) y subiendo `hijack_steps`/`η_hijack`:
rise_rate sube monótonamente de 0.7% (baseline) a **30.2%** en la config más
agresiva (`θ_death=0.01` → ~28 seguidores, `hijack_steps=150`, `η=0.80`).
Mejora de ~40x, pero esos parámetros son 10x los valores de diseño
originales.

## hub_boost (Ronda 5) — sin efecto, retirado (Ronda 6)
Privilegio estructural del root (`hub_boost` hasta 5x): **sin efecto
medible** (0.7% y 30.2% iguales en boost=1, 2 y 5) — saturación de
`plv_intra_group()`, no falla de implementación. La analogía
tálamo/hub_boost fue **retirada formalmente** del paper (Ronda 6). El
código (`thalamic_model.py`) se conserva como evidencia del intento, no
debe citarse como mecanismo activo.

## Recomendación
No citar C3 como verificada a los parámetros de diseño originales. Si se
sigue explorando, documentar cualquier resultado nuevo en este archivo,
no en el paper del núcleo, hasta cumplir `../../CORE_RULES.md`.
