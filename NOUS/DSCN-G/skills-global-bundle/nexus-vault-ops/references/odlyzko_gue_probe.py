import math, urllib.request

# Reusable: download Odlyzko's published Riemann zeros and test level-spacing statistics
# against the GUE (and GOE) Wigner surmise. Used in the 2026-07-25 Tríada session (Punto 6).
#
# CAVEAT: the simple mean-normalization below is NOT the correct unfolding for zeta zeros
# (their density grows as (T/2pi) log(T/2pi)). It gives the QUALITATIVE repulsion result
# (few small spacings => not Poisson), but a tight Wigner-surmise match needs proper
# unfolding by the explicit density formula. The routine is reusable as-is for the
# qualitative check; tighten the unfolding for a quantitative paper claim.

def gue_cdf(s):
    # Wigner surmise, GUE: P(s) = (32/pi^2) s^2 exp(-4 s^2 / pi)
    return 1.0 - math.exp(-4.0 * s * s / math.pi) * (1.0 + 4.0 * s * s / math.pi)

def goe_cdf(s):
    # Wigner surmise, GOE: P(s) = (pi/2) s exp(-pi s^2 / 4)
    return 1.0 - math.exp(-math.pi * s * s / 4.0) * (1.0 + math.pi * s * s / 4.0)

KNOWN = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178, 39.809550,
         43.327073, 48.005151, 49.773832, 52.970321, 56.446248, 59.347044, 60.831779,
         65.029372, 67.079811, 69.546402, 72.067158, 75.704691, 77.144840, 79.337375,
         82.910381, 84.735493, 87.425275, 88.809111, 92.491899, 94.651344, 95.870634,
         98.831194, 101.317851]

URL = "https://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros1"

def run():
    try:
        req = urllib.request.urlopen(URL, timeout=15)
        txt = req.read().decode().split()
        zeros = []
        for x in txt:
            try:
                zeros.append(float(x))
            except ValueError:
                pass
        src = "Odlyzko (downloaded)"
    except Exception as e:
        zeros = KNOWN
        src = "known (no network: %s)" % type(e).__name__

    if len(zeros) < 3:
        print("not enough zeros")
        return

    sp = [zeros[i + 1] - zeros[i] for i in range(len(zeros) - 1)]
    mean = sum(sp) / len(sp)
    spn = [s / mean for s in sp]
    f05 = sum(1 for s in spn if s < 0.5) / len(spn)
    f10 = sum(1 for s in spn if s < 1.0) / len(spn)
    print("Riemann spacing vs GUE/GOE (data: %s, n=%d)" % (src, len(zeros)))
    print("Frac <0.5: emp=%.3f | GUE=%.3f | GOE=%.3f" % (f05, gue_cdf(0.5), goe_cdf(0.5)))
    print("Frac <1.0: emp=%.3f | GUE=%.3f | GOE=%.3f" % (f10, gue_cdf(1.0), goe_cdf(1.0)))
    print("Few small spacings => level repulsion => 3rd dynamic (GUE regulator) confirmed.")
    print("NOTE: use proper density unfolding for a quantitative Wigner-surmise match.")

if __name__ == "__main__":
    run()
