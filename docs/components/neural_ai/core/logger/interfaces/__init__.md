# Logger Interfészek

## Áttekintés

Ez a modul exportálja a logger komponens által definiált interfészeket, és biztosítja a csomag verzióinformációinak dinamikus betöltését. A TYPE_CHECKING blokk segítségével elkerüljük a körkörös importokat.

## Elérhető interfészek

### [`LoggerInterface`](logger_interface.md)
A naplózási műveletek absztrakt definíciója.

### [`LoggerFactoryInterface`](factory_interface.md)
Logger factory interfész.

## Verzióinformációk

A modul automatikusan betölti a csomag verzióját a pyproject.toml-ból:

```python
from neural_ai.core.logger.interfaces import __version__

print(f"Logger interfész verzió: {__version__}")
```

## Használat

### Interfészek importálása

```python
from neural_ai.core.logger.interfaces import (
    LoggerInterface,
    LoggerFactoryInterface,
    __version__
)

print(f"Logger interfész verzió: {__version__}")
```

### LoggerInterface implementálása

```python
from neural_ai.core.logger.interfaces import LoggerInterface
import logging

class CustomLogger(LoggerInterface):
    """Egyéni logger implementáció."""
    
    def __init__(self, name: str, **kwargs):
        self.logger = logging.getLogger(name)
        # Egyéni inicializálás
        pass
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        self.logger.critical(message, extra=kwargs)
    
    def set_level(self, level: int):
        self.logger.setLevel(level)
    
    def get_level(self) -> int:
        return self.logger.level

# Használat
custom_logger = CustomLogger("my_app")
custom_logger.info("Egyéni logger használatban")
```

### LoggerFactoryInterface implementálása

```python
from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface
)
from typing import Any

class CustomLoggerFactory(LoggerFactoryInterface):
    """Egyéni logger factory implementáció."""
    
    _loggers = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása."""
        cls._loggers[logger_type] = logger_class
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása."""
        if logger_type not in cls._loggers:
            raise ValueError(f"Ismeretlen logger típus: {logger_type}")
        
        logger_class = cls._loggers[logger_type]
        return logger_class(name, **kwargs)
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása."""
        # Konfiguráció implementáció
        pass

# Használat
factory = CustomLoggerFactory()
factory.register_logger("custom", CustomLogger)
logger = factory.get_logger("my_app", logger_type="custom")
```

## Verziókezelés

A modul dinamikusan betölti a verzióinformációkat:

```python
from neural_ai.core.logger.interfaces import __version__

try:
    # A verzió automatikusan betöltődik
    print(f"Logger interfész verzió: {__version__}")
except Exception as e:
    # Fallback verzió, ha a csomag nincs telepítve
    print(f"Hiba a verzió betöltésénél: {e}")
    print("Fallback verzió: 1.0.0")
```

## TYPE_CHECKING használata

A modul TYPE_CHECKING blokkot használ a körkörös importok elkerülésére:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

# Itt már biztonságosan importálhatjuk
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Komplex példa

```python
from neural_ai.core.logger.interfaces import (
    LoggerInterface,
    LoggerFactoryInterface,
    __version__
)
import logging
from typing import Any

# Egyéni logger implementáció
class DatabaseLogger(LoggerInterface):
    """Adatbázisba logoló implementáció."""
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.db_connection = kwargs.get('db_connection')
    
    def debug(self, message: str, **kwargs):
        self._log_to_db("DEBUG", message, kwargs)
    
    def info(self, message: str, **kwargs):
        self._log_to_db("INFO", message, kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_to_db("WARNING", message, kwargs)
    
    def error(self, message: str, **kwargs):
        self._log_to_db("ERROR", message, kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log_to_db("CRITICAL", message, kwargs)
    
    def set_level(self, level: int):
        self.level = level
    
    def get_level(self) -> int:
        return self.level
    
    def _log_to_db(self, level: str, message: str, extra: dict):
        # Adatbázisba írás implementáció
        if self.db_connection:
            # SQL insert művelet
            pass

# Egyéni factory implementáció
class DatabaseLoggerFactory(LoggerFactoryInterface):
    """Adatbázis logger factory."""
    
    _loggers = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        cls._loggers[logger_type] = logger_class
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        if logger_type not in cls._loggers:
            raise ValueError(f"Ismeretlen logger típus: {logger_type}")
        
        return cls._loggers[logger_type](name, **kwargs)
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        # Konfiguráció implementáció
        pass

# Használat
print(f"Logger interfész verzió: {__version__}")

# Factory inicializálása
factory = DatabaseLoggerFactory()
factory.register_logger("database", DatabaseLogger)

# Logger létrehozása
db_logger = factory.get_logger(
    "my_app",
    logger_type="database",
    db_connection="connection_string"
)

# Használat
db_logger.info("Alkalmazás elindult")
db_logger.warning("Figyelmeztető üzenet")
```

## További információk

- [LoggerInterface Részletes Dokumentáció](logger_interface.md)
- [LoggerFactoryInterface Részletes Dokumentáció](factory_interface.md)
- [Logger Modul Áttekintés](../__init__.md)
- [Logger Implementációk](../implementations/__init__.md)