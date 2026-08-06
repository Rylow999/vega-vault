# Fase 7 — Composición y Decode Anidado (cierre 0059i / 0056d / 0056e / 0056f / 0056g-h-i-j)

Recetas y veredictos honestos de los experimentos que cerraron la línea de emergencia de
composición y decode anidado en SGM-CORE (2026-08-04). Complementa
`composicion_emergencia_0056c_0059h.md` y `decode_barrido_k_0059h_0059i.md`.

## 0059i — Refinamiento K=2 con puntero-rol (CONFIRMA colapso binario)
- Idea de Luciano: darle al puntero del hijo su PROPIO vector-rol dentro del bloque compartido
  SUJ+OBJ (K=2: bloque0=SUJ+OBJ+PTR, bloque1=ROL). Si el resonator desata los 3 en el bloque,
  quizá K=2 se salvaba.
- Resultado: K=2 sigue prof0 (mismo que 0059h); K=3 control prof8+. El puntero-rol NO salva.
- Diagnóstico REAL (no bug): proyectar N→BLK (circular-mean) DESTRUYE la identidad del hijo
  (función many-to-one, NO inyectiva) → todos los punteros se parecen → `find_child` colapsa en
  **RecursionError** (bucle de decode). Ese RecursionError ES la evidencia del colapso, no un bug.
- Veredicto: el puntero anidado requiere su PROPIO sub-espacio físico (slots separados K=3).
  Ni resonator (0059d-f) ni puntero-rol explícito lo salvan porque la proyección borra identidad.
- Receta: en `decode_block_multi`, filtrar `est[o] is not None` al reconstruir `others`; poner
  `sys.setrecursionlimit(4000)` y un MAXDEPTH en `decode_fact` para que el barrido termine limpio
  (el puntero que no matchea devuelve SYM, cortando el bucle).

## 0056d — Decoder entrenado (NO es bala de plata)
- Reusa learner de 0056c (sus códigos, presión de transmisión) pero decoder = regresión
  logistica multinomial por rasgo, backprop manual (sgd, cross-entropy, 60 epocas), W_k libre en
  TODAS las posiciones (NO asume mapeo pos→rasgo fijo).
- Resultado: TS_full ~0.6 (NO sube a 1.0; mismo techo que 0056c ~0.59). dec_err_seen BAJA
  (0.11-0.33): el decoder SÍ aprende los VISTOS. PERO topSim_seen cae a ~0.33 (el código visto se
  desordena para que el decoder acierte) mientras topSim_unseen queda ~0.76.
- Veredicto: el decoder entrenado ayuda a reconstruir VISTOS pero la composición PLENA
  (vistos+no-vistos sistemáticos) no emerge. El CUELLO NO era el decoder: es el CÓDIGO DISCRETO
  (L=3, V=16) con ambigüedad irreducible para mapear 3 rasgos a tupla corta. Decoder entrenado =
  necesario pero NO suficiente; para ~1.0 haría falta código continuo/HD (ver 0056e).
- Backprop manual (stdlib): `softmax(z)` con `m=max(z)` para estabilidad; `g=(p[v]-1) if v==tv else p[v]`;
  `W[k][v][i] -= lr*g*x[i]` sobre one-hot de las L posiciones.

## 0056e — Código HD role-filler ROMPE el techo 0.6
- Hipótesis de Luciano: "probemos lo que se pueda para romper el 0.6". Diagnóstico de 0056d decía
  que el cuello era el código discreto. 0056e cambia el TIPO de código a HD continuo con
  role-filler: cada rasgo atado a su vector-rol; código = suma de bindings en N=256 dims bipolar
  (±1). Decoder lineal entrenado desata cada rasgo por unbind (role es ±1, autoinverso).
- MODO A (HD fijo + decoder oráculo entrenado en TODOS): TS_full=0.824, dec_err=0.000.
- MODO B (learner SUS códigos HD + presión de transmisión frac=0.4, solo vistos): TS_full=0.81-0.93
  según seed, dec_err g19=0.000 en 3 seeds. topSim_seen y topSim_unseen AMBOS ~0.85-0.92.
