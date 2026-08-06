# Decode anidado — Barrido K (0059h + 0059i) y el colapso de identidad del puntero

Receta + hallazgos del barrido de bindings-por-bloque propuesto por Luciano (2026-08-04).
Complementa `composicion_emergencia_0056c_0059h.md` (que cubre 0059h desde el lado composición).

## Pregunta
¿Cuánta superposición tolera el decode anidado? Mapear la curva capacidad-vs-superposición entre
superposición pura (K=1: 3 roles en 1 bloque, resonator desata) y slots separados (K=3: cada rol su
bloque, 0059g).

## Setup del barrido
- K = nro de bloques de dimensiones que COMPARTEN los roles. K=1: SUJ/ROL/OBJ todos en 1 bloque.
  K=2: SUJ+OBJ en bloque 0, ROL en bloque 1 (o SUJ+ROL / OBJ según `j % K`). K=3: cada rol su bloque.
- BLK = N // K. El hijo se apunta por proyección N→BLK en el bloque que le toca.
- Resonator canónico de Frady 2020 (M_i⁻¹ por bloque multi-rol) SOLO en bloques con >1 rol.
- Barrer K ∈ {1,2,3} × N ∈ {64,128,192}; medir prof-max con acierto ≥0.85.

## Resultado (0059h)
| K | N=64 | N=128 | N=192 |
|---|------|-------|-------|
| K=1 | prof0 | prof0 | prof0 |
| K=2 | prof0 | prof0 | prof0 |
| K=3 | prof8 | prof8 | prof8 |

Curva BINARIA: superposición colapsa, aislamiento total abre. El resonator NO salva el anidado bajo
superposición cuando hay punteros a hechos hijos (el puntero proyectado no es un filler canónico).

## 0059i — refinamiento de K=2 con puntero-rol explícito (confirma la curva)
Intento honesto de matizar: dar al puntero su PROPIO vector-rol (PTR) DENTRO del mismo bloque físico
(bloque 0 = SUJ, OBJ, PTR; bloque 1 = ROL), subir T del resonator a 40. Hipótesis: si el puntero tiene
"su propia voz" el resonator lo separa y K=2 abre.

Resultado: K=1/K=2 siguen prof0 (ambas métricas: todo≥0.85 y solo-padre≥0.85), K=3 prof8.

### DIAGNÓSTICO CLAVE (nuevo, el cuello de fondo)
Al correr profundo el decode ENTRO EN RecursionError. Causa: el puntero proyectado circular-mean
(N→BLK) **COLAPSA la identidad del hijo** → todos los punteros se parecen → `find_child` SIEMPRE
matchea → bucle infinito de decode. NO es que el resonator no desate; es que **la proyección N→BLK
destruye la identidad del hijo** (pierde info irreduciblemente cuando el bloque es más chico que el
hijo). Con corte de recursión (MAXDEPTH=12) y umbral de puntero 0.5, K=2 da prof0 limpio.

### Veredicto
El puntero exige su PROPIO sub-espacio físico. No alcanza con "su propio vector-rol en bloque
compartido" porque el bloque sigue siendo más chico que el hijo y la proyección lo borra. Decode
anidado en SGM REQUIERE SLOTS SEPARADOS (K=3); cualquier superposición de un rol-puntero colapsa por
pérdida de identidad en la proyección.

## Bugs de implementación que costaron ciclos (ya corregidos, para no repetirlos)
1. `Minv` indexado por rol global `j` en vez de por bloque → IndexError. Una sola Minv por bloque.
2. `self.roles[b]` dimensionado con K fijo en vez de nroles-del-bloque → IndexError al usar `self.roles[b][j]`.
   Dimensionar `self.roles[b]` con `len(br[b])` (nroles reales del bloque).
3. `proj_fhr` recibía la tupla `(c, mem)` en vez del vector `c` (desempacado mal en encode_fact).
   Usar `hijo_vec, _ = self.encode_fact(...)` y pasar `hijo_vec`.
4. `self.roles[b][j]` usaba índice global `j` en vez de índice local `idx` dentro del bloque.
5. Decode recursivo sin corte de profundidad → RecursionError cuando el puntero proyectado colapsa
   identidad. SIEMPRE pasar `depth` y cortar con `MAXDEPTH`; decidir FACT vs SYM por `found[2] > db_sym`
   (como 0059g), no por umbral fijo bajo (0.2) sobre punteros proyectados.

## Regla de diseño del barrido (reutilizable)
- Medir DOS métricas: `todo≥0.85` Y `solo-padre≥0.85`. Sino reportás "prof0" cuando en realidad
  decodifica 1 nivel y falla en el 2do (K=2 decodifica el hijo directo pero colapsa en el nieto por
  doble proyección).
- Umbral estricto + corte de recursión para que el sweep TERMINE limpio (sin RecursionError).
- Es la forma honesta de responder "¿cuánta X tolera el sustrato?": el barrido revela si hay pendiente
  o es binaria, y si el mecanismo intermedio (resonator + puntero-rol) salva algo.
- Metodología "barrido K" aplicable a cualquier parámetro de compromiso binario-sospechado: no probar
  solo extremos, barrer el intermedio para mapear la curva.
