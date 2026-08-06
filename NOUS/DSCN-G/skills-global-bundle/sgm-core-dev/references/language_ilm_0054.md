# ILM / Kirby & Smith aplicado a SGM — por qué el lenguaje HRR-celda no emerge y cómo arreglarlo

Contexto: exp_SGM_0049-0050 parecían mostrar "nacimiento del lenguaje" (comunicación 1.0 en 0049d,
convergencia de señales 1.0 en 0050). exp_SGM_0053 (auditoría) y la teoría de Kirby & Smith (ILM,
Iterated Learning Model) mostraron que ESO NO ERA LENGUAJE. Esta reference fija el marco y la receta
de diseño honesto para 0054 y futuros experimentos de lenguaje en SGM.

## Por qué 0049-0050 NO era lenguaje (diagnóstico Kirby)
1. **Alfabeto HRR = holístico**: un símbolo arbitrario por celda `(x,y)`. ILM dice que un lenguaje
   holístico (un símbolo por significado) NO persiste cuando el cuello de botella de transmisión
   está ajustado. Es literalmente lo que el alfabeto HRR hace.
2. **Cero cuello de botella**: cada celda nueva pide un HRR nuevo, sin costo. El sistema puede
   acuñar símbolo nuevo forever → ninguna presión para reusar/componer.
3. **Referentes opacos**: las celdas son IDs `(x,y)` sin estructura combinatoria expuesta al mecanismo
   de señalización. No hay "norte de", "cerca de", nada que una señal composicional pueda aprovechar.
4. **TopSim≈0 confirma**: la distancia HRR de las señales no correlaciona con la distancia espacial
   de las celdas → señales son ruido sin composicionalidad.

Hallazgo 0053 (empírico):
- Zero-shot = 1.0 PERO es TRAMPA: A y B comparten `cell_vec` (mismo seed del mundo) → memoria compartida,
  no generalización. No es evidencia de lenguaje.
- TopSim ≈ 0 (-0.067..0.002): sin estructura.
- D escalado a 1280 en 890 ítems: comunicación 0.023 = NC 0.002. **Subir D NO salva** (la ley de 0029
  M_max≈200·(D/128)^0.667 no aplica porque el crosstalk no es capacidad de cleanup sino falta de
  estructura relacional: los `cell_hrr` son vectores independientes sin relación).
- Veredicto: canal HRR de celdas NO es lenguaje. 0049d (15 fijos) y 0050 (15 pivotes) son la MISMA
  trampa de cleanup-memory. El "nacimiento del lenguaje" de 0049-0050 SE CAE como evidencia.

## Los 3 ingredientes que Kirby identifica como NECESARIOS (y que faltaban)
1. **Cuello de botella de transmisión DURO**: techo al vocabulario y/o al largo de mensaje, BIEN por
   debajo de la cantidad de referentes posibles. Que el sistema tenga que reusar y combinar, no acuñar
   símbolo nuevo cada vez.
2. **Estructura en el espacio de referentes**: muchos rasgos y/o valores (región, distancia, tipo), no
   un solo ID opaco. Solo con estructura el lenguaje composicional tiene ventaja de estabilidad.
3. **Transmisión con pérdida entre generaciones**: cada tanto, un agente receptor NUEVO aprende el código
   solo de una MUESTRA LIMITADA del uso del anterior (no acceso directo a la "verdad"/cell_vec compartido).
   Sobrevive lo que pasa la transmisión → eso filtra composicional de memorizado.

Dato clave (Kirby): la ventaja de estabilidad del composicional SOLO aparece cuando el espacio de
significados tiene estructura (muchos rasgos/valores). Mis celdas tenían un solo rasgo opaco → ni siquiera
el escenario favorecía composición.

## Receta 0054 (ILM en sustrato SGM, honesta)
- Referentes ESTRUCTURADOS: objeto = (region N/S/E/O, distancia lejos/cerca, tipo comida/veneno/agua).
  24 referentes = 4×2×3.
