# neural_ai/core/config/interfaces/async_config_interface.py

Aszinkron konfiguráció kezelő interfész.

Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
különösen az adatbázis-alapú dinamikus konfigurációkezelőkhöz.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from collections.abc import Awaitable
from collections.abc import Callable
from typing import TYPE_CHECKING
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from neural_ai.core.logger.interfaces import LoggerInterface
```

## Konstansok

- **`ConfigListener`**
: `Callable[[str, Any], Awaitable[None]]`


## Osztály: `AsyncConfigManagerInterface(ABC)`

Aszinkron konfigurációkezelő interfész.

Ez az interfész definiálja az aszinkron konfigurációkezelők által implementálandó metódusokat,
amelyek főleg adatbázis-alapú dinamikus konfigurációkezelésre szolgálnak.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None, session: 'AsyncSession | None' = None, logger: 'LoggerInterface | None' = None) -> None
```

Inicializálja az aszinkron konfigurációkezelőt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: Konfigurációs fájl útvonala (opcionális, lehet None)
- **`session`** (`'AsyncSession | None'`) = `None`: Adatbázis session interfész (opcionális)
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész (opcionális)

**Visszatérési érték:**

- Típus: `None`

#### `get()`

```python
async def get(self) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`
- A konfigurációs érték vagy az alapértelmezett érték.

#### `get_section()`

```python
async def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`): A konfigurációs szekció/kategória neve.

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A szekció konfigurációs adatai.

**Kivételek:**

- **`KeyError`**: Ha a szekció nem található.

#### `set()`

```python
async def set(self) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha érvénytelen a kulcs vagy érték.

#### `save()`

```python
async def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: A mentési cél (opcionális, implementációfüggő).

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Ha a művelet nem támogatott.

#### `load()`

```python
async def load(self, filename: str) -> None
```

Konfiguráció betöltése.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`): A betöltési forrás.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Ha a művelet nem támogatott.

#### `load_directory()`

```python
async def load_directory(self, path: str) -> None
```

Betölti az összes konfigurációs fájlt egy mappából.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A konfigurációs mappa útvonala.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Ha a művelet nem támogatott.

#### `validate()`

```python
async def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, Any]`): A validáláshoz használt séma.

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`
- Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

#### `add_listener()`

```python
def add_listener(self, callback: ConfigListener) -> None
```

Listener hozzáadása konfiguráció változásokhoz.

**Paraméterek:**

- **`self`**
- **`callback`** (`ConfigListener`): A callback függvény, amelyet hívni kell a változás esetén.

**Visszatérési érték:**

- Típus: `None`

#### `remove_listener()`

```python
def remove_listener(self, callback: ConfigListener) -> None
```

Listener eltávolítása.

**Paraméterek:**

- **`self`**
- **`callback`** (`ConfigListener`): Az eltávolítandó callback függvény.

**Visszatérési érték:**

- Típus: `None`

#### `start_hot_reload()`

```python
async def start_hot_reload(self, interval: float = 5.0) -> None
```

Hot reload indítása (háttérben fut).

**Paraméterek:**

- **`self`**
- **`interval`** (`float`) = `5.0`: Az ellenőrzési időköz másodpercben.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`RuntimeError`**: Ha a hot reload már fut.

#### `stop_hot_reload()`

```python
async def stop_hot_reload(self) -> None
```

Hot reload leállítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `get_all()`

```python
async def get_all(self, category: str | None = None) -> dict[str, Any]
```

Összes konfiguráció lekérdezése.

**Paraméterek:**

- **`self`**
- **`category`** (`str | None`) = `None`: Opcionális kategória szűréshez.

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Szótár az összes (vagy kategóriához tartozó) konfigurációval.

#### `set_with_metadata()`

```python
async def set_with_metadata(self, key: str, value: Any, category: str = 'system', description: str | None = None, is_active: bool = True) -> None
```

Konfiguráció beállítása metaadatokkal.

**Paraméterek:**

- **`self`**
- **`key`** (`str`): A konfigurációs kulcs.
- **`value`** (`Any`): A konfigurációs érték.
- **`category`** (`str`) = `'system'`: A konfiguráció kategóriája.
- **`description`** (`str | None`) = `None`: A konfiguráció leírása.
- **`is_active`** (`bool`) = `True`: A konfiguráció aktív-e.

**Visszatérési érték:**

- Típus: `None`

#### `delete()`

```python
async def delete(self, key: str) -> bool
```

Konfiguráció törlése (soft delete).

**Paraméterek:**

- **`self`**
- **`key`** (`str`): A törlendő konfigurációs kulcs.

**Visszatérési érték:**

- Típus: `bool`
- True ha a konfiguráció törölve lett, False ha nem található.

---

**Forrásfájl:** [`neural_ai/core/config/interfaces/async_config_interface.py`](../../neural_ai/core/config/interfaces/async_config_interface.py)
