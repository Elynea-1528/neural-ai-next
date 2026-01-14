# SupportError Kivételek

## Áttekintés

A `support_error.py` modul definiálja a D02 Support/Resistance processzor modul specifikus kivételeit. Minden kivétel a `SupportError` alap osztályból örököl, amely biztosítja az egységes hibakezelést és naplózást.

## Kivétel Hierarchia

```
SupportError (Exception)
├── SwingPointCalculationError
├── SupportResistanceLevelError
└── TimeframeConfigurationError
```

## SupportError (Alap Kivétel)

### Leírás
Az alap kivétel osztály minden support/resistance számítással kapcsolatos hiba számára.

### Attribútumok
- `message`: str - Részletes hibaüzenet
- `error_code`: str | None - Opcionális hibakód kategorizáláshoz

### Használat
```python
raise SupportError("Általános support processor hiba", "GENERAL_ERROR")
```

## SwingPointCalculationError

### Leírás
Swing pont számítási hibák esetén dobódik. Ez tartalmazhatja a rolling window műveletek vagy érvénytelen adatok miatti hibákat.

### Attribútumok
- `window_size`: int | None - Használt rolling window méret
- `column_name`: str | None - Érintett oszlop neve

### Error Code
`"SWING_POINT_CALCULATION_ERROR"`

### Használat
```python
raise SwingPointCalculationError(
    "Swing high számítás sikertelen",
    window_size=5,
    column_name="mid_high"
)
```

## SupportResistanceLevelError

### Leírás
Support vagy resistance szintek aggregálási hibái esetén dobódik. Ez tartalmazhatja az átlagolási műveletek vagy érvénytelen swing pont adatok miatti hibákat.

### Attribútumok
- `level_type`: str | None - Szint típusa ("support" vagy "resistance")
- `aggregation_method`: str | None - Használt aggregációs módszer

### Error Code
`"SUPPORT_RESISTANCE_LEVEL_ERROR"`

### Használat
```python
raise SupportResistanceLevelError(
    "Resistance szint aggregálás sikertelen",
    level_type="resistance",
    aggregation_method="rolling_mean"
)
```

## TimeframeConfigurationError

### Leírás
Timeframe-specifikus konfigurációs hibák esetén dobódik. Ez akkor történik, ha a swing_window vagy min_distance paraméterek érvénytelenek vagy hiányoznak.

### Attribútumok
- `timeframe`: str | None - Érintett timeframe
- `config_key`: str | None - Hiányzó vagy érvénytelen konfigurációs kulcs

### Error Code
`"TIMEFRAME_CONFIGURATION_ERROR"`

### Használat
```python
raise TimeframeConfigurationError(
    "Érvénytelen swing_window érték H4 timeframe-hez",
    timeframe="H4",
    config_key="swing_window"
)
```

## Gyakori Használati Példák

### Konfigurációs Validáció
```python
if swing_window <= 0:
    raise TimeframeConfigurationError(
        f"swing_window értéknek pozitívnak kell lennie: {swing_window}",
        timeframe=timeframe,
        config_key="swing_window"
    )
```

### Swing Pont Számítás Hiba
```python
try:
    swing_highs = df["mid_high"].rolling_max(window_size)
except Exception as e:
    raise SwingPointCalculationError(
        f"Swing high számítás sikertelen: {str(e)}",
        window_size=window_size,
        column_name="mid_high"
    )
```

### Szint Aggregálás Hiba
```python
try:
    resistance_levels = swing_highs.rolling_mean(window_size)
except Exception as e:
    raise SupportResistanceLevelError(
        f"Resistance szint aggregálás sikertelen: {str(e)}",
        level_type="resistance",
        aggregation_method="rolling_mean"
    )
```

## Testing

A kivételek teljes unit test lefedettséggel rendelkeznek (`100%` coverage):

- Kivétel létrehozás tesztelése
- Attribútumok validációja
- Öröklődési kapcsolatok tesztelése
- Error code helyesség ellenőrzése

## Error Code Referencia

| Error Code | Kivétel | Leírás |
|------------|---------|--------|
| `SWING_POINT_CALCULATION_ERROR` | `SwingPointCalculationError` | Swing pont számítási hibák |
| `SUPPORT_RESISTANCE_LEVEL_ERROR` | `SupportResistanceLevelError` | Szint aggregálási hibák |
| `TIMEFRAME_CONFIGURATION_ERROR` | `TimeframeConfigurationError` | Konfigurációs hibák |

## Kapcsolódó Modulok

- [`D02SupportProcessor`](implementations/support_processor.md): Processor implementáció amely ezeket a kivételeket használja
- [`D02SupportFactory`](factory.md): Factory amely kivételeket kezelhet inicializálás során