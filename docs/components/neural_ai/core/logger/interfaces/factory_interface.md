# Logger Factory Interface

## Áttekintés

A `LoggerFactoryInterface` egy absztrakt interfész, amely definiálja a logger factory-k alapvető működését. Ez az interfész lehetővé teszi különböző logger implementációk dinamikus regisztrálását és példányosítását a **Factory Pattern** segítségével.

## Cél

A factory interfész fő célja, hogy:
- **Dinamikus logger regisztrációt** biztosítson
- **Logger példányok létrehozását** egységesítse
- **Konfigurálható logger rendszert** valósítson meg
- **Bővíthetőséget** nyújtson új logger típusok hozzáadásához

## Osztály Struktúra

```python
class LoggerFactoryInterface(ABC):
    """Logger factory interfész.
    
    Az interfész lehetővé teszi különböző logger implementációk
    dinamikus regisztrálását és példányosítását factory pattern
    segítségével.
    """
```

## Metódusok

### `register_logger`

```python
@classmethod
@abstractmethod
def register_logger(
    cls,
    logger_type: str,
    logger_class: Type[LoggerInterface]
) -> None:
    """Új logger típus regisztrálása a factory számára.

    Args:
        logger_type: A logger típus egyedi azonosítója
        logger_class: A logger osztály, amely implementálja a LoggerInterface-t

    Raises:
        ValueError: Ha a logger_type már létezik
        TypeError: Ha a logger_class nem implementálja a LoggerInterface-t
    """
```

**Feladata:**
- Új logger típus regisztrálása a factory rendszerben
- Ellenőrzi, hogy a logger osztály implementálja-e a `LoggerInterface`-t
- Megakadályozza a duplikált típusok regisztrálását

**Paraméterek:**
- `logger_type` (str): A logger típus egyedi azonosítója (pl: "default", "colored", "file")
- `logger_class` (Type[LoggerInterface]): A logger osztály, amely implementálja a LoggerInterface-t

**Kivételek:**
- `ValueError`: Ha a logger_type már létezik
- `TypeError`: Ha a logger_class nem implementálja a LoggerInterface-t

### `get_logger`

```python
@classmethod
@abstractmethod
def get_logger(
    cls,
    name: str,
    logger_type: str = "default",
    **kwargs: Any
) -> LoggerInterface:
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

**Feladata:**
- Logger példány létrehozása vagy meglévő visszaadása
- Paraméterek továbbítása a logger inicializálásához
- Gyorsítótárazás a hatékonyság érdekében

**Paraméterek:**
- `name` (str): A logger egyedi neve
- `logger_type` (str, optional): A kért logger típus (alapértelmezett: "default")
- `**kwargs` (Any): További paraméterek a logger inicializálásához

**Visszatérési érték:**
- `LoggerInterface`: Az inicializált logger példány

**Kivételek:**
- `KeyError`: Ha a logger_type nincs regisztrálva
- `ValueError`: Ha a name üres string

### `configure`

```python
@classmethod
@abstractmethod
def configure(cls, config: Dict[str, Any]) -> None:
    """Logger rendszer konfigurálása.

    Args:
        config: Konfigurációs beállítások dictionary formátumban

    Raises:
        ValueError: Ha a konfiguráció érvénytelen
    """
```

**Feladata:**
- A logger rendszer globális konfigurálása
- Beállítások alkalmazása az összes loggerre

**Paraméterek:**
- `config` (Dict[str, Any]): Konfigurációs beállítások dictionary formátumban

**Kivételek:**
- `ValueError`: Ha a konfiguráció érvénytelen

## Használati Példák

### Alapvető Használat

```python
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

class MyLogger(LoggerInterface):
    def __init__(self, name: str):
        self.name = name
    
    def debug(self, message: str, **kwargs) -> None:
        print(f"DEBUG [{self.name}]: {message}")
    
    def info(self, message: str, **kwargs) -> None:
        print(f"INFO [{self.name}]: {message}")
    
    def warning(self, message: str, **kwargs) -> None:
        print(f"WARNING [{self.name}]: {message}")
    
    def error(self, message: str, **kwargs) -> None:
        print(f"ERROR [{self.name}]: {message}")
    
    def critical(self, message: str, **kwargs) -> None:
        print(f"CRITICAL [{self.name}]: {message}")
    
    def set_level(self, level: int) -> None:
        self.level = level
    
    def get_level(self) -> int:
        return getattr(self, 'level', 0)

