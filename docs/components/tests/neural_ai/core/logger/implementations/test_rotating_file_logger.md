# 🧪 Teszt: tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py

**Tesztelt modul:** [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../neural_ai/core/logger/implementations/rotating_file_logger.py)

Unit tesztek a neural_ai.core.logger.implementations.rotating_file_logger modulhoz.

Ez a teszt ellenőrzi a RotatingFileLogger osztály alapvető funkcionalitását:
1. Inicializálás
2. Fájlba írás
3. Méret alapú rotáció
4. Idő alapú rotáció
5. LoggerInterface implementáció

## Teszt Függvények

### ✓ `test_rotating_file_logger_initialization()`

Teszt: A RotatingFileLogger inicializálható.

### ✓ `test_rotating_file_logger_default_level()`

Teszt: A RotatingFileLogger alapértelmezett log szintje INFO.

### ✓ `test_rotating_file_logger_custom_level()`

Teszt: A RotatingFileLogger egyedi log szinttel inicializálható.

### ✓ `test_rotating_file_logger_writes_to_file()`

Teszt: A RotatingFileLogger fájlba ír.

### ✓ `test_rotating_file_logger_size_rotation()`

Teszt: A RotatingFileLogger méret alapú rotációt végez.

### ✓ `test_rotating_file_logger_time_rotation()`

Teszt: A RotatingFileLogger idő alapú rotációval inicializálható.

### ✓ `test_rotating_file_logger_multiple_messages()`

Teszt: A RotatingFileLogger több üzenetet tud logolni.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py`](../../tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py)

**Tesztelt modul:** [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../neural_ai/core/logger/implementations/rotating_file_logger.py)
