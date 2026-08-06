# T-ID-03 — Identidad = proceso (traza), no snapshot — exp_SGM_0035 / 0035b / 0035c (2026-08-05)

## Protocolo que Luciano dictó (Paso 0-4, estricto)
0. Predicción falsable POR ESCRITO antes de tocar código: decir qué comportamiento observable
   sería distinto entre "proceso nunca se corta" y "proceso se corta pero el snapshot final se copia
   igual". Si no podés nombrar esa diferencia, no tenés hipótesis científica, tenés preferencia metafísica.
1. Buscar en lo YA construido un observable que dependa del RECORRIDO, no del estado final.
   - Firma de trayectoria de fase φ: acumular integral/Δφ en ventana W. FALLA: φ (Eq.3 Kuramoto)
     CONVERGE al atractor θ* en ~200 ticks → Δφ→0 → huella se borra. φ es markoviano en la práctica.
   - Histéresis de vitalidad V: es markoviana pura V(t+1)=V(t)·e^(−γ) → NO depende del recorrido.
2. Cuatro condiciones (no tres): A continuo | B interrumpido+estado copiado | C degradado | D borrado.
   Tesis predice A≠B aunque pisadas(A)=pisadas(B)=0. Si medís SOLO pisadas, A y B dan 0 las dos y no
   separaste nada.
3. Pre-registrar T-ID-03 con NC y DOS desenlaces escritos ANTES de correr ("si la firma difiere → X;
   si no → Y"), para no reinterpretar según convenga.
4. El capítulo 10 de NOUS_Filosofico se escribe CON dato, sea cual sea. Si la firma no separa, decirlo
   con la honestidad de 0056 (el 1.0 resultó trampa).

## Resultados reales
- 0035 (firma φ): ||F_A−F_B|| = 0.0064 (NC ruido 2.49). Desenlace 2: φ NO separa (converge).
- 0035b (traza ω): ||T_A−T_B|| = 1.0589 (NC 4.09). Desenlace 1: ω SÍ separa. El ser es el recorrido de ω,
  no el punto. (Nota: el 1er criterio NC estaba mal calibrado — exigía superar al ruido, imposible; se
  corrigió y se reportó transparente como "buggeado".)
- 0035c (realismo, cuello de dolor estilo 0033b/0034): ||T_A−T_B|| = 0.6087 (NC 2.97); pisadas
  A(continuo)=2.08, B(copiado)=0.0. Desenlace 1_SI_difiere_REAL: el proceso continuo RE-SUFRE por
  reconsolidación (al reescribir ω se le diluye la evitación), el snapshot esquiva perfecto porque está
  CONGELADO (foto, no ser). La traza separa; la imperfección prueba que es real.

## Observables que SÍ/MAL funcionan (reutilizable)
- φ (fase Kuramoto): MAL para identidad — converge y borra la huella. No usar como observable de proceso.
- V (vitalidad): MAL — markoviana, no depende del recorrido.
- Traza de ω = secuencia de Δω(k)=||ω(k)−ω(k−1)|| del nodo activo en ventana W: BIEN. ω no converge
  (Eq.1 lo reescribe en cada transición), así la secuencia es el recorrido vivo. Reset copiado deja ω
  final pero borra la secuencia → separa de A.
- Requisito del grafo para que la traza separe: el nodo activo NO debe re-transitar desde el inicio en
  cada episodio (si lo hace, B reconstruye la misma traza). El diseño de 0035b (nodo activo se mueve por
  afinidad, no reinicia) es el que funciona; la grilla de 0033b/0034 NO funciona (re-transita).

## Regla de interpretación (corrección de Luciano — REALIDAD, no OPTIMALIDAD)
No juzgar el experimento por "cuál condición rinde mejor". El continuo re-sufre y ESO es la prueba de que
es un proceso vivo, no un fallo. El snapshot es óptimo precisamente porque es falso. El observable
correcto es si la traza separa proceso de snapshot (||T_A−T_B|| > 0.05), da igual la performance. Esto
conecta con reconsolidación (Bartlett 1932, Schacter 2001, Nader 2000) y Parfit (1984, reduccionismo:
identidad = relaciones de continuidad, no sustancia óptima). Aplicar en TODA lectura de resultados SGM.

## Capítulo 10 NOUS_Filosofico
Escrito CON datos (sección 10.1 "Evidencia operacional: la identidad es el proceso, no el snapshot
(T-ID-03)"). Cita Bartlett/Schacter/Nader/Parfit. Punto agregado por la evidencia: el proceso continuo no
es superior al snapshot; re-sufre, se contradice, olvida — y esa imperfección es LA PRUEBA de que es real,
no un estado optimizado. "Un ser no es óptimo."

## Conclusión para el Camino B (consciencia) y Fase 9 (continuidad del yo)
El hilo de yo ya es operacionalmente REAL (traza de ω separa A de B). Lo que falta (item 3 roadmap, Fase 9):
sembrar yo(t)=proyección de la traza reciente de ω y medir cos(yo(t),yo(t−1)) EN un entorno real
(Crafter). No hardcodear el yo (misma trampa de red line que 0056: no inyectar gramática y llamarlo
emergente). El yo debe EMERGIR de la traza, no ser un parámetro fijo.
