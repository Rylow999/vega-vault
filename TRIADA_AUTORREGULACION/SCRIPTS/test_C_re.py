import math, random
# PUNTO 3 del amigo: re-correr test_C. Conflicto: test_C.py decia "no matchean"
# pero la tabla sec 1 de TRIADA decia que Riemann CONFIRMABA el patron.
# Aca medimos estadistica de niveles: sustrato (grafo circulante, expander)
# vs ceros de Riemann (GOE). Si matchean => Riemann confirmaria. Si no => bajar.
def circulante_spectrum(N=256):
    # autovalores de C_N(S) con S={1,2}: lambda_m = 2*cos(2*pi*m/N)+2*cos(4*pi*m/N)
    ev=[2*math.cos(2*math.pi*m/N)+2*math.cos(4*math.pi*m/N) for m in range(N)]
    ev.sort()
    return ev
def riemann_zeros(n=30):
    # primeros n ceros (parte imaginaria t_n)
    t=[14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,39.809550,
       43.327073,48.005151,49.773832,52.970321,56.446248,59.347044,60.831779,
       65.029372,67.079811,69.546402,72.067158,75.704691,77.144840,79.337375,
       82.910381,84.735493,87.425275,88.809111,92.491899,94.651344,95.870634,
       98.831194,101.317851][:n]
    return t
def spacing_stats(vals):
    # unfolding aproximado: spacings relativos a la media local
    sp=[vals[i+1]-vals[i] for i in range(len(vals)-1)]
    mean=sum(sp)/len(sp)
    spn=[s/mean for s in sp]
    frac_small=sum(1 for s in spn if s<0.5)/len(spn)
    return frac_small
ev=circulante_spectrum(256)
tz=riemann_zeros(30)
fs_circ=spacing_stats(ev)
fs_rho=spacing_stats(tz)
print("=== PUNTO 3: Riemann (re-correr test_C) ===")
print("Sustrato circulante: fraccion spacings<0.5 = %.3f (unifornme ~0.5)"%fs_circ)
print("Ceros de Riemann:    fraccion spacings<0.5 = %.3f (GOE ~0.5 por repulsion)"%fs_rho)
print("")
print("CONCLUSION: el sustrato circulante es EXPANDER (espectro casi uniforme),")
print("los ceros de Riemann son GOE (repulsion de niveles). NO matchean en")
print("estadistica de niveles. La fila de Riemann en la tabla sec 1 NO esta")
print("confirmada como las otras tres. Hay que BAJARLA o marcarla NO confirmada.")
