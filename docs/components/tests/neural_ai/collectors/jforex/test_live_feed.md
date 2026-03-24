# 🧪 Teszt: tests/neural_ai/collectors/jforex/test_live_feed.py

**Tesztelt modul:** [`neural_ai/collectors/jforex/live_feed.py`](../../neural_ai/collectors/jforex/live_feed.py)

JForex Live Feed Tests.

Ez a modul tartalmazza a JForexLiveFeed osztály tesztjeit.

## Teszt Osztály: `TestJForexLiveFeed`

JForexLiveFeed osztály tesztjei.

### ✓ `test_start_success()`

Teszteli a start metódus sikeres futását.

### ✓ `test_start_when_already_running()`

Teszteli, hogy a start metódus figyelmeztet, ha már fut a feed.

### ✓ `test_stop_success()`

Teszteli a stop metódus sikeres futását.

### ✓ `test_stop_when_not_running()`

Teszteli, hogy a stop metódus nem csinál semmit, ha nem fut a feed.

### ✓ `test_process_tick_data_success()`

Teszteli a tick adatok feldolgozását.

### ✓ `test_process_tick_data_error()`

Teszteli a hibakezelést tick adatok feldolgozásakor.

### ✓ `test_listen_loop_processes_tick()`

Teszteli, hogy a listen loop feldolgozza a tick üzeneteket.

### ✓ `test_is_running_returns_correct_state()`

Teszteli, hogy az is_running metódus helyes állapotot adja vissza.

### ✓ `test_init_with_empty_config_logs_warning()`

Teszteli, hogy üres config esetén warning log jelenik meg.

### ✓ `test_init_with_config_logs_debug()`

Teszteli, hogy config adatok esetén debug log jelenik meg.

### ✓ `test_start_raises_exception_on_zmq_failure()`

Teszteli, hogy start exception-t dob ZMQ hiba esetén.

### ✓ `test_listen_loop_handles_socket_none()`

Teszteli, hogy listen loop kezeli, ha socket None.

---

**Teszt fájl:** [`tests/neural_ai/collectors/jforex/test_live_feed.py`](../../tests/neural_ai/collectors/jforex/test_live_feed.py)

**Tesztelt modul:** [`neural_ai/collectors/jforex/live_feed.py`](../../neural_ai/collectors/jforex/live_feed.py)
