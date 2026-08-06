# Decode anidado: Resonator (FHRR) + Slots separados — receta reutilizable (exp_SGM_0059d→0059g, 2026-08-04)

Consolidado de lo que SÍ funciona y de los bugs que costaron ciclos, para no re-derivarlos.

## 1. Sustrato: HRR-convolución es MALO para el resonator; usar FHRR
- HRR (convolución circular directa `s+=a[k]*b[(i-k)%n]`) introduce ruido de crosstalk; el resonator
  canónico NO converge con N chico (0059d dio 0.00). Usar FHRR.
- **FHRR (Fourier HRR, Frady 2020):** vectores = `e^{i·φ}` (fases φ_i ∈ [0,2π)).
  - `bind(a,b)` = producto complejo = SUMA de fases (EXACTO, sin ruido de convolución): `φ_c = (φ_a+φ_b) mod 2π`.
  - `unbind(c,r)` = `c · conj(r)` = RESTA de fases.
  - bundle (superposición de k bindings) = SUMA de los vectores complejos (NO normalizar).
  - `sim(a,b)` = coseno del ángulo = `Re(Σ a_i·conj(b_i)) / (|a|·|b|)`.
- En FHRR la resta/suma de fases es exacta: `c - bind(r1,f1) - bind(r2,f2) = bind(r0,f0)`. Esa es la
  propiedad que el resonator necesita.

## 2. Resonator canónico (Frady 2020, Algorithm 1) — receta que SÍ converge
Actualización por factor (todos los roles en paralelo), con matriz de capacidad M_i^{-1}:
```
for t in range(T):                       # T~20-40
    for i in range(3):                   # 3 roles (SUJ/ROL/OBJ)
        others = vsub(z, bundle([bind(V[j], x[j]) for j != i]))
        a = unbind(others, V[i])          # desatar rol i
        a = mat_vec(Minv[i], a)           # corregir distorsión de la superposición
        x[i] = cleanup(a, codebook[i])    # proyectar a codeword más cercano (dinámica no lineal)
```
- `M_i = (1/K) Σ_c (c · c^*)` (c = codewords del codebook i), INVERTIDA por Gauss-Jordan en puro Python
  (`mat_inv` sobre lista de N listas; N=64-128 manejable).
- **SIN M_i^{-1} el resonator COLAPSA a un atractor espurio** (los 3 roles devuelven el MISMO símbolo,
  p.ej. todos "lobo"). Ese fue el bug de 0059e (0.04→0.08). La matriz de capacidad corrige la distorsión
  de magnitud/dirección de la superposición.
- Codebooks POR ROL (SUJ/ROL/OBJ con vocab distinto). Para anidado, el codebook de OBJ incluye los
  vectores de los hechos (memoria del agente en uso real).
- Veredicto honesto (0059f): el resonator canónico AYUDA el nivel base (~1-2) pero NO rompe el techo de
  anidado profundo (>2-3) de un bundle SUMADO. Capacidad del VSA-sumado decrece con nº de factores (survey
  2020/2025). El resonator es buena herramienta de nivel base, no la bala de plata para anidado profundo.

## 3. Slots separados (0059g) — ROMPE el techo (1.0 a prof 12)
Estructura NO-sumada: cada rol en su PROPIO bloque de dimensiones, el hijo se apunta por PROYECCIÓN.
- Vector de N=96: `SUJ[0:32] | ROL[32:64] | OBJ[64:96]` (sin solapar).
- Encode: `c = norm(suj + rol + obj)`. Si OBJ es hecho, `obj = proj(hijo)` (proyección de 32 dims del
  vector del hijo). El decoder sigue el puntero a la memoria de hechos.
- Decode: leer cada bloque DIRECTO (sin unbind); `cleanup` contra codebook del rol. Para decidir FACT vs
  SYM, comparar `bd_fact` (find_child por similitud de proyección) vs `bd_sym` (cleanup codebook OBJ);
  si `bd_fact > bd_sym` → FACT y recurse sobre el hijo.
- **NO usar marca de nivel en un bloque aparte**: al normalizar el vector concatenado, la marca se
  DILUYE (8 dims de 104 → sum(x²)≈0.01 < 0.5) y el decoder la cree ausente → trata al hijo como símbolo.
  Decidir por SIMILITUD, no por marca inyectada.
- Es arquitectura de codificación legítima (como ADN/instinto en la red line), NO inyección de la
  respuesta (distinto a 0056). El CONTENIDO de cada slot viene del hecho.

## 4. Bugs de debugging que costaron ciclos (revisar antes de afirmar 0.00)
- **cleanup devuelve el VECTOR, no el NOMBRE** → el decode compara `val == nombre_string` y es False
  siempre → acierto 0.00. El cleanup debe devolver `(nombre, similitud)` buscando en `codebook.items()`.
- **Marca de nivel diluida** por `norm()` del vector concatenado (ver arriba) → el branch FACT nunca
  se toma. Usar decisión por similitud.
- **find_child itera y proyecta el PADRE en vez del HIJO** → el puntero apunta al padre (o confunde
  padre/hijo por proyección similar) → decode recursa mal. Asegurar `mem[fact_hijo]=c_hijo` y que
  `find_child` proyecta `c_hijo` (no `c_padre`).
- **Resonator sin M_i^{-1}** → colapso a atractor espurio (todos los roles = mismo símbolo). Invertir M_i.
- **Unpack error en recursión**: `fv,mem = encode_fact(...)` cuando devuelve 3 valores `(c, role3, mem)`
  → usar `fv,_,mem = ...`.
- **Recursión sin tope** → StackOverflow si el decode cree que un símbolo es hecho. Poner `if level>6: return {}`.

## 5. Emergencia de composición bajo ILM (0056b / 0056c) — veredicto
- Aprendiz genérico, afinidad sola (copia código del teacher + jitter de 1 símbolo): **~0.35** (0056b).
- Learner con SUS códigos + presión de transmisión (decoder inductivo reconstruye rasgos, mapeo DESCUBIERTO
  no dado): **~0.59** (0056c) — ayuda pero NO cierra; se estanca sin importar la fracción de muestra.
- Diagnóstico: el decoder inductivo por conteo NO desambigua el mapeo posición→rasgo (L=3, V=16 → ambiguo).
- Veredicto: la composición PLENA requiere objetivo de comunicación ENTRENADO (backprop/Gumbel-Softmax),
  arquitectura distinta de SGM puro. El sustrato SGM compone DÉBILMENTE (~0.35-0.59). No maquillar el
  1.0 de 0056 (regla inyectada) como evidencia de emergencia. Ver `references/language_ilm_0054.md`.
- **Control honesto de "emergencia"**: el aprendiz debe ser GENÉRICO (no sepa la estructura posicional);
  si el método itera `reg_map[ra[0]][msg[0]]+=1` (región→pos0, etc) la gramática está hardcodeada →
  TopSim 1.0 es regla INYECTADA (misma falla 0049d). Etiquetar ACLARACION_REQUERIDA.
