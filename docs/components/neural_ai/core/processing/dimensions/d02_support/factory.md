# D02SupportFactory

## Áttekintés

A `D02SupportFactory` osztály felelős a `D02SupportProcessor` példányok létrehozásáért és konfigurációjáért. A factory minta implementációjával biztosítja a megfelelő dependency injection és konfiguráció kezelését.

## Architektúra

A factory osztály a `neural_ai.core.processing.dimensions.d02_support.factory` modulban található és a következő interfészeket használja:

- `ConfigManagerInterface`: Konfigurációs adatok kezelése
- `LoggerInterface`: Loggolás és monitoring
- `IDimensionProcessor`: A létrehozott processor interfésze

## Használat

```python
from neural_ai.core.processing.dimensions.d02_support.factory import D02SupportFactory

# Processor létrehozása factory-val
processor = D02SupportFactory.create(config, logger)

# Használat
result_df = processor.process(input_df, timeframe="H1")
```

## Konfiguráció

A factory a következő konfigurációs kulcsokat használja a processor inicializálásához:

- `swing_window`: Swing pontok detektálásához használt ablakméret (default: 5)
- `min_distance`: Minimum távolság a swing pontok között (default: 10)
- `timeframe_configs`: Timeframe-specifikus beállítások

## Példa Konfiguráció

```yaml
processing:
  dimensions:
    d02_support:
      swing_window: 5
      min_distance: 10
      timeframe_configs:
        h4:
          swing_window: 10
          min_distance: 20
        d1:
          swing_window: 15
          min_distance: 30
```

## Exception Handling

A factory a következő kivételeket dobhatja:

- `SupportError`: Általános support processor hibák
- `TimeframeConfigurationError`: Érvénytelen timeframe konfiguráció esetén

## Testing

A factory teljes unit test lefedettséggel rendelkezik (`100%` coverage), amely tartalmazza:

- Helyes típus visszaadása
- Új példány létrehozása minden hívásnál
- Dimension ID validáció
- Funkcionális működés tesztelése
- Timeframe-specifikus konfiguráció használata

## Kapcsolódó Modulok

- [`D02SupportProcessor`](implementations/support_processor.md): A létrehozott processor implementáció
- [`SupportError`](exceptions/support_error.md): Specifikus kivételek
- [`IDimensionProcessor`](../../interfaces/dimension_processor_interface.md): Processor interfész