# RotatingFileLogger - Rotáló Fájl Logger

## Áttekintés

File alapú logger, ami automatikusan rotálja a log fájlokat. A logger támogatja a méret alapú és idő alapú rotációt is. A méret alapú rotáció esetén a fájl elér egy bizonyos méretet, az idő alapú rotáció esetén pedig egy adott időközönként történik a rotáció.

## Osztály leírása

```python
class RotatingFileLogger(LoggerInterface):
    """File alapú logger, ami automatikusan rotálja a log fájlokat.

    A logger támogatja a méret alapú és idő alapú rotációt is. A méret alapú
    rotáció esetén a fájl elér egy bizonyos méretet, az idő alapú rotáció
    esetén pedig egy adott időközönként történik a rotáció.

    Attributes:
        logger: A Python logging logger példány
    """
```

## Inicializálás

```python
def __init__(
    self,
    name: str,
    log_file: str,
    level: int = logging.INFO,
    max_bytes: int = 1024 * 1024,  # 1MB
    backup_count: int = 5,
    format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    rotation_type: Literal["size", "time"] = "size",
    when: str = "D",
    **kwargs: object,
) -> None:
    """Logger inicializálása.

    Args:
        name: A logger egyedi neve.
        log_file: A log fájl teljes útvonala.
        level: A log szint (alapértelmezett: INFO).
        max_bytes: Maximum fájlméret bájtban rotálás előtt (méret alapú rotációhoz).
        backup_count: Megtartott backup fájlok száma.
        format_str: A log üzenetek formátuma.
        rotation_type: A rotáció típusa ('size' vagy 'time').
        when: Időegység időalapú rotáció esetén ('S', 'M', 'H', 'D', stb.).
        **kwargs: További paraméterek (az interfész kompatibilitás miatt).

    Raises:
        ValueError: Ha a log_file nincs megadva vagy érvénytelen a rotation_type.
    """
```

## Paraméterek

- `name` (str): A logger egyedi neve
- `log_file` (str): A log fájl teljes útvonala (kötelező)
- `level` (int, opcionális): Log szint, alapértelmezett: `logging.INFO`
- `max_bytes` (int, opcionális): Maximum fájlméret bájtban, alapértelmezett: 1MB
- `backup_count` (int, opcionális): Megtartott backup fájlok száma, alapértelmezett: 5
- `format_str` (str, opcionális): Log formátum string
- `rotation_type` (Literal["size", "time"], opcionális): Rotáció típusa, alapértelmezett: "size"
- `when` (str, opcionális): Időegység időalapú rotációhoz, alapértelmezett: "D"
- `**kwargs`: További paraméterek

## Rotáció típusok

### Méret alapú rotáció (`rotation_type="size"`)

A fájl automatikusan rotálódik, amikor eléri a megadott méretet.

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

logger = RotatingFileLogger(
    name="my_app",
    log_file="/var/log/app.log",
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5,
    rotation_type="size"
)
```

### Idő alapú rotáció (`rotation_type="time"`)

A fájl adott időközönként rotálódik.

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

logger = RotatingFileLogger(
    name="my_app",
    log_file="/var/log/app.log",
    backup_count=7,
    rotation_type="time",
    when="D"  # Napi rotáció
)
```

## Időegységek (`when` paraméter)

- `'S'`: Másodperc
- `'M'`: Perc
- `'H'`: Óra
- `'D'`: Nap
- `'W0'-'W6'`: Hét (0=hétfő, 6=vasárnap)
- `'midnight'`: Éjfél

## Alap használat

### Méret alapú rotáció

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

# 5MB-os rotáció
logger = RotatingFileLogger(
    name="my_app",
    log_file="logs/app.log",
    max_bytes=5*1024*1024,
    backup_count=3,
    level=logging.DEBUG
)

# Használat
for i in range(10000):
    logger.info(f"Log üzenet {i}")
    # Amikor a fájl eléri az 5MB-ot, rotálódik
