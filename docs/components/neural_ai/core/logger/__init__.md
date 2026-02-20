# neural_ai/core/logger/__init__.py

Logger komponens fő inicializációs modulja.

Ez a modul biztosítja a Neural-AI-Next rendszer naplózási funkcionalitását.
Központi exportmodulként szolgál, amely összegyűjti és elérhetővé teszi
a logger komponens összes fontos osztályát és interfészét.

A modul a következő fő komponenseket exportálja:
    - Interfészek: LoggerInterface, LoggerFactoryInterface
    - Implementációk: ColoredLogger, DefaultLogger, LoggerFactory, RotatingFileLogger
    - Kivételek: LoggerError, LoggerConfigurationError, LoggerInitializationError

Verziókezelés:
    A modul importálja a projekt verzióinformációit a fő neural_ai csomagból,
    és biztosítja a konfigurációs séma verzióját a kompatibilitás ellenőrzéséhez.

Példa használatra:
    >>> from neural_ai.core.logger import LoggerFactory, DefaultLogger
    >>> logger = DefaultLogger()
    >>> logger.info("Alkalmazás indítása...")
    >>> print(f"Logger verzió: {__version__}")

## Importok

```python
from importlib import metadata
from typing import TYPE_CHECKING
from typing import Final
from neural_ai.core.logger.exceptions import LoggerConfigurationError
from neural_ai.core.logger.exceptions import LoggerError
from neural_ai.core.logger.exceptions import LoggerInitializationError
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.core.logger.implementations import ColoredLogger
from neural_ai.core.logger.implementations import DefaultLogger
from neural_ai.core.logger.implementations import RotatingFileLogger
# ... és még 12 import
```

## Konstansok

- **`_version`**
: `'1.0.0'`


### `_get_schema_version()`

```python
def _get_schema_version() -> str
```

**Visszatérési érték:**

- Típus: `str`

---

**Forrásfájl:** [`neural_ai/core/logger/__init__.py`](../../neural_ai/core/logger/__init__.py)
