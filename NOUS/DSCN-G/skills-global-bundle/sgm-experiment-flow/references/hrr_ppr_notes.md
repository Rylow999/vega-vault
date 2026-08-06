# HRR + PPR combined routing (exp_SGM_0027b)

Combinar binding HRR (0027) con ruteo PPR (0016/0019). Idea de Luciano: el PPR no camina de
nodo a nodo por identidad (ω crudo), sino por RELACIÓN. Cada nodo empaqueta sus relaciones en un
vector HRR; el PPR se sesga a un rol y navega caminos relacionales (q→a→b vía rol R) que el PPR
crudo no distingue.

## Setup
- `S_i = normalize( Σ_{(k,r) ∈ aristas(i)} HRR(role_vec[r], ω[k]) )`  # estado compuesto del nodo
- role_vecs: NROLES vectores unitarios gaussianos (ortogonales entre sí).
- HRR bind/unbind: ver hrr_binding_notes.md (signo (i−k) en unbind, clean-up obligatorio).

## PPR sesgado a rol (la parte que NO es obvia)
Peso de la arista (i→k, rol r) saliendo de i, con query sesgado a rol `bias`:
```
bm = hrr_bind(role_vec[bias], ω[k])
rm = cos(S_i, bm)              # alto si i tiene arista rol bias→k (el binding aparece en S_i)
base = max(0.0, rm)            # DOMINA la transición; NO multiplicar por cos(S_i, S_k)
```
P[i][k] ∝ base (normalized sobre vecinos de i). Power iteration estándar (α=0.15, ~60 iters).

## TRAMPAS (3 bugs reales de 0027b, corregidos antes de afirmar PASS)
1. **role_match enmascarado.** No usar `cos(HRR(rol_r,ω_k), HRR(rol_bias,ω_k))` — ambos convolucionados
   con el MISMO ω_k enmascara la diferencia de rol (role_vecs ortogonales → ambos ~0). Usar el estado
   compuesto `S_i` del nodo contra `HRR(rol_bias, ω_k)`.
2. **multiplicar en vez de dominar.** `base = cos(S_i,S_k) * role_match` mata el sesgo porque los estados
   compuestos S_i, S_k son casi ortogonales entre nodos conectados → coseno bajo. El role_match DEBE
   dominar: `base = role_match`.
3. **métrica rank no discrimina** en grafo chico/simétrico (empatan 3.0 vs 2.97). Usar **diferencia de
   masa estacionaria** `π[b] − π[d]`. HRR+R dio 0.256 vs 0.005 del PPR crudo ciego (50× más separación).

## Baseline honesto
El PPR "raw" (ω crudo, 0016) debe ser **ciego a roles** (bias=None, sin role_match). Si el raw también
lleva role_match, empata con HRR+R (falsa paridad) — no es baseline.

## Tests (con negative control)
- T-HPPR-01: sesgo R ubica b con diff masa b−d > 0 y > raw+margen(0.01).  (PASS: 0.256 vs 0.005)
- T-HPPR-02 (simetría): sesgo S ubica d con diff masa d−b > 0.              (PASS: 0.258)
- T-HPPR-NC: sin sesgo diff masa ≈ 0 (el rol es lo que ayuda, no ruido).  (PASS: 0.0)

## Grafo de prueba mínimo
q=0 → a=1 (R) → b=2 (R);  q=0 → c=3 (S) → d=4 (S);  distractores 5..24 con 2 aristas aleatorias.
N=25, D=128, NROLES=4, TRIALS=30, ALPHA=0.15, ITERS=60, seed=42.

## Conclusión honesta
HRR+PPR FUNCIONA: primera vez que SGM navega estructura relacional (no solo identidad de nodos).
El anidamiento profundo de bindings se resolvió en 0027c con **roles independientes por nivel**
(`role_vecs[k]`), NO cyclic shift (ver hrr_binding_notes.md: la correlación circular de shifts da
autocorrelación desplazada, no ruido ~0). Cierre del Gap 2 completo: 0027 (superposición) + 0027b
(ruteo relacional) + 0027c (anidamiento orden N).
