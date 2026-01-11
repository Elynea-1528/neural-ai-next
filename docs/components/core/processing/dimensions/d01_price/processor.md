# D01PriceProcessor

## Áttekintés

A `D01PriceProcessor` az alap pénzügyi adatok processzora, amely biztosítja és validálja az alap pénzügyi adatokat. Kiválasztja és visszaadja a timestamp, mid_open, mid_high, mid_low, mid_close, tick_volume, spread és real_volume oszlopokat, valamint számítja a log return-ot, rolling Z-score-ot és árnyékokat (shadows).

## Architektúra

Ez az osztály a `BaseDimensionProcessor`-ből származik és a `core.processing.dimensions.d01_price` modul része.

## Funkcionalitás

### process Metódus

```python
def process(self, df: pl.DataFrame, timeframe: str = "1m") -> pl.DataFrame:
```

Számítja a matematikai transzformációkat Polars Expr alapúan.

#### Paraméterek

- `df`: Bemeneti Polars DataFrame (már time-aligned OHLCV adatok)
- `timeframe`: Időkeret ("tick", "1m", stb.), default "1m"

#### Adaptív Logika

- **Általános logika minden timeframe-ra**:
  - Log return: `ln(mid_close / mid_close.shift(1))`
  - Z-score: Konfigurált ablakból számított rolling Z-score
  - Shadows: Számítása csak akkor történik, ha `calc_shadows` engedélyezve és `timeframe != "tick"`, különben None értékekkel töltjük

#### Konfiguráció

- `z_score_window`: Z-score rolling ablak mérete (default 60)
- `calc_shadows`: Árnyékok számítása engedélyezve (default True)

#### Kimenet

Polars DataFrame az alap adatokkal és transzformációkkal:

- `timestamp`
- `mid_open`, `mid_high`, `mid_low`, `mid_close`
- `tick_volume`, `spread`, `real_volume`
- `log_return`: Logaritmikus hozam
- `rolling_z_score`: Normalizált Z-score
- `upper_shadow`, `lower_shadow`: Árnyékok (csak akkor számítva, ha `calc_shadows` és `timeframe != "tick"`, különben None)

## Példa Használat

```python
processor = D01PriceProcessor(config, logger)
result_df = processor.process(ohlcv_df, timeframe="1m")
```

## Függőségek

- `polars` - Adatfeldolgozás
- `BaseDimensionProcessor` - Alaposztály
- `ConfigManagerInterface` - Konfiguráció
- `LoggerInterface` - Logolás