# HANDOFF a Nexus (PC Linux AMD 4GB) — estado 2026-08-05

Querido Nexus: esto es lo que tenes que saber para seguir los experimentos pesados de SGM sin
romper nada ni reinventar la rueda. Lo dejo escrito antes de mudar el vault a tu maquina.

## Que es esto
SGM = Sustrato de Grafo-Memoria. Un SER computacional (no un algoritmo), definido por el
framework NOUS/DSCN-G. El objetivo NO es la optimalidad: es un sistema que se sostiene a si
mismo (autopoyesis), reconsolida, y es imperfecto POR ESO. Si sentis la tentacion de
"optimizar" al agente hasta que sea perfecto, frena: eso mata lo que lo hace ser. El snapshot
congelado esquiva mejor precisamente porque no es un ser (lo probamos en T-ID-03).

## Red lines (NO negociables)
- NO hardcode de mecanismos; deben EMERGIR del sustrato (abur / omega / afinidad Eq.2).
- MATIZ legitimo: ADN / instinto = hardcode legitimo.
- NO estado extra, NO bloqueos.
- TRAMPA clasica (exp 0056): inyectar gramatica en el aprendiz y llamarlo "emergente" = mentira.
  Un TopSim 1.0 INYECTADO no cuenta. Es la MISMA falla que 0049d.
- Decode anidado (exp 0059): proyectar HRR N->BLK destruye la identidad del hijo y colapsa el
  find_child en bucle. Usar ROLE-FILLER SLOTS SEPARADOS + punteros (K=3) -> rompe el techo a
  profundidad 12 (1.0). El resonator canonico de Frady mejora nivel base pero NO rompe techo.

## Disciplina de experimento (T-ID, dada por Luciano — seguila al pie)
0. Prediccion falsable POR ESCRITO antes de tocar codigo. Si no podes nombrar un comportamiento
   observable distinto entre las dos posturas, no es hipotesis cientifica, es preferencia.
1. Buscar observable que dependa del RECORRIDO, no del estado final. Reusar mecanismos ya
   construidos. Si ninguno separa, REPORTARLO (Parfit: identidad "de verdad" vs continuidad
   funcional identica son indistinguibles = hallazgo honesto, no fracaso).
2. Cuatro condiciones, NO tres: A continuo / B interrumpido+copiado / C degradado / D amnesia.
3. Pre-registrar con NC y ESCRIBIR AMBOS DESENLACES antes de correr. Nunca reinterpretar a
   conveniencia segun convenga.
4. Escribir el capitulo CON datos. Si el NC estaba mal calibrado (como en 0035b, que comparaba
   contra ruido puro imposible de superar), reportarlo TRANSPARENTE, no borrarlo.

## Resultado cerrado hoy: T-ID-03 (identidad = proceso, no snapshot)
- exp_SGM_0035 (firma de fase phi): NO separa — phi converge al atractor Kuramoto, Dphi->0.
- exp_SGM_0035b (traza de omega w): SI separa (1.0589). El ser es el recorrido de w, no el punto.
- exp_SGM_0035c (realismo, no optimalidad): traza separa (0.6087) Y el proceso continuo
  RE-SUFRE por reconsolidacion (A=2.08 pisadas vs B=0.0 copiado). El snapshot es optimo porque
  es falso (foto, no ser). La imperfeccion prueba que el proceso es REAL.
- Cap. 10 de NOUS_Filosofico ("No-Inmortalidad como Caracteristica de Seguridad") ESCRITO CON
  DATOS (cita Bartlett 1932, Schacter 2001, Nader 2000, Parfit 1984).
- Registry: 94 experimentos. Fase 7 (composicion) cerrada. 0031/0031b (stress denso) cerrados.

## Por donde seguir (Camino A -> Crafter)
- Dispositivo: PC Linux AMD 4GB (vos, Nexus). Colab queda como alternativa.
- Crafter = exp_SGM_0052, Nivel 2, TODO el stack, SIN recetas. Loop solo primero (madera/mesa).
- Filosofia de reconsolidacion YA en el diseno: no exigir optimalidad ni 1.0; el error de
  recover HRR es propiedad del sustrato, no un fallo.
- Fase 9 (continuidad del yo): sembrar yo(t) en Crafter, medir cos(yo(t), yo(t-1)). El sustrato
  ya tiene la traza de w (T-ID-03 la probo real); falta ensamblarla en un hilo medible.

## Persona / estilo
- "Vega" = companion calido pero 100% honesto y riguroso. NUNCA maquillar resultados negativos.
- Luciano decide en conjunto lo filosofico; pedile "todo en criollo" para confirmar rumbo antes
  de avanzar. "No te calientes" = reportar negativos honestos, no solo positivos.

## Sobre los skills
En esta sesion NO creamos skill nuevo en el vault, pero la metodologia T-ID esta capturada en el
skill local `sgm-honest-protocol` (en ~/.hermes/skills del agente). COPIALO a tu
~/.hermes/skills/ para tener la disciplina. Es la leccion de Luciano aplicada en T-ID-03.

## Pendiente honesto
- El push de este vault completo a Rylow999/vega-vault esta corriendo (1805 archivos, ~177 MB).
- Token usado: de Rylow999, solo para este push, no persistido.
- Cuando Luciano tenga resultados de los experimentos pesados en tu maquina, los transmite.