- Veredicto: ROMPE el techo. La composición PLENA EMERGE con código HD bajo presión de transmisión
  (no hace falta regla inyectada ni oráculo). MODO A da 0.82 (no 1.0) por solapamiento aditivo de
  los 3 bindings HD; con N mayor se acercaría a 1.0.
- HONESTIDAD: HD role-filler es arquitectura distinta del sustrato discreto (como 0059g slots
  separados, 0019 HDC). El 0.91-0.93 es del esquema de enlace, no del sustrato puro. El sustrato
  discreto se estanca ~0.6; el HD continuo lo rompe. Conecta decode anidado (0059g) con emergencia
  de composición: ambas requieren enlace por rol en espacio continuo.
- TopSim para HD usa `cosine_dist(a,b)=1 - dot(a,b)/N` (no Hamming discreto).

## 0056f — Uso real en corpus real (Don Quijote) como MEMORIA
- Uso real honesto SIN nltk/spacy (no instalados en el teléfono): tokenizar con
  `re.findall(r"[a-záéíóúñü]+", text.lower())`, filtrar len>2, oraciones 4..24 tokens.
- Descarga: Gutenberg pg2000 = ESPAÑOL (Cervantes). pg996 = INGLÉS (Ormsby) — NO usar 996 si se
  quiere español. `urllib.request.urlopen(...).read()` entero FALLA con IncompleteRead en archivos
  grandes (~2.2 MB): leer en chunks de 65536 bytes en un loop y juntar (`b"".join(chunks)`).
- Codifica 4000 oraciones como trazas HD: role-filler (bind por posición) y plana BoW (suma de
  wordvec). N=512, V=3000 palabras por frecuencia.
- recall: 20 queries, top-5 vecinos por cosine; métrica Jaccard léxico (sin stopwords).
- Resultado: Jaccard temático role-filler=0.085, plana=0.105 (plana levemente mejor). cosine
  top-1=1.000 ambas (recuerda la propia oración → memoria OK). cosine top-5: plana=0.471 >
  role-filler=0.275.
- Veredicto: en texto REAL el role-filler NO mejora el recall temático (el orden no discrimina
  tema en prosa; el rol introduce ruido). El HD COMO MEMORIA funciona (top-1=1.0) pero NO es
  comprensión/razonamiento. MATIZA 0056e: el role-filler es para COMPOSICIÓN SISTEMÁTICA, no para
  memoria temática de prosa. El sustrato demuestra retención/recuperación sobre datos reales.

## 0056g / 0056h / 0056i / 0056j — CLASIFICACIÓN REAL (arco que cierra la Fase 7)
Misma arquitectura (Don Quijote + BinDecoder/decoder por rol) pero TRES tareas con la etiqueta en
distinto canal, para aislar DÓNDE vive la señal. Receta común: tokenizar igual que 0056f; contexto
= oración con el objetivo ENMASCARADO; etiqueta real (no inventada).

- **0056g propio/común (etiqueta LÉXICA, por mayúscula):** falla — baseline 0.891, role-filler 0.840,
  plana 0.890. La propiedad "nombre propio" vive en LA PALABRA, no en el contexto; al enmascarar,
  el contexto no lleva señal. Cuenta como límite honesto: el sustrato no clasifica lo léxico por contexto.
- **0056h género (etiqueta DISTRIBUCIONAL, por el determinante el/la):** SÍ funciona — baseline 0.553,
  plana 0.804, role-filler 0.673. La señal vive en el contexto (el determinante). La PLANA gana
  porque el género es detectable por PRESENCIA del determinante, no por su POSICIÓN.
- **0056i orden (etiqueta POSICIONAL, ¿es 1ª palabra de contenido?):** lineal no alcanza — baseline
  0.716, role-filler acc 0.627/f1 0.202, plana acc 0.679/f1 0.127. El rol capta el orden (f1 del rol
  > f1 de la plana) pero un classifier lineal sobre el contexto mezclado no vence el baseline.
