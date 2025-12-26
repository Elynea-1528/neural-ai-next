# Logger Formázók

## Áttekintés

Ez a modul tartalmazza a különböző logger formázókat, amelyek a log üzenetek megjelenítését vezérlik (pl. színes kimenet).

## Osztályok

### `ColoredFormatter`

Színes megjelenítést biztosító formatter.

```python
class ColoredFormatter(logging.Formatter):
    """Színes megjelenítést biztosító formatter.

    Különböző színekkel jelöli a különböző log szinteket:
    - DEBUG: Kék
    - INFO: Zöld
    - WARNING: Sárga
    - ERROR: Piros
    - CRITICAL: Piros (háttér)
    """
```

#### Attribútumok

**Osztályszintű konstansok:**

```python
COLORS: dict[int, str] = {
    logging.DEBUG: "\033[94m",      # Kék
    logging.INFO: "\033[92m",       # Zöld
    logging.WARNING: "\033[93m",    # Sárga
    logging.ERROR: "\033[91m",      # Piros
    logging.CRITICAL: "\033[97;41m", # Fehér szöveg piros háttéren
}
RESET: str = "\033[0m"
```

#### Metódusok

##### `format()`

Log rekord formázása színes kimenettel.

```python
def format(self, record: logging.LogRecord) -> str:
    """Log rekord formázása színes kimenettel.

    Args:
        record: A formázandó log rekord

    Returns:
        str: A színes formázott log üzenet
    """
```

## Használat

### Közvetlen használat

```python
import logging
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

# Handler létrehozása
handler = logging.StreamHandler()

# ColoredFormatter alkalmazása
formatter = ColoredFormatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Logger létrehozása
logger = logging.getLogger("my_app")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Különböző szintű üzenetek
logger.debug("Debug üzenet")      # Kék színnel
logger.info("Info üzenet")        # Zöld színnel
logger.warning("Figyelmeztetés")  # Sárga színnel
logger.error("Hiba")              # Piros színnel
logger.critical("Kritikus hiba")  # Fehér szöveg piros háttéren
```

### ColoredLogger-rel együtt

```python
from neural_ai.core.logger import ColoredLogger
import logging

# ColoredLogger automatikusan használja a ColoredFormatter-t
logger = ColoredLogger(
    name="my_app",
    level=logging.DEBUG,
    format_str="%(asctime)s - %(levelname)s - %(message)s"
)

# Üzenetek színesen jelennek meg
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés")
logger.error("Hiba történt")
```

### Egyéni formázás

```python
import logging
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

# Egyéni formátum
custom_formatter = ColoredFormatter(
    fmt='[%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)

# Handler beállítása
handler = logging.StreamHandler()
handler.setFormatter(custom_formatter)

# Logger konfigurálása
logger = logging.getLogger("custom_app")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Használat
logger.info("Egyéni formázású üzenet")
```

## Színkódok

A ColoredFormatter ANSI színkódokat használ:

| Log Szint | ANSI Kód | Szín |
|-----------|----------|------|
| DEBUG | `\033[94m` | Kék |
| INFO | `\033[92m` | Zöld |
| WARNING | `\033[93m` | Sárga |
| ERROR | `\033[91m` | Piros |
| CRITICAL | `\033[97;41m` | Fehér szöveg piros háttéren |
| RESET | `\033[0m` | Szín visszaállítása |

## Komplex példa

```python
import logging
import sys
from neural_ai.core.logger.formatters.logger_formatters import ColoredFormatter

class CustomColoredFormatter(ColoredFormatter):
    """Egyéni színes formázó."""
    
    # Egyéni színek
    COLORS = {
        logging.DEBUG: "\033[36m",      # Cián
        logging.INFO: "\033[32m",       # Zöld
        logging.WARNING: "\033[33m",    # Sárga
        logging.ERROR: "\033[31m",      # Piros
        logging.CRITICAL: "\033[30;41m", # Fekete szöveg piros háttéren
    }
    
    def format(self, record):
        """Egyéni formázás."""
        # Alap formázás
        message = super().format(record)
        
        # Egyéni logika
        if record.levelno >= logging.ERROR:
            # Hiba esetén hozzáadunk egy csillagot
            message = f"⚠️  {message}"
        
        return message

# Handler létrehozása
handler = logging.StreamHandler(sys.stdout)

# Egyéni formázó alkalmazása
formatter = CustomColoredFormatter(
    fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Logger beállítása
logger = logging.getLogger("custom_app")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Tesztelés
logger.debug("Debug üzenet")
logger.info("Info üzenet")
logger.warning("Figyelmeztető üzenet")
logger.error("Hibaüzenet")      # ⚠️  jellel jelenik meg
logger.critical("Kritikus hiba") # ⚠️  jellel jelenik meg
```

## Támogatott terminálok

A ColoredFormatter ANSI színkódokat használ, amelyek a legtöbb modern terminálban támogatottak:

- **Linux/macOS**: Alapértelmezett terminálok (GNOME Terminal, Konsole, Terminal.app, stb.)
- **Windows**: Windows Terminal, PowerShell, Git Bash
- **IDE-k**: VS Code, PyCharm, Jupyter Notebook

**Megjegyzés:** Elavult Windows konzolban (cmd.exe) a színes kimenet nem fog megjelenni.

## Formázási lehetőségek

A ColoredFormatter a standard logging formázási opciókat támogatja:

### Alap formázók

- `%(asctime)s`: Időbélyeg
- `%(name)s`: Logger neve
- `%(levelname)s`: Log szint neve
- `%(message)s`: Az üzenet szövege
- `%(filename)s`: Fájl neve
- `%(lineno)d`: Sor szám
- `%(funcName)s`: Függvény neve
- `%(process)d`: Process ID
- `%(thread)d`: Thread ID

### Példa formátumok

```python
# Egyszerű formátum
simple_format = "%(levelname)s: %(message)s"

# Részletes formátum
detailed_format = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"

# JSON formátum
json_like_format = '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
```

## További információk

- [Logger Modul Áttekintés](../__init__.md)
- [ColoredLogger Implementáció](../implementations/colored_logger.md)
- [Python logging dokumentáció](https://docs.python.org/3/library/logging.html)