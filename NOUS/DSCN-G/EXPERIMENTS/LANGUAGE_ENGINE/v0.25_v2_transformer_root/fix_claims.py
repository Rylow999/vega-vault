p="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/CLAIMS_STATUS.md"
s=open(p).read()
old="| Dinámica discreta — relación con el núcleo | EXTENSIÓN | ⚠️ Hipótesis — sin contenido aún, ver `EXTENSIONS/DISCRETE_DYNAMICS/` |"
new="| Dinámica discreta — relación con el núcleo (Tríada disipativa) | EXTENSIÓN | ✅ Marco formalizado 2026-07-25: DSCN-G = capa cognitiva de la Tríada (fase φ_i + vector ω_i → vitalidad V_i). Conecta con DDSD/Collatz/NS/Riemann por disipación. Ver `EXTENSIONS/DISCRETE_DYNAMICS/README.md` y `/TRIADA_AUTORREGULACION/` |"
assert old in s, "fila no encontrada"
s=s.replace(old,new)
# tambien actualizar el resumen de conteo al final si menciona "sin contenido"
open(p,"w").write(s)
print("CLAIMS_STATUS.md actualizado: Dinamica discreta -> formalizada via Triada.")
