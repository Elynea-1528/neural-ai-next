# 🧪 Teszt: tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py

**Tesztelt modul:** [`neural_ai/core/db/exceptions/db_exceptions_init.py`](../../neural_ai/core/db/exceptions/db_exceptions_init.py)

Tesztelő modul a neural_ai.core.db.exceptions.__init__.py fájlnak.

Ez a modul tartalmazza azokat a teszteket, amelyek ellenőrzik az exceptions csomag
__init__.py fájljának helyes működését, különös tekintettel az exportált osztályokra.

## Teszt Osztály: `TestExceptionsInit`

Tesztosztály az exceptions csomag __init__.py exportjainak ellenőrzésére.

### ✓ `test_database_error_import()`

Teszteli, hogy a DatabaseError osztály importálható-e.

### ✓ `test_db_connection_error_import()`

Teszteli, hogy a DBConnectionError osztály importálható-e.

### ✓ `test_transaction_error_import()`

Teszteli, hogy a TransactionError osztály importálható-e.

### ✓ `test_all_list_content()`

Teszteli, hogy a __all__ lista csak a várt osztályokat tartalmazza.

### ✓ `test_exception_instantiation()`

Teszteli, hogy az exportált kivétel osztályok példányosíthatók-e.

---

**Teszt fájl:** [`tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py`](../../tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py)

**Tesztelt modul:** [`neural_ai/core/db/exceptions/db_exceptions_init.py`](../../neural_ai/core/db/exceptions/db_exceptions_init.py)
