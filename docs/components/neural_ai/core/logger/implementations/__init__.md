# Logger Implementációk

## Áttekintés

Ez a modul exportálja a logger komponens implementációit, és biztosítja a központosított hozzáférést a különböző logger típusokhoz.

## Elérhető implementációk

### [`DefaultLogger`](default_logger.md)
Alapértelmezett logger implementáció a Python standard logging könyvtárával.

### [`ColoredLogger`](colored_logger.md)
Színes konzol kimenetű logger implementáció.

### [`RotatingFileLogger`](rotating_file_logger.md)
Fájl rotálást támogató logger implementáció.

## Gyors használat

### Alapértelmezett logger

```python
from neural_ai.core.logger.implementations import DefaultLogger

logger = DefaultLogger("my_app")
logger.info("Alkalmazás elindult")
```

### Színes logger

```python
from neural_ai.core.logger.implementations import ColoredLogger
import logging

logger = ColoredLogger("my_app", level=logging.DEBUG)
logger.info("Színes log üzenet")
```

### Fájl logger

```python
from neural_ai.core.logger.implementations import RotatingFileLogger

logger = RotatingFileLogger(
    name="my_app",
    log_file="/var/log/app.log",
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5
)
logger.info("Log fájlba írás")
```

## Logger Factory használata

```python
from neural_ai.core.logger import LoggerFactory

# Alapértelmezett logger
logger = LoggerFactory.get_logger("my_app")

# Színes logger
colored = LoggerFactory.get_logger("app", logger_type="colored")

# Fájl logger
file_logger = LoggerFactory.get_logger(
    "file_app",
    logger_type="rotating",
    log_file="/var/log/app.log"
)
```

## Log szintek

Minden logger támogatja a standard Python log szinteket:

- `DEBUG` (10): Részletes hibakeresési információk
- `INFO` (20): Általános információk
- `WARNING` (30): Figyelmeztetések
- `ERROR` (40): Hibák
- `CRITICAL` (50): Kritikus hibák

### Példa log szintekre

```python
from neural_ai.core.logger.implementations import DefaultLogger
import logging

logger = DefaultLogger("my_app", level=logging.DEBUG)

logger.debug("Hibakeresési információ")
logger.info("Sikeres művelet")
logger.warning("Figyelmeztető üzenet")
logger.error("Hiba történt")
logger.critical("Kritikus hiba")
```

## Komplex példa

```python
import logging
from neural_ai.core.logger.implementations import (
    DefaultLogger,
    ColoredLogger,
    RotatingFileLogger
)

# Több logger használata egyszerre
console_logger = DefaultLogger("console_app")
colored_logger = ColoredLogger("colored_app", level=logging.DEBUG)
file_logger = RotatingFileLogger(
    name="file_app",
    log_file="app.log",
    max_bytes=5*1024*1024,
    backup_count=3
)

# Különböző célokra különböző loggerek
console_logger.info("Felhasználói interfész esemény")
colored_logger.debug("Fejlesztői debug információ")
file_logger.info("Fontos esemény naplózása fájlba")

# Log szint módosítása futás közben
console_logger.set_level(logging.WARNING)
console_logger.debug("Ez az üzenet már nem jelenik meg")  # Nem lesz logolva
console_logger.warning("Ez még mindig látszik")

# Aktuális log szint lekérdezése
current_level = console_logger.get_level()
print(f"Aktuális log szint: {current_level}")
```

## Logger összehasonlítás

| Funkció | DefaultLogger | ColoredLogger | RotatingFileLogger |
|---------|---------------|---------------|-------------------|
| Konzol kimenet | ✓ | ✓ | ✗ |
| Színes kimenet | ✗ | ✓ | ✗ |
| Fájlba írás | ✗ | ✗ | ✓ |
| Automatikus rotáció | ✗ | ✗ | ✓ |
| Méret alapú rotáció | ✗ | ✗ | ✓ |
| Idő alapú rotáció | ✗ | ✗ | ✓ |
| Formázható | ✓ | ✓ | ✓ |

## Egyéni logger létrehozása

```python
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger import LoggerFactory
import logging

class CustomLogger(LoggerInterface):
    """Egyéni logger implementáció."""
    
    def __init__(self, name: str, **kwargs):
        self.logger = logging.getLogger(name)
        # Egyéni inicializálás
        pass
    
    def debug(self, message: str, **kwargs):
        # Egyéni debug implementáció
        pass
    
    def info(self, message: str, **kwargs):
        # Egyéni info implementáció
        pass
    
    def warning(self, message: str, **kwargs):
        # Egyéni warning implementáció
        pass
    
    def error(self, message: str, **kwargs):
        # Egyéni error implementáció
        pass
    
    def critical(self, message: str, **kwargs):
        # Egyéni critical implementáció
        pass
    
    def set_level(self, level: int):
        # Log szint beállítása
        pass
    
    def get_level(self) -> int:
        # Log szint lekérdezése
        return self.logger.level

# Egyéni logger regisztrálása
LoggerFactory.register_logger("custom", CustomLogger)

# Használat
custom_logger = LoggerFactory.get_logger("my_app", logger_type="custom")
```

## További információk

- [DefaultLogger Részletes Dokumentáció](default_logger.md)
- [ColoredLogger Részletes Dokumentáció](colored_logger.md)
- [RotatingFileLogger Részletes Dokumentáció](rotating_file_logger.md)
- [Logger Modul Áttekintés](../__init__.md)
- [Logger Factory](../factory.md)