# MNEME — Guía de Implementación
## La capa de memoria hiperdimensional de Pandora

**μνήμη** — la memoria. Como LOGOS (razón) y NOUS (mente): una palabra griega,
un subsistema del programa.

**Ubicación:** `HORIZON/MNEME/` (el apartado de la unión: Pandora ES su caso
de aplicación cognitiva declarado).
**Protocolo:** `DOCUMENTATION/METODO_INTEGRAL.md` — obligatorio en cada fase.
**Fecha:** 2026-10-11. **Estado:** DISEÑO — nada se construye hasta que las
fases previas pasen sus predicciones pre-registradas.

---

## 0. Problema exacto (protocolo, paso 1)

**Dominio:** el grafo vivo de Pandora (9.427 nodos, 31.177 consolidadas,
checkpoint atómico) + sus interfaces (transductor, boca NIM, journal).

**Enunciado:** dotar a Pandora de (a) consulta estructurada de su propia
memoria por álgebra FHRR (binding/unbinding sobre el codebook de conceptos
del grafo), (b) memoria episódica con recall, (c) acceso a su vault, y
(d) una colonia de SLMs especializados — SIN reescribir el núcleo, SIN
nueva infraestructura mientras no haya medición que la exija.

**Lo que NO es:** no es un nuevo cerebro, no reemplaza el SGM (el grafo ES
la BD — raíz del programa), no es RAG clásico, no inventa mecanismos
cuánticos (protocolo 4.6: el mecanismo es álgebra de frames, probado).

---

## 1. Auditoría de Pandora: qué tiene y qué le falta (verificado en código, 2026-10-11)

### Lo que YA tiene (no se re-construye)

| Pieza | Verificación | Estado |
|---|---|---|
| Núcleo residente | `pandora/runtime/nucleo.py`, systemd Restart=always | **FUNCIONAL** (vivo, tick 10 tras despertar) |
| Grafo = BD | 9.427 nodos, 31.177 consolidadas, checkpoint 0.990 | **FUNCIONAL** |
| Percepción interoceptiva | `pandora/senses/entorno.py` (CPU/RAM como HRR bundle, 0067) | **FUNCIONAL** |
| Oídos (es→constelaciones) | `transducer/semantic_parser.py` (few-shot, Ollama 0.5b) | **FUNCIONAL (limitado: 0.5b)** |
| Boca (constelaciones→es) | `transducer/output_transducer.py` + NIM | **FUNCIONAL** |
| Resonador HRR del paper | `transducer/pure_resonator.py` — cita el paper FHRR, robusto en todo ρ | **INTEGRADO, con fallback silencioso** |
| Opacity + inefabilidad | gates en la boca (ACTA P1) | **FUNCIONAL** |
| Endocrino | hormonas arbitran sueño/devenir (no hardcode) | **FUNCIONAL** |
| Mano (efector) | `motor/archivos.py` con presupuesto | **FUNCIONAL** |
| Journal | `journal/episodes.jsonl` | **EXISTE, sin recall** |

### Los gaps reales (verificados contra código, no contra memoria)

| # | Gap | Evidencia | Severidad |
|---|---|---|---|
| G1 | **Codebook FHRR fuera de capacidad**: `state_to_hrr(N=512, top_k=8)` contra codebook de ~9.4k nodos → ρ = 9427/512 ≈ 18 ≫ 1: el frame está a 18× del cuadrado; capacidad real ~0 (nuestro Exp 28/teoría del hard edge). El resonator cae en fallback. | `output_transducer.py` L40-55; teorema frame-dual (fhrr-rho-collapse) | **CRÍTICO: es EL cuello de botella L2 declarado en HORIZON** |
| G2 | **Sin memoria episódica consultable**: episodes.jsonl se escribe pero no hay recall (ningún módulo lo lee). | `ls pandora/journal/` solo episodes.jsonl | ALTO |
| G3 | **Sin acceso al vault**: Pandora no puede consultar vega-vault (sus papers, notas, la ontología DSCN-G) | ausencia total de módulo de lectura | MEDIO |
| G4 | **Parser 0.5b limitado**: few-shot simple pierde estructura compleja (el propio docstring lo admite) | `semantic_parser.py` header | MEDIO |