# Logger regisztrálása
LoggerFactory.register_logger("my_logger", MyLogger)

# Logger példány létrehozása
logger = LoggerFactory.get_logger("test_app", "my_logger")
logger.info("Alkalmazás elindult")
```

### Több Logger Típus Használata

```python
# Különböző logger típusok regisztrálása
LoggerFactory.register_logger("console", ConsoleLogger)
LoggerFactory.register_logger("file", FileLogger)
LoggerFactory.register_logger("colored", ColoredLogger)

# Logger példányok létrehozása
console_logger = LoggerFactory.get_logger("app", "console")
file_logger = LoggerFactory.get_logger("app", "file", filename="app.log")
colored_logger = LoggerFactory.get_logger("app", "colored")
```

### Konfiguráció Használata

```python
# Logger rendszer konfigurálása
config = {
    "log_level": "DEBUG",
    "handlers": {
        "console": {"enabled": True},
        "file": {"enabled": True, "filename": "app.log"}
    }
}
LoggerFactory.configure(config)
```

## Implementációs Javaslatok

### Singleton Pattern

A factory implementációkban érdemes a **Singleton Pattern**-t használni a logger példányok kezeléséhez:

```python
class LoggerFactory(LoggerFactoryInterface):
    _logger_types: Dict[str, Type[LoggerInterface]] = {}
    _instances: Dict[str, LoggerInterface] = {}
    
    @classmethod
    def get_logger(cls, name: str, logger_type: str = "default", **kwargs):
        instance_key = f"{name}_{logger_type}"
        if instance_key not in cls._instances:
            logger_class = cls._logger_types[logger_type]
            cls._instances[instance_key] = logger_class(name=name, **kwargs)
        return cls._instances[instance_key]
```

### Dependency Injection

A factory-t érdemes **Dependency Injection** segítségével használni:

```python
class MyService:
    def __init__(self, logger_factory: LoggerFactoryInterface):
        self.logger = logger_factory.get_logger("MyService")
    
    def process(self):
        self.logger.info("Feldolgozás elkezdve")
```

## Hibakezelés

### Érvénytelen Logger Típus

```python
try:
    logger = LoggerFactory.get_logger("app", "unknown_type")
except KeyError as e:
    print(f"Hiba: {e}")
    # Kezelés: regisztráld a hiányzó logger típust
    LoggerFactory.register_logger("unknown_type", DefaultLogger)
```

### Duplikált Regisztráció

```python
try:
    LoggerFactory.register_logger("default", MyLogger)
    LoggerFactory.register_logger("default", AnotherLogger)  # ValueError
except ValueError as e:
    print(f"Hiba: {e}")
```

## Tesztelés

A factory interfész tesztelésekor érdemes a következő teszteseteket lefedni:

1. **Sikeres regisztráció** - Ellenőrzi, hogy a logger típusok helyesen regisztrálódnak-e
2. **Duplikált regisztráció** - Ellenőrzi a duplikált típusok elutasítását
3. **Érvénytelen osztály** - Ellenőrzi a nem megfelelő interfész implementációk elutasítását
4. **Logger létrehozás** - Ellenőrzi a logger példányok helyes létrehozását
5. **Gyorsítótárazás** - Ellenőrzi, hogy ugyanazt a példányt adja-e vissza
6. **Konfiguráció** - Ellenőrzi a rendszer konfigurálásának működését

## Kapcsolódó Komponensek

- [`LoggerInterface`](logger_interface.md) - A logger implementációk alapinterfésze
- [`LoggerFactory`](../implementations/logger_factory.md) - Konkrét factory implementáció
- [`DefaultLogger`](../implementations/default_logger.md) - Alapértelmezett logger implementáció
- [`ColoredLogger`](../implementations/colored_logger.md) - Színes kimenetű logger

## Jegyzetek

- Az interfész **absztrakt osztály**, nem példányosítható közvetlenül
- Minden metódus **@abstractmethod**, kötelező implementálni
- A factory pattern **bővíthetőséget** és **rugalmasságot** nyújt
- A logger példányokat érdemes **gyorsítótárazni** a hatékonyság érdekében
- A konfiguráció **globálisan** érvényesül a rendszerben