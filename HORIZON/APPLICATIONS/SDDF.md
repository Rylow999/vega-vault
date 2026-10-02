# SDDF — aporte al marco HORIZŌN

**Repositorio:** `github.com/Rylow999/sddf` — repo git local `/home/delorien/sddf`.

## El resultado central (qué es el SDDF)

G[u] = ∫ (d ln E(k)/d ln k)² d ln k  — curvatura espectral del espectro de energía.

**Forma cerrada exacta** (la ancla matemática del marco): G*[u] = (25/12)·ln Re + b(δ) + O(Re⁻¹) — el cuadrado de la pendiente de Kolmogorov (−5/3)² = 25/9 por el exponente de escala de la escala de Kolmogorov η ∝ Re^(−3/4) = 3/4. Eso es teorema, no ajuste.

Cómo serve al marco: la disipación viscosa (confinamiento) tiene forma cerrada exacta; en los otros dominos del marco el confinamiento es teorema numérico (Collatz), control (DSCN-G) o ley geométrica (Gauge). Navier-Stokes es donde la estructura tiene fórmula.

## Qué es nuevo acá (28-09-26, commits v3.2–v3.4)

**1. Null model Migdal (v3.2):** el "SNR~19 sin señal" del v3 era 100% artefacto del método (média de los 500 nulos = 19.42, max = 19.63). Umbrales reales: amp=0.005 no pasa; amp=0.02 pasa con p_bonferroni=0.01. El test ahora es calibrado de verdad.

**2. Sync Rust ↔ Python (v3.2):** truncate_by_slope_interp portado a Rust con interpolación idéntica; verificado al dígito contra Python (G*=10.2392, mismo k_corte, 930 puntos, en `spectrum_Re_1000.csv`). Fallback sintético cambiado a Pao β=2.25 (la quimera acordada), no Pope 5.2.

**3. DNS real (v3.3, la montaña):**

| dato | resultado |
|------|-----------|
| Sub-cubo mirror ArielLubonja | no confiable: salto de borde 300-360× el interior → NO periódico; una sola escala integral dentro → sin muestra estadística |
| Box TUM thuerey-group (1024³ float16, periódico de verdad) | ε por gradientes = 0.0891±0.0021 vs documentado 0.0928 (0.96×) |
| Núcleo inercial k∈[8,64] | **q = 1.60 ± 0.02** (−4% vs K41) |
| Invariante 〈s²〉 | NO: 2.1–3.3 según la ventana — patrón de la ley ρ en DNS real |

**4. Detector sobre pendiente suavizada (v3.4, la lección metodológica):**
- El detector puntual (delta=0.5, calibrado en espectros sintéticos suaves) **falla en datos reales**: el ruido concha-a-concha del espectro DNS (sem ~10-15% a k bajos) hace que corte en 3-8 puntos; `inertial_window` devuelve ok=False.
- Solución: `smoothed_slope` (regresión móvil de 5-11 conchas) + `inertial_window_smoothed` (dos lados, bordes excluidos porque su ventana es recortada y no confiable).
- Validación: cosa nula K41 exacto (atol 1e-9) en interior; con ruido 1% el puntual falla y w=9 encuentra la ventana; DNS real con w=5 detecta k∈[12,56] (q=1.53).
- 4 tests de regresión: `tests/test_detector_suavizado.py`.

## Estado epistémico dentro del marco

- Integración: **sólida** (la segunda más sólida después de fhrr, porque tiene forma cerrada + validación DNS real).
- El "punto crítico de colapso" del informe (pregunta abierta #1) tiene evidencia acá: el punto de corte del rango inercial depende del método de medición; mismo sistema, instrumentos distintos, resultado distinto (puntual ok=False vs suavizado q=1.53).

## Lo que falta acá

1. ~~Pushear los commits locales~~ **HECHO** — todo v3.6 (`26072cd`) está en `origin/main`, sincronizado (verificado 2-10-26).
2. **Pendiente científico:** paper 2D (sigue bloqueado por datos de entrada).
3. **Pipeline:** hacer que `exp_detector_suavizado.py` use realmente `spectrum_jhtdb_box_hanning.csv` como test permanente.

*Reescrito después de terminar la validación contra DNS. Todo el numerología venera de `datos/16-19*.csv` y los resúmenes en `datos/17|18_dns_real*_resumen.txt`.*
