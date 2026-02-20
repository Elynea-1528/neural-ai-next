# neural_ai/processors/dimensions/base.py

BaseDimensionProcessor - Absztrakt alap osztály minden dimenzió processzor számára.

## Importok

```python
from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING
from typing import Any
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `BaseDimensionProcessor(IDimensionProcessor, ABC)`

Absztrakt alap osztály minden dimenzió processzor számára.

Ez az osztály biztosítja a Dependency Injection támogatást és az alapvető
konfigurációs kezelést minden dimenzió processzor számára.

### Metódusok

#### `__init__()`

```python
def __init__(self, config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> None
```

Inicializálja a dimenzió processzort DI-val.

**Paraméterek:**

- **`self`**
- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `None`

#### `dimension_id()`

```python
def dimension_id(self) -> int
```

Dimenzió azonosító (1-15).

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `int`
- int: A dimenzió egyedi azonosítója

---

**Forrásfájl:** [`neural_ai/processors/dimensions/base.py`](../../neural_ai/processors/dimensions/base.py)
