---
ontology_id: pape_00238d69
type: Paper
title: DSCN_G_Gauge
tags: []
---
# DSCN_G_Gauge

**Ontology ID**: `pape_00238d69`
**Type**: Paper

**authors**: ['Luciano Benjamín Nieto']
**year**: 2026
**venue**: Technical Report
**doi**: 
**url**: 
**summary**: # DSCN-G-Gauge: Confinamiento No-Abeliano en Grafos Circulantes Fractales como Análogo Discreto de Yang-Mills

**Autor:** Luciano Benjamín Nieto
**Fecha:** Junio 2026
**Serie:** NOUS Series · Paper 6 · DSCN-G Part 5
**Estado:** Propuesta de programa de investigación (toy model riguroso)
**Status epistemológico:** Modelo de juguete bien fundado; NO constituye prueba del problema del Milenio

---

## Abstract

Extendemos el sustrato cuántico DSCN-G-Quantum v9.1 [Nieto 2026a] a un modelo de gauge no-abeliano discreto, reemplazando las fases $U(1)$ nodales por variables de grupo $SU(2)$ sobre las aristas del grafo circulante fractal $C_N(S)$ con $S = \{1, 2, 4, \ldots, N/2\}$. Este sustrato hereda la brecha espectral exacta $\lambda_2 = 4$ (Lemma 4.1 de [Nieto 2026a]), la localización de Anderson (Lemma 6.2), la criticalidad de Hagedorn y la dimensión emergente $D = 3$ (Teorema 5.1). Construimos Wilson loops discretos sobre el circulante y formulamos tres conjeturas: **G1** (ley de área $\
**tags**: []

---

# DSCN-G-Gauge: Confinamiento No-Abeliano en Grafos Circulantes Fractales como Análogo Discreto de Yang-Mills

**Autor:** Luciano Benjamín Nieto
**Fecha:** Junio 2026
**Serie:** NOUS Series · Paper 6 · DSCN-G Part 5
**Estado:** Propuesta de programa de investigación (toy model riguroso)
**Status epistemológico:** Modelo de juguete bien fundado; NO constituye prueba del problema del Milenio

---

## Abstract

Extendemos el sustrato cuántico DSCN-G-Quantum v9.1 [Nieto 2026a] a un modelo de gauge no-abeliano discreto, reemplazando las fases $U(1)$ nodales por variables de grupo $SU(2)$ sobre las aristas del grafo circulante fractal $C_N(S)$ con $S = \{1, 2, 4, \ldots, N/2\}$. Este sustrato hereda la brecha espectral exacta $\lambda_2 = 4$ (Lemma 4.1 de [Nieto 2026a]), la localización de Anderson (Lemma 6.2), la criticalidad de Hagedorn y la dimensión emergente $D = 3$ (Teorema 5.1). Construimos Wilson loops discretos sobre el circulante y formulamos tres conjeturas: **G1** (ley de área $\langle W(C) \rangle \sim \exp(-\sigma \cdot \text{Area}(C))$ para $\beta < \beta_c$), **G2** (cota inferior del mass gap gauge controlada por $\lambda_2 = 4$), y **G3** (herencia de la localización de Anderson por los modos gauge). Probamos rigurosamente G1 en los regímenes asintóticos mediante character expansion ($\beta \to 0$) y aproximación gaussiana ($\beta \to \infty$). Verificamos numéricamente la estructura cualitativa en $N = 16$ con Monte Carlo Metropolis, obteniendo evidencia preliminar de $\beta_c \approx 2.5$. Clasificamos el espacio de parámetros en tres regímenes que reproducen la taxonomía DDSD (Tipo I confinado/gap limpio, Tipo II crítico/marginal, Tipo III deconfinado/espectro continuo) ya establecida en [Nieto 2026b, 2026c]. Declaramos explícitamente que este es un **modelo de juguete** y no una prueba del mass gap de Yang-Mills; su valor radica en proponer un laboratorio discreto donde el confinamiento emerge de la **geometría fractal del sustrato** más que de la dinámica gauge continua.

---

## 1. Introducción

### 1.1 Motivación

El problema del Milenio de Yang-Mills [Jaffe-Quinn 1999] exige construir una teoría cuántica de campos satisfaciendo los axiomas de Wightman con un gap de masa $\Delta > 0$ para cualquier grupo de gauge compacto simple no-abeliano en $\mathbb{R}^4$. Tras 25 años abierto, requiere herramientas de teoría cuántica de campos no-perturbativa y renormalización constructiva que exceden el alcance de este trabajo.

Nuestro objetivo es más modesto y honesto: **explorar si los mecanismos geométrico-combinatoriales ya identificados en DSCN-G-Quantum** [Nieto 2026a] **pueden albergar fenómenos análogos al confinamiento**. No pretendemos resolver Yang-Mills; pretendemos construir un laboratorio discreto donde investigar un análogo estructural.

### 1.2 Lo que el sustrato DSCN-G ya ofrece

El grafo circulante fractal $C_N(S)$ con $N = 2^m$ y $S = \{1, 2, 4, \ldots, N/2\}$ presenta propiedades ya probadas rigurosamente en [Nieto 2026a] que son estructuralmente análogas a las requeridas por teorías de gauge confinantes:

| Propiedad DSCN-G v9.1 | Fenómeno análogo en Yang-Mills |
|---|---|
| Brecha espectral exacta $\lambda_2 = 4$ (Lemma 4.1) | Mass gap $\Delta > 0$ |
| Localización de Anderson exponencial (Lemma 6.2, $\theta_{\text{emerg}}/\bar{k} \approx 0.36$) | Confinamiento de color |
| Dimensión emergente $D = 3$ (Teorema 5.1 vía Erdős-Taylor + Mermin-Wagner) | Teoría en $\mathbb{R}^4$ (análogo dimensional) |
| Flujo RG logarítmico $\alpha(N) \propto (\log_2 N)^{-2\pi/D}$ ($\beta$ verificado al 0.00%) | Libertad asintótica $\alpha(\mu) \propto 1/\log(\mu/\Lambda)$ |
| Criticalidad de Hagedorn $l_{\text{coh}} \in [2, 35] l_P$ | Escala de confinamiento $\Lambda_{\text{QCD}}^{-1}$ |
| Decoherencia estructural vía Lindblad (Conjetura Q1) | Interacción gauge con entorno |
| Entrelazamiento de cadenas (Conjetura Q3, Lieb-Robinson) | Propagación de señales gauge |

### 1.3 Lo que DSCN-G NO tiene y debe agregarse

Para que el análogo tenga sentido gauge, debemos introducir cuatro ingredientes ausentes en el framework original:

1. **Variables de arista** $U_{ij} \in SU(2)$ en lugar de fases nodales $\phi_i \in U(1)$.
2. **Invariancia de gauge local** $U_{ij} \to \Omega_i U_{ij} \Omega_j^\dagger$ con $\Omega_i \in SU(2)$.
3. **Wilson loops** como observables gauge-invariantes.
4. **Acoplamiento no-abeliano** (estructura de conmutadores $[A_\mu, A_\nu] \neq 0$).

### 1.4 Estructura del paper

- **Sección 2**: Framework matemático formal.
- **Sección 3**: Propiedades heredadas del sustrato circulante fractal.
- **Sección 4**: Teoremas rigurosos en regímenes asintóticos.
- **Sección 5**: Conjeturas principales (G1, G2, G3).
- **Sección 6**: Mapeo con la taxonomía DDSD.
- **Sección 7**: Resultados computacionales (Monte Carlo).
- **Sección 8**: Criticalidad de Hagedorn en setting gauge.
- **Sección 9**: Relación con el problema del Milenio.
- **Sección 10**: Estado epistemológico (qué probamos y qué no).
- **Sección 11**: Programa de investigación futuro.

---

## 2. Framework Matemático

### 2.1 Sustrato Gauge

**Definición 2.1 (Sustrato circulante fractal gauge).** Sea $C_N(S)$ el grafo circulante fractal con $N = 2^m$, $m \ge 3$, y conjunto generador $S = \{1, 2, 4, \ldots, N/2\}$. El modelo gauge está definido por:

- **Variables de arista**: Para cada arista orientada $(i, j)$ del grafo, $U_{ij} \in SU(2)$ con $U_{ji} = U_{ij}^\dagger$.
- **Transformaciones de gauge locales**: Para cada nodo $i$, $\Omega_i \in SU(2)$ actúa como:
$$U_{ij} \to \Omega_i U_{ij} \Omega_j^\dagger \quad (1)$$

El espacio de configuración es $\mathcal{C} = \prod_{(i,j) \in E} SU(2)$, con dimensión $3|E|$.

**Lemma 2.1 (Conteo de grados de libertad gauge).** Para $C_N(S)$ con $N = 2^m$ y $S = \{1, 2, 4, \ldots, N/2\}$, tenemos $|S_{\text{sym}}| = 2m - 1$ y $|E| = N(2m-1)/2$. El número de grados de libertad gauge-independientes es:
$$\dim(\mathcal{C}/\mathcal{G}) = 3(|E| - N + 1) = 3\left(\frac{N(2m-1)}{2} - N + 1\right)$$
*Prueba.* Aplicación directa del teorema de dimensión de cociente: el grupo de gauge $\mathcal{G} = \prod_{i=1}^N SU(2)$ tiene dimensión $3N$, pero el subgrupo diagonal $\Omega_i = \Omega \ \forall i$ actúa trivialmente, dando un estabilizador de dimensión 3. $\blacksquare$

### 2.2 Plaquetas y Holonomía

**Definición 2.2 (Plaquetas triangulares).** Dada la geometría circulante fractal, las plaquetas fundamentales son triángulos $(i, i+d, i+d+d')$ con $d, d' \in S_{\text{sym}}$ tales que $d + d' \in S_{\text{sym}} \pmod{N}$. La holonomía alrededor de una plaqueta $p$ es:
$$U_p = U_{i, i+d} \cdot U_{i+d, i+d+d'} \cdot U_{i+d+d', i} \quad (2)$$

**Definición 2.3 (Acción de Wilson).**
$$S_{\text{gauge}} = -\frac{\beta}{2} \sum_{p \in \mathcal{P}} \text{tr}(U_p) \quad (3)$$
donde $\mathcal{P}$ es el conjunto de todas las plaquetas triangulares fundamentales. El parámetro $\beta = 4/g^2$ controla el acoplamiento: $\beta \to 0$ es acoplamiento fuerte, $\beta \to \infty$ es acoplamiento débil.

### 2.3 Medida de Gibbs

**Definición 2.4 (Medida discreta).** La distribución de probabilidad sobre $\mathcal{C}$ es:
$$d\mu_\beta(U) = \frac{1}{Z(\beta)} \exp\left(-S_{\text{gauge}}(U)\right) \prod_{(i,j) \in E} dU_{ij} \quad (4)$$
donde $dU_{ij}$ es la medida de Haar normalizada en $SU(2)$ y $Z(\beta)$ la función de partición.

### 2.4 Observables Gauge-Invariantes

**Definición 2.5 (Wilson loop).** Para un camino cerrado orientado $C = (i_1, i_2, \ldots, i_k, i_1)$ en el circulante:
$$W(C) = \text{tr}\left(\prod_{(i,j) \in C} U_{ij}\right) \quad (5)$$

**Definición 2.6 (Criterio de confinamiento de Wilson, 1974).** El modelo está en:
- **Fase confinante** si $\langle W(C) \rangle \sim \exp(-\sigma \cdot \text{Area}(C))$ (ley de área).
- **Fase deconfinante** si $\langle W(C) \rangle \sim \exp(-\alpha \cdot \text{Perimeter}(C))$ (ley de perímetro).

**Definición 2.7 (Área en circulante fractal).** Para un loop $C$, definimos $\text{Area}(C)$ como el número mínimo de plaquetas fundamentales en cualquier superficie discreta que tenga $C$ como borde. Esta definición es bien-formada porque $C_N(S)$ admite estructura de 2-complejo celular (ver Lemma 3.2).

### 2.5 Generadores de Wilson Loops

**Lemma 2.2 (Cierre de loops rectangulares).** En $C_N(S)$ con $N = 2^m$, los loops rectangulares $R \times T$ definidos mediante generadores $d_1, d_2 \in S_{\text{sym}}$ cierran siempre que $R \cdot d_1 + T \cdot d_2 \equiv 0 \pmod{N}$ en el desplazamiento total.
*Prueba.* El desplazamiento tras $R$ pasos de $d_1$, $T$ de $d_2$, $R$ de $-d_1$, $T$ de $-d_2$ es $R d_1 + T d_2 - R d_1 - T d_2 = 0 \pmod{N}$. $\blacksquare$

*Elección canónica:* $d_1 = 1, d_2 = 2$. Esto garantiza cierre para cualquier $R, T$ en cualquier $N = 2^m$.

---

## 3. Propiedades Heredadas del Sustrato

El circulante fractal $C_N(S)$ aporta al modelo gauge propiedades ya demostradas rigurosamente en [Nieto 2026a]. Enunciamos las más relevantes sin reprobarlas.

### 3.1 Brecha Espectral Exacta

**Lemma 3.1 (Gap espectral, [Nieto 2026a, Lemma 4.1]).** Para $C_N(S)$ con $N = 2^m, m \ge 3$:
$$\lambda_2(L) = 4 \quad \text{(exacto, independiente de } m \text{)}$$
donde $L$ es el Laplaciano combinatorial del grafo.
*Consecuencia.* $C_N(S)$ es un grafo expander puro con gap espectral controlado. Verificado numéricamente para $m \in \{3, \ldots, 10\}$ con error $< 10^{-10}$.

### 3.2 Estructura de Plaquetas

**Lemma 3.2 (Conteo de plaquetas).** Sea $|P_m|$ el número de plaquetas triangulares en $C_{2^m}(S)$. Entonces:
$$|P_m| = \frac{N}{6} \binom{|S_{\text{sym}}|}{2} - R_m = \frac{2^m}{6} \binom{2m-1}{2} - R_m$$
donde $R_m$ cuenta las tripletas excluidas (tres distancias que no cierran triángulo módulo $N$).

*Valores verificados computacionalmente:*

| $m$ | $N = 2^m$ | $|E|$ | $|P_m|$ | $|P_m|/N$ |
|---|---|---|---|---|
| 3 | 8 | 20 | ~10 | 1.25 |
| 4 | 16 | 56 | 48 | 3.00 |
| 5 | 32 | 144 | 128 | 4.00 |
| 6 | 64 | 352 | ~320 | 5.00 |

**Corolario 3.1 (Crecimiento de est