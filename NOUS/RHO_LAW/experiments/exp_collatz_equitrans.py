#!/usr/bin/env python3
"""
RHO_LAW-Collatz: la desviacion de equidistribucion vs longitud de orbita.

LA PREGUNTA: |f_P - 0.5| escala como longitud^(-1/2)?
Si SI -> el azar de una orbita se cancela a si mismo como 1/sqrt(n)
(sistema mezclante), la LEH es asintoticamente cierta por-orbita,
y la divergencia de Collatz es imposible (la conjetura cae).
Si NO -> hay un segundo orden que no se cancela, y ahi puede vivir
una orbita divergente.

Protocolo:
  1. Simular 200k orbitas impares hasta 1M (con cap de pasos generoso)
  2. Medir (f_P - 0.5) y longitud de cada orbita
  3. Binning por longitud: media y std de |f_P - 0.5| por bin
  4. Ajuste log-log: log|f_P - 0.5| = a + b*log(longitud)
     - b = -0.5 -> azar se cancela (1/sqrt(n)) -> LEH asintotica
     - b > -0.5 (ej -0.3 o 0) -> no se cancela -> hueco para divergencia
  5. Comparar con el null model: 200k secuencias RANDOM de pasos P/N
     con la misma longitud — el azar puro DEBE dar -1/2 exacto.
     La diferencia entre Collatz y azar puro ES el sustrato.
"""
import numpy as np
import json
import random
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path(__file__).parent.parent / "data"


def nu2(n):
    v = 0
    while n % 2 == 0 and n > 0:
        n //= 2
        v += 1
    return v


def orbit_fP_length(n0, max_steps=100000, cap=1e18):
    """(f_P, longitud) de la orbita de n0 (contando pasos P y N acelerados)."""
    n = int(n0)
    p = 0
    tot = 0
    for _ in range(max_steps):
        if n <= 1:
            return p / max(tot, 1), tot
        if n > cap:
            return p / max(tot, 1), tot
        if n % 2 == 1:
            m = 3 * n + 1
            v = nu2(m)
            p += 1
            tot += 1 + v
            n = m >> v
        else:
            n //= 2
            tot += 1
    return p / max(tot, 1), tot


def random_sequence_fP(length, seed):
    """Null model: secuencia random P/N con probabilidad de P = 1/3
    (lo que el mapa produce en promedio por paso total: 1/(1+2)=1/3)."""
    rng = np.random.RandomState(seed)
    # cada paso P viene acompanado de ~nu2 pasos N. Modelamos:
    # P (1 evento) seguido de N con numero de N ~ geometrica media 2
    nP = 0
    tot = 0
    while tot < length:
        nP += 1
        tot += 1 + rng.geometric(0.5)  # nu2 ~ geometrica(p=0.5), media 2
    return nP / max(tot, 1)


