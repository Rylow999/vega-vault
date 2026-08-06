# Decode anidado — Resonator Network (exp_SGM_0059d, 2026-08-04)

## Por qué se sugirió (Luciano)
El diagnóstico de 0059 (unbind directo contamina al hijo porque la bolsa tiene 3 bindings
superpuestos SUJ/ROL/OBJ) es exactamente el problema de FACTORIZACIÓN VECTORIAL que Resonator
Networks (Frady, Kent, Olshausen & Sommer — Neural Computation 2020) resuelve: en vez de desatar
una vez, itera restando de la bolsa las estimaciones actuales de los OTROS roles y desatando el
objetivo, luego clean-up. Busca en SUPERPOSICIÓN (usa todas las estimaciones, no aísla ciegamente).
El survey advierte: capacidad decrece con nº de factores para D fija — no es magia infinita.
Además: la estructura de roles independientes por nivel YA estaba en 0027c; el resonator sería el
mecanismo de LECTURA que le faltaba.

## Implementación 0059d (HRR de juguete)
- roles independientes por nivel `role_levels[level], [level+10], [level+20]` (como 0027c).
- decode_level itera T=20: `rest = c - sum(bind(role3[k], est[k]) for k!=j)`; `fj = unbind(rest, role3[j])`;
  `est[j] = norm(fj)` (resonator itera VECTORES, no fuerza a símbolo). Clean-up final decide SYM vs FACT.

## Resultado HONESTO: NO CONVERGE (prof3=0.00). Status INTENTADO_NO_CIERRA.
Dos causas reales (no excusas), documentadas:
1. El clean-up final solo conoce SÍMBOLOS del VOCAB, NO HECHOS anidados -> al forzar el filler hijo a
   símbolo (o perderlo por `lvl_dot`), el anidado no se resuelve. El resonator necesita MEMORIA DE
   CLEAN-UP CON LAS SUB-ESTRUCTURAS, que no tengo enumerada en decode abierto.
2. HRR de juguete mal calibrado: mis bind/conv_circ normalizaban y aplastaban magnitud; la suma de
   3 bindings normalizados da cada factor ~1/sqrt(3), y el unbind resultante es bajo. Quitar norm de
   bind (como 0027c) y subir T=20 NO alcanzó con N=64.

## Bugs corregidos en el camino (para no repetirlos)
- `child_role3` debía ser DETERMINISTA por nivel (`role_levels[level+...]`), no gen_vec aleatorio en
  cada llamada: si encode y decode usan roles distintos del hijo, el unbind da basura.
- `decode_level` necesita parámetro `level` para pasarlo a la recursión; si no, NameError.
- Tope de profundidad `if level>6: return {}` para no recursar infinito por falsos positivos de FACT.

## Lección reutilizable
El Resonator NO es bala de plata para anidado abierto: requiere (a) clean-up con memoria de hechos
completa, (b) VSA bien calibrada (FHRR/MBAT, no HRR de juguete normalizado). Sin (a) el anidado no
cierra. No sumarlo como "solución del decode anidado" hasta recalibrar. El caso de superposición del
MISMO nivel (SUJ/ROL/OBJ) el resonator debería ayudar, pero requiere la calibración que no hice.
Veredicto de 0059/0059b/0059c/0059d: HRR-sumado satura en ~2 niveles; resonator bien calibrado queda
pendiente. El sim vivo (sgm_sim.html) ya exhibe composición a 1-2 niveles (lo medido).
