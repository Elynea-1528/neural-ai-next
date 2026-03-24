# 🧪 Teszt: tests/neural_ai/core/db/exceptions/test_db_error.py

**Tesztelt modul:** [`neural_ai/core/db/exceptions/db_error.py`](../../neural_ai/core/db/exceptions/db_error.py)

Adatbázis kivételek tesztek.

## Teszt Osztály: `TestDatabaseError`

DatabaseError osztály tesztei.

### ✓ `test_database_error_creation()`

DatabaseError létrehozásának tesztelése.

### ✓ `test_database_error_with_details()`

DatabaseError létrehozása részletekkel.

### ✓ `test_database_error_is_neural_ai_exception()`

DatabaseError NeuralAIException-ből származik.

## Teszt Osztály: `TestDBConnectionError`

DBConnectionError osztály tesztei.

### ✓ `test_db_connection_error_creation()`

DBConnectionError létrehozásának tesztelése.

### ✓ `test_db_connection_error_with_connection_string()`

DBConnectionError létrehozása connection stringgel.

### ✓ `test_db_connection_error_inheritance()`

DBConnectionError DatabaseError-ből származik.

## Teszt Osztály: `TestTransactionError`

TransactionError osztály tesztei.

### ✓ `test_transaction_error_creation()`

TransactionError létrehozásának tesztelése (47-48. sorok).

### ✓ `test_transaction_error_with_transaction_id()`

TransactionError létrehozása transaction ID-vel (47-48. sorok).

### ✓ `test_transaction_error_inheritance()`

TransactionError DatabaseError-ből származik.

---

**Teszt fájl:** [`tests/neural_ai/core/db/exceptions/test_db_error.py`](../../tests/neural_ai/core/db/exceptions/test_db_error.py)

**Tesztelt modul:** [`neural_ai/core/db/exceptions/db_error.py`](../../neural_ai/core/db/exceptions/db_error.py)
