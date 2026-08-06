# Demo HTML portable para experimentos SGM (exp_SGM_0032/0033, Camino A)

Patrón para generar una demo visual IN VIVO de un agente/simulación SGM SIN servidor, SIN CORS,
SIN dependencias: el script Python corre la simulación, recolecta un frame por tick, y escribe un
`demo_xxx.html` con TODOS los frames embebidos en un `const DATA = {...}` de JavaScript. El usuario
abre el archivo y ve la animación con canvas + indicadores en tiempo real + play/pause/slider.

## Por qué este patrón (en Android no hay backend de ventana, matplotlib no sirve)
- En el celular no hay servidor ni navegador headless cómodo. Un mini-HTTP server + `fetch` sufre de
  CORS y de que el usuario tenga que levantar el server. Embeber los datos en el HTML lo evita: el
  archivo es autosuficiente y se abre desde cualquier gestor de archivos / navegador.
- `write_file` de Hermes funciona en /data/user/0/.../home; el HTML se escribe ahí y se copia al vault
  con `cp` + `chown root:everybody` + `chmod 664` (FUSE en /sdcard).

## Estructura del script Python (`run_demo_html.py`)
1. `sys.path.insert(0, dirname(__file__))` + `import run_grid_dolor as G` / `import run_grid_agent as G2`
   para reusar los `GridAgent` ya validados (NO re-implementar la simulación).
2. `run_scenario_XXXX()`: instancia el agente con `random.Random(SEED)` fijo, corre tick a tick,
   y en cada tick hace `snapshot()` que lee `ag.history[-1]` (debe tener tick/pos/dist/E/dolor/masa/huella/reached)
   y acumula `visitas[(r,c)]` (para dibujar huella con opacidad). Guarda `frames=[]`.
3. Construye `layout` (matriz de chars: 'W' pared, 'D' dolor, 'G' meta, 'B' inicio, '.' libre) UNA vez.
4. `write_html(layout, frames, meta, body, dolor, visitas, out_path, title)`:
   - `data = {W,Ht,layout,frames,meta,body,dolor,visitas,seed}`
   - `html = HTML_TEMPLATE.replace("/*__DATA__*/", json.dumps(data, ensure_ascii=False))`
   - reemplaza el <title> por el del scenario.
5. `HTML_TEMPLATE` es un string con `<canvas>` + panel de indicadores + controles
   (play/pause/slider de tick/velocidad) y un `<script>` que hace `draw(i)` por frame.

## Fragmento del HTML_TEMPLATE (lo esencial)
```html
<canvas id="cv" width="480" height="480"></canvas>
<script>
const DATA = /*__DATA__*/;
const cv = document.getElementById('cv'); const ctx = cv.getContext('2d');
const cell = cv.width / DATA.W;
let idx = 0, playing = false, timer = null;
function draw(i){
  const f = DATA.frames[i];
  ctx.clearRect(0,0,cv.width,cv.height);
  for(let r=0;r<DATA.Ht;r++) for(let c=0;c<DATA.W;c++){
    const ch = DATA.layout[r][c];
    ctx.fillStyle = ch==='W' ? '#30363d' : ch==='D' ? '#7d1f1f' :
                   ch==='G' ? '#1f5f2f' : ch==='B' ? '#1f3a5f' : '#0d1117';
    ctx.fillRect(c*cell, r*cell, cell-1, cell-1);
    const vk = r+','+c;
    if(DATA.visitas[vk]){ const a=Math.min(0.5,DATA.visitas[vk]*0.08);
      ctx.fillStyle='rgba(240,200,60,'+a+')'; ctx.fillRect(c*cell,r*cell,cell-1,cell-1); }
  }
  const [pr,pc]=f.pos; ctx.fillStyle='#58a6ff';
  ctx.beginPath(); ctx.arc(pc*cell+cell/2, pr*cell+cell/2, cell*0.35, 0, 2*Math.PI); ctx.fill();
  // indicadores: i_tick,i_pos,i_dist,i_E,i_dolor,i_masa,i_huella,i_reached
  slider.value = i;
}
function tickStep(){ if(idx>=DATA.frames.length-1){playing=false;clearInterval(timer);return;} idx++; draw(idx); }
play.onclick=()=>{ if(playing)return; playing=true; const sp=+speed.value; timer=setInterval(tickStep,1000/sp); };
pause.onclick=()=>{ playing=false; clearInterval(timer); };
slider.oninput=(e)=>{ idx=+e.target.value; draw(idx); };
draw(0);
</script>
```

## Reglas
- El agente simulado DEBE exponer `history` con un dict por tick que incluya al menos
  `pos` (tuple), `dist`, `E`, `dolor`, `masa`, `huella`, `reached`, `tick`. Si no, adaptar snapshot().
- `frames` debe incluir el estado INICIAL (tick 0) para que el slider arranque en 0.
- Verificar el HTML escrito: `len(b)>0`, `'const DATA =' in b`, `b.rstrip().endswith('</html>')`,
  y que `json.loads(re.search(r'const DATA = (\{.*?\});', b, re.S).group(1))` parsea.
- Para dos demos (ej. grid con dolor + maze), generar DOS archivos (`demo_grid.html`, `demo_grid_maze.html`)
  con el mismo template pero distinto `title`.
- El HTML puede ser pesado si hay miles de frames; limitar frames (≤~60) o submuestrear ticks para demo.

## Veredicto de la sesión (0032/0033)
- demo_grid.html: grid abierto con zona de dolor (0033). demo_grid_maze.html: maze aleatorio 10×10 (0032, 32 paredes).
- Ambas llegan a meta; canvas + indicadores vivos + play/pause/slider. Abiertas desde el archivo, sin server.

## Mejoras vistas en demo_grid_0044.html (exp_SGM_0044, 2026-08-03)
La demo del sistema completo (frustración + dolor + HRR) sumó dos toques que mejoran la legibilidad y
vale reusar en futuras demos:
1. **Paleta synthwave + glow:** fondo radial oscuro, `ctx.shadowColor`/`shadowBlur` en agente (cian),
   comida (verde) y dolor (rojo) para que "brillen". Celdas visitadas en azul tenue (`#1b2552`),
   obstáculos gris. Esto hace la traza mucho más legible que el amarillo plano del template base.
2. **Estela de huella (últimos ~14 ticks):** dibujar un rect translúcido en las celdas de los últimos N
   pasos antes del agente, para ver el "camino" que recorrió, no solo la posición actual.
3. **Scrub robusto:** `scrub.oninput` setea `i` y pausa (`playing=false`); el botón play reinicia desde `i`.
   El panel lateral (tick/pos/celdas/comida/dolor/η/abur/retornos + barras + cobertura por cuadrante) se
   recalcula por tramo desde `TRAJ.slice(0,t+1)` (no precalculado) → el scrub es fiel a cualquier tick.
4. **Sin límite de frames para demo corta:** 0044 usó 300 ticks embebidos sin problema (HTML ~13-19KB).
   Para >1000 ticks, submuestrear como dice la regla general.
El generador quedó en `phases/phase7_composicion/run_demo_0044.py` (reusa World/Agent de 0044, NO
re-implementa la simulación). Plantilla de partida ya existe en `templates/grid_html_demo_template.py`.
