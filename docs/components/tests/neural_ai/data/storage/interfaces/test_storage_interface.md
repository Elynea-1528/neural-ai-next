# tests/neural_ai/data/storage/interfaces/test_storage_interface.py

StorageInterface teszt modul.

Ez a modul tartalmazza a StorageInterface interfész tesztjeit.

## Importok

```python
import inspect
import pytest
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
```

## Osztály: `TestStorageInterface`

StorageInterface interfész tesztjei.

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

#### `test_has_required_methods()`

```python
def test_has_required_methods(self) -> None
```

Teszteli, hogy az interfész rendelkezik az összes szükséges metódussal.

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

#### `test_save_dataframe_signature()`

```python
def test_save_dataframe_signature(self) -> None
```

Teszteli a save_dataframe metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_dataframe_signature()`

```python
def test_load_dataframe_signature(self) -> None
```

Teszteli a load_dataframe metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_save_object_signature()`

```python
def test_save_object_signature(self) -> None
```

Teszteli a save_object metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_load_object_signature()`

```python
def test_load_object_signature(self) -> None
```

Teszteli a load_object metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_exists_signature()`

```python
def test_exists_signature(self) -> None
```

Teszteli az exists metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_get_metadata_signature()`

```python
def test_get_metadata_signature(self) -> None
```

Teszteli a get_metadata metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_delete_signature()`

```python
def test_delete_signature(self) -> None
```

Teszteli a delete metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `test_list_dir_signature()`

```python
def test_list_dir_signature(self) -> None
```

Teszteli a list_dir metódus aláírását.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`tests/neural_ai/data/storage/interfaces/test_storage_interface.py`](../../tests/neural_ai/data/storage/interfaces/test_storage_interface.py)
