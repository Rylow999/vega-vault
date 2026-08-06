# Decode anidado profundo (0059g/h/i) + Emergencia de composición (0056c/d/e)

Receta y veredictos de la tanda 2026-08-04. Complementa `decode_anidado_0059_0059b.md`
(HRR plano satura ~2 niveles) y `decode_resonator_0059d.md` (resonator no rompe techo).

## 1. DECODE ANIDADO — barrido de bindings por bloque (aportes de Luciano)

### Setup canónico (BlockBundle, reusado en 0059g/h/i)
Hecho = tupla (SUJ, ROL, OBJ) donde OBJ puede ser otro hecho (anidado). Rol-filler:
- K bloques físicos de BLK dims. Role asignado por `j % K` (K=1: todo en un bloque; K=3: un rol por bloque = slots separados).
- Hijo apuntado por PROYECCIÓN circular-mean N→BLK dentro del bloque que le toca (K=3: bloque OBJ del padre).
- Decode: bloque de 1 rol → clean-up directo; bloque multi-rol → RESONATOR canónico (M_i⁻¹ por bloque, mat_vec) que desata los roles.
- `find_child(filler, mem)`: el filler proyectado se compara por coseno contra los hechos hijos en mem; si `sim > umbral_símbolo` → FACT (recurre), sino SYM. Decidir FACT-vs-SYM por SIMILITUD, no por marca de nivel (la marca se diluye por norma total).

### 0059g — SLOTS SEPARADOS rompen el techo (PASÓ)
K=3 (cada rol su bloque, hijo apuntado en bloque OBJ del padre sin mezclarse con SUJ/ROL).
Resultado: 1.00 de prof 3 a 12. CIERRA el decode anidado: el mecanismo es ARQUITECTURA DE SLOTS
SEPARADOS, no ILM. Es legítimo (como ADN/instinto en red line: el esquema de enlace no es la respuesta).

### 0059h — BARRIDO K=1/2/3 → CURVA BINARIA
| K | N=64 | N=128 | N=192 |
|---|------|-------|-------|
| K=1 (superposición pura) | prof0 | prof0 | prof0 |
| K=2 (SUJ+OBJ / ROL) | prof0 | prof0 | prof0 |
| K=3 (slots separados) | prof8 | prof8 | prof8 |
Veredicto: resonator canónico NO salva el anidado bajo superposición. Solo aislamiento total (K=3) abre.

### 0059i — K=2 con PUNTERO-ROL EXPLÍCITO (intentó matizar, confirmó el cuello)
Dio al puntero su propio vector-rol (PTR) DENTRO del bloque compartido (bloque0 = SUJ, OBJ, PTR; bloque1 = ROL), T resonator=40, umbral puntero 0.5.
Resultado: K=2 sigue prof0. Diagnóstico por RecursionError: al proyectar el puntero circular-mean (N→BLK) se
COLABSA la identidad del hijo → todos los punteros se parecen → `find_child` siempre matchea → bucle.
Con corte de recursión (MAXDEPTH=12) K=2 da prof0 en serio.
**HALLAZGO:** no es que el resonator no desate; es que LA PROYECCIÓN DEL PUNTERO DESTRUYE LA IDENTIDAD DEL
HIJO (función many-to-one, no inyectiva). El puntero exige su PROPIO SUB-ESPACIO FÍSICO (K=3); no alcanza
con "su propia voz en bloque compartido" porque el bloque sigue siendo más chico que el hijo.

### Conclusión del barrido (0059h + 0059i)
Decode anidado en SGM requiere SLOTS SEPARADOS (K=3). Cualquier superposición de un rol-puntero con otros
roles colapsa por pérdida de identidad en la proyección. No es cuestión de "afinar el resonator".

## 2. PREGUNTA CONCEPTUAL (Luciano): ¿por qué 0029 degrada SUAVE y 0059h/i colapsa BINARIO?
Es el TIPO de operación, no la cantidad:
- **0029 (superposición plana) = SUMA (interferencia ADITIVA).** Cada ítem extra es ruido que se acumula;
  el clean-up recupera mientras la señal propia supere al ruido. Curva SUAVE y (en principio) reversible
  con más dims. (Analogía: fiesta con más gente, voces se cruzan.)
- **0059h/i (punteros anidados) = PROYECCIÓN (many-to-one).** El hijo grande se COMPRIME al cajón chico;
  muchos hijos distintos colapsan al MISMO vector. No es ruido que crece, es INFORMACIÓN QUE DESAPARECE
  (no inyectiva). Por eso es BINARIO: o el sub-espacio alcanza (K=3) o TODO colapsa (RecursionError 0059i).
  (Analogía: código postal de 3 dígitos para 1000 casas.)
LENTE REUTILIZABLE: al diagnosticar por qué falla una superposición, distinguir SIEMPRE "ruido acumulativo
reversible" (suma) de "pérdida de identidad irreversible" (proyección). No es lo mismo y el fix es distinto
(más dims vs aislar sub-espacio).

## 3. EMERGENCIA DE COMPOSICIÓN — romper el techo 0.6 (0056c → 0056e)

