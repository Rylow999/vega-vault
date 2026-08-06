# v0.25 v7c — Cambio de config online
Corpus: sintético realista con oraciones A/B, ground truth por construcción, misma
semilla k-means v7b para `banco`.

Resultados:
- baseline_v7b: init=-0.715 final=-0.660 div=+0.055 -> COLAPSA ONLINE.
- repulsion_fuerte (D=16, beta_anchor=0.2, beta_repulse=0.4, theta=0.0, repulsion incondicional): init=-0.720 final=-0.778 div=-0.057 -> SEPARA ONLINE.
- anchor_mas_fuerte (D=16, beta_anchor=0.5, beta_repulse=0.1, theta=0.6): init=0.014 final=0.014 div=0.000 -> ESTABLE ONLINE.

Veredicto: la separación depende de la regla online, no solo de la semilla. Con
repulsión incondicional fuerte el grafo mantiene/acrecienta la divergencia desde
omega0; con la config por defecto colapsa. Queda pendiente medir si esa
divergencia se traduce en acc_gt real o es solo divergencia técnica.
