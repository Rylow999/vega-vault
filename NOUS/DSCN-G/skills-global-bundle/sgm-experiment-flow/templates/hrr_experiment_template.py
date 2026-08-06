# -*- coding: utf-8 -*-
"""
TEMPLATE: experimento HRR (circular convolution/correlation, Plate 1995 / VSA survey Tabla 2).
Copiar y modificar para nuevos experimentos de binding/composicion en SGM.
Reusa las lecciones de 0027/0027b/0027c (ver references/hrr_binding_notes.md).

Requisitos antes de correr:
  - Debuguear bind/unbind a 1 nivel: cos(unbind(bind(A,B),A), B) > 0.5 (sale ~0.72).
  - Clean-up memory OBLIGATORIO tras cada unbind (coseno contra item memory).
  - Negative control honesto (unigram/loop-abierto/rand), NO "barajar filas".
  - Métrica de anidamiento: tasa de ACIERTO del clean-up (no coseno ni rank).
  - Anidamiento: usar roles INDEPENDIENTES por nivel (role_vecs[k]), NO cyclic shift del mismo rol.
"""
import math, random

SEED = 42
D = 128

def hrr_bind(a, b):
    """Circular convolution (a⋆b)[k] = Σ_i a[i]·b[(k−i) mod D]."""
    c = [0.0]*D
    for k in range(D):
        s = 0.0
        for i in range(D):
            s += a[i] * b[(k - i) % D]
        c[k] = s
    return c

def hrr_unbind(a, b):
    """Circular correlation (a⋆b)[k] = Σ_i a[i]·b[(i−k) mod D]. signo (i−k)."""
    c = [0.0]*D
    for k in range(D):
        s = 0.0
        for i in range(D):
            s += a[i] * b[(i - k) % D]
        c[k] = s
    return c

def rnd_unit(rng):
    v = [rng.gauss(0, 1) for _ in range(D)]
    n = math.sqrt(sum(x*x for x in v))
    return [x/n for x in v]

def cos(a, b):
    s = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a)); nb = math.sqrt(sum(x*x for x in b))
    return s/(na*nb) if na*nb > 0 else 0.0

def cleanup(vec, memory):
    """Clean-up: item de mayor coseno en la item memory (VSA survey p.10)."""
    best, bi = -2.0, -1
    for i, m in enumerate(memory):
        c = cos(vec, m)
        if c > best:
            best, bi = c, i
    return bi, best

# --- EJEMPLO: anidamiento orden N con roles independientes por nivel ---
def build_nested(op_idxs, role_vecs, mem):
    """R = Σ_k HRR(role_vecs[k], mem[idx_k]). Cada nivel usa rol INDEPENDIENTE."""
    acc = [0.0]*D
    for k, idx in enumerate(op_idxs):
        b = hrr_bind(role_vecs[k], mem[idx])
        acc = [acc[i] + b[i] for i in range(D)]
    return acc

def recover_nested(R, k, role_vecs, mem):
    rec = hrr_unbind(R, role_vecs[k])
    bi, _ = cleanup(rec, mem)        # clean-up obligatorio
    return bi, cos(rec, mem[k]) if False else None

if __name__ == "__main__":
    rng = random.Random(SEED)
    mem = [rnd_unit(rng) for _ in range(50)]
    role_vecs = [rnd_unit(rng) for _ in range(10)]
    A, B = mem[0], mem[1]
    # sanity check 1 nivel
    sc = cos(hrr_unbind(hrr_bind(A, B), A), B)
    print("1-nivel coseno (debe ser >0.5):", round(sc, 4))
    # anidamiento d=3
    idxs = [0, 1, 2]
    R = build_nested(idxs, role_vecs, mem)
    ok = all(recover_nested(R, k, role_vecs, mem)[0] == idxs[k] for k in range(3))
    print("anidamiento d=3 recupera todos:", ok)
