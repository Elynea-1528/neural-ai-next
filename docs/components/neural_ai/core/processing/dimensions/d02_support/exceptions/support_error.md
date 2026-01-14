# SupportError kivételek

## Áttekintés

A `support_error.py` modul tartalmazza a D02 Support/Resistance processzor specifikus kivételeit.

## Kivételek hierarchiája

```
SupportError (alap kivétel)
├── SwingPointCalculationError
├── SupportResistanceLevelError
└── TimeframeConfigurationError
```

## SupportError

Alap kivétel osztály minden support/resistance hibához.

### Attribútumok

- `error_code`: Opcionális hibakód a hibák kategorizálásához

## SwingPointCalculationError

Swing pont számítási hibák esetén dobódik.

### Attribútumok

- `window_size`: A használt rolling window mérete
- `column_name`: Az érintett oszlop neve

## SupportResistanceLevelError

Support/resistance szint aggregációs hibák esetén dobódik.

### Attribútumok

- `level_type`: A szint típusa ("support" vagy "resistance")
- `aggregation_method`: A használt aggregációs módszer

## TimeframeConfigurationError

Timeframe-specifikus konfigurációs hibák esetén dobódik.

### Attribútumok

- `timeframe`: Az érintett timeframe
- `config_key`: A hiányzó vagy érvénytelen konfigurációs kulcs