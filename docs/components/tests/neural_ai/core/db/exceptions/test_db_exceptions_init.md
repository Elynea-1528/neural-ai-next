# tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py

Tesztelő modul a neural_ai.core.db.exceptions.__init__.py fájlnak.

Ez a modul tartalmazza azokat a teszteket, amelyek ellenőrzik az exceptions csomag
__init__.py fájljának helyes működését, különös tekintettel az exportált osztályokra.

## Importok

```python
from neural_ai.core.db.exceptions import DatabaseError
from neural_ai.core.db.exceptions import DBConnectionError
from neural_ai.core.db.exceptions import TransactionError
from neural_ai.core.db.exceptions import __all__
```

## Osztály: `TestExceptionsInit`

Tesztosztály az exceptions csomag __init__.py exportjainak ellenőrzésére.

### Metódusok

#### `test_database_error_import()`

```python
def test_database_error_import(self) -> None
```

Teszteli, hogy a DatabaseError osztály importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_db_connection_error_import()`

```python
def test_db_connection_error_import(self) -> None
```

Teszteli, hogy a DBConnectionError osztály importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_transaction_error_import()`

```python
def test_transaction_error_import(self) -> None
```

Teszteli, hogy a TransactionError osztály importálható-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_all_list_content()`

```python
def test_all_list_content(self) -> None
```

Teszteli, hogy a __all__ lista csak a várt osztályokat tartalmazza.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exception_instantiation()`

```python
def test_exception_instantiation(self) -> None
```

Teszteli, hogy az exportált kivétel osztályok példányosíthatók-e.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py`](../../tests/neural_ai/core/db/exceptions/test_db_exceptions_init.py)
