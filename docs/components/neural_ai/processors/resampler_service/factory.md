# neural_ai/processors/resampler_service/factory.py

ResamplerService Factory - A ResamplerService létrehozásáért felelős.

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.processors.resampler_service.implementations.resampler_service import ResamplerService
from neural_ai.processors.resampler_service.interfaces.resampler_interface import ResamplerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.logger.factory import LoggerFactory
from neural_ai.data.storage.factory import StorageFactory
```

## Osztály: `ResamplerServiceFactory`

Factory osztály a ResamplerService létrehozásához és kezeléséhez.

### Metódusok

#### `create()`

```python
def create(storage: 'StorageInterface', logger: 'LoggerInterface') -> ResamplerInterface
```

ResamplerService példány létrehozása.

**Paraméterek:**

- **`storage`** (`'StorageInterface'`): A tárolási interfész példány
- **`logger`** (`'LoggerInterface'`): A naplózási interfész

**Visszatérési érték:**

- Típus: `ResamplerInterface`
- ResamplerInterface: A létrehozott ResamplerService példány

#### `get_instance()`

```python
def get_instance(cls) -> ResamplerInterface
```

ResamplerService példány lekérdezése a DI konténerből.

**Paraméterek:**

- **`cls`**

**Visszatérési érték:**

- Típus: `ResamplerInterface`
- ResamplerInterface: A ResamplerService példány

**Kivételek:**

- **`ComponentNotFoundError`**: Ha a komponens nem található a konténerben

---

**Forrásfájl:** [`neural_ai/processors/resampler_service/factory.py`](../../neural_ai/processors/resampler_service/factory.py)
