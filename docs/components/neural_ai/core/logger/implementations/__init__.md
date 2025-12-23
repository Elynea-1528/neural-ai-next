# Logger Implementációk Modul

## Áttekintés

Ez a modul a Neural AI Next projekt logger komponensének implementációit tartalmazza. A modul célja, hogy egységes és bővíthető logolási megoldást nyújtson a projekt számára, különböző logolási stratégiákat támogatva.

## Tartalom

A modul a következő főbb komponenseket exportálja:

### 1. ColoredLogger
Színes konzol kimenetű logger implementáció, amely a log szintek alapján különböző színeket használ a kimenet formázásához. Ez segít a gyorsabb hibakeresésben és a logok könnyebb olvashatóságában.

### 2. DefaultLogger
Alapértelmezett logger implementáció, amely egyszerű szöveges formátumban jeleníti meg a log üzeneteket. Ez a leginkább általános célú logger, amely a legtöbb használati esetre megfelelő.

### 3. LoggerFactory
Logger példányok létrehozásáért felelős gyár osztály. Ez az osztály biztosítja a különböző logger típusok egységes inicializálását és kezelését. A factory pattern alkalmazásával lehetővé teszi a logger implementációk dinamikus cserélhetőségét.

### 4. RotatingFileLogger
Fájl rotálást támogató logger implementáció. Ez a logger automatikusan kezeli a log fájlok rotálását méret vagy idő alapján, megelőzve ezzel a túl nagy fájlok keletkezését. Támogatja a méret alapú rotációt (maxBytes) és az idő alapú rotációt (when paraméter).

## Használat

### Alapvető használat

```python
from neural_ai.core.logger.implementations import LoggerFactory

# Logger létrehozása alapértelmezett típussal
logger = LoggerFactory.get_logger("my_app")

# Naplózás
logger.info("Alkalmazás elindult")
logger.debug("Hibakeresési információ")
logger.error("Hiba történt")
```

### Speciális logger típusok használata

```python
# Színes konzol logger
colored_logger = LoggerFactory.get_logger(
    "my_app", 
    logger_type="colored"
)

# Fájl rotálós logger
file_logger = LoggerFactory.get_logger(
    "my_app", 
    logger_type="rotating",
    log_file="/path/to/logfile.log",
    max_bytes=1048576,  # 1MB
    backup_count=5
)
```

### Logger konfigurálása

```python
from neural_ai.core.logger.implementations import LoggerFactory

config = {
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

LoggerFactory.configure(config)
```

## Függőségek

A logger implementációk modul a következő külső függőségeket használja:

- Python standard library: `logging`, `logging.handlers`
- Típusellenőrzés: `typing.TYPE_CHECKING`

A modul nem rendelkezik körkörös függőséggel más core komponensekkel, mivel a függőség injektálás mintát alkalmazza.

## Fejlesztés és Bővítés

### Új logger típus hozzáadása

1. Hozz létre egy új osztályt, amely implementálja a `LoggerInterface`-t
2. Regisztráld az új logger típust a `LoggerFactory`-ban:

```python
from neural_ai.core.logger.implementations import LoggerFactory
from neural_ai.core.logger.interfaces import LoggerInterface

class MyCustomLogger(LoggerInterface):
    # implementáció...

# Regisztráció
LoggerFactory.register_logger("custom", MyCustomLogger)

# Használat
logger = LoggerFactory.get_logger("my_app", logger_type="custom")
```

### Konfiguráció bővítése

A logger konfigurációt a `LoggerFactory.configure()` metóduson keresztül lehet bővíteni. A konfiguráció dictionary formátumban adható meg, és a rendszer automatikusan alkalmazza a megadott beállításokat.

## Hibakezelés

A logger implementációk robusztus hibakezelést biztosítanak:

- Érvénytelen konfiguráció esetén a rendszer alapértelmezett értékeket használ
- Fájl írási hibák esetén a logger automatikusan visszavált konzol kimenetre
- A rotáló file logger ellenőrzi a lemezterületet és a fájl jogosultságokat

## Teljesítmény

A logger implementációk a következő teljesítményoptimalizálásokat alkalmazzák:

- Lazy initialization: A logger csak akkor inicializálódik, amikor először használják
- Handler pooling: A handler-eket újrahasznosítja a gyakori logger létrehozásoknál
- Aszinkron naplózás: A naplózási műveletek nem blokkolják a fő alkalmazás folyamatot

## Kapcsolódó dokumentáció

- [Logger Interface](../interfaces/logger_interface.md)
- [Logger Factory](logger_factory.md)
- [Colored Logger](colored_logger.md)
- [Default Logger](default_logger.md)
- [Rotating File Logger](rotating_file_logger.md)