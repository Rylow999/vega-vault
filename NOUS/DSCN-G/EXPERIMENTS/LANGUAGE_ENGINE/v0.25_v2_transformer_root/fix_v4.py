p="/sdcard/Hermes/nexus-vault/NOUS/DOCUMENTATION/v4.0/NOUS_Tecnico_v4.md"
s=open(p).read()

# 1) Corregir T3 "100% de semillas" -> 76.7% estricto
old_t3="**100% de semillas** alcanzan bloqueo de fase antes del paso 500."
new_t3="**76.7% de semillas (criterio estricto R≥0.9)** alcanzan bloqueo de fase antes del paso 500. [CORREGIDO 2026-07-25: el v4.0 original decía 100%; la auditoría Ronda 6 fija el consenso estricto en 76.7%, no 100% laxo]"
assert old_t3 in s
s=s.replace(old_t3,new_t3)

# 2) Marcar C3 como RETIRADO en el catalogo (linea ~1614)
old_c3="#### **C3 — Phase-Hijacking por Valencia** (Predicción central DSCN-G-BIO)"
new_c3="#### **C3 — Phase-Hijacking por Valencia** (RETIRADO en Ronda 6, 2026-07-24 — NO SOSTENIDO a parámetros originales: 0.9% triggers, ΔPLV≈0; rediseño llega a 30.2%, lejos de \"la norma\". Se mantiene como Predicción histórica, no como claim activo)"
assert old_c3 in s
s=s.replace(old_c3,new_c3)

# 3) Aclarar T1 N_ss* en el resumen de valores (si aparece 9-10 o similar)
if "9–10" in s or "9-10" in s:
    s=s.replace("9–10","4–5 (el 9–10 es del N-back v6, no de T1)").replace("9-10","4-5 (el 9-10 es del N-back v6, no de T1)")

open(p,"w").write(s)
print("v4.0 actualizado: T3->76.7%, C3->RETIRADO, aclaracion T1 N_ss*.")