def main():
    print("=" * 72)
    print("COLLATZ: |f_P - 0.5| vs longitud — ¿el azar se cancela por-orbita?")
    print("=" * 72)

    # 1. Orbitas reales
    n_orbits = 100000
    print(f"\nSimulando {n_orbits} orbitas impares (n0 hasta 2M)...")
    rng = random.Random(42)
    fPs, lengths = [], []
    for i in range(n_orbits):
        n0 = rng.randrange(1, 2_000_000, 2)
        fP, L = orbit_fP_length(n0)
        fPs.append(fP)
        lengths.append(L)
        if (i + 1) % 20000 == 0:
            print(f"  {i+1}/{n_orbits}")
    fPs = np.array(fPs); lengths = np.array(lengths)

    dev = np.abs(fPs - 0.5)
    print(f"  |f_P-0.5|: media={dev.mean():.4f}  max={dev.max():.4f}")
    print(f"  longitudes: media={lengths.mean():.0f}  max={lengths.max()}")

    # 2. Binning por longitud (log bins)
    logL = np.log10(lengths)
    bins = np.percentile(logL, np.linspace(0, 100, 13))
    bin_centers, bin_means, bin_stds = [], [], []
    for i in range(len(bins) - 1):
        m = (logL >= bins[i]) & (logL < bins[i + 1])
        if m.sum() < 30:
            continue
        bin_centers.append(float(np.mean(lengths[m])))
        bin_means.append(float(dev[m].mean()))
        bin_stds.append(float(dev[m].std() / np.sqrt(m.sum())))

    # 3. Ajuste log-log
    x = np.log10(bin_centers)
    y = np.log10(np.array(bin_means))
    coef = np.polyfit(x, y, 1)
    print(f"\nAjuste Collatz:  log|f_P-0.5| = {coef[0]:.4f} * log(longitud) + {coef[1]:.4f}")
    print(f"  exponente b = {coef[0]:.4f}  (azar puro seria -0.5)")

    # 4. Null model (mismas longitudes, secuencia random)
    print(f"\nNull model: {n_orbits//5} secuencias random con las mismas longitudes...")
    null_fPs, null_lengths = [], []
    for i in range(n_orbits // 5):
        L = int(lengths[i])
        fP = random_sequence_fP(L, seed=i)
        null_fPs.append(fP)
        null_lengths.append(L)
    null_fPs = np.array(null_fPs); null_lengths = np.array(null_lengths)
    null_dev = np.abs(null_fPs - 0.5)

    nlogL = np.log10(null_lengths)
    nbins = np.percentile(nlogL, np.linspace(0, 100, 13))
    ncenters, nmeans = [], []
    for i in range(len(nbins) - 1):
        m = (nlogL >= nbins[i]) & (nlogL < nbins[i + 1])
        if m.sum() < 30:
            continue
        ncenters.append(float(np.mean(null_lengths[m])))
        nmeans.append(float(null_dev[m].mean()))
    ncoef = np.polyfit(np.log10(ncenters), np.log10(nmeans), 1)
    print(f"Ajuste null:     log|f_P-0.5| = {ncoef[0]:.4f} * log(longitud) + {ncoef[1]:.4f}")
    print(f"  exponente b = {ncoef[0]:.4f}  (teoria azar: -0.5)")

    # 5. Comparacion: el GAP entre Collatz y azar
    print("\n" + "=" * 72)
    print("VEREDICTO:")
    print(f"  Collatz:  b = {coef[0]:+.4f}")
    print(f"  Null:     b = {ncoef[0]:+.4f}")
    gap = coef[0] - ncoef[0]
    print(f"  GAP:      {gap:+.4f}")
    # La comparacion correcta es Collatz vs NULL (no vs -0.5 teorico):
    # el null con racimos geometricos NO es i.i.d. y ACUMULA desviacion.
    if gap < -0.05:
        print("  -> Collatz CANCELA la desviacion mas rapido que el azar puro:")
        print("     la equidistribucion es un ATRACTOR (auto-correccion activa).")
        print("     Si el exponente es asintotico, la divergencia es IMPOSIBLE:")
        print("     ninguna orbita acumula desviacion para cruzar f_P*=0.7075.")
        print(f"     Teorema a buscar: |f_P-0.5| ~ n^({coef[0]:.2f}) por orbita.")
    elif abs(gap) <= 0.05:
        print("  -> Collatz se comporta como el azar puro: sin auto-correccion.")
    else:
        print("  -> Collatz ACUMULA mas desviacion que el azar: hueco real.")

    # 6. Figura
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].errorbar(bin_centers, bin_means, yerr=bin_stds, fmt="o-", lw=2,
                     color="C0", label="Collatz (200k orbitas)")
    axes[0].plot(ncenters, nmeans, "s--", lw=2, color="C1", label="Null (azar puro)")
    ref = np.array(bin_centers) ** (-0.5) * bin_means[0]
    axes[0].plot(bin_centers, ref, ":", color="gray", label="1/sqrt(n) referencia")
    axes[0].set_xscale("log"); axes[0].set_yscale("log")
    axes[0].set_xlabel("longitud de orbita")
    axes[0].set_ylabel("|f_P - 0.5|")
    axes[0].set_title("Desviacion de equidistribucion vs longitud")
    axes[0].legend(fontsize=9); axes[0].grid(alpha=0.3, which="both")

    axes[1].hist(fPs, bins=60, color="C0", alpha=0.75, density=True, label="Collatz")
    axes[1].axvline(0.5, color="k", ls="--", alpha=0.5)
    axes[1].set_xlabel("f_P"); axes[1].set_ylabel("densidad")
    axes[1].set_title("Distribucion de f_P (200k orbitas)")
    axes[1].legend(fontsize=9)

    plt.tight_layout()
    fig_path = DATA.parent / "figures" / "fig_collatz_equitrans.png"
    fig_path.parent.mkdir(exist_ok=True)
    plt.savefig(fig_path, dpi=150)
    print(f"\nFigura: {fig_path}")

    out = DATA / "collatz_equitrans.json"
    out.write_text(json.dumps({
        "n_orbits": n_orbits,
        "collatz_slope": float(coef[0]), "collatz_intercept": float(coef[1]),
        "null_slope": float(ncoef[0]), "null_intercept": float(ncoef[1]),
        "gap": float(gap),
        "bins": {"centers": bin_centers, "means": bin_means, "stds": bin_stds},
    }, indent=1))
    print(f"JSON: {out}")


if __name__ == "__main__":
    main()
