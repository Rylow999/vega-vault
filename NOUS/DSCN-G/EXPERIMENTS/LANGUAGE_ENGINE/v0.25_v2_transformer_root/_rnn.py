#!/usr/bin/env python3
"""
rnn_baseline.py — Baseline "recurrente simple" para el N-back, pedido
explícito de REVIEW_RECOMMENDATIONS.md ("Comparación contra modelos
recurrentes simples") y de la Ronda 4 de auditoría.

Diseño (para que la comparación sea justa):
  - Mismo generador de secuencias que nback_v6_occurrence_aware.py
    (_generate_balanced_sequence), mismos n_back, mismo n_stimuli=50,
    mismo seq_len=300, mismas 40 seeds de TEST (0..39) que usa DSCN-G v6.
  - A diferencia de DSCN-G (que es un mecanismo sin entrenamiento, corrido
    directo sobre las 40 seeds), el RNN necesita entrenarse. Se entrena
    sobre 40 secuencias adicionales (seeds 1000..1039, disjuntas de las
    de test) y se evalúa sobre las mismas seeds 0..39 que DSCN-G, para que
    ambos modelos se evalúen en las mismas 40 instancias del task.
  - Arquitectura: Elman RNN vainilla (tanh, sin gating) — "simple" en el
    sentido literal, no un LSTM/GRU. Input: one-hot del estímulo en cada
    paso (dim=n_stimuli). Salida: P(match) en cada paso vía sigmoid.
    BPTT completo (300 pasos), Adam, gradient clipping.
  - Honestidad: un RNN vainilla sin gating es conocido por sufrir
    vanishing gradients en dependencias largas — es exactamente lo que se
    espera ver degradarse más rápido que DSCN-G en n_back alto, y eso en
    sí es un resultado válido para reportar, no algo a esconder.
"""
import sys, os, json, time
import numpy as np
from scipy.stats import norm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "nback_v6_corrected"))
from nback_v6_occurrence_aware import _generate_balanced_sequence  # noqa: E402


def make_dataset(n_back, n_stimuli, seq_len, seeds, p_match=0.5):
    Xs, Ys, masks = [], [], []
    for s in seeds:
        rng = np.random.default_rng(s)
        seq, is_match = _generate_balanced_sequence(seq_len, n_back, n_stimuli, p_match, rng)
        X = np.eye(n_stimuli)[seq]                      # (T, n_stimuli) one-hot
        Y = np.array([1.0 if m else 0.0 for m in is_match])
        mask = np.array([1.0 if (t >= n_back) else 0.0 for t in range(seq_len)])
        Xs.append(X); Ys.append(Y); masks.append(mask)
    return np.stack(Xs), np.stack(Ys), np.stack(masks)   # (B,T,D) (B,T) (B,T)


class VanillaRNN:
    def __init__(self, n_in, n_hidden, seed=0):
        rng = np.random.default_rng(seed)
        s_in = 1.0 / np.sqrt(n_in)
        s_h = 1.0 / np.sqrt(n_hidden)
        self.Wxh = rng.uniform(-s_in, s_in, (n_hidden, n_in))
        self.Whh = rng.uniform(-s_h, s_h, (n_hidden, n_hidden))
        self.bh = np.zeros(n_hidden)
        self.Wy = rng.uniform(-s_h, s_h, (1, n_hidden))
        self.by = np.zeros(1)
        self.n_hidden = n_hidden

        # Adam state
        self.params = ["Wxh", "Whh", "bh", "Wy", "by"]
        self.m = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.v = {p: np.zeros_like(getattr(self, p)) for p in self.params}
        self.t_adam = 0

    def forward(self, X):
        B, T, D = X.shape
        H = self.n_hidden
        h = np.zeros((B, H))
        h_hist = np.zeros((T, B, H))
        y_hist = np.zeros((T, B))
        for t in range(T):
            z = X[:, t, :] @ self.Wxh.T + h @ self.Whh.T + self.bh
            h = np.tanh(z)
            y_pre = h @ self.Wy.T + self.by
            y = 1.0 / (1.0 + np.exp(-y_pre))
            h_hist[t] = h
            y_hist[t] = y[:, 0]
        return h_hist, y_hist

    def train_step(self, X, Y, mask, lr=0.01, clip=5.0):
        B, T, D = X.shape
        H = self.n_hidden
        h_prev_hist = np.zeros((T, B, H))
        h_hist = np.zeros((T, B, H))
        y_hist = np.zeros((T, B))
        h = np.zeros((B, H))
        for t in range(T):
            h_prev_hist[t] = h
            z = X[:, t, :] @ self.Wxh.T + h @ self.Whh.T + self.bh
            h = np.tanh(z)
            y_pre = h @ self.Wy.T + self.by
            y = 1.0 / (1.0 + np.exp(-y_pre))
            h_hist[t] = h
            y_hist[t] = y[:, 0]

        n_valid = mask.sum()
        loss = -np.sum(mask * (Y * np.log(y_hist + 1e-9) + (1 - Y) * np.log(1 - y_hist + 1e-9))) / n_valid

        dWxh = np.zeros_like(self.Wxh); dWhh = np.zeros_like(self.Whh)
        dbh = np.zeros_like(self.bh); dWy = np.zeros_like(self.Wy); dby = np.zeros_like(self.by)
        dh_next = np.zeros((B, H))

        for t in reversed(range(T)):
            dy_pre = (y_hist[t] - Y[t]) * mask[t] / n_valid          # (B,)
            dWy += (dy_pre[:, None].T @ h_hist[t])                   # (1,H)
            dby += dy_pre.sum(keepdims=True)
            dh = dy_pre[:, None] @ self.Wy + dh_next                 # (B,H)
            dz = dh * (1 - h_hist[t] ** 2)                           # (B,H)
            dWxh += dz.T @ X[:, t, :]
            dWhh += dz.T @ h_prev_hist[t]
            dbh += dz.sum(axis=0)
            dh_next = dz @ self.Whh

        grads = dict(Wxh=dWxh, Whh=dWhh, bh=dbh, Wy=dWy, by=dby)
        self.t_adam += 1
        beta1, beta2, eps = 0.9, 0.999, 1e-8
        for p in self.params:
            g = np.clip(grads[p], -clip, clip)
            self.m[p] = beta1 * self.m[p] + (1 - beta1) * g
            self.v[p] = beta2 * self.v[p] + (1 - beta2) * (g ** 2)
            mhat = self.m[p] / (1 - beta1 ** self.t_adam)
            vhat = self.v[p] / (1 - beta2 ** self.t_adam)
            setattr(self, p, getattr(self, p) - lr * mhat / (np.sqrt(vhat) + eps))

        return loss


