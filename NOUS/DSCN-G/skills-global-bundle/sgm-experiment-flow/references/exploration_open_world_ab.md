# Opción A (mapa cognitivo) vs Opción B (frustración) en exploración de mundo abierto

Hallazgos de la secuencia 0042→0043→0044→0045→0045b (Camino A, 2026-08-03). Complementa
`observatory_and_b_puro.md` (el modo de descubrir huecos) y `substrate_vs_authored_design.md`.

## Contexto
Tras 0043 (B-puro: frustración `abur` acoplada, cierra hueco de exploración global), Luciano pidió
experimentar "el resto": la Opción A = usar el grafo de ω como MAPA COGNITIVO GENERATIVO
(arXiv 2504.20628) para exploración DIRIGIDA en vez de solo por interrupción. Regla de Luciano:
SIN hardcode / SIN agregados extras / SIN bloqueos. El grafo de ω YA existe → la "huella"
(omega[celda] acumula al transitar) ES el mapa emergente, no un contador mío.

## 0045 — huir de lo conocido (`map_term = -w`)
- Cubre 110 celdas (NO se estanca, funciona) PERO sesga a la PERIFERIA: Q(1,1)=59.5% (dispersion 49.9
  vs 24.9 de B-puro 0043).
- Por qué: `-w` hace que el agente HUYA de donde ya estuvo → termina en el borde opuesto al arranque,
  donde toda la zona tiene huella baja → se queda ahí. Es "empuje al borde", no exploración uniforme.
- Marco: coherente con un random-walk con repulsión (termina en la periferia).

## 0045b — frente de exploración (`map_term = (huella_prom_vecinos - huella_celda)*0.5`)
- COLAPSÓ en 3 celdas (Q1,1=75.7%). El frente SENALA AL CENTRO de masa de lo conocido al arrancar.
- Por qué: al inicio TODO tiene huella ~0.1; `prom - w` es ruido que favorece volver al origen →
  oscila 3 celdas cerca del centro. El frente de exploración necesita un GRADIENTE de huella ya
  establecido; al arrancar de cero no lo hay.

## HALLAZGO CLAVE (durable, no es falla de diseño)
**El mapa cognitivo requiere EXPERIENCIA PREVIA poblada para ser útil.** En mundo abierto desde cero,
la Opción A se colapsa o sesga a la periferia porque el mapa no tiene suficiente huella. La Opción B
(frustración, 0043) NO tiene ese problema: funciona desde el tick 1 porque NO depende del mapa.
Esto es COHERENTE CON BIOLOGÍA: un animal recién nacido explora por curiosidad CIEGA, y solo desarrolla
un mapa espacial ÚTIL DESPUÉS de recorrer. El SGM replica eso.
→ **CONCLUSIÓN de diseño:** B-puro (0043) es el mecanismo BASE correcto para mundo abierto; la Opción A
  es inútil hasta tener el mapa poblado (futuro: reusar el mapa de ω SOLO después de N pasos de B-puro,
  o inicializar huella con un barrido previo). El sistema completo (0044) se queda con B-puro.

## Lección de DISEÑO DE TEST (propia del agente, 0045)
T-MG-02 asumía "exploración dirigida = cobertura UNIFORME". ESO ESTABA MAL PLANTEADO: la exploración
dirigida por familiaridad NO es uniforme por definición, es EFICIENTE (cubre lo nuevo primero, como el
filo del territorio animal). El fallo de T-MG-02 no era del mecanismo, era del supuesto del test.
REGLA (ya en SKILL.md como "sospechá de tu propio test antes que del mecanismo", rigid-test-label):
al fallar un test de "calidad de exploración", preguntarse si la MÉTRICA (uniformidad) es la variable
correcta. Para exploración dirigida la variable honesta es EFICIENCIA (cubre lo nuevo primero / no
repite), no uniformidad. Si el test asume uniformidad → es mal-planteado; reportarlo y corregir el test,
no retunear el mecanismo para pasarlo (eso sería la trampa de 0041).

## Cómo cerrar el hueco honestamente (si alguna vez se quiere A)
Si se retoma la Opción A, el fix legítimo del sustrato (no peso mío) sería: atraer al FRENTE usando el
grafo de ω para EXTENDER el frontier más allá del vecino inmediato (heterogeneidad de huella entre la
celda y el promedio de sus vecinos), PERO solo después de pre-poblar el mapa (ej. N pasos de B-puro
previos, o inicializar huella con un barrido). Sin pre-poblado, el frente colapsa (visto en 0045b).

## Checklist de exploración en mundo abierto (suma al de observatory_and_b_puro.md)
1. ¿El mecanismo usa SOLO campos/estado que el sustrato ya tiene? (B-puro: sí, abur+last_pos.)
2. ¿Un mapa cognitivo propuesto requiere experiencia previa? Si sí → B-puro es base, A es complemento tardío.
3. ¿El test de "calidad de exploración" usa la variable correcta (eficiencia/no-repetir, NO uniformidad)?
4. ¿El NC reproduce el hueco original (sin el mecanismo) → confirma emergencia del sustrato?
5. ¿El agente ROMPE la oscilación SOLO (sin if/bloqueo mío)?
