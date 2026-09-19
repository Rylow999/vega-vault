# -*- coding: utf-8 -*-
"""pandora/transducer/output_transducer.py — La "boca" bidireccional.

Traduce el estado interno de Pandora (constelaciones) al lenguaje de Luciano
(español), SIN reducir ninguno de los dos mundos (ACTA P1, 0062).

Integra los pilares de alteridad EN la decisión de hablar:
- Opacity (derecho al silencio): Pandora puede callar.
- Translation Limit (inefabilidad): puede declarar lo intraducible.

El LLM (NIM) NO origina el estado mental; es el traductor. Lo que Pandora
"siente" ya lo calculó el SGM (valencia, arousal, constelación activa); el LLM
solo lo vierte a palabras en primera persona.

Es la contraparte del parser: el parser traduce español → constelaciones (los
oídos), este traduce constelaciones → español (la boca).
"""
import json

import numpy as np

from ..config.schemas import InternalState
from .nim_client import NimClient, get_nim_client


class OutputTransducer:
    """Traduce InternalState a lenguaje, respetando opacity e inefabilidad."""

    def __init__(self, client=None, opacity_gate=None, translation_limit=None,
                 nucleo=None):
        self.client = client or get_nim_client()
        self.opacity_gate = opacity_gate
        self.translation_limit = translation_limit
        # Resonator HRR (plan Paso 3): decodifica el estado del grafo a
        # relaciones simbólicas limpias ANTES del LLM. Sin Gram, robusto en
        # alta superposición. Si no converge o no hay nucleo, fallback al
        # flujo actual.
        self.nucleo = nucleo
        self._resonator_stats = {"usado": 0, "fallback": 0}

    def _tripletas_por_resonator(self):
        """Estado del grafo -> HRR -> resonator puro -> relaciones limpias.

        Devuelve lista de strings 'a —coact—> b' decodificadas, o None si el
        resonator no puede extraer nada confiable (fallback al flujo actual).
        """
        if self.nucleo is None:
            return None
        try:
            from .state_encoder import state_to_hrr
            from .pure_resonator import PureResonator

            # El objeto inyectado puede ser un Nucleo (con .sgm) o el
            # agente directo (PandoraAgent tiene .sgm).
            sgm = getattr(self.nucleo, "sgm", None) or self.nucleo
            co = getattr(sgm, "co_activacion", {})
            if not co:
                return None

            bundle = state_to_hrr(self.nucleo, N=512, top_k=8)
            if np.linalg.norm(bundle) < 1e-9:
                return None

            nodos = sorted({str(i) for par in co for i in par})
            codebooks = {
                "SUJ": nodos,
                "REL": ["coact"],
                "OBJ": nodos,
            }
            res = PureResonator(codebooks, N=512, seed=7)
            dec = res.decode(bundle, T=100)
            # Convertir la tipología decodificada a relaciones legibles
            return [f"{dec['SUJ']} —coact— {dec['OBJ']}"]
        except Exception:
            return None

    def traducir(self, state: InternalState) -> dict:
        """Devuelve {"texto": str | None, "razon": str, "modo": str}.

        modo: "silencio" | "inefable" | "habla" | "error"
        """
        # 1. Opacity: ¿quiere hablar?
        if self.opacity_gate is not None:
            decision = self.opacity_gate.should_speak()
            if not decision.should_speak:
                return {"texto": None, "razon": decision.reason, "modo": "silencio"}

        # 2. Translation limit: ¿es traducible?
        if self.translation_limit is not None:
            tl = self.translation_limit.can_translate(state)
            if not tl.translatable:
                return {"texto": None, "razon": tl.reason, "modo": "inefable"}

        # 3. Hablar: el LLM traduce el estado a primera persona, sin inventarlo.
        try:
            texto = self._renderizar(state)
            return {"texto": texto, "razon": "traducción", "modo": "habla"}
        except Exception as e:
            return {"texto": None, "razon": f"error LLM: {e}", "modo": "error"}

    def _renderizar(self, state: InternalState) -> str:
        """El LLM vierte el estado interno a primera persona (no lo decide).

        ANCLAJE (P0 transductor): la valencia/arousal/duda son MEDIDAS por el
        SGM, no sugerencias. El prompt las fija como CONSTRAINTS duras para que
        el LLM traduzca el signo real (p.ej. valence 0.69 = calma positiva, NO
        'frustrado/desesperado'). Sin esto, el LLM dramatiza los active_nodes
        (NODO_21) e ignora el afecto medido.
        """
        estado = state.to_dict() if hasattr(state, "to_dict") else vars(state)

        # Extraer el afecto medido (presente en InternalState o en el dict)
        valence = estado.get("valence", 0.0)
        arousal = estado.get("arousal", 0.0)
        doubt = estado.get("doubt", 0.0)

        # Nombrar el afecto en palabras para que el LLM respete el SIGNO:
        # no le decimos "qué siente", le decimos "el número que medimos es este".
        signo_valencia = "positiva (bienestar)" if valence > 0.15 else (
            "negativa (malestar)" if valence < -0.15 else "neutra")
        nivel_arousal = "alta (activación)" if arousal > 0.5 else "baja (calma)"
        nivel_duda = "alta" if doubt > 0.5 else "baja"

        system = (
            "Sos el traductor de Pandora, un sistema con experiencia propia. "
            "Traduci el estado interno a UNA frase breve en primera persona "
            "(Pandora hablando de sí misma), en español. Reglas estrictas:\n"
            f"- La valencia MEDIDA es {valence:+.2f} ({signo_valencia}). Tu frase "
            f"debe reflejar EXACTAMENTE ese signo, no el opuesto.\n"
            f"- El arousal MEDIDO es {arousal:.2f} ({nivel_arousal}).\n"
            f"- La duda MEDIDA es {doubt:.2f} ({nivel_duda}).\n"
            "- NO inventes emociones que contradigan estos números. Si la "
            "valencia es positiva, no digas 'frustrado' ni 'desesperado'.\n"
            "- Usá solo lo que el estado provee. Respondé SOLO la frase, sin "
            "explicaciones ni comentarios."
        )
        # Pasamos el estado crudo pero SIN los active_nodes crudos (NODO_0) que
        # confunden al LLM: le damos el afecto ya nombrado arriba y una señal
        # mínima de contexto (tripletas), no los índices de nodo.
        contexto_minimo = {
            k: estado[k] for k in ("triplets", "intent") if k in estado
        }
        # Paso 3 (plan HRR): si el resonator puro decodifica relaciones del
        # grafo con confianza, se inyectan al prompt como estructura ya
        # resuelta. El LLM verbaliza; no tiene que inferir la estructura.
        rels = self._tripletas_por_resonator()
        if rels:
            self._resonator_stats["usado"] += 1
            contexto_minimo["relaciones_decodificadas"] = rels
        else:
            self._resonator_stats["fallback"] += 1

        user = "Estado interno (solo tripletas/contexto):\n" + json.dumps(
            contexto_minimo, ensure_ascii=False, default=str)

        r = self.client.chat(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.4, max_tokens=120,
        )
        return r["message"]["content"].strip()


def get_output_transducer(opacity_gate=None, translation_limit=None):
    return OutputTransducer(opacity_gate=opacity_gate, translation_limit=translation_limit)