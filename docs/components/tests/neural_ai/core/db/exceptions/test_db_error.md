# tests/neural_ai/core/db/exceptions/test_db_error.py

Adatbázis kivételek tesztek.

## Importok

```python
from neural_ai.core.base.exceptions import NeuralAIException
from neural_ai.core.db.exceptions.db_error import DatabaseError
from neural_ai.core.db.exceptions.db_error import DBConnectionError
from neural_ai.core.db.exceptions.db_error import TransactionError
```

## Osztály: `TestDatabaseError`

DatabaseError osztály tesztei.

### Metódusok

#### `test_database_error_creation()`

```python
def test_database_error_creation(self) -> None
```

DatabaseError létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_error_with_details()`

```python
def test_database_error_with_details(self) -> None
```

DatabaseError létrehozása részletekkel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_database_error_is_neural_ai_exception()`

```python
def test_database_error_is_neural_ai_exception(self) -> None
```

DatabaseError NeuralAIException-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestDBConnectionError`

DBConnectionError osztály tesztei.

### Metódusok

#### `test_db_connection_error_creation()`

```python
def test_db_connection_error_creation(self) -> None
```

DBConnectionError létrehozásának tesztelése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_db_connection_error_with_connection_string()`

```python
def test_db_connection_error_with_connection_string(self) -> None
```

DBConnectionError létrehozása connection stringgel.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_db_connection_error_inheritance()`

```python
def test_db_connection_error_inheritance(self) -> None
```

DBConnectionError DatabaseError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TestTransactionError`

TransactionError osztály tesztei.

### Metódusok

#### `test_transaction_error_creation()`

```python
def test_transaction_error_creation(self) -> None
```

TransactionError létrehozásának tesztelése (47-48. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_transaction_error_with_transaction_id()`

```python
def test_transaction_error_with_transaction_id(self) -> None
```

TransactionError létrehozása transaction ID-vel (47-48. sorok).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_transaction_error_inheritance()`

```python
def test_transaction_error_inheritance(self) -> None
```

TransactionError DatabaseError-ből származik.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/exceptions/test_db_error.py`](../../tests/neural_ai/core/db/exceptions/test_db_error.py)
