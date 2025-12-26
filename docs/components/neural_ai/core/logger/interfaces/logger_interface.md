# LoggerInterface - Logger Interfész

## Áttekintés

Logger interfész a naplózási műveletek absztrakt definíciójához. Ez az interfész definiálja azokat a metódusokat, amelyeket minden logger implementációnak implementálnia kell a konzisztens naplózási viselkedés érdekében.

## Interfész leírása

```python
class LoggerInterface(ABC):
    """Logger interfész a naplózási műveletek absztrakt definíciójához.

    Ez az interfész definiálja azokat a metódusokat, amelyeket minden logger
    implementációnak implementálnia kell a konzisztens naplózási viselkedés
    érdekében.
    """
```

## Absztrakt metódusok

### `__init__()`

Logger inicializálása.

```python
@abstractmethod
def __init__(
    self,
    name: str,
    config: Optional["ConfigManagerInterface"] = None,
    **kwargs: Mapping[str, AnyStr],
) -> None:
    """Logger inicializálása.

    Args:
        name: A logger egyedi azonosítója.
        config: Opcionális konfigurációs interfész a logger beállításaihoz.
        **kwargs: További opcionális paraméterek (pl. file_path, level).
    """
```

**Paraméterek:**
- `name` (str): A logger egyedi azonosítója
- `config` (Optional[ConfigManagerInterface]): Opcionális konfigurációs interfész
- `**kwargs` (Mapping[str, AnyStr]): További opcionális paraméterek

### `debug()`

Debug szintű üzenet naplózása.

```python
@abstractmethod
def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
    """Debug szintű üzenet naplózása.

    Részletes hibakeresési információk naplózására szolgál, amelyek általában
    csak fejlesztés közben relevánsak.

    Args:
        message: A naplózandó üzenet szövege.
        **kwargs: További kontextusparaméterek (pl. extra, exc_info).
    """
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

### `info()`

Információs szintű üzenet naplózása.

```python
@abstractmethod
def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
    """Információs szintű üzenet naplózása.

    Általános információk naplózására szolgál, amelyek a rendszer normál
    működéséről adnak tájékoztatást.

    Args:
        message: A naplózandó üzenet szövege.
        **kwargs: További kontextusparaméterek (pl. extra, exc_info).
    """
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

### `warning()`

Figyelmeztető szintű üzenet naplózása.

```python
@abstractmethod
def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
    """Figyelmeztető szintű üzenet naplózása.

    Olyan helyzetek naplózására szolgál, amelyek nem kritikusak, de
    figyelmet igényelnek.

    Args:
        message: A naplózandó üzenet szövege.
        **kwargs: További kontextusparaméterek (pl. extra, exc_info).
    """
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

### `error()`

Hiba szintű üzenet naplózása.

```python
@abstractmethod
def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
    """Hiba szintű üzenet naplózása.

    Hibák naplózására szolgál, amelyek befolyásolják a rendszer működését,
    de nem okoznak alkalmazásleállást.

    Args:
        message: A naplózandó üzenet szövege.
        **kwargs: További kontextusparaméterek (pl. extra, exc_info).
    """
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

### `critical()`

Kritikus szintű üzenet naplózása.

```python
@abstractmethod
def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
    """Kritikus szintű üzenet naplózása.

    Súlyos hibák naplózására szolgál, amelyek alkalmazásleállást okozhatnak.

    Args:
        message: A naplózandó üzenet szövege.
        **kwargs: További kontextusparaméterek (pl. extra, exc_info).
    """
```

**Paraméterek:**
- `message` (str): A naplózandó üzenet szövege
- `**kwargs` (Mapping[str, AnyStr]): További kontextusparaméterek

### `set_level()`

Logger naplózási szintjének beállítása.

```python
@abstractmethod
def set_level(self, level: int) -> None:
    """Logger naplózási szintjének beállítása.

    Beállítja a minimális naplózási szintet. A szintnél alacsonyabb
    prioritású üzenetek nem lesznek naplózva.

    Args:
        level: Az új naplózási szint (0-50 közötti egész szám).
    """
```

**Paraméterek:**
- `level` (int): Az új naplózási szint

### `get_level()`

Aktuális naplózási szint lekérdezése.

```python
@abstractmethod
def get_level(self) -> int:
    """Aktuális naplózási szint lekérdezése.

    Returns:
        int: A jelenleg beállított naplózási szint értéke.
    """
```

**Visszatérési érték:**
- `int`: A jelenleg beállított naplózási szint értéke

## Implementáció példa

### Alap logger implementáció

```python
from neural_ai.core.logger.interfaces import LoggerInterface
import logging
from typing import Mapping, AnyStr, Optional

class BasicLogger(LoggerInterface):
    """Alap logger implementáció."""
    
    def __init__(
        self,
        name: str,
        config: Optional["ConfigManagerInterface"] = None,
        **kwargs: Mapping[str, AnyStr]
    ) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self.logger.debug(message, extra=kwargs if kwargs else None)
    
    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self.logger.info(message, extra=kwargs if kwargs else None)
    
    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self.logger.warning(message, extra=kwargs if kwargs else None)
    
    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self.logger.error(message, extra=kwargs if kwargs else None)
    
    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self.logger.critical(message, extra=kwargs if kwargs else None)
    
    def set_level(self, level: int) -> None:
        self.logger.setLevel(level)
    
    def get_level(self) -> int:
        return self.logger.level

# Használat
logger = BasicLogger("my_app")
logger.info("Alap logger használatban")
```

