# neural_ai/core/logger/implementations/colored_logger.py

Színes konzol logger implementáció.

Ez a modul a ColoredLogger osztályt tartalmazza, amely színes konzol kimenetet
biztosít a log üzenetekhez a Python standard logging könyvtárát felhasználva.

## Importok

```python
import logging
import sys
from typing import IO
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
```

## Osztály: `ColoredLogger(LoggerInterface)`

Színes konzol kimenettel rendelkező logger implementáció.

Ez az osztály a LoggerInterface-t implementálja, és színes formázást alkalmaz
a log üzenetekhez a konzolon. A színek a log szinttől függenek, ami segít
a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

Attributes:
    logger: A belső Python logger objektum

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, level: int = logging.INFO, format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', stream: IO[str] = sys.stdout, config: 'ConfigManagerInterface | None' = None, event_bus: 'EventBusInterface | None' = None) -> None
```

Logger inicializálása színes konzol kimenettel.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
- **`level`** (`int`) = `logging.INFO`: A log szint (pl. logging.DEBUG, logging.INFO). Alapértelmezett értéke a logging.INFO.
- **`format_str`** (`str`) = `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`: A log üzenetek formátuma. Alapértelmezett formátum: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
- **`stream`** (`IO[str]`) = `sys.stdout`: A kimeneti stream, ahova a logok íródnak. Alapértelmezett értéke a sys.stdout.
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: Opcionális konfigurációs interfész.
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Opcionális esemény busz interfész. **kwargs: További opcionális paraméterek, amelyeket a jövőbeli bővíthetőség érdekében elfogad az osztály. Példa: >>> logger = ColoredLogger("my_app", level=logging.DEBUG) >>> logger.info("Alkalmazás elindult")

**Visszatérési érték:**

- Típus: `None`

#### `debug()`

```python
def debug(self, message: str) -> None
```

Debug szintű üzenet logolása. Ez a metódus részletes hibakeresési információkat logol, amelyek általában csak fejlesztés közben hasznosak.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó debug üzenet. **kwargs: További paraméterek, amelyek az extra adatokhoz adhatók a log rekordban. Példa: >>> logger.debug("Adatfeldolgozás elkezdődött", file="data.txt")

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

Info szintű üzenet logolása. Ez a metódus általános információkat logol az alkalmazás működéséről.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó info üzenet. **kwargs: További paraméterek az extra adatokhoz. Példa: >>> logger.info("Sikeres bejelentkezés", user="admin")

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

Warning szintű üzenet logolása. Ez a metódus figyelmeztető üzeneteket logol, amelyek nem kritikusak, de érdemes rájuk figyelni.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó warning üzenet. **kwargs: További paraméterek az extra adatokhoz. Példa: >>> logger.warning("A cache majdnem tele van", usage=85)

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

Error szintű üzenet logolása. Ez a metódus hibákat logol, amelyek befolyásolják az alkalmazás működését, de nem okoznak leállást.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó error üzenet. **kwargs: További paraméterek az extra adatokhoz. Példa: >>> logger.error("Adatbázis kapcsolódási hiba", error=str(e))

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

Critical szintű üzenet logolása. Ez a metódus kritikus hibákat logol, amelyek az alkalmazás leállását okozhatják vagy jelentős problémát jeleznek.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A logolandó critical üzenet. **kwargs: További paraméterek az extra adatokhoz. Példa: >>> logger.critical("A rendszer leállt", reason="Nincs elég memória")

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

Logger log szintjének beállítása. Ez a metódus lehetővé teszi a log szint dinamikus módosítását futás közben.

**Paraméterek:**

- **`self`**
- **`level`** (`int`): Az új log szint (pl. logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL). Példa: >>> logger.set_level(logging.DEBUG)

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
- int: Az aktuális log szint numerikus értéke. Példa: >>> current_level = logger.get_level() >>> print(f"Aktuális log szint: {current_level}")

---

**Forrásfájl:** [`neural_ai/core/logger/implementations/colored_logger.py`](../../neural_ai/core/logger/implementations/colored_logger.py)
