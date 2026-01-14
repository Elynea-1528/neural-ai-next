# D02SupportProcessor

## Áttekintés

A `D02SupportProcessor` a support/resistance szintek processzora, amely azonosítja és számítja a swing pontokat különböző timeframe-ekre. Ez a D2 dimenzió része a hierarchikus AI rendszer adatfeldolgozási pipeline-jának.

## Architektúra

Ez az osztály a `BaseDimensionProcessor`-ből származik és a `neural_ai.core.processing.dimensions.d02_support` modul része.

## Funkcionalitás

### process Metódus

```python
def process(self, df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame:
```

Swing pontokat keres különböző ablakméretekkel, majd ezek alapján számítja a support és resistance szinteket.

#### Paraméterek

- `df`: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
- `timeframe`: Időkeret ("H1", "H4", "D1"), default "H1"

#### Swing Pont Számítás

- **Swing High**: `mid_high == mid_high.rolling_max(window_size)`
- **Swing Low**: `mid_low == mid_low.rolling_min(window_size)`

#### Support/Resistance Szintek

- **Resistance**: Swing high-ok átlaga (felső szintek)
- **Support**: Swing low-ok átlaga (alsó szintek)

#### Konfiguráció

- `swing_window`: Rolling window mérete a swing pontok kereséséhez (default 5)
- `min_distance`: Minimum távolság a szintek aggregálásához (default 10)
- `timeframe_configs`: Opcionális szótár timeframe-specifikus konfigurációkkal (case-insensitive kereséssel):
  - Kulcs: timeframe string (pl. "H1", "H4")
  - Érték: konfigurációs szótár, amely felülírhatja a globális beállításokat

#### Kimenet

Polars DataFrame a következő új oszlopokkal:

- `swing_high`: Boolean flag swing high pontokra
- `swing_low`: Boolean flag swing low pontokra
- `resistance`: Aggregált resistance szintek (rolling mean)
- `support`: Aggregált support szintek (rolling mean)

## Példa Használat

```python
processor = D02SupportProcessor(config, logger)
result_df = processor.process(ohlcv_df, timeframe="H1")
```

## Függőségek

- `polars` - Adatfeldolgozás
- `BaseDimensionProcessor` - Alaposztály
- `ConfigManagerInterface` - Konfiguráció
- `LoggerInterface` - Logolás

## Hibakezelés

A processzor a következő kivételeket dobhatja:

- `SwingPointCalculationError`: Swing pont számítási hiba
- `SupportResistanceLevelError`: Szint aggregációs hiba
- `TimeframeConfigurationError`: Érvénytelen timeframe konfiguráció