### Adatbázis logger implementáció

```python
from neural_ai.core.logger.interfaces import LoggerInterface
from typing import Mapping, AnyStr, Optional
import datetime

class DatabaseLogger(LoggerInterface):
    """Adatbázisba logoló implementáció."""
    
    def __init__(
        self,
        name: str,
        config: Optional["ConfigManagerInterface"] = None,
        **kwargs: Mapping[str, AnyStr]
    ) -> None:
        self.name = name
        self.db_connection = kwargs.get('db_connection')
        self.level = logging.INFO
    
    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        if self.level <= logging.DEBUG:
            self._insert_log("DEBUG", message, kwargs)
    
    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        if self.level <= logging.INFO:
            self._insert_log("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        if self.level <= logging.WARNING:
            self._insert_log("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        if self.level <= logging.ERROR:
            self._insert_log("ERROR", message, kwargs)
    
    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        if self.level <= logging.CRITICAL:
            self._insert_log("CRITICAL", message, kwargs)
    
    def set_level(self, level: int) -> None:
        self.level = level
    
    def get_level(self) -> int:
        return self.level
    
    def _insert_log(self, level: str, message: str, extra: Mapping[str, AnyStr]) -> None:
        """Log bejegyzés beszúrása az adatbázisba."""
        if self.db_connection:
            timestamp = datetime.datetime.now()
            # SQL insert művelet
            # INSERT INTO logs (timestamp, level, logger_name, message, extra)
            # VALUES (?, ?, ?, ?, ?)
            pass

# Használat
db_logger = DatabaseLogger("my_app", db_connection="connection_string")
db_logger.info("Adatbázis logger használatban")
```

### HTTP API logger implementáció

```python
from neural_ai.core.logger.interfaces import LoggerInterface
import requests
from typing import Mapping, AnyStr, Optional
import json

class HttpLogger(LoggerInterface):
    """HTTP API-ba logoló implementáció."""
    
    def __init__(
        self,
        name: str,
        config: Optional["ConfigManagerInterface"] = None,
        **kwargs: Mapping[str, AnyStr]
    ) -> None:
        self.name = name
        self.api_url = kwargs.get('api_url')
        self.api_key = kwargs.get('api_key')
        self.level = logging.INFO
    
    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self._send_log("DEBUG", message, kwargs)
    
    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self._send_log("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self._send_log("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self._send_log("ERROR", message, kwargs)
    
    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:
        self._send_log("CRITICAL", message, kwargs)
    
    def set_level(self, level: int) -> None:
        self.level = level
    
    def get_level(self) -> int:
        return self.level
    
    def _send_log(self, level: str, message: str, extra: Mapping[str, AnyStr]) -> None:
        """Log küldése HTTP API-nak."""
        if self.api_url:
            payload = {
                "level": level,
                "logger": self.name,
                "message": message,
                "extra": dict(extra) if extra else {}
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            try:
                response = requests.post(
                    f"{self.api_url}/logs",
                    data=json.dumps(payload),
                    headers=headers
                )
                response.raise_for_status()
            except Exception as e:
                print(f"Hiba a log küldésénél: {e}")

# Használat
http_logger = HttpLogger(
    "my_app",
    api_url="https://api.example.com",
    api_key="your_api_key"
)
http_logger.info("HTTP logger használatban")
```

## Log szintek

A LoggerInterface a standard Python log szinteket támogatja:

| Szint | Érték | Leírás |
|-------|-------|--------|
| DEBUG | 10 | Részletes hibakeresési információk |
| INFO | 20 | Általános információk |
| WARNING | 30 | Figyelmeztető üzenetek |
| ERROR | 40 | Hibák |
| CRITICAL | 50 | Kritikus hibák |

## Kompatibilitás

Minden logger implementációnak implementálnia kell a LoggerInterface összes absztrakt metódusát:

```python
from neural_ai.core.logger.interfaces import LoggerInterface
import inspect

def check_logger_implementation(logger_class):
    """Ellenőrzi, hogy a logger osztály implementálja-e az interfészt."""
    abstract_methods = [
        name for name, method in inspect.getmembers(
            LoggerInterface,
            predicate=inspect.isfunction
        )
        if getattr(method, '__isabstractmethod__', False)
    ]
    
    missing_methods = []
    for method_name in abstract_methods:
        if not hasattr(logger_class, method_name):
            missing_methods.append(method_name)
    
    if missing_methods:
        raise TypeError(
            f"A {logger_class.__name__} osztály nem implementálja a következő metódusokat: "
            f"{', '.join(missing_methods)}"
        )
    
    return True

# Ellenőrzés
class IncompleteLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        pass
    
    def info(self, message: str, **kwargs):
        pass
    # Hiányzik a többi metódus

try:
    check_logger_implementation(IncompleteLogger)
except TypeError as e:
    print(f"Hiba: {e}")
```

## További információk

- [Logger Interfészek Áttekintés](__init__.md)
- [LoggerFactoryInterface](factory_interface.md)
- [Logger Implementációk](../implementations/__init__.md)
- [Logger Modul](../__init__.md)