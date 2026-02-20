# neural_ai/core/config/implementations/dynamic_config_manager.py

Dinamikus konfiguráció kezelő implementáció.

Ez a modul implementálja a DynamicConfigManager osztályt, amely a futás közben
módosítható konfigurációkat kezeli SQL adatbázisban tárolva, hot reload támogatással.

## Importok

```python
import asyncio
from collections.abc import Awaitable
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import cast
from sqlalchemy import select
# ... és még 5 import
```

## Konstansok

- **`ConfigListener`**
: `Callable[[str, Any], Awaitable[None]]`


## Osztály: `DynamicConfigManager(AsyncConfigManagerInterface)`

Dinamikus konfiguráció kezelő SQL adatbázissal.

Ez az osztály kezeli a futás közben módosítható konfigurációkat, amelyek
hot reload támogatással rendelkeznek. A konfigurációk SQL adatbázisban
tárolódnak, és változásukról a rendszer azonnal értesítést kap.

Attributes:
    session: Az adatbázis session (Dependency Injection).
    logger: Logger interfész a naplózásra (opcionális).
    _cache: Konfigurációs értékek gyorsítótára.
    _listeners: Konfiguráció változásokat figyelő callback-ek listája.
    _last_update: Az utolsó frissítés időpontja.
    _hot_reload_task: A háttérben futó hot reload task referenciája.
    _stop_hot_reload: Esemény a hot reload leállításához.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None, session: AsyncSession | None = None, logger: 'LoggerInterface | None' = None) -> None
```

Inicializálja a DynamicConfigManager-t.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: Nincs használatban, csak a kompatibilitás miatt (deprecated).
- **`session`** (`AsyncSession | None`) = `None`: Az adatbázis session (kötelező a működéshez).
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális).

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha nincs megadva session.

#### `get()`

```python
async def get(self) -> str | int | float | bool | list[Any] | dict[str, Any] | None
```

Konfigurációs érték lekérdezése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str | int | float | bool | list[Any] | dict[str, Any] | None`
- A konfigurációs érték vagy az alapértelmezett érték.

**Kivételek:**

- **`ValueError`**: Ha több kulcsot adnak meg.

#### `set()`

```python
async def set(self) -> None
```

Konfigurációs érték beállítása.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha több kulcsot adnak meg vagy érvénytelen az érték.

#### `get_section()`

```python
async def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése kategória alapján.

**Paraméterek:**

- **`self`**
- **`section`** (`str`): A konfigurációs kategória neve.

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A kategóriához tartozó összes konfigurációs érték.

**Kivételek:**

- **`KeyError`**: Ha a kategória nem található vagy nincs aktív konfiguráció.

#### `save()`

```python
async def save(self, filename: str | None = None) -> None
```

Konfiguráció mentése (nincs értelmezve dinamikus konfigurációnál). A DynamicConfigManager nem támogatja a fájlba mentést, mivel az adatbázisban tárol. Ez a metódus csak a kompatibilitás miatt van jelen.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: Nincs használatban.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Mindig, mivel nem támogatott művelet.

#### `load()`

```python
async def load(self, filename: str) -> None
```

Konfiguráció betöltése (nincs értelmezve dinamikus konfigurációnál). A DynamicConfigManager nem támogatja a fájlból betöltést, mivel az adatbázisból olvas. Ez a metódus csak a kompatibilitás miatt van jelen.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`): Nincs használatban.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Mindig, mivel nem támogatott művelet.

#### `load_directory()`

```python
async def load_directory(self, path: str) -> None
```

Konfigurációs mappa betöltése (nincs értelmezve dinamikus konfigurációnál). A DynamicConfigManager nem támogatja a mappából betöltést. Ez a metódus csak a kompatibilitás miatt van jelen.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): Nincs használatban.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`NotImplementedError`**: Mindig, mivel nem támogatott művelet.

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
- Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None) Note: A validáció jelenleg csak a cache-ben lévő értékeket ellenőrzi.

#### `add_listener()`

```python
def add_listener(self, callback: ConfigListener) -> None
```

Listener hozzáadása konfiguráció változásokhoz.

**Paraméterek:**

- **`self`**
- **`callback`** (`ConfigListener`): A callback függvény, amelyet hívni kell a változás esetén. A callbacknek két paramétert kell fogadnia: (key, value).

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

Hot reload indítása (háttérben fut). A hot reload rendszeres időközönként ellenőrzi az adatbázist konfigurációs változásokért, és frissíti a cache-t.

**Paraméterek:**

- **`self`**
- **`interval`** (`float`) = `5.0`: Az ellenőrzési időköz másodpercben (alapértelmezett: 5.0).

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`RuntimeError`**: Ha a hot reload már fut.

#### `_hot_reload_loop()`

```python
async def _hot_reload_loop() -> None
```

A hot reload fő ciklusa.

**Visszatérési érték:**

- Típus: `None`

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
- **`category`** (`str`) = `'system'`: A konfiguráció kategóriája (alapértelmezett: "system").
- **`description`** (`str | None`) = `None`: A konfiguráció leírása (opcionális).
- **`is_active`** (`bool`) = `True`: A konfiguráció aktív-e (alapértelmezett: True).

**Visszatérési érték:**

- Típus: `None`

#### `delete()`

```python
async def delete(self, key: str) -> bool
```

Konfiguráció törlése (soft delete: is_active = False).

**Paraméterek:**

- **`self`**
- **`key`** (`str`): A törlendő konfigurációs kulcs.

**Visszatérési érték:**

- Típus: `bool`
- True ha a konfiguráció törölve lett, False ha nem található.

**Kivételek:**

- **`ConfigError`**: Ha hiba történik a törlés során.

#### `_notify_listeners()`

```python
async def _notify_listeners(self, key: str, value: Any) -> None
```

Listener-ek értesítése konfiguráció változásról.

**Paraméterek:**

- **`self`**
- **`key`** (`str`): A megváltozott konfigurációs kulcs.
- **`value`** (`Any`): Az új konfigurációs érték.

**Visszatérési érték:**

- Típus: `None`

#### `_check_for_updates()`

```python
async def _check_for_updates(self) -> None
```

Ellenőrzi, hogy történt-e változás az adatbázisban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

#### `_determine_value_type()`

```python
def _determine_value_type(value: Any) -> str
```

Érték típusának meghatározása.

**Paraméterek:**

- **`value`** (`Any`): Az ellenőrizendő érték.

**Visszatérési érték:**

- Típus: `str`
- Az érték típusa string formátumban.

---

**Forrásfájl:** [`neural_ai/core/config/implementations/dynamic_config_manager.py`](../../neural_ai/core/config/implementations/dynamic_config_manager.py)
