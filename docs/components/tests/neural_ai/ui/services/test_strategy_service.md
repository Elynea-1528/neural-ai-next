# 🧪 Teszt: tests/neural_ai/ui/services/test_strategy_service.py

**Tesztelt modul:** [`neural_ai/ui/services/strategy_service.py`](../../neural_ai/ui/services/strategy_service.py)

Strategy Service tesztek.

Ez a modul tartalmazza a StrategyService osztály tesztjeit,
beleértve az új get_candles metódust.

## Teszt Osztály: `TestStrategyService`

Strategy Service tesztek.

### ✓ `test_init()`

StrategyService inicializáció tesztelése.

### ✓ `test_get_strategies()`

Stratégiák lekérdezésének tesztelése.

### ✓ `test_create_strategy()`

Új stratégia létrehozásának tesztelése.

### ✓ `test_update_strategy()`

Stratégia módosításának tesztelése.

### ✓ `test_update_strategy_not_found()`

Ismeretlen stratégia módosításának tesztelése.

### ✓ `test_delete_strategy()`

Stratégia törlésének tesztelése.

### ✓ `test_delete_strategy_not_found()`

Ismeretlen stratégia törlésének tesztelése.

### ✓ `test_backtest_strategy()`

Backtest indításának tesztelése.

### ✓ `test_backtest_strategy_not_found()`

Ismeretlen stratégia backtestelésének tesztelése.

### ✓ `test_get_backtest_status()`

Backtest állapot lekérdezésének tesztelése.

### ✓ `test_get_backtest_status_not_found()`

Ismeretlen backtest állapot lekérdezésének tesztelése.

### ✓ `test_optimize_strategy()`

Optimalizálás indításának tesztelése.

### ✓ `test_optimize_strategy_not_found()`

Ismeretlen stratégia optimalizálásának tesztelése.

### ✓ `test_get_candles()`

OHLCV gyertyák lekérdezésének tesztelése.

### ✓ `test_get_candles_date_format()`

Dátum formátum konverzió tesztelése.

### ✓ `test_get_candles_different_timeframes()`

Különböző időkeretek tesztelése.

### ✓ `test_run_sma_backtest_success_with_trades()`

SMA backtest sikerességének tesztelése trades adatokkal.

### ✓ `test_run_sma_backtest_no_trades()`

SMA backtest tesztelése trades nélkül.

### ✓ `test_run_sma_backtest_missing_pnl_column()`

SMA backtest tesztelése hiányzó PnL oszloppal.

### ✓ `test_analyze_market_structure_with_df()`

Piaci struktúra elemzés tesztelése meglévő DataFrame-mel.

### ✓ `test_analyze_market_structure_without_df()`

Piaci struktúra elemzés tesztelése DataFrame betöltéssel.

### ✓ `test_analyze_market_structure_no_data()`

Piaci struktúra elemzés tesztelése adatok hiányában.

### ✓ `test_analyze_market_structure_empty_data()`

Piaci struktúra elemzés tesztelése üres adatokkal.

### ✓ `test_analyze_market_structure_missing_components()`

Piaci struktúra elemzés tesztelése hiányzó komponensekkel.

---

**Teszt fájl:** [`tests/neural_ai/ui/services/test_strategy_service.py`](../../tests/neural_ai/ui/services/test_strategy_service.py)

**Tesztelt modul:** [`neural_ai/ui/services/strategy_service.py`](../../neural_ai/ui/services/strategy_service.py)
