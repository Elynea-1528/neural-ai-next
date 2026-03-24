# 🧪 Teszt: tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py

**Tesztelt modul:** [`neural_ai/processors/dimensions/d01_price/d01_processor.py`](../../neural_ai/processors/dimensions/d01_price/d01_processor.py)

Unit tesztek a D01PriceProcessor osztályhoz.

## Teszt Osztály: `TestD01PriceProcessorInitialization`

D01PriceProcessor inicializálás tesztjei.

### ✓ `test_init_success()`

Sikeres inicializálás tesztje.

### ✓ `test_dimension_id_property()`

Dimenzió ID property tesztje.

## Teszt Osztály: `TestD01PriceProcessorProcess`

D01PriceProcessor process metódus tesztjei.

### ✓ `test_process_happy_path()`

Process metódus normál működés tesztje.

### ✓ `test_process_calculates_log_return()`

Log return számítás tesztje.

### ✓ `test_process_calculates_bid_ask_from_spread()`

Bid/Ask számítás spread alapján tesztje.

### ✓ `test_process_calculates_shadows_for_ohlc()`

Árnyékok számítása OHLC timeframe esetén.

### ✓ `test_process_no_shadows_for_tick_timeframe()`

Árnyékok NEM számítása tick timeframe esetén.

### ✓ `test_process_with_custom_z_score_window()`

Egyedi Z-score ablak használata.

### ✓ `test_process_with_timeframe_specific_config()`

Timeframe specifikus konfiguráció használata.

### ✓ `test_process_preserves_existing_bid_ask_columns()`

Meglévő bid/ask oszlopok megőrzése.

## Teszt Osztály: `TestD01PriceProcessorEdgeCases`

D01PriceProcessor edge case tesztek.

### ✓ `test_process_with_empty_dataframe()`

Üres DataFrame kezelése.

### ✓ `test_process_with_single_row()`

Egyetlen sor kezelése.

### ✓ `test_process_with_calc_shadows_disabled()`

Árnyék számítás kikapcsolva.

## Teszt Osztály: `TestD01PriceProcessorMarketHours`

D01PriceProcessor market hours szűrés tesztjei.

### ✓ `test_process_with_market_hours_disabled()`

Market hours szűrés kikapcsolva.

### ✓ `test_process_with_market_hours_enabled_no_filtering()`

Market hours szűrés bekapcsolva, de nincs szűrés (minden adat market hours-ban).

### ✓ `test_process_with_market_hours_logging_triggered()`

Market hours szűrés logging aktiválása hétvégi adatokkal.

## Teszt Osztály: `TestD01PriceProcessorTickColumns`

D01PriceProcessor tick oszlopok kezelése tesztjei.

### ✓ `test_process_with_tick_columns()`

Tick oszlopok hozzáadása, ha rendelkezésre állnak.

### ✓ `test_process_without_tick_columns()`

Tick oszlopok hiánya nem okoz hibát.

---

**Teszt fájl:** [`tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py`](../../tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py)

**Tesztelt modul:** [`neural_ai/processors/dimensions/d01_price/d01_processor.py`](../../neural_ai/processors/dimensions/d01_price/d01_processor.py)
