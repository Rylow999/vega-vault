# Fase 7 — Decode por ROL EXPLÍCITO (unbinding) y RECUPERACIÓN DE ORDEN (exp_SGM_0056j)

Receta + hallazgos del cierre del arco 0056g→h→i→j sobre Don Quijote (corpus real, stdlib puro).

## La tarea que cierra el arco
"Dado el contexto con la palabra objetivo ENMASCARADA, ¿esa palabra era la PRIMERA palabra de contenido
de la oración?" — etiqueta 100% POSICIONAL. El BoW plano no puede saber qué slot ocupaba la palabra
ausente; el role-filler SÍ ve el "hueco" en rol 0. Cierra 0056i (donde un classifier lineal no alcanzaba).

## Técnica: decoder por rol explícito (NO entrenado, unbinding puro)
1. Rellena la oración con token PAD hasta MAXLEN (así solo el hueco verdadero da max-cosine bajo).
2. `full` = suma de `bind(role[i], wordvec[token_i])` para todos los slots.
3. Para cada posición j: `u = unbind(role[j], ctx)` donde `ctx = full - binding_objetivo`.
4. `max_cos(j) = max over vocab of cos(u, wordvec[w])`. El HUECO es `argmin_j max_cos(j)`
   (ruido puro → max-cosine bajo; palabra real → max-cosine alto; PAD → matchea PAD alto).
5. Sin pesos entrenados: la señal de orden vive en la estructura HD, no en aprendizaje.

## RESULTADO (lo que SÍ pasó, honesto)
- **N=128, V=1000, MAXLEN=10:** gap-recuperado = **0.428** (PEOR que lineales 0.536). FALLA.
  Causa: con ~9 bindings sumados en N=128, el ruido de los otros bindings (norma ~√(9·128)≈34) ensucia
  tanto que ni palabra ni hueco dan max-cosine distinguible. Interferencia aditiva, igual que 0029.
- **N=1024, V=300, MAXLEN=10:** gap-recuperado = **1.000** (recupera PERFECTO la posición enmascarada).
  APLASTA a los lineales (0.48/0.50). ARCO CERRADO: el rol codifica orden y se recupera con N suficiente.
- Lineales (role-filler / plana) colapsan a ~0.48-0.50 (no aprenden la tarea posicional pura).

## Veredicto del arco 0056g→h→i→j
- 0056g propio/común (LÉXICO): contexto no lleva señal → falla baseline.
- 0056h género (DISTRIBUCIONAL): señal en contexto → plana gana (>baseline).
- 0056i orden (POSICIONAL, lineal): rol capta orden (f1 rol>plana) pero lineal no alcanza.
- **0056j rol-explícito N=1024: gap=1.000 → el rol codifica orden y es RECUPERABLE por unbinding.**
Límite honesto: con N chico el unbinding naive falla por ruido; con N=1024 funciona. Eso es el régimen de
capacidad del HD role-filler (coherente con curva suave de 0029: más N = menos ruido relativo).

## BUG-PATTERNS stdlib-HD que costaron corridas (reutilizables)
1. **urllib `.read()` IncompleteRead en ~2.2 MB Gutenberg** → leer en chunks `resp.read(65536)` en loop.
2. **Sigmoid overflow** cuando `z = W·x` explota (contexto HD suma muchos ±1): clip `z = max(-30, min(30, z))`
   antes de `1/(1+exp(-z))`. Sin clip → `OverflowError: math range error` y crashea todo el fit.
3. **Contexto HD no normalizado** → `W·x` diverge. Normalizar `ctx /= sqrt(sum(ctx²))` antes de entrenar/evaluar.
4. **BinDecoder importado de otro módulo arrastra su propio N** (ej. 256) → IndexError si el script usa N=128/1024.
   FIX: definir `BinDecoderLocal(seed, n=N)` con `n` local; no importar el de otro experimento.
5. **Índice de binds vs índice de oración**: al filtrar tokens fuera de vocab, `binds` solo tiene los in-vocab.
   Si usás el índice de la oración (del `enumerate(s)`) para indexar `binds`, da IndexError. Usar SIEMPRE el
   índice del `enumerate(binds)`; o rellenar con PAD antes de filtrar (la opción usada en 0056j N=1024).
6. **Token case-sensitive en vocab**: `wordvec["El"]` KeyErrors si vocab está en minúsculas. Canonicalizar
   `tl = t.lower()` al construir binds.

## Performance (Android, sin numpy)
decode_gap = MAXLEN × V × N ops por sample. En N=1024, V=300, MAXLEN=10, ~840 test → ~2.5e9 ops → ~150-200s.
Para entrar en tiempo: capar V (300), NSENT (600), SAMPLE_CAP (2000). N=128 es ~8x más rápido pero falla.
N=1024 es el que cierra; vale la espera.
