# 🧪 Teszt: tests/neural_ai/processors/dimensions/d02_support/test_d02_processor_extended.py

**Tesztelt modul:** [`neural_ai/processors/dimensions/d02_support/d02_processor_extended.py`](../../neural_ai/processors/dimensions/d02_support/d02_processor_extended.py)

Extended tests for D02 Support Processor - Coverage pótlás.

## Teszt Osztály: `TestD02ProcessorCategorizeZones`

Test _categorize_zones method coverage.

### ✓ `test_categorize_zones_strong_levels()`

Test: Strong levels kategorizálása (strength > 0.7, touches >= min_touches).

### ✓ `test_categorize_zones_moderate_levels()`

Test: Moderate levels kategorizálása (0.3 <= strength <= 0.7).

### ✓ `test_categorize_zones_weak_levels()`

Test: Weak levels kategorizálása (strength < 0.3).

### ✓ `test_categorize_zones_moderate_low_touches_high_strength()`

Test: Moderate kategória (touches < min_touches de strength > 0.4).

### ✓ `test_categorize_zones_missing_min_touches_config()`

Test: min_touches hiányzik a configból (default 1 használata).

## Teszt Osztály: `TestD02ProcessorMidColumnsHandling`

Test mid oszlopok hiányának kezelése.

### ✓ `test_process_with_bid_columns_no_mid()`

Test: Mid oszlopok hiányoznak, Bid oszlopok másolása.

### ✓ `test_process_with_simple_ohlc_no_mid()`

Test: Mid oszlopok hiányoznak, sima OHLC oszlopok másolása.

### ✓ `test_process_missing_all_ohlc_columns()`

Test: Hiányzó OHLC oszlopok (ColumnNotFoundError várható).

## Teszt Osztály: `TestD02ProcessorMarketHoursFiltering`

Test market hours filtering coverage.

### ✓ `test_process_with_market_hours_enabled_filtering()`

Test: Market hours enabled, filtering triggered.

### ✓ `test_process_with_market_hours_outside_hours()`

Test: Market hours filtering - outside trading hours.

## Teszt Osztály: `TestD02ProcessorNearestLevels`

Test find_nearest_support/resistance coverage.

### ✓ `test_process_calculates_nearest_support()`

Test: Legközelebbi support szint számítása (ha implementálva).

### ✓ `test_process_calculates_nearest_resistance()`

Test: Legközelebbi resistance szint számítása (ha implementálva).

## Teszt Osztály: `TestD02ProcessorEdgeCases`

Test edge cases és branch coverage.

### ✓ `test_process_with_empty_dataframe()`

Test: Üres DataFrame kezelése (Polars rolling_max hiba várható).

### ✓ `test_process_with_insufficient_data()`

Test: Kevés adat (< min_candles).

### ✓ `test_dimension_id_property()`

Test: dimension_id property.

---

**Teszt fájl:** [`tests/neural_ai/processors/dimensions/d02_support/test_d02_processor_extended.py`](../../tests/neural_ai/processors/dimensions/d02_support/test_d02_processor_extended.py)

**Tesztelt modul:** [`neural_ai/processors/dimensions/d02_support/d02_processor_extended.py`](../../neural_ai/processors/dimensions/d02_support/d02_processor_extended.py)
