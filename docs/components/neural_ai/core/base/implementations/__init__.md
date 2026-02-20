# neural_ai/core/base/implementations/__init__.py

Base komponensek implementációi.

Ez a modul tartalmazza a Neural AI Next base komponens rendszerének
összes implementációját, beleértve a DI konténert, lusta betöltést,
singleton mintát és komponens gyűjteményeket.

## Importok

```python
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.implementations.di_container import LazyComponent
from neural_ai.core.base.implementations.lazy_loader import LazyLoader
from neural_ai.core.base.implementations.lazy_loader import lazy_property
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.logger.factory import LoggerFactory
```

## Konstansok

- **`__all__`**
: `['DIContainer', 'LazyComponent', 'LazyLoader', 'lazy_property', 'SingletonMeta']`


- **`_logger`**
: `LoggerFactory.get_logger('neural_ai.core.base.implementations')`


---

**Forrásfájl:** [`neural_ai/core/base/implementations/__init__.py`](../../neural_ai/core/base/implementations/__init__.py)
