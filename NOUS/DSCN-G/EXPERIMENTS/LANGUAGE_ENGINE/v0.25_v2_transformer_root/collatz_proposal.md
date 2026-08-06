# Propuesta de estructura y título para el paper de Collatz
## (2026-07-25, Vega + Luciano) — preparación para envío

> Base: LOGOS/COLLATZ/PAPER/Collatz_Structural_Characterization.md (316 líneas, 5 teoremas, 2 conjeturas).
> Objetivo: reenmarcar para máximo impacto en revista de teoría de números / dinámica discreta
> (ej: Journal of Number Theory, Discrete & Continuous Dynamical Systems, Advances in Mathematics).

## 1. TÍTULO (3 opciones, elegir una)

A) The Divergence Threshold of the Collatz Map: An Exact Closed-Form Necessary Condition
   (enfocado en el resultado cerrado f_P* — el más vendible)

B) 2-Adic Drift and the Critical Frequency of Collatz Divergence
   (enfocado en deriva + umbral, equilibrado)

C) Why a=3: Exact Drift, Golden-Ratio Isolation, and the Baire Gap in Collatz Dynamics
   (más amplio, con gancho de a=3 y phi — pero diluye el resultado principal)

RECOMENDADO: A. El umbral exacto f_P* es el "sello" que un revisor recuerda.

## 2. ABSTRACT REESCRITO (jerarquizado: el cerrado primero)

We prove an exact closed-form necessary condition for divergence in the Collatz map
R_3(n) = (3n+1)/2^{nu_2(3n+1)}. Defining f_P as the empirical frequency of visits to the
class P = {n == 3 mod 4}, we show that any orbit diverging sub-exponentially must satisfy
f_P >= f_P* = log_4(8/3) = (3 - log_2 3)/2 approx 0.7075. The proof is fully analytic and
rests on an exact identity mu_P + mu_N = -2 between the conditional expected drifts in the
natural metric V_{4/3}(n) = log_{4/3}(n). As corollaries we obtain: (i) the exact 2-adic
drift Phi(a) = log_2(a) - 2, recovering the unique contractive odd map a=3 (arithmetic
isolation via 2^phi approx 3.0696); (ii) exact drift -1 in V_{4/3}; (iii) the Fibonacci
structure of log_2(3) convergents. Empirical analysis of 24,866 orbits (n <= 50,000) shows
maximum observed f_P = 0.6667, a 5.8% margin below the threshold, consistent with — but not
proving — convergence. We identify the gap between Tao's "almost every" (2019) and "every"
as the central open problem and propose two precise conjectures (Universal Map Balance,
Baire emptiness of the divergent subspace).

Keywords: Collatz conjecture, 2-adic dynamics, drift analysis, divergence threshold,
Baire category, ergodic theory.

## 3. ESTRUCTURA DE SECCIONES (reordenada para impacto)

1. Introduction — la pregunta: ¿qué condición necesaria y exacta impide la divergencia?
2. Mathematical Framework — mapa acelerado, métrica V_{4/3}, clasificación P/N
3. Main Result — Theorem 5 (Divergence Threshold f_P*) [PRIMERO, es el cerrado]
4. Supporting Results — Theorem 1 (drift 2-adic), Theorem 2 (drift V_{4/3}=-1),
   Theorem 3 (aislamiento a=3 / 2^phi), Theorem 4 (Fibonacci de log_2(3))
5. Empirical Evidence — 24,866 órbitas, margen 5.8%, autocorrelación P/N ~0
6. Open Conjectures — Universal Map Balance, Baire emptiness [claramente future work]
7. The Gap: Almost Every vs Every — Tao 2019, ergodic pathway
8. Conclusions

## 4. QUÉ ESTÁ PROBADO vs ABIERTO (para no inflar)

PROBADO (cerrar como theorems):
- Phi(a) = log_2(a)-2 (Teorema 1)
- Drift V_{4/3} = -1 (Teorema 2)
- Aislamiento a=3, 2^phi=3.0696 (Teorema 3, Part 1 esencial)
- Convergents Fibonacci de log_2(3) (Teorema 4, aritmético)
- Umbral f_P* = log_4(8/3) exacto (Teorema 5) — EL SELLO

ABIERTO (conjectures, no claims):
- Universal Map Balance (f_P -> 0.5): SUFICIENTE para convergencia si se prueba
- Baire emptiness de Sigma_div: vía categoría de Baire

NOTA HONESTA: el paper NO prueba la conjetura de Collatz. Prueba una CONDICIÓN
NECESARIA exacta (f_P >= 0.7075 para diverger). Eso es original y sólido por sí solo.
No decir "avance hacia Collatz" si no se prueba; decir "caracterización exacta del
borde de divergencia".

## 5. DETALLES DE AUDITORÍA
- 2^phi = 3.0696 en el paper original (CORRECTO; el error 3.694 estaba en mis docs de
  la Tríada, ya corregido, no afecta este paper).
- Teorema 5 es fully analytic, sin inputs empíricos => no depende de simulaciones.
- Empírico es corroboración, no soporte del teorema. Separar bien en el paper.
