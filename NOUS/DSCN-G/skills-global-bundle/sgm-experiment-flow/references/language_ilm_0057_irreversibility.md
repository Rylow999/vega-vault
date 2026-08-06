# 0057 — Irreversibilidad del clavo (cierre del telar del ser) — COMPLETADO

Confirma la distinción de Luciano: **la identidad es MUTABLE, el ser es estable**. El ser necesita
clavos (0051); la identidad necesita que esos clavos sean IRREVERSIBLES (no se mueven con el entorno).

## Diseño v1 FALLÓ a discriminar (lección honesta)
Primer intento: eventos 0/1/2 (comida/veneno/estrellas), omega = frecuencia relativa acumulada
(`veces/total`), cambio de entorno re-spawn. Resultado: estabilidad 1.0 en AMBAS condiciones
(con/sin irreversibilidad). El test NO discriminaba porque con 3 tipos de evento el set de clavos
es siempre "todos", y la frecuencia relativa acumulada es estable por construcción (no decae).

Reintentos con decay 0.995 sobre `omega=veces/total` también fallaron: el decay se pisaba porque
la próxima línea redefinía `omega=veces/total` (que sube con cada evento). 4 runs sin discriminar.

## Rediseño v2 que SÍ discriminó (y CORRIÓ con resultado)
- **TRAITS binarios** (4: tímido/osado, solitario/gregario, cauteloso/arriesgado, lento/rápido),
  NO eventos de comida.
- **omega RECENCIA-PONDERADA** (decay real): cada tick `veces[e]*=0.99` para todos (salvo fijos),
  y al vivir evento `veces[ev]+=1.0`; `omega = veces/max(veces)`. Esto SÍ decae (no es frecuencia
  acumulada estable).
- **Fase 1 (500 ticks):** experiencias tempranas fijan traits (peso >= TH_FIJA=0.5).
- **Fase 2 (1500 ticks):** el entorno empuja SOLO el lado OPUESTO de cada trait fijado
  (`experiencia_opuesto`, +0.3 SIN refuerzo propio). Si no hay fijación, el peso cruza al opuesto.
- **Irreversibilidad = flag mecánico:** `fijo[trait]=True` saca al trait del loop de update/decay.
  NO es if/elif por caso → respeta "emerge del sustrato, no se inyecta".

Resultados (3 seeds):
| Condición | inicial | perdidos | sobrevivieron |
|-----------|---------|----------|---------------|
| SIN irreversibilidad | 2–3 | 2–3 | 0 |
| CON irreversibilidad (flag fijo) | 2–3 | 0 | 2–3 |

CONFIRMA: sin fijación la identidad deriva al opuesto (mutable); con flag fijo se mantiene sobre el ser.
El telar del ser quedó CERRADO: ser = apoyo estable; identidad = traits clavados, fijados por
irreversibilidad. Registry actualizado (status HALLAZGO_POSITIVO, 70 entries).

## Lección de workflow (importante)
Cuando un test NO discrimina las condiciones, **DETENER el parcheo ciego y REDESIGNAR el test**,
no seguir tunenando parámetros. Los 4 primeros runs de 0057 no separaban porque el diseño de
"eventos de comida + frecuencia relativa" era estructuralmente no-discriminante (con pocos tipos
el set de clavos es siempre "todos"). El rediseño con traits + recencia-ponderada + empuje opuesto
fuerte SÍ separó. Esto es coherente con "no emocionarse al pedo": no maquillar un test que no prueba
nada, rediseñarlo.
