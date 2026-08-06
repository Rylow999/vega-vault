# DSCN-G Language Engine — Idea de Luciano (candidata v0.3)

Fecha: 2026-07-25 (surge durante charla de v0.2).
Estado: ESBOZO, no experimentado.

## Idea
Una BASE DE DATOS SEMÁNTICA que use los valores de DSCN-G (ω vector, φ fase,
V vitalidad) como formato de almacenamiento nativo. No es "grafo que se poda
hasta 4 nodos" (v0.1) sino memoria de MASA persistida:

- Cada nodo se almacena como BITS + PUERTAS LÓGICAS en la misma RAM
  (no embeddings flotantes en disco, sino representación lógica/bitwise).
- La memoria se divide en VARIOS TIPOS y RELACIONES diferentes
  (tipo de nodo, tipo de arista), no un grafo homogéneo.

## Por qué encaja con v0.1/v0.2
v0.1 mostró que el punto fijo homeostático colapsa a ~4.5 nodos. Eso es
compatible con MEMORIA DE TRABAJO (working set), no con base de conocimiento.
La propuesta de Luciano es exactamente la "opción 3" del README de v0.1:
separar memoria de masa (persistida, V latente, NO se poda) de working set
(subgrafo activo ~N*). La DB semántica SERÍA la memoria de masa.

## Posible forma (a refinar)
- Tipo de slot: ENTITY / EVENT / PROPERTY / ACTION / RELATION (como las 4 raíces
  del reference code, pero persistidos).
- Cada nodo: ω (bits o float16 comprimido), φ (fase lógica), V (relevancia,
  decae pero NO se borra — pasa a estado HIBERNADO en vez de eliminado).
- Puertas lógicas: el GATEO de aristas (afinidad exp(-α‖ω_m-ω_n‖)) implementado
  como operación bitwise sobre los bits del nodo, no como norma flotante.
- Relaciones: aristas tipadas (ej: "mordió" es EVENT con slots agente/paciente).

## Qué falta para ser experimento
1. Decidir representación de bits (¿cuántos bits por nodo? ¿hash? ¿código?).
2. Decidir si φ es fase real o "tag" lógico.
3. Medir: ¿la afinidad bitwise es suficiente para recuperar conceptos, o se
   pierde semántica vs norma flotante?
4. Integración: ¿el working set de DSCN-G se "llena" desde esta DB masiva?

## Relación con la propuesta original (GPT)
GPT decía "100.000 nodos semánticos" como si fuera parámetro. Luciano lo baja
a tierra: eso requiere una MEMORIA PERSISTENTE aparte del bucle de poda. La DB
semántica es el componente que GPT daba por sentado y no existía.
