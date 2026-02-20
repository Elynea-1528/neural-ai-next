# neural_ai/processors/dimensions/d01_price/factory.py

D01PriceProcessor Factory - Az alap adatok processzor létrehozásáért felelős.

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.processors.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
```

## Osztály: `D01PriceFactory`

Factory osztály a D01PriceProcessor létrehozásához.

### Metódusok

#### `create()`

```python
def create(config: 'ConfigManagerInterface', logger: 'LoggerInterface') -> IDimensionProcessor
```

D01PriceProcessor példány létrehozása.

**Paraméterek:**

- **`config`** (`'ConfigManagerInterface'`): Konfigurációs menedzser interfész
- **`logger`** (`'LoggerInterface'`): Logger interfész

**Visszatérési érték:**

- Típus: `IDimensionProcessor`
- IDimensionProcessor: A D01PriceProcessor példány

---

**Forrásfájl:** [`neural_ai/processors/dimensions/d01_price/factory.py`](../../neural_ai/processors/dimensions/d01_price/factory.py)
