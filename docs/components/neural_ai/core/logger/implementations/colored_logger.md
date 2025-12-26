# ColoredLogger - Színes Konzol Logger

## Áttekintés

Színes konzol logger implementáció. Ez az osztály a LoggerInterface-t implementálja, és színes formázást alkalmaz a log üzenetekhez a konzolon. A színek a log szinttől függenek, ami segít a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

## Osztály leírása

```python
class ColoredLogger(LoggerInterface):
    """Színes konzol kimenettel rendelkező logger implementáció.

    Ez az osztály a LoggerInterface-t implementálja, és színes formázást alkalmaz
    a log üzenetekhez a konzolon. A színek a log szinttől függenek, ami segít
    a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

    Attributes:
        logger: A belső Python logger objektum
    """
```

## Inicializálás

```python
def __init__(
    self,
    name: str,
    level: int = logging.INFO,
    format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream: IO[str] = sys.stdout,
    **kwargs: Any,
) -> None:
    """Logger inicializálása színes konzol kimenettel.

    Args:
        name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
        level: A log szint (pl. logging.DEBUG, logging.INFO). Alapértelmezett
            értéke a logging.INFO.
        format_str: A log üzenetek formátuma. Alapértelmezett formátum:
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        stream: A kimeneti stream, ahova a logok íródnak. Alapértelmezett
            értéke a sys.stdout.
        **kwargs: További opcionális paraméterek, amelyeket a jövőbeli
            bővíthetőség érdekében elfogad az osztály.
    """
```

## Paraméterek

- `name` (str): A logger egyedi neve
- `level` (int, opcionális): Log szint, alapértelmezett: `logging.INFO`
- `format_str` (str, opcionális): Log formátum string
- `stream` (IO[str], opcionális): Kimeneti stream, alapértelmezett: `sys.stdout`
- `**kwargs`: További opcionális paraméterek

## Alap használat

```python
from neural_ai.core.logger.implementations import ColoredLogger
import logging

# Egyszerű inicializálás
logger = ColoredLogger("my_app")

# Log üzenetek (színesen jelennek meg)
logger.info("Alkalmazás elindult")      # Zöld
logger.warning("Figyelmeztetés")        # Sárga
logger.error("Hiba történt")            # Piros
logger.critical("Kritikus hiba")        # Fehér piros háttéren
```

## Speciális konfiguráció

```python
from neural_ai.core.logger.implementations import ColoredLogger
import logging
import sys

# Egyéni konfigurációval
logger = ColoredLogger(
    name="my_app",
    level=logging.DEBUG,  # DEBUG szint beállítása
    format_str="%(levelname)s: %(message)s",  # Egyszerű formátum
    stream=sys.stdout  # stdout-ra írás
)

# Használat
logger.debug("Hibakeresési információ")   # Kék
logger.info("Sikeres művelet")            # Zöld
logger.warning("Figyelmeztető üzenet")    # Sárga
```

## Színek

A ColoredLogger a következő színeket használja a log szintekhez:

| Log Szint | Szín | ANSI Kód | Leírás |
|-----------|------|----------|--------|
| DEBUG | Kék | `\033[94m` | Részletes hibakeresési információk |
| INFO | Zöld | `\033[92m` | Általános információk |
| WARNING | Sárga | `\033[93m` | Figyelmeztető üzenetek |
| ERROR | Piros | `\033[91m` | Hibák |
| CRITICAL | Fehér/Piros háttér | `\033[97;41m` | Kritikus hibák |

## Metódusok

### `debug()`

Debug szintű üzenet logolása (kék színnel).

```python
def debug(self, message: str, **kwargs: Any) -> None:
    """Debug szintű üzenet logolása.

    Ez a metódus részletes hibakeresési információkat logol, amelyek általában
    csak fejlesztés közben hasznosak.

    Args:
        message: A logolandó debug üzenet.
        **kwargs: További paraméterek, amelyek az extra adatokhoz adhatók
            a log rekordban.

    Példa:
        >>> logger.debug("Adatfeldolgozás elkezdődött", file="data.txt")
    """
```

**Példa:**

```python
logger.debug("Adatfeldolgozás elkezdődött", file="data.txt", line=42)
# Output: [KÉK] 2024-01-01 10:00:00 - my_app - DEBUG - Adatfeldolgozás elkezdődött
```

### `info()`

Info szintű üzenet logolása (zöld színnel).