```

### Idő alapú rotáció

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

# Napi rotáció
logger = RotatingFileLogger(
    name="my_app",
    log_file="logs/app.log",
    backup_count=30,  # 30 napig tartjuk meg
    rotation_type="time",
    when="D",
    level=logging.INFO
)

# Használat
logger.info("Napi log üzenet")
# A fájl minden éjfélkor rotálódik
```

## Metódusok

### `debug()`

Debug szintű üzenet logolása fájlba.

```python
def debug(self, message: str, **kwargs: object) -> None:
    """Debug szintű üzenet logolása.

    Args:
        message: A logolandó üzenet.
        **kwargs: További paraméterek (pl. extra adatok a loghoz).
    """
```

**Példa:**

```python
logger.debug("Hibakeresési információ", file="data.txt", line=42)
```

### `info()`

Info szintű üzenet logolása fájlba.

```python
def info(self, message: str, **kwargs: object) -> None:
    """Info szintű üzenet logolása.

    Args:
        message: A logolandó üzenet.
        **kwargs: További paraméterek (pl. extra adatok a loghoz).
    """
```

**Példa:**

```python
logger.info("Felhasználó bejelentkezett", user="admin", ip="192.168.1.1")
```

### `warning()`

Warning szintű üzenet logolása fájlba.

```python
def warning(self, message: str, **kwargs: object) -> None:
    """Warning szintű üzenet logolása.

    Args:
        message: A logolandó üzenet.
        **kwargs: További paraméterek (pl. extra adatok a loghoz).
    """
```

**Példa:**

```python
logger.warning("A cache majdnem tele van", usage=85, limit=90)
```

### `error()`

Error szintű üzenet logolása fájlba.

```python
def error(self, message: str, **kwargs: object) -> None:
    """Error szintű üzenet logolása.

    Args:
        message: A logolandó üzenet.
        **kwargs: További paraméterek (pl. extra adatok a loghoz).
    """
```

**Példa:**

```python
try:
    # Valami művelet
    pass
except Exception as e:
    logger.error("Művelet sikertelen", error=str(e), component="database")
```

### `critical()`

Critical szintű üzenet logolása fájlba.

```python
def critical(self, message: str, **kwargs: object) -> None:
    """Critical szintű üzenet logolása.

    Args:
        message: A logolandó üzenet.
        **kwargs: További paraméterek (pl. extra adatok a loghoz).
    """
```

**Példa:**

```python
logger.critical("A rendszer leállt", reason="Nincs elég memória", action="restart")
```

### `set_level()`

Logger log szintjének beállítása.

```python
def set_level(self, level: int) -> None:
    """Logger log szintjének beállítása.

    Args:
        level: Az új log szint (pl. logging.DEBUG, logging.INFO).
    """
```

**Példa:**

```python
import logging

logger = RotatingFileLogger("my_app", log_file="app.log")
logger.set_level(logging.DEBUG)
logger.debug("Ez az üzenet most már látható a fájlban")
```

### `get_level()`

Aktuális log szint lekérése.

```python
def get_level(self) -> int:
    """Aktuális log szint lekérése.

    Returns:
        Az aktuális log szint értéke.
    """
```

**Példa:**

```python
import logging

logger = RotatingFileLogger("my_app", log_file="app.log")
current_level = logger.get_level()

if current_level <= logging.DEBUG:
    print("Debug mód aktív")
```

### `clean_old_logs()`

Régi log fájlok eltávolítása.

```python
@staticmethod
def clean_old_logs(log_dir: str | Path) -> None:
    """Régi log fájlok eltávolítása.

    Figyelmeztetés: Ez a metódus véglegesen törli a log könyvtárat
    és annak teljes tartalmát!

    Args:
        log_dir: A log könyvtár útvonala.
    """
```

**Példa:**

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
from pathlib import Path

# Régi logok törlése
RotatingFileLogger.clean_old_logs(Path("logs/old_logs"))

