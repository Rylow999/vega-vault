import math, random

# ============================================================
# TEST C: estadistica de niveles del sustrato circulante fractal
# vs ceros no triviales de la funcion zeta de Riemann.
# Hipotesis unificadora: "todo es la red de nodos fase-vector" =>
# el espectro de mi sustrato deberia emparentarse con el de zeta (Hilbert-Polya).
# ============================================================

# --- (1) Autovalores del Laplaciano del circulante fractal C_N(S) ---
# lambda_j = kbar - sum_{d in S} 2 cos(2 pi j d / N),  j=0..N-1
def eigenvalues_circulant(m):
    N=2**m; S=[2**k for k in range(m-1)]; kbar=2*(m-1)
    ev=[]
    for j in range(N):
        s=sum(2*math.cos(2*math.pi*j*d/N) for d in S)
        ev.append(kbar-s)
    return sorted(ev)

def level_spacing(evs):
    # quitar el 0 (autovalor dominante) y tomar spacings adyacentes
    evs=[e for e in evs if e>1e-9]
    evs.sort()
    sp=[evs[i+1]-evs[i] for i in range(len(evs)-1)]
    # normalizar por la media (unfolding burdo)
    if not sp: return []
    mean=sum(sp)/len(sp)
    return [s/mean for s in sp]

# --- (2) Ceros de Riemann (primeros ~30) via formula de Gram/Riemann-von Mangoldt ---
# t_n ~ 2*pi*n / log(n/...) ... usamos la aproximacion t_n ~ 2*pi*(n - 11/8)/log(...)
# Para precision modesta usamos la formula de guia: t_n ~ (2*pi/W)*(n - 11/8), W=ln(2pi)-1
# Mejor: usamos valores conocidos de los primeros ceros (tabla corta) y completamos por formula.
known_zeros=[14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,
39.809550,43.327073,48.005151,49.773832,52.970321,56.446248,59.347044,
60.831779,65.029372,67.079811,69.546402,72.067158,75.704691,77.144840,
79.337375,82.910381,84.735493,87.425275,88.809111,92.491899,94.651344,
95.870634,98.831194,101.317851]
def zeta_zero_spacings():
    sp=[known_zeros[i+1]-known_zeros[i] for i in range(len(known_zeros)-1)]
    mean=sum(sp)/len(sp)
    return [s/mean for s in sp]

# Estadistica: fraccion de spacings pequeños (P(s) cerca de 0)
# GOE (caotico/universal) => P(s)~ (pi/2) s  (lineal, muchos pequenos)
# Poisson (integrable) => P(s)~ exp(-s) (pico en 0)
def small_fraction(spacings, eps=0.3):
    if not spacings: return 0.0
    return sum(1 for s in spacings if s<eps)/len(spacings)

print("=== TEST C: estadistica de niveles ===")
ev=eigenvalues_circulant(8)  # N=256
c_sp=level_spacing(ev)
z_sp=zeta_zero_spacings()
print(f"Circulante fractal (N=256): niveles={len(c_sp)}, fraccion spacing<0.3 = {small_fraction(c_sp):.3f}")
print(f"Ceros de Riemann (30):       niveles={len(z_sp)}, fraccion spacing<0.3 = {small_fraction(z_sp):.3f}")
print()
print("Interpretacion:")
print("- Riemann (GUE/GOE caotico): muchos spacings pequenos => fraccion <0.3 ALTA (~0.5).")
print("- Circulante fractal es EXPANDER (gap 4): espectro muy regular/uniforme => spacings")
print("  tienden a ser mas uniformes (menos pequenos que GOE).")
print("- Si ambas fracciones coinciden => puente espectral real (apoya Hilbert-Polya + tu red).")
print("- Si difieren => tu sustrato NO reproduce la estadistica de zeta; la unificacion")
print("  con Riemann queda solo a nivel narrativo, no espectral.")
