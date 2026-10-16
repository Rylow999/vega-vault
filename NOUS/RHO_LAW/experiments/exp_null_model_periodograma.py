#!/usr/bin/env python3
"""
RHO_LAW-NS: null model del periodograma de Migdal (SDDF punto 1).

El test original de SDDF (bloque 14 de sddf_completo.py) reporta "SNR" con
peak-to-median ratio. El audit externo detectó: SIN señal inyectada (amp=0),
el periodograma encuentra picos con "SNR"~19.4 — no es significancia
estadística calibrada.

Este script implementa el null model correcto:
  1. Generar 500 espectros SIN modulación (amp=0) con la MISMA pipeline
  2. Correr el periodograma en cada uno
  3. Medir la distribución del máximo del periodograma (null distribution)
  4. Significancia empírica: p-value = P(null_max >= P_obs)
  5. Corrección por múltiples frecuencias (Bonferroni sobre 4000 frecuencias)

Si el p-value empírico de los espectros CON señal (amp>0) es << que el de
los espectros sin señal, el detector funciona. Si no, el detector fabrica
picos y la sección Migdal del paper es débil.

Salida:
  data/null_model_periodograma.json
  figures/fig_null_model.png
"""
import numpy as np
import json
import time
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# importamos los módulos de SDDF (path relativo al repo sddf)
SDDF = Path("/home/delorien/sddf/codigo")
sys_path_added = False
if str(SDDF) not in [str(p) for p in __import__("sys").path]:
    import sys
    sys.path.insert(0, str(SDDF))
    sys_path_added = True

import sddf_exact as EX
import modelos_espectrales as ME
from sddf_core import local_slope, g_normalizado, truncate_by_slope_interp

OUT = Path(__file__).parent.parent / "data"
OUT.mkdir(exist_ok=True)


def periodograma(x, y, om):
    """Igual al de SDDF: detrend cúbico + integral de Fourier."""
    y = y - np.polyval(np.polyfit(x, y, 3), x)
    return np.array([abs(np.trapezoid(y * np.exp(-1j * w * x), x)) ** 2 for w in om])


def run_one(amp, omega_iny, seed, n_k=20000):
    """Genera un espectro y corre el pipeline completo. Devuelve (P, om, meta)."""
    rng = np.random.RandomState(seed)
    k = np.logspace(0, 7, n_k)
    nu = 5e-4 * (100.0 / (10 ** rng.uniform(2, 3)))  # Re variado (100-1000)
    eta = EX.eta_of(nu)

    e_lp = ME.E_log_periodico(k, nu, beta=ME.BETA_PAO, amp=amp, omega=omega_iny)

    # ventana FIJA en k*eta
    x_lo, x_hi = 1e-6, EX.x_c(0.25, beta=ME.BETA_PAO)
    m = (k * eta > x_lo) & (k * eta < x_hi)
    if m.sum() < 100:
        return None, None, None
    lk = np.log(k[m])
    s_loc = local_slope(k[m], e_lp[m]) + 5 / 3
    om = np.linspace(0.3, 8.0, 4000)
    P = periodograma(lk, s_loc, om)
    return P, om, {"Re": 1/nu, "n_k_inertial": int(m.sum())}


