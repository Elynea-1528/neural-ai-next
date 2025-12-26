# DefaultLogger - Alapértelmezett Logger Implementáció

## Áttekintés

Alapértelmezett logger implementáció a Python standard logging könyvtárával. Ez az osztály a Python standard library logging rendszerét használja, és implementálja a LoggerInterface-t. Konfigurálható log szinttel, formátummal és stream handlerrel.

## Osztály leírása

```python
class DefaultLogger:
    """Alapértelmezett logger implementáció a Python logging moduljával.

    Ez az osztály a Python standard library logging rendszerét használja,
    és implementálja a LoggerInterface-t. Konfigurálható log szinttel,
    formátummal és stream handlerrel.

    Attributes:
        logger: A belső Python logger objektum
    """
```

## Inicializálás

```python
def __init__(self, name: str, **kwargs: Any) -> None:
    """Logger inicializálása.

    A konstruktor létrehoz egy Python logger objektumot a megadott névvel,
    eltávolítja a korábbi handlereket (ha voltak), és beállítja a log szintet,
    formátumot és stream handlert a kapott paraméterek alapján.

    Args:
        name: A logger egyedi neve. Ez a név jelenik meg a log üzenetekben.
        **kwargs: Opcionális kulcsszó argumentumok:
            - level (int): Log szint (pl. logging.DEBUG, logging.INFO).
              Alapértelmezett: logging.INFO.
            - format (str): Log formátum string. Alapértelmezett:
              "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            - stream: Kimeneti stream. Alapértelmezett: sys.stderr.
    """
```

## Paraméterek

- `name` (str): A logger egyedi neve
- `level` (int, opcionális): Log szint, alapértelmezett: `logging.INFO`
- `format` (str, opcionális): Log formátum string
- `stream` (opcionális): Kimeneti stream, alapértelmezett: `sys.stderr`

## Alap használat

```python
from neural_ai.core.logger.implementations import DefaultLogger

# Egyszerű inicializálás
logger = DefaultLogger("my_app")

# Log üzenetek
logger.info("Alkalmazás elindult")
logger.warning("Figyelmeztetés")
logger.error("Hiba történt")
```

## Speciális konfiguráció

```python
from neural_ai.core.logger.implementations import DefaultLogger
import logging
import sys

# Egyéni konfigurációval
logger = DefaultLogger(
    name="my_app",
    level=logging.DEBUG,  # DEBUG szint beállítása
    format="%(levelname)s: %(message)s",  # Egyszerű formátum
    stream=sys.stdout  # stdout-ra írás
)

# Használat
logger.debug("Hibakeresési információ")
logger.info("Sikeres művelet")
```

## Metódusok

### `debug()`

Debug szintű üzenet logolása.

```python
def debug(self, message: str, **kwargs: Any) -> None:
    """Debug szintű üzenet logolása.

    Args:
        message: A log üzenet szövege.
        **kwargs: További paraméterek, amelyek az extra kulcs alatt
            kerülnek átadásra a loggernek.

    Példa:
        >>> logger.debug("Hibakeresési üzenet", user_id=123)
    """
```

**Példa:**

```python
logger.debug("Adatfeldolgozás elkezdődött", file="data.txt", line=42)
```

### `info()`

Info szintű üzenet logolása.

```python
def info(self, message: str, **kwargs: Any) -> None:
    """Info szintű üzenet logolása.

    Args:
        message: A log üzenet szövege.
        **kwargs: További paraméterek, amelyek az extra kulcs alatt
            kerülnek átadásra a loggernek.

    Példa:
        >>> logger.info("Sikeres művelet", duration=0.5)
    """
```

**Példa:**

```python
logger.info("Felhasználó bejelentkezett", user="admin", ip="192.168.1.1")
```

### `warning()`

Warning szintű üzenet logolása.

```python
def warning(self, message: str, **kwargs: Any) -> None:
    """Warning szintű üzenet logolása.

    Args:
        message: A log üzenet szövege.
        **kwargs: További paraméterek, amelyek az extra kulcs alatt
            kerülnek átadásra a loggernek.

    Példa:
        >>> logger.warning("Elavult API hívás", version="1.0")
    """
```

**Példa:**

```python
logger.warning("A cache majdnem tele van", usage=85, limit=90)
```

### `error()`

Error szintű üzenet logolása.

