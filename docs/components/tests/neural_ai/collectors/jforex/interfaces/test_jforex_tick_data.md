# 🧪 Teszt: tests/neural_ai/collectors/jforex/interfaces/test_jforex_tick_data.py

**Tesztelt modul:** [`neural_ai/collectors/jforex/interfaces/jforex_tick_data.py`](../../neural_ai/collectors/jforex/interfaces/jforex_tick_data.py)

Unit tesztek a JForex TickData modellhez.

## Teszt Osztály: `TestTickData`

Tesztek a TickData dataclass-hoz.

### ✓ `test_tick_data_creation_with_required_fields()`

Ellenőrzi, hogy TickData létrehozható kötelező mezőkkel.

### ✓ `test_tick_data_creation_with_all_fields()`

Ellenőrzi, hogy TickData létrehozható minden mezővel.

### ✓ `test_spread_calculation()`

Ellenőrzi a spread számítást pip-ben.

### ✓ `test_spread_calculation_with_larger_spread()`

Ellenőrzi a spread számítást nagyobb spread esetén.

### ✓ `test_mid_price_calculation()`

Ellenőrzi a mid ár számítást.

### ✓ `test_mid_price_rounding()`

Ellenőrzi a mid ár kerekítését 5 tizedesjegyre.

### ✓ `test_tick_data_is_dataclass()`

Ellenőrzi, hogy TickData dataclass.

### ✓ `test_tick_data_equality()`

Ellenőrzi, hogy két azonos TickData egyenlő.

### ✓ `test_tick_data_inequality()`

Ellenőrzi, hogy két különböző TickData nem egyenlő.

### ✓ `test_spread_with_zero_spread()`

Ellenőrzi a spread számítást nulla spread esetén.

---

**Teszt fájl:** [`tests/neural_ai/collectors/jforex/interfaces/test_jforex_tick_data.py`](../../tests/neural_ai/collectors/jforex/interfaces/test_jforex_tick_data.py)

**Tesztelt modul:** [`neural_ai/collectors/jforex/interfaces/jforex_tick_data.py`](../../neural_ai/collectors/jforex/interfaces/jforex_tick_data.py)
