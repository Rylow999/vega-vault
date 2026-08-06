# Discrete Dynamics

## Estado: CON CONTENIDO PARCIAL (actualizado 2026-07-25, Vega + Luciano)

Este directorio era placeholder vacío. El 2026-07-25 se documentó la relación
real con DSCN-G Core vía la **Tríada de autorregulación disipativa** (ver
/sdcard/Hermes/nexus-vault/TRIADA_AUTORREGULACION/).

## Relación formalizada con DSCN-G (Tríada)

DSCN-G es el dominio COGNITIVO de una arquitectura común de 3 capas:
- Dinámica A: fase φ_i (acoplamiento Kuramoto, Eq. del paper core)
- Dinámica B: vector ω_i (actividad de membrana / peso sináptico)
- 3ra dinámica (reguladora): Vitalidad V_i (Ecs. 5–6, poda homeostática)

La vitalidad V_i es la cantidad que autorregula la competencia fase↔vector,
manteniendo el grafo confinado a N_ss*≤~5 (T1 verificado, Ronda 6). Esto es
el análogo cognitivo del "Tercer Motor" de Navier-Stokes (curvatura espectral G)
y del balance f_P de Collatz. Los tres son confinamiento disipativo del MISMO
tipo estructural, aunque con constantes distintas (ver tests A/B/C/M en TRIADA).

## Qué está probado (nuevo, 2026-07-25)

- DSCN-G CALIFICA en el criterio operacional de la Tríada (Punto 2 del amigo):
  C1 (fase/vector compiten), C2 (V_i acotada por poda), C3 (la cota sale de la
  ESTRUCTURA de poda, no de variable externa). Es decir, no es "sistema estable
  genérico" —es disipación estructural específica.
- La relación con DDSD/Collatz/NS/Riemann está documentada en TRIADA_Autorregulacion_Disipativa.md
  (sección 1, fila DSCN-G: CONFIRMADO). NO es unificación de constantes; es
  unificación de PRINCIPIO (disipación que confina).

## Qué sigue pendiente

- Bajar la Tríada de "marco de principios" a predicción cuantitativa cruzada
  entre DSCN-G y los otros dominios (Punto 4 del amigo: aún NEGATIVO, los bounds
  son independientes). No hay fórmula que derive N_ss* de DSCN-G desde f_P* de
  Collatz o G* de NS.
- El Φ_proxy O(log N) sigue retirado (Ronda 6); el "Φ" real de DSCN-G es V_i,
  no el proxy de información integrada.

## No integrar al CORE sin formalización propia adicional
La Tríada es un MARCO comparativo, no parte del núcleo congelado v1.0.
Mantener fuera del CORE hasta que haya predicción cuantitativa cruzada sostenida.
