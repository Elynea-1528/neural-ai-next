# RotatingFileLogger

## Áttekintés

A `RotatingFileLogger` egy fejlett logger implementáció, amely a Python standard library `logging` modulját használja, és támogatja a log fájlok automatikus rotációját. Ez az osztály lehetővé teszi a log fájlok méret vagy idő alapú rotációját, így biztosítva, hogy a log fájlok ne nőjenek túl nagyra, és könnyen kezelhetők legyenek.

## Osztály

```python
class RotatingFileLogger
```

### Attribútumok

- **logger** (`logging.Logger`): A belső Python logger objektum, amely a tényleges naplózási műveleteket végzi.

### Konstruktor

```python
def __init__(
    self,
    name: str,
    log_file: str,
    level: int = logging.INFO,
    max_bytes: int = 1024 * 1024,
    backup_count: int = 5,
    format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    rotation_type: Literal["size", "time"] = "size",
    when: str = "D",
    **kwargs: object
) -> None
```

A konstruktor létrehoz egy Python logger objektumot a megadott névvel, eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet, formátumot és file handlert a kapott paraméterek alapján.

#### Paraméterek

- **name** (`str`): A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
- **log_file** (`str`): A log fájl teljes útvonala. Ez egy kötelező paraméter.
- **level** (`int`): Log szint (pl. `logging.DEBUG`, `logging.INFO`). Alapértelmezett: `logging.INFO`.
- **max_bytes** (`int`): Maximum fájlméret bájtban rotálás előtt (csak méret alapú rotáció esetén). Alapértelmezett: 1MB (1024 * 1024).
- **backup_count** (`int`): Megtartott backup fájlok száma. Alapértelmezett: 5.
- **format_str** (`str`): Log formátum string. Alapértelmezett: `"%(asctime)s - %(name)s - %(levelname)s - %(message)s"`.
- **rotation_type** (`Literal["size", "time"]`): A rotáció típusa. Lehet 'size' (méret alapú) vagy 'time' (idő alapú). Alapértelmezett: 'size'.
- **when** (`str`): Időegység időalapú rotáció esetén ('S' - másodperc, 'M' - perc, 'H' - óra, 'D' - nap, stb.). Alapértelmezett: 'D' (naponta).
- **kwargs** (`object`): További paraméterek (az interfész kompatibilitás miatt).

#### Kivételek

- **ValueError**: Ha a `log_file` paraméter nincs megadva vagy érvénytelen a `rotation_type`.

#### Példák

```python
import logging
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# Alapértelmezett méret alapú rotációval
logger = RotatingFileLogger("my_app", log_file="/var/log/myapp.log")

# Egyéni mérettel és több backup fájllal
logger = RotatingFileLogger(
    "my_app",
    log_file="/var/log/myapp.log",
    max_bytes=5 * 1024 * 1024,  # 5MB
    backup_count=10
)

# Idő alapú rotáció (óránként)
logger = RotatingFileLogger(
    "my_app",
    log_file="/var/log/myapp.log",
    rotation_type="time",
    when="H"
)
```

### Metódusok

#### debug

```python
def debug(self, message: str, **kwargs: object) -> None
```

Debug szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`object`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.debug("Hibakeresési üzenet", user_id=123)
```

#### info

```python
def info(self, message: str, **kwargs: object) -> None
```

Info szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`object`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.info("Sikeres művelet", duration=0.5)
```

#### warning

```python
def warning(self, message: str, **kwargs: object) -> None
```

