# 🧪 Teszt: tests/neural_ai/ui/pages/test_strategy_lab_page.py

**Tesztelt modul:** [`neural_ai/ui/pages/strategy_lab_page.py`](../../neural_ai/ui/pages/strategy_lab_page.py)

Tesztelési modul a Strategy Lab oldalhoz.

Ez a modul tartalmazza a StrategyLabPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását és a session_state persistence-t.

## Teszt Osztály: `TestStrategyLabPage`

StrategyLabPage osztály tesztjei.

Ezek a tesztek ellenőrzik az oldal inicializálását, renderelését,
navigációs metódusait és a szimbólum lekérést.

### ✓ `test_init()`

Teszteli az osztály inicializálását.

### ✓ `test_init_with_kwargs()`

Teszteli az inicializálást további paraméterekkel.

### ✓ `test_title_property()`

Teszteli a title property-t.

### ✓ `test_is_loaded_property_initial()`

Teszteli az is_loaded property kezdeti állapotát.

### ✓ `test_on_navigate_to_resets_state()`

Teszteli, hogy a navigálás visszaállítja az állapotot (session_state-kel).

### ✓ `test_on_navigate_to_with_params()`

Teszteli a navigációt paraméterekkel.

### ✓ `test_on_navigate_from()`

Teszteli az oldal elhagyásakor történő akciót.

### ✓ `test_get_symbols_from_config()`

Teszteli a szimbólumok lekérését a konfigurációból.

### ✓ `test_get_symbols_from_config_empty()`

Teszteli a szimbólumok lekérését üres konfigurációval.

### ✓ `test_get_symbols_config_returns_none()`

Teszteli a szimbólumok lekérését, ha a konfiguráció None.

### ✓ `test_get_symbols_config_exception()`

Teszteli a szimbólumok lekérését, ha a konfiguráció hibát dob.

### ✓ `test_get_strategy_service_success()`

Teszteli a Strategy Service sikeres lekérését.

### ✓ `test_get_strategy_service_exception()`

Teszteli a Strategy Service lekérését, ha hibát dob.

### ✓ `test_render_sidebar()`

Teszteli az oldalsáv renderelését.

### ✓ `test_render_without_data()`

Teszteli a renderelést adatok nélkül.

### ✓ `test_render_without_errors()`

Teszteli, hogy a render metódus hiba nélkül lefut.

## Teszt Osztály: `TestStrategyLabPageSessionState`

Session State tesztek a Strategy Lab oldalhoz.

Ezek a tesztek ellenőrzik a session_state alapú adat persistence funkcionalitást.

### ✓ `test_init_session_state_candles_initialization()`

Teszteli, hogy az __init__ metódus inicializálja a session state candles-t.

### ✓ `test_render_syncs_session_state_candles()`

Teszteli, hogy a render metódus szinkronizálja a session state candles értékét.

### ✓ `test_on_navigate_to_clears_session_state()`

Teszteli, hogy az on_navigate_to metódus törli a session state candles értékét.

### ✓ `test_candles_persistence_between_interactions()`

Teszteli, hogy a gyertyák megmaradnak a felhasználói interakciók között.

### ✓ `test_backtest_result_persistence()`

Teszteli, hogy a backteszt eredménye megmarad a session state-ben.

### ✓ `test_price_type_session_state_initialization()`

Teszteli a price_type session state inicializálását.

### ✓ `test_render_data_table_with_price_type_bid()`

Teszteli a _render_data_table metódust Bid price type-pal.

### ✓ `test_render_data_table_with_price_type_mid()`

Teszteli a _render_data_table metódust Mid price type-pal.

### ✓ `test_render_candlestick_chart_with_bid_price_type()`

Teszteli a candlestick chart renderelését Bid price type-pal.

### ✓ `test_render_candlestick_chart_with_mid_price_type()`

Teszteli a candlestick chart renderelését Mid price type-pal.

---

**Teszt fájl:** [`tests/neural_ai/ui/pages/test_strategy_lab_page.py`](../../tests/neural_ai/ui/pages/test_strategy_lab_page.py)

**Tesztelt modul:** [`neural_ai/ui/pages/strategy_lab_page.py`](../../neural_ai/ui/pages/strategy_lab_page.py)
