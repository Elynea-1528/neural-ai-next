# Logger Interfészek Modul (`neural_ai.core.logger.interfaces`)

## Áttekintés

Ez a modul tartalmazza a logger rendszer interfészeit, amelyek definiálják a loggerek és logger factory-k által implementálandó alapvető metódusokat és viselkedést. A modul biztosítja a verzióinformációk dinamikus kezelését is, automatikusan szinkronizálva a projekt konfigurációjával.

## Verziókezelés

A modul támogatja a dinamikus verzióbetöltést az `importlib.metadata` segítségével:

```python
from neural_ai.core.logger.interfaces import __version__

print(f"Logger interfész verzió: {__version__}")
# Output: Logger interfész verzió: 1.0.0
```

A verziószám automatikusan frissül a `pyproject.toml`-ban megadott verzióval, így nincs szükség manuális verziókezelésre.

## Tartalom

### Exportált Interfészek

#### `LoggerInterface`

Az alapvető logger interfész, amely meghatározza a loggerek által támogatott műveleteket.

**Metódusok:**
- `debug(message: str, **kwargs: Any) -> None` - Debug szintű üzenet logolása
- `info(message: str, **kwargs: Any) -> None` - Info szintű üzenet logolása
- `warning(message: str, **kwargs: Any) -> None` - Warning szintű üzenet logolása
- `error(message: str, **kwargs: Any) -> None` - Error szintű üzenet logolása
- `critical(message: str, **kwargs: Any) -> None` - Critical szintű üzenet logolása
- `set_level(level: int) -> None` - Logger log szintjének beállítása
- `get_level() -> int` - Aktuális log szint lekérése

**Használat:**
```python
from neural_ai.core.logger.interfaces import LoggerInterface

class MyLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        # Saját inicializálás
    
    def debug(self, message: str, **kwargs) -> None:
        # Saját debug implementáció
        pass
    
    # ... további metódusok implementációja
```

#### `LoggerFactoryInterface`

A logger factory interfész, amely meghatározza a logger példányok létrehozásának és kezelésének módját.

**Metódusok:**
- `register_logger(logger_type: str, logger_class: type[LoggerInterface]) -> None` - Új logger típus regisztrálása
- `get_logger(name: str, logger_type: str = "default", **kwargs: Any) -> LoggerInterface` - Logger példány létrehozása vagy visszaadása
- `configure(config: dict[str, Any]) -> None` - Logger rendszer konfigurálása

**Használat:**
```python
from neural_ai.core.logger.interfaces import LoggerFactoryInterface

class MyLoggerFactory(LoggerFactoryInterface):
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        # Saját regisztrációs logika
        pass
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs) -> LoggerInterface:
        # Saját logger létrehozási logika
        pass
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        # Saját konfigurációs logika
        pass
```

## Importálás

```python
# Összes interfész importálása
from neural_ai.core.logger.interfaces import (
    LoggerInterface,
    LoggerFactoryInterface,
    __version__
)

# Egyéni importálás
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface

# Verzió lekérdezése
print(f"Logger interfész verzió: {__version__}")
```

## Kapcsolódó Komponensek

- [`neural_ai.core.logger.implementations`](../implementations/__init__.md) - Logger implementációk
- [`neural_ai.core.logger.formatters`](../formatters/logger_formatters.md) - Log formázók
- [`neural_ai.core.logger.exceptions`](../exceptions.md) - Logger kivételek

## Fejlesztés

### Interfész Implementálása

Amikor új logger implementációt készítesz, mindenképpen implementáld az összes absztrakt metódust:

```python
from neural_ai.core.logger.interfaces import LoggerInterface

class CustomLogger(LoggerInterface):
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        # Inicializálás
    
    def debug(self, message: str, **kwargs) -> None:
        # Implementáció
        pass
    
    def info(self, message: str, **kwargs) -> None:
        # Implementáció
        pass
    
    # ... minden absztrakt metódus implementálása kötelező
```

### Factory Implementálása

```python
from neural_ai.core.logger.interfaces import LoggerFactoryInterface, LoggerInterface

class CustomLoggerFactory(LoggerFactoryInterface):
    _logger_types: dict[str, type[LoggerInterface]] = {}
    
    @classmethod
    def register_logger(cls, logger_type: str, logger_class: type[LoggerInterface]) -> None:
        cls._logger_types[logger_type] = logger_class
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs) -> LoggerInterface:
        if logger_type not in cls._logger_types:
            raise ValueError(f"Ismeretlen logger típus: {logger_type}")
        return cls._logger_types[logger_type](name=name, **kwargs)
    
    @classmethod
    def configure(cls, config: dict[str, Any]) -> None:
        # Konfiguráció feldolgozása
        pass
```

## Hibakezelés

Az interfészek használatakor figyelj a következőkre:

1. **Absztrakt metódusok**: Minden absztrakt metódust implementálni kell
2. **Típusmegfelelés**: A paraméterek és visszatérési értékek típusai meg kell egyezzenek
3. **Interfész példányosítás**: Az interfészeket nem lehet közvetlenül példányosítani

```python
# Helytelen - TypeError-t okoz
logger = LoggerInterface()  # ❌

# Helyes - implementációt kell használni
logger = DefaultLogger(name="my_logger")  # ✅
```

## Jövőbeli Fejlesztések

- [ ] Aszinkron logolás támogatása
- [ ] Strukturált logolás interfésze
- [ ] Metrikák és teljesítményfigyelés interfészei
- [ ] Plug-in rendszer interfészei
- [x] Dinamikus verziókezelés implementálva
- [ ] Verziókompatibilitás ellenőrzése

## Lásd még

- [Logger komponens fő dokumentációja](../__init__.md)
- [Fejlesztői dokumentáció](../../../../development/component_development_guide.md)
- [Tesztelési útmutató](../../../../development/unified_development_guide.md)