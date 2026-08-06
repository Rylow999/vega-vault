# Método: aislar la variable antes de declarar un límite de sustrato

(2026-07-28, Luciano corrigió un error de visión de la agente en v0.21.)

## El error
Tras v0.21 v1→v5 (0/40 sentidos separados), la agente concluyó "el grafo rústico
D=16 no tiene señal / aplana". Era una conjetura no probada. La verdad: el grafo
podía separar (v0.21 v6 llegó a 50 palabras separadas en la época 11) pero:
- el corpus (Don Quijote) tiene polisemia rara y poco frecuente → poca señal,
- la medición fue prematura (solo 2 épocas; el grafo arranca de ruido y mejora
  con el tiempo, no al instante como una LLM pre-entrenada),
- el VQ suave sin repulsión era inestable (separaba y recolapsaba).

## Por qué el grafo y el transformer NO son comparables a iguales épocas
- Transformer v0.14d/17 viene PRE-ENTRENADO: millones de ejemplos, embeddings ya
  útiles. Da 9.6% a las 2 épocas porque ya "sabe".
- Grafo rústico arranca de RUIDO GAUSSIANO puro. Su curva de aprendizaje empieza en
  cero y sube con las épocas. Medirlo a las 2 épocas y compararlo con un transformer
  a las 2 épocas es comparar estados opuestos (ruido vs útil).

## Protocolo de aislar la variable (correr ANTES de decir "no puede")
1. CURVA DE ÉPOCAS: correr 10-15 épocas y medir el efecto por época. Si sube con el
   tiempo → el sistema mejora con el tiempo (hipótesis de Luciano) y el límite era
   premura, no sustrato.
2. CORPUS CONTRASTIVO: armar un corpus SINTÉTICO PEQUEÑO con la señal fuerte y
   explícita que el corpus real no da. Ej. polisemia: "banco" 50× sentido A
   (dinero) + 50× sentido B (río), intercalados. Si el grafo SEPARA ahí → la culpa
   era el corpus real (señal escasa), no D=16.
3. UMBRAL RELAJADO: contar separación 60/40, no solo 85/15, para no descartar
   divergencia parcial prematura.
4. VOCAB = todas las palabras del corpus (PITFALL #21); la evaluación filtra después.
5. SI el grafo SÍ separa en corpus contrastivo + curva → el límite era aplicación,
   no sustrato. Documentar "D=16 puede, el bug era X".

## Plantilla de corpus contrastivo (polisemia)
```
poly = {
  "banco": (["dinero","pagar","cuenta","oro","plata"], ["rio","agua","pez","orilla","puente"]),
  "llave": (["puerta","cerradura","abrir","candado"], ["musica","nota","tono","cancion"]),
  "mouse": (["computadora","click","pantalla","cable"], ["animal","cola","raton","hueco"]),
}
filler = ["el","la","de","y","en","con","por","un","una","que","los","las"]
for w,(sa,sb) in poly.items():
    for _ in range(50):
        seq += [rng.choice(filler) for _ in range(3)] + sa[:3] + [w] + sa[1:3]
    for _ in range(50):
        seq += [rng.choice(filler) for _ in range(3)] + sb[:3] + [w] + sb[1:3]
rng.shuffle(seq)
vocab = list(dict.fromkeys(seq))   # TODAS las palabras vistas
poly_words = list(poly.keys())     # solo estas se evalúan
```

## Señal de alarma
Si la agente dice "el sustrato no puede / aplana / no tiene señal" → STOP. Pedir:
¿se corrió la curva de épocas? ¿se usó un corpus contrastivo? Si no, es una
conjetura. Aislar la variable primero.
