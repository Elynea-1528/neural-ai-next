# 🧪 Teszt: tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py

**Tesztelt modul:** [`neural_ai/processors/dimensions/d01_price/d01_processor.py`](../../neural_ai/processors/dimensions/d01_price/d01_processor.py)

Unit tesztek a D01PriceProcessor osztályhoz.

## Teszt Osztály: `TestD01PriceProcessor`

Tesztek a D01PriceProcessor osztályhoz.

### ✓ `test_processor_initialization()`

Ellenőrzi, hogy a processzor inicializálható.

### ✓ `test_dimension_id_is_one()`

Ellenőrzi, hogy a dimension_id 1.

### ✓ `test_process_with_basic_dataframe()`

Ellenőrzi a process metódust alapvető DataFrame-mel.

### ✓ `test_process_calculates_bid_ask_from_mid_and_spread()`

Ellenőrzi, hogy a bid/ask értékek helyesen számítódnak.

### ✓ `test_process_with_custom_z_score_window()`

Ellenőrzi a process metódust egyedi z_score_window-val.

### ✓ `test_process_with_tick_timeframe()`

Ellenőrzi a process metódust tick timeframe-mel.

### ✓ `test_process_calculates_shadows_for_non_tick_timeframe()`

Ellenőrzi, hogy az árnyékok számítódnak nem-tick timeframe esetén.

### ✓ `test_process_with_existing_bid_ask_columns()`

Ellenőrzi, hogy a meglévő bid/ask oszlopokat használja.

### ✓ `test_process_logs_debug_message()`

Ellenőrzi, hogy a process metódus naplóz.

---

**Teszt fájl:** [`tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py`](../../tests/neural_ai/processors/dimensions/d01_price/test_d01_processor.py)

**Tesztelt modul:** [`neural_ai/processors/dimensions/d01_price/d01_processor.py`](../../neural_ai/processors/dimensions/d01_price/d01_processor.py)
