# EMERGENCIA DE COMPOSICIÓN + BARRIDO BINDINGS-POR-BLOQUE (0056c / 0059h)

Receta condensada y debugging de los dos experimentos de fase 7 sobre el "lenguaje del sustrato"
(2026-08-04). Complementa `docs/EMERGENCIA_COMPOSICION_0056_0056b_0056c.md` y `docs/DECODE_ANIDADO_0059_HALLAZGO.md` en el vault.

## 1. 0056c — composición con presión de transmisión (RESULTADO NEGATIVO-DECISIVO)

**Pregunta:** ¿el sustrato SGM compone PLENO (~0.9-1.0) bajo presión de transmisión, o solo débil?

**Setup (exp_SGM_0056c, `/data/user/0/.../home/run_ilm_0056c.py`):**
- 24 referentes = región × distancia × tipo (VS/VR/VO, V=16, L=3).
- 3 seeds, 20 generaciones, frac=0.4.
- `ILMLearner`: tiene SUS PROPIOS códigos (no los del teacher). Ajusta los vistos para que un
  **decoder inductivo** (`reconstruct`) reconstruya los rasgos; el decoder busca en TODAS las posiciones
  (NO asume posición fija → no inyecta la regla, a diferencia de 0056).
- Para no-vistos: copia el código del más-afín (por afinidad de rasgos) + jitter de 1 símbolo
  (versión naïve, dio ~0.35) O bien **unificación global por rasgo descubierto** (versión v3, dio ~0.59).

**Resultado honesto:**
- TS_full se estanca en **~0.59** sin importar la fracción (0.4→0.59, 0.5→0.586, 0.6→0.599,
  0.7→0.596, 0.9→0.374 porque no hay no-vistos que componer).
- Diagnóstico: el decoder inductivo por conteo NO desambigua el mapeo posición→rasgo (L=3, V=16 →
  espacio ambiguo; el conteo no separa competidores). La presión de transmisión AYUDA (sube de 0.35 a
  0.59) pero no cierra.

**Veredicto:** la composición PLENA (~0.9-1.0) requiere OBJETIVO DE COMUNICACIÓN ENTRENADO
(backprop / Gumbel-Softmax), que es arquitectura distinta de SGM puro. El sustrato compone DÉBILMENTE
(~0.35-0.59 según presión). Esto confirma la tesis del doc 0056.

**Implicaciones del decoder entrenado (pedido por Luciano, en criollo):**
1. El loop deja de ser sustrato puro: SGM no tiene motor de gradiente; entrenar un decoder es una
   arquitectura nueva encima. El 1.0 sería del traductor entrenado, no del sustrato (que se queda ~0.59).
   Etiquetar como "composición con objetivo entrenado", no "emerge del sustrato".
2. El código se ordena para la red, no necesariamente para el operador humano.
3. La trampa de 0056 sigue viva: si se entrena con slots fijos (posición 0 = región) es la MISMA trampa.
   Para ser honesto, el decoder debe DESCUBRIR la estructura (buscar en todas las posiciones, como 0056c)
   pero entrenado. Eso da ~1.0 y es "emergente bajo objetivo", no "regla inyectada".
4. No resuelve el "lenguaje que evoluciona a sí mismo": un decoder con objetivo fijo da composición
   plena, pero el "evolucionar su propia visión" requeriría que el OBJETIVO también cambie.

**Decisión pendiente de Luciano:** implementar 0056d (decoder entrenado honesto) o dejar el límite
documentado y pasar a otro tema.

## 2. 0059h — barrido bindings-por-bloque (EN CURSO, metodología de Luciano)

**Idea:** mapear la curva capacidad-vs-superposición entre los dos extremos ya medidos:
- K=1 → superposición pura (3 roles en 1 bloque, resonator desata) = 0059/59b/59c (techo ~2-3 niveles).
- K=3 → slots separados (cada rol su bloque) = 0059g (1.0 a prof 12, ROMPE el techo).
- K=2 → punto intermedio (SUJ+ROL en un bloque, OBJ aparte) — el aporte concreto propuesto.

**Setup (exp_SGM_0059h, `/data/user/0/.../home/run_decode_0059h.py`):**
- `BlockBundle(K, N)`: N dims, BLK=N//K. Roles asignados por `j % K` (j=0 SUJ, 1 ROL, 2 OBJ).
- Para cada bloque con 1 rol → clean-up directo (sin resonator).
- Para cada bloque con >1 rol → bundle de `bind(role_vec, filler)` + **resonator canónico Frady 2020**
  (matriz de capacidad M_i = (1/K) Σ c·c*, inversa por Gauss-Jordan, `a_i = M_i⁻¹ · unbind(...)`).
- El hijo anidado se apunta por **proyección circular-mean** (`proj_fhr`) en el bloque que le toca.
- Barrido: K∈{1,2,3} × N∈{64,128,192}; medir prof-max con acierto≥0.85.

**BUGS DE DIMENSIONAMIENTO ya corregidos (no repetir):**
1. `Minv` es por **BLOQUE**, no por rol: todos los roles de un bloque comparten BLK dims → una sola
   matriz de capacidad por bloque (`self.Minv = [None]*K`, no `[[None]*K]*K`).
2. `self.roles[b]` debe tener `len = nroles del bloque b` (NO K fijo). Calcular `br` inline en
   `__init__` para dimensionar correctamente antes de crear los vectores de rol.
3. `proj_fhr(vec, dim)` debe tomar un **VECTOR COMPLEJO** (lista de `cmath.exp(1j*phase)`), NO una
   lista de fases float. La proyección hace mean de las partes real/imag por segmento y re-exponencia.
4. `encode_fact` devuelve `(c, mem)` (tupla). Al anidar, usar `hijo_vec = self.encode_fact(...)[0]`,
   NO pasar la tupla entera a `proj_fhr` (da `AttributeError: 'list' object has no attribute 'real'`).
5. En `decode_block_multi`, el índice del rol dentro del bloque es `idx` (enumerate local), NO `j`
   global. Usar `self.roles[b][idx]` y `self.roles[b][o]` en la construcción de `others`.

**ESTADO:** al 2026-08-04 el script 0059h aún NO terminó de correr limpio (se corrigieron los 5 bugs
arriba pero el run final con el barrido completo K×N no se ejecutó/verificó). NO reportar números de
prof-max hasta confirmar el run con output real y acierto≥0.85 estable en las 3 seeds del barrido.

**Por qué importa:** el barrido K=1→3 cuantifica CUÁNTA superposición se puede tolerar antes de que el
decode anidado colapse. Es el dato que faltaba entre "todo sumado" (techo) y "todo aislado" (1.0), y
operacionaliza la distinción del doc 0059: el cuello era la codificación SUMADA, no el sustrato.
