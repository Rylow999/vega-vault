#!/usr/bin/env bash
# DSCN-G v3 — pipeline completo (auditado y corregido, 2026-07-22)
#
# Uso:
#   bash run_pipeline.sh            # escala canónica (seeds=30, steps=2000) — ~3-4 min
#   bash run_pipeline.sh --quick    # smoke test (seeds=5, steps=500) — ~20 s
#
# Genera, en este orden (cada paso depende del anterior):
#   1. verification_results_v3.json   (verify_dscng_v3.py)
#   2. nback_v5_paper_ready.json      (nback_v5_grounded.py)
#   3. figure2_nback_v5_paper.png     (generate_figure2.py)
#   4. salida de consola con el resumen final (analyze_results.py)
#
# IMPORTANTE: antes de este audit, el paso 2 no escribía ningún archivo,
# así que el paso 3 y el paso 4 (mitad "nback") fallaban siempre con
# FileNotFoundError si se seguían las instrucciones del README original al
# pie de la letra. Ver AUDIT_NOTES.md para el detalle completo de qué se
# encontró y qué se corrigió.

set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--quick" ]]; then
    echo "=== Modo quick (seeds=5, steps=500) ==="
    python3 verify_dscng_v3.py --quick
else
    echo "=== Modo canónico (seeds=30, steps=2000) ==="
    python3 verify_dscng_v3.py --seeds 30 --steps 2000
fi

echo
echo "=== N-back grounded (n-back hasta 15, como cita el paper) ==="
python3 nback_v5_grounded.py --n-backs 1 2 3 4 5 6 8 10 12 15 --n-trials 40

echo
echo "=== Generando Figura 2 ==="
python3 generate_figure2.py

echo
echo "=== Análisis final ==="
python3 analyze_results.py