Warning szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`object`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.warning("Elavult API hívás", version="1.0")
```

#### error

```python
def error(self, message: str, **kwargs: object) -> None
```

Error szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`object`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

**Példa:**
```python
logger.error("Adatbázis kapcsolat hiba", db="main")
```

#### critical

```python
def critical(self, message: str, **kwargs: object) -> None
```

Critical szintű üzenet logolása.

**Paraméterek:**
- **message** (`str`): A log üzenet szövege.
- **kwargs** (`object`): További paraméterek, amelyek az `extra` kulcs alatt kerülnek átadásra a loggernek.

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

#### clean_old_logs

```python
@staticmethod
def clean_old_logs(log_dir: Union[str, Path]) -> None
```

Régi log fájlok eltávolítása. Ez a statikus metódus véglegesen törli a megadott log könyvtárat és annak teljes tartalmát.

**Figyelmeztetés:** Ez a metódus véglegesen törli a log könyvtárat és annak teljes tartalmát!

**Paraméterek:**
- **log_dir** (`Union[str, Path]`): A log könyvtár útvonala.

**Példa:**
```python
RotatingFileLogger.clean_old_logs("/var/log/old_logs")
```

## Használati Példák

### Alap használat

```python
import logging
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# Logger létrehozása alapértelmezett rotációval
logger = RotatingFileLogger("my_application", log_file="logs/app.log")

# Különböző szintű üzenetek logolása
logger.debug("Ez egy debug üzenet")
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés: alacsony a memória")
logger.error("Hiba történt a fájl olvasásakor")
logger.critical("Kritikus hiba: adatbázis elérhetetlen")
```

### Méret alapú rotáció

```python
import logging
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# Logger létrehozása 5MB-os rotációval és 10 backup fájllal
logger = RotatingFileLogger(
    "my_app",
    log_file="logs/app.log",
    max_bytes=5 * 1024 * 1024,  # 5MB
    backup_count=10,
    level=logging.DEBUG
)

# Sok log üzenet generálása a rotáció teszteléséhez
for i in range(10000):
    logger.info(f"Log message {i}")
```

### Idő alapú rotáció

```python
import logging
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# Logger létrehozása óránkénti rotációval
logger = RotatingFileLogger(
    "my_app",
    log_file="logs/app.log",
    rotation_type="time",
    when="H",  # Óránként
    backup_count=24  # 24 óra (1 nap) log megtartása
)

logger.info("Ez az üzenet óránként rotálódik")
```

### Egyéni formátummal

```python
import logging
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# Logger létrehozása egyéni formátummal
logger = RotatingFileLogger(
    "my_app",
    log_file="logs/app.log",
    format_str="%(asctime)s [%(levelname)s] %(message)s"
)

logger.info("Egyéni formátumú log üzenet")
```

### Log könyvtár automatikus létrehozása

```python
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

# A logger automatikusan létrehozza a könyvtárat, ha az nem létezik
logger = RotatingFileLogger(
    "my_app",
    log_file="logs/nested/deep/app.log"  # A 'logs/nested/deep' könyvtár automatikusan létrejön
)

logger.info("A könyvtár automatikusan létrejött")
```

## Jellemzők

- **Automatikus rotáció**: Támogatja a méret és idő alapú rotációt.
- **Konfigurálható**: Log szint, formátum, rotációs paraméterek egyszerűen testreszabhatók.
- **Handler kezelés**: Automatikusan kezeli a handler-eket, elkerülve a duplikált üzeneteket.
- **Könyvtár létrehozás**: Automatikusan létrehozza a szükséges könyvtárakat.
- **Típusbiztonság**: Teljes típusannotációval ellátott, támogatva a modern IDE-k és típusellenőrző eszközök használatát.
- **Dokumentáció**: Magyar nyelvű docstring-ekkel és példákkal ellátott.

## Függőségek

- **Python Standard Library**: `logging` modul, `logging.handlers`
- **Típusellenőrzés**: `typing.Union`, `typing.Literal`, `pathlib.Path`

## Kapcsolódó Komponensek

- [`LoggerInterface`](../../interfaces/logger_interface.md): A logger interfész definíciója
- [`LoggerFactory`](logger_factory.md): Logger példányok létrehozásához
- [`DefaultLogger`](default_logger.md): Alapértelmezett logger implementáció
- [`ColoredLogger`](colored_logger.md): Színes kimenetű logger implementáció

## Forráskód

A teljes forráskód elérhető itt: [`neural_ai/core/logger/implementations/rotating_file_logger.py`](../../../../../neural_ai/core/logger/implementations/rotating_file_logger.py)