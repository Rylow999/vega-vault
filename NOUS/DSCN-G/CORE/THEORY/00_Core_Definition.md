# DSCN-G — Definición Conceptual

**DSCN-G = Dual-State Cognitive Geometry.** Nombre canónico único a partir de este
documento — reemplaza expansiones previas del acrónimo usadas en borradores anteriores
del proyecto ("Dynamic Substrate Computational Network – Grounded", "Dynamic
Self-Coordinating Neural Geometry").

Este documento es una **portada conceptual**, en lenguaje llano, sobre el núcleo ya
formalizado y auditado. No es una versión nueva ni reemplaza nada: el modelo con
teoremas, verificación computacional y programa de ablaciones es
[`01_DSCN-G_Paper.md`](../01_DSCN-G_Paper.md) (DSCN-G v3, auditado en 6 rondas,
2026-07-22/24). Léase ese documento para cualquier cifra, criterio de verificación o
afirmación técnica precisa; este archivo es solo el mapa de entrada.

---

# 1. ¿Qué es DSCN-G?

DSCN-G es un marco teórico que propone que los sistemas cognitivos pueden entenderse
como sistemas dinámicos autoorganizados capaces de:

- mantener estabilidad interna,
- coordinar múltiples procesos,
- adaptarse a cambios,
- reorganizar su dinámica según las demandas del entorno.

El núcleo de DSCN-G no depende de una representación fija de información, sino de la
interacción dinámica entre estados internos, regulación y coordinación temporal.

---

# 2. Principios fundamentales

## Principio 1: Regulación dinámica

Los sistemas cognitivos requieren mecanismos internos que mantengan su funcionamiento
dentro de rangos estables (homeostasis computacional). En el núcleo auditado esto se
implementa como poda por vitalidad (Ecs. 5–6 del paper).

## Principio 2: Coordinación temporal

Los procesos distribuidos requieren mecanismos de sincronización para producir
comportamiento coherente. En el núcleo auditado esto se implementa como acoplamiento de
fase Kuramoto (Ecs. 3–4 del paper).

## Principio 3: Recursos cognitivos dinámicos

La memoria y la atención se modelan como recursos variables, no como slots fijos.
Evaluado en el paper mediante la tarea N-back grounded (Sección 4).

## Principio 4: Aprendizaje adaptativo

Los sistemas cognitivos modifican su comportamiento mediante experiencia y error. En el
núcleo auditado esto se implementa como TD-learning sobre un vector semántico (Ec. 1).

*(Se alinea aquí con los cuatro principios de `02_Design_Notes/`, no con una versión
anterior de tres.)*

---

# 3. Arquitectura mínima

## Componentes

- **Regulación interna** — mantiene estabilidad dinámica.
- **Sistema de coordinación temporal** — sincronización entre procesos.
- **Memoria dinámica** — conserva información relevante, modifica estados futuros.
- **Mecanismo adaptativo** — cambios internos derivados de experiencia o perturbaciones.

La correspondencia exacta entre estos componentes y las ecuaciones formales (TD-learning,
Kuramoto, vitalidad/poda) está en `../01_DSCN-G_Paper.md`, Sección 2.

---

# 4. Evidencia experimental

## Tarea N-back

Objetivo: evaluar si la arquitectura mantiene y utiliza estados dinámicos durante tareas
con demanda de memoria de trabajo, comparado contra baselines recurrentes.

Resultados, cifras y metodología (versión occurrence-aware, v6, la única con números
válidos): `../01_DSCN-G_Paper.md`, Sección 4.

---

# 5. Elementos que permanecen como investigación abierta

No forman parte del núcleo hasta demostrar necesidad experimental o teórica.

## C3 — Sincronización patológica ("Phase Hijacking")

**Estado:** hipótesis experimental, probada explícitamente y **no sostenida** a los
parámetros de diseño originales (0.9% de los eventos de disparo muestra el efecto
reclamado; ΔPLV≈−0.007, no el −0.46 de borradores previos). Ver `../01_DSCN-G_Paper.md`
§3.4 y `../../DOCUMENTATION/03_Estado_Auditoria/ANALISIS_ESTADO_2026-07-24.md` §2–3 para el detalle y las
decisiones pendientes sobre su rediseño.

C3 debe considerarse un posible comportamiento emergente o una condición de
fallo/transición del sistema — no es necesario para definir el núcleo DSCN-G.

## Propiedades emergentes adicionales (sin numeración de teorema propia)

Existen hipótesis relacionadas con propiedades emergentes del sistema dinámico que
todavía no tienen formulación formal completa, demostración o predicciones verificables.
Deben permanecer separadas del núcleo hasta contar con eso.

*(Nota: el Teorema 3 del paper auditado — consenso de fase — **sí** está formalizado y
verificado computacionalmente; no confundir con las hipótesis emergentes sin numerar de
este apartado.)*

---

# 6. Relación con FATE

FATE es una aplicación del marco DSCN-G: usa DSCN-G como fundamento arquitectónico en su
implementación (dependencia real en el código, no solo conceptual).

```
DSCN-G
 |-- Marco teórico dinámico
 |-- Principios fundamentales
 |
 FATE
 |-- Aplicación computacional
 |-- Motor de optimización basado en DSCN-G
 |-- Sistema experimental/aplicado
```

DSCN-G no existe para justificar FATE. FATE utiliza DSCN-G como fundamento.

---

# 7. Criterio para agregar nuevas ideas al núcleo

Una nueva hipótesis solo se incorpora si cumple:

- **Necesidad** — ¿el modelo actual no puede explicar un fenómeno sin esta pieza?
- **Formalización** — ¿existe una definición matemática o computacional clara?
- **Predicción** — ¿genera una predicción comprobable?
- **Evidencia** — ¿existe evidencia experimental reproducible?

Si no cumple estos puntos, permanece como extensión experimental.

---

# 8. Objetivo posterior a este núcleo

1. Consolidar el núcleo (hecho: `../01_DSCN-G_Paper.md`, 6 rondas de auditoría).
2. Validar experimentalmente más allá de simulación (EEG/fMRI — pendiente).
3. Aplicar DSCN-G en sistemas concretos (FATE).
4. Evaluar nuevas extensiones individualmente (C3, propiedades emergentes).

---

# Definición corta

DSCN-G (Dual-State Cognitive Geometry) es un marco teórico para estudiar sistemas
cognitivos como procesos dinámicos autoorganizados capaces de regularse, coordinarse y
adaptarse. El núcleo formal está verificado computacionalmente en `../01_DSCN-G_Paper.md`
(v3). FATE es una aplicación construida sobre este marco. C3 y otras hipótesis
emergentes permanecen como líneas de investigación independientes hasta demostrar su
necesidad.
