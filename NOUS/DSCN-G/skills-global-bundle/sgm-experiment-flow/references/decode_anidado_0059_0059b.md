# Decode anidado profundo — 0059 / 0059b / 0059c (sesión 2026-08-04)

## Contexto
Cerramos composición relacional plana y anidado 1 nivel (0058, TopSim 0.75-1.0). Quedaba pulir el
decode ANIDADO PROFUNDO (>2 niveles).

## Mecánica probada (test-first en Python)
HRR con convolución circular (Plate 1995): bind=conv circular, unbind=permutación inversa de índices
(`b[i]=a[(-i)%n]`, NO FFT — la FFT casera daba unbind roto). gen_vec = ruido gaussiano normalizado.
Cleanup contra VOCAB por coseno.

## Opción 1 — Subir N (más dimensiones = menos crosstalk)
  N=64 : prof1=1.00 prof2=0.67 prof3=0.67   (techo ~2 niveles)
  N=256: prof1=1.00 prof2=0.90 prof3=0.67   (subió a prof2, prof3 estancado)
  N=512: TIMEOUT en Android (conv N²=262144 ops/bind). No usable en celular.
VEREDICTO: HRR puro satura en ~2 niveles. Subir N es "comprar espacio", no resolver la raíz.

## Opción 2 — TPR-walk (punteros que bajan niveles, Plate 2003)
  prof3=0.56 prof4=0.53 prof5=0.58 → PEOR que HRR plano. El "puntero de nivel" se suma al filler y
  al desatar queda mezclado con el ruido de los otros roles del padre (mismo error de contaminación:
  el hijo queda atrapado en suma(bind(rol,filler)) del padre).

## Caso 0059c — TPR-walk CORRECTO (filler autónomo, NO re-sumado)
El filler hijo viaja como vector AUTÓNOMO (ya codificado, no se re-ató). Resultados (N=128,
prof 3/4/5/6): 0.56/0.53/0.58/0.67 → TAMPOCO rompió el techo. Causa raíz: el unbind de HRR N=128
NO aísla limpio el filler cuando la bolsa tiene 3 bindings; el ruido de los otros 2 roles del padre
contamina al hijo. Límite físico de HRR-sumado (Plate 1995).

## BANDERA ROJA POST-HOC — exp_SGM_0056 (lo más importante de la sesión)
Luciano detectó que 0056 reportaba TopSim=1.0 como "composición plena emergente", pero la estructura
(region→pos0, distancia→pos1, tipo→pos2) está HARDCODEADA en `RuleLearner.infer_rule`. El 1.0 es
regla INYECTADA en el aprendiz, MISMA falla que 0049d. 0056 y 0055a responden preguntas DISTINTAS
(0055a=¿emerge con aprendiz genérico? ~0.35; 0056=¿techo si das inferir regla exacta? no, 1.0).
CORRECCIÓN APLICADA y pusheada: registry 0056 → ACLARACION_REQUERIDA; 0058 depuró la cita; 0059
matizó marco. Ver regla 5 y ítem 12 de ANTI-PAPER-VISION en SKILL.md. El contraste decisivo
(0056b, aprendiz genérico) dio ~0.35 y confirmó que el 1.0 de 0056 era regla inyectada. Ver
references/language_ilm_0055_0056.md.

## Regla de flujo que Luciano reafirmó
- "No lo hagas a las apuradas... es importante que nos lleve el tiempo necesario" → ante mecanismo
  que no anda, DETENERSE, testear en Python, mostrar métricas, recién portar.
- "Explicame todo en criollo por favor" → en modo investigación abierto, reporte en criollo:
  qué hacemos, diferencias, por qué es necesario, qué podemos probar.
- "no quisiera emocionarme al pedo" → veredicto honesto aunque el mecanismo no escale.

## 0059d — Resonator Network (Frady 2020) sobre roles indep por nivel (0027c)
Idea de Luciano: Resonator resuelve el problema de factorización vectorial cuando hay varios bindings
superpuestos (mi caso prof>=3). En vez de unbind una vez, ITERA restando las estimaciones de los OTROS
roles y desatando el objetivo, luego clean-up. Busca en superposición. La estructura de roles
independientes por nivel ya la tenía 0027c. RESULTADO HONESTO: mi impl NO converge (prof3=0.00,
status INTENTADO_NO_CIERRA) por dos causas reales: (1) clean-up final solo conoce SÍMBOLOS, no
HECHOS anidados → el filler hijo se pierde; (2) HRR de juguete mal calibrado (magnitudes/normalización)
no converge en 20 iter con N=64. El survey 2020/2025 avisa: capacidad decrece con nº de factores para
D fija (no es magia infinita). Conclusión: el resonator requiere clean-up con memoria de sub-estructuras
y VSA bien calibrada (FHRR/MBAT); mi impl no los tiene. NO se suma como solución hasta recalibrar.
Detalle completo en references/decode_resonator_0059d.md.
