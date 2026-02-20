# neural_ai/core/logger/implementations/rotating_file_logger.py

Rotáló fájl logger implementáció.

## Importok

```python
import logging
import os
import shutil
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Literal
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
# ... és még 1 import
```

## Osztály: `RotatingFileLogger(LoggerInterface)`

File alapú logger, ami automatikusan rotálja a log fájlokat.

A logger támogatja a méret alapú és idő alapú rotációt is. A méret alapú
rotáció esetén a fájl elér egy bizonyos méretet, az idő alapú rotáció
esetén pedig egy adott időközönként történik a rotáció.

Attributes:
    logger: A Python logging logger példány

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, log_file: str, level: int = logging.INFO, max_bytes: int = 1024 * 1024, backup_count: int = 5, format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', rotation_type: Literal['size', 'time'] = 'size', when: str = 'D', config: 'ConfigManagerInterface | None' = None, event_bus: 'EventBusInterface | None' = None) -> None
```

Logger inicializálása.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A logger egyedi neve.
- **`log_file`** (`str`): A log fájl teljes útvonala.
- **`level`** (`int`) = `logging.INFO`: A log szint (alapértelmezett: INFO).
- **`max_bytes`** (`int`) = `1024 * 1024`: Maximum fájlméret bájtban rotálás előtt (méret alapú rotációhoz).
- **`backup_count`** (`int`) = `5`: Megtartott backup fájlok száma.
- **`format_str`** (`str`) = `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`: A log üzenetek formátuma.
- **`rotation_type`** (`Literal['size', 'time']`) = `'size'`: A rotáció típusa ('size' vagy 'time').
- **`when`** (`str`) = `'D'`: Időegység időalapú rotáció esetén ('S', 'M', 'H', 'D', stb.).
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: Opcionális konfigurációs interfész.
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Opcionális esemény busz interfész. **kwargs: További paraméterek (az interfész kompatibilitás miatt).

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha a log_file nincs megadva vagy érvénytelen a rotation_type.

#### `debug()`

```python
def debug(self, message: str) -> None
```

Debug szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó üzenet. **kwargs: További paraméterek (pl. extra adatok a loghoz).

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

Info szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó üzenet. **kwargs: További paraméterek (pl. extra adatok a loghoz).

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

Warning szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó üzenet. **kwargs: További paraméterek (pl. extra adatok a loghoz).

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

Error szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó üzenet. **kwargs: További paraméterek (pl. extra adatok a loghoz).

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

Critical szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó üzenet. **kwargs: További paraméterek (pl. extra adatok a loghoz).

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

Logger log szintjének beállítása.

**Paraméterek:**

- **`self`**
- **`level`** (`int`): Az új log szint (pl. logging.DEBUG, logging.INFO).

**Visszatérési érték:**

- Típus: `None`

#### `get_level()`

```python
def get_level(self) -> int
```

Aktuális log szint lekérése.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- Az aktuális log szint értéke.

#### `clean_old_logs()`

```python
def clean_old_logs(log_dir: str | Path) -> None
```

Régi log fájlok eltávolítása. Figyelmeztetés: Ez a metódus véglegesen törli a log könyvtárat és annak teljes tartalmát!

**Paraméterek:**

- **`log_dir`** (`str | Path`): A log könyvtár útvonala.

**Visszatérési érték:**

- Típus: `None`

---

**Forrásfájl:** [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../neural_ai/core/logger/implementations/rotating_file_logger.py)
