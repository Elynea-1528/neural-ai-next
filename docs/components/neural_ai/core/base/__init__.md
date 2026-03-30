# neural_ai/core/base/__init__.py

Neural AI core komponensek alap modulja.

Ez a modul tartalmazza a core komponensek közös alapjait és a
dependency injection megvalósításához szükséges infrastruktúrát.

## Importok

```python
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.interfaces import CoreComponentFactoryInterface
from neural_ai.core.base.interfaces import CoreComponentsInterface
from neural_ai.core.base.interfaces import DIContainerInterface
from neural_ai.core.base.interfaces import LazyComponentInterface
```

## Konstansok

- **`__all__`**
: `['CoreComponentFactory', 'CoreComponentFactoryInterface', 'CoreComponentsInterface', 'DIContainerInterface', 'LazyComponentInterface']`


---

**Forrásfájl:** [`neural_ai/core/base/__init__.py`](../../neural_ai/core/base/__init__.py)
