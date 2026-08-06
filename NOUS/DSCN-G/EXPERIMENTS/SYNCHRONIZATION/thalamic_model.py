#!/usr/bin/env python3
"""
thalamic_model.py — Ronda 5: privilegio estructural del root ("hub
talámico"), FIX del bug de Ronda 4.

Contexto (ver AUDIT_NOTES_ROUND5.md): en el primer intento de Ronda 5 se
le dio al root un `hub_boost` multiplicando su fila/columna en la matriz
de acoplamiento de Kuramoto basal (`_apply_kuramoto_coupling`). Resultado:
no cambió nada (T1 con boost ≈ T1 sin boost, ver
`c3_redesign_results.json` vs los números "Thalamic" de esta ronda antes
del fix). Motivo: el mecanismo que realmente domina la dinámica del root
durante el hijack es `_apply_hijack_pull` — un tirón directo hacia la
fase del root, separado de la matriz de Kuramoto y NO modulado por ella.
Reforzar la conexión equivocada no tiene efecto observable.

FIX: `hub_boost` ahora escala `eta_hijack` dentro de `_apply_hijack_pull`
(con un tope duro en 1.0 — más allá de eso el update per-paso ya no tiene
sentido físico como "paso hacia la fase del root", se vuelve un salto).
El resto del modelo (Kuramoto basal, homeostasis T1, alineación T2) queda
exactamente igual que `DSCN_G_v3` — se hereda sin tocar `verify_dscng_v3.py`,
siguiendo la misma convención que `verify_maximality_real.py` /
`verify_c3_redesign.py` / `verify_phi_proxy.py` de Ronda 4: el núcleo no
se modifica, todo lo nuevo son subclases/scripts que lo importan.

hub_boost=1.0 debe reproducir DSCN_G_v3 byte-a-byte (mismo eta_hijack
efectivo) — se verifica al final del módulo como smoke test.
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from verify_dscng_v3 import DSCN_G_v3, DEFAULTS  # noqa: E402


class ThalamicDSCN_G_v3(DSCN_G_v3):
    """DSCN_G_v3 + privilegio estructural del root durante el hijack.

    hub_boost: multiplicador de eta_hijack aplicado SOLO dentro de
    _apply_hijack_pull (el mecanismo que de verdad conduce la dinámica
    del hijack). Efectivo = min(1.0, eta_hijack * hub_boost).
    """

    def __init__(self, *, hub_boost: float = 1.0, **kw):
        super().__init__(**kw)
        self.hub_boost = hub_boost

    def _apply_hijack_pull(self):
        if len(self.nodes_active) < 2:
            return
        root = self.nodes_active[0]
        eta_eff = min(1.0, self.eta_hijack * self.hub_boost)
        for i in self.nodes_active[1:]:
            delta_phi = np.sin(self.phi[root] - self.phi[i])
            self.phi[i] = (self.phi[i] + eta_eff * delta_phi) % (2 * np.pi)


if __name__ == "__main__":
    # Smoke test: hub_boost=1.0 debe coincidir exactamente con DSCN_G_v3
    # (misma seed, misma trayectoria) — si esto falla, el fix rompió algo.
    a = DSCN_G_v3(seed=0, N=50, steps=None) if False else DSCN_G_v3(seed=0, N=50)
    b = ThalamicDSCN_G_v3(seed=0, N=50, hub_boost=1.0)
    for _ in range(300):
        a.step()
        b.step()
    same_phi = np.allclose(a.phi, b.phi)
    same_active = a.nodes_active == b.nodes_active
    print(f"hub_boost=1.0 == DSCN_G_v3 (300 steps, seed=0): "
          f"phi {'✓' if same_phi else '✗'}  nodes_active {'✓' if same_active else '✗'}")
    assert same_phi and same_active, "FIX ROTO: hub_boost=1.0 debe ser idéntico al núcleo"
    print("Smoke test OK.")
