# LoggerFactoryInterface - Logger Factory Interfész

## Áttekintés

Logger factory interfész. Ez az interfész definiálja a logger factory-k alapvető működését, beleértve a logger típusok regisztrálását, példányosítását és a logger rendszer konfigurálását.

## Interfész leírása

```python
class LoggerFactoryInterface(ABC):
    """Logger factory interfész.

    Az interfész lehetővé teszi különböző logger implementációk
    dinamikus regisztrálását és példányosítását factory pattern
    segítségével.
    """
```

## Absztrakt metódusok

### `register_logger()`

Új logger típus regisztrálása a factory számára.

```python
@classmethod
@abstractmethod
def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
    """Új logger típus regisztrálása a factory számára.

    Args:
        logger_type: A logger típus egyedi azonosítója
        logger_class: A logger osztály, amely implementálja a LoggerInterface-t

    Raises:
        ValueError: Ha a logger_type már létezik
        TypeError: Ha a logger_class nem implementálja a LoggerInterface-t
    """
```

**Paraméterek:**
- `logger_type` (str): A logger típus egyedi azonosítója
- `logger_class` (type[LoggerInterface]): A logger osztály

**Kivételek:**
- `ValueError`: Ha a logger_type már létezik
- `TypeError`: Ha a logger_class nem implementálja a LoggerInterface-t

### `get_logger()`

Logger példány létrehozása vagy visszaadása.

```python
@classmethod
@abstractmethod
def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
    """Logger példány létrehozása vagy visszaadása.

    Args:
        name: A logger egyedi neve
        logger_type: A kért logger típus (alapértelmezett: "default")
        **kwargs: További paraméterek a logger inicializálásához

    Returns:
        LoggerInterface: Az inicializált logger példány

    Raises:
        KeyError: Ha a logger_type nincs regisztrálva
        ValueError: Ha a name üres string
    """
```

**Paraméterek:**
- `name` (str): A logger egyedi neve
- `logger_type` (str): A kért logger típus (alapértelmezett: "default")
- `**kwargs`: További paraméterek a logger inicializálásához

**Visszatérési érték:**
- `LoggerInterface`: Az inicializált logger példány

**Kivételek:**
- `KeyError`: Ha a logger_type nincs regisztrálva
- `ValueError`: Ha a name üres string

### `configure()`

Logger rendszer konfigurálása.

```python
@classmethod
@abstractmethod
def configure(cls, config: dict[str, Any]) -> None:
    """Logger rendszer konfigurálása.

    Args:
        config: Konfigurációs beállítások dictionary formátumban

    Raises:
        ValueError: Ha a konfiguráció érvénytelen
    """
```

**Paraméterek:**
- `config` (dict[str, Any]): Konfigurációs beállítások dictionary formátumban

**Kivételek:**
- `ValueError`: Ha a konfiguráció érvénytelen

## Implementáció példa

### Alap factory implementáció

```python
from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface
)
from typing import Any

class BasicLoggerFactory(LoggerFactoryInterface):
    """Alap logger factory implementáció."""
    
    _logger_types: dict[str, type[LoggerInterface]] = {}
    _instances: dict[str, LoggerInterface] = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása."""
        if not issubclass(logger_class, LoggerInterface):
            raise TypeError(
                f"A {logger_class.__name__} nem implementálja a LoggerInterface-t"
            )
        
        cls._logger_types[logger_type] = logger_class
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása."""
        if not name:
            raise ValueError("A logger neve nem lehet üres")
        
        if logger_type not in cls._logger_types:
            raise KeyError(f"Ismeretlen logger típus: {logger_type}")
        
        # Ha már létezik ilyen nevű logger, adjuk vissza
        if name in cls._instances:
            return cls._instances[name]
        
        # Új logger létrehozása
        logger_class = cls._logger_types[logger_type]
        logger = logger_class(name, **kwargs)
        
        # Elmentjük a gyorsítótárba
        cls._instances[name] = logger
        return logger
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása."""
        # Alap konfiguráció implementáció
        # Pl. root logger beállítása
        pass

# Használat
factory = BasicLoggerFactory()
factory.register_logger("basic", BasicLogger)
logger = factory.get_logger("my_app", logger_type="basic")
```

