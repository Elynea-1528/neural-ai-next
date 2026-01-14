# D02SupportProcessor

## Áttekintés

A `D02SupportProcessor` implementálja a D2 dimenzió processzort, amely support és resistance szintek kiszámítására szolgál swing pontok alapján különböző timeframe-eken keresztül.

## Architektúra

Az osztály a `BaseDimensionProcessor`-ből örököl és a következő interfészeket használja:

- `ConfigManagerInterface`: Konfigurációs adatok elérése
- `LoggerInterface`: Loggolás és monitoring
- `IDimensionProcessor`: Processor interfész implementáció

## Főbb Funkciók

### Swing Pont Detektálás

A processor swing high és swing low pontokat detektál rolling window maximum/minimum műveletekkel külön body (középső) és wick (teljes) részek számára:

#### Body Swing Pontok (mid árak alapján)
```python
swing_high_body = pl.when(pl.col("mid_high") == pl.col("mid_high").rolling_max(window_size=swing_window))
swing_low_body = pl.when(pl.col("mid_low") == pl.col("mid_low").rolling_min(window_size=swing_window))
```

#### Wick Swing Pontok (teljes árak alapján)
```python
swing_high_wick = pl.when(pl.col("high") == pl.col("high").rolling_max(window_size=swing_window))
swing_low_wick = pl.when(pl.col("low") == pl.col("low").rolling_min(window_size=swing_window))
```

### Support/Resistance Szintek Számítása

A swing pontokból aggregált szinteket számol rolling mean használatával külön body és wick számára:

- **Resistance Body**: Body swing high-ok átlaga
- **Support Body**: Body swing low-ok átlaga
- **Resistance Wick**: Wick swing high-ok átlaga
- **Support Wick**: Wick swing low-ok átlaga

## Konfiguráció

### Alap Konfiguráció

```yaml
processing:
  dimensions:
    d02_support:
      swing_window: 5      # Swing pont detektáláshoz használt ablakméret
      min_distance: 10     # Minimum távolság swing pontok között
```

### Timeframe-Specifikus Konfiguráció

```yaml
timeframe_configs:
  h1:
    swing_window: 5
    min_distance: 10
  h4:
    swing_window: 10
    min_distance: 20
  d1:
    swing_window: 15
    min_distance: 30
```

## Használat

```python
from neural_ai.core.processing.dimensions.d02_support.factory import D02SupportFactory

# Processor létrehozása
processor = D02SupportFactory.create(config, logger)

# Adatfeldolgozás
result_df = processor.process(input_df, timeframe="H1")

# Eredmény tartalmazza az új oszlopokat:
# - swing_high_body: boolean flag body swing high pontokra
# - swing_low_body: boolean flag body swing low pontokra
# - swing_high_wick: boolean flag wick swing high pontokra
# - swing_low_wick: boolean flag wick swing low pontokra
# - resistance_body: aggregált resistance szintek body alapján
# - support_body: aggregált support szintek body alapján
# - resistance_wick: aggregált resistance szintek wick alapján
# - support_wick: aggregált support szintek wick alapján
```

## Bemeneti Adatok

A processor a következő oszlopokat várja a bemeneti Polars DataFrame-ben:

- `timestamp`: Időbélyegek
- `mid_open`, `mid_high`, `mid_low`, `mid_close`: Mid árak
- `tick_volume`: Tick volumen
- `spread`: Spread értékek
- `real_volume`: Valós volumen

## Kimeneti Adatok

Az eredmény DataFrame tartalmazza az összes bemeneti oszlopot plusz:

- `swing_high_body`: `bool` - True body swing high pontoknál
- `swing_low_body`: `bool` - True body swing low pontoknál
- `swing_high_wick`: `bool` - True wick swing high pontoknál
- `swing_low_wick`: `bool` - True wick swing low pontoknál
- `resistance_body`: `float` - Aggregált resistance szintek body alapján
- `support_body`: `float` - Aggregált support szintek body alapján
- `resistance_wick`: `float` - Aggregált resistance szintek wick alapján
- `support_wick`: `float` - Aggregált support szintek wick alapján

## Algoritmus Részletek

### Swing Pont Detektálás

#### Body Swing Pontok (mid árak)
1. **Rolling Maximum**: Minden pontnál ellenőrzi, hogy az adott `mid_high` érték a legnagyobb-e az ablakban
2. **Rolling Minimum**: Minden pontnál ellenőrzi, hogy az adott `mid_low` érték a legkisebb-e az ablakban

#### Wick Swing Pontok (teljes árak)
1. **Rolling Maximum**: Minden pontnál ellenőrzi, hogy az adott `high` érték a legnagyobb-e az ablakban
2. **Rolling Minimum**: Minden pontnál ellenőrzi, hogy az adott `low` érték a legkisebb-e az ablakban

3. **Flag Generálás**: Boolean oszlopok létrehozása minden swing pont típusra

### Szint Aggregálás

1. **Resistance Body**: Body swing high-ok `rolling_mean(window_size=min_distance * 2)` aggregálása
2. **Support Body**: Body swing low-ok `rolling_mean(window_size=min_distance * 2)` aggregálása
3. **Resistance Wick**: Wick swing high-ok `rolling_mean(window_size=min_distance * 2)` aggregálása
4. **Support Wick**: Wick swing low-ok `rolling_mean(window_size=min_distance * 2)` aggregálása

## Performance

- **Polars Optimalizáció**: Zero-copy műveletek és vektorizált számítások
- **Memory Efficient**: O(n) idő és memória komplexitás
- **Configurable Windows**: Timeframe-ekhez igazított ablakméretek

## Exception Handling

A processor a következő kivételeket dobhatja:

- `SwingPointCalculationError`: Swing pont számítási hibák esetén
- `SupportResistanceLevelError`: Szint aggregálási hibák esetén
- `TimeframeConfigurationError`: Érvénytelen timeframe konfiguráció esetén

## Testing

Teljes unit test lefedettséggel rendelkezik (`100%` coverage):

- Dimension ID validáció
- Body swing high detektálás tesztelése
- Body swing low detektálás tesztelése
- Wick swing high detektálás tesztelése
- Wick swing low detektálás tesztelése
- Resistance body szintek számítása
- Support body szintek számítása
- Resistance wick szintek számítása
- Support wick szintek számítása
- Edge case kezelések (üres DataFrame, hiányzó oszlopok)
- Adat típus megőrzés
- Sorrend megőrzés

## Kapcsolódó Modulok

- [`D02SupportFactory`](factory.md): Factory osztály a processor létrehozásához
- [`SupportError`](exceptions/support_error.md): Modul specifikus kivételek
- [`BaseDimensionProcessor`](../../base.md): Alap osztály