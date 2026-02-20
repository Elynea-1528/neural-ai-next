# neural_ai/core/logger/interfaces/__init__.py

Logger interfészek inicializáló modulja.

Ez a modul exportálja a logger komponens által definiált interfészeket,
és biztosítja a csomag verzióinformációinak dinamikus betöltését.
A TYPE_CHECKING blokk segítségével elkerüljük a körkörös importokat.

Verziókezelés:
    A modul automatikusan betölti a csomag verzióját a pyproject.toml-ból
    az importlib.metadata segítségével. Ez biztosítja, hogy a verzió
    mindig szinkronban legyen a projekt konfigurációjával.

Példa használat:
    >>> from neural_ai.core.logger.interfaces import (
    ...     LoggerInterface,
    ...     LoggerFactoryInterface,
    ...     __version__
    ... )
    >>> print(f"Logger interfész verzió: {__version__}")
    Logger interfész verzió: 1.0.0

## Importok

```python
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from typing import TYPE_CHECKING
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.interfaces.factory_interface import LoggerFactoryInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Konstansok

- **`__version__`**
: `version('neural-ai-next')`


- **`__version__`**
: `'1.0.0'`


- **`__all__`**
: `['LoggerInterface', 'LoggerFactoryInterface', '__version__']`


---

**Forrásfájl:** [`neural_ai/core/logger/interfaces/__init__.py`](../../neural_ai/core/logger/interfaces/__init__.py)
