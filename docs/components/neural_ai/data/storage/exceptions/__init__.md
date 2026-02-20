# neural_ai/data/storage/exceptions/__init__.py

Storage komponens kivételek.

## Importok

```python
from typing import TYPE_CHECKING
```

## Konstansok

- **`__all__`**
: `['StorageError', 'StorageFormatError', 'StorageSerializationError', 'StorageIOError', 'StorageNotFoundError', 'StorageValidationError']`


## Osztály: `StorageError(Exception)`

Alap kivétel a storage műveletekhez.

### Metódusok

#### `__init__()`

```python
def __init__(self, message: str, original_error: Exception | None = None) -> None
```

Kivétel inicializálása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): Hibaüzenet
- **`original_error`** (`Exception | None`) = `None`: Eredeti kivétel, ha van

**Visszatérési érték:**

- Típus: `None`

## Osztály: `StorageFormatError(StorageError)`

Nem támogatott vagy érvénytelen formátum esetén.

## Osztály: `StorageSerializationError(StorageError)`

Szerializációs vagy deszerializációs hiba esetén.

## Osztály: `StorageIOError(StorageError)`

I/O műveletek során fellépő hibák esetén.

## Osztály: `StorageNotFoundError(StorageError)`

Nem létező erőforrás esetén.

## Osztály: `StorageValidationError(StorageError)`

Érvénytelen adat vagy paraméter esetén.

---

**Forrásfájl:** [`neural_ai/data/storage/exceptions/__init__.py`](../../neural_ai/data/storage/exceptions/__init__.py)