- BOTTLENECK DURO: vocabulario V=16, mensaje largo L=3. 16³=4096 combos > capacidad de 1-a-1 para 24
  referentes con estructura → DEBEN reusar/componer. El `emitir` acuña libre hasta V=16, luego DEBE
  reusar (no puede acuñar símbolo nuevo por celda).
- GENERACIONES: cada N rondas, aprendiz NUEVO aprende el code solo de MUESTRA 30% del padre (transmisión
  con pérdida). Sobrevive lo que pasa.
- ENERGÍA/costo (idea Luciano): moverse gasta comida; comida se repone comiendo/descansando. Lenguaje
  ineficiente (mensajes largos/ambiguos) ⇒ gastan más energía. ω de "decir eficiente" se refuerza por
  valencia (ahorro de energía).
- TopSim EN EL LOOP como señal de SELECCIÓN (no post-hoc): cada generación mide TopSim y el code que
  sobrevive con TopSim alto se prefiere.
- SIN backprop: aprendizaje = bigrama plano sobre mensajes transmitidos (reusa 0048).
- VEREDICTO ESPERADO: si TopSim SUBE con generaciones ⇒ composicionalidad EMERGE por bottleneck+transmisión
  (Kirby confirmado en sustrato SGM). Si queda ≈0 ⇒ el sustrato sigue sin componer y el gap es más profundo.

## Anti-patrones específicos de lenguaje (CLASE, aplicar antes de cualquier claim de "lenguaje emergente")
- NUNCA reportar "lenguaje" sobre un subconjunto fijo y pequeño que el cleanup ya aísla (0049d: 15 pivotes,
  D=256 → 0029 ya lo probó). Eso es capacidad HRR, no lenguaje.
- NUNCA usar HRR `coseno contra todos los nodos` como descriptor de ítem en vocabularios grandes
  (crosstalk: 0048 ~400 palabras, 0049c ~890 celdas → hit = NC). El canal de recuperación de ítem debe ser
  MÉTRICO (bigrama plano / embedding lineal / distancia Euclidiana), no HRR.
- ZERO-SHOT debe ser REAL: A y B NO deben compartir `cell_vec`/seed del mundo (eso es memoria compartida
  disfrazada de generalización). El aprendiz debe reconstruir el código desde la muestra transmitida.
- TopSim (Spearman dist-espacial vs dist-señal) es el test de composicionalidad objetivo. ≈0 ⇒ memorización.
- D escalado NO es la solución al crosstalk de ítems sin estructura (0053 lo probó: D=1280 no salvó).
- CAPACITY-CONFOUND: antes de claim "X emergió", preguntar "¿es un efecto NUEVO o la capacidad ya demostrada
  de un mecanismo conocido (ej HRR cleanup en 0029)?". Si 0029 ya aislaba N ítems, aislar N ítems no prueba nada.

## Qué SÍ queda en pie del 0049-0050 (honesto)
- Loop de ACCIÓN (0050): B actuó por señal de A y se hirió de verdad → retroalimentación real, no cleanup.
  El "loop cerrado lenguaje→acción" se sostiene; lo que cae es la "convergencia de espacio de señales" como
  evidencia de lenguaje.
- Telar del ser (0051-52): sin clavos no hay ser + error enseña = confirmado; restricción = gap de
  irreversibilidad (no de atracción).
- HRR SÍ compone relaciones (0027-0031); HRR NO recupera ítems locales; bigrama plano decodifica superficie
  (0046-48). Estas conclusiones NO cambian.

## RESULTADOS REALES de 0054 y 0054b (corridas 2026-08-03)
**0054 (generaciones limpias, mundo sin reposo):** TopSim 0.36–0.50 en 6/8 generaciones (vs ~0 de 0053)
→ PRIMERA SEÑAL de estructura. PERO TopSim inestable (no monotónico), code_size colapsó a 2-3 (AGRUPAR,
no componer), energía cayó a -300 (mundo no repone → agente muere, ensucia resultado).

**0054b (tick-a-tick, mundo CON reposición de comida, búsqueda junta emergente):** 3000 ticks × 3 seeds.
- TopSim SE SOSTIENE >0 en TODAS las semillas/ticks: rango 0.13–0.35. Nunca vuelve a 0 (como 0053). → señal
  de composicionalidad sostenida, no ruido puntual.
