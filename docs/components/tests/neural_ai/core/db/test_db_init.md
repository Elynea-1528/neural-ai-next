# 🧪 Teszt: tests/neural_ai/core/db/test_db_init.py

**Tesztelt modul:** [`neural_ai/core/db/db_init.py`](../../neural_ai/core/db/db_init.py)

Tesztek a neural_ai.core.db.__init__.py modulhoz.

Ez a tesztmodul ellenőrzi a db modul inicializálását és exportált elemeit.

## Teszt Osztály: `TestDbInit`

Tesztek a db __init__ modulhoz.

### ✓ `test_module_import()`

Teszteli, hogy a modul importálható.

### ✓ `test_module_docstring_exists()`

Teszteli, hogy a modul docstring létezik.

### ✓ `test_database_factory_exported()`

Teszteli, hogy a DatabaseFactory exportálva van.

### ✓ `test_database_error_exported()`

Teszteli, hogy a DatabaseError exportálva van.

### ✓ `test_db_connection_error_exported()`

Teszteli, hogy a DBConnectionError exportálva van.

### ✓ `test_transaction_error_exported()`

Teszteli, hogy a TransactionError exportálva van.

### ✓ `test_all_exports()`

Teszteli, hogy az __all__ lista tartalmazza az összes exportált elemet.

### ✓ `test_factory_in_all()`

Teszteli, hogy a DatabaseFactory az __all__ listában van.

### ✓ `test_exceptions_in_all()`

Teszteli, hogy az összes exception az __all__ listában van.

### ✓ `test_no_implementation_exports()`

Teszteli, hogy az implementációk NEM exportáltak (DDD szabály).

### ✓ `test_module_file_attribute()`

Teszteli, hogy a modul __file__ attribútuma helyes.

### ✓ `test_module_name_attribute()`

Teszteli, hogy a modul __name__ attribútuma helyes.

### ✓ `test_module_package_attribute()`

Teszteli, hogy a modul __package__ attribútuma helyes.

## Teszt Osztály: `TestDbFactoryImport`

Tesztek a DatabaseFactory importálására.

### ✓ `test_factory_has_create_manager()`

Teszteli, hogy a DatabaseFactory rendelkezik create_manager metódussal.

### ✓ `test_factory_is_class()`

Teszteli, hogy a DatabaseFactory osztály.

## Teszt Osztály: `TestDbExceptionsImport`

Tesztek az exception osztályok importálására.

### ✓ `test_database_error_inheritance()`

Teszteli, hogy a DatabaseError Exception leszármazott.

### ✓ `test_db_connection_error_inheritance()`

Teszteli, hogy a DBConnectionError DatabaseError leszármazott.

### ✓ `test_transaction_error_inheritance()`

Teszteli, hogy a TransactionError DatabaseError leszármazott.

### ✓ `test_exceptions_can_be_raised()`

Teszteli, hogy az exception osztályok dobhatók.

### ✓ `test_exceptions_have_message()`

Teszteli, hogy az exception osztályok üzenettel rendelkeznek.

---

**Teszt fájl:** [`tests/neural_ai/core/db/test_db_init.py`](../../tests/neural_ai/core/db/test_db_init.py)

**Tesztelt modul:** [`neural_ai/core/db/db_init.py`](../../neural_ai/core/db/db_init.py)
