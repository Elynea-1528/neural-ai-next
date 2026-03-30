# 🧪 Teszt: tests/neural_ai/core/logger/implementations/test_colored_logger.py

**Tesztelt modul:** [`neural_ai/core/logger/implementations/colored_logger.py`](../../neural_ai/core/logger/implementations/colored_logger.py)

Unit tesztek a neural_ai.core.logger.implementations.colored_logger modulhoz.

Ez a teszt ellenőrzi a ColoredLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Log szintek (debug, info, warning, error, critical)
3. Színes formázás
4. LoggerInterface implementáció

## Teszt Függvények

### ✓ `test_colored_logger_initialization()`

Teszt: A ColoredLogger inicializálható.

### ✓ `test_colored_logger_default_level()`

Teszt: A ColoredLogger alapértelmezett log szintje INFO.

### ✓ `test_colored_logger_custom_level()`

Teszt: A ColoredLogger egyedi log szinttel inicializálható.

### ✓ `test_colored_logger_info_message()`

Teszt: A ColoredLogger info üzenetet tud logolni.

### ✓ `test_colored_logger_warning_message()`

Teszt: A ColoredLogger warning üzenetet tud logolni.

### ✓ `test_colored_logger_error_message()`

Teszt: A ColoredLogger error üzenetet tud logolni.

### ✓ `test_colored_logger_debug_message()`

Teszt: A ColoredLogger debug üzenetet tud logolni DEBUG szinten.

### ✓ `test_colored_logger_critical_message()`

Teszt: A ColoredLogger critical üzenetet tud logolni.

### ✓ `test_colored_logger_with_extra_fields()`

Teszt: A ColoredLogger extra mezőkkel tud logolni.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/implementations/test_colored_logger.py`](../../tests/neural_ai/core/logger/implementations/test_colored_logger.py)

**Tesztelt modul:** [`neural_ai/core/logger/implementations/colored_logger.py`](../../neural_ai/core/logger/implementations/colored_logger.py)
