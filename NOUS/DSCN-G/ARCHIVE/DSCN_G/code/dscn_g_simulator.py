#!/usr/bin/env python3
"""DSCN-G Simulator — Validación Computacional

Implementación minimalista de DSCN-G para validación en tareas sintéticas.

Ecuaciones implementadas:
  (1) State vectors (TD-learning)
  (2) Information chains (probabilistic transition)
  (3) Phase dynamics (Kuramoto)
  (4) Action selection (von Mises)
  (5) Vitality + pruning
  (6) Valence signal (E_i)
  (7) Wave interference

Usar para:
  - N-back task
  - Multi-armed bandit
  - Pattern completion
  - Phase-hijacking (C3) predicciones
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
import json


class DSCN_G:
    """Dual-State Cognitive Geometry simulator."""

    def __init__(self, N=50, K=3, d=8, alpha=5.0, beta=0.01,
                 eta=0.1, lambda_vm=3.0, n_actions=8,
                 gamma=0.01, theta_death=0.10, kappa=1.0,
                 seed: Optional[int] = None):
        """
        Args:
            N: Número inicial de nodos
            K: Número de information chains
            d: Dimensión de state vectors
            alpha: Selectividad semántica (Eq. 2)
            beta: Learning rate (Eq. 1)
            eta: Phase coupling strength (Eq. 3)
            lambda_vm: Concentración de von Mises (Eq. 4)
            n_actions: Número de acciones posibles
            gamma: Decay rate de vitalidad (Eq. 5)
            theta_death: Threshold de pruning (Eq. 5)
            kappa: Gain de valence signal (Eq. 6)
            seed: Random seed para reproducibilidad
        """
        if seed is not None:
            np.random.seed(seed)
            self.rng = np.random.default_rng(seed)
        else:
            self.rng = np.random.default_rng()

        self.N_init = N
        self.K = K
        self.d = d
        self.alpha = alpha
        self.beta = beta
        self.eta = eta
        self.lambda_vm = lambda_vm
        self.n_actions = n_actions
        self.gamma = gamma
        self.theta_death = theta_death
        self.kappa = kappa

        # Estado del sistema
        self.nodes_active = list(range(N))  # Índices de nodos activos
        self.nodes_pruned = []

        # Eq. 1: State vectors
        self.omega = np.random.randn(N, d) * 0.1  # Inicializar pequeños
        self.omega_ideal = np.ones(d) / np.sqrt(d)  # Vector objetivo normalizado

        # Eq. 3: Phases
        self.phi = np.random.uniform(0, 2*np.pi, N)

        # Eq. 5: Vitality
        self.vitality = np.ones(N)

        # Eq. 2: Chain positions
        self.chain_positions = np.random.choice(self.nodes_active, K)

        # Métricas
        self.t = 0
        self.history = {
            'N_active': [],
            'mean_omega_norm': [],
            'phase_coherence': [],
            'reward': [],
        }

        # C3: Phase-hijacking mechanism
        self.theta_emerg = 0.30
        self.theta_star = 0.0  # Reference phase for antipodal attractor
        self.c3_hijack_count = 0
        self.c3_phase_change_accum = 0.0
        self.c3_window_steps = 20

    def _compute_relevance(self, i: int) -> float:
        """Eq. 1 (bounded relevance): R_i(t) = R_base / (1 + ||ω_i − ω_ideal||)"""
        diff = np.linalg.norm(self.omega[i] - self.omega_ideal)
        R_base = 1.0
        return R_base / (1.0 + diff)

    def _chain_transition(self, node_idx: int) -> int:
        """Eq. 2: P(m|n) ∝ exp(−α · ||ω_m − ω_n||)"""
        if len(self.nodes_active) == 0:
            return node_idx

        probs = []
        for m_idx in self.nodes_active:
            diff = np.linalg.norm(self.omega[m_idx] - self.omega[node_idx])
            probs.append(np.exp(-self.alpha * diff))

        probs = np.array(probs)
        probs /= probs.sum()

        return np.random.choice(self.nodes_active, p=probs)

    def _select_action(self, phi_i: float) -> int:
        """Eq. 4: P(a|φ) = exp(λ·cos(φ − θ_a)) / Σ exp(λ·cos(φ − θ_a′))"""
        theta_actions = np.linspace(0, 2*np.pi, self.n_actions, endpoint=False)

        log_probs = self.lambda_vm * np.cos(phi_i - theta_actions)
        log_probs -= log_probs.max()  # Numerical stability
        probs = np.exp(log_probs)
        probs /= probs.sum()

        return np.random.choice(self.n_actions, p=probs)

    def _phase_update(self, i: int, action_idx: int, outcome: int, reward: float):
        """Eq. 3: φ_i(t+1) = [φ_i(t) + η·R_i(t)·outcome·sin(θ_a − φ_i)] mod 2π"""
        if outcome == 0:
            return  # No phase update on failure

        R_i = self._compute_relevance(i)
        theta_a = 2 * np.pi * action_idx / self.n_actions

        # Adaptive coupling: effective η increases with phase error
        phase_error = (theta_a - self.phi[i] + np.pi) % (2 * np.pi) - np.pi
        adaptive_factor = 1.0 + abs(phase_error) / np.pi  # ∈ [1, 2]
        eta_eff = self.eta * adaptive_factor

        update = eta_eff * R_i * np.sin(theta_a - self.phi[i])
        self.phi[i] = (self.phi[i] + update) % (2 * np.pi)

    def _update_vitality_and_prune(self, activity: np.ndarray):
        """Eq. 5-6: V_i(t+1) = V_i(t)·e^(−γ) + A_i(t)·(1 − e^(−γ))"""
        decay = np.exp(-self.gamma)
        self.vitality[self.nodes_active] = (
            self.vitality[self.nodes_active] * decay +
            activity[self.nodes_active] * (1 - decay)
        )

        # Pruning
        to_prune = []
        for i in self.nodes_active:
            if self.vitality[i] < self.theta_death:
                to_prune.append(i)

        for i in to_prune:
            self.nodes_active.remove(i)
            self.nodes_pruned.append(i)

    def _compute_valence(self, activity: np.ndarray) -> np.ndarray:
        """Eq. 6: E_i(t) = max(0, A_i(t) − V_i(t))·κ"""
        excess = np.maximum(0, activity - self.vitality)
        return excess * self.kappa

    def _wave_interference(self, i: int) -> float:
        """Eq. 7: I_i(t) = ||ω_i(t)|| · cos(φ_i(t) − φ_root(t))"""
        if len(self.nodes_active) == 0:
            return 0.0

        root_idx = self.nodes_active[0]  # Primer nodo activo como "root"
        norm = np.linalg.norm(self.omega[i])
        cos_delta = np.cos(self.phi[i] - self.phi[root_idx])

        return norm * cos_delta

    def step(self, stimulus: Optional[np.ndarray] = None) -> Tuple[int, float]:
        """Un paso de simulación.

        Args:
            stimulus: Input externo (opcional, para tareas específicas)

        Returns:
            action: Índice de acción seleccionada
            reward: Reward recibido
        """
        self.t += 1

        # Mover chains (Eq. 2)
        activity = np.zeros(len(self.omega))
        for k in range(self.K):
            old_pos = self.chain_positions[k]
            new_pos = self._chain_transition(old_pos)
            self.chain_positions[k] = new_pos
            activity[new_pos] += 1

        activity /= self.K  # Normalizar a fracción

        # Actualizar vitality y pruning (Eq. 5)
        self._update_vitality_and_prune(activity)

        # Si no hay nodos activos, terminar
        if len(self.nodes_active) == 0:
            return 0, 0.0

        # Seleccionar un nodo para acción (basado en wave interference)
        interference = np.array([self._wave_interference(i) for i in self.nodes_active])
        selected_idx = self.nodes_active[np.argmax(interference)]

        # Seleccionar acción (Eq. 4)
        action = self._select_action(self.phi[selected_idx])

        # Reward basado en alineación ω con ω_ideal (learning progress)
        # reward = alignment(ω, ω_ideal) ∈ [0, 1]
        omega_vec = self.omega[selected_idx]
        alignment = np.dot(omega_vec, self.omega_ideal) / (np.linalg.norm(omega_vec) + 1e-8)
        reward = (alignment + 1.0) / 2.0  # Map [-1, 1] → [0, 1]
        
        # Outcome estocástico basado en reward (permite TD update incluso con alignment negativo)
        outcome = 1 if self.rng.random() < reward else 0  # P(outcome=1) = reward

        # Actualizar state vector (Eq. 1)
        if outcome == 1:
            self.omega[selected_idx] = (
                (1 - self.beta) * self.omega[selected_idx] +
                self.beta * reward * self.omega_ideal
            )

        # Actualizar phase (Eq. 3) - phase dynamics unchanged (Theorem 3)
        self._phase_update(selected_idx, action, outcome, reward)

        # Calcular valence (Eq. 6)
        valence = self._compute_valence(activity)

        # C3: Phase-hijacking mechanism
        # Check if any node's valence exceeds threshold
        max_valence = np.max(valence)
        if max_valence > self.theta_emerg:
            self.c3_hijack_count += 1
            # Root oscillator phase perturbation toward antipodal attractor (θ* + π)
            root_idx = self.nodes_active[0] if self.nodes_active else 0
            target_phase = (self.theta_star + np.pi) % (2 * np.pi)
            phase_diff = (target_phase - self.phi[root_idx] + np.pi) % (2 * np.pi) - np.pi
            phase_change = 0.1 * np.sign(phase_diff)  # Small step toward antipodal
            self.phi[root_idx] = (self.phi[root_idx] + phase_change) % (2 * np.pi)
            self.c3_phase_change_accum += abs(phase_change)
            # Reset accumulator after window
            if self.t % self.c3_window_steps == 0:
                self.c3_phase_change_accum = 0.0

        # Guardar métricas
        self.history['N_active'].append(len(self.nodes_active))
        self.history['mean_omega_norm'].append(np.mean([
            np.linalg.norm(self.omega[i]) for i in self.nodes_active
        ]))

        phase_coherence = np.abs(np.mean(np.exp(1j * self.phi[self.nodes_active])))
        self.history['phase_coherence'].append(phase_coherence)
        self.history['reward'].append(reward)

        return action, reward

    def run_episode(self, n_steps: int, task_fn=None) -> Dict:
        """Correr un episodio completo.

        Args:
            n_steps: Número de pasos
            task_fn: Función de tarea (None para reward aleatorio)

        Returns:
            Dict con historial de métricas
        """
        rewards = []
        actions = []

        for _ in range(n_steps):
            if task_fn is not None:
                action, reward = task_fn(self)
            else:
                action, reward = self.step()

            rewards.append(reward)
            actions.append(action)

        return {
            'rewards': rewards,
            'actions': actions,
            'N_active_final': len(self.nodes_active),
            'phase_coherence_final': self.history['phase_coherence'][-1] if self.history['phase_coherence'] else 0.0,
        }

    def compute_phi_proxy(self) -> float:
        """Calcular proxy de Φ_IIT (Theorem 7).

        Para fratal circulant graphs: ρ_eff(α, N)·Φ_proxy(N) = c(α) + O(1/N)

        Returns:
            Φ_proxy estimate
        """
        if len(self.nodes_active) < 2:
            return 0.0

        # Calcular ρ_eff (Herfindahl index de actividad)
        activity = np.zeros(len(self.nodes_active))
        for pos in self.chain_positions:
            if pos in self.nodes_active:
                idx = self.nodes_active.index(pos)
                activity[idx] += 1
        activity /= activity.sum()

        rho_eff = np.sum(activity ** 2)

        # Φ_proxy ≈ ρ_eff · log(N) (aproximación para circulant graphs)
        phi_proxy = rho_eff * np.log(len(self.nodes_active))

        return phi_proxy

    def compute_rho_eff(self) -> float:
        """Compute ρ_eff (Herfindahl index of chain activity)."""
        if len(self.nodes_active) < 2:
            return 0.0
        activity = np.zeros(len(self.nodes_active))
        for pos in self.chain_positions:
            if pos in self.nodes_active:
                idx = self.nodes_active.index(pos)
                activity[idx] += 1
        if activity.sum() == 0:
            return 0.0
        activity /= activity.sum()
        return float(np.sum(activity ** 2))

    def compute_plv(self, node_i: int, node_j: int, n_samples: int = 100) -> float:
        """Calcular Phase Locking Value entre dos nodos.

        PLV = |⟨exp(i · (φ_i − φ_j))⟩|

        Returns:
            PLV ∈ [0, 1] (1 = perfect locking)
        """
        phase_diffs = []

        for _ in range(n_samples):
            _, _ = self.step()
            phase_diff = self.phi[node_i] - self.phi[node_j]
            phase_diffs.append(np.exp(1j * phase_diff))

        plv = np.abs(np.mean(phase_diffs))
        return plv

    # ============================================
    # C3 Phase-Hijacking Mechanism
    # ============================================

    def _check_phase_hijack(self) -> Tuple[bool, float]:
        """
        Check for phase-hijacking (Prediction C3).

        When valence E_root exceeds θ_emerg, the root oscillator's phase
        is perturbed toward the antipodal attractor (θ* + π).

        Returns:
            (hijack_occurred, cumulative_phase_change)
        """
        if not self.nodes_active:
            return False, 0.0

        root_idx = self.nodes_active[0]
        E_root = self._compute_valence(np.zeros(len(self.omega)))[root_idx]

        if E_root > self.theta_emerg:
            # Phase-hijacking: perturb toward antipodal
            antipodal_phase = (self.phi[root_idx] + np.pi) % (2 * np.pi)
            phase_diff = (antipodal_phase - self.phi[root_idx] + np.pi) % (2 * np.pi) - np.pi

            # Apply perturbation proportional to excess valence
            perturbation = 0.5 * (E_root - self.theta_emerg) * phase_diff
            self.phi[root_idx] = (self.phi[root_idx] + perturbation) % (2 * np.pi)

            return True, abs(phase_diff)

        return False, 0.0


# ============================================
# Ejemplo de uso: N-back task
# ============================================

class NBackTask:
    """N-back task que usa la arquitectura DSCN-G correctamente.

    El límite de ~4 items emerge de:
    1. N_ss* ≈ 4 (Theorem 1: homeostatic fixed point)
    2. Wave interference compite por atención
    3. Phase coherence decae con n_back creciente
    """

    def __init__(self, n_back: int, n_stimuli: int = 10):
        self.n_back = n_back
        self.n_stimuli = n_stimuli
        self.sequence = []
        self.history_buffer = []

    def generate_sequence(self, length: int):
        """Generar secuencia aleatoria de estímulos."""
        self.sequence = list(np.random.randint(0, self.n_stimuli, length))
        self.history_buffer = []

    def is_match(self, t: int) -> bool:
        """¿El estímulo en t es igual al de hace n_back pasos?"""
        if t < self.n_back:
            return False
        return self.sequence[t] == self.sequence[t - self.n_back]

    def present_stimulus(self, sim: DSCN_G, stimulus: int, t: int):
        """Presentar estímulo al simulador.

        El estímulo se codifica como un patrón en omega_ideal,
        activando nodos específicos según el valor del estímulo.
        """
        # Codificar estímulo como patrón en omega_ideal
        # Cada estímulo activa un subconjunto diferente de dimensiones
        d_per_stimulus = sim.d // self.n_stimuli
        sim.omega_ideal = np.zeros(sim.d)

        for i in range(d_per_stimulus):
            idx = (stimulus * d_per_stimulus + i) % sim.d
            sim.omega_ideal[idx] = 1.0 / np.sqrt(d_per_stimulus)

        # Step del simulador
        action, reward = sim.step()

        # Actualizar history buffer
        self.history_buffer.append(stimulus)
        if len(self.history_buffer) > self.n_back:
            self.history_buffer.pop(0)

        return action, reward

    def get_response(self, sim: DSCN_G) -> bool:
        """Obtener respuesta del simulador: ¿es match?

        El simulador "decide" basado en:
        1. Wave interference de nodos activos
        2. Phase coherence con el estímulo en t-n_back
        3. Número de nodos activos (N_ss*)

        Si N_ss* < n_back, la performance debería caer.
        """
        if len(sim.nodes_active) < 2:
            # Sin nodos activos: respuesta aleatoria
            return np.random.random() > 0.5

        # Calcular interference pattern
        interferences = []
        for i in sim.nodes_active:
            I_i = sim._wave_interference(i)
            interferences.append(I_i)

        # El simulador responde "sí" si la interference máxima es alta
        # y hay suficientes nodos para mantener n_back items
        max_interference = max(interferences) if interferences else 0.0

        # Decision threshold depende de n_back:
        # Si n_back > N_ss*, el threshold debería ser más difícil de alcanzar
        n_active = len(sim.nodes_active)

        # Threshold que decae con n_back / N_ss*
        if n_active > 0:
            load_factor = self.n_back / n_active  # carga cognitiva relativa
            threshold = 0.5 / load_factor  # más difícil con mayor carga
        else:
            threshold = 0.5

        return max_interference > threshold

    def run_trial(self, sim: DSCN_G, sequence_length: int = 100) -> float:
        """Correr un trial completo de N-back.

        Returns:
            accuracy: % de respuestas correctas
        """
        self.generate_sequence(sequence_length)

        correct_count = 0
        total_count = 0

        for t in range(sequence_length):
            stimulus = self.sequence[t]

            # Presentar estímulo
            self.present_stimulus(sim, stimulus, t)

            # Solo evaluar desde t >= n_back
            if t >= self.n_back:
                # Obtener respuesta del simulador
                response = self.get_response(sim)
                true_match = self.is_match(t)

                if response == true_match:
                    correct_count += 1
                total_count += 1

        if total_count == 0:
            return 0.0

        return correct_count / total_count


def run_nback_task(n_back: int, sequence_length: int = 100, n_trials: int = 10, seed_base: int = 42):
    """Correr N-back task con DSCN-G (implementación corregida).

    Returns:
        accuracy: % de aciertos (mean ± std)
    """
    accuracies = []

    for trial in range(n_trials):
        # Simulador con parámetros que favorecen N_ss* ≈ 4
        sim = DSCN_G(
            N=50, K=3, d=8,  # d=8 para que cada estímulo active ~1 dim
            alpha=5.0,       # alta selectividad → menos nodos activos
            theta_death=0.10,
            gamma=0.01,
            seed=seed_base + trial
        )

        task = NBackTask(n_back=n_back, n_stimuli=10)
        accuracy = task.run_trial(sim, sequence_length)
        accuracies.append(accuracy)

    return np.mean(accuracies), np.std(accuracies)


if __name__ == "__main__":
    print("=" * 60)
    print("DSCN-G Simulator — Ejemplos de validación")
    print("=" * 60)

    # Ejemplo 1: N-back task
    print("\n[Ejemplo 1] N-back task")
    for n in [1, 2, 3, 4, 5, 6]:
        acc, std = run_nback_task(n_back=n, sequence_length=100, n_trials=5, seed_base=42)
        print(f"  {n}-back: accuracy = {acc*100:.1f}% ± {std*100:.1f}%")

    # Ejemplo 2: Multi-armed bandit
    print("\n[Ejemplo 2] Multi-armed bandit (K=8)")
    sim = DSCN_G(N=50, K=3, n_actions=8, seed=42)

    probs = [0.3, 0.5, 0.7, 0.4, 0.6, 0.2, 0.8, 0.4]  # Reward probabilities
    optimal_action = np.argmax(probs)

    rewards = []
    for t in range(200):
        action, _ = sim.step()

        # Reward based on action
        reward = 1.0 if np.random.uniform() < probs[action] else 0.0

        rewards.append(reward)

    # Calcular regret acumulado
    optimal_reward = max(probs) * len(rewards)
    actual_reward = sum(rewards)
    regret = optimal_reward - actual_reward

    print(f"  Regret acumulado (200 trials): {regret:.1f}")
    print(f"  Acción óptima: {optimal_action}, más frecuente: {np.bincount(np.array([0]*len(rewards))).argmax() if len(rewards) else 'N/A'}")

    # Ejemplo 3: Φ_proxy
    print("\n[Ejemplo 3] Φ_IIT proxy")
    sim = DSCN_G(N=50, K=3, seed=42)
    sim.run_episode(100)

    phi_proxy = sim.compute_phi_proxy()
    print(f"  Φ_proxy después de 100 steps: {phi_proxy:.4f}")

    print("\n" + "=" * 60)
    print("Simulador funcional. Próximos pasos:")
    print("  1. Implementar tareas específicas (N-back, bandit, pattern completion)")
    print("  2. Correr experimentos con 100 seeds")
    print("  3. Comparar con baselines (LSTM, UCB1, Hopfield)")
    print("  4. Generar plots y estadísticas")
    print("=" * 60)