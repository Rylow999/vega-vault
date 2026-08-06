---
name: html_js_sim_pitfalls
description: Pitfalls y receta para el demo HTML/JS autónomo (canvas, loop infinito) del sim SGM, cuando no hay node/browser para validar en el Android. De sgm_sim.html (2026-08-04).
---

# HTML/JS sim autónomo — pitfalls (de sgm_sim.html, 2026-08-04)

Cuándo usar ESTE enfoque en vez de `templates/grid_html_demo_template.py` (que embebe frames de Python
grabados): cuando el user quiere un sim VIVO e INFINITO (loop `requestAnimationFrame`) que corra en el
browser del PC/celular sin server. Escribís el sim COMPLETO en JS, portado de los stages de Python ya
validados (testeados UNO POR UNO: mundo+energía → búsqueda junta → lenguaje → identidad).

## Bugs que rompieron el primer intento ("ni la grilla se ve")
1. **Script antes del DOM** → `document.getElementById("cv")` da null → nada pinta. FIX: envolver TODO en
   `window.addEventListener("load", function(){ ... })`.
2. **Fallo silencioso** → pantalla en blanco sin pista. FIX: `window.onerror=function(msg,src,line){...}` +
   `try{...}catch(e){showErr(e.stack)}` que escribe en un `<div id="err">` visible. Si falla, el user
   LEE el error en vez de quedarse ciego.
3. **No distinguir "canvas roto" de "lógica crasheó"**. FIX: `drawGrid()` pinta la grilla completa
   (líneas tenues) INMEDIATAMENTE al cargar, antes del loop. Si la grilla se ve y los agentes no →
   error de lógica (ver #err). Si ni la grilla → el script no corrió.
4. **`last_pos` null** → primera llamada a `step` hace `this.last_pos[0]` con last_pos=null → TypeError.
   FIX: inicializar `this.last_pos=[x,y]` en el constructor.
5. **Helper `int()` usado antes de definirse** (aunque las function declarations hoistean, ensucia). Usar
   `Math.floor()` directo; no depender de helpers propios en código top-level.
6. **`Set` + `for...of`** funciona en JS moderno, pero para robustez en viewers viejos usar objetos
   planos `{}` con claves string (`walls[key(p)]=true`) en vez de `new Set()`.
7. **Pasar `null` como parámetro que no se usa** (ej `step(world=null,...)`) es inofensivo pero confunde;
   borrar el parámetro muerto.

## Validar JS SIN node (el Android no tiene node)
- **NO usar `python compile(js)`** → da FALSE POSITIVES (`const` → "invalid decimal literal", porque
  Python no parsea JS). No confíes en ese check.
- Check confiable: `Counter(js)` de `{} () []` → deben balancear (ej 63/63, 231/231, 111/111); afirmar
  que `requestAnimationFrame` y `loop();` están presentes; afirmar que no quedan llamadas `int(`;
  `"use strict"` ayuda a superficiar errores en el browser.
- La ÚNICA prueba real es abrir en browser. En Android el viewer de archivos del sistema a menudo NO
  ejecuta JS → abrir con **Chrome** (o `python3 -m http.server` en PC y entrar por IP). Si el panel
  #err muestra "ERROR: ...", copiar ese texto para arreglar.

## Esqueleto robusto (copy-modify)
Armar desde cero con: load-wrapper + try/catch + drawGrid-al-principio + init de last_pos + objetos
planos + sin helpers colgados. Mantener el loop con `if(!paused){...} requestAnimationFrame(loop)` y
un botón Pausar/Seguir. Indicadores en tiempo real vía `getElementById(...).textContent` (tick#, pos,
energía con barra, modo, traits fijos, último mensaje decodificado, % acierto, encuentros junta).
