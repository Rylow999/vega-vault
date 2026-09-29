# Aplicaciones en HORIZŌN

Cada aplicación de LOGOS o NOUS que inspire el marco merece una nota acá.
No duplico los repos ni los papers; sólo mapeo qué aporta cada una al
marco y en qué estado está su integración.

## Tabla viva

| proyecto | repositorio | qué aporta al marco | estado de la integración |
|----------|-------------|---------------------|--------------------------|
| SDDF / Navier-Stokes | `github.com/Rylow999/sddf` | observable con Fc cerrada, confinamiento con forma analítica | **sólida** — ver `SDDF.md` |
| fhrr-rho-collapse | `github.com/Rylow999/fhrr-rho-collapse` | colocación del operador; colapso y reparación dual | **sólida** — ver §7 del informe |
| DSCN-G | `NOUS/DSCN-G` en este vault | núcleo cognitivo; vitalidad, N_ss*≤4.93 | parcial — test de la predicción pendiente |
| Pandora | `github.com/Rylow999/Pandora` | agente cognitiva residente, observadores anidados forzando colapso controlado | planeado — colapso generativo *controlado*, su caso |
| Quantum v9.1 | `NOUS/Quantum` | decoherencia como colapso | parcial — análoga, no causal |
| Gauge | `NOUS/Gauge` | ley de área, tensión σ | parcial — heredado del sustrato |
| RHO_LAW | `NOUS/RHO_LAW` | patrón trans-dominio del observador | transversal — el marco usa su lenguaje |

## Qué entra y cómo

1. Para integrarse, un proyecto tiene que poder decir **qué es el
observador, qué es la proyección fallida, y qué es el resquicio** dentro de
él. Sin eso, la integración es ornamental.
2. El terreno medio entre "integrado" y "solido" es la intervención
controlada: cambiar una cosa a la vez y demostrar que el resultado cambia
con eso y no con otra cosa (como en fhrr: mismo codebook, cambiar solo
colocación; como en SDDF: mismo espectro, cambiar solo suavizado).
3. Está prohibido usar el marco como validación cruzada sin declararlo:
LP lacuóos y NOUS son orígenes, no argumentos de autoridad.

## Qué sigue

- `SDDF.md` ya está — con el resultado del DNS real y la lección del
detector suavizado.
- Pendientes: `DSCNG.md` con el test de la predicción (E_i umbral vs
método de medida) y `PANDORA/README.md` con el diseño del aparato de
observadores anidados para Pandora.
