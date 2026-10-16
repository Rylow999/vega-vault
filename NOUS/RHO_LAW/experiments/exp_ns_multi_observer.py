#!/usr/bin/env python3
"""
Experimento RHO_LAW-NS: múltiples observadores del MISMO objeto turbulento.

El "objeto" es el espectro E(k) del archivo (SDDF v3).
Los "observadores" son operadores G[u] especializados:

  G_full:     G sobre todo el espectro (referencia)
  G_inertial: G solo sobre el rango inercial (corte por pendiente)
  G_energy:   G solo sobre el rango de energía (k pequeños)
  G_diss:     G solo sobre disipación (k grandes)
  G_window_x: G en ventanas móviles (5 ventanas log)

Pregunta: ¿existe una cantidad invariante entre observadores?
Hipótesis (por el resultado SDDF): el RATIO entre G de rangos adyacentes
debería escalar con d ln k, no con el detalle del modelo. Si el ratio es
constante entre observadores, es la invariante buscada.

Salida:
  - tabla por espectro: G por ventana, ratios entre ventanas
  - verificación: la variación de G entre modelos (intermitente vs logper)
    debe ser MAYOR que la variación entre observadores del mismo objeto

Eso último es el análogo SDDF del paper FHRR:
  "El colapso es del observador" -> "El artefacto es del método de corte"
"""
import numpy as np
import pandas as pd
from pathlib import Path


def load_spectrum(path):
    """Devuelve (k, E) saltando comentarios."""
    data = pd.read_csv(path, comment="#")
    k = data["k"].to_numpy()
    E = data["E(k)"].to_numpy()
    return k, E


def dlogE_dlogk(k, E):
    lk = np.log(k)
    lE = np.log(np.maximum(E, 1e-30))
    return np.gradient(lE, lk), lk


def G_window(k, E, kmin, kmax):
    """G sobre una ventana [kmin, kmax]."""
    s, lk = dlogE_dlogk(k, E)
    mask = (lk >= np.log(kmin)) & (lk < np.log(kmax))
    if mask.sum() < 5:
        return np.nan
    return float(np.sum(s[mask] ** 2))


def main():
    exp_dir = Path("/home/delorien/vaults/vega-vault/NOUS/RHO_LAW/experiments")
    espec_dir = Path("/home/delorien/vaults/vega-vault/LOGOS/NAVIER_STOKES/sddf_v3/datos/espectros")

    files = sorted(espec_dir.glob("*_Re_*.csv"))
    print(f"Espectros encontrados: {len(files)}")

    results = []
    for f in files:
        # Extraer metadata del nombre
        name = f.name.replace(".csv", "")
        modelo = "logper" if "logper" in name else "intermitente"
        Re = int(name.split("_Re_")[-1])

        k, E = load_spectrum(f)
        kmin, kmax = k.min(), k.max()

        # Definir 5 ventanas logarítmicas iguales
        nwin = 5
        edges = np.logspace(np.log10(kmin), np.log10(kmax), nwin + 1)

        Gs = []
        for i in range(nwin):
            G = G_window(k, E, edges[i], edges[i + 1])
            Gs.append(G)
        Gs = np.array(Gs)

        # G por segmento y totales
        # Rangos canónicos: inercial (kmin, k_d) donde k_d ~ 1/eta
        # eta está en el header del archivo; lo leemos
        head = "".join(f.open().readline() for _ in range(10))
        # fallback: eta de la curva (donde E cae bruscamente)
        G_total = G_window(k, E, kmin, kmax)

        # Ratios entre ventanas adyacentes
        ratios = []
        for i in range(len(Gs) - 1):
            if Gs[i] > 1e-12 and not np.isnan(Gs[i + 1]):
                ratios.append(Gs[i + 1] / Gs[i])
        ratios = np.array(ratios)

        # La "invariante candidata": varianza LOG entre ventanas
        # (un espectro puro de potencia daria G_i = const * f(ventana),
        #  la varianza log de G_i entre ventanas debe ser estable)
        valid = ~np.isnan(Gs) & (Gs > 0)
        Gs_valid = Gs[valid]
        if len(Gs_valid) >= 3:
            log_G = np.log(Gs_valid)
            # La segunda diferencia log (curvatura del observable)
            second_diff = np.mean(np.abs(np.diff(np.log(Gs_valid), n=2))) if len(Gs_valid) > 2 else np.nan
            ratio_mean = np.mean(ratios)
            ratio_std = np.std(ratios)
        else:
            second_diff = np.nan
            ratio_mean = np.nan
            ratio_std = np.nan

        results.append({
            "file": name,
            "modelo": modelo,
            "Re": Re,
            "G_total": G_total,
            "G_ventanas": list(Gs),
            "ratio_mean": ratio_mean,
            "ratio_std": ratio_std,
            "second_diff_log": second_diff,
            "n_ventanas_validas": int(valid.sum()),
        })

    df = pd.DataFrame(results)
    df = df.sort_values(["modelo", "Re"]).reset_index(drop=True)

    # === ANÁLISIS ===
    print("\n=== Resumen por modelo ===")
    for modelo in df.modelo.unique():
        sub = df[df.modelo == modelo]
        print(f"\n-- {modelo} (n={len(sub)}) --")
        print(sub[["Re", "G_total", "ratio_mean", "ratio_std", "second_diff_log"]].to_string(index=False))

    # La pregunta clave: ¿qué varía vs qué permanece?
    print("\n=== ¿Invariante entre observadores? ===")
    for col in ["G_total", "ratio_mean", "second_diff_log"]:
        for modelo in df.modelo.unique():
            sub = df[df.modelo == modelo][col].dropna()
            if len(sub) > 1:
                cv = sub.std() / abs(sub.mean())
                print(f"  {modelo:>12} | {col:>18}: CV={cv:.3f} (mean={sub.mean():.4f})")

    # Comparación clave: misma ventana, distintos modelos, mismo Re
    print("\n=== Comparación por Re (ventana central = ventana 2) ===")
    for Re in sorted(df.Re.unique()):
        sub = df[df.Re == Re]
        if len(sub) < 2:
            continue
        g2 = [r["G_ventanas"][2] for _, r in sub.iterrows()]
        gm = np.mean(g2)
        gs = np.std(g2)
        print(f"  Re={Re:5d}: G_ventana2 = {gm:.4f} ± {gs:.4f} (CV={gs/gm:.3f})")

    out = Path("/home/delorien/vaults/vega-vault/NOUS/RHO_LAW/experiments/rho_law_ns_multi_observer.json")
    import json
    df.to_json(out, orient="records", indent=2)
    print(f"\nGuardado: {out}")


if __name__ == "__main__":
    main()