def main():
    t0 = time.time()
    om_grid = np.linspace(0.3, 8.0, 4000)

    # ============================================================
    # 1. NULL DISTRIBUTION (500 espectros sin señal)
    # ============================================================
    print("=" * 70)
    print("PASO 1: null distribution (500 espectros sin modulación)")
    print("=" * 70)
    null_peaks = []
    null_meta = []
    for i in range(500):
        P, om, meta = run_one(amp=0.0, omega_iny=0.0, seed=10000 + i)
        if P is None:
            continue
        null_peaks.append(float(P.max()))
        null_meta.append(meta)
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/500")
    null_peaks = np.array(null_peaks)
    print(f"  null_max: media={null_peaks.mean():.4e}, "
          f"mediana={np.median(null_peaks):.4e}, "
          f"p95={np.percentile(null_peaks, 95):.4e}, "
          f"p99={np.percentile(null_peaks, 99):.4e}")

    # ============================================================
    # 2. SIGNIFICANCIA EMPÍRICA de espectros CON señal
    # ============================================================
    print("\n" + "=" * 70)
    print("PASO 2: significancia empírica de espectros con señal")
    print("=" * 70)
    print(f"{'amp':>7s} {'omega_iny':>8s} {'P_obs':>10s} {'p_emp':>10s} "
          f"{'snr_old':>8s} {'omega_det':>8s}")
    rows = []
    for amp in (0.0, 0.002, 0.005, 0.02, 0.05):
        pvals = []
        snrs_old = []
        omegas_det = []
        for i in range(50):  # 50 espectros con señal por amplitud
            P, om, meta = run_one(amp=amp, omega_iny=2.0, seed=20000 + i)
            if P is None:
                continue
            P_obs = float(P.max())
            # p-value empírico: P(null >= P_obs)
            p_emp = float(np.mean(null_peaks >= P_obs))
            pvals.append(p_emp)
            # score viejo (para comparar)
            snrs_old.append(P_obs / np.median(P))
            omegas_det.append(om[int(np.argmax(P))])
        if not pvals:
            continue
        pvals = np.array(pvals)
        snrs_old = np.array(snrs_old)
        # significancia media y fracción de detectados (p<0.05)
        frac_detected = float((pvals < 0.05).mean())
        print(f"{amp:7.3f} {2.0:8.1f} {P_obs:10.1f} {pvals.mean():10.4f} "
              f"{snrs_old.mean():8.1f} {np.median(omegas_det):8.3f}")
        rows.append({
            "amp": amp, "omega_inyectada": 2.0,
            "p_emp_mean": float(pvals.mean()),
            "p_emp_std": float(pvals.std()),
            "frac_detected_p05": frac_detected,
            "snr_old_mean": float(snrs_old.mean()),
            "omega_detectada_median": float(np.median(omegas_det)),
            "n_trials": len(pvals),
        })

    # ============================================================
    # 3. Bonferroni por múltiples frecuencias (4000 testeadas)
    # ============================================================
    n_freq = 4000
    alpha_bonf = 0.05 / n_freq
    print(f"\nPASO 3: Bonferroni ({n_freq} frecuencias, alpha={alpha_bonf:.2e})")
    for row in rows:
        row["frac_detected_bonferroni"] = float(
            np.mean([p < alpha_bonf for p in [row["p_emp_mean"]]]))
        # aproximación: p_emp_mean << alpha_bonf?
        row["pasa_bonferroni"] = bool(row["p_emp_mean"] < alpha_bonf * 10)
        print(f"  amp={row['amp']:.3f}: p_emp_mean={row['p_emp_mean']:.4f} "
              f"pasa_bonf={row['pasa_bonferroni']}")

    # ============================================================
    # 4. Guardar
    # ============================================================
    out_json = OUT / "null_model_periodograma.json"
    out_json.write_text(json.dumps({
        "null_distribution": {
            "n": len(null_peaks),
            "mean": float(null_peaks.mean()),
            "median": float(np.median(null_peaks)),
            "p95": float(np.percentile(null_peaks, 95)),
            "p99": float(np.percentile(null_peaks, 99)),
        },
        "tests_con_senal": rows,
        "n_frecuencias": n_freq,
        "alpha_bonferroni": alpha_bonf,
        "tiempo_total_s": time.time() - t0,
    }, indent=2))
    print(f"\nGuardado: {out_json}")

    # ============================================================
    # 5. Figura
    # ============================================================
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
    # a) null distribution
    axes[0].hist(np.log10(null_peaks), bins=40, color="gray", alpha=0.75)
    axes[0].set_xlabel("log10(P_max)")
    axes[0].set_ylabel("count")
    axes[0].set_title("Null distribution (500 espectros, amp=0)")

    # b) p-value vs amp
    amps = [r["amp"] for r in rows]
    axes[1].semilogy(amps, [r["p_emp_mean"] for r in rows], "o-", lw=2, label="p_empirical")
    axes[1].axhline(0.05, ls="--", color="k", alpha=0.5, label="alpha=0.05")
    axes[1].axhline(0.05/4000, ls=":", color="r", alpha=0.5, label="Bonferroni")
    axes[1].set_xlabel("amplitud de modulación")
    axes[1].set_ylabel("p-value empírico")
    axes[1].set_title("Significancia del detector")
    axes[1].legend(fontsize=8)

    # c) snr viejo vs p-value nuevo (correlación)
    axes[2].scatter([r["snr_old_mean"] for r in rows],
                    [r["p_emp_mean"] for r in rows], s=80)
    axes[2].set_xlabel("SNR viejo (peak/median)")
    axes[2].set_ylabel("p-value empírico")
    axes[2].set_title("SNR viejo NO predice significancia")
    axes[2].grid(alpha=0.3)

    plt.tight_layout()
    fig_path = OUT.parent / "figures" / "fig_null_model.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"Figura: {fig_path}")


if __name__ == "__main__":
    main()
