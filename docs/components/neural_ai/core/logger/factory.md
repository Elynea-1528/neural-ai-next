# neural_ai/core/logger/factory.py

Logger factory implementáció structlog használatával.

Ez a modul biztosítja a LoggerFactory osztályt, amely felelős a különböző
típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve
lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

A factory kizárólag structlog renderereket használ:
- Console: structlog.dev.ConsoleRenderer(colors=True)
- File: structlog.processors.JSONRenderer()

## Importok

```python
import logging
import sys
from typing import Any
from typing import cast
import structlog
from structlog.processors import JSONRenderer
from structlog.stdlib import ProcessorFormatter
from structlog.types import Processor
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
# ... és még 6 import
```

## Osztály: `LoggerFactory(LoggerFactoryInterface)`

Factory osztály loggerek létrehozásához structlog-gal.

A factory mintát követve centralizálja a logger példányosítást és
életciklus kezelést. Támogatja a különböző logger implementációk
regisztrálását és lekérdezését.

A configure metódus kizárólag structlog renderereket használ:
- Console: structlog.dev.ConsoleRenderer(colors=True)
- File: structlog.processors.JSONRenderer()

Attributes:
    _logger_types: Regisztrált logger típusok és osztályaik.
    _instances: Létrehozott logger példányok gyorsítótárban.

### Metódusok

#### `register_logger()`

```python
def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None
```

Új logger típus regisztrálása.

**Paraméterek:**

- **`cls`**
- **`logger_type`** (`str`): A logger típus neve.
- **`logger_class`** (`type[LoggerInterface]`): A logger osztály.

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`TypeError`**: Ha a logger_class nem implementálja a LoggerInterface-t.

#### `get_logger()`

```python
def get_logger(cls, name: str, logger_type: str = 'default') -> LoggerInterface
```

Logger példány létrehozása vagy visszaadása.

**Paraméterek:**

- **`cls`**
- **`name`** (`str`): A logger egyedi neve.
- **`logger_type`** (`str`) = `'default'`: A kért logger típus ('default', 'colored', 'rotating'). **kwargs: További paraméterek a loggernek (pl. log_file, level).

**Visszatérési érték:**

- Típus: `LoggerInterface`
- LoggerInterface: Az inicializált logger példány.

**Kivételek:**

- **`ValueError`**: Ha a 'rotating' típushoz nincs megadva 'log_file'.
- **`TypeError`**: Ha a létrehozott logger nem implementálja az interfészt.

#### `configure()`

```python
def configure(cls, config: dict[str, Any]) -> None
```

Logger rendszer konfigurálása structlog-gal. A metódus kizárólag structlog renderereket használ: - Console: structlog.dev.ConsoleRenderer(colors=True) - File: structlog.processors.JSONRenderer() Ha a konfiguráció hiányos (nincs handlers szekció), automatikusan fallback módba vált alapértelmezett console handler-rel, és warning-ot logol.

**Paraméterek:**

- **`cls`**
- **`config`** (`dict[str, Any]`): Konfigurációs dict a következő struktúrával: { 'default_level': 'DEBUG', 'handlers': { 'console': { 'enabled': True, 'level': 'DEBUG', 'colored': True }, 'file': { 'enabled': True, 'filename': 'logs/neural_ai.log', 'level': 'DEBUG', 'json_format': True, 'rotating': True, 'max_bytes': 10485760, 'backup_count': 5 } }, 'loggers': { 'neural_ai': {'level': 'DEBUG', 'propagate': True}, 'aiosqlite': {'level': 'WARNING'}, 'asyncio': {'level': 'WARNING'} } }

**Visszatérési érték:**

- Típus: `None`

#### `get_schema_version()`

```python
def get_schema_version(cls) -> str
```

A logger factory sémaváltozatának lekérdezése.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `str`
- str: A sémaváltozat string formátumban (pl. '1.0.0').

#### `set_schema_version()`

```python
def set_schema_version(cls, version: str) -> None
```

A logger factory sémaváltozatának beállítása.

**Paraméterek:**

- **`cls`**
- **`version`** (`str`): Az új sémaváltozat (pl. '1.1.0').

**Visszatérési érték:**

- Típus: `None`

#### `clear_instances()`

```python
def clear_instances(cls) -> None
```

Összes logger példány törlése a gyorsítótárból. Ez a metódus hasznos teszteléskor vagy amikor teljesen új logger példányokat szeretnénk létrehozni.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `None`

#### `get_registered_types()`

```python
def get_registered_types(cls) -> list[str]
```

Regisztrált logger típusok listázása.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `list[str]`
- list[str]: A regisztrált logger típusok neveinek listája.

#### `is_logger_registered()`

```python
def is_logger_registered(cls, logger_type: str) -> bool
```

Ellenőrzi, hogy egy logger típus regisztrálva van-e.

**Paraméterek:**

- **`cls`**
- **`logger_type`** (`str`): A logger típus neve.

**Visszatérési érték:**

- Típus: `bool`
- bool: True, ha a logger típus regisztrálva van, egyébként False.

---

**Forrásfájl:** [`neural_ai/core/logger/factory.py`](../../neural_ai/core/logger/factory.py)
