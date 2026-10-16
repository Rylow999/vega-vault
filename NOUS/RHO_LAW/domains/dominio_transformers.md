# Dominio: Redes neuronales / Transformers — la ley ρ en deep learning

**Fuente:** paper FHRR + observaciones de la literatura

## El análogo

Una capa de atención proyecta queries/keys sobre un espacio de dimensión d_k.
Cuando la atención distribuye su presupuesto sobre n_heads y la dimensión por
cabeza cae por debajo del umbral de resolución, la representación se degrada
**de forma no gradual** (como predice la ley ρ: singularidad, no decaimiento suave).

Evidencia circunstancial:
- Los fallos de LLMs al recuperar "la palabra exacta en el medio de una
  secuencia larga" (lost-in-the-middle) son errores categóricos, no graduales.
- Los modos de fallo por "head collapse" en Transformers aparecen con
  umbrales discretos (n_heads vs dim).

**Experimento posible (futuro):** en un modelo chiquito, reducir artificialmente
la dimensión por cabeza hasta cruzar el "ρ=1" efectivo y medir si el accuracy
cae en escalón (singularidad) o en rampa (capacidad).

Estado: pendiente. Requiere entrenamiento corto controlado.
