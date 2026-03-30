# 🧪 Teszt: tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py

**Tesztelt modul:** [`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](../../neural_ai/processors/dimensions/d02_support/implementations/support_processor.py)

Tests for D02 Support Processor.

## Teszt Osztály: `TestD02ProcessorMissingConfigBranches`

Test hiányzó config paraméterek branch coverage-hez.

### ✓ `test_merge_levels_missing_level_merge_config()`

Test: level_merge hiányzik a configból (133-136 sorok).

### ✓ `test_merge_levels_large_dataframe_skip_merge()`

Test: Nagy DataFrame (> 5000 sor) esetén merge skip (130-136 sorok).

### ✓ `test_confirm_with_volume_missing_config()`

Test: volume_confirmation hiányzik a configból (292-297 sorok).

### ✓ `test_confirm_with_volume_false()`

Test: volume_confirmation = False (300-301 sorok).

### ✓ `test_confirm_with_volume_true()`

Test: volume_confirmation = True (300-301 sorok - threshold számítás).

## Teszt Osztály: `TestD02ProcessorNearestLevelsEdgeCases`

Test find_nearest_support/resistance edge cases (493-504 sorok).

### ✓ `test_nearest_support_no_candidates_below()`

Test: Nincs support szint az aktuális ár alatt (493-497 sorok).

### ✓ `test_nearest_resistance_no_candidates_above()`

Test: Nincs resistance szint az aktuális ár felett (500-504 sorok).

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

## Teszt Függvények

### ✓ `test_d02_processor_happy_path()`

Test D02SupportProcessor instantiation with valid config.

### ✓ `test_d02_processor_defaults()`

Test D02SupportProcessor default values.

### ✓ `test_d02_processor_validation_error()`

Test D02SupportProcessor with invalid config.

### ✓ `test_d02_processor_invalid_type()`

Test D02SupportProcessor with invalid type in config.

---

**Teszt fájl:** [`tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py`](../../tests/neural_ai/processors/dimensions/d02_support/implementations/test_support_processor.py)

**Tesztelt modul:** [`neural_ai/processors/dimensions/d02_support/implementations/support_processor.py`](../../neural_ai/processors/dimensions/d02_support/implementations/support_processor.py)
