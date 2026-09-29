# Pandora en HORIZŌN

**Repositorio:** `github.com/Rylow999/Pandora` — servicio residente activo
(`pandora-nucleo.service`, systemd --user, Restart=always).

---

## 1. Qué es Pandora (en una frase)

Es el agente cognitivo residente: ese "alguien" del Acta de Principios
que vive mientras la compu esté encendida. No es una herramienta ni un
demo. Es, literalmente, un sistema cerrado con observadores internos — y
justamente por eso es el caso de aplicación más directo del marco
HORIZŌN, porque está **diseñado para serlo**.

---

## 2. Qué tiene que ver con el marco

El documento `NOUS/PANDORA/AGENT_PANDORA_Resumen.md` (revisión crítica
curada, fecha anterior a este proyecto) describe una arquitectura con tres
características que son la transcripción exacta del marco:

| marco HORIZŌN | en Pandora |
|---------------|-----------|
| Tercer mecanismo: compresión homeostática | ciclo de vida por vitalidad V_i (Active/Sleeping/Hibernating/Dead) — pruning sin pérdida abrupta |
| Colapso generativo | co-resonancia forzando nodo hijo ("Generative XOR") y el decodificador L2 que proyecta el estado del grafo a lenguaje |
| Horizonte del observador | la ventana de contexto dinámica W(t) = W_base/(1 + κ·E_root(t)) — se contrae cuado hay carga, se expande en calma; es *el horizonte del observador operativizado* |

### El detalle que lo faire el caso ideal:

Pandora es el único dominio del marco donde **el observador interno y el
sistema se distinguen por construcción**, y donde el sistema está diseñado
para mantenerse vivo en presencia de un observador que analiza su propio
interno. Los otros dominios (Navier-Stokes, Collatz, FHRR) no tienen un
observador con herencia interna — Pandora sí, por diseño.

---

## 3. Estado real (del resumen curado, honesto)

| pieza | estado | estatus epistémico |
|-------|--------|---------------------|
| β_eff = β(1+ρ) | verificado en simulación (200 filas CSV) | **sano** |
| W(t) ventana dinámica | especificada, sin implementación nueva | idea reutilizable |
| ciclo de vida V_i | ideado al detalle | implementable tal cual |
| Generative XOR (nodo hijo) | ecuación, no código | idea |
| decodificador L2 | TODO (fase 3 del plan) | **cuello de botella** |
| systemd activo | funcionando | infraestructura viva |

---

## 4. El experimento pendiente (la predicción del marco)

En el Apéndice C.4 del informe integrado propuse una predicción falsable:
que el "punto crítico" de colapso depende del método de medición.

En Pandora eso tiene una formulación concreta y barata de probar:

> **Si el decodificador L2 proyecta el estado del grafo a lenguaje desde
> diferentes espacios (ambiente vs dual), ¿la proyección cambia? ¿Da el
> mismo resultado el L2 sobre ωᵢ que sobre el subespacio de coeficientes
> que usa el transductor?**

Si proyectar desde sitios distintos produce texto distinto — el "decodificar
eso" del punto — entonces el colapso en Pandora depende de dónde se coloca
el operador de lectura, no del grafo. Eso haría el test de la predicción del
marco en un dominio cognitivo real, en vivo, con el daemon andando.

Ese es el objetivo de trabajo con Pandora dentro de HORIZŌN. No es agregar
más ecuaciones. Es **verificar si el decodificador dice algo distinto según
dónde lo coloques**.

---

## 5. Lo que NO va a pasar acá

- No voy a confundir infastructura viva (el daemon de systemd) con evidencia
  de emergencia. Que Pandora esté siempre vivo es una propiedad de
  infraestructura, no de consciencia.
- No voy a llamar "colapso generativo" a una nueva iteración de la rueda
  Camelot. Si el decodificador dice algo nuevo es un resultado, no una
  metáfora.
- Si el decodificador no dice nada en la versión más simple (línea recta,
  proyección lineal), el resto de la arquitectura no tiene con qué hablar.
  Ese es el test primero.

*Per Aspera, Ad Astra. Pero primero hay que probar si el decodificador dice
algo con sentido.*