def z(p, n):
    p = min(max(p, 1.0 / (2 * n)), 1 - 1.0 / (2 * n))
    return norm.ppf(p)


def evaluate(rnn, X, Y, mask, threshold=0.5):
    _, y_hist = rnn.forward(X)                      # (T,B)
    y_hist = y_hist.T                                # (B,T)
    pred = (y_hist >= threshold).astype(float)
    m = mask.astype(bool)
    hits = np.sum((pred == 1) & (Y == 1) & m)
    misses = np.sum((pred == 0) & (Y == 1) & m)
    fas = np.sum((pred == 1) & (Y == 0) & m)
    crs = np.sum((pred == 0) & (Y == 0) & m)
    n_match = hits + misses
    n_nonmatch = fas + crs
    hit_rate = hits / n_match if n_match else np.nan
    fa_rate = fas / n_nonmatch if n_nonmatch else np.nan
    bal_acc = 0.5 * (hit_rate + (1 - fa_rate))
    dprime = z(hit_rate, n_match) - z(fa_rate, n_nonmatch)
    return float(bal_acc), float(dprime)


def run_one_nback(n_back, n_stimuli=50, seq_len=300, n_hidden=32,
                   epochs=400, lr=0.05, seed=0, verbose=True):
    train_seeds = list(range(1000, 1040))
    test_seeds = list(range(0, 40))

    Xtr, Ytr, Mtr = make_dataset(n_back, n_stimuli, seq_len, train_seeds)
    Xte, Yte, Mte = make_dataset(n_back, n_stimuli, seq_len, test_seeds)

    rnn = VanillaRNN(n_in=n_stimuli, n_hidden=n_hidden, seed=seed)
    t0 = time.time()
    for ep in range(epochs):
        loss = rnn.train_step(Xtr, Ytr.T, Mtr.T, lr=lr)
        if verbose and (ep % 30 == 0 or ep == epochs - 1):
            print(f"    n_back={n_back:2d} epoch={ep:3d} loss={loss:.4f}")
    train_time = time.time() - t0

    bal_acc, dprime = evaluate(rnn, Xte, Yte, Mte)
    if verbose:
        print(f"  n_back={n_back:2d}: bal.acc={bal_acc*100:5.1f}%  d'={dprime:5.2f}  "
              f"({train_time:.1f}s train)")
    return dict(n_back=n_back, bal_acc=bal_acc, dprime=dprime, train_time_s=train_time)


def run_one_nback_multiseed(n_back, n_stimuli=50, seq_len=300, n_hidden=32,
                             epochs=400, lr=0.05, train_seeds=(0, 1, 2), verbose=True):
    """Average over several training-initialization seeds (not the task's
    own trial seeds, which stay fixed at 0..39 for test — see make_dataset
    calls inside run_one_nback). A single training run can land in a bad
    local optimum (observed directly: n_back=2 scored below n_back=3 on a
    single seed, which is not a plausible property of the task itself) —
    averaging removes that as a confound before comparing to DSCN-G."""
    accs, dps = [], []
    for sd in train_seeds:
        r = run_one_nback(n_back, n_stimuli=n_stimuli, seq_len=seq_len, n_hidden=n_hidden,
                           epochs=epochs, lr=lr, seed=sd, verbose=False)
        accs.append(r["bal_acc"]); dps.append(r["dprime"])
    bal_acc_m, bal_acc_s = float(np.mean(accs)), float(np.std(accs))
    dp_m, dp_s = float(np.nanmean(dps)), float(np.nanstd(dps))
    if verbose:
        print(f"  n_back={n_back:2d}: bal.acc={bal_acc_m*100:5.1f}%±{bal_acc_s*100:4.1f}%  "
              f"d'={dp_m:5.2f}±{dp_s:4.2f}  (seeds={list(train_seeds)}, per-seed d'={[round(x,2) for x in dps]})")
    return dict(n_back=n_back, bal_acc=bal_acc_m, bal_acc_std=bal_acc_s,
                dprime=dp_m, dprime_std=dp_s, per_seed_dprime=dps)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-backs", type=int, nargs="+",
                     default=[1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20])
    ap.add_argument("--out", type=str, default="rnn_baseline_results.json")
    args = ap.parse_args()

    print("Baseline recurrente simple (Elman RNN, tanh, sin gating) — N-back")
    print("Promediado sobre 3 semillas de entrenamiento por n_back")
    print("=" * 70)
    rows = []
    for n in args.n_backs:
        rows.append(run_one_nback_multiseed(n))

    out = dict(model="vanilla_rnn", n_hidden=32, epochs=400, lr=0.05,
               train_seeds_per_nback=[0, 1, 2],
               test_seeds="0-39 (same as DSCN-G v6)",
               results=rows)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()
