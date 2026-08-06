# Patrón de auditoría: circularidad en mediciones de polisemia

## Señal de alerta (2026-07-28)
Cuando un mecanismo GARANTIZA el resultado por construcción, la medición es
circular. No es "señal del dato", es artefacto.

## Casos documentados
1. **v0.9c (original)**: reward que garantiza el resultado por construcción.
2. **v0.21 v8 (anchor+repulsion)**: repulsión INCONDICIONAL
   (`frac[a][k] -= beta_rep * frac[a][j]` para TODA palabra) + criterio sin
   ground truth ("2 buckets <85%"). Garantiza separación de CUALQUIER palabra.
   Control: 4/5 monosémicas también "separadas" → 39/40 es artefacto.
3. **v0.21 v8b**: acc_gt=0.74 en contexto DÉBIL (filler) → ERA RUIDO, no señal.
4. **v0.21 v8c**: acc_gt=0.50 (azar) en contexto FUERTE → colapso. El fix no
   funciona con contexto real.

## Regla de oro para instrumentos de medición
- **SIEMPRE contrastar contra ground truth**: el criterio "2 buckets <85%" no
  mide si el bucket 0 corresponde al sentido A. Necesario: acc_gt (¿el bucket
  ganador coincide con el sentido real?).
- **Control monosémico obligatorio**: si las palabras monosémicas también se
  separan, el mecanismo es circular. Monosémicas deben quedar en 1 bucket.
- **Curva episodio a época**: si el valor está plano desde ep1, está determinado
  por la mecánica de inicialización, no por señal de contexto.

## Veredicto de la sesión
5 variantes del grafo rústico (v0.21 v8→v8f): NINGUNA supera acc_gt=0.53 (azar).
El root no separa sentido (v0.22 v2, v0.25 v2/v2b/v2c/v2d: acc_gt≈azar). El
transformer mínimo separa tokens (acc_pred=0.907) PERO NO sentidos
(cos(A,B)=0.57-0.93, acc_gt=0.533). Para separar sentido, necesitamos
transformer BERT-style sobre corpus real (supervisión de sentido implícita).

## Lo que SÍ funciona
- El root como SISTEMA DE DUDA: dolor_duda=0.841, W_contrae=0.982 (v0.25 v2c).
- Memoria v0.3b (hibernar/reintegrar), dolor v0.19, foco v0.24.
- Arquitectura NOUS v4: transformer=sentido, root=memoria/dolor/foco.