### Bővíthető factory implementáció

```python
from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface
)
from typing import Any
import logging

class ExtensibleLoggerFactory(LoggerFactoryInterface):
    """Bővíthető logger factory implementáció."""
    
    _logger_types: dict[str, type[LoggerInterface]] = {}
    _instances: dict[str, LoggerInterface] = {}
    _config: dict[str, Any] = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása."""
        if logger_type in cls._logger_types:
            raise ValueError(f"A '{logger_type}' logger típus már létezik")
        
        if not issubclass(logger_class, LoggerInterface):
            raise TypeError(
                f"A {logger_class.__name__} nem implementálja a LoggerInterface-t"
            )
        
        cls._logger_types[logger_type] = logger_class
        print(f"Logger típus regisztrálva: {logger_type} -> {logger_class.__name__}")
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása."""
        if not name or not name.strip():
            raise ValueError("A logger neve nem lehet üres")
        
        if logger_type not in cls._logger_types:
            available_types = list(cls._logger_types.keys())
            raise KeyError(
                f"Ismeretlen logger típus: {logger_type}. "
                f"Elérhető típusok: {available_types}"
            )
        
        # Singleton viselkedés: ha már létezik, adjuk vissza
        instance_key = f"{name}_{logger_type}"
        if instance_key in cls._instances:
            return cls._instances[instance_key]
        
        # Új logger létrehozása
        logger_class = cls._logger_types[logger_type]
        
        # Konfigurációs paraméterek egyesítése
        merged_kwargs = {**cls._config, **kwargs}
        
        logger = logger_class(name, **merged_kwargs)
        
        # Elmentjük a gyorsítótárba
        cls._instances[instance_key] = logger
        return logger
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása."""
        cls._config.update(config)
        
        # Root logger konfigurálása
        if 'default_level' in config:
            level = getattr(logging, config['default_level'])
            logging.getLogger().setLevel(level)
    
    @classmethod
    def get_registered_types(cls) -> list[str]:
        """Regisztrált logger típusok listázása."""
        return list(cls._logger_types.keys())
    
    @classmethod
    def clear_cache(cls) -> None:
        """Logger példányok gyorsítótárának ürítése."""
        cls._instances.clear()

# Használat
factory = ExtensibleLoggerFactory()

# Logger regisztrálása
factory.register_logger("console", ConsoleLogger)
factory.register_logger("file", FileLogger)

# Konfiguráció beállítása
factory.configure({
    'default_level': 'INFO',
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
})

# Logger létrehozása
console_logger = factory.get_logger("my_app", logger_type="console")
file_logger = factory.get_logger("my_app", logger_type="file", log_file="app.log")

# Regisztrált típusok listázása
types = factory.get_registered_types()
print(f"Regisztrált típusok: {types}")
```

### Dinamikus factory implementáció

