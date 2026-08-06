# Tests decisivos para validar LENGUAJE REAL vs MEMORIZACION (exp_SGM_0053, 2026-08-03)
Contexto: 0049d reporto "comunicacion 1.0 = lenguaje cerrado", pero era cleanup de 15 simbolos
fijos ya demostrado en 0029. Estos 3 tests deciden si hay lenguaje emergente o memorizacion.

## 1) ZERO-SHOT (generalizacion a items no vistos)
- Entrenar el alfabeto compartido sobre un SUBGRUPO (ej. 8 de 15 celdas del puente).
- Luego A debe senalar celdas NUEVAS (las 7 restantes) que B nunca vio en el alfabeto.
- Si B identifica > NC -> hay generalizacion (el codigo transfiere a lo no visto = lenguaje).
- Si cae a azar -> es memorizacion de 15 fijos (el HRR solo aisla lo que ya conocia).
- Veredicto: hit_celdas_nuevas ~ NC  => memorizacion; hit >> NC => generalizacion.

## 2) TOPSIM (composicionalidad objetiva, no intuicion)
- Calcular correlacion de SPEARMAN entre:
  - distancia ESPACIAL de las celdas (|pos_A - pos_B|)
  - distancia HRR de las SENALES (1 - cos(cell_hrr(A), cell_hrr(B)))
- TopSim alto (>0.5) => las senales HRR reflejan la geometria => composicionalidad real.
- TopSim ~0 => las senales son memorizadas sin estructura (no hay mapa geometrico en el codigo).
- Esto reemplaza "se ve bien" por una medida objetiva.

## 3) D ESCALADO (resolver escala abierta, no recortar vocabulario)
- Ley de capacidad de 0029: M_max ~ 200 * (D/128)^0.667  (medido: D=128->200 items, D=1024->800).
- Para aislar ~890 items (0049c abierto) necesitas D tal que 200*(D/128)^0.667 >= 890
  => D >= 128 * (4.45)^(1/0.667) ~ 128 * 9.4 ~ 1200. Usar D=1280.
- Repetir 0049c (alfabeto abierto ~890) con D=1280 en vez de recortar a 15.
- Si la comunicacion sube >> NC en 890 items => el HRR SÍ resuelve escala abierta (faltaba D).
- Si sigue en 0 => el crosstalk no es solo D, es otro problema (el HRR no es recuperador de items).

## Veredicto combinado
- Si (1) cae a azar Y (2) ~0  => 0049d era MEMORIZACION, no lenguaje. Confirmado.
- Si (3) sube con D alto    => el canal HRR funciona a escala, solo faltaba dimension.
- Estos tests cierran la pregunta "¿hay lenguaje o es cleanup?" sin tunear mas.
