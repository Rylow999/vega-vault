# -*- coding: utf-8 -*-
"""pandora/transducer/pure_resonator.py — Decoder resonator SIN Gram.

Implementa el decoder que el paper FHRR demuestra robusto en todo el grid
de rho (incluida la anti-resonancia en rho=1): resonador iterativo sin
corrección de Gram. Dado un vector bundle y los codebooks por rol,
recupera los fillers.

Referencia: docs/PLAN_HRR_TRANSDUCTOR.md (Paso 2) y
FHRR-HRO-COLLAPSE/src/exp_observer_taxonomy_v3.py (BundleV3).
"""
import numpy as np

from .state_encoder import ROLES, _sym_vec, hrr_bind


def hrr_unbind(c: np.ndarray, r: np.ndarray) -> np.ndarray:
    """Correlación circular (unbind HRR real)."""
    return np.fft.ifft(np.fft.fft(c) * np.conj(np.fft.fft(r))).real


class PureResonator:
    """Resonador puro: N roles → N estimaciones iterativas con cleanup.

    codebooks: dict rol -> lista de símbolos candidatos (nombres de nodo).
    N: dimensionalidad del bundle (debe coincidir con la del encoder).
    """

    def __init__(self, codebooks: dict, N: int = 512, seed: int = 7):
        self.codebooks = {r: list(syms) for r, syms in codebooks.items()}
        self.N = N
        self.np_rng = np.random.RandomState(seed)
        self.role_vec = {r: _sym_vec(f"__role_{r}__", N) for r in self.codebooks}
        self.sym_vec = {
            s: _sym_vec(s, N)
            for syms in self.codebooks.values() for s in syms
        }
        # arrays para cleanup rápido
        self.cb_names = self.codebooks
        self.cb_arr = {
            r: np.array([self.sym_vec[s] for s in syms])
            for r, syms in self.codebooks.items()
        }

    def _cleanup(self, v: np.ndarray, rol: str) -> str:
        CB = self.cb_arr[rol]
        n = np.linalg.norm(v)
        if n == 0:
            return self.cb_names[rol][0]
        sims = (CB @ v) / (np.linalg.norm(CB, axis=1) * n)
        return self.cb_names[rol][int(np.argmax(sims))]

    def decode(self, bundle: np.ndarray, T: int = 100) -> dict:
        """Resonador iterativo. Devuelve dict rol -> símbolo."""
        roles = list(self.codebooks.keys())
        est = []
        for _r in roles:
            v = self.np_rng.randn(self.N)
            est.append(v / np.linalg.norm(v))
        for _ in range(T):
            new = []
            for i, rol in enumerate(roles):
                others = bundle.copy()
                for j in range(len(roles)):
                    if j != i:
                        others = others - hrr_bind(self.role_vec[roles[j]], est[j])
                cand = hrr_unbind(others, self.role_vec[rol])
                # SIN Gram: cleanup directo (el hallazgo del paper)
                new.append(self.sym_vec[self._cleanup(cand, rol)])
            est = new
        return {rol: self._cleanup(est[i], rol) for i, rol in enumerate(roles)}