```python
def info(self, message: str, **kwargs: Any) -> None:
    """Info szintű üzenet logolása.

    Ez a metódus általános információkat logol az alkalmazás működéséről.

    Args:
        message: A logolandó info üzenet.
        **kwargs: További paraméterek az extra adatokhoz.

    Példa:
        >>> logger.info("Sikeres bejelentkezés", user="admin")
    """
```

**Példa:**

```python
logger.info("Felhasználó bejelentkezett", user="admin", ip="192.168.1.1")
# Output: [ZÖLD] 2024-01-01 10:00:00 - my_app - INFO - Felhasználó bejelentkezett
```

### `warning()`

Warning szintű üzenet logolása (sárga színnel).

```python
def warning(self, message: str, **kwargs: Any) -> None:
    """Warning szintű üzenet logolása.

    Ez a metódus figyelmeztető üzeneteket logol, amelyek nem kritikusak,
    de érdemes rájuk figyelni.

    Args:
        message: A logolandó warning üzenet.
        **kwargs: További paraméterek az extra adatokhoz.

    Példa:
        >>> logger.warning("A cache majdnem tele van", usage=85)
    """
```

**Példa:**

```python
logger.warning("A cache majdnem tele van", usage=85, limit=90)
# Output: [SÁRGA] 2024-01-01 10:00:00 - my_app - WARNING - A cache majdnem tele van
```

### `error()`

Error szintű üzenet logolása (piros színnel).

```python
def error(self, message: str, **kwargs: Any) -> None:
    """Error szintű üzenet logolása.

    Ez a metódus hibákat logol, amelyek befolyásolják az alkalmazás
    működését, de nem okoznak leállást.

    Args:
        message: A logolandó error üzenet.
        **kwargs: További paraméterek az extra adatokhoz.

    Példa:
        >>> logger.error("Adatbázis kapcsolódási hiba", error=str(e))
    """
```

**Példa:**

```python
try:
    # Valami művelet
    pass
except Exception as e:
    logger.error("Művelet sikertelen", error=str(e), component="database")
# Output: [PIROS] 2024-01-01 10:00:00 - my_app - ERROR - Művelet sikertelen
```

### `critical()`

Critical szintű üzenet logolása (fehér szöveg piros háttéren).

```python
def critical(self, message: str, **kwargs: Any) -> None:
    """Critical szintű üzenet logolása.

    Ez a metódus kritikus hibákat logol, amelyek az alkalmazás leállását
    okozhatják vagy jelentős problémát jeleznek.

    Args:
        message: A logolandó critical üzenet.
        **kwargs: További paraméterek az extra adatokhoz.

    Példa:
        >>> logger.critical("A rendszer leállt", reason="Nincs elég memória")
    """
```

**Példa:**

```python
logger.critical("A rendszer leállt", reason="Nincs elég memória", action="restart")
# Output: [FEHÉR PIROS HÁTTÉREN] 2024-01-01 10:00:00 - my_app - CRITICAL - A rendszer leállt
```

### `set_level()`

Logger log szintjének beállítása.

```python
def set_level(self, level: int) -> None:
    """Logger log szintjének beállítása.

    Ez a metódus lehetővé teszi a log szint dinamikus módosítását futás közben.

    Args:
        level: Az új log szint (pl. logging.DEBUG, logging.INFO,
            logging.WARNING, logging.ERROR, logging.CRITICAL).

    Példa:
        >>> logger.set_level(logging.DEBUG)
    """
```

**Példa:**

```python
import logging

logger = ColoredLogger("my_app")

# DEBUG mód bekapcsolása
logger.set_level(logging.DEBUG)
logger.debug("Ez az üzenet most már látható kék színnel")

# Vissza INFO szintre
logger.set_level(logging.INFO)
logger.debug("Ez az üzenet már nem látható")
```

### `get_level()`

Aktuális log szint lekérése.

```python
def get_level(self) -> int:
    """Aktuális log szint lekérése.

    Returns:
        int: Az aktuális log szint numerikus értéke.

    Példa:
        >>> current_level = logger.get_level()
        >>> print(f"Aktuális log szint: {current_level}")
    """
```

**Példa:**

```python
import logging

logger = ColoredLogger("my_app")
current_level = logger.get_level()

if current_level <= logging.DEBUG:
    print("Debug mód aktív")
elif current_level == logging.INFO:
    print("Info mód aktív")
```

## Komplex példák

### Alkalmazás naplózása