# VIGYÁZAT: Ez véglegesen törli az összes fájlt a könyvtárból!
```

## Komplex példák

### Alkalmazás naplózása fájlba

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

class Application:
    def __init__(self):
        self.logger = RotatingFileLogger(
            name="MyApp",
            log_file="logs/application.log",
            max_bytes=10*1024*1024,  # 10MB
            backup_count=5,
            level=logging.DEBUG
        )
        
    def start(self):
        self.logger.info("Alkalmazás indítása...")
        
        try:
            self.logger.debug("Komponensek inicializálása")
            self._init_components()
            
            self.logger.info("Alkalmazás sikeresen elindult")
            
        except Exception as e:
            self.logger.critical(f"Indítási hiba: {e}")
            raise
    
    def _init_components(self):
        self.logger.debug("Adatbázis kapcsolat létrehozása")
        # ...
        self.logger.info("Komponensek inicializálva")
    
    def process_data(self, data):
        self.logger.debug(f"Adatfeldolgozás: {len(data)} elem")
        
        try:
            # Feldolgozás
            result = self._process(data)
            self.logger.info("Adatfeldolgozás sikeres")
            return result
            
        except Exception as e:
            self.logger.error(f"Feldolgozási hiba: {e}", data_size=len(data))
            raise
    
    def _process(self, data):
        # Feldolgozási logika
        pass

# Használat
app = Application()
app.start()
```

### Több logger használata

```python
from neural_ai.core.logger.implementations import (
    RotatingFileLogger,
    ColoredLogger
)
import logging

# Konzol logger (színes)
console_logger = ColoredLogger("ConsoleApp", level=logging.INFO)

# Fájl logger (részletes)
file_logger = RotatingFileLogger(
    name="FileApp",
    log_file="logs/detailed.log",
    max_bytes=5*1024*1024,
    backup_count=10,
    level=logging.DEBUG
)

# Különböző célokra különböző loggerek
console_logger.info("Felhasználói esemény")  # Csak konzolon
file_logger.debug("Részletes debug információ")  # Csak fájlban

# Mindkettőbe logolás
def log_both(message, level="info", **kwargs):
    getattr(console_logger, level)(message, **kwargs)
    getattr(file_logger, level)(message, **kwargs)

log_both("Fontos esemény", level="warning", reason="teszt")
```

### Időalapú rotáció

```python
from neural_ai.core.logger.implementations import RotatingFileLogger
import logging

# Heti rotáció
weekly_logger = RotatingFileLogger(
    name="WeeklyApp",
    log_file="logs/weekly.log",
    backup_count=52,  # 1 év
    rotation_type="time",
    when="W0",  # Minden hétfőn
    level=logging.INFO
)

# Óránkénti rotáció
hourly_logger = RotatingFileLogger(
    name="HourlyApp",
    log_file="logs/hourly.log",
    backup_count=168,  # 1 hét (24*7)
    rotation_type="time",
    when="H",
    level=logging.DEBUG
)

# Használat
weekly_logger.info("Heti jelentés")
hourly_logger.debug("Óránkénti statisztika")
```

## Fájl struktúra rotáció után

### Méret alapú rotáció

```
logs/
├── app.log          # Aktuális log fájl
├── app.log.1        # Legutóbbi backup
├── app.log.2        # Előző backup
├── app.log.3        # ...
└── app.log.5        # Legrégebbi backup
```

### Idő alapú rotáció

```
logs/
├── app.log          # Aktuális log fájl
├── app.log.2024-01-01  # Előző nap
├── app.log.2024-01-02  # ...
└── app.log.2024-01-30  # 30 napja
```

## Log formázási lehetőségek

```python
from neural_ai.core.logger.implementations import RotatingFileLogger

# Egyszerű formátum
simple_logger = RotatingFileLogger(
    name="SimpleApp",
    log_file="logs/simple.log",
    format_str="%(levelname)s: %(message)s"
)

# Részletes formátum
detailed_logger = RotatingFileLogger(
    name="DetailedApp",
    log_file="logs/detailed.log",
    format_str="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

# JSON-szerű formátum
json_logger = RotatingFileLogger(
    name="JsonApp",
    log_file="logs/json.log",
    format_str='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

## További információk

- [Logger Implementációk Áttekintés](__init__.md)
- [Logger Modul](../__init__.md)
- [Logger Factory](../factory.md)
- [Python logging.handlers dokumentáció](https://docs.python.org/3/library/logging.handlers.html)