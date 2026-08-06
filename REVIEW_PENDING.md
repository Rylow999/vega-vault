# Review Pending — Decisiones humanas

> Generado en la reorg 2026-07-25. Los ítems marcados [RESUELTO] ya tienen
> veredicto de Luciano; los demás son notas de rigor que no requieren
> nueva decisión (son caveats de citación). No se asumió ni validó nada.

## 1. [RESUELTO] Rol de NOUS = HÍBRIDO
NOUS es paraguas activo (DSCN-G núcleo + Quantum/Gauge/Cosmos en desarrollo +
doc filosófica especulativa). Todo lo no-core lleva etiqueta "extensión en
revisión". Operativamente: DSCN-G = "paper 0 de NOUS". FATE y LOGOS son
líneas independientes al mismo nivel (raíz).

## 2. [RESUELTO] Claim 5 — C3 / Face Hijacking = OPEN QUESTION en EXTENSIONS
C3 es efecto del sistema, NO core. En NOUS/DSCN-G/EXTENSIONS/C3_Face_Hijacking/.
No sustentado a params orig (0.9% triggers, ΔPLV≈0; rise_rate 30.2% solo con
params agresivos). Open question para revisión final pre-congelación.
Analogía thálamo/hub_boost RETIRADA (Ronda 6, sin efecto por saturación).

## 3. [RESUELTO] Claim 7 — Φ_proxy O(log N) = OPEN QUESTION en EXTENSIONS
Investigación en NOUS/DSCN-G/EXTENSIONS/PHI_PROXY/. Dos métricas indep NO
sostienen O(log N): MI cruda R² vs log(N)=0.22; TE-bottleneck (aprobada) da
Φ_proxy plano ~0.01-0.02 en N* 2.7-29.4 (R² vs log(N)=0.337). TE-bottleneck SÍ
es métrica útil (arrastre-vs-integración durante hijack). Open question.

## 4. [RESUELTO] Teorema 3 — consenso de fase = REPORTE ESTRICTO
T3 es del NÚCLEO (se sostiene con matiz). Paper debe reportar: consenso
estricto R≥0.9 = 23/30 (76.7%); 0 bimodales; el código cuenta además criterio
laxo R≥0.5 (weak_unimodal) por diseño, dando 100% operacional. NO ajustar el
teorema a R≥0.5 (sería bajar el estándar sin justificación). Mostrar ambos
números y explicar el desajuste. Esto blinda el claim para revisión externa.

## 5. [NOTA DE RIGOR] Posibles duplicados / mezclas
- nback_v5_legacy_flawed/ en EXPERIMENTS/N_BACK: bug legacy, conservado por
  transparencia. NO mover sin aviso.
- verify_phi_proxy.py (legacy) y verify_phi_proxy_v3.py en EXTENSIONS/PHI_PROXY.
- Collatz en 3 papers (Complexity, Structural, Confinement): complementarios,
  no duplicados; conviene índice cruzado en LOGOS.

## 6. [NOTA DE RIGOR] Caveat numérico al citar
Control P1 del test de robustez TE-bottleneck dio TE_baseline=0.0000±0.0000
(probable artefacto del guard du>dr en covarianzas casi-simétricas). No citar
P1 con valores absolutos sin revisar el estimador.

## 7. [RESUELTO] Claims 9 y 10 — redistribuidos
- Claim 9 (NCC / conciencia): NOUS/DOCUMENTATION/ (especulativo, no verificado).
- Claim 10 (drug discovery): FATE/ (es la aplicación FATE).