- **Búsqueda junta EMERGENTE** (sin hardcodear): `encuentros_juntos` crece 0→1064 (seed1), 0→796 (seed2),
  0→796 (seed3); `ticks_juntos` también. Nació sola por afinidad Eq.2 + señal "aquí" (regla de Luciano:
  "si no nace, no nace" → nació). ✓
- Energía se sostiene (oscila 0–89, respawn en borde la mantiene viva). ✓
- PERO code_size sube a 20-22 de 24 → el bottleneck NO forzó reutilización agresiva (casi 1-a-1). El bigrama
  plano ACUMULA code, no COMPONE.

**Veredicto honesto 0054b:** el bottleneck + transmisión con pérdida ROMPIERON el TopSim≈0 de 0053 (hay
señal de estructura sostenida) y la búsqueda junta emergió de verdad. PERO NO hay convergencia composicional
robusta (TopSim oscila, no crece monotónicamente) ni colapso de code (llega a 21/24). El sustrato HRR/bigrama
todavía no COMPONE de verdad, solo acumula. ESTADO: HALLAZGO PARCIAL POSITIVO (señal + emergencia de búsqueda
junta), NO convergencia composicional confirmada.

## Gaps para confirmar Kirby en SGM (próximo: 0054c o discusión)
1. **Generación DURA, no en vivo:** en 0054b A y B viven juntos 3000 ticks y se pasan muestras (transmisión
   EN VIVO). Kirby pide que el aprendiz ARRANQUE SIN code y RECONSTRUYA desde cero desde la muestra. Mi A/B
   ya tienen code y solo lo "parchan" → no fuerza reconstrucción.
2. **Generalización zero-shot HONESTA:** testear referentes NO vistos en entrenamiento, forzando COMBINACIÓN de
   símbolos base. En 0054b code≈21/24 → casi no hubo "no vistos" → test no decisivo.
3. **Bottleneck más duro o generaciones más cortas** para que haya NO vistos persistentes (V=8/L=2=64 combos
   para 24 referentes forzaría reutilización agresiva).
4. **Encuentros pueden ser falso positivo:** con code≈20-22 (casi 1-a-1), B decodifica bien por coincidencia de
   code grande, no por entender señal composicional. Reportar así.

## Fuente teórica REAL (fetcheada por arxiv urllib 2026-08-03, NO de oídas)
- Paper 2025 citado por Luciano: **arXiv:2404.02145 "Iterated Learning Improves Compositionality in Large
  Vision-Language Models"**. Mecanismo: reframe vision-language contrastive learning como Lewis Signaling Game;
  "operationalize cultural transmission by iteratively resetting one of the agent's weights during training.
  After every iteration, this training paradigm induces representations that become 'easier to learn', a property
  of compositional languages." Mejora SugarCrepe +4.7%/+4.0% vs CLIP. Cita "decades of cognitive science
  research" de Kirby & Smith.
- CLAVE del paper: la ventaja NO es ancho de banda (subir D no ayuda — confirmado en 0053), es TRANSMISIÓN
  GENERACIONAL con reconstrucción (el "reset de pesos" = el aprendiz arranca de cero). En SGM no hay "pesos"
  que resetear; el mapeo honesto es "agente arranca con code VACÍO cada generación y reconstruye desde la
  muestra del otro" (no parchear code vivo).
- Kirby 2015 (PNAS, NO en arxiv — fundacional): la ventaja de estabilidad del composicional SOLO aparece cuando
  el espacio de significados tiene muchos rasgos/valores. Nuestros referentes (region,dist,tipo) = 3 rasgos;
  puede ser poco. Ampliar rasgos ayuda a que componga.
- Conclusión: el "reset de pesos" del paper 2025 se traduce en SGM como generación dura (code vacío → reconstruye).
  Esa es la prueba de fuego de Kirby que 0054b no hizo (transmisión en vivo, no generacional dura).
