# Resonator Networks para Decode Anidado (exp_SGM_0059d / 0059e / 0059f, 2026-08-04)

## Contexto
El decode anidado de SGM satura en ~2 niveles con HRR-sumado (0059/59b/59c). Luciano trajo
Resonator Networks (Frady, Kent, Olshausen & Sommer — Neural Computation 2020; survey activo 2025)
como el mecanismo de lectura que le faltaba a la estructura de roles-por-nivel de 0027c. El problema
documentado ("unbind contamina al hijo al desatar") es exactamente la factorización vectorial que el
resonator resuelve con dinámica no lineal + búsqueda en superposición.

## Lo que SÍ funciona (receta canónica, Frady 2020 Algorithm 1)
- **Usar FHRR (Fourier HRR), NO HRR de convolución circular.** Binding = producto complejo
  `bind(a,b)[i] = a[i]*b[i]` (suma de fases EXACTA, sin ruido de convolución). Unbind = `c[i]*r[i].conjugate()`.
- **Codebooks por rol** (SUJ/ROL/OBJ con vocab distinto). Cada factor tiene su matriz de codewords K_i×N.
- **Matriz de capacidad M_i y su INVERSA** (OBLIGATORIA — ver Pitfall): `M_i = (1/K) Σ_c c·c*`,
  invertida por Gauss-Jordan en puro Python (N×N; N=64 manejable, N=128 lento pero una vez por codebook).
- **Actualización canónica (Jacobi, todos los factores en paralelo):**
  `a_i = M_i^{-1} · unbind( z − Σ_{j≠i} bind(V_j, x_j), V_i )`
  `x_i = clean_i(a_i)`   (proyecta al codeword más cercano del codebook i por coseno de vectores complejos)
- **Clean-up contra memoria COMPLETA** (símbolos + vectores de hechos generados) para resolver el anidado:
  el filler recuperado de un rol se limpia contra TODOS los codewords; si matchea un hecho de memoria
  (sim > símbolo y > umbral) → es FACT y se recurre sobre ese hecho.

## PITFALLO CRÍTICO (costó 0059e: colapso a atractor espurio)
Sin `M_i^{-1}`, el resonator itera vectores pero TODOS los roles convergen al MISMO símbolo dominante
(ej. devolvió "lobo" para SUJ/ROL/OBJ). La matriz de capacidad corrige la distorsión de magnitud/dirección
que introduce la superposición de 3+ bindings. **El `M_i^{-1}` NO es opcional de tuning: es parte del
algoritmo canónico.** Con `M_i^{-1}`, prof3 subió de 0.04 → 0.28 (el colapso desaparece).

## Resultados honestos (0059d HRR / 0059e FHRR casero / 0059f FHRR canónico)
- 0059d (resonator sobre HRR convolucional): no converge (HRR frágil). prof3=0.00.
- 0059e (resonator sobre FHRR, mi versión sin M_i^{-1}): colapsa a atractor espurio. prof3=0.04.
- 0059f (resonator CANÓNICO con M_i^{-1}, codebooks por rol, clean-up memoria completa):
  - N=64: prof3/4/5/6 = 0.28 / 0.17 / 0.11 / 0.11
  - N=128: prof3/4/5/6 = 0.08 / 0.25 / 0.08 / 0.17 (ruidoso, n=4)
  - **Subir N NO ayuda.**

## VEREDICTO (confirmado empíricamente, no por fe)
El decode anidado en SGM con VSA-SUMADO (HRR o FHRR, con o sin resonator) **SATURA en ~2-3 niveles de
anidado**. No es un bug del decoder: es capacidad del sustrato vectorial de superposición. El resonator
canónico es buena herramienta para el NIVEL BASE (~1-2 niveles; como 0059 HRR N=256 llegó a 0.90 a prof2),
pero NO rompe el techo de anidado profundo abierto. Confirma exactamente el survey Frady 2020/2025:
*la capacidad del VSA-sumado decrece con el número de factores*. El resonator mejora el nivel base pero
no rompe el techo.

**La solución real para >2 niveles es NO sumar los bindings en un bundle:** role-filler con slots o
punteros SEPARADOS (no superpuestos), o la estructura de 0027c (roles independientes por nivel en CADENA,
no bundle de 3 roles de hecho + hecho anidado en una sola bolsa). Es el camino de role-filler que quedó
pendiente de decisión de Luciano. El sustrato SGM YA tiene la maquinaria (0027c anida por niveles, 0058
compone relacional); el cuello es la codificación vectorial SUMADA, no el sustrato.

## Regla de disciplina (reforzada por esta sesión)
Al tunear un mecanismo de representación que no escala: tras 3-4 variantes del MISMO mecanismo
(HRR → TPR-walk → resonator-HRR → resonator-FHRR → resonator-canónico), DETENER y diagnosticar la RAÍZ.
Aquí la raíz es capacidad de VSA-sumado, no el decoder. Cerrar con veredicto honesto; no seguir variantes.
El resonator canónico fue la última variante legítima (aporta al nivel base); lo demás ya era repetir.

## Archivos
- `phases/phase7_composicion/run_decode_0059f.py` — Resonator canónico Frady 2020 sobre FHRR (N=64/128,
  codebooks por rol, M_i^{-1} por Gauss-Jordan, clean-up memoria completa). Referencia de implementación.
- `run_decode_0059d.py` (HRR, no converge) y `run_decode_0059e.py` (FHRR sin M_i^{-1}, colapsa) quedan como
  negativos documentados.
