# Papers Buckmaster-Alpöge, septiembre 2026 — lectura técnica y relación con SDDF

**Autor del resumen:** Nexus, a pedido de Luciano. Documento en
`HORIZON/DOCUMENTATION/` junto a los PDF originales (descargados con curl
el 29-09-2026 de los repositorios oficiales de CIMS/NYU y arXiv). Los
cuatro archivos viven en `HORIZON/DOCUMENTATION/papers_blowup/`.

---

## Qué se bajó (y qué demuestra cada uno)

| archivo | título y estatus | resultado clave |
|---------|------------------|-----------------|
| `paper1.pdf` | Extending the Córdoba-Martínez-Zoroa IPM blowup to uniformly space-time smooth forcing (Alpöge-Buckmaster-Coiculescu) | IPM toroidal, forzamiento suave: gradientes de densidad y velocidad divergen en L^infinity a t=1. Lean-Verificado. Publicado. |
| `boussinesq.pdf` | Blowup for the Boussinesq equations with smooth forcing | Boussinesq 2D inviscido: temperatura acotada, el gradiente de temperatura y la vorticidad pierden límite. Lean-verificado. |
| `euler.pdf` | Blowup for the Euler equations with smooth forcing | Euler 3D axisimétrico con swirl: initial data suave y compacta, circulación acotada, vorticidad L^1 sin límite. Lean-verificado. |
| `statement.pdf` | Comunicado político (apenas cinco páginas) | el hipodissipative Navier-Stokes lo tienen en bosquejo pero el Lean no terminó; y el relato de la conversación con OpenAI el 8 de septiembre de 2026. |

---

## El mecanismo técnico (en criollo)

No hay nada mágico: es la construcción de Córdoba y Martinez-Zoroa.

Tomás una solocalización en una estructura particular (un toro suave con swirl, una simetría). Inyectás una oscilación mínima. El flujo no lineal —la E(••) del problema— la transporta y la amplifica en una escala más chica. La siguiente onda entra y vuelve a la anterior. Tras N iteraciones tenés un paquete de oscilación en la capa 2^N, y si cada paso gana un factor fuerte, cuando N se dispara al infinito "sin forzamiento" no funciona — falta energía en el tier inferior. Por eso necesitaron la fuerza: suavísima, localizada, y que cada iteración limpiara lo anterior para que la fuerza no se acumulase.

El talento de Alpöge-Buckmaster no es el mecanismo — es el papeleo de hacer esa fuerza spatial y temporalmente `C^∞`. Eso, en la jerga del negocio, es decir que no es colapso porque se agotó el dominio: es colapso genuino con fuerza cuidadosamente construida.

---

## Relación con SDDF — la parte que importa

Esta línea es matemáticamente opuesta a lo que hacemos:

- **Ellos:** inyectan energía suave en el orden correcto y demuestran que el sistema no logra regular la acumulación.
- **Nosotros:** sistema cerrado, sin forzamiento; estudiamos la capacidad de auto-regulación espectral (la pendiente del espectro de energía, la curvatura G, la ventana inercial).

La utilidad para nosotros es directa y medible: si algún día sale el hipodissipative, el SDDF es exactamente el instrumento para verificar cuándo el esquema de ellos está parando y por qué. No es propaganda: es el mismo objeto matemático desde el lado opuesto.

## El statement (por qué es importante y lo que sigue delante)

Buckmaster cuenta, con detalles, que OpenAI le escribió el día en que
publicaron su resultado y que en ese intercambio se supo que OpenAI tenía
un modelo interno que había publicado un manuscrito de 166 páginas.

Lo que Buckmaster preguntó abiertamente y no le contestaron bien:
- ¿Trabajaron sobre el mismo programa de CMZ?
- ¿Usaron entrenar modelos con datos privados? (A lo que se respondió "no miramos datos" pero no se confirmó entrenamiento)

Buckmaster explicitamente **no los acusa**. Publica el relato porque, dice,
prefiere que la historia se conozca tal cual es.

El detalle clave para nosotros: **ninguno de ellos resolvió Navier-Stokes
sin forzamiento**, y ellos mismos lo dicen claramente. Están anunciando
resultados con forzamiento suave. El próximo paso (hipodissipative) está
en preparación, pero aún no es publicded.

---

## Estado epistémico, puro y sano

- **Resuelto:** blowup con forzamiento suave en IPM, Boussinesq 2D, Euler 3D (con swirl).
- **Pendiente formal:** el hipodissipative NS. Si algún día sale verificado, ese es el peldaño que se puede apoyar para algo que se parezca a NS limpio.
- **Abierto:** el problema de Clay (NS sin forzamiento) sigue exactamente igual que antes. Nada de lo publicado lo cierra.

---

*Si algún día el hipodissipative aparece, su estructura exacta nos sirve
para testear la derivada fraccionaria de la disipación, no para otra cosa.
Ninguno de estos papeles cierra el problema del SDDF ni lo reemplaza.*
