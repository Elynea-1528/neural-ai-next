# 🧪 Teszt: tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py

**Tesztelt modul:** [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../neural_ai/core/logger/implementations/rotating_file_logger.py)

Rotating file logger implementáció tesztei.

## Teszt Osztály: `TestRotatingFileLogger`

RotatingFileLogger osztály tesztei.

### ✓ `test_init_basic()`

Alap logger inicializálás tesztelése.

### ✓ `test_init_without_file_raises_error()`

Logger inicializálás fájl nélkül hibát dob.

### ✓ `test_init_with_empty_file_raises_error()`

Logger inicializálás üres fájlnévvel hibát dob. Ez a teszt lefedi a 60. sort, ahol a ValueError-t dobjuk.

### ✓ `test_init_with_custom_level()`

Logger inicializálás egyéni szinttel.

### ✓ `test_init_creates_directory()`

Logger létrehozza a könyvtárat, ha az nem létezik.

### ✓ `test_debug_logging()`

Debug üzenet logolásának tesztelése.

### ✓ `test_debug_logging_without_kwargs()`

Debug üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 106. sort.

### ✓ `test_info_logging()`

Info üzenet logolásának tesztelése.

### ✓ `test_info_logging_without_kwargs()`

Info üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 118. sort.

### ✓ `test_warning_logging()`

Warning üzenet logolásának tesztelése.

### ✓ `test_warning_logging_without_kwargs()`

Warning üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 130. sort.

### ✓ `test_error_logging()`

Error üzenet logolásának tesztelése.

### ✓ `test_error_logging_without_kwargs()`

Error üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 142. sort.

### ✓ `test_critical_logging()`

Critical üzenet logolásának tesztelése.

### ✓ `test_critical_logging_without_kwargs()`

Critical üzenet logolásának tesztelése kwargs nélkül. Ez a teszt lefedi a 154. sort.

### ✓ `test_set_level()`

Log szint módosításának tesztelése.

### ✓ `test_logger_name()`

Logger nevének ellenőrzése.

### ✓ `test_invalid_rotation_type_raises_error()`

Érvénytelen rotáció típus hibát dob.

### ✓ `test_time_based_rotation()`

Időalapú rotáció tesztelése. Ez a teszt lefedi a 75. sort, ahol a TimedRotatingFileHandler-t hozzuk létre.

### ✓ `test_clean_old_logs()`

Régi log fájlok törlésének tesztelése.

### ✓ `test_existing_handlers_removed()`

Teszteli, hogy a meglévő handlerek eltávolításra kerülnek. Ez a teszt lefedi a 56. sort, ahol a meglévő handlerek eltávolítása történik.

### ✓ `test_di_dependencies_none()`

DI függőségek None értékkel történő elfogadásának tesztelése.

---

**Teszt fájl:** [`tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py`](../../tests/neural_ai/core/logger/implementations/test_rotating_file_logger.py)

**Tesztelt modul:** [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../neural_ai/core/logger/implementations/rotating_file_logger.py)
