# neural_ai/__init__.py

Neural-AI-Next projekt fő inicializációs modulja.

Ez a modul felelős a projekt verzióinformációinak és alapvető konfigurációjának
exportálásáért. A verziószámot dinamikusan tölti be a pyproject.toml fájlból
az importlib.metadata segítségével.

Attributes:
    __version__: A projekt aktuális verziószáma string formátumban.
    __schema_version__: A konfigurációs séma verziószáma a kompatibilitás
        ellenőrzéséhez.

Példa:
    >>> import neural_ai
    >>> print(f"Neural-AI-Next verzió: {neural_ai.__version__}")
    Neural-AI-Next verzió: 1.0.0

## Importok

```python
from importlib import metadata
from typing import Final
from neural_ai.core.logger.factory import LoggerFactory
```

## Konstansok

- **`_version`**
: `'1.0.0'`


- **`_logger`**
: `LoggerFactory.get_logger('neural_ai')`


---

**Forrásfájl:** [`neural_ai/__init__.py`](../../neural_ai/__init__.py)
