# Paloma-π vision + BORIS dataset (dominio para exp_SGM_0020)

Contexto de la charla 2026-08-02 (post-0019). Luciano trajo una nota "Paloma-π" (comunicación
humano-paloma vía SGM) y luego la corrigió honestamente: el punto "datos etológicos públicos
etiquetados" NO existe como dataset listo para Columba livia — es redactado como si existiera.
La solución honesta que propuso: generar el dataset PROPIO con **BORIS** (Behavioral Observation
Research Interactive Software, open-source, gratis, con espectrograma de audio sincronizado).

## Por qué importa para SGM
Paloma-π es el CASO DE USO de todo lo construido en la sesión:
- Codificador Sensorial (audio FFT + pose + GPS → TSE) == exp_SGM_0019 (SensorBridge, HDC binding).
- "Valencia sube si entrada ambigua" == Eq.6 dolor (exp_SGM_0014 / 0015).
- Métrica Nº1 (homeostasis = baja valencia = éxito) == loop saludable del 0014/0015.
- Métrica Nº2 (validación etológica: si dice "peligro" y la paloma huye, acertó) == el ground
  truth CONDUCTUAL que el 0017 NO tenía (medíamos resolución interna, no conducta real). Esto es
  la aplicación de la DSCN-G LOOP RULE ("no declarar loop exitoso sin validación externa").
- Self-mod (exp_SGM_0018) sobre las conexiones TSE→nodo etológico: si la conducta valida la
  inferencia → PROMOVER; si falla → marca a fuego / revierte.

## Riesgos marcados (no olvidar al retomar)
- **Decoder L2 lineal NO funciona.** La nota Paloma-π dice "proyector lineal" para humanos, pero
  el roadmap Fase 5 ya advirtió: similarity-NN / proyección lineal sobre embeddings FALLA
  (v0.25 v12 top1=0.020). El decoder debe ser bigrama o transformer entrenado sobre alineamiento
  ω↔texto (Fase 5, no ahora).
- **Grafo de conceptos etológicos debe EMERGIR, no estar etiquetado por biólogos.** El self-mod
  (0018) es el mecanismo: si la paloma hace algo no previsto, el sistema duda; si duele, lo marca.
- **No asumir dataset ajeno.** BORIS genera el ethogram desde videos propios (o de YouTube). Hasta
  tenerlo, el 0020 es SYNTH con arquitectura REAL (TSE multimodal sintético → HDC → grafo →
  conducta simulada → self-mod). El dataset real solo cambia la FUENTE de la señal, no el loop.

## Diseño propuesto para exp_SGM_0020 (Paloma-π toy)
1. TSE multimodal sintético: audio FFT sintética (senoidal+ruido) + pose sintética (ángulos) →
   proyectar a ω_D via HDC reusando run_sensor_bridge.py.
2. Grafo de conceptos etológicos (hambre/peligro/cortejo/juego/sed) como nodos con ω/fase/vitalidad.
3. K cadenas (Eq.2) recorren el grafo; interferencia constructiva → nodo inferido.
4. Valencia (Eq.6): si TSE ambiguo (señales opuestas) → dolor alto.
5. Validación conductual SIMULADA: regla que dice "si infirió X, el ave hace Y_post"; comparar.
6. Self-mod (0018): si acierto → promover conexión TSE→nodo; si falla → marca a fuego.
7. Decodificador para humanos: postergado a Fase 5 (bigrama, no lineal).

## Nota filosófica
Paloma-π es un caso de prueba de la hipótesis de "conciencia alienígena" (NOTA_FILOSOFICA_0016_0017):
si la paloma tiene estados internos (hambre/miedo) estructuralmente similares a los nuestros y se
manifiestan en patrones físicos modelables, un sistema que modele esos estados PUEDE acercarse a
una forma de conciencia alienígena. Generaliza a "leer cualquier lenguaje animal/extraterrestre":
no necesitás saber el idioma, necesitás saber si tu inferencia predijo el comportamiento siguiente.
