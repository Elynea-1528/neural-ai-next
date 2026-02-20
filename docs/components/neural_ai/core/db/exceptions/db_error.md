# neural_ai/core/db/exceptions/db_error.py

Adatbázis-specifikus kivételek.

Ez a modul tartalmazza az összes adatbázis-műveletekhez kapcsolódó kivételeket.

## Importok

```python
from neural_ai.core.base.exceptions import NeuralAIException
```

## Osztály: `DatabaseError(NeuralAIException)`

Általános adatbázis hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, details: str | None = None) -> None
```

Inicializálja a DatabaseError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`details`** (`str | None`) = `None`: Opcionális részletes leírás a hibáról.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `DBConnectionError(DatabaseError)`

Adatbázis kapcsolat hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, connection_string: str | None = None) -> None
```

Inicializálja a DBConnectionError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`connection_string`** (`str | None`) = `None`: Az adatbázis kapcsolati sztringje.

**Visszatérési érték:**

- Típus: `None`

## Osztály: `TransactionError(DatabaseError)`

Tranzakció hiba.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, transaction_id: str | None = None) -> None
```

Inicializálja a TransactionError kivételt.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A hibaüzenet.
- **`transaction_id`** (`str | None`) = `None`: A tranzakció azonosítója.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/db/exceptions/db_error.py`](../../neural_ai/core/db/exceptions/db_error.py)
