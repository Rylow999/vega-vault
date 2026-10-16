# Dominio: Collatz (dinámicas discretas) — análogo de la ley ρ

**Fuente:** LOGOS/COLLATZ/collatz-divergence-threshold (paper + 25.000 órbitas)

## El patrón

El observable es la **frecuencia de visitas** a la clase P = {n ≡ 3 mod 4}:

    f_P = visitas_P / total_pasos

- El umbral teórico es **f_P* = log₄(8/3) = 0.7075** (derivado, condicional a LEH).
- **25.000 órbitas simuladas: 0 superan el umbral** (máximo observado 0.667).
- La correlación f_P ↔ longitud de órbita es **0.7355** (fuerte): cuantas más
  visitas a P, más larga la órbita.

## Análogo de la ley ρ

| VSA/HRR | Collatz |
|---|---|
| ρ = n_codevectors / dim | f_P = visitas_P / total |
| Umbral κ* = 5.81×10³ | Umbral f_P* = 0.7075 |
| ρ=1 → colapso del decoder | f_P ≥ f_P* → divergencia de la órbita |

**El patrón común:** un parámetro admisible (ρ, f_P, κ) con un umbral exacto
que separa el régimen estable del colapso. En los tres dominios, el umbral es
**derivado** (no ajustado) y **falsable** con datos.

**La conexión más profunda:** en VSA, ρ mide cuánta información se apila por
dimensión. En Collatz, f_P mide cuánto "presupuesto de pasos P" consume la
órbita. En SDDF, κ mide cuánta resolución pide el observador. **Los tres son
razones de saturación** — y los tres tienen una singularidad puntual donde el
sistema cambia de régimen de forma no-gradual.
