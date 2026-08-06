# Fractal grafo + ruteo competitivo (VQ) — receta y progresión v0.21

Problema: "concepto = conjunto de subnodos con peso semántico distinto" (idea de
Luciano: banco = {lugar→[dinero,trabajo], objeto→[descanso]} resuelve polisemia por
construcción, no por inferencia). El root recibe las fases de los subnodos activos
(bottom-up), no las dicta — atención global EMERGENTE y barata.

## Progresión (qué falló y por qué)

**v0.21 v1/v2 (next-token, root bottom-up):**
- v1 promediaba todas las fases de los subnodos → vector borroso → acc 0.024 < plano 0.034.
- v2 tenía un root "director" pero `root_weight=1.0` y nunca lo usó para desempatar
  (bug: el score fue solo coseno local). También 0.024.
- Lección: next-token global es el PEOR test para grafo rústico; el transformer
  (v0.14d 9.6%) le gana por atención global aprendida.

**v0.21 v3 (desambiguación, test real de la idea):**
- 0/40 sentidos separados. Causa: `ka=i%K` → ROUND-ROBIN por posición de secuencia.
  Los subnodos se turnan a ciegas, cada uno recibe mezcla aleatoria de TODOS los
  contextos → nunca divergen. BUG detectado por auditoría de Luciano (línea `ka=i%K`).

**v0.21 v4 (VQ winner-take-all, fix del bug):**
- Ruteo: `k* = argmax_k cos(subnodo_k, contexto)` (competencia real, no i%K).
- Update: solo subnodo[k*] se mueve hacia target (Hebbiano); los otros quietos.
- Dead-code: si un subnodo no gana en N pasos, reinicializarlo cerca del contexto
  que más lo "casi-ganó".
- Resultado: 0/40 IGUAL, pero por COLAPSO AL GANADOR (cold-start WTA): el primero
  que gana se acerca a contextos futuros → gana siempre; el otro queda en 0 y el
  dead-code lo respawn en la misma región → re-pierde.

**v0.21 v5 (SOFT competition, fix del colapso — EN MARCHA 2026-07-28):**
- `w_k = softmax( cos(subnodo_k, contexto) / T )`, T alta al arranque (0.6).
- AMBOS subnodos se mueven, pesados por w_k (Hebbiano suave) → nadie queda en 0.
- T baja linealmente a 0.05 durante el entrenamiento (annealing): arranca suave,
  afila la competencia cuando ya hay especialización.
- 3 semillas, promediado (robustez).
- Hipótesis de Luciano: el colapso v4 era cold-start WTA, no escasez de señal; la
  competencia suave lo evita y los subnodos divergen. Si v5 da >0, la idea de
  fractal queda validada sobre grafo rústico.

## Receta mínima (reproducible)
```python
# contexto local = promedio de omega vecinos (ventana chica, sin Q/K/V)
ctx = mean(omega[vecino] for vecino in window)
# ruteo SUAVE con temperatura
T = T_min + (T_init - T_min) * (1 - step/total_steps)
sims = [cos(subnodo[k], ctx) for k in range(K)]
w = softmax([s/T for s in sims])
# update: todos los subnodos se mueven, pesados por w_k
for k in range(K):
    subnodo[k] = (1 - BETA*w[k])*subnodo[k] + BETA*w[k]*target
# dead-code: si un subnodo no gana en N pasos -> reinicializar cerca de su mejor "casi-ganó"
```
O(K·D) por nodo, solo productos punto. Sin gradientes, sin GPU, sin numpy.

## Si v5 sigue en 0/40
El límite es SEÑAL ESCASA en el grafo rústico (D=16, 20k tok): el contexto en D=16
es ruido, no hay señal para que 'banco+dinero' rutee distinto de 'banco+río'. La
idea de fractal sobrevive como ORQUESTADOR SOBRE transformer (v0.22): el transformer
(v0.17) da representaciones ricas donde los sentidos SÍ se separan (6/150). El root
fractal coordina dominios y habilita "no estoy seguro" emergente (2+ subnodos activos
sin dominante → duda). Eso no existe en una LLM (softmax siempre elige top-1).
