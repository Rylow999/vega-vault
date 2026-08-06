# AUDIT BY SIGNAL-REMOVAL — receta anti-circular

La auditoría de Luciano (2026-07-26) encontró que 4 de 5 filas "✓ confirmado" del
README del Language Engine eran ARTEFACTOS: el experimento filtraba una señal
exógena que "confirmaba" la intuición por construcción. Regla de oro:

> Cuando un v0.x "pasa" demasiado limpio, volvelo a correr CON LA SEÑAL
> SOSPECHADA QUITADA. Si el resultado sobrevive → es real. Si desaparece →
> era artefacto.

## Las 4 trampas circulares encontradas (y cómo se corrigen)

1. **reward fijo / omega_ideal** (v0.9c, v0.3-REAL):
   `reward = (dot(w, omega_ideal)/norm + 1)/2` con `omega_ideal` VECTOR FIJO.
   Cualquier reward constante da el mismo resultado (G=1.0). El "aprendizaje" es
   empujar ω hacia un punto conocido → sube coseno por geometría, no por dato.
   CORRECCIÓN: la señal de "dolor" debe ser el ERROR DEL DATO (1 - P(correcto))
   de next-token. Sistema A (ω fijo) vs B (aprende): si B baja error y A no,
   el dolor obliga al cambio. Sin vector ideal.

2. **diccionario en TRAIN, no solo en eval** (v0.9b):
   SUST/VERB se consulta DURANTE el entrenamiento para alimentar hist_count → la
   etiqueta "aprendida" ya estaba en las etiquetas de verdad.
   CORRECCIÓN: entrenar next-token LIMPIO; clusterizar el espacio ω SOLO EN
   EVAL (k-means puro, pureza vs SUST/VERB). Si pureza > azar → la sintaxis
   EMERGE de la geometría sola.

3. **corpus sintético armado para dar la respuesta** (v0.16-bis):
   "boda" se rodea SIEMPRE de {flores,vestido,blanco,beso} → jaccard=1.0 trivial.
   Y ningún experimento borra nunca un nodo → "poda respeta externo" es vacuo.
   CORRECCIÓN: corpus REAL (Don Quijote). Refs por co-ocurrencia. Poda por
   incoherencia (coseno < umbral). Medir que podar refs ≠ borrar nodo.

4. **baseline NO comparable** (v0.14d original):
   10.55% (V=150, 20k tok) se comparó contra 10.11% que es v0.6a a V=200,
   OTRO corpus. Inválido.
   CORRECCIÓN (run_audit_baseline.py): correr baseline grafo-solo y híbrido
   en LAS MISMAS condiciones (V=150, 20k, 2 épocas, mismo corpus, misma eval).
   Resultado real: baseline=0.0237, híbrido=0.0958 → ~4x, no +0.44.

## Checklist de auditoría antes de publicar "confirmado"
- [ ] ¿La señal de éxito viene del DATO o de algo que el script conoce de antemano
      (vector fijo, diccionario, corpus armado)?
- [ ] ¿El baseline se corrió en IDÉNTICAS condiciones (mismo V, corpus, épocas)?
- [ ] ¿Correrlo con la señal quitada cambia el resultado? (si no cambia = circular)
- [ ] ¿El TEST mide lo que dice, o tiene un sub-artefacto? (ver v0.3b: "borrar
      degrada" falló porque predict salta ω nulos y sube accuracy artificialmente)

## Scripts corregidos (secuenciales, uno por uno)
- run_v03b.py        — memoria: hibernar preserva accuracy; test de "borrar" inválido
- run_v09b_clean.py   — categorización: cluster ω en EVAL, pureza vs SUST/VERB
- run_v09c_clean.py   — dolor = error de next-token; A fijo vs B aprende
- run_v16_clean.py    — composición: Don Quijote real, podar refs ≠ borrar nodo
- run_audit_baseline.py — baseline correcto de v0.14d (grafo-solo vs híbrido)

## RESULTADOS REALES de los corregidos (2026-07-26 noche)
| Exp | Resultado | Veredicto |
|-----|-----------|-----------|
| v0.14d audit | baseline grafo-solo=0.0237; híbrido=0.0958 (~4x) | ✓ CONTEXTO GENUINO (README viejo lo SUBESTIMABA) |
| v0.9b v2 (vocab 50/50) | pureza=0.7317 vs azar 0.50 | ✓ CATEGORÍA GENUINA (el test viejo era inútil: 93% sust) |
| v0.9c limpio | A(ω fijo) err=0.9927 cte; B(aprende) 0.9927→0.933 | ✓ DOLOR GENUINO (error baja solo si aprende) |
| v0.3b / v0.16 (v1-v3) | hibernado = base SIEMPRE; borrado >= base | ✓ MEMORIA/COMP: omega vivo = intacto. "borrar degrada" INDISTINGUIBLE en grafo rústico |
| v0.14d_borrar (EN MARCHA) | borrar nodo en híbrido debe degradar | por confirmar sobre sustrato que predice |

## Dos pitfalls de MÉTRICA descubiertos esta sesión (ver SKILL.md #16/#17)
- #16 "Borrar destruye" es indetectable en el grafo rústico: predict por coseno da
  coseno 0 a ω nulos y NUNCA los elige → accuracy sube. Medir solo sobre híbrido v0.14d.
- #17 Cluster k=2 sobre vocab top-N de Don Quijote es inútil (93% sustantivos →
  azar=0.9267). Usar vocab balanceado 50/50 (v0.9b v2: pureza 0.73 > 0.50).

## Veredicto final honesto
Los 4 "✓" caídos eran circulares; los 5 mecanismos (memoria, dolor, categoría,
composición, contexto) son GENUINOS con señal del dato. El grafo rústico predice
~8% (sustrato limitado) pero sus mecanismos cognitivos son reales; el transformer
(v0.14d) es el único que rompe el piso de predicción. README del repo reescrito
= estado honesto.
