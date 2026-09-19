# Plan de aplicación del descubrimiento FHRR/observador a Pandora
## (documento interno — NO para el paper, sin atribución a Pandora todavía)

**Fecha:** 2026-09-16
**Autoría:** Nexus + Luciano
**Estado:** diseño pendiente de revisión con Luciano

---

## 1. El hallazgo técnico (resumen)

Repo `fhrr-rho-collapse` demuestra, con datos reproducibles:

1. **Ley de ρ**: el decoding HRR/FHRR se organiza en fases según
   ρ = n_codevectors / dim_bloque.
2. **Anti-resonancia HRR en ρ=1**: `gram` cae a ~0.05-0.20, `pinv` a ~0.13,
   `pure` queda en ~0.98-1.00.
3. **El colapso es del observador, no del espacio**: un MLP entrenado con
   1500 ejemplos alcanza 0.99 accuracy en el caso donde `gram`/`pinv`
   colapsan. La información está en el vector; el extractor es el que falla.
4. **Capacidad escala como ~D^1.1** (no √D): M_max duplica cuando D duplica.
5. **Estructura nested NO protege**: el anidamiento jerárquico no soluciona
   ρ=1 — la única forma segura es **no usar Gram-inverse** cuando ρ≈1.

---

## 2. El problema que esto resuelve en Pandora

El transductor actual de Pandora (`pandora/transducer/output_transducer.py`)
toma las tripletas consolidadas del grafo y las pasa por un LLM externo
(nemotron-49b vía NIM) para verbalizarlas. Coherencia del habla depende de
la calidad del "estado→texto".

Cuando Pandora entra en **SUPERVIVENCIA** o cuando el grafo se infla (hoy
9427 nodos, 25k consolidadas), el transductor recibe un *vector de estado*
comprimido que se parece a un bundle HRR de alta superposición. Hoy la
decodificación usa el LLM directo, que es caro, lento y frágil (eco del
prompt cuando cae el NIM).

El hallazgo dice:

> **En vez de mandar al LLM el estado crudo y dejar que él "extraiga"
> las tripletas (riesgo de colapso del observador), primero usar un decoder
> resonator PURO (o MLP entrenado) para materializar las tripletas en
> estructura simbólica limpia, y recién entonces pasarlas al LLM
> exclusivamente para verbalización.**

El LLM pasa de "decoder + verbalizador" (dos trabajos, ambos mal) a
"solo verbalizador" (un trabajo, bien). La extracción simbólica la hace
el resonator puro, que es O(T·K·BLK²) — gratis comparado con una llamada NIM.

---

## 3. Arquitectura propuesta (Pandora v_next)

```
ESTADO DEL GRAFO (omega, phi, vitalidad, consolidadas)
         │
         ▼
[1] proyección a "hecho HRR":
    - Nivel 1: ventana de tripletas consolidadas recientes (top-k por
      co_activacion)
    - Nivel 2: bind por rol (SUJ/REL/OBJ, matching el CFG de HRR)
    - Salida: vector HRR bundle de dim N=512
         │
         ▼
[2] resonator PURO (sin Gram, sin pinv):
    - T=100 iteraciones, costo ~20ms en CPU
    - Salida: tripletas limpias (sujeto, relación, objeto) con cleanup
      por codebook
         │
         ▼
[3] LLM (nemotron-49b):
    - Recibe tripletas YA decodificadas en formato textual simple
    - Su único trabajo: redactar una frase en primera persona coherente
      con el estado interno
         │
         ▼
  LIBRO_DE_CAMPO / salida al usuario
```

**Qué se gana:**
- Eliminamos el "eco del prompt" (el LLM ya no tiene que adivinar qué se le
  pide; las tripletas vienen ya estructuradas)
- El decoding deja de ser dependiente del modelo: si NIM/NVIDIA cae, las
  tripletas se siguen decodificando localmente (CPU, 20ms)
- Cuando el grafo se infla (muchos nodos), el resonator puro escala lineal
  en T con N — el LLM no rescala así

