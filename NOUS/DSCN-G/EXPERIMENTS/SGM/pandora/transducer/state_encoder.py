# -*- coding: utf-8 -*-
"""pandora/transducer/state_encoder.py — Estado del grafo → vector HRR.

Empaqueta las top-k tripletas consolidadas del grafo (por co_activacion)
como un único vector HRR: para cada tripleta (suj, rel, obj) sumamos
bind(role_SUJ, sym_s) + bind(role_REL, sym_r) + bind(role_OBJ, sym_o).

Los símbolos se mapean a vectores gaussianos normalizados en R^N por hash
determinístico (sha1 del nombre como seed), así el mismo concepto da el
mismo vector en cualquier máquina y cualquier corrida.

Referencia: docs/PLAN_HRR_TRANSDUCTOR.md (Paso 1).
"""
import hashlib

import numpy as np

# Roles canónicos del bundle de estado (separados del CFG del paper FHRR:
# acá el rol es semántico del grafo, no sintáctico del experimento).
ROLES = ("SUJ", "REL", "OBJ")


def _sym_vec(nombre: str, N: int) -> np.ndarray:
    """Vector gaussiano normalizado determinístico para un nombre de nodo."""
    seed = int(hashlib.sha1(str(nombre).encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.RandomState(seed)
    v = rng.randn(N)
    return v / np.linalg.norm(v)


def hrr_bind(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Convolución circular (bind HRR real)."""
    return np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real


def state_to_hrr(nucleo, N: int = 512, top_k: int = 8) -> np.ndarray:
    """Empaqueta las top-k relaciones más co-activadas del grafo como HRR.

    nucleo: instancia de pandora.runtime.nucleo.Nucleo (o cualquier objeto
            con .sgm que tenga .co_activacion y .consolidadas).
    N : dimensionalidad del vector de salida.
    top_k : cuántas relaciones entran al bundle.

    Devuelve vector en R^N (ceros si el grafo aún no tiene relaciones).
    """
    sgm = nucleo.sgm
    co = getattr(sgm, "co_activacion", {})
    if not co:
        return np.zeros(N)

    # top-k pares más co-activados (claves son tuplas (a, b) de índices)
    top = sorted(co.items(), key=lambda kv: -kv[1])[:top_k]

    # Vectores-rol fijos por bundle (hash del nombre del rol)
    role_vecs = {r: _sym_vec(f"__role_{r}__", N) for r in ROLES}

    bundle = np.zeros(N)
    for (a, b), _w in top:
        s_a = _sym_vec(str(a), N)
        s_b = _sym_vec(str(b), N)
        # la relación se etiqueta por el propio par (co-activación)
        s_rel = _sym_vec(f"coact", N)
        bundle += hrr_bind(role_vecs["SUJ"], s_a)
        bundle += hrr_bind(role_vecs["REL"], s_rel)
        bundle += hrr_bind(role_vecs["OBJ"], s_b)
    return bundle
