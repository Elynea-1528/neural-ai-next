# Processor Konfigurációs Fájl

A `configs/processors.yaml` fájl tartalmazza a dimenzió processzorok konfigurációs beállításait a neural-ai-next rendszerben.

## Struktúra

```yaml
processors:
  d01:
    required_timeframes: ["tick", "1m", "5m", "15m", "1h", "4h", "1d"]

    timeframe_configs:
      tick:
        z_score_window: 2000
      1m:
        z_score_window: 60
      # ... többi timeframe config

    z_score_window: 60
    calc_shadows: true
```

## Konfigurációs Paraméterek

### required_timeframes
- **Típus:** Lista (string-ek)
- **Leírás:** Azon timeframe-ek listája, amelyeket a processzor támogat és feldolgoz
- **Értékek:** ["tick", "1m", "5m", "15m", "1h", "4h", "1d"]

### timeframe_configs
- **Típus:** Dictionary
- **Leírás:** Timeframe-specifikus konfigurációs paraméterek
- **Alparaméterek:**
  - **z_score_window:** Az ablakméret a rollázó Z-score számításához (int)
    - tick: 2000 (nagyobb ablak tick adatoknál stabilitás miatt)
    - 1m: 60 (standard 1 perces ablak)

### z_score_window
- **Típus:** Integer
- **Leírás:** Általános Z-score ablakméret, ha timeframe-specifikus nincs definiálva
- **Alapértelmezett:** 60

### calc_shadows
- **Típus:** Boolean
- **Leírás:** Meghatározza, hogy számítsák-e az árnyékokat (shadows) az OHLC adatoknál
- **Alapértelmezett:** true

## Használat

A konfigurációt a `ConfigManagerInterface` olvassa be és adja át a dimenzió processzoroknak. A processzorok timeframe alapján választják ki a megfelelő konfigurációs értékeket a `timeframe_configs` szekcióból, vagy használják az általános értékeket.