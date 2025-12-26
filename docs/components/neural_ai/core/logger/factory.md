# LoggerFactory - Logger Gyár Osztály

## Áttekintés

Logger factory implementáció, amely biztosítja a `LoggerFactory` osztályt, felelős a különböző típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

## Támogatott logger típusok

- `default`: Alapértelmezett konzol logger
- `colored`: Színes kimenetű konzol logger
- `rotating`: Fájlba író, automatikusan rotáló logger

## Osztály leírása

```python
class LoggerFactory(LoggerFactoryInterface):
    """Factory osztály loggerek létrehozásához.
    
    A factory mintát követve centralizálja a logger példányosítást és
    életciklus kezelést. Támogatja a különböző logger implementációk
    regisztrálását és lekérdezését.
    """
```

## Metódusok

### `register_logger()`

Új logger típus regisztrálása.

```python
@classmethod
def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
    """Új logger típus regisztrálása.

    Args:
        logger_type: A logger típus neve.
        logger_class: A logger osztály.

    Raises:
        TypeError: Ha a logger_class nem implementálja a LoggerInterface-t.
    """
```

**Paraméterek:**
- `logger_type` (str): A logger típus neve
- `logger_class` (type[LoggerInterface]): A logger osztály

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory, LoggerInterface

class CustomLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        # Egyéni implementáció
        pass
    # ... egyéb metódusok

# Egyéni logger regisztrálása
LoggerFactory.register_logger("custom", CustomLogger)
```

### `get_logger()`

Logger példány létrehozása vagy visszaadása.

```python
@classmethod
def get_logger(
    cls,
    name: str,
    logger_type: str = "default",
    **kwargs: Any,
) -> LoggerInterface:
    """Logger példány létrehozása vagy visszaadása.

    Args:
        name: A logger egyedi neve.
        logger_type: A kért logger típus ('default', 'colored', 'rotating').
        **kwargs: További paraméterek a loggernek (pl. log_file, level).

    Returns:
        LoggerInterface: Az inicializált logger példány.

    Raises:
        ValueError: Ha a 'rotating' típushoz nincs megadva 'log_file'.
        TypeError: Ha a létrehozott logger nem implementálja az interfészt.
    """
```

**Paraméterek:**
- `name` (str): A logger egyedi neve
- `logger_type` (str): A kért logger típus (alapértelmezett: "default")
- `**kwargs`: További paraméterek

**Visszatérési érték:**
- `LoggerInterface`: Az inicializált logger példány

**Példák:**

```python
from neural_ai.core.logger import LoggerFactory
import logging

# Alapértelmezett logger
logger = LoggerFactory.get_logger("my_app")

# Színes logger
colored_logger = LoggerFactory.get_logger("my_app", logger_type="colored")

# Fájl logger
file_logger = LoggerFactory.get_logger(
    "file_app",
    logger_type="rotating",
    log_file="/var/log/app.log",
    level=logging.DEBUG
)

# Ugyanazt a loggert többször is lekérhetjük
same_logger = LoggerFactory.get_logger("my_app")  # Visszaadja a meglévőt
```

### `configure()`

Logger rendszer konfigurálása.

```python
@classmethod
def configure(cls, config: dict[str, Any]) -> None:
    """Logger rendszer konfigurálása.

    Args:
        config: Konfigurációs dict a következő struktúrával:
            {
                'default_level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'date_format': '%Y-%m-%d %H:%M:%S',
                'handlers': {
                    'console': {
                        'enabled': True,
                        'level': 'INFO'
                    },
                    'file': {
                        'enabled': True,
                        'filename': 'app.log',
                        'level': 'DEBUG'
                    }
                }
            }
    """
```

**Konfigurációs struktúra:**

```python
config = {
    'default_level': 'INFO',  # Alapértelmezett log szint
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log formátum
    'date_format': '%Y-%m-%d %H:%M:%S',  # Dátum formátum
    'handlers': {
        'console': {  # Konzol handler
            'enabled': True,
            'level': 'INFO'
        },
        'file': {  # Fájl handler
            'enabled': True,
            'filename': 'app.log',
            'level': 'DEBUG'
        }
    }
}
```

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory

config = {
    'default_level': 'DEBUG',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'handlers': {
        'console': {
            'enabled': True,
            'level': 'INFO'
        },
        'file': {
            'enabled': True,
            'filename': 'application.log',
            'level': 'DEBUG'
        }
    }
}

LoggerFactory.configure(config)
```

