# 0056j — Decoder por rol explícito (unbinding) sobre Don Quijote

## Objetivo
Cerrar el arco de 0056i: en 0056i un clasificador lineal sobre el contexto mezclado no recuperaba la
posición del hueco (role-filler captaba orden f1 0.20 > plana 0.13, pero no vencía baseline 0.716).
Acá se cambia el decoder: en vez de tirarle el vector mezclado a un clasificador, se hace UNBIND de cada
posición j y se busca la que queda sin palabra limpia (el hueco enmascarado). Sin entrenar pesos, solo
álgebra HD.

## Receta (stdlib puro, sin numpy)
- Don Quijote (Gutenberg pg2000, es). N=128, V_KEEP=1000, MAXLEN=10, 1000 oraciones.
- Tokenizar `re.findall(r"[a-záéíóúñü]+", text.lower())`; descartar oraciones con token fuera de vocab
  (filtro robusto: `if any(tk not in idx for tk in toks): continue`).
- Rellenar con "PAD" las posiciones libres (para que solo el hueco verdadero dé max-cosine bajo).
- `binds=[(i, tl, bind(role[i], wordvec[tl])) ...]`; `full = Σ binds`; contexto = `full - binding[hueco]`.
- `decode_gap(ctx)`: para j en MAXLEN: `u=unbind(role[j], ctx)`; `score = max_dot(u, vocab)/|u|`;
  gap = argmin score.
- Comparar contra lineal (BinDecoder LOCAL con N=128, NO el importado con N=256) y baseline.

## Bugs que costaron ciclos (detectables por lectura PRE-run)
1. `cidx` usaba índice de oración en vez de índice en `binds` → IndexError en `binds[sel]`.
   FIX: `cidx=[bi for bi,(oi,tl,b) in enumerate(binds) if is_content(tl)]`.
2. `KeyError 'licenciado'` / `'El'`: vocab muy chico (V=400) o tokens sin lowercase.
   FIX: subir V_KEEP=1000; canonicalizar `t.lower()`; filtrar oraciones con token fuera de vocab.
3. `BinDecoder` importado de 0056g usa `N=256` global; 0056j redefine `N=128` → IndexError en `_logits`.
   FIX: clase `BinDecoderLocal` con `self.n=N` local.

## Resultado (honesto)
- baseline acc = 0.710
- ROL-EXPLICITO gap-recuperado = 0.428, tarea-orden = 0.234
- lineal role-filler: acc = 0.536, f1 = 0.299
- lineal plana: acc = 0.508, f1 = 0.213

## Veredicto
El unbinding por rol NO recupera el hueco: 0.428 < lineales (0.536) y lejos de baseline (0.710). Con
MAXLEN=10 y ~9 bindings sumados en N=128, el ruido de los OTROS 8 bindings (norma ≈ √(9·128) ≈ 34)
ensucia tanto que ni la palabra real ni el hueco dan max-cosine distinguible del ruido — es
INTERFERENCIA ADITIVA pura (misma clase 0029-SUAVE). El argmin no elige el hueco. Los lineales superan
al rol-explícito porque el clasificador aprende a usar el contexto mezclado mejor que el unbinding ciego.

## Cierre del arco 0056g→h→i→j (taxonomía de etiquetas)
- 0056g LÉXICA (propio/común): falla baseline — la etiqueta vive en la PALABRA, no en el contexto.
- 0056h DISTRIBUCIONAL (género por el/la): supera baseline; plana gana porque basta PRESENCIA del determinante.
- 0056i POSICIONAL (1ra palabra de contenido): rol capta orden (f1>plana) pero decoder lineal no vence baseline.
- 0056j POSICIONAL + decoder por rol explícito: rol-explícito NO recupera el hueco (ruido aditivo N=128);
  requiere N-grande o decoder entrenado que aprenda a desatar.
- Conclusión: el role-filler SÍ codifica orden (evidencia f1 de 0056i), pero recuperar el hueco por
  unbinding naive necesita N≫128 (o decoder entrenado). Hallazgo real que delimita el régimen de
  capacidad del HD role-filler en recuperación posicional. NO es un fracaso: cierra el arco con veredicto
  honesto. (Para cerrarlo de verdad: 0056k con N=1024 para diluir el ruido y ver si el unbinding sí
  recupera el hueco.)
