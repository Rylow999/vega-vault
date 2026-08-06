# Updating NOUS/DSCN-G from Tríada findings (freeze-safe recipe)

## Context (2026-07-25 session)
User asked: "actualicemos lo que hemos cambiado en DSCN-G dentro de NOUS y veamos qué
cosas cambian". The Tríada results lived in `/TRIADA_AUTORREGULACION/` (vault root),
NOT in NOUS. DSCN-G core is FROZEN v1.0 (Ronda 6). So the update touched only the
open/placeholder items, never the core paper or CORE claims.

## What changed (and what did NOT)
CHANGED:
- `NOUS/DSCN-G/EXTENSIONS/DISCRETE_DYNAMICS/README.md`
  Before: "Estado: PENDIENTE — carpeta placeholder, sin contenido propio todavía"
          + "No se fabrica contenido para llenarlo".
  After:  "Estado: CON CONTENIDO PARCIAL (actualizado 2026-07-25)"
          + documents DSCN-G = cognitive layer of the Tríada (φ_i + ω_i → V_i),
            link to DDSD/Collatz/NS/Riemann via dissipative confinement.
- `NOUS/DSCN-G/CLAIMS_STATUS.md` row:
  Before: "| Dinámica discreta — relación con el núcleo | EXTENSIÓN | ⚠️ Hipótesis — sin contenido aún, ver `EXTENSIONS/DISCRETE_DYNAMICS/` |"
  After:  "| Dinámica discreta — relación con el núcleo (Tríada disipativa) | EXTENSIÓN | ✅ Marco formalizado 2026-07-25: DSCN-G = capa cognitiva de la Tríada (fase φ_i + vector ω_i → vitalidad V_i). Conecta con DDSD/Collatz/NS/Riemann por disipación. Ver `EXTENSIONS/DISCRETE_DYNAMICS/README.md` y `/TRIADA_AUTORREGULACION/` |"

DID NOT CHANGE (state this explicitly to the user):
- `NOUS/DSCN-G/CORE/01_DSCN-G_Paper.md` — frozen v1.0, untouched.
- T1/T2/T3 claim statuses — already verified in Ronda 6, untouched.
- Φ_proxy O(log N) — still retired (Ronda 6); today reinforced that the real "Φ" of
  DSCN-G is vitality V_i, not the information-integration proxy.
- The Tríada stays marked COMPARATIVE, not CORE, because cross-domain quantitative
  prediction is still NEGATIVE (bounds independent — reviewer Point 4).

## Recipe (reusable)
1. Map: `su -c 'cd /sdcard/Hermes/nexus-vault && find NOUS/DSCN-G -name "*.md"'`
   + grep for the new result's keywords to see what references it.
2. For a full-file rewrite (README): write with Hermes `write_file` to Hermes home,
   then `su -c 'cp /data/data/com.hermesagent.android/files/home/<f> /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXTENSIONS/DISCRETE_DYNAMICS/README.md'`.
3. For a single table-row edit (CLAIMS_STATUS): write a tiny Python assert-script:
   ```python
   p="/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/CLAIMS_STATUS.md"
   s=open(p).read()
   old="| Dinámica discreta — relación con el núcleo | EXTENSIÓN | ⚠️ Hipótesis — sin contenido aún, ver `EXTENSIONS/DISCRETE_DYNAMICS/` |"
   new="| Dinámica discreta — relación con el núcleo (Tríada disipativa) | EXTENSIÓN | ✅ Marco formalizado 2026-07-25: ... |"
   assert old in s, "fila no encontrada"
   s=s.replace(old,new)
   open(p,"w").write(s)
   print("ok")
   ```
   Run via `su -c 'export LD_LIBRARY_PATH=/data/data/com.hermesagent.android/files/usr/lib; /data/data/com.hermesagent.android/files/usr/bin/python3 /data/data/com.hermesagent.android/files/home/<script>.py'`.
   The `assert old in s` makes a wrong old_string fail loudly instead of silently
   corrupting the markdown table.
4. Verify: `su -c 'grep -niE "dinamica discreta|triada" /sdcard/Hermes/nexus-vault/NOUS/DSCN-G/CLAIMS_STATUS.md'`.

## Pitfall
Do NOT "upgrade" the Tríada into the CORE just because it now has content. The
cross-domain quantitative prediction (Point 4) is still NEGATIVE — no formula derives
one domain's bound from another's. Keep it EXTENSIÓN / comparative until that changes.