```python
from neural_ai.core.logger.implementations import ColoredLogger
import logging

class Application:
    def __init__(self):
        self.logger = ColoredLogger("MyApp", level=logging.DEBUG)
        
    def start(self):
        self.logger.info("Alkalmazás indítása...")  # Zöld
        
        try:
            self.logger.debug("Komponensek inicializálása")  # Kék
            self._init_components()
            
            self.logger.info("Alkalmazás sikeresen elindult")  # Zöld
            
        except Exception as e:
            self.logger.critical(f"Indítási hiba: {e}")  # Piros háttér
            raise
    
    def _init_components(self):
        self.logger.debug("Adatbázis kapcsolat")  # Kék
        # ...
        self.logger.info("Komponensek inicializálva")  # Zöld
    
    def process_request(self, request):
        self.logger.debug(f"Kérés feldolgozása: {request}")  # Kék
        
        try:
            # Feldolgozás
            result = self._process(request)
            self.logger.info("Kérés sikeresen feldolgozva")  # Zöld
            return result
            
        except ValueError as e:
            self.logger.warning(f"Érvénytelen kérés: {e}")  # Sárga
            return None
            
        except Exception as e:
            self.logger.error(f"Feldolgozási hiba: {e}")  # Piros
            raise
    
    def _process(self, request):
        # Feldolgozási logika
        pass

# Használat
app = Application()
app.start()
result = app.process_request({"data": "test"})
```

### Több szálú alkalmazás

```python
import threading
import time
from neural_ai.core.logger.implementations import ColoredLogger
import logging

class WorkerThread(threading.Thread):
    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id
        self.logger = ColoredLogger(f"Worker-{thread_id}", level=logging.DEBUG)
        
    def run(self):
        self.logger.info(f"Szál elindult: {self.thread_id}")  # Zöld
        
        for i in range(5):
            self.logger.debug(f"Feldolgozás {i+1}/5")  # Kék
            time.sleep(1)
            
            if i == 3:
                self.logger.warning(f"Félúton: {self.thread_id}")  # Sárga
        
        self.logger.info(f"Szál befejezte: {self.thread_id}")  # Zöld

# Több szál futtatása
threads = []
for i in range(3):
    worker = WorkerThread(i)
    threads.append(worker)
    worker.start()

for worker in threads:
    worker.join()

print("Minden szál befejezte a munkát")
```

### Dinamikus log szint változtatás

```python
from neural_ai.core.logger.implementations import ColoredLogger
import logging

logger = ColoredLogger("DynamicApp")

# Alapértelmezett INFO szint
logger.info("Alkalmazás elindult")  # Zöld

# DEBUG mód bekapcsolása
logger.set_level(logging.DEBUG)
logger.debug("Részletes debug információ")  # Kék
logger.info("Sikeres művelet")  # Zöld

# WARNING szintre váltás
logger.set_level(logging.WARNING)
logger.info("Ez az info már nem látható")  # Nem jelenik meg
logger.warning("Figyelmeztetés látható")  # Sárga

# CRITICAL szintre váltás
logger.set_level(logging.CRITICAL)
logger.warning("Ez a figyelmeztetés sem látható")  # Nem jelenik meg
logger.critical("Csak kritikus hibák láthatók")  # Fehér piros háttéren
```

## Támogatott terminálok

A ColoredLogger ANSI színkódokat használ, amelyek a legtöbb modern terminálban támogatottak:

- **Linux/macOS**: GNOME Terminal, Konsole, Terminal.app, stb.
- **Windows**: Windows Terminal, PowerShell, Git Bash
- **IDE-k**: VS Code, PyCharm, Jupyter Notebook

**Megjegyzés:** Elavult Windows konzolban (cmd.exe) a színes kimenet nem fog megjelenni.

## Formázási lehetőségek

```python
from neural_ai.core.logger.implementations import ColoredLogger

# Egyszerű formátum
simple_logger = ColoredLogger(
    "SimpleApp",
    format_str="%(levelname)s: %(message)s"
)

# Részletes formátum
detailed_logger = ColoredLogger(
    "DetailedApp",
    format_str="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

# Időalapú formátum
time_logger = ColoredLogger(
    "TimeApp",
    format_str="%(asctime)s | %(levelname)s | %(message)s"
)
```

## További információk

- [Logger Implementációk Áttekintés](__init__.md)
- [ColoredFormatter](../formatters/logger_formatters.md)
- [Logger Modul](../__init__.md)
- [Logger Factory](../factory.md)