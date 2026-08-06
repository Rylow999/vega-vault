# ROOT DIRECTOR (v0.22) — receta y resultados COMPLETOS

Root bottom-up SOBRE el grafo fractal. ADVERTENCIA (2026-07-28): v0.21 v8 (el grafo
fractal como base de sentido) fue REFUTADO por negative control (4/5 monosémicas
también "separaban"; acc_gt<=0.53 en corpus controlado). El root director como
PROYECTOR DE SENTIDO fue también REFUTADO (v0.22 v2: root_acc=0.545=baseline sobre
transformer). El root NO proyecta sentido; el transformer lo hace. El root es
MEMORIA/DOLOR/FOCO sobre el contexto (v0.3b, v0.19, v0.24). Ver PITFALL #23 y #24.

## Diseno
- Cada palabra = K=2 subnodos (sentidos), separados por ANCHOR+REPULSION (v0.21 v8).
- Ruteo competitivo: `k* = argmax_k cos(subnodo_k, contexto)`.
- DUDA: si `top1 - top2 < MARGIN` -> el root declara DOUBT (2+ subgrafos sin dominante).
- MARGIN fijo sweep [0.05..0.20] (v1/v2) o MARGIN ADAPTATIVO = percentil p de la
  distribucion de (top1-top2) en el corpus (v4/v5, no hardcodear umbral).

## Tests
- FASE A (corpus contrastivo banco/llave/mouse, 2 sentidos x40-50, ground-truth en tags):
  routing_acc = fraction routed correctly when not in doubt.
- FASE A probe AMBIGUO: contexto = promedio de los dos sentidos -> debe dudar.
- FASE B (Don Quijote real, top-150, 20k tok): tasa_duda emergente.
- FASE MIX (v5): contextos con AMBOS sentidos mezclados -> la duda debe emerger AHI.

## Resultados (medidos 2026-07-28, sesion v0.22 v1->v5)
| Variante | routing_acc (Fase A) | tasa_duda DQ | probe ambiguo | nota |
|----------|---------------------|--------------|---------------|------|
| v1 contexto = promedio de TODOS los subnodos vecinos | 0.57->0.41 | 0.086->0.33 | 0/3 | coseno plano ~azar |
| v2 contexto = subnodos GANADORES de vecinos | 0.56->0.45 | 0.072->0.265 | 0/3 | agregado no era el problema |
| v3 proyeccion W Hebb (sin backprop), MARGIN fijo | **1.0** (4 m) | **0.0** (4 m) | 0/3 | rutea PERFECTO, MATA duda |
| v4 MARGIN adaptativo (percentil) + W Hebb | bug NaN->0.0 | 0.0 | — | NaN por norma cero (PITFALL #25) |
| v4 (corregido) MARGIN adaptativo + W Hebb | 1.0 | 0.0 | — | margin=0.0: diffs siempre >0 |
| v5 proyeccion SUAVE (1 ep, lr 0.005) + MARGIN adapt + contextos MIX | EN CIERRE DE SESION | — | — | ver abajo |

## Conclusion honesta (CIERRE v0.22)
- Separar sentidos (v0.21 v8: 39/40) != RUTEARLOS. El coseno plano ~= azar.
- v3 CONFIRMA: el grafo rustico necesitaba PROYECCION para que el contexto sea
  informativo (intuicion de Luciano). routing_acc = 1.0 = perfecto.
- TRADE-OFF REAL (hallazgo central): con proyeccion el root rutea perfecto PERO la
  proyeccion separa TANTO que nunca hay ambiguedad aparente -> MATA la duda (Fase B
  duda=0.0; probe ambiguo 0/3). Sin proyeccion hay duda (Fase B v1/v2: 0.07-0.33)
  pero ruteo es azar.
- MARGIN adaptativo (v4) NO recupera la duda porque la distribucion de (top1-top2)
  no tiene cola de ambiguedad: la proyeccion resuelve tanto que diffs>0 siempre.
- v5 (contextos MIXTOS + proyeccion suave) fue el intento de recuperar la duda donde
  DEBE emerger (contexto verdaderamente ambiguo). Estado: corrida final de la sesion;
  si duda(MIX) > duda(A/B univocos), el mecanismo de duda es honesto (dispara donde
  hay ambiguedad real, no por ruido). Ver resultados en results_v22_v5.json.

## Lecciones de implementacion (bugs de la sesion)
- PITFALL #25: W Hebb -> NaN por norma cero en contexto proyectado. Fix: norm(v) or
  1e-9 en TODAS las normalizaciones + pct filtra None/NaN.
- PITFALL #26: modelo+indice deben coincidir con el corpus de evaluacion (KeyError
  'don' en Fase B si reusas el idx del grafo contrastivo). Cada fase entrena su
  propio grafo+W sobre su corpus.
- EDICION POR CHUNKS: al hacer patch que reemplaza una linea por un bloque grande,
  el old_string puede ser UNA funcion auxiliar (ej def mat_vec) que se pierde si el
  new_string no la re-incluye -> NameError en runtime. REGLA: al reemplazar, verificar
  que las funciones auxiliares del old_string reaparezcan en el new_string, o agregarlas
  aparte despues. (v0.22 v5 perdio mat_vec asi y fallo con NameError.)
- NO reusar W para ventana Y matriz en el mismo script (colision -> TypeError).
  Ventana = WIN, matriz = W.

## Archivos en el repo
- v0.22_root_director/run_v22.py — v0.22 v1/v2/v3 (sobreescrito).
- v0.22_root_director/results_v22.json — v3 (ultimo con MARGIN fijo).
- v0.22_root_director/run_v22_v4.py + results_v22_v4.json — MARGIN adaptativo.
- v0.22_root_director/run_v22_v5.py + results_v22_v5.json — contextos mixtos.
- Grafo base: v0.21_fractal/run_v21_v8.py + run_v21_v8_real.py (anchor+repulsion).