### `get_schema_version()`

A logger factory sémaváltozatának lekérdezése.

```python
@classmethod
def get_schema_version(cls) -> str:
    """A logger factory sémaváltozatának lekérdezése.

    Returns:
        str: A sémaváltozat string formátumban (pl. '1.0.0').
    """
```

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory

version = LoggerFactory.get_schema_version()
print(f"Séma verzió: {version}")
```

### `set_schema_version()`

A logger factory sémaváltozatának beállítása.

```python
@classmethod
def set_schema_version(cls, version: str) -> None:
    """A logger factory sémaváltozatának beállítása.

    Args:
        version: Az új sémaváltozat (pl. '1.1.0').
    """
```

### `clear_instances()`

Összes logger példány törlése a gyorsítótárból.

```python
@classmethod
def clear_instances(cls) -> None:
    """Összes logger példány törlése a gyorsítótárból.

    Ez a metódus hasznos teszteléskor vagy amikor teljesen
    új logger példányokat szeretnénk létrehozni.
    """
```

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory

# Logger létrehozása
logger1 = LoggerFactory.get_logger("app")

# Példányok törlése
LoggerFactory.clear_instances()

# Új logger létrehozása (most már új példány jön létre)
logger2 = LoggerFactory.get_logger("app")
```

### `get_registered_types()`

Regisztrált logger típusok listázása.

```python
@classmethod
def get_registered_types(cls) -> list[str]:
    """Regisztrált logger típusok listázása.

    Returns:
        list[str]: A regisztrált logger típusok neveinek listája.
    """
```

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory

types = LoggerFactory.get_registered_types()
print(f"Regisztrált típusok: {types}")
# Output: ['default', 'colored', 'rotating']
```

### `is_logger_registered()`

Ellenőrzi, hogy egy logger típus regisztrálva van-e.

```python
@classmethod
def is_logger_registered(cls, logger_type: str) -> bool:
    """Ellenőrzi, hogy egy logger típus regisztrálva van-e.

    Args:
        logger_type: A logger típus neve.

    Returns:
        bool: True, ha a logger típus regisztrálva van, egyébként False.
    """
```

**Példa:**

```python
from neural_ai.core.logger import LoggerFactory

if LoggerFactory.is_logger_registered("colored"):
    print("A színes logger regisztrálva van")
```

## Komplex példa

```python
import logging
from neural_ai.core.logger import LoggerFactory

# 1. Rendszer konfigurálása
config = {
    'default_level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'handlers': {
        'console': {
            'enabled': True,
            'level': 'INFO'
        }
    }
}
LoggerFactory.configure(config)

# 2. Különböző típusú loggerek létrehozása
console_logger = LoggerFactory.get_logger("console_app")
colored_logger = LoggerFactory.get_logger("colored_app", logger_type="colored")
file_logger = LoggerFactory.get_logger(
    "file_app",
    logger_type="rotating",
    log_file="app.log",
    max_bytes=10*1024*1024,
    backup_count=5
)

# 3. Loggerek használata
console_logger.info("Konzol log üzenet")
colored_logger.warning("Színes figyelmeztetés")
file_logger.debug("Részletes debug információ a fájlba")

# 4. Információk lekérdezése
print(f"Regisztrált típusok: {LoggerFactory.get_registered_types()}")
print(f"Séma verzió: {LoggerFactory.get_schema_version()}")

# 5. Ellenőrzés
if LoggerFactory.is_logger_registered("custom"):
    print("Custom logger elérhető")
```

## Singleton viselkedés

A factory biztosítja, hogy minden egyedi névhez csak egy logger példány jöjjön létre:

```python
logger1 = LoggerFactory.get_logger("my_app")
logger2 = LoggerFactory.get_logger("my_app")

print(logger1 is logger2)  # True - ugyanaz a példány
```

## További információk

- [Logger Modul Áttekintés](__init__.md)
- [Logger Implementációk](implementations/__init__.md)
- [Logger Interfészek](interfaces/__init__.md)