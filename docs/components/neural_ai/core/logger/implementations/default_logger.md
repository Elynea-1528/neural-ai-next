# DefaultLogger

## Áttekintés

A `DefaultLogger` egy alapértelmezett logger implementáció, amely a Python standard library `logging` modulját használja. Ez az osztály egyszerű és hatékony naplózási megoldást nyújt, konfigurálható log szinttel, formátummal és stream handlerrel.

## Osztály

```python
class DefaultLogger
```

### Attribútumok

- **logger** (`logging.Logger`): A belső Python logger objektum, amely a tényleges naplózási műveleteket végzi.

### Konstruktor

```python
def __init__(self, name: str, **kwargs: Any) -> None
```

A konstruktor létrehoz egy Python logger objektumot a megadott névvel, eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet, formátumot és stream handlert a kapott paraméterek alapján.

#### Paraméterek

- **name** (`str`): A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
- **kwargs** (`Any`): Opcionális kulcsszó argumentumok:
  - **level** (`int`): Log szint (pl. `logging.DEBUG`, `logging.INFO`). Alapértelmezett: `logging.INFO`.
  - **format** (`str`): Log formátum string. Alapértelmezett: `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`
  - **stream**: Kimeneti stream. Alapértelmezett: `sys.stderr`.

#### Példák

```python
# Alapértelmezett logger létrehozása
logger = DefaultLogger("my_app")

# Egyéni log szinttel
logger = DefaultLogger("my_app", level=logging.DEBUG)

# Egyéni formátummal
logger = DefaultLogger("my_app", format="%(levelname)s: %(message)s")
```

### Metódusok

#### debug

```python
def debug(self, message: str, **kwargs: Any) -> None
```

Debug szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`Any`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.debug("Hibakeresési üzenet", user_id=123)
```

#### info

```python
def info(self, message: str, **kwargs: Any) -> None
```

Info szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`Any`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.info("Sikeres művelet", duration=0.5)
```

#### warning

```python
def warning(self, message: str, **kwargs: Any) -> None
```

Warning szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`Any`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.warning("Elavult API hívás", version="1.0")
```

#### error

```python
def error(self, message: str, **kwargs: Any) -> None
```

Error szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`Any`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.error("Adatbázis kapcsolat hiba", db="main")
```

#### critical

```python
def critical(self, message: str, **kwargs: Any) -> None
```

Critical szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`Any`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.critical("Kritikus rendszerhiba", component="auth")
```

#### set_level

```python
def set_level(self, level: int) -> None
```

Logger log szintjének beállítása. A metódus beállítja a logger és a hozzá tartozó handler minimális log szintjét. Ez határozza meg, hogy melyik szintű üzenetek kerüljenek naplózásra.

**Paraméterek:**
- **level** (`int`): Az új log szint (pl. `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`).

**Példa:**
```python
logger.set_level(logging.DEBUG)
```

#### get_level

```python
def get_level(self) -> int
```

Aktuális log szint lekérése.

**Visszatérési érték:**
- `int`: Az aktuális log szint numerikus értéke. A visszaadott érték a logging modul konstansainak egyike (pl. `logging.INFO` -> 20).

**Példa:**
```python
level = logger.get_level()
print(f"Aktuális log szint: {level}")
```

## Használati Példák

### Alap használat

```python
import logging
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Logger létrehozása
logger = DefaultLogger("my_application")

# Különböző szintű üzenetek logolása
logger.debug("Ez egy debug üzenet")
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés: alacsony a memória")
logger.error("Hiba történt a fájl olvasásakor")
logger.critical("Kritikus hiba: adatbázis elérhetetlen")
```

### Egyéni konfigurációval

```python
import logging
import sys
from io import StringIO
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Egyéni streammel és formátummal
stream = StringIO()
logger = DefaultLogger(
    "custom_app",
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
    stream=stream
)

# Log üzenetek
logger.info("Test message")

# Kimenet lekérése
output = stream.getvalue()
print(output)  # INFO - Test message
```

### Log szint módosítása futás közben

```python
import logging
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

logger = DefaultLogger("dynamic_app", level=logging.INFO)

# Csak INFO és magasabb szintű üzenetek jelennek meg
logger.debug("Ez nem jelenik meg")
logger.info("Ez megjelenik")

# Log szint váltása DEBUG-ra
logger.set_level(logging.DEBUG)

# Most már a DEBUG üzenetek is megjelennek
logger.debug("Ez most már megjelenik")
```

## Jellemzők

- **Egyszerű használat**: A Python standard logging moduljára épül, így ismerős és kiszámítható.
- **Konfigurálható**: Log szint, formátum és stream egyszerűen testreszabható.
- **Handler kezelés**: Automatikusan kezeli a handler-eket, elkerülve a duplikált üzeneteket.
- **Típusbiztonság**: Teljes típusannotációval ellátott, támogatva a modern IDE-k és típusellenőrző eszközök használatát.
- **Dokumentáció**: Magyar nyelvű docstring-ekkel és példákkal ellátott.

## Függőségek

- **Python Standard Library**: `logging` modul
- **Típusellenőrzés**: `typing.TYPE_CHECKING` a körkörös importok elkerülésére

## Kapcsolódó Komponensek

- [`LoggerInterface`](../../interfaces/logger_interface.md): A logger interfész definíciója
- [`LoggerFactory`](logger_factory.md): Logger példányok létrehozásához
- [`ColoredLogger`](colored_logger.md): Színes kimenetű logger implementáció
- [`RotatingFileLogger`](rotating_file_logger.md): Forgatófájlos logger implementáció

## Forráskód

A teljes forráskód elérhető itt: [`neural_ai/core/logger/implementations/default_logger.py`](../../../../../neural_ai/core/logger/implementations/default_logger.py)