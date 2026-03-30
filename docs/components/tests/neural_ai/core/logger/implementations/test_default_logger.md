# 🧪 Teszt: tests/neural_ai/core/logger/implementations/test_default_logger.py

**Tesztelt modul:** [`neural_ai/core/logger/implementations/default_logger.py`](../../neural_ai/core/logger/implementations/default_logger.py)

Unit tesztek a neural_ai.core.logger.implementations.default_logger modulhoz.

Ez a teszt ellenőrzi a DefaultLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Log szintek (debug, info, warning, error, critical)
3. Structlog integráció
4. LoggerInterface implementáció

## Teszt Függvények

### ✓ `test_default_logger_initialization()`

Teszt: A DefaultLogger inicializálható.

### ✓ `test_default_logger_default_level()`

Teszt: A DefaultLogger alapértelmezett log szintje INFO.

### ✓ `test_default_logger_custom_level()`

Teszt: A DefaultLogger egyedi log szinttel inicializálható.

### ✓ `test_default_logger_info_message()`

Teszt: A DefaultLogger info üzenetet tud logolni.

### ✓ `test_default_logger_warning_message()`

Teszt: A DefaultLogger warning üzenetet tud logolni.

### ✓ `test_default_logger_error_message()`

Teszt: A DefaultLogger error üzenetet tud logolni.

### ✓ `test_default_logger_debug_message()`

Teszt: A DefaultLogger debug üzenetet tud logolni DEBUG szinten.

### ✓ `test_default_logger_critical_message()`

Teszt: A DefaultLogger critical üzenetet tud logolni.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/implementations/test_default_logger.py`](../../tests/neural_ai/core/logger/implementations/test_default_logger.py)

**Tesztelt modul:** [`neural_ai/core/logger/implementations/default_logger.py`](../../neural_ai/core/logger/implementations/default_logger.py)
