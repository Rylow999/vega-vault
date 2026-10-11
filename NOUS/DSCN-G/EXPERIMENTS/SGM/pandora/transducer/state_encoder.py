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
    N : dimensionalidad del vector HRR del bundle. INDEPENDIENTE del
        D del SGM (el grafo corre con D=128 internamente; el bundle de la
        boca es su propia capa FHRR). No confundir: 512 = espacio de
        consulta del transductor, 128 = espacio de estados del grafo.
    top_k : cuántas relaciones entran al bundle.

    Devuelve vector en R^N (ceros si el grafo aún no tiene relaciones).
    """
    sgm = nucleo.sgm
    co = getattr(sgm, "co_activacion", {})
    if not co:
        return np.zeros(N)

    # top-k pares más co-activados
    # FIX (2026-10-11): las claves llegan como STRING "(a, b)" tras la
    # serialización del checkpoint (np.save de un dict con tuplas), no
    # como tuplas. El unpack `for (a, b), _w in top` crasheaba
    # silenciosamente en el try/except de la boca => el resonator NUNCA
    # corrió con datos reales. Parseo robusto de ambos formatos:
    import ast as _ast

    def _parse_key(k):
        """Clave de co_activacion -> (a, b) sea tupla o string serializada."""
        if isinstance(k, tuple) and len(k) == 2:
            return k
        if isinstance(k, str):
            try:
                t = _ast.literal_eval(k)
                if isinstance(t, tuple) and len(t) == 2:
                    return t
            except (ValueError, SyntaxError):
                pass
        # fallback: no es un par parseable -> None (se salta)
        return None

    # FIX 2 (2026-10-11, medido contra el grafo real): dedup de pares espejo.
    # La co-activacion es SIMETRICA: (a,b) y (b,a) tienen el mismo peso y
    # entraban AMBOS al top-k => mitad de relaciones reales + interferencia.
    # Regla: un par entra una sola vez (orden canónico a<=b); el peso es el
    # maximo de sus dos espejos.
    top = []
    vistos = set()
    for k, w in sorted(co.items(), key=lambda kv: -kv[1]):
        par = _parse_key(k)
        if par is None:
            continue
        canon = tuple(sorted(par))
        if canon in vistos:
            # actualizar peso al maximo de espejos (por si difieren)
            for i, (pp, ww) in enumerate(top):
                if pp == canon:
                    top[i] = (pp, max(ww, w))
                    break
            continue
        vistos.add(canon)
        top.append((canon, w))
        if len(top) >= top_k:
            break

    # FIX 3 (2026-10-11, medido): el bundle anterior sumaba 3 binds por par
    # con peso IGUAL (24 terminos para top-8): unbind(SUJ) dejaba el real en
    # rango 4/6462 con sim 0.154 (NO top-1). Ponderar por la fuerza de la
    # co-activacion (normalizada al max del top) para que las relaciones
    # dominantes pesen mas que el ruido de las debiles:
    w_max = max((w for _, w in top), default=1.0)

    # Vectores-rol fijos por bundle (hash del nombre del rol)
    role_vecs = {r: _sym_vec(f"__role_{r}__", N) for r in ROLES}
    s_rel = _sym_vec("coact", N)

    bundle = np.zeros(N)
    for (a, b), w in top:
        s_a = _sym_vec(str(a), N)
        s_b = _sym_vec(str(b), N)
        # la relacion se etiqueta por el propio par (co-activacion)
        pw = w / w_max if w_max > 0 else 1.0
        bundle += pw * hrr_bind(role_vecs["SUJ"], s_a)
        bundle += pw * hrr_bind(role_vecs["OBJ"], s_b)
    # el termino REL va UNA sola vez (identico para todos: era 8x la misma
    # senal saturando el bundle — ahora es una marca constante limpia)
    bundle += 0.25 * hrr_bind(role_vecs["REL"], s_rel)
    return bundle
