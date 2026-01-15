# Processors Configuration Dokumentáció

## Áttekintés
Ez a konfigurációs fájl (`configs/processors.yaml`) tartalmazza a dimenzió processzorok (D1-D15) beállításait a Neural AI rendszerben.

## Struktúra
- `processors`: A fő konfigurációs objektum
  - `d01`: D1 dimenzió (alap adatok) konfiguráció
  - `d02`: D2 dimenzió (Support/Resistance) konfiguráció

## D02 - Support/Resistance Paraméterek
- `swing_window`: Az ablakméret a swing pontok kiszámításához (alapértelmezett: 5)
- `min_distance`: Minimális távolság a szintek között (alapértelmezett: 10)
- `use_close_open`: Használja-e a close/open árakat (alapértelmezett: true)
- `use_high_low`: Használja-e a high/low árakat (alapértelmezett: true)
- `primary_weight`: Elsődleges súlyozás (alapértelmezett: 0.7)
- `secondary_weight`: Másodlagos súlyozás (alapértelmezett: 0.3)
- `level_merge`: Szintek egyesítésének küszöbe (frissítve: 0.0005)
- `min_touches`: Minimális érintések száma a szint érvényesítéséhez (új: 2)
- `volume_confirmation`: Volumen megerősítés használata (frissítve: true)
- `strength_window`: Erősség ablakának mérete (új: 100)
- `timeframe_configs`: Időkeret specifikus beállítások
  - `M1`, `H1`, `D1`: Swing window beállítások különböző időkeretekre

## Használat
Ez a konfiguráció betöltődik a rendszer indulásakor és használatos a processzorok inicializálásához.