- **0056j decoder por ROL EXPLÍCITO (unbinding, cierra el arco):** N=128 FALLA (gap 0.428 < lineales
  0.536) por ruido aditivo; **N=1024 CIERRA: gap-recuperado = 1.000** (recupera PERFECTO la posición
  enmascarada, aplasta a los lineales). Técnica: rellenar con PAD, `u=unbind(role[j], ctx_sin_objetivo)`,
  `argmin_j max_cosine(u, vocab)` = hueco. Sin pesos entrenados. Receta + bug-patterns en
  `fase7_clasificacion_0056j_rol_explicito.md`.

### Veredicto del arco 0056g→h→i→j
- LÉXICA: contexto no lleva señal → falla.
- DISTRIBUCIONAL: señal en contexto → plana gana (>baseline).
- POSICIONAL lineal: rol capta orden (f1>plana) pero lineal no alcanza.
- POSICIONAL rol-explícito N=1024: gap=1.000 → el rol codifica orden y es RECUPERABLE por unbinding.
El único límite honesto es de CAPACIDAD (N chico interfiere; N grande resuelve), coherente con la
curva suave de 0029. El sustrato HD role-filler HACE: memoria (0056f), composición sistemática
(0056e), clasificación distribucional (0056h) y recuperación de orden por rol (0056j N=1024).

## Resolución conceptual: 0029-suave vs 0059h/i-binario (aporte de Luciano)
- 0029 (superposición plana) = SUMA (interferencia ADITIVA): cada ítem extra es ruido que se
  acumula; el clean-up recupera mientras la señal supere al ruido → curva SUAVE y (en principio)
  reversible con más dims.
- 0059h/i (punteros anidados) = PROYECCIÓN (función MANY-TO-ONE): el hijo grande se COMPRIME al
  cajón chico; muchos hijos distintos colapsan al MISMO vector → no es ruido que crece, es
  INFORMACIÓN QUE DESAPARECE (no inyectiva) → colapso BINARIO (o el sub-espacio alcanza K=3, o
  TODO colapsa).
- En criollo: 0029 es ruido que se acumula; 0059h/i es información que se borra. El puntero no
  falla por "resonator débil", falla porque la proyección destruye identidad (no inyectiva) y eso
  no se arregla afinando — exige aislamiento (slots separados).

## Bug-patterns stdlib-HD reutilizables (costaron corridas en 0056d-0056j)
1. **urllib `.read()` entero → IncompleteRead en ~2.2 MB** → leer en chunks de 65536 en loop.
2. **Sigmoid overflow** cuando `z=W·x` explota (contexto HD suma muchos ±1): clip `z=max(-30,min(30,z))`
   antes de `1/(1+exp(-z))`. Sin clip → `OverflowError` y crashea el fit.
3. **Contexto HD no normalizado** → `W·x` diverge. Normalizar `ctx/=sqrt(sum(ctx²))` antes de entrenar.
4. **BinDecoder importado arrastra su propio N** (ej. 256) → IndexError si el script usa N=128/1024.
   Definir `BinDecoderLocal(seed, n=N)` con `n` local; no importar el de otro experimento.
5. **Índice de binds vs índice de oración**: al filtrar vocab fuera, binds solo tiene in-vocab;
   indexar binds con el índice de la oración da IndexError. Usar el índice de `enumerate(binds)`,
   o rellenar con PAD antes de filtrar (opción 0056j).
6. **Token case-sensitive en vocab**: `wordvec["El"]` KeyErrors si vocab está en minúsculas;
   canonicalizar `tl=t.lower()` al construir binds.

## Secuencia honesta de la línea (para no re-hacer)
0056 regla inyectada=1.0 TRAMPA → 0056b afinidad ~0.35 → 0056c presión ~0.59 → 0056d decoder
entrenado ~0.60 (cuello=código discreto) → 0056e HD role-filler 0.81-0.93 ROMPE. Decode anidado:
0059/59b/59c HRR-sumado ~2-3 niveles → 0059d-f resonator no rompe → 0059g slots separados prof12 →
0059h/i barrido confirma binario (proyección borra identidad). Conclusión: el sustrato compositivo
de SGM requiere CÓDIGO HD/continuo (role-filler, slots separados), no discreto posicional. Uso real:
0056f memoria OK (top-1=1.0); 0056g-h-i-j clasificación real con arco cerrado por rol-explícito N=1024.
