# Decode Anidado (0059 / 0059b / 0059c) — hallazgo completo y decisión pendiente

Fecha: 2026-08-04. Fase: phase7_composicion. Autor: Vega (con Luciano).

## Por qué importa
El lenguaje del sustrato SGM debe codificar/decodificar hechos ANIDADOS
("el lobo que CORRE come la manzana que ESTA_EN el pasto"). Es núcleo del
"lenguaje que hace evolucionar al sistema y su forma de ver el mundo" (Luciano,
2026-08-04) — NO es un tunable: lo decide él tras pensarlo. 0058 cerró el gap
relacional a 1-2 niveles vía TPR sobre HRR.

## Método (HRR from scratch, CORRECTO)
- Convolución circular DIRECTA (`for k: s+=a[k]*b[(i-k)%n]`, O(N²), N=64 trivial),
  NO FFT propia (da inversa rota → unbind no recupera el filler).
- Inversa de HRR = permutación circular inversa de índices (`b[i]=a[(-i)%n]`,
  Plate 1995), NO conjugada de FFT.
- `gen_vec` = ruido gaussiano normalizado (`rng.gauss(0,1)`), NO fase compleja.
- Decoder recursivo: por rol, `unbind(c, role)` aísla el filler; si
  `dot(filler, símbolo)` tiene separación clara (top1>0.15 y top1-top2>0.05) →
  símbolo; si no → recurrir sobre el filler (tope de profundidad + budget para
  no explotar).

## Resultados (honestos, sin maquillar)
| Exp | Método | N | prof1 | prof2 | prof3 | prof4 | prof5 | prof6 |
|-----|--------|---|-------|-------|-------|-------|-------|-------|
| 0059 | HRR plano, recursivo | 64  | 1.00 | 0.67 | 0.64 | — | — | — |
| 0059 | HRR plano, recursivo | 256 | 1.00 | 0.90 | 0.67 | — | — | — |
| 0059b| TPR-walk NAIF (re-suma hijo en bolsa padre) | 128 | — | — | 0.56 | 0.53 | 0.58 | — |
| 0059c| TPR-walk CORRECTO (filler hijo autónomo) | 128 | — | — | 0.56 | 0.53 | 0.58 | 0.67 |

- HRR-summed satura en ~2 niveles de anidado. Subir N 64→256 AYUDA a prof2
  (0.67→0.90) pero NO rompe prof3 (sigue 0.67).
- TPR-walk (naif Y correcto) NO escala: el unbind de HRR N=128 NO aísla limpio
  el filler cuando la bolsa tiene 3 bindings; el ruido de los otros 2 roles del
  padre contamina al hijo al desatarlo.
- N=512 no corre en este equipo (conv N² = 262144 ops/bind, timeout).

## Veredicto
El decode anidado profundo (>2 niveles) en HRR-SUMMED es un LÍMITE DE CAPACIDAD
del sustrato, NO un bug de decoder. El sim vivo ya tiene composición a 1-2
niveles y funciona (test: 80-87% mapa, 0 bucles, 0-1 muertes). El anidado
profundo queda como límite documentado de HRR-summed, no de SGM (el sustrato ya
compone; el cuello es la codificación vectorial barata).

## Analogía (para explicar a Luciano, en criollo)
Cada hecho es una hoja de papel. Para guardar varios los PEGAMOS en un cartel
(el vector = bolsa de números). Para leer "borramos" lo que no es un rol → queda
ruido de los otros. 1 hecho se lee bien; 2 anidados (6 papeles traslapados) ya
no. Agrandar el cartel (N=256) ayuda a 2; a 3 se vuelve a traslapar. TPR-walk =
sobres cerrados pegados al cartel: al despegarlos, el cartel les deja tinta
encima. Solución real (NO probada): CAJONES SEPARADOS con etiqueta (rol), sin
pegar los sobres al cartel → role-filler con slots separados, no convolución
sumada. Eso SÍ escala.

## Próximo paso (decisión de Luciano, pendiente 2026-08-04)
Evaluar role-filler con slots separados para romper el techo de 2 niveles. Más
código y otra estructura, pero es el camino que SÍ escala. Mientras tanto el sim
vivo queda con composición 1-2 niveles.

## Archivos
- run_decode_0059.py  (HRR plano, N=64/256)
- run_decode_0059b.py (TPR-walk naif)
- run_decode_0059c.py (TPR-walk correcto)
- sim/sgm_sim.html    (sim vivo, composición 1-2 niveles, movimiento reactivo puro sin hardcode)

## Anti-patrones que costaron ciclos (no repetir)
1. FFT-propia de convolución → inversa rota. Usar conv_circ directa + invert por permutación.
2. `decode_recursive` sin tope → RecursionError (el unbind da ruido, el umbral
   nunca se cumple, recurre infinito). Poner `depth>5` y `budget`.
3. Medir solo "acierto" sin comparar contra el método viejo → no ves que no
   mejoró. Siempre comparar viejo vs nuevo por profundidad.
4. `gen_vec` con fase compleja (`exp(1j*...)`) → basura. Usar `gauss(0,1)` normalizado.
5. TPR-walk NAIF re-suma los roles del hijo dentro de la bolsa del padre →
   contaminación cruzada (el puntero de nivel también se ensucia). El hijo debe
   viajar como vector AUTÓNOMO (ya codificado, sin re-procesar).
6. Creer que "TPR-walk correcto" arregla el techo: con HRR-summed el unbind
   contamina igual porque la bolsa del padre tiene 3 bindings. El techo es de
   HRR-summed, no del decoder. Para romperlo hace falta estructura NO-sumada.
