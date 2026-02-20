# neural_ai/processors/dimensions/d02_support/factory.py

D02SupportProcessor Factory - A Support/Resistance processzor létrehozásáért felelős.

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import D02SupportProcessor
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `D02SupportFactory`

Factory osztály a D02SupportProcessor létrehozásához.

### Metódusok

#### `create()`

```python
def create(config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> IDimensionProcessor
```

D02SupportProcessor példány létrehozása.

**Paraméterek:**

- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `IDimensionProcessor`
- IDimensionProcessor: A D02SupportProcessor példány

---

**Forrásfájl:** [`neural_ai/processors/dimensions/d02_support/factory.py`](../../neural_ai/processors/dimensions/d02_support/factory.py)
