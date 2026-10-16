# Dominio: Bioacústica (Columba livia) — validación de la ley ρ en señal real

**Fuente:** Paloma-π v2 + FHRR rho-collapse (comparten el resonator puro)

## El patrón encontrado

- Decoder con Gram (gram/pinv) falla en ρ=1 (colapso).
- Resonator puro: 100% en todo el grid (FHRR y HRR real).
- En audio real de paloma: 6/6 roles recuperados = 1.000 en 83 clips.
- Secuencias temporales: la trayectoria del pitch se recupera ventana a ventana.

**Análogo de la ley ρ:** la señal de la paloma *contiene* la estructura
(pitch, ritmo, individuo). Los análisis clásicos (espectro, PCA) la ven
parcialmente; el resonator puro la ve completa. El "colapso" del análisis
clásico es del observador, no del ave.

**Validación pendiente:** BORIS (etograma conductual) dirá si los símbolos
recuperados correlacionan con conductas observables.
