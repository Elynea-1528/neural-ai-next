# D02SupportProcessor

## Áttekintés

A `D02SupportProcessor` felelős a support és resistance szintek azonosításáért és számításáért swing pontok alapján különböző timeframe-ekre.

## Architektúra

- **Base Class**: `BaseDimensionProcessor`
- **Dimension ID**: 2
- **Interfaces**: `IDimensionProcessor`

## Főbb Metódusok

### `_find_swing_points_close_open(df: pl.DataFrame) -> pl.DataFrame`

Swing pontok keresése záró/nyitó árak alapján.

- **Paraméterek**:
  - `df`: Bemeneti Polars DataFrame
- **Visszatérési érték**: `swing_high_body` és `swing_low_body` oszlopokkal kiegészített DataFrame

### `_find_swing_points_high_low(df: pl.DataFrame) -> pl.DataFrame`

Swing pontok keresése high/low értékeken.

- **Paraméterek**:
  - `df`: Bemeneti Polars DataFrame
- **Visszatérési érték**: `swing_high_wick` és `swing_low_wick` oszlopokkal kiegészített DataFrame

### `_merge_levels(df: pl.DataFrame) -> pl.DataFrame`

Szintek összevonása swing pontok alapján.

- **Paraméterek**:
  - `df`: Bemeneti Polars DataFrame swing pontokkal
- **Visszatérési érték**: `resistance` oszloppal kiegészített DataFrame

### `_confirm_with_volume(df: pl.DataFrame, swing_mask: pl.Expr) -> pl.Expr`

Swing pontok megerősítése volumen alapján.

- **Paraméterek**:
  - `df`: Bemeneti Polars DataFrame (nem használt, konzisztenciáért)
  - `swing_mask`: Swing pontokat jelölő kifejezés
- **Visszatérési érték**: Szorzó kifejezés (1.2 ha megerősített, 1.0 ha nem)

### `process(df: pl.DataFrame, timeframe: str = "H1") -> pl.DataFrame`

Support/Resistance szintek számítása swing pontok alapján.

- **Paraméterek**:
  - `df`: Bemeneti Polars DataFrame (time-aligned OHLCV adatok)
  - `timeframe`: Időkeret ("H1", "H4", "D1"), default "H1"
- **Visszatérési érték**: Support/resistance szintekkel kiegészített Polars DataFrame

## Konfiguráció

A processzor a `processors.d02` konfigurációs szekciót használja:

- `swing_window`: Swing ablak mérete (default: 5)
- `volume_confirmation`: Volumen megerősítés engedélyezése (default: true)

## Használat

```python
from neural_ai.core.processing.dimensions.d02_support.implementations.support_processor import D02SupportProcessor

processor = D02SupportProcessor(config, logger)
result_df = processor.process(ohlcv_df, timeframe="H1")