```python
from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface
)
from typing import Any
import importlib

class DynamicLoggerFactory(LoggerFactoryInterface):
    """Dinamikus logger factory, ami futás közben is betölthet loggereket."""
    
    _logger_types: dict[str, type[LoggerInterface]] = {}
    _instances: dict[str, LoggerInterface] = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        """Új logger típus regisztrálása."""
        if not issubclass(logger_class, LoggerInterface):
            raise TypeError(
                f"A {logger_class.__name__} nem implementálja a LoggerInterface-t"
            )
        
        cls._logger_types[logger_type] = logger_class
    
    @classmethod
    def register_logger_from_module(cls, logger_type: str, module_path: str, class_name: str) -> None:
        """Logger regisztrálása modulból dinamikusan."""
        try:
            module = importlib.import_module(module_path)
            logger_class = getattr(module, class_name)
            
            if not issubclass(logger_class, LoggerInterface):
                raise TypeError(
                    f"A {class_name} nem implementálja a LoggerInterface-t"
                )
            
            cls.register_logger(logger_type, logger_class)
            print(f"Logger betöltve: {module_path}.{class_name} -> {logger_type}")
            
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Hiba a logger betöltésénél: {e}")
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        """Logger példány létrehozása."""
        if not name:
            raise ValueError("A logger neve nem lehet üres")
        
        if logger_type not in cls._logger_types:
            raise KeyError(f"Ismeretlen logger típus: {logger_type}")
        
        # Singleton viselkedés
        instance_key = f"{name}_{logger_type}"
        if instance_key in cls._instances:
            return cls._instances[instance_key]
        
        # Új logger létrehozása
        logger_class = cls._logger_types[logger_type]
        logger = logger_class(name, **kwargs)
        
        cls._instances[instance_key] = logger
        return logger
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        """Logger rendszer konfigurálása."""
        # Konfiguráció implementáció
        pass
    
    @classmethod
    def reload_logger(cls, logger_type: str, module_path: str, class_name: str) -> None:
        """Logger újratöltése futás közben."""
        # Régi példányok törlése
        cls._instances = {
            k: v for k, v in cls._instances.items() 
            if not k.endswith(f"_{logger_type}")
        }
        
        # Logger újratöltése
        cls.register_logger_from_module(logger_type, module_path, class_name)

# Használat
factory = DynamicLoggerFactory()

# Logger betöltése dinamikusan
factory.register_logger_from_module(
    "custom",
    "my_custom_loggers",
    "CustomLogger"
)

# Logger létrehozása
logger = factory.get_logger("my_app", logger_type="custom")

# Logger újratöltése futás közben
factory.reload_logger("custom", "my_updated_loggers", "UpdatedCustomLogger")
```

## Factory mintázat előnyei

A LoggerFactoryInterface használatának fő előnyei:

1. **Laza csatolás**: A kliens kód nem függ a konkrét logger implementációktól
2. **Bővíthetőség**: Új logger típusok egyszerűen hozzáadhatók
3. **Konfigurálhatóság**: A logger rendszer centralizáltan konfigurálható
4. **Tesztelhetőség**: Mock logger-ek egyszerűen cserélhetők
5. **Singleton viselkedés**: Minden névhez csak egy logger példány jön létre

## Komplex példa

```python
from neural_ai.core.logger.interfaces import (
    LoggerFactoryInterface,
    LoggerInterface
)
from typing import Any
import logging

# Logger implementációk
class ConsoleLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        self.logger = logging.getLogger(name)
        # Konzol handler beállítása
        pass
    
    # ... implementáció

class FileLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        self.logger = logging.getLogger(name)
        # Fájl handler beállítása
        pass
    
    # ... implementáció

# Factory implementáció
class ApplicationLoggerFactory(LoggerFactoryInterface):
    """Alkalmazás specifikus logger factory."""
    
    _logger_types = {}
    _instances = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        if not issubclass(logger_class, LoggerInterface):
            raise TypeError(f"{logger_class.__name__} nem implementálja a LoggerInterface-t")
        cls._logger_types[logger_type] = logger_class
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface:
        if not name:
            raise ValueError("A logger neve nem lehet üres")
        
        if logger_type not in cls._logger_types:
            raise KeyError(f"Ismeretlen logger típus: {logger_type}")
        
        instance_key = f"{name}_{logger_type}"
        if instance_key not in cls._instances:
            logger = cls._logger_types[logger_type](name, **kwargs)
            cls._instances[instance_key] = logger
        
        return cls._instances[instance_key]
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        # Konfiguráció implementáció
        pass

# Alkalmazás
factory = ApplicationLoggerFactory()

# Logger-ek regisztrálása
factory.register_logger("console", ConsoleLogger)
factory.register_logger("file", FileLogger)

# Konfiguráció
factory.configure({
    'default_level': 'INFO'
})

# Logger-ek használata
console_log = factory.get_logger("app.console", "console")
file_log = factory.get_logger("app.file", "file", filename="app.log")

console_log.info("Konzol log üzenet")
file_log.info("Fájl log üzenet")
```

## További információk

- [Logger Interfészek Áttekintés](__init__.md)
- [LoggerInterface](logger_interface.md)
- [Logger Factory](../factory.md)
- [Logger Implementációk](../implementations/__init__.md)