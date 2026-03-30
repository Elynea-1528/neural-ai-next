# neural_ai/core/base/exceptions/__init__.py

Kivételek modul a Neural AI Next projektben.

Ez a modul exportálja az összes alap és specifikus kivétel osztályt,
amelyeket a rendszer különböző komponensei használnak.

## Importok

```python
from neural_ai.core.base.exceptions.base_error import ComponentNotFoundError
from neural_ai.core.base.exceptions.base_error import ConfigurationError
from neural_ai.core.base.exceptions.base_error import ConnectionError
from neural_ai.core.base.exceptions.base_error import DependencyError
from neural_ai.core.base.exceptions.base_error import InsufficientDiskSpaceError
from neural_ai.core.base.exceptions.base_error import NetworkException
from neural_ai.core.base.exceptions.base_error import NeuralAIException
from neural_ai.core.base.exceptions.base_error import PermissionDeniedError
from neural_ai.core.base.exceptions.base_error import SingletonViolationError
from neural_ai.core.base.exceptions.base_error import StorageException
# ... és még 4 import
```

## Konstansok

- **`__all__`**
: `['NeuralAIException', 'StorageException', 'StorageWriteError', 'StorageReadError', 'StoragePermissionError', 'ConfigurationError', 'DependencyError', 'SingletonViolationError', 'ComponentNotFoundError', 'NetworkException', 'TimeoutError', 'ConnectionError', 'InsufficientDiskSpaceError', 'PermissionDeniedError']`


---

**Forrásfájl:** [`neural_ai/core/base/exceptions/__init__.py`](../../neural_ai/core/base/exceptions/__init__.py)