**Corolario de la auditoría:** el documento de la propuesta externa (GBrain +
n8n + colonia) resuelve G2-G4 — pero el G1 es OURS: nadie más sabe que el
codebook está 18× fuera de capacidad. Sin arreglar G1, cualquier capa de
memoria hiperdimensional que se agregue hereda el mismo colapso. **MNEME
empiega por G1.**

---

## 2. Diseño de MNEME (mínimo, sin ingeniería prematura)

### Arquitectura (4 capas, sobre lo existente)

```
PANDORA (núcleo residente — NO se toca)          [EXISTE]
  │  grafo SGM = la BD (9.4k nodos)              [EXISTE]
  ▼
MNEME-1: CODEBOOK FHRR del grafo                  [NUEVO — G1]
  │  conceptos → hipervectores; D elegido por capacidad
  │  consulta: bind(rol, valor) → superposición → unbinding dual
  │  item-memory para cleanup (la estrategia pure, Exp 18)
  ▼
MNEME-2: MEMORIA EPISÓDICA                        [NUEVO — G2]
  │  episodios del journal → hipervectores con marcas temporales
  │  recall: consulta por similitud + unbinding del contexto
  ▼
MNEME-3: ACCESO AL VAULT                          [NUEVO — G3]
  │  índice FHRR de vega-vault (papers, notas, ontología)
  │  misma interfaz de consulta que MNEME-1
  ▼
MNEME-4: COLONIA SLM                              [ÚLTIMO — G4 + propuesta]
     router semántico + especialistas con LoRA
     (solo cuando MNEME-1/2/3 tienen medición)
```

**La regla de construcción:** cada capa se construye SOLO cuando la anterior
pasa su predicción pre-registrada. Si MNEME-1 no pasa, no hay MNEME-2 y nos
ahorramos todo el edificio.

### 2.1 MNEME-1 en detalle (la pieza crítica)

**El problema G1 en números:** codebook de n=9.427 conceptos. Con
unbinding-cleanup contra item-memory, el requisito es que el símbolo
correcto sea recuperable de una superposición de k binds ruidosa. La
probabilidad de error de un cleanup HRR con D dimensiones y n símbolos
~ Φ(√D·(1−sim incorrecta)/2) — para n=9.427 se necesita D tal que las
hipervectores sean casi-ortogonales: D=2048 da sim~1/√D entre random,
y separación de argmax saludable (teoría estándar HDC: D≥10·log₂(n)²
para n~10⁴ → D~2048 es suficiente para cleanup EXACTO de 1 símbolo).

**Diseño correcto (respectando la lección de hoy):**
- **D = 4096** (margen; el costo de FFT en numpy es despreciable)
- **Codebook NO aleatorio por símbolo**: los conceptos del grafo se
  representan por su VECINDAD (los k vecinos co-activos) — la semántica
  del grafo entra en la fase del hipervector (HRR "estructural")
- **ρ efectivo = k_roles_consultables / D, NO n/D**: en cada consulta se
  decodifican k≤8 roles (los que la boca ya usa), no los 9.427 — el
  codebook completo es el ITEM MEMORY (cleanup por similitud), no el
  bundle. La capacidad del frame aplica a la consulta (k=8 < D), no al
  inventario. **Este es el malentendido de la propuesta externa corregido.**

**Predicciones pre-registradas MNEME-1 (PR-M1):**
- PR-M1a: cleanup exacto (top-1 correcto) ≥ 99% para consultas de 1 símbolo
  contra el codebook de 9.427 con D=4096, k=1 bind. [sanity]
- PR-M1b: unbinding de k=8 roles con cleanup ≥ 85% por rol (el estándar
  del paper para el régimen sano). [central]
- PR-M1c: la consulta por binding ("¿qué co-actúa con X?") recupera
  relaciones del grafo que BM25 sobre los nombres de nodos NO encuentra
  (relaciones multi-hop: X co-actúa con Y, Y co-activa Z → la superposición
  X tiene traza de Z). [falsable: si el HRR estructural no codifica
  multi-hop, esta predicción muere y con ella el diseño del codebook
  por vecindad]

