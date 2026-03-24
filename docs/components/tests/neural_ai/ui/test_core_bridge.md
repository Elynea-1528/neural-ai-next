# 🧪 Teszt: tests/neural_ai/ui/test_core_bridge.py

**Tesztelt modul:** [`neural_ai/ui/core_bridge.py`](../../neural_ai/ui/core_bridge.py)

Core Bridge tesztesetek - teljes lefedettség biztosítása.

## Teszt Osztály: `TestCoreBridge`

CoreBridge osztály tesztelése.

### ✓ `test_singleton_pattern()`

Singleton minta tesztelése.

### ✓ `test_initialization()`

Inicializálás tesztelése.

### ✓ `test_initialization_strategy_service()`

Strategy Service inicializálás tesztelése.

### ✓ `test_initialization_strategy_service_error()`

Strategy Service inicializálási hiba tesztelése.

### ✓ `test_get_component_not_initialized()`

Komponens lekérés inicializálatlan bridge esetén.

### ✓ `test_get_component_parquet_storage()`

Parquet storage komponens lekérés tesztelése.

### ✓ `test_get_component_parquet_storage_none()`

Parquet storage None esetén.

### ✓ `test_get_component_bi5_downloader()`

BI5 downloader komponens létrehozás tesztelése.

### ✓ `test_get_component_bi5_downloader_missing_deps()`

BI5 downloader hiányzó függőségekkel.

### ✓ `test_get_component_strategy_service()`

Strategy Service komponens lekérés tesztelése.

### ✓ `test_get_component_strategy_service_none()`

Strategy Service None esetén.

### ✓ `test_get_component_config()`

Config komponens lekérés tesztelése.

### ✓ `test_get_component_config_none()`

Config None esetén.

### ✓ `test_get_component_unknown()`

Ismeretlen komponens típus tesztelése.

### ✓ `test_get_component_logger()`

Logger komponens lekérés tesztelése.

### ✓ `test_send_command_connected()`

Parancs küldés csatlakoztatott bridge esetén.

### ✓ `test_send_command_not_connected()`

Parancs küldés nem csatlakoztatott bridge esetén.

### ✓ `test_get_system_info_connected()`

Rendszerinformáció lekérés csatlakoztatott bridge esetén.

### ✓ `test_get_system_info_not_connected()`

Rendszerinformáció lekérés nem csatlakoztatott bridge esetén.

### ✓ `test_core_property()`

Core property tesztelése.

### ✓ `test_is_connected_property()`

is_connected property tesztelése.

---

**Teszt fájl:** [`tests/neural_ai/ui/test_core_bridge.py`](../../tests/neural_ai/ui/test_core_bridge.py)

**Tesztelt modul:** [`neural_ai/ui/core_bridge.py`](../../neural_ai/ui/core_bridge.py)
