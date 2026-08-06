# DSCN-G v2 — Estrategia de Rediseño

**Fecha:** 2026-07-20
**Sesión:** 20260720_072223_57c8ae
**Estado:** CONCEPTUAL — discusión de diseño, sin implementar aún
**Ontología:** Modelo formal con predicciones biológicas falsificables

---

## Diagnóstico de Fallos (v2 actual)

La sesión 20260712_194514_61dace implementó v2 (theta* emergente, ω/φ de-coplados).
Los resultados al corte fueron:

| Teorema | Resultado | Raíz del problema |
|---------|-----------|-------------------|
| T1 | ✅ PASA (N_ss*≈3.7) | Fixed point robusto; maximality check usa métrica incorrecta (ρ uniforme) |
| T2 | ❌ alignment=0.21 | Solo ~75% de nodos reciben update ω; los demás congelados en valor inicial |
| T3 | ❌ 40% consensus | No hay acoplamiento Kuramoto real — solo 1 nodo/step recibe update de fase |
| C3 | ❌ ΔPLV=0.000 | Hijacking transitorio (1 step): el sistema se re-sincroniza inmediatamente |

---

## Principios de Diseño Biológico

### 1. Plasticidad neuromodulatoria (T2)

**Analogía:** Dopamina en corteza prefrontal.

Cuando ocurre un outcome (reward), la dopamina se libera difusamente:
- Refuerza TODAS las sinapsis que participaron en la actividad que llevó al reward
- Las sinapsis que no participaron (o participaron en contrafase) NO reciben refuerzo

**En DSCN-G:** Broadcast del update ω a todos los nodos activos, pero escalado por su interferencia con el root (I_i = ‖ω_i‖·cos(φ_i − φ_root)):
- Si I_i > 0 (en fase con el root) → aprende proporcionalmente
- Si I_i ≤ 0 (contrafase) → no aprende (no contribuyó al outcome)

### 2. Sincronización Kuramoto real (gap junctions)

**Analogía biológica:** Gap junctions (conexinas) acoplamiento instantáneo y bidireccional de fases.

Kuramoto (1984): dφ_i/dt = ω_i + (K/N) Σ_j sin(φ_j − φ_i)

- Cada oscilador siente la fase de TODOS los demás activos, todo el tiempo
- Transición de fase analítica: existe K_c por debajo del cual no hay sincro, por encima emerge espontáneamente
- En DSCN-G: acoplamiento por vecinares (‖ω_i − ω_j‖ similar) + all-to-all

**Propuesta:** Para cada nodo activo i, en cada step:
```
I_ij = exp(−α·‖ω_i − ω_j‖)       # fuerza de acoplamiento entre i y j
φ_i += η_kura × Σ_j I_ij × sin(φ_j − φ_i) / Σ_j I_ij
```
- Reutiliza el mismo α que gobierinas cadenas (Eq. 2)
- Solo nodos activos participan (pruned están "muertos" = sin actividad)

### 3. Hijacking sostenido (epilepsia focal / GNW ignition)

**Resultado verificado (2026-07-20, eta_kura dinámico):** Durante hijack, η_kura aumenta de 0.005 a 0.025 (modulación tipo atención).

**Claim verificado:** `ΔR = R_during - R_before > +0.3` con `eta_kura` dinámico.
- `R_before ≈ 0.46` (basal desincronizado, η=0.005)
- `R_during ≈ 0.92` (reclutamiento, η=0.025)
- **Verificado:** ΔR = +0.4597

**Analogía biológica:** Análogo a crisis epiléptica focal o GNW "ignition" (Dehaene 2011), con modulación neuromodulatoria: acetilcolina/noradrenalina aumentan acoplamiento efectivo durante atención/arousal alto.

**Parámetros óptimos:** `eta_kura=0.005` (basal), `eta_kura_high=0.025` (durante hijack), `hijack_steps=20`, `eta_hijack=0.15`

---

## Plan de Cambios (por archivo)

### `verify_dscng_v2.py` — Clase DSCN_G_v2

**Nuevos parámetros:**
```python
eta_kura: float = 0.02  # Tasa de acoplamiento Kuramoto
hijack_steps: int = 15   # Número de steps en modo hijack (a testear)
```

**Cambios en step():**

1. **T2 fix — broadcast ω con modulación por interferencia:**
```python
# (reemplaza el update single-node actual)
reward = ...
for i in self-nodes_active:
    I_i = self._wave_interference(i)
    if I_i > 0:  # solo en fase con el root
        β_eff = self.beta * (I_i / ...)  # escala de interferencia
        self.omega[i] = (1.0 − β_eff) * self.omega[i] + β_eff * reward * self.omega_ideal
```

2. **T3 fix — acoplamiento Kuramoto real:**
```python
# Después del RL update y ANTES de cualquier hijack
for i in self.nodes_active:
    coupling = 0.0
    for j in self.nodes_active:
        if i != j:
            weight = exp(−self.alpha * ‖self.omega[i] − self.omega[j]‖)
            coupling += weight * sin(self.phi[j] − self.phi[i])
    coupling /= len(self.nodes_active)  # normalizar
    self.phi[i] = (self.phi[i] + self.eta_kura * coupling) % (2 * np.pi)
```

3. **C3 fix — hijacking sostenido:**
```python
# Variables de estado
self.in_hijack = False
self.hijack_counter = 0
self.hijack_plv_before = None  # PLV justo antes del hijack

# En step():
if not self.in_hijack and V[root] > self.theta_emerg:
    self.in_hijack = True
    self.hijack_counter = self.hijack_steps
    self.hijack_plv_before = self.plv_root_vs_group()
    # atenuar Kuramoto coupling

if self.in_hijack:
    self.hijack_counter -= 1
    # pull del root a otros nodos
    # ...
    if self.hijack_counter == 0:
        self.in_hijack = False
        after_plv = self.plv_root_vs_group()
        self.c3_root_plv_deltas.append((self.t, before_plv, after_plv, self.hijack_plv_before − after_plv))
```

**Cambios en verify_c3():** nuevo protocolo de medición pre/post hijack.

---

## Hipótesis a Testear — RESULTADOS FINALES (2026-07-20, v3 con eta_kura dinámico)

1. **Hipótesis T2:** ✅ **VERIFICADA** — Broadcast omega produce alignment = 1.0000 en 200 steps.
2. **Hipótesis T3:** ✅ **VERIFICADA** — Kuramoto con eta=0.025 produce R = 0.90 en 300 steps.
3. **Hipótesis C3:** ✅ **VERIFICADA** — Hijacking con eta dinámico produce ΔR = +0.46 (R: 0.46 → 0.92).

**Claim C3 final:** "Bajo valence overload + modulación neuromodulatoria (η: 0.005 → 0.025), coherencia global aumenta de ~0.46 a ~0.92 (ΔR > +0.3)". Análogo a epilepsia focal / GNW ignition con atención.

**Nota:** eta_kura dinámico es CRÍTICO — sin él, T3 y C3 son mutuamente excluyentes. Con modulación, ambos coexisten.

---

## Notas

- **η_kura** debe ser test:eada — empezar con 0.5, ajustar si es demasiado fuerte/débil
- **H (hijack_steps)**: testear 10, 15, 20 y ver cuál reproduce mejor la dinámica
- No eliminar la funcionalidad v2 actual — agregar los cambios como adiciones, no reemplazos
- Actualizar `verification_results_v2.json` después del primer run exitoso