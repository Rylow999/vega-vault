# Curiosidad humana — mecanismo y mapeo a SGM (knowledge bank)

Resumen condensado de la charla 2026-08-03 que gui\xc3\xb3 el dise\xc3\xb1o de 0035/0036/0038. NO es
literatura citada del vault; es síntesis de mecanismo humano conocido, usada para no medir humo al
modelar curiosidad en SGM.

## C\xc3\xb3mo funciona la curiosidad humana (mecanismo, medido)
1. **Error de predicci\xc3\xb3n (RPE / dopamina).** El cerebro es m\xc3\xa1quina que predice y odia estar
   equivocada. La dopamina es se\xc3\xb1al de error de predicci\xc3\xb3n (Schultz), no de "placer". Friston:
   minimizar energ\xc3\xada libre / sorpresa. La curiosidad es el motor que gira para reducir la discrepancia
   modelo-mundo. NO necesita t\xc3\xa9rmino externo que fuerce explorar: el error es la fuerza intr\xc3\xadnseca.
2. **Curva U invertida (Berlyne 1954).** La curiosidad no crece lineal con novedad: pico en el medio
   (ni muy sabido=aburrido, ni muy raro=rechazo/angustia). dopamina(eta) debe ser U invertida, NO
   minimizar error ciegamente.
3. **Gap de informaci\xc3\xb3n (Loewenstein 1994).** La curiosidad es la tensi\xc3\xb3n desagradable de saber
   que falta algo, no un anhelo tierno. Es una deuda percibida.
4. **Aburrimiento como homeostato.** No es "no pasa nada": es el sensor de "mi modelo predice todo, no
   hay error, me atrofio". Empuja a buscar novedad para mantener el arousal arriba del piso. Es el
   disparador ACUMULATIVO de la curiosidad sostenida (no el RPE puntual).
5. **Soporte neuro (Kang 2009).** Curiosidad -> n\xc3\xbacleo accumbens (dopamina) + mejor consolidaci\xc3\xb3n
   hippocampal. Aprendemos mejor lo que aprendemos curiosos.

## Qu\xc3\xa9 nos hace curiosos (s\xc3\xadntesis)
No es "deseo noble de conocer": es sistema de recompensa atado a reducir error de predicci\xc3\xb3n.
- forward model que FALLA continuamente,
- la falla se se\xc3\xb1aliza como dopamina/RPE (excitaci\xc3\xb3n o tensi\xc3\xb3n),
- el aburrimiento empuja cuando el modelo es demasiado bueno (error~0),
- buscamos el punto "interesante" (U invertida) donde el error es reducible.

## Mapeo honesto a SGM
- El "bonus de novedad" (0035) es sustrato BAJO: drive programado, no deseo emergente. \xc3\x9apera 35% vs
  greedy 7.5% en maze, pero es un add-on, no "el sistema decide".
- El salto real (0036) es curiosidad COMO CAMPO: eta=1-cos(omega_pred, omega_real) es variable de estado
  hermana de E y dolor; dopamina(eta) en U invertida + aburrimiento acumulado (eta~0 sostenido) + fallback
  novedad bruta. GLOBAL 50% vs BASE 5%. Esto es lo que el user quer\xc3\xada: curiosidad latente del sustrato.
- 0038: balance eta global vs dolor en maze 2D. CUR 45% vs BASE 12.5%; pisos de dolor 0.475 (<0.5: evita,
  no suicida). Home bias del riesgo: dolor CONOCIDO pesa menos. La curiosidad es global PERO se modula.

## Lo que el modelo NO captura (dejar apuntado, no prometer)
- QUALIA de "interesarse": se mide el operador (eta->dopa->explora), no la vivencia. Problema del otro cuerpo.
- Asimetr\xc3\xada dolor/curiosidad: el humano tolera m\xc3\xa1s dolor POR curiosidad que por placer neutro.
  El eta deber\xc3\xada AMORTIGUAR el delta_dolor en alta novedad (no solo sumarse). NO implementado (candidato 0039).
- Dolor IMPREDICTO paraliza m\xc3\xa1s que el conocido; a veces el humano BUSCA dolor leve por control
  (deporte/estudio) -> el dolor se vuelve dopamina. No implementado.
- Curiosidad SOCIAL: nos volvemos curiosos por lo que OTROS exploran. SGM es de un agente; frontera futura.

## Reglas de dise\xc3\xb1o extra\xc3\xaddas por esta charla (ya en SKILL.md ANTI-PAPER-VISION 6-9)
- La se\xc3\xb1al derivada (eta/E_root) debe VARIAR entre casos; la norma de proyecci\xc3\xb3n HDC normalizada
  es constante (1.0) -> no discrimina (lecci\xc3\xb3n 0019). Usar intensidad de se\xc3\xb1al cruda.
- Campo global, no m\xc3\xb3dulo add-on: si eta vive solo en el maze, la curiosidad es local/falsa.