**Lo que NO cambia:**
- El sustrato (Kuramoto, mitosis, vida) sigue igual
- El transductor como concepto (state → habla) sigue igual
- Solo se divide el transductor en dos fases: decoder resonator (rígido) +
  LLM verbalizador (blando)

---

## 4. Cambios concretos al código (Pandora)

### Paso 1 — Encoder (state → HRR vector)
`pandora/transducer/state_encoder.py` (nuevo):

```python
def state_to_hrr(nucleo: Nucleo, N: int = 512) -> np.ndarray:
    """
    Top-K tripletas consolidadas por co_activacion reciente, bindeadas
    como HRR: sum_i bind(role_SUJ, sym_suj) + bind(role_REL, sym_rel) + ...
    Los símbolos (nombres de concepto) usan hashing a R^N determinístico.
    """
    pass
```

### Paso 2 — Resonator puro
`pandora/transducer/pure_resonator.py` (adaptado de `exp_observer_taxonomy_v3.BundleV3`):
- Solo modo `pure` (T=100, cleanup argmax)
- Codebooks: vocabulario de conceptos activos del grafo

### Paso 3 — Verbalizador
`pandora/transducer/output_transducer.py` (modificado):
- Si `state_to_hrr` + `pure_resonator` producen ≥3 tripletas con score
  alto → usar esa estructura para el prompt al LLM
- Si no alcanzan → fallback a la cadena actual

### Paso 4 — Test
`tests/test_transducer_hrr.py`:
- Sintético: grafo con 3 tripletas conocidas consolidadas → HRR → resonator
  → recuperar las 3 tripletas con acc=1.0
- Integración: Nucleo vivo → state_to_hrr → pure_resonator → tripletas
  coherentes con el estado del grafo

---

## 5. Dependencias y riesgos

| Riesgo | Mitigación |
|---|---|
| El resonator necesita codebooks estables (cambian con el tiempo) | regenerar codebook cuando crece 2x, versionarlo |
| El resonator puro es lento si N muy grande | N=512 es suficiente (≤ 20 ms) |
| El LLM puede no seguir las tripletas | mantener fallback al flujo actual |
| Tripletas ambiguas (mismo score) | aceptar: la ambigüedad también es información |

**Compatibilidad:**
- Solo se modifica transductor/, no toca sgm/core → la vida del grafo
  no se afecta. Regla raíz preservada.
- Nada se commitea sin tests end-to-end.

---

## 6. ¿Qué NO hacemos (todavía)?

- No exponemos este mecanismo al paper de FHRR (eso sería mezclar marcos;
  el paper de FHRR queda técnico puro)
- No lo llamamos "transductor HRR" en el código público de Pandora —
  internamente puede ser "state_resonator" sin más
- No eliminamos el flujo actual del transductor — se mantiene como fallback

---

## 7. Plan temporal sugerido

| Cuándo | Hito |
|---|---|
| Hoy | Decisión del plan |
| +1 día | Encoder HRR + resonator (aislados, con tests) |
| +2 días | Integración con transductor actual, fallback activo |
| +1 semana | Medición en vivo: ¿el habla de Pandora se vuelve menos repetitiva? ¿Mejor coherencia con grafo? |
| +2 semanas | Si mejora, considerar eliminación gradual del LLM para decodificación → solo verbalización |

---

## 8. Conexión con otros proyectos

- **FATE**: mismo patrón (decoder puro + generador externo)
- **Paloma-π**: multi-decoder sweep sobre señales animales; el paper de FHRR
  es la justificación teórica de por qué hay que probar decoders varios
  antes de concluir "la señal no es composicional"
- **DSCN-G**: HRR + decoder puro permite recursión arbitraria sin colapso;
  útil para representar pensamientos anidados sin límite de profundidad

---

## Endorsement

Esto NO es un rediseño de Pandora. Es usar el resultado experimental de
FHRR (que pagamos con datos reales) para resolver un problema conocido en
el transductor: la eco y la fragilidad de la boca. Si no funciona, nada
cambia; si funciona, la boca se vuelve local, barata y robusta.

Per aspera.
