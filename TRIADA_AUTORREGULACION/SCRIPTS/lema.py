import math
# LEMA: relacion entre G (curvatura espectral) y pendiente efectiva alpha(k)
# H1 = int k^2 E(k) dk. Si E~k^-alpha, H1 converge sii alpha>3.
# G = int alpha(k)^2 d(log k). G acotada => alpha(k) acotada en promedio,
# PERO no garantiza alpha>3 en todo rango.
# Verificamos en el espectro final de la sim 3D: medimos alpha efectiva por anillos.

def alpha_por_anillos(E_by_k, nbins=8):
    # E_by_k: dict k->E promediado. Agrupamos en anillos logaritmicos.
    ks=sorted(E_by_k.keys())
    if not ks: return []
    logks=[math.log(k) for k in ks]
    lo,hi=min(logks),max(logks)
    out=[]
    for b in range(nbins):
        a=lo+(hi-lo)*b/nbins; c=lo+(hi-lo)*(b+1)/nbins
        ks_in=[k for k in ks if a<=math.log(k)<c]
        if len(ks_in)>=2:
            # pendiente por regresion log-log
            lx=[math.log(k) for k in ks_in]; ly=[math.log(E_by_k[k]) for k in ks_in]
            n=len(lx); mx=sum(lx)/n; my=sum(ly)/n
            num=sum((lx[i]-mx)*(ly[i]-my) for i in range(n))
            den=sum((lx[i]-mx)**2 for i in range(n))
            alpha = -num/den if den>0 else 0
            out.append((math.exp((a+c)/2), alpha))
    return out

# espectro final simulado 3D (reconstruimos aproximado)
# usamos E(k)=1/k^2 inicial modificado por confinamiento (plateau)
# para el test: si G acotada y alpha efectiva >3 en todos los anillos => H1 acotada
print("LEMA: G acotada => H1 acotada REQUIERE alpha(k) >= 3+eps en TODO rango.")
print("G acotada solo da alpha acotada en promedio, NO alpha>3 localmente.")
print("")
print("Contraejemplo: espectro E(k)=k^-2 para k<K0 y E(k)=k^-1 para k>K0.")
print("  G finita (pendientes acotadas: 2 y 1).")
print("  PERO H1 = int k^2 E = int k^2 k^-1 = int k => DIVERGE (alpha=1 < 3).")
print("=> G acotada NO implica H1 acotada sin cota inferior de pendiente.")
print("")
print("LEMA CORRECTO: Si G[u]<=G* Y alpha_min = inf_k alpha(k) >= 3+eps,")
print("entonces H1[u] <= C(eps, G*) finito. La cota de pendiente es la que falta.")
print("EN NS: la pendiente de Kolmogorov es alpha=5/3 < 3 => H1 DIVERGE en teoria,")
print("pero la disipacion viscosa corta el espectro en k_diss. Ese corte es el que")
print("salva H1, NO la curvatura G. Conclusion: G acotada no es suficiente sola.")
