# neural_ai/core/logger/implementations/default_logger.py

Alapértelmezett logger implementáció.

Ez a modul a standard logging könyvtár alapú logger implementációt tartalmazza,
amely a Python beépített logging rendszerét használja.

## Importok

```python
import logging
from typing import TYPE_CHECKING
from typing import Any
import structlog
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
```

## Osztály: `DefaultLogger(LoggerInterface)`

Alapértelmezett logger implementáció a Python logging moduljával.

Ez az osztály a Python standard library logging rendszerét használja,
és implementálja a LoggerInterface-t. Konfigurálható log szinttel,
formátummal és stream handlerrel.

Attributes:
    logger: A belső Python logger objektum

### Metódusok

#### `__init__()`

```python
def __init__(self, name: str, config: 'ConfigManagerInterface | None' = None, event_bus: 'EventBusInterface | None' = None, level: int = logging.INFO) -> None
```

Logger inicializálása. A konstruktor létrehoz egy Python logger objektumot a megadott névvel, eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet, formátumot és stream handlert a kapott paraméterek alapján.

**Paraméterek:**

- **`self`**
- **`name`** (`str`): A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
- **`config`** (`'ConfigManagerInterface | None'`) = `None`: Opcionális konfigurációs interfész.
- **`event_bus`** (`'EventBusInterface | None'`) = `None`: Opcionális esemény busz interfész.
- **`level`** (`int`) = `logging.INFO`: A logger alapértelmezett szintje (pl. logging.DEBUG, logging.INFO). **kwargs: Opcionális kulcsszó argumentumok: - format (str): Log formátum string. Alapértelmezett: "%(asctime)s - %(name)s - %(levelname)s - %(message)s" - stream: Kimeneti stream. Alapértelmezett: sys.stderr. Példa: >>> logger = DefaultLogger("my_app") >>> logger = DefaultLogger("my_app", level=logging.DEBUG) >>> logger = DefaultLogger("my_app", ...                       format="%(levelname)s: %(message)s")

**Visszatérési érték:**

- Típus: `None`

#### `debug()`

```python
def debug(self, message: str) -> None
```

Debug szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A log üzenet szövege. **kwargs: További paraméterek, amelyek az extra kulcs alatt kerülnek átadásra a loggernek. Példa: >>> logger.debug("Hibakeresési üzenet", user_id=123)

**Visszatérési érték:**

- Típus: `None`

#### `info()`

```python
def info(self, message: str) -> None
```

Info szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A log üzenet szövege. **kwargs: További paraméterek, amelyek az extra kulcs alatt kerülnek átadásra a loggernek. Példa: >>> logger.info("Sikeres művelet", duration=0.5)

**Visszatérési érték:**

- Típus: `None`

#### `warning()`

```python
def warning(self, message: str) -> None
```

Warning szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A log üzenet szövege. **kwargs: További paraméterek, amelyek az extra kulcs alatt kerülnek átadásra a loggernek. Példa: >>> logger.warning("Elavult API hívás", version="1.0")

**Visszatérési érték:**

- Típus: `None`

#### `error()`

```python
def error(self, message: str) -> None
```

Error szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A log üzenet szövege. **kwargs: További paraméterek, amelyek az extra kulcs alatt kerülnek átadásra a loggernek. Ha exc_info van, külön kezeljük. Példa: >>> logger.error("Adatbázis kapcsolat hiba", db="main")

**Visszatérési érték:**

- Típus: `None`

#### `critical()`

```python
def critical(self, message: str) -> None
```

Critical szintű üzenet logolása.

**Paraméterek:**

- **`self`**
- **`message`** (`str`): A log üzenet szövege. **kwargs: További paraméterek, amelyek az extra kulcs alatt kerülnek átadásra a loggernek. Ha exc_info van, külön kezeljük. Példa: >>> logger.critical("Kritikus rendszerhiba", component="auth")

**Visszatérési érték:**

- Típus: `None`

#### `set_level()`

```python
def set_level(self, level: int) -> None
```

Logger log szintjének beállítása. Beállítja a logger szintjét a példány szintjén.

**Paraméterek:**

- **`self`**
- **`level`** (`int`): Az új log szint. Példa: >>> logger.set_level(logging.DEBUG)

**Visszatérési érték:**

- Típus: `None`

#### `get_level()`

```python
def get_level(self) -> int
```

Aktuális log szint lekérése. Visszaadja a konstruktorban beállított log szintet.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- int: A beállított log szint. Példa: >>> level = logger.get_level() >>> print(f"Aktuális log szint: {level}")

---

**Forrásfájl:** [`neural_ai/core/logger/implementations/default_logger.py`](../../neural_ai/core/logger/implementations/default_logger.py)
