# LA TRIADA: Autorregulación Disipativa en NS, DSCN-G, Collatz y Riemann
## Documento de trabajo (2026-07-25, Vega + Luciano)

> Los dominios comparten la MISMA arquitectura: dos dinamicas compiten => 3ra que autorregula.

## 1. La Tríada — 4 dominios
- NS: Transferencia T(k) + Disipacion D(k) => G[k] (Tercer Motor). G acotada 1D/2D/3D.
- DSCN-G: Fase phi_i + Vector omega_i => Vitalidad V_i. Podaa confina grafo (T1).
- Collatz: Deriva 2-adica + Recurrencia => f_P (balance P/N). f_P < 0.7075.
- Riemann: Ceros zeta + Funcion Xi => Regulador GOE. Ceros confinados en linea critica.

## 2. Correccion DDSD
DDSD (sec 11.3) omite E(2^p-1)=p como "no dynamical content". Correcto. Mi test M uso
E=bits y dio aproximado; error de prueba, no del paper.

## 3. Candidato Phi (Galileo) y regularidad
Phi[u]=G[u] cumple: (1) cota invariante Galileo; (2) principio maximo suave (G acotada);
(3) controla H1 via R(k,t)<=C_sat/k.
Numericos: 1D Gmax=3.5e5 H1=1.7 | 2D Gmax=3.2e5 H1=9.6 | 3D Gmax=2.7e4 H1=42.3.

### 3.2 Lema corregido (honesto)
"G acotada => H1 acotada" es FALSO sin mas. Contraejemplo: E=k^-2 abajo de K0, E=k^-1
arriba => G finita pero H1=int k diverge. H1 converge sii alpha(k)>3. G acotada solo da
alpha acotada en promedio. Lema correcto: G* Y alpha_min>=3+eps => H1 finita.
En NS real: Kolmogorov alpha=5/3<3 => H1 divergeria; la viscosidad corta en k_diss.

### 3.3 Lema fuerte (b) — resultado negativo
"G acotada => alpha>=3+eps (no aplanamiento)". Test 3D: CON G alpha_min=0.000,
SIN G alpha_min=0.000. G modera transferencia pero NO impone pendiente minima.
G es regulador REAL (confina T en 1D/2D/3D) pero solo no prueba regularidad NS 3D.
La salva el corte viscoso k_diss (Foias-Temam). Aporte: observacion nueva, no Milenio.

## 4. Nota: 2^phi (aureo) y Collatz/NS
ENCONTRADA en Master-Document/DSCN-G_Master_Document.md (linea 99):
"Corollary: a=3 is arithmetically isolated as the only odd integer in (1, 2^phi),
phi=(1+sqrt5)/2 => 2^phi~3.694."
Esto es AISLAMIENTO ARITMETICO: a=3 es el unico mapa impar en (1, 3.694); arriba
esta el borde a=4 (Phi=0, inaccesible para impares). NO es el umbral dinamico
(ese es f_P*=log4(8/3)~0.7075). Son distintos, no mezclar en paper.
ANALOGO EN NS: el borde critico es R(k,t)=1 (punto R=1 del Galileo sec 5.1), donde
el sistema pasa de disipativo (R<1, confinado) a expansivo (R>1). Misma estructura de
umbral que el a=4 de Collatz. El "2^phi de NS" seria la escala de Reynolds donde G*
se estabiliza (Re~50 en 2D, ver SDDF_NS2D). VER sec 5 (intentar b).

## 5. Scripts
- /tmp/test_triada.py, /tmp/test_M.py, /tmp/test_C.py, /tmp/r.py, /tmp/g.py
- /tmp/ns2d2.py, /tmp/ns3d2.py, /tmp/lema.py, /tmp/lema_fuerte.py
- /tmp/ns_phi.py (buscar escala dorada en NS, pendiente b)
