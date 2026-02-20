# neural_ai/core/base/__init__.py

Neural AI core komponensek alap modulja.

Ez a modul tartalmazza a core komponensek közös alapjait és a
dependency injection megvalósításához szükséges infrastruktúrát.

## Importok

```python
from typing import TYPE_CHECKING
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer
```

## Konstansok

- **`__all__`**
: `['DIContainer', 'CoreComponents', 'CoreComponentFactory']`


---

**Forrásfájl:** [`neural_ai/core/base/__init__.py`](../../neural_ai/core/base/__init__.py)