```python
def error(self, message: str, **kwargs: Any) -> None:
    """Error szintű üzenet logolása.

    Args:
        message: A log üzenet szövege.
        **kwargs: További paraméterek, amelyek az extra kulcs alatt
            kerülnek átadásra a loggernek.

    Példa:
        >>> logger.error("Adatbázis kapcsolódási hiba", db="main")
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

Critical szintű üzenet logolása.

```python
def critical(self, message: str, **kwargs: Any) -> None:
    """Critical szintű üzenet logolása.

    Args:
        message: A log üzenet szövege.
        **kwargs: További paraméterek, amelyek az extra kulcs alatt
            kerülnek átadásra a loggernek.

    Példa:
        >>> logger.critical("Kritikus rendszerhiba", component="auth")
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

    A metódus beállítja a logger és a hozzá tartozó handler minimális
    log szintjét. Ez határozza meg, hogy melyik szintű üzenetek kerüljenek
    naplózásra.

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

# Alapértelmezett INFO szint
logger = DefaultLogger("my_app")

# DEBUG szintre váltás
logger.set_level(logging.DEBUG)
logger.debug("Ez az üzenet most már látható")

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
        int: Az aktuális log szint numerikus értéke. A visszaadott érték
            a logging modul konstansainak egyike (pl. logging.INFO -> 20).

    Példa:
        >>> level = logger.get_level()
        >>> print(f"Aktuális log szint: {level}")
    """
```

**Példa:**

```python
import logging

logger = DefaultLogger("my_app")
current_level = logger.get_level()

if current_level <= logging.DEBUG:
    print("Debug mód aktív")
elif current_level == logging.INFO:
    print("Info mód aktív")
```

## Komplex példák

### Alkalmazás indítása és leállítása

```python
from neural_ai.core.logger.implementations import DefaultLogger
import logging

class Application:
    def __init__(self):
        self.logger = DefaultLogger("MyApplication", level=logging.DEBUG)
        
    def start(self):
        self.logger.info("Alkalmazás indítása...")
        
        try:
            # Inicializálás
            self.logger.debug("Komponensek inicializálása")
            self._init_components()
            
            self.logger.info("Alkalmazás sikeresen elindult")
            
        except Exception as e:
            self.logger.critical(f"Indítási hiba: {e}")
            raise
    
    def _init_components(self):
        # Komponens inicializálás
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
from neural_ai.core.logger.implementations import DefaultLogger
import logging

# Különböző komponensekhez külön loggerek
main_logger = DefaultLogger("MainApp", level=logging.INFO)
db_logger = DefaultLogger("Database", level=logging.DEBUG)
api_logger = DefaultLogger("API", level=logging.WARNING)

# Használat
main_logger.info("Alkalmazás elindult")

try:
    db_logger.debug("Adatbázis lekérdezés indítása")
    # DB művelet
    db_logger.info("Lekérdezés sikeres")
    
    api_logger.info("API hívás")
    # API művelet
    api_logger.warning("API válasz késleltetve")
    
except Exception as e:
    main_logger.error(f"Hiba történt: {e}")
    db_logger.error(f"Adatbázis hiba: {e}")
```

### Dinamikus log szint változtatás

```python
from neural_ai.core.logger.implementations import DefaultLogger
import logging

logger = DefaultLogger("DynamicApp")

# Alapértelmezett INFO szint
logger.info("Alkalmazás elindult")

# DEBUG mód bekapcsolása
logger.set_level(logging.DEBUG)
logger.debug("Részletes debug információ")

# Vissza INFO szintre
logger.set_level(logging.INFO)
logger.debug("Ez már nem jelenik meg")

# CRITICAL szintre váltás
logger.set_level(logging.CRITICAL)
logger.warning("Ez a figyelmeztetés sem jelenik meg")
logger.critical("Csak kritikus hibák jelennek meg")
```

## Formázási lehetőségek

### Alap formázók

```python
from neural_ai.core.logger.implementations import DefaultLogger

# Egyszerű formátum
simple_logger = DefaultLogger(
    "SimpleApp",
    format="%(levelname)s: %(message)s"
)

# Részletes formátum
detailed_logger = DefaultLogger(
    "DetailedApp",
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)

# JSON-szerű formátum
json_logger = DefaultLogger(
    "JsonApp",
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
```

## További információk

- [Logger Implementációk Áttekintés](__init__.md)
- [Logger Modul](../__init__.md)
- [Logger Factory](../factory.md)
- [Python logging dokumentáció](https://docs.python.org/3/library/logging.html)