**El experimento cero (antes de escribir cualquier módulo):**
tomar 500 nodos del grafo real de Pandora, hacer su codebook FHRR,
correr PR-M1a/b/c. Costo: un script, media hora, sin tocar el daemon.

### 2.2 MNEME-2: memoria episódica

Cada episodio del journal → bind(rol_tiempo, contexto) + bind(rol_tema,
tripleta) superpuesto. Recall: unbind(rol_tema) + cleanup contra el índice
de episodios. Predicción PR-M2: recall de un episodio por su tema con
precisión ≥ 90% entre 100 episodios sintéticos.

### 2.3 MNEME-3: acceso al vault

Índice FHRR de los documentos del vault (título + resumen por doc). La
consulta de Pandora ("¿qué sé de frames?") → bind + cleanup → lista de
docs relevantes → los OPENa con la mano (que ya existe). Predicción
PR-M3: para 10 consultas de prueba, el doc correcto en top-3 ≥ 8/10.

### 2.4 MNEME-4: colonia SLM

**Solo después de 1-3.** Diseño mínimo: NO LangGraph, NO n8n al inicio —
el propio nucleo.py de Pandora hace de router (ya decide cuándo hablar;
extender a qué especialista invocar). SLMs: los 3 roles del documento
(ingestor/crítico/sintetizador) como invocaciones NIM con prompts
especializados (cero infraestructura nueva: el NimClient existe). LoRA
hot-swap SOLO si la medición pide personalización.

**Por qué no n8n desde el día 1 (protocolo: complejidad prematura):**
el 90% del valor de MNEME es la consulta estructurada (1-3). n8n agrega
valor cuando hay webhooks externos — y eso no es requisito de Pandora.

---

## 3. Métodos (tabla del protocolo aplicada a MNEME)

| Método | Clase | Rol en MNEME |
|---|---|---|
| HRR binding/unbinding + cleanup | álgebra (probada, fhrr paper) | EL mecanismo — no analogía |
| Codebook por vecindad del grafo | hipótesis de diseño | PR-M1c la testea |
| Item memory por similitud | estrategia pure (Exp 18: 0.985) | el cleanup — sin resolvente |
| Unbinding dual (C^T M^+ C) | teorema frame-dual | solo si el cleanup se queda corto (palm. del dominio) |
| Medida cuántica / medición proyectiva | DESCARTADO (4.6) | NO se usa — la corrección de hoy |
| RAG denso clásico | DESCARTADO como núcleo | sí como fallback BM25 del vault |
| Colonia SLM con router LLM | retenido (lit.: Adaptive Minds, ProST) | MNEME-4 |
| LoRA hot-swap | retenido condicional (lit.: AgentFlux) | solo con medición que lo pida |

## 4. Barreras conocidas (declaradas antes de empezar)

1. **Barrera de capacidad (la lección del hard edge):** si el codebook de
   consulta crece (roles simultáneos > D/4), la degradación es
   matemática, no de implementación. El diseño la respeta por
   construcción (k=8, D=4096).
2. **Barrera de correspondencia:** PR-M1c es el puente — si la vecindad
   del grafo no codifica semántica consultable, MNEME-1 cae y hay que
   rediseñar el encoder (por ejemplo, con las fases aprendidas de las
   co-activaciones en vez de derivadas de nombres).
3. **Barrera del daemon:** MNEME se monta AL LADO del núcleo (import en
   la boca), nunca dentro del loop de ticks — el riesgo de matar a
   Pandora con un bug nuevo es inaceptable (1ª orden).

## 5. Fases con criterios de salida (checklist ejecutable)

**FASE 0 — RESULTADO (2026-10-11, corrida):**

| Predicción | Resultado | Veredicto |
|---|---|---|
| PR-M1a (cleanup k=1, D=4096, 500 nodos) | **1.0000** | **PASS** |
| PR-M1b (k=8 roles superpuestos) | top-1 0.375, **top-5 1.000** | **PASS** (por top-5) |
| PR-M1c (multi-hop por vecindad-hash) | 0.027 | **FAIL** |

