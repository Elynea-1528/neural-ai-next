# Logger Kivételek

Ez a dokumentáció a logger komponens kivételkezelését mutatja be.

## Áttekintés

A [`neural_ai/core/logger/exceptions.py`](../../../../neural_ai/core/logger/exceptions.py) modul tartalmazza a logger komponenshez tartozó kivételeket. Ezek a kivételek a logger működése során fellépő különböző hibákat reprezentálják.

## Kivétel Hierarchia

```python
Exception
└── LoggerError
    ├── LoggerConfigurationError
    └── LoggerInitializationError
```

## Kivételek

### LoggerError

Az alap kivétel a logger komponenshez.

**Definíció:**
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

### LoggerConfigurationError

Logger konfigurációs hibákat jelzi.

**Definíció:**
```python
class LoggerConfigurationError(LoggerError):
    """Logger konfigurációs hiba."""
    pass
```

**Használat:**
```python
from neural_ai.core.logger.exceptions import LoggerConfigurationError

try:
    # Konfiguráció betöltése
    pass
except LoggerConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
```

### LoggerInitializationError

Logger inicializálási hibákat jelzi.

**Definíció:**
```python
class LoggerInitializationError(LoggerError):
    """Logger inicializálási hiba."""
    pass
```

**Használat:**
```python
from neural_ai.core.logger.exceptions import LoggerInitializationError

try:
    # Logger inicializálása
    pass
except LoggerInitializationError as e:
    print(f"Inicializálási hiba: {e}")
```

## Példák

### 1. Konfigurációs hiba kezelése

```python
from neural_ai.core.logger.exceptions import LoggerConfigurationError

def load_logger_config(config_path: str) -> dict:
    """Betölti a logger konfigurációt."""
    if not os.path.exists(config_path):
        raise LoggerConfigurationError(f"Konfigurációs fájl nem található: {config_path}")
    
    # Konfiguráció betöltése
    return config
```

### 2. Inicializálási hiba kezelése

```python
from neural_ai.core.logger.exceptions import LoggerInitializationError

def initialize_logger(config: dict) -> Logger:
    """Inicializálja a loggert."""
    try:
        logger = Logger(config)
        return logger
    except Exception as e:
        raise LoggerInitializationError(f"Logger inicializálása sikertelen: {e}")
```

### 3. Általános logger hiba kezelése

```python
from neural_ai.core.logger.exceptions import (
    LoggerError,
    LoggerConfigurationError,
    LoggerInitializationError
)

def setup_logger() -> Logger:
    """Beállítja a loggert."""
    try:
        config = load_logger_config("config.yaml")
        logger = initialize_logger(config)
        return logger
    except LoggerConfigurationError:
        # Konfigurációs hiba kezelése
        pass
    except LoggerInitializationError:
        # Inicializálási hiba kezelése
        pass
    except LoggerError:
        # Általános logger hiba kezelése
        pass
```

## Tesztelés

A kivételeket a [`tests/core/logger/test_exceptions.py`](../../../../tests/core/logger/test_exceptions.py) fájl teszteli.

### Tesztesetek

1. **LoggerError tesztelése**
   - Kivétel dobásának ellenőrzése
   - Hibaüzenet ellenőrzése
   - Öröklődés ellenőrzése

2. **LoggerConfigurationError tesztelése**
   - Kivétel dobásának ellenőrzése
   - Hibaüzenet ellenőrzése
   - Öröklődés ellenőrzése

3. **LoggerInitializationError tesztelése**
   - Kivétel dobásának ellenőrzése
   - Hibaüzenet ellenőrzése
   - Öröklődés ellenőrzése

### Futtatás

```bash
pytest tests/core/logger/test_exceptions.py -v
```

### Coverage

A tesztek 100% coverage-t biztosítanak a kivételekre.

## Kapcsolódó Dokumentáció

- [Logger komponens áttekintése](__init__.md)
- [Logger implementációk](../implementations/)
- [Logger interfészek](../interfaces/)
- [Fejlesztői dokumentáció](../../../development/error_handling.md)