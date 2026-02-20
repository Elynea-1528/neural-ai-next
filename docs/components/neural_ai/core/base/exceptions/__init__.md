# neural_ai/core/base/exceptions/__init__.py

Kivételek modul a Neural AI Next projektben.

Ez a modul exportálja az összes alap és specifikus kivétel osztályt,
amelyeket a rendszer különböző komponensei használnak.

## Importok

```python
from base_error import ComponentNotFoundError
from base_error import ConfigurationError
from base_error import ConnectionError
from base_error import DependencyError
from base_error import InsufficientDiskSpaceError
from base_error import NetworkException
from base_error import NeuralAIException
from base_error import PermissionDeniedError
from base_error import SingletonViolationError
from base_error import StorageException
# ... és még 4 import
```

## Konstansok

- **`__all__`**
: `['NeuralAIException', 'StorageException', 'StorageWriteError', 'StorageReadError', 'StoragePermissionError', 'ConfigurationError', 'DependencyError', 'SingletonViolationError', 'ComponentNotFoundError', 'NetworkException', 'TimeoutError', 'ConnectionError', 'InsufficientDiskSpaceError', 'PermissionDeniedError']`


---

**Forrásfájl:** [`neural_ai/core/base/exceptions/__init__.py`](../../neural_ai/core/base/exceptions/__init__.py)
