# SGM SIM — HTML canvas portable (técnica + receta de movimiento funcional)

Cuando Luciano pide "simulador", "demo in vivo", "visualización a gran escala", o ver el
sistema andando, el entregable es un **HTML autónomo con `<canvas>`** (JS embebido, sin
server, sin matplotlib, sin CORS). En el Android NO hay `node`, así que no se puede ejecutar
el browser para validar; la estrategia honesta es: (1) testear la LÓGICA en Python headless
primero, (2) portar fielmente a JS, (3) validar sintaxis del JS por balance de llaves/paréntesis
(Python `compile()` NO sirve para JS — da falsos errores), (4) envolver en `window.onload` +
`try/catch` + `window.onerror` para que cualquier error se imprima en pantalla (no pantalla en blanco).

## Reglas duras del HTML (aprendidas 2026-08-04, sesión del sim)
- **`window.addEventListener("load", ...)`** para correr el script DESPUÉS de que el DOM
  (canvas, panel) exista. Si el canvas se busca antes, `getContext` da null y nada pinta.
- **`try/catch` + `window.onerror`** escriben el error en un `<div id="err">` rojo. Si el
  usuario abre el archivo y "no se ve nada", el panel de error le dice exactamente qué falló
  (en vez de pantalla muerta). Esto es OBLIGATORIO porque no podemos depurar el browser.
- **Dibujar la GRILLA primero** (`drawGrid()` con líneas tenues) al cargar, así siempre se ve
  la estructura aunque los agentes no aparezcan. Confirma que el canvas funciona.
- **No pasar `world=null`** si el step lo usa; o quitar el parámetro. En la V1 se pasaba
  `null` y se confiaba en globals — frágil. Mejor: funciones globales `blocked()`, `objAt()`.
- **`"use strict"`** para que errores semánticos (no solo sintaxis) estallen temprano.
- **Validar balance** antes de entregar: `Counter(js)` de `{ } ( ) [ ]` debe ser par; contar
  `requestAnimationFrame`, `loop();`, y que no quede ningún `int(` suelto (usar `Math.floor`).
- **Cópialo al vault con `su -c 'cp ... /sdcard/...'`** — el `cp` plano da "Permission denied"
  por FUSE; el `su -c` sí escribe.

## Receta de MOVIMIENTO FUNCIONAL (el bug que Luciano detectó y corrigió)
SÍNTOMA que el usuario reportó: "se quedan sin energía muy rápido, se ven aleatorios, a veces
quedan en bucle, mueren de inanición". Eso era un **walker ciego**: el agente elegía la celda
vecina con mayor peso local donde el peso de comida era +3 y decaía rápido → vagaba al azar,
oscilaba, y se moría. NO era un detalle visual; era la lógica de búsqueda.

FIX validado en Python (5 seeds, 3000 ticks, 0 bucles, 1-5 muertes) y portado al HTML:
1. **Memoria de comida (huella ω de SGM):** al ver comida, `mem_comida[pos]=1.0` con
   `decay 0.995` lento. El agente RECUERDA dónde vio comida (no hardcodear "andá ahí").
2. **Visión (radio 3):** ve comida a distancia 3 y la usa como META dirigida. No camina ciego.
3. **Dirección de exploración persistente:** si no hay comida conocida, avanza en UNA dirección
   consistente (`dir_explora`) en vez de random → no se queda en un cuadrante.
4. **Anti-bucle real:** volver a `last_pos` penaliza **-8** (antes -1, insuficiente). Si todas
   las opciones son peores, gira `dir_explora`.
5. **Energía suave:** `COST=0.15/tick`, `FOOD=+40`, `WATER=+20`, `POISON=-20` (+dolor).
   (En la V1 era COST=1.0/FOOD=+20 → se moría al toque.)

Resultado del test Python (honesto):
```
seed=20260803 -> muertes=4,  loops=0, energy_final=90.2
seed=777      -> muertes=5,  loops=0, energy_final=40.4
seed=12345    -> muertes=1,  loops=0, energy_final=0.0
seed=999      -> muertes=3,  loops=0, energy_final=20.1
seed=4242     -> muertes=2,  loops=0, energy_final=50.1
```
Cero bucles, supervivencia sostenida. El agente busca de verdad.

## Preferencias de Luciano para el sim (embebidas, no negociables)
- **Infinito por defecto**: sin tope de ticks; si el user quiere acotar, él lo dice.
- **Mostrar TODO**: veneno (rojo), agua (azul), comida (verde), señal del emisor (naranja),
  agente A (amarillo), agente B (morado), y traits fijos en el panel. Incluir leyenda.
- **Velocidad regulable**: sliders de `ticks/frame` (1-20) y `delay` (0-200ms). Con delay alto
  se ve casi paso a paso. Usar `setTimeout(loop, delay)` cuando delay>0, si no `requestAnimationFrame`.
- "Bonito y funciona": el sim debe verse limpio y la lógica debe ser funcional, no cosmética.

## Checklist antes de entregar el HTML
- [ ] Lógica testeada en Python headless (supervivencia + sin bucles medidos).
- [ ] `window.onload` + `try/catch` + `window.onerror` -> panel `#err`.
- [ ] `drawGrid()` pinta grilla al cargar.
- [ ] Balance de llaves/paréntesis/corchetes = par.
- [ ] Sin `int(` suelto; `Math.floor` en su lugar.
- [ ] Copiado al vault con `su -c cp`.
- [ ] Avisar al user: abrir con Chrome (el visor de archivos del celular a menudo no ejecuta JS).
