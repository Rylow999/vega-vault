import re
base="/sdcard/Hermes/nexus-vault/TRIADA_AUTORREGULACION/"
for fn in ["TRIADA_Autorregulacion_Disipativa.md","RESOLUCION_FINAL.md"]:
    p=base+fn
    s=open(p).read()
    s=s.replace("2^phi~3.694","2^phi=3.069 (CORREGIDO: antes decia 3.694, error de calculo; 2^phi real = 3.069)")
    s=s.replace("en (1,3.694)","en (1, 3.069)")
    s=s.replace("2^phi~3.694 es el limite donde","2^phi=3.069 es el limite donde")
    open(p,"w").write(s)
    print("Corregido:",fn)
