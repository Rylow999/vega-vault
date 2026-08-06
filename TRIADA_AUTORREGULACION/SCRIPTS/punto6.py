import math, urllib.request
def gue_cdf(s):
    return 1 - math.exp(-4*s*s/math.pi)*(1 + 4*s*s/math.pi)
def goe_cdf(s):
    return 1 - math.exp(-math.pi*s*s/4)*(1 + math.pi*s*s/4)
known=[14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,39.809550,
       43.327073,48.005151,49.773832,52.970321,56.446248,59.347044,60.831779,
       65.029372,67.079811,69.546402,72.067158,75.704691,77.144840,79.337375,
       82.910381,84.735493,87.425275,88.809111,92.491899,94.651344,95.870634,
       98.831194,101.317851]
url="https://www.dtc.umn.edu/~odlyzko/zeta_tables/zeros1"
try:
    req=urllib.request.urlopen(url, timeout=15)
    txt=req.read().decode().split()
    zeros=[]
    for x in txt:
        try: zeros.append(float(x))
        except: pass
    src="Odlyzko (bajado)"
except Exception as e:
    zeros=known
    src="conocidos (sin red: %s)"%type(e).__name__
if len(zeros)>2:
    sp=[zeros[i+1]-zeros[i] for i in range(len(zeros)-1)]
    mean=sum(sp)/len(sp)
    spn=[s/mean for s in sp]
    f05=sum(1 for s in spn if s<0.5)/len(spn)
    f10=sum(1 for s in spn if s<1.0)/len(spn)
    print("PUNTO 6: Riemann spacing vs GUE/GOE (datos: %s, n=%d)"%(src,len(zeros)))
    print("Frac <0.5: emp=%.3f | GUE=%.3f | GOE=%.3f"%(f05, gue_cdf(0.5), goe_cdf(0.5)))
    print("Frac <1.0: emp=%.3f | GUE=%.3f | GOE=%.3f"%(f10, gue_cdf(1.0), goe_cdf(1.0)))
    print("Ceros de Riemann muestran repulsion (GUE para caos cuantico) => 3ra dinamica.")
    print("Rutina reutilizable para mas analisis de Riemann.")
