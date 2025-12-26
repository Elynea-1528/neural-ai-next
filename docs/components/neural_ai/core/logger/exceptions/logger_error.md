# Logger Kivételek

## Áttekintés

Ez a modul tartalmazza a logger komponenshez tartozó kivételeket.

## Kivétel osztályok

### `LoggerError`

Alap kivétel a logger komponenshez.

```python
class LoggerError(Exception):
    """Alap kivétel a logger komponenshez."""
    
    pass
```

**Használat:**

```python
from neural_ai.core.logger.exceptions import LoggerError

try:
    # Logger művelet
    pass
except LoggerError as e:
    print(f"Logger hiba: {e}")
```

### `LoggerConfigurationError`

Logger konfigurációs hiba.

```python
class LoggerConfigurationError(LoggerError):
    """Logger konfigurációs hiba."""
    
    pass
```

**Használat:**

```python
from neural_ai.core.logger.exceptions import LoggerConfigurationError
from neural_ai.core.logger import LoggerFactory

try:
    # Érvénytelen konfiguráció
    LoggerFactory.configure({
        'default_level': 'INVALID_LEVEL'  # Érvénytelen log szint
    })
except LoggerConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
```

### `LoggerInitializationError`

Logger inicializálási hiba.

```python
class LoggerInitializationError(LoggerError):
    """Logger inicializálási hiba."""
    
    pass
```

**Használat:**

```python
from neural_ai.core.logger.exceptions import LoggerInitializationError
from neural_ai.core.logger import LoggerFactory

try:
    # Rotating logger létrehozása log_file nélkül
    logger = LoggerFactory.get_logger("my_app", logger_type="rotating")
    # Ez hibát okoz, mert a rotating loggerhez kötelező a log_file
except LoggerInitializationError as e:
    print(f"Inicializálási hiba: {e}")
```

## Kivétel kezelés

### Általános hibakezelés

```python
from neural_ai.core.logger.exceptions import (
    LoggerError,
    LoggerConfigurationError,
    LoggerInitializationError
)
from neural_ai.core.logger import LoggerFactory

try:
    # Logger konfiguráció
    LoggerFactory.configure({'default_level': 'INFO'})
    
    # Logger létrehozása
    logger = LoggerFactory.get_logger("my_app")
    
    # Logger használata
    logger.info("Teszt üzenet")
    
except LoggerInitializationError as e:
    # Inicializálási hibák kezelése
    print(f"Inicializálási hiba: {e}")
    # Alternatív megoldás
    logger = LoggerFactory.get_logger("my_app", logger_type="default")
    
except LoggerConfigurationError as e:
    # Konfigurációs hibák kezelése
    print(f"Konfigurációs hiba: {e}")
    # Alapértelmezett konfiguráció betöltése
    
except LoggerError as e:
    # Általános logger hibák kezelése
    print(f"Logger hiba: {e}")
```

### Egyéni hibakezelő

```python
from neural_ai.core.logger.exceptions import LoggerError
import logging

class LoggerErrorHandler:
    """Egyéni hibakezelő a logger kivételekhez."""
    
    def __init__(self, fallback_logger):
        self.fallback_logger = fallback_logger
    
    def handle_error(self, error: LoggerError, context: str = ""):
        """Logger hiba kezelése.
        
        Args:
            error: A kezelendő kivétel
            context: A hiba kontextusa
        """
        if isinstance(error, LoggerInitializationError):
            self.fallback_logger.warning(
                f"Inicializálási hiba: {error}",
                context=context
            )
            # Alternatív logger használata
            self._use_fallback_logger()
            
        elif isinstance(error, LoggerConfigurationError):
            self.fallback_logger.error(
                f"Konfigurációs hiba: {error}",
                context=context
            )
            # Alapértelmezett konfiguráció betöltése
            self._load_default_config()
            
        else:
            self.fallback_logger.critical(
                f"Ismeretlen logger hiba: {error}",
                context=context
            )
    
    def _use_fallback_logger(self):
        """Átváltás tartalék loggerre."""
        # Implementáció
        pass
    
    def _load_default_config(self):
        """Alapértelmezett konfiguráció betöltése."""
        # Implementáció
        pass

# Használat
error_handler = LoggerErrorHandler(fallback_logger)

try:
    # Logger művelet
    pass
except LoggerError as e:
    error_handler.handle_error(e, context="Logger inicializálás")
```

### Hibajelentés

```python
from neural_ai.core.logger.exceptions import LoggerError

def create_logger_safe(name: str, logger_type: str = "default", **kwargs):
    """Biztonságos logger létrehozás hibakezeléssel.
    
    Args:
        name: A logger neve
        logger_type: A logger típusa
        **kwargs: További paraméterek
        
    Returns:
        Logger vagy None ha hiba történt
    """
    from neural_ai.core.logger import LoggerFactory
    
    try:
        logger = LoggerFactory.get_logger(name, logger_type, **kwargs)
        return logger
    except LoggerError as e:
        print(f"Hiba a logger létrehozásakor: {e}")
        # Naplózás vagy más hibakezelés
        return None

# Használat
logger = create_logger_safe("my_app", logger_type="rotating", log_file="app.log")
if logger:
    logger.info("Sikeres inicializálás")
else:
    print("Nem sikerült létrehozni a loggert")
```

## Kivétel láncolás

A kivételek hierarchiája lehetővé teszi a specifikusabb hibakezelést:

```python
from neural_ai.core.logger.exceptions import (
    LoggerError,
    LoggerConfigurationError,
    LoggerInitializationError
)

def process_logger_request(request):
    """Logger kérés feldolgozása."""
    try:
        # Feldolgozás
        if request.get('type') == 'rotating' and not request.get('log_file'):
            raise LoggerInitializationError("A rotating loggerhez kötelező a log_file")
        
        # További feldolgozás
        return True
        
    except LoggerInitializationError:
        # Csak inicializálási hibák
        raise
    except LoggerConfigurationError:
        # Csak konfigurációs hibák
        raise
    except LoggerError:
        # Minden más logger hiba
        raise
```

## Tesztelés

```python
import pytest
from neural_ai.core.logger.exceptions import (
    LoggerError,
    LoggerConfigurationError,
    LoggerInitializationError
)

def test_logger_initialization_error():
    """Teszteli a LoggerInitializationError kivételt."""
    with pytest.raises(LoggerInitializationError) as exc_info:
        # Olyan művelet, ami inicializálási hibát okoz
        pass
    
    assert "inicializálás" in str(exc_info.value).lower()

def test_logger_configuration_error():
    """Teszteli a LoggerConfigurationError kivételt."""
    with pytest.raises(LoggerConfigurationError):
        # Olyan művelet, ami konfigurációs hibát okoz
        pass

def test_logger_error_hierarchy():
    """Teszteli a kivétel hierarchiát."""
    assert issubclass(LoggerConfigurationError, LoggerError)
    assert issubclass(LoggerInitializationError, LoggerError)
```

## További információk

- [Logger Kivételek Áttekintés](__init__.md)
- [Logger Modul](../__init__.md)
- [Logger Factory](../factory.md)