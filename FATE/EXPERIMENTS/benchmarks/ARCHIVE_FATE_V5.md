# Archivar FATE v5 - Proyecto Finalizado

**Fecha:** 2026-07-19  
**Estado:** ✅ COMPLETADO (v5 es histórico, v6 es el activo)

---

## Comandos para archivar (ejecutar con gh CLI autenticado)

```bash
# Archivar el repo (read-only, no se pueden hacer push nuevos)
gh repo archive Rylow999/fate-v5-stable --confirm

# Verificar que está archivado
gh repo view Rylow999/fate-v5-stable | grep -i archived
```

## Alternativa manual (GitHub Web)

1. Ir a https://github.com/Rylow999/fate-v5-stable
2. Settings → Scroll al final → "Danger Zone"
3. Click en "Archive this repository"
4. Confirmar escribiendo el nombre del repo

---

## Motivo

FATE v5 fue el prototype que validó la topología cognitiva:
- ✅ Moving peaks: 0.86-0.93 (D=10)
- ✅ Pipe mode funcional
- ✅ Oracle ChEMBL embebido

**Pero v6 lo supera en todo:**
- ✅ Moving peaks: **0.998** (D=10) — +15% mejora
- ✅ Batch protocol: 10× throughput
- ✅ Arquitectura modular
- ✅ Pipe mode bidireccional funcionando

**v5 queda como referencia histórica, v6 es el producto final.**

---

**Nota:** Archivar no elimina el repo, solo lo hace read-only. El código sigue disponible para consulta.