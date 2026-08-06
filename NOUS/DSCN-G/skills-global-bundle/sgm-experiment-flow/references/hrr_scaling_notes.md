# HRR Scaling / Ganancia Real al Subir D (exp_SGM_0029)

Receta reproducida del experimento que cerró la Fase 7 (composición relacional). El objetivo NO
era solo afirmar que "subir D ayuda" sino CUANTIFICARLO con variables discriminantes.

## Variables medidas (todas en el celular, O(D²) HRR)
1. **Acierto de anidamiento vs D** a profundidad d en {2,3,4,5}, M=200:
   - D=128: [1.0, 1.0, 1.0, 0.933]   <- unico punto debil
   - D=256/512/1024: [1.0, 1.0, 1.0, 1.0]
   -> subir D elimina el fallo a d=5.
2. **Capacidad M_max** (max items en memoria que mantienen acierto clean-up >=0.95 a d=5):
   - D=128: M_max = 200   (M=400 da 0.9, cae)
   - D=1024: M_max = 800  (todos los M hasta 800 dan 1.0)
   -> 4x mas capacidad al subir 8x D (teoria HRR ~sqrt(D) = 2.8x; medido mejor).
3. **Formas de anidamiento** (D=128, M=80): lineal=1.0, arbol=1.0, ciclico=1.0.
4. **NC**: recuperado vs vector random = 0.013 (senal no es ruido).

## Trucos de ejecucion en celular (Android)
- **TRIALS por D**: trials = 15 si D<=256 sino 6. A D=1024 cada HRR bind es ~1M ops.
- **CORRER EN BACKGROUND** (terminal background=true, notify_on_complete=true) para D>=512:
  el sweep completo tardo ~650s. No bloquear el foreground.
- **Sweep de capacidad solo a extremos** (D=128 vs D=1024), no todos los D, para ahorrar CPU.

## TRAMPA de diseno que costo un run falso-negativo (arbol=0.067, ciclico=0.0)
En measure_form el rol se uso INCONSISTENTEMENTE:
- CONSTRUIR: build_relation([a1,a2], [role_vecs[a1], role_vecs[a2]], ...) -> rol = indice REAL del item.
- RECUPERAR: recover(Rh1, 1, role_vecs, ...) -> usa role_vecs[1] = POSICION en la relacion.

Como build_relation internamente hace hrr_bind(role_vecs[k], mem[idxs[k]]) (k=posicion), y
recover hace hrr_unbind(R, role_vecs[k]) (k=posicion), la convencion correcta es POSICION en
ambos. El fix: en measure_form pasar role_vecs[0], role_vecs[1] (posiciones) en build y recover.
Al fijarlo, las 3 formas dieron 1.0. Regla: el rol de construccion y recuperacion debe coincidir
en significado (posicion vs indice de item).

## NC honesto de anidamiento
Un NC de orden 2 (Y->X->A) pasa AUN con rol fijo, porque no hay competencia de niveles. El NC
valido es orden 3: Y R2 X, X=(Z R1 W), W=(A R0 B). Con rol fijo (role_vecs[0] para TODAS las
aristas, superposicion unica) el unbind da la mezcla de todos los hijos -> anidamiento NO se
recupera (acierto 0.0). Ese si discrimino.

## Resultado
PASS. Fase 7 COMPLETA: SGM compone (0027c), navega relacionalmente (0027b), enchufa al tick (0028)
y escala 4x al subir D (0029). El sustrato composicional esta completo y cuantificado.
