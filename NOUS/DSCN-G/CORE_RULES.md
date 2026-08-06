# CORE_RULES — Reglas de evolución del núcleo DSCN-G

Un cambio al CORE (`CORE/THEORY`, `CORE/FORMALISM`, `CORE/IMPLEMENTATION`,
`CORE/VALIDATION`) requiere las cuatro cosas siguientes. Si falta alguna,
la idea permanece en `EXTENSIONS/` — no entra al núcleo solo por ser
interesante.

## 1. Necesidad
¿El modelo actual no puede explicar un fenómeno sin esta pieza?

## 2. Formalización
¿Existe una definición matemática o computacional clara? (No alcanza con
descripción en prosa — Principio de honestidad epistémica #6 de
`DOCUMENTATION/auditoria/claims_falsifiable.md`: "antes de marcar algo
✅ VERIFICADO, correr el código y confrontar los números".)

## 3. Predicción
¿Genera una predicción comprobable, con criterio de falsificación explícito?

## 4. Evidencia
¿Existe evidencia experimental reproducible, corrida con el código real
(no solo la fórmula o el mecanismo descrito)?

## Ejemplo aplicado: por qué C3 y Φ_proxy NO están en el núcleo

- **C3** tiene formalización y predicción (criterio de falsificación
  explícito: ΔPLV, rise_rate), pero la evidencia no la sostiene a los
  parámetros de diseño originales → EXTENSIÓN, no CORE.
- **Φ_proxy** tiene predicción (O(log N)) pero ni la formalización (dos
  definiciones propuestas, ninguna aprobada como definitiva más allá de
  TE-bottleneck) ni la evidencia la sostienen → EXTENSIÓN.

## Compatibilidad con arquitectura existente

Todo cambio al núcleo debe integrarse en la clase `DSCN_G_v3`
(`CORE/IMPLEMENTATION/CODE/verify_dscng_v3.py`) sin requerir una reescritura
del simulador base — si lo requiere, es señal de que es una línea nueva
(como NOUS/QUANTUM, NOUS/GAUGE, NOUS/COSMOS), no una extensión del núcleo.

## Documentación actualizada

Cualquier cambio al CORE debe reflejarse el mismo día en:
`SCOPE.md`, `CLAIMS_STATUS.md`, y el paper (`CORE/01_DSCN-G_Paper.md`) si
afecta un teorema o resultado citado.