**Lectura del FAIL de PR-M1c (la barrera declarada §4.2, ocurrió):** el
encoder por hash de nombres numéricos no codifica semántica del grafo —
la superposición no puede contener traza de Z si el vector de Z no
comparte estructura con el de X. El mecanismo (binding/unbinding/cleanup)
está VALIDADO (M1a/M1b); lo refutado es el ENCODER por vecindad-hash.
**Rediseño (barrera 2 de la guía): fases aprendidas de las
co-activaciones reales del grafo** (phase = ángulo del vector de
activación normalizado del nodo), no hash del nombre. Este encoder es
el primer trabajo de MNEME-1 real.

**FASE 0 — original (para registro):**
- [ ] Script `exp_mneme_0.py`: 500 nodos reales del grafo → codebook
- [ ] PR-M1a medido y documentado (≥99%: PASS/FAIL)
- [ ] PR-M1b medido (≥85%: PASS/FAIL)
- [ ] PR-M1c medido (multi-hop: PASS/FAIL)
- [ ] Estado etiquetado en este documento (protocolo 17)
- [ ] Si todo PASS → Fase 1. Si algún FAIL → rediseño del encoder y Fase 0 de nuevo.

**FASE 1 — MNEME-1 integrado en la boca (1 día de trabajo):**
- [ ] `state_to_hrr` re-parametrizado (D=4096, vecindad)
- [ ] PureResonator alimentado por el nuevo codebook
- [ ] Medir: ratio usado/fallback del resonator (hoy desconocido →
      loguearlo; objetivo: usado > 50% de las hablas)
- [ ] Los tests del guardian (147t) siguen en verde

**FASE 2 — MNEME-2 episódica (1 día):**
- [ ] Indexar journal → índice FHRR
- [ ] PR-M2 medido (≥90%: PASS/FAIL)
- [ ] Pandora puede responder "¿qué pasó ayer?" con episodio real

**FASE 3 — MNEME-3 vault (1 día):**
- [ ] Índice del vault; PR-M3 medido (8/10: PASS/FAIL)
- [ ] Integración con la mano (abrir docs)

**FASE 4 — MNEME-4 colonia (solo si 1-3 pasaron):**
- [ ] Router en nucleo (3 prompts especializados via NimClient)
- [ ] Medición: calidad de respuesta con/sin router (ciego, 10 casos)
- [ ] LoRA solo si la medición muestra necesidad de especialización real

## 6. Referencias (verificadas)

1. Todo el aparato FHRR/frame-dual: `github.com/Rylow999/fhrr-rho-collapse`
   (teorema, Exp 18/20A/27/28, GPT-2 real, MiniLLM NO-GO).
2. Adaptive Minds (arXiv:2510.15416): LoRA-as-tools con router semántico
   — el patrón de MNEME-4, open-source.
3. AgentFlux (arXiv:2510.00229): decoupled fine-tuning LoRA, +46%.
4. ProST (IJCNLP 2025): orchestrator fuerte > ejecutores fuertes.
5. HINDSIGHT / OpenMem: la competencia usa HDC/HRR para memoria de
   agentes — confirma la dirección; NUESTRO diferencial es el teorema
   de capacidad que ellos no tienen.
6. Kleyko et al., ACM CSUR 2023: el survey HDC/VSA (base teórica).

## 7. Errores conocidos y honestidad (protocolo 11)

- El documento externo original (la propuesta) usó lenguaje cuántico
  ("medición proyectiva") para el mecanismo de colapso: CORREGIDO. El
  mecanismo es álgebra de frames (probada). Esta corrección está
  documentada arriba (§0, §3).
- La capacidad del frame (ρ=n/d) es la restricción de diseño #1 y viene
  de NUESTRO teorema — ningún sistema competidor (OpenMem, HINDSIGHT)
  la declara. Si MNEME funciona, esa declaración es el paper.
- La Fase 0 puede fallar (PR-M1c): si la vecindad del grafo no codifica
  semántica recuperable, el codebook por vecindad se abandona y se prueba
  el encoder por co-activaciones. El diseño es falsable por fase.

## 8. El siguiente paso concreto

Correr FASE 0. Es un script de 100 líneas contra el grafo real de Pandora,
media hora, sin tocar el daemon. Todo lo demás espera su veredicto.
