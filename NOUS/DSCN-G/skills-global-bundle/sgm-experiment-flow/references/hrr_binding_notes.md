# HRR Binding — notas reproducidas (exp_SGM_0027)

Fuente canónica confirmada en `lit/papers/vsa_survey_2022_2111.06077.pdf`, Tabla 2 (p.10):
**HRR [Plate, 1995a]** | Binding = circular convolution | Unbinding = circular correlation |
Superposition = component-wise | Similarity = coseno.

## Fórmulas (D = dimensión, índices mod D)
- bind(a,b)[k] = Σ_i a[i] · b[(k − i) mod D]
- unbind(a,b)[k] = Σ_i a[i] · b[(i − k) mod D]   ← signo (i−k), NO (i+k)
- HVs atómicos: vectores gaussianos normalizados por norma (unit vectors).

## Checklist antes de correr cualquier experimento HRR
1. Debug a 1 nivel: `cos(unbind(bind(A,B), A), B)` debe ser > 0.5 (sale ~0.72 con gaussianos;
   es ruidoso pero no roto). Si da ~0.06 → el signo del unbind está al revés.
2. Clean-up OBLIGATORIO tras cada unbind: reemplazar el vector recuperado por el item más similar
   (coseno) en la item memory. Sin clean-up, anidamiento profundo da ~0 aunque el bind esté bien.
3. Al comparar contra XOR/spatter: la superposición de N bindings binarios (±1) da S ∈ [−N, N];
   tomar `sign(S)` antes del unbind XOR. HRR opera en continuo, correlación directa (sin sign).

## Diseño de tests (T-REL) con negative control
- T-REL-01 anidamiento: R = bind(A1, bind(A2, … bind(Ad-1, Ad)…)); recuperar Ad por unbind en
  cadena CON clean-up en cada paso. Medir coseno vs profundidad. (En 0027 ambos HRR/XOR ~0:
  anidamiento profundo sigue siendo problema abierto → requiere cyclic shift/permutaciones.)
- T-REL-02 superposición: S = Σ_i bind(Xi,Yi); recuperar Yi = unbind(S,Xi)+clean-up; tasa de
  acierto vs k. HRR [1.0,1.0,0.875,0.525] vs XOR [0.467,0.533,0.467,0.263] a k=[2,4,8,16].
  HRR aguanta el doble de relaciones superpuestas — variable que discrimina.
- T-REL-03 NC: vectores aleatorios no-relacionados → coseno ~0 (señal no es ruido del operador).

## Negative control que NO usar
"Barajar filas de matriz" no sirve: mantiene frecuencias marginales y da falsos positivos
(0.029 vs azar 0.0025 en 0026). Usar modelo sin la propiedad (unigram / loop abierto / rand).

## Resultado 0027 (honesto)
HRR supera XOR en superposición (k=16: 0.525 vs 0.263, ~2x). Anidamiento profundo falla en ambos.
Gap 2 de binding parcialmente cerrado; el siguiente paso propuesto es HRR+PPR (0027-b).

## Anidamiento orden N (exp_SGM_0027c — CIERRA Gap 2)
El anidamiento plano falla porque `unbind(unbind(R,A),B)` da un intermediate que NO es item de
memoria → crosstalk se acumula y la cadena se rompe a profundidad ≥3.
- **Solución: rol INDEPENDIENTE por nivel**, `role_vecs[k]` (vector ortogonal), NO cyclic shift del mismo rol.
  - Cyclic shift del mismo rol: correlación circular de dos shifts = AUTOCORRELACIÓN DESPLAZADA
    (pico en 0, colas ~1/√D), NO ruido ~0 → los niveles NO se aíslan → anidamiento ~0.
  - Roles independientes: `rol_j ⋆_corr rol_k ≈ 0` para j≠k → cada nivel en su canal → clean-up 1.0 a d=5.
- **Métrica = TASA DE ACIERTO del clean-up** (¿recuperó el item correcto? Sí/No), NO coseno promedio
  (dio 0.41, ambiguo) ni rank. Resultado HRR+roles [1.0,1.0,1.0,1.0] a d={2,3,4,5}; XOR y HRR planos
  [0.5,0.33,0.25,0.2] (azar entre 5 items). Esa es la variable que dice "resuelto".
- NC (0027c): R con vectores aleatorios no-relacionados → coseno 0.006.
