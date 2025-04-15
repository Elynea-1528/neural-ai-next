# Logger Komponens Dokumentáció

## Tartalomjegyzék
- [Áttekintés](#áttekintés)
- [Architektúra](#architektúra)
- [Szolgáltatások](#szolgáltatások)
- [Telepítés és Konfiguráció](#telepítés-és-konfiguráció)
- [Használati Útmutató](#használati-útmutató)
- [API Dokumentáció](#api-dokumentáció)
- [Példák](#példák)
- [Hibaelhárítás](#hibaelhárítás)

## Áttekintés

A Logger komponens a Neural AI Next keretrendszer központi naplózó rendszere. A komponens felelős a rendszer minden részéből érkező naplóbejegyzések kezeléséért, formázásáért és tárolásáért.

### Főbb funkciók

- Színes konzol kimenet a jobb olvashatóságért
- Fájl alapú naplózás rotációs támogatással
- Méret és idő alapú log rotáció
- Automatikus log tömörítés
- Különböző log szintek támogatása
- Testreszabható formátumok
- Többszintű konfiguráció

## Architektúra

A komponens a következő fő részekből áll:

```
neural_ai/core/logger/
├── interfaces/                # Interfész definíciók
│   ├── logger_interface.py   # Alap logger interfész
│   └── factory_interface.py  # Logger factory interfész
├── implementations/          # Implementációk
│   ├── default_logger.py     # Alapértelmezett logger
│   ├── colored_logger.py     # Színes konzol logger
│   ├── rotating_logger.py    # Rotáló fájl logger
│   └── logger_factory.py     # Logger gyártó osztály
├── formatters/              # Formázók
│   └── logger_formatters.py # Színes formázó
└── exceptions.py            # Logger specifikus kivételek
```

### Interfészek

- `LoggerInterface`: Definiálja az alap logger műveleteket
- `LoggerFactoryInterface`: Logger példányok létrehozásáért felelős

### Implementációk

1. **DefaultLogger**
   - Alap naplózási funkciók
   - Egyszerű szöveges kimenet

2. **ColoredLogger**
   - Színes konzol kimenet
   - Különböző színek a log szinteknek
   - ANSI színkódok használata

3. **RotatingFileLogger**
   - Fájl alapú naplózás
   - Méret vagy idő alapú rotáció
   - Automatikus tömörítés

## Szolgáltatások

### Log Szintek

- `DEBUG`: Fejlesztési információk
- `INFO`: Általános információk
- `WARNING`: Figyelmeztetések
- `ERROR`: Hibák
- `CRITICAL`: Kritikus hibák

### Színkódok

| Szint      | Szín                     |
|------------|--------------------------|
| DEBUG      | Kék                      |
| INFO       | Zöld                     |
| WARNING    | Sárga                    |
| ERROR      | Piros                    |
| CRITICAL   | Fehér piros háttéren     |

### Rotációs Beállítások

- **Méret alapú**:
  - Maximális fájlméret beállítható
  - Backup fájlok száma konfigurálható
  - Automatikus tömörítés

- **Idő alapú**:
  - Különböző időintervallumok (óránként, naponta, stb.)
  - Időbélyeggel ellátott backup fájlok
  - Automatikus archiválás

## Telepítés és Konfiguráció

### Függőségek

A komponens nem igényel külső függőségeket, csak a Python standard library-t használja.

### Konfiguráció

A konfigurációt a `configs/logger/logging.yaml` fájlban lehet megadni:

```yaml
default_level: "INFO"
format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format: "%Y-%m-%d %H:%M:%S"

handlers:
  console:
    enabled: true
    level: "INFO"
    colored: true

  file:
    enabled: true
    level: "DEBUG"
    filename: "logs/app.log"
    rotating: true
    max_bytes: 1048576  # 1MB
    backup_count: 5
```

## Használati Útmutató

### Alapvető használat

```python
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

logger = DefaultLogger("my_app")
logger.info("Alkalmazás elindult")
logger.error("Hiba történt", error_code=500)
```

### Színes Logger használata

```python
from neural_ai.core.logger.implementations.colored_logger import ColoredLogger

logger = ColoredLogger("my_app.ui")
logger.warning("Felhasználói munkamenet lejárt")
logger.critical("Adatbázis kapcsolat megszakadt")
```

### Rotáló Logger használata

```python
from neural_ai.core.logger.implementations.rotating_file_logger import RotatingFileLogger

logger = RotatingFileLogger(
    name="my_app.data",
    filename="logs/data.log",
    max_bytes=1024 * 1024,  # 1MB
    backup_count=5
)

logger.info("Adatok mentése")
```

## API Dokumentáció

### LoggerInterface

```python
class LoggerInterface(ABC):
    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def error(self, message: str, **kwargs: Any) -> None: ...

    @abstractmethod
    def critical(self, message: str, **kwargs: Any) -> None: ...
```

### ColoredLogger

```python
class ColoredLogger(LoggerInterface):
    def __init__(
        self,
        name: str,
        format_str: Optional[str] = None,
        stream: Optional[TextIO] = None
    ) -> None: ...
```

### RotatingFileLogger

```python
class RotatingFileLogger(LoggerInterface):
    def __init__(
        self,
        name: str,
        filename: str,
        rotation_type: str = "size",
        max_bytes: int = 1024 * 1024,
        backup_count: int = 5,
        when: str = "midnight",
        encoding: str = "utf-8",
        format_str: Optional[str] = None,
        level: str = "DEBUG"
    ) -> None: ...
```

## Példák

Részletes példák az `examples/logger_usage.py` fájlban találhatók, amelyek bemutatják:

- Alap naplózási funkciókat
- Színes konzol kimenetet
- Méret alapú rotációt
- Idő alapú rotációt
- Log tömörítést

## Hibaelhárítás

### Gyakori problémák és megoldások

1. **Nem jelenik meg színes kimenet**
   - Ellenőrizze, hogy a terminál támogatja-e az ANSI színkódokat
   - Windows esetén használja a `colorama` csomagot

2. **Log rotáció nem működik**
   - Ellenőrizze a jogosultságokat a log könyvtárban
   - Ellenőrizze a max_bytes és backup_count beállításokat

3. **Duplikált log bejegyzések**
   - Ellenőrizze a logger propagációs beállításait
   - Használja a `logger.propagate = False` beállítást
