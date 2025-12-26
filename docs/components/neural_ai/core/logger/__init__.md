# Logger Modul - Naplózási Rendszer

## Áttekintés

A Logger komponens fő inicializációs modulja, amely biztosítja a Neural-AI-Next rendszer naplózási funkcionalitását. Központi exportmodulként szolgál, amely összegyűjti és elérhetővé teszi a logger komponens összes fontos osztályát és interfészét.

## Fő komponensek

### Interfészek
- **[`LoggerInterface`](interfaces/logger_interface.md)**: A naplózási műveletek absztrakt definíciója
- **[`LoggerFactoryInterface`](interfaces/factory_interface.md)**: Logger factory interfész

### Implementációk
- **[`DefaultLogger`](implementations/default_logger.md)**: Alapértelmezett logger implementáció
- **[`ColoredLogger`](implementations/colored_logger.md)**: Színes konzol kimenetű logger
- **[`RotatingFileLogger`](implementations/rotating_file_logger.md)**: Fájl rotálást támogató logger
- **[`LoggerFactory`](factory.md)**: Logger példányok létrehozásáért felelős gyár

### Kivételek
- **[`LoggerError`](exceptions/logger_error.md)**: Alap kivétel a logger komponenshez
- **[`LoggerConfigurationError`](exceptions/logger_error.md#loggerconfigurationerror)**: Logger konfigurációs hiba
- **[`LoggerInitializationError`](exceptions/logger_error.md#loggerinitializationerror)**: Logger inicializálási hiba

### Formázók
- **[`ColoredFormatter`](formatters/logger_formatters.md)**: Színes megjelenítést biztosító formatter

## Verzióinformációk

A modul verzióinformációkat tartalmaz:

```python
from neural_ai.core.logger import __version__, __schema_version__

print(f"Logger verzió: {__version__}")
print(f"Séma verzió: {__schema_version__}")
```

## Gyors használat

### Alapértelmezett logger

```python
from neural_ai.core.logger import DefaultLogger

# Logger létrehozása
logger = DefaultLogger("my_app")

# Különböző szintű üzenetek logolása
logger.debug("Hibakeresési információ")
logger.info("Alkalmazás indítása...")
logger.warning("Figyelmeztetés")
logger.error("Hiba történt")
logger.critical("Kritikus hiba")
```

### Színes logger

```python
from neural_ai.core.logger import ColoredLogger
import logging

# Színes logger létrehozása
logger = ColoredLogger("my_app", level=logging.DEBUG)
logger.info("Színes log üzenet")
```

### Fájl logger

```python
from neural_ai.core.logger import RotatingFileLogger

# Fájlba író logger
logger = RotatingFileLogger(
    name="my_app",
    log_file="/var/log/my_app.log",
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5
)
logger.info("Log üzenet fájlba")
```

### Factory használata

```python
from neural_ai.core.logger import LoggerFactory

# Alapértelmezett logger
logger = LoggerFactory.get_logger("my_app")

# Színes logger
colored_logger = LoggerFactory.get_logger("my_app", logger_type="colored")

# Fájl logger
file_logger = LoggerFactory.get_logger(
    "my_app",
    logger_type="rotating",
    log_file="/var/log/app.log"
)
```

## Konfiguráció

A logger rendszer konfigurálható dictionary alapú konfigurációval:

```python
from neural_ai.core.logger import LoggerFactory

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

## Modul szerkezete

```
neural_ai/core/logger/
├── interfaces/              # Interfészek
│   ├── logger_interface.py      # Logger alapinterfész
│   └── factory_interface.py     # Factory interfész
├── implementations/         # Implementációk
│   ├── default_logger.py        # Alap logger
│   ├── colored_logger.py        # Színes logger
│   └── rotating_file_logger.py  # Fájl logger
├── formatters/              # Formázók
│   └── logger_formatters.py     # Színes formázó
├── exceptions/              # Kivételek
│   └── logger_error.py          # Logger kivételek
└── factory.py               # Logger factory
```

## Log szintek

A logger támogatja a standard Python log szinteket:

- `DEBUG` (10): Részletes hibakeresési információk
- `INFO` (20): Általános információk a rendszer működéséről
- `WARNING` (30): Figyelmeztetések
- `ERROR` (40): Hibák, amelyek befolyásolják a működést
- `CRITICAL` (50): Kritikus hibák, amelyek leállást okozhatnak

## További információk

- [Logger Factory](factory.md)
- [Logger Implementációk](implementations/__init__.md)
- [Logger Interfészek](interfaces/__init__.md)
- [Logger Kivételek](exceptions/logger_error.md)
- [Logger Formázók](formatters/logger_formatters.md)