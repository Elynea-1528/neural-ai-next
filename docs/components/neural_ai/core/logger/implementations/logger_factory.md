# LoggerFactory

## Áttekintés

A `LoggerFactory` osztály egy factory implementáció, amely felelős a különböző típusú loggerek létrehozásáért és kezeléséért. A factory mintát követve lehetővé teszi a dinamikus logger típusok regisztrálását és példányosítását.

## Osztály

```python
class LoggerFactory(LoggerFactoryInterface)
```

### Attribútumok

- **`_logger_types`**: `dict[str, type[LoggerInterface]]`
  - A regisztrált logger típusok szótára. Alapértelmezésként tartalmazza a `default`, `colored` és `rotating` logger típusokat.

- **`_instances`**: `dict[str, LoggerInterface]`
  - A létrehozott logger példányok gyorsítótárja, név alapján.

### Metódusok

#### `register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None`

Új logger típus regisztrálása a factory-be.

**Paraméterek:**
- `logger_type` (str): A logger típus egyedi neve.
- `logger_class` (type[LoggerInterface]): A logger osztály, amely implementálja a `LoggerInterface`-t.

**Példa:**
```python
LoggerFactory.register_logger("custom", CustomLogger)
```

#### `get_logger(cls, name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface`

Logger példány létrehozása vagy meglévő visszaadása név alapján.

**Paraméterek:**
- `name` (str): A logger egyedi neve.
- `logger_type` (str, opcionális): A kért logger típus. Alapértelmezés: `"default"`.
- `**kwargs` (Any): További paraméterek a logger inicializálásához.

**Visszatérési érték:**
- `LoggerInterface`: Az inicializált logger példány.

**Példa:**
```python
logger = LoggerFactory.get_logger("my_app", logger_type="colored")
```

#### `configure(cls, config: dict[str, Any]) -> None`

A logger rendszer konfigurálása a Python `logging` moduljának használatával.

**Paraméterek:**
- `config` (dict[str, Any]): Konfigurációs szótár a következő struktúrával:

```python
{
    'default_level': 'INFO',  # Alapértelmezett log szint
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log formátum
    'date_format': '%Y-%m-%d %H:%M:%S',  # Dátum formátum
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
```

**Példa:**
```python
config = {
    "default_level": "DEBUG",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "console": {"enabled": True, "level": "INFO"},
        "file": {"enabled": True, "filename": "app.log", "level": "DEBUG"}
    }
}
LoggerFactory.configure(config)
```

## Használat

### Alapvető használat

```python
from neural_ai.core.logger.implementations.logger_factory import LoggerFactory

# Alapértelmezett logger létrehozása
logger = LoggerFactory.get_logger("my_application")

# Színes logger létrehozása
colored_logger = LoggerFactory.get_logger("my_app", logger_type="colored")

# Rotating file logger létrehozása
rotating_logger = LoggerFactory.get_logger("my_app", logger_type="rotating", max_bytes=1000000, backup_count=5)
```

### Egyéni logger regisztrálása

```python
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

class CustomLogger(LoggerInterface):
    def __init__(self, name: str, custom_param: str):
        # Implementáció
        pass

    def debug(self, message: str) -> None:
        # Implementáció
        pass

    def info(self, message: str) -> None:
        # Implementáció
        pass

    def warning(self, message: str) -> None:
        # Implementáció
        pass

    def error(self, message: str) -> None:
        # Implementáció
        pass

    def critical(self, message: str) -> None:
        # Implementáció
        pass

# Regisztrálás
LoggerFactory.register_logger("custom", CustomLogger)

# Használat
logger = LoggerFactory.get_logger("my_app", logger_type="custom", custom_param="value")
```

## Implementáció részletek

### Típusbiztonság

A `LoggerFactory` szigorú típusellenőrzést használ a `mypy` segítségével. A `TYPE_CHECKING` blokk biztosítja, hogy a típusellenőrzés során ne legyenek körkörös import problémák.

### Factory minta

Az osztály a factory tervezési mintát követi, amely lehetővé teszi:
- A logger implementációk lazítását a létrehozásuktól.
- Az egységes interfész használatát különböző logger típusok esetén.
- A logger típusok dinamikus bővítését futási időben.

### Singleton jelleg

A `get_logger` metódus gyorsítótárazza a létrehozott logger példányokat, így ugyanazzal a névvel történő hívás mindig ugyanazt a példányt adja vissza.

## Függőségek

- `neural_ai.core.logger.interfaces.factory_interface.LoggerFactoryInterface`
- `neural_ai.core.logger.interfaces.logger_interface.LoggerInterface`
- `neural_ai.core.logger.implementations.colored_logger.ColoredLogger`
- `neural_ai.core.logger.implementations.default_logger.DefaultLogger`
- `neural_ai.core.logger.implementations.rotating_file_logger.RotatingFileLogger`

## Kapcsolódó dokumentáció

- [LoggerInterface](logger_interface.md)
- [DefaultLogger](default_logger.md)
- [ColoredLogger](colored_logger.md)
- [RotatingFileLogger](rotating_file_logger.md)