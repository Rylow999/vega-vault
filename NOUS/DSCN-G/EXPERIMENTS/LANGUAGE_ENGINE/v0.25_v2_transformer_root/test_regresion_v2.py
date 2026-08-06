#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regresión mínima: comparar run_v25_v2.py vs run_v25_v2_core.py por métricas canónicas."""
import json, os
from dscng_core import MetricLogger

keys=["acc_pred_avg","acc_gt_avg","dolor_avg","foco_acc_avg","W_actual_avg","steps"]
orig=json.load(open("results_v25_v2.json"))
core=json.load(open("results_v25_v2_core.json"))
o=orig if "summary" not in orig else orig["summary"]
c=core["summary"]
print("orig:", {k:o.get(k) for k in keys})
print("core:", {k:c.get(k) for k in keys})
# diferencia relativa tolerada
for k in keys:
    a,b=o.get(k,0.0),c.get(k,0.0)
    if a==0 and b==0: continue
    if abs(a-b)/max(abs(a),1e-9) > 0.05:
        print("REGRESION", k, a, b)
print("REG_OK")
