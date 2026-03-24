# 🧪 Teszt: tests/neural_ai/core/logger/implementations/test_colored_logger.py

**Tesztelt modul:** [`neural_ai/core/logger/implementations/colored_logger.py`](../../neural_ai/core/logger/implementations/colored_logger.py)

Colored logger implementáció tesztei.

## Teszt Osztály: `TestColoredLogger`

ColoredLogger osztály tesztei.

### ✓ `test_init_basic()`

Alap logger inicializálás tesztelése.

### ✓ `test_init_with_custom_level()`

Logger inicializálás egyéni szinttel.

### ✓ `test_debug_logging()`

Debug üzenet logolásának tesztelése.

### ✓ `test_info_logging()`

Info üzenet logolásának tesztelése.

### ✓ `test_warning_logging()`

Warning üzenet logolásának tesztelése.

### ✓ `test_error_logging()`

Error üzenet logolásának tesztelése.

### ✓ `test_critical_logging()`

Critical üzenet logolásának tesztelése.

### ✓ `test_set_level()`

Log szint módosításának tesztelése.

### ✓ `test_logger_name()`

Logger nevének ellenőrzése.

### ✓ `test_colored_formatter_present()`

Színes formázó jelenlétének ellenőrzése.

### ✓ `test_existing_handlers_removed()`

Teszteli, hogy a meglévő handlerek eltávolításra kerülnek. Ez a teszt lefedi a 54-55. sorokat, ahol a meglévő handlerek eltávolítása történik, hogy ne legyenek duplikált üzenetek.

### ✓ `test_di_dependencies_none()`

DI függőségek None értékkel történő elfogadásának tesztelése.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/implementations/test_colored_logger.py`](../../tests/neural_ai/core/logger/implementations/test_colored_logger.py)

**Tesztelt modul:** [`neural_ai/core/logger/implementations/colored_logger.py`](../../neural_ai/core/logger/implementations/colored_logger.py)
