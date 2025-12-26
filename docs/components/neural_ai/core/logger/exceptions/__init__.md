# Logger Kivételek - Áttekintés

## Áttekintés

Ez a csomag tartalmazza a logger komponenshez tartozó kivételosztályokat.

## Elérhető kivételek

### [`LoggerError`](logger_error.md#loggererror)
Alap kivétel a logger komponenshez.

### [`LoggerConfigurationError`](logger_error.md#loggerconfigurationerror)
Logger konfigurációs hiba.

### [`LoggerInitializationError`](logger_error.md#loggerinitializationerror)
Logger inicializálási hiba.

## Használat

```python
from neural_ai.core.logger.exceptions import (
    LoggerError,
    LoggerConfigurationError,
    LoggerInitializationError
)

try:
    # Logger művelet
    logger = LoggerFactory.get_logger("my_app")
except LoggerInitializationError as e:
    print(f"Inicializálási hiba: {e}")
except LoggerConfigurationError as e:
    print(f"Konfigurációs hiba: {e}")
except LoggerError as e:
    print(f"Logger hiba: {e}")
```

## Kivétel hierarchia

```
Exception
└── LoggerError
    ├── LoggerConfigurationError
    └── LoggerInitializationError
```

## További információk

- [Részletes kivétel dokumentáció](logger_error.md)
- [Logger modul áttekintés](../__init__.md)