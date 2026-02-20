# neural_ai/core/config/interfaces/config_interface.py

Konfiguráció kezelő interfész.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import Any
```

## Konstansok

- **`ConfigInterface`**
: `ConfigManagerInterface`


## Osztály: `ConfigManagerInterface(ABC)`

Konfigurációkezelő interfész.

Ez az interfész definiálja a konfigurációkezelők által implementálandó metódusokat.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None) -> None
```

Inicializálja a konfigurációkezelőt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: Konfigurációs fájl útvonala (opcionális) **kwargs: További opcionális paraméterek a konkrét implementációknak

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
def get(self) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`

#### `get_section()`

```python
def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`)

**Visszatérési érték:**

- Típus: `dict[str, Any]`

#### `set()`

```python
def set(self) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `save()`

```python
def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése fájlba.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`

**Visszatérési érték:**

- Típus: `None`

#### `load()`

```python
def load(self, filename: str) -> None
```

Konfiguráció betöltése fájlból.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`)

**Visszatérési érték:**

- Típus: `None`

#### `load_directory()`

```python
def load_directory(self, path: str) -> None
```

Betölti az összes YAML fájlt egy mappából namespaced struktúrába.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A konfigurációs mappa útvonala

**Visszatérési érték:**

- Típus: `None`

#### `validate()`

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, Any]`): A validáláshoz használt séma

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`
- Tuple[bool, Optional[Dict[str, str]]]: (érvényes-e, hibák szótára)

---

**Forrásfájl:** [`neural_ai/core/config/interfaces/config_interface.py`](../../neural_ai/core/config/interfaces/config_interface.py)