### Setup canónico (ILM, reusado en 0056b/c/d/e)
Referentes = REGION(4) × DIST(2) × TIPO(3) = 24. Cada referente tiene 3 rasgos. TopSim = Spearman entre
(distancia de rasgos) y (distancia de Hamming en código). ~1.0 = composición sistemática plena.
Presión de transmisión: learner ajusta SUS códigos para que un decoder reconstruya los rasgos; el decoder
NO asume posiciones fijas (busca en TODAS las posiciones) → no inyecta la gramática (evita trampa 0056).

### 0056c — presión de transmisión, decoder por CONTEo: ~0.59
Learner con sus códigos + decoder inductivo (Counter de símbolo→valor de rasgo por posición, elige la pos
que más predice). TS_full ~0.59 constante (sweep frac 0.4-0.9). Confirma: afinidad sola (~0.35) no alcanza
y decoder por conteo no cierra.

### 0056d — decoder ENTRENADO (backprop stdlib) NO cierra: ~0.60
Mismo learner, decoder = regresión logística multinomial por rasgo, W libre en todas las posiciones
(cross-entropy, sgd 60 epocas). TS_full ~0.6 (NO sube a 1.0). dec_err_seen BAJA (0.11-0.33, reconstruye
vistos) pero topSim_seen cae a ~0.33 (el código visto se desordena para que el decoder acierte) mientras
topSim_unseen queda ~0.76.
**HALLAZGO:** el decoder entrenado NO es bala de plata. Ayuda a vistos, pero la composición PLENA no emerge.
El cuello NO era el decoder: es el CÓDIGO DISCRETO (tupla L=3, V=16) con ambigüedad irreducible de mapeo
posicional. Decoder entrenado = necesario pero NO suficiente.

### 0056e — CÓDIGO HD ROLE-FILLER ROMPE el techo: 0.81-0.93
Cambió el TIPO de código: cada rasgo atado a su vector-rol; código = suma de bindings en N=256 dims
bipolar. Decoder lineal entrenado desata cada rasgo por unbind (sin ambigüedad posicional).
- MODO A (HD fijo + decoder oráculo): TS_full=0.824, dec_err=0.000.
- MODO B (learner SUS códigos HD + presión transm. frac=0.4): TS_full=0.81-0.93, dec_err g19=0.000 (3 seeds).
  Vistos y no-vistos ambos ~0.85-0.92.
**Veredicto:** el techo 0.6 era del CÓDIGO DISCRETO. HD role-filler lo ROMPE: la composición plena EMERGE
desde parcial (frac=0.4), sin regla inyectada ni oráculo. MODO A da 0.82 (no 1.0) por solapamiento aditivo
de los 3 bindings HD; con N mayor se acercaría a 1.0.
HONESTIDAD: HD role-filler es arquitectura distinta del sustrato discreto (como 0059g slots separados y
0019 HDC). El 0.91-0.93 es del esquema de enlace HD, no del sustrato discreto puro. El sustrato discreto
se estanca ~0.6; el HD continuo rompe a 0.81-0.93.

### Línea 0056 → 0056e
- 0056 regla inyectada: 1.0 = TRAMPA (hardcode en el aprendiz).
- 0056b afinidad sola: ~0.35.
- 0056c presión transmisión (conteo): ~0.59.
- 0056d decoder entrenado discreto: ~0.60 (cuello = código discreto).
- 0056e código HD role-filler: 0.81-0.93 (ROMPE el techo; emergencia real con HD).

### CONEXIÓN de las dos líneas (decode anidado + emergencia de composición)
Ambas requieren ENLACE POR ROL EN ESPACIO CONTINUO, no código discreto posicional:
- 0059g (slots separados) y 0059i (colapso de identidad del puntero) → el sustrato compositivo necesita
  sub-espacios separados / HD para no perder identidad por proyección.
- 0056e (HD role-filler) → la composición sistemática EMERGE si el código es HD continuo.
El sustrato DISCRETO es el límite (~0.6); el HD es el mecanismo que lo rompe. Esto conecta con 0019 (HDC
SensorBridge) y 0059g: el enlace por rol en espacio continuo es la clave del sustrato compositivo de SGM.

## 4. RECETAS REUTILIZABLES
- Barrido K (BlockBundle): `br` = role→bloque por `j%K`; `self.roles[b]` dimensionado a `len(br[b])` (NO a K
  fijo); índice DENTRO del bloque es local (enumerar `roles`), no `j` global; `Minv[b]` UNA matriz por bloque
  (no por rol); `proj_fhr` recibe VECTOR COMPLEJO (no tupla), promedia por segmento N→BLK.
- HD role-filler: `code_of(vals, role, valvec)` = `Σ_k bind(role[k], valvec[k][valor_k])`; decoder desata con
  `unbind(code, role[k])` (role bipolar ±1 es autoinverso) + softmax(W_k @ unbind). Para TopSim usar distancia
  cosine (no Hamming discreto) porque el código es continuo.
- Test de fuego estructural aplicado: 0056d diagnosticó "cuello = código discreto" (no decoder) → 0056e cambió
  la VARIABLE de código (HD) en vez de seguir tunenando el decoder. Eso rompió el techo. (Patrón ya en skill:
  "test de fuego estructural" + "cerrar sin tunear".)
