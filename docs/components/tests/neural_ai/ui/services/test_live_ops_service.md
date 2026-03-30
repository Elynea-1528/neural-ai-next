# 🧪 Teszt: tests/neural_ai/ui/services/test_live_ops_service.py

**Tesztelt modul:** [`neural_ai/ui/services/live_ops_service.py`](../../neural_ai/ui/services/live_ops_service.py)

Unit tesztek a LiveOpsService osztályhoz.

## Teszt Osztály: `TestLiveOpsService`

Tesztek a LiveOpsService osztályhoz.

### ✓ `test_initialization()`

Teszt: LiveOpsService inicializálása.

### ✓ `test_get_active_positions_empty()`

Teszt: Aktív pozíciók lekérdezése üres állapotban.

### ✓ `test_get_active_positions_with_active()`

Teszt: Aktív pozíciók lekérdezése aktív pozíciókkal.

### ✓ `test_get_account_status()`

Teszt: Fiók állapotának lekérdezése.

### ✓ `test_place_order_basic()`

Teszt: Alapvető rendelés leadása.

### ✓ `test_place_order_with_sl_tp()`

Teszt: Rendelés leadása SL/TP szintekkel.

### ✓ `test_modify_order_success()`

Teszt: Rendelés sikeres módosítása.

### ✓ `test_modify_order_unknown()`

Teszt: Ismeretlen rendelés módosítása hibát dob.

### ✓ `test_cancel_order_success()`

Teszt: Rendelés sikeres visszavonása.

### ✓ `test_cancel_order_unknown()`

Teszt: Ismeretlen rendelés visszavonása hibát dob.

### ✓ `test_close_position_success()`

Teszt: Pozíció sikeres lezárása.

### ✓ `test_close_position_unknown()`

Teszt: Ismeretlen pozíció lezárása hibát dob.

### ✓ `test_get_market_data()`

Teszt: Piaci adatok lekérdezése.

### ✓ `test_subscribe_to_market_updates()`

Teszt: Feliratkozás piaci frissítésekre.

### ✓ `test_subscribe_to_market_updates_multiple()`

Teszt: Több callback feliratkozása ugyanarra a szimbólumra.

### ✓ `test_get_performance_summary()`

Teszt: Teljesítmény összegzés lekérdezése.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_live_ops_service.py`](../../tests/neural_ai/ui/services/test_live_ops_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/live_ops_service.py`](../../neural_ai/ui/services/live_ops_service.py)
