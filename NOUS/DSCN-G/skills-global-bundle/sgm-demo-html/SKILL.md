---
name: sgm-demo-html
description: Demo visual SGM en el browser SIN server (HTML + canvas + JS autónomo, loop infinito con requestAnimationFrame). Cubre cuándo usar este enfoque vs templates/grid_html_demo_template.py (frames grabados), los pitfalls que dejan la pantalla en blanco en el Android (sin node para validar), y cómo validar el JS sin browser. Usar cuando Luciano pida "demo in vivo", "sim HTML", "para mostrar en vivo", o un sim infinito portable.
---

# SGM Demo HTML/JS autónomo (sin server)

Proyecto: SGM-CORE en `/sdcard/Hermes/nexus-vault/NOUS/DSCN-G/EXPERIMENTS/SGM/phases/phase7_composicion/sim/sgm_sim.html`.
El sim VIVE en el browser (PC o celular con Chrome). No hay server, no matplotlib (prohibido en celular).

## Cuándo usar ESTE enfoque
- El user quiere un **sim INFINITO en vivo** (loop `requestAnimationFrame`), no una animación de frames
  grabados. → escribir el sim COMPLETO en JS, portado de los stages de Python ya validados (testeados
  UNO POR UNO: mundo+energía+respawn → búsqueda junta → lenguaje → identidad).
- Si solo querés una visualización de UNA corrida ya hecha → usá `templates/grid_html_demo_template.py`
  (embebe frames en JS). No reinventes el loop.

## PITFALLS que dejaron "ni la grilla se ve" (sgm_sim.html, 2026-08-04)
1. **Script antes del DOM** → `getElementById("cv")` es null → nada pinta. FIX: envolver TODO en
   `window.addEventListener("load", function(){ ... })`.
2. **Fallo silencioso** → pantalla en blanco sin pista. FIX: `window.onerror=function(msg,src,line){...}` +
   `try{...}catch(e){showErr(e.stack)}` que escribe en `<div id="err">`. Si falla, el user LEE el error.
3. **No distinguir "canvas roto" de "lógica crasheó"**. FIX: `drawGrid()` pinta la grilla completa
   (líneas tenues) INMEDIATAMENTE al cargar, antes del loop. Si la grilla se ve y los agentes no →
   error de lógica (ver #err). Si ni la grilla → el script no corrió.
4. **`last_pos` null** → primer `step` hace `this.last_pos[0]` con null → TypeError. FIX: inicializar
   `this.last_pos=[x,y]` en el constructor.
5. **Helper `int()` usado antes de definirse**. Usar `Math.floor()` directo.
6. **`Set` + `for...of`** funciona en JS moderno, pero para robustez en viewers viejos usar objetos
   planos `{}` con claves string (`walls[key(p)]=true`) en vez de `new Set()`.
7. **Pasar `null` como parámetro muerto** (ej `step(world=null,...)`) → borrarlo.

## Validar JS SIN node (el Android NO tiene node)
- **NO usar `python compile(js)`** → FALSE POSITIVES (`const` → "invalid decimal literal", Python no
  parsea JS). No confíes en ese check.
- Check confiable: `Counter(js)` de `{} () []` debe balancear (ej 63/63, 231/231, 111/111); afirmar que
  `requestAnimationFrame` y `loop();` están; que no quedan llamadas `int(`; `"use strict"` ayuda.
- La ÚNICA prueba real es abrir en browser. En Android el **viewer de archivos del sistema a menudo NO
  ejecuta JS** → abrir con **Chrome**, o `python3 -m http.server` en PC y entrar por IP. Si #err muestra
  "ERROR: ...", copiar ese texto para arreglar.
 
## REGLA DE ORO: validar la LÓGICA en Python ANTES de tocar el HTML (2026-08-04)
Luciano detectó hardcode en el movimiento del sim y lo rechazó ("hay hardcode en el sistema, resolvelo
o me encargo yo"). Lección de flujo:
1. **NUNCA ajustar números mágicos hasta que "el test pase".** Los pesos `w+=4/-3/+0.5/-8`, la
   "dirección favorita" `dir_explora`, el `0.3` de atracción, etc. son HARDCODE y van contra la regla de
   SGM ("el comportamiento debe EMERGIR del sustrato, no inyectarse"). Luciano los ve y los rechaza.
2. **Testear la mecánica en Python PRIMERO** (script `sim_sgm_stageN_test.py` que corra miles de ticks
   y mida métricas honestas: % mapa visitado, muertes, bucles detectados). Solo cuando el test Python
   sea bueno, portar a JS.
3. **Métrica anti-hardcode honesta:** si el agente se queda en esquina o en bucle, es hardcode
   (dirección favorita) o lógica ciega. El test debe reportar `pct_mapa` (poco => en esquina) y
   `bucles` (rebote). Sin esas métricas no sabés si "funciona".
4. **Movimiento reactivo puro que SÍ emerge (validado, sin hardcode):** huella ω de travesía
   (`omega[pos]` con decay 0.97 → penaliza repetir = anti-bucle EMERGENTE, SIN `-8` puesto a mano) +
   memoria de comida vista (atracción por cercanía geométrica `1/(1+d)`) + señal del otro (afinidad
   social 0054b). Test (8 seeds, 4000 ticks): pct_mapa 80-87%, bucles=0, muertes 0-1.
5. **No apurar:** Luciano pidió "no lo hagas a las apuradas... es importante que nos lleve el tiempo
   necesario". Ante un sim que no anda, DETENERSE, testear en Python, mostrar métricas, recién portar.
   No parchear el HTML a ciegas.
 
## Esqueleto robusto (copy-modify)
load-wrapper + try/catch + drawGrid-al-principio + init de last_pos + objetos planos + sin helpers
colgados. Loop: `if(!paused){...} requestAnimationFrame(loop)`. Botón Pausar/Seguir. Indicadores en
tiempo real vía `getElementById(...).textContent` (tick#, pos, energía con barra, modo, traits fijos,
último mensaje decodificado, % acierto, encuentros junta).

## Qué mostrar (sustrato ya validado que el sim debe exhibir)
- Composición de rasgos (0056, inferencia de regla, TopSim 0.86-1.0) y relacional (0058, TPR/HRR).
- Búsqueda junta EMERGENTE por afinidad (0054b: encuentros_juntos crecen solos).
- Identidad por irreversibilidad (0057: traits que se fijan y resisten el empuje del entorno).
- Indicadores: energía (barra), modo (EXPLORA/BUSCA/URGE), traits fijos, último mensaje compuesto,
  % acierto de decode, encuentros junta, identidad perdida.

Receta + bugs exactos en `references/html_js_sim_pitfalls.md` (del skill sgm-experiment-flow).
