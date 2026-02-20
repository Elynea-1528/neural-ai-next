# tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py

StorageFactoryInterface teszt modul.

Ez a modul tartalmazza a StorageFactoryInterface interfész tesztjeit.

## Importok

```python
import inspect
import pytest
from neural_ai.data.storage.interfaces.factory_interface import StorageFactoryInterface
```

## Osztály: `TestStorageFactoryInterface`

StorageFactoryInterface interfész tesztjei.

### Metódusok

#### `test_is_protocol()`

```python
def test_is_protocol(self) -> None
```

Teszteli, hogy az interfész Protocol-t használ.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_register_storage_method()`

```python
def test_has_register_storage_method(self) -> None
```

Teszteli, hogy az interfész rendelkezik register_storage metódussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_has_get_storage_method()`

```python
def test_has_get_storage_method(self) -> None
```

Teszteli, hogy az interfész rendelkezik get_storage metódussal.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_cannot_instantiate_directly()`

```python
def test_cannot_instantiate_directly(self) -> None
```

Teszteli, hogy az interfész nem példányosítható közvetlenül.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_register_storage_signature()`

```python
def test_register_storage_signature(self) -> None
```

Teszteli a register_storage metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_storage_signature()`

```python
def test_get_storage_signature(self) -> None
```

Teszteli a get_storage metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py`](../../tests/neural_ai/data/storage/interfaces/test_storage_factory_interface.py)
