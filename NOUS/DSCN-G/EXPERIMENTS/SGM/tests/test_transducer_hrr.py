# -*- coding: utf-8 -*-
"""tests/test_transducer_hrr.py — Guardián del plan HRR (Pasos 1-3)."""
import random

import numpy as np

from pandora.transducer.state_encoder import state_to_hrr, hrr_bind, _sym_vec, ROLES
from pandora.transducer.pure_resonator import PureResonator
from sgm.core.sgm_core import SGMAgentCore
from pandora.runtime.nucleo import Nucleo


class _StubSGM:
    def __init__(self):
        self.consolidadas = {(0, 1), (2, 3), (4, 5)}
        self.co_activacion = {(0, 1): 10, (2, 3): 8, (4, 5): 5}


class _StubNucleo:
    def __init__(self):
        self.sgm = _StubSGM()


def test_state_to_hrr_ceros_si_no_hay_relaciones():
    class Vacio:
        co_activacion = {}
        consolidadas = set()
    class N:
        sgm = Vacio()
    v = state_to_hrr(N(), N=128)
    assert np.allclose(v, 0)


def test_state_to_hrr_no_cero_con_actividad():
    v = state_to_hrr(_StubNucleo(), N=128)
    assert np.linalg.norm(v) > 0


def test_roundtrip_encoder_resonator():
    N = 512
    nodos = ["0", "1", "2", "3", "4", "5"]
    codebooks = {"SUJ": nodos[:3], "REL": ["coact"], "OBJ": nodos[3:]}
    res = PureResonator(codebooks, N=N, seed=7)
    bundle = (hrr_bind(_sym_vec("__role_SUJ__", N), _sym_vec("0", N))
              + hrr_bind(_sym_vec("__role_REL__", N), _sym_vec("coact", N))
              + hrr_bind(_sym_vec("__role_OBJ__", N), _sym_vec("3", N)))
    dec = res.decode(bundle, T=150)
    assert dec["SUJ"] == "0"
    assert dec["REL"] == "coact"
    assert dec["OBJ"] == "3"


def test_integracion_nucleo_real(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sgm = SGMAgentCore(random.Random(42), D=32, n_nodes=8, gamma=0.01)
    sgm.set_edges({i: random.Random(i).sample(range(8), 3) for i in range(8)})

    class _AgenteMin:
        def __init__(self, sgm):
            self.sgm = sgm

    from pandora.runtime.estado import EstadoVivo
    estado = EstadoVivo(base_dir=str(tmp_path))
    nucleo = Nucleo(estado, _AgenteMin(sgm))
    sgm.co_activacion[(0, 1)] = 5
    sgm.co_activacion[(2, 3)] = 3
    v = state_to_hrr(nucleo, N=128)
    assert isinstance(v, np.ndarray)
    assert v.shape == (128,)
    assert np.linalg.norm(v) > 0


def test_paso3_resonator_en_transductor(tmp_path, monkeypatch):
    """Paso 3: el transductor con nucleo usa el resonator y lo anota."""
    from pandora.transducer.output_transducer import OutputTransducer
    monkeypatch.chdir(tmp_path)
    sgm = SGMAgentCore(random.Random(42), D=32, n_nodes=8, gamma=0.01)
    sgm.set_edges({i: random.Random(i).sample(range(8), 3) for i in range(8)})

    class _AgenteMin:
        def __init__(self, sgm):
            self.sgm = sgm

    from pandora.runtime.estado import EstadoVivo
    estado = EstadoVivo(base_dir=str(tmp_path))
    nucleo = Nucleo(estado, _AgenteMin(sgm))
    sgm.co_activacion[(0, 1)] = 9
    sgm.co_activacion[(2, 3)] = 7
    sgm.co_activacion[(4, 5)] = 4

    t = OutputTransducer(client=None, nucleo=nucleo)
    rels = t._tripletas_por_resonator()
    # Debe devolver la lista con la relación decodificada (o None si no llega,
    # pero con 3 pares fuertes a N=512 el resonator converge)
    assert rels is not None
    assert any("coact" in r for r in rels)


def test_paso3_sin_nucleo_fallback():
    """Sin nucleo, el resonator no se usa y no rompe nada."""
    from pandora.transducer.output_transducer import OutputTransducer
    t = OutputTransducer(client=None, nucleo=None)
    assert t._tripletas_por_resonator() is None
    assert t._resonator_stats == {"usado": 0, "fallback": 0}
