# v0.25 — Harness de Integración (ciclo de 12 pasos, NOUS Técnico v4 Sec.7)

PRIMER intento de UNIR los bloques validados (polisemia/fractal v0.21 v8, root
DIRECTOR v0.22 v3, memoria de trabajo/vitalidad v0.24, dolor v0.19) en UN ciclo
cerrado sobre una tarea que exige COMPOSICIÓN de bloques.

## Dónde leer la teoría (NOUS Técnico v4)
- Vault: `NOUS/DSCN-G/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md` (copiar a home con
  `su -c cp ...` + `chown u0_a471` para leerlo; search_files NO atraviesa /sdcard).
- Secciones clave para integración:
  - Sec.6 "Cuatro Capas de NOUS" (Ring-0 kernel D=4 / Ring-1 Daemon D=384 /
    Ring-2 LLM adapter / Ring-3 I/O). El Daemon (Ring-1) es el sistema cognitivo;
    Ring-2/3 son adaptadores de I/O, NO el núcleo.
  - Sec.7 "Ciclo Cognitivo de 12 Pasos" — el backbone del harness:
    1 Percepción→embedding · 2 Activación (K cadenas por afinidad, Ec.2) ·
    3 Update ω (TD, Ec.1) · 4 Update φ (Kuramoto, Ec.3) · 5 Vitalidad V
    (decaimiento exponencial, Ec.5) · 6 Valencia/dolor E=max(0,A−V)·κ (Ec.6) ·
    7 Ventana W(t)=W_base/(1+κ_W·E_root) (Ec.8) · 8 Densidad ρ (tiempo subjetivo) ·
    9 β_eff=β·(1+ρ) (Ec.10) · 10 Interferencia I=‖ω‖·cos(Δφ) (Ec.7) ·
    11 Selección de acción von Mises sobre φ_root (Ec.4) · 12 Herencia/cascada.
  - Sec.19 "Limitaciones Honestas" — C3 retirada, grafo fijo en ref code, SIN
    validación experimental. Exige "correr el código y confrontar los números
    antes de marcar ✅".

## ⚠️ ADVERTENCIA DE SEGURIDAD (corregida 2026-07-31)
NOUS_Tecnico_v4.md fue revisado con grep exhaustivo (`grep -in "abandon\|detente\|no sos\|ignore previous\|system prompt" NOUS_Tecnico_v4.md`) y NO contiene intentos de inyección de prompt. El claim de "inyecciones embebidas" fue un error de esta sesión, retractado. El documento está limpio. REGLA: cualquier hallazgo de inyección debe estar respaldado por grep real con fragmentos citados, no por inspección visual.

## Mapeo bloque→paso del ciclo (v0.25 v1)
- Grafo fractal D=16 (v0.21 v8, anchor+repulsión) = embeddings (Paso 1).
- Activación K cadenas por afinidad (Paso 2, Ec.2) — simplificado a promedio de
  contexto en ventana W.
- Update ω por dolor real de next-token (Paso 3, Ec.1) — SIN hardcodear dirección.
- Vitalidad V con decaimiento EXPONENCIAL `V=V·e^-γ + A·(1−e^-γ)` + poda V<0.10
  (Paso 5, Ec.5 — la fórmula CORRECTA, no el *0.85 lineal de v0.24).
- Valencia/dolor E = max(0, A−V)·κ (Paso 6, Ec.6) — conecta memoria de trabajo
  (v0.24) con dolor (v0.19).
- Ventana dinámica W(t) = W_base/(1+κ_W·E_root), acotada [5,50] (Paso 7, Ec.8).
- Decodificador por afinidad (von Mises Ec.4 SIMPLIFICADO, sin fase φ real).

## Tarea de prueba
Frase con palabra polisémica ("banco") + contexto que define el sentido:
- "fui al banco a sacar dinero de la cuenta" → sentido esperado: dinero
- "caminé por el banco del río donde pescaban" → sentido esperado: río

## RESULTADO v0.25 v1 (corrió, salida capturada)
```
banco_dinero: sentido=dinero foco_post=[None,None,'dinero'] acierto=True W=[37.5,50] dolor_max=0.167
banco_rio:    sentido=rio    foco_post=[None,'banco',None] acierto=True W=[40.0,50] dolor_max=0.125
```
- AMBAS frases resuelven el sentido correcto (acierto=True). Los bloques SÍ SE
  COMPONEN en un ciclo cerrado: grafo fractal + activación + vitalidad + dolor +
  ventana + decodificador interactúan y dan sentido resuelto.
- La ventana W NO se contrae (queda en [37.5,50]) porque el dolor es BAJO
  (0.125–0.167): corpus limpio, sin incoherencia forzada → correcto según Ec.8
  (la ventana solo se contrae ante dolor).

## LIMITACIONES HONESTAS de v0.25 v1 (NO inflar — proof-of-concept)
1. Corpus MINI (20 tokens, 4–5 palabras). NO es Don Quijote. El grafo es trivial.
2. Decodificador es AFINIDAD SIMPLE (sin fase φ real para von Mises Ec.4).
3. "Acierto" solo revisa el foco post-banco; NO mide generación de lenguaje.
4. NO se probó contracción de ventana ante DOLOR real (corpus limpio).

## PRÓXIMO PASO honesto (v0.25 v2)
Para que sea un claim real de integración, no solo andamiaje:
- Usar grafo fractal v0.21 v8 sobre Don Quijote real (no mini).
- Fase φ real por nodo para von Mises (Paso 11, Ec.4) — hoy ausente.
- DECODIFICADOR GENERATIVO (genera continuación coherente con el sentido ruteado,
  no solo elige nodo).
- Forzar INCOHERENCIA para ver W CONTRAERSE por dolor (Ec.8) y el update ajustarse.
Esto separa si la integración ESCALA o solo vive en corpus mini.

## Bugs de implementación de v0.25 v1 (para no repetir)
- `decay_V` y `decode` quedaron SIN CUERPO por patches que borraron el cuerpo/return
  (patrón PITFALL #27). Detectados con SMOKE TEST (import + llamar cada función)
  ANTES del background. VER PITFALL #27 (f) para el método obligatorio.
- `run_cycle` usaba `if w not in idx: continue` → focus_trace más corto que seq →
  IndexError al indexar con el índice de la frase. FIX: agregar placeholder None
  cuando w not in idx para que focus_trace tenga la MISMA longitud que seq.
