# neural_ai/core/utils/__init__.py

Core segédfunkciók és utility osztályok.

Ez a csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit,
beleértve a hardver detekciót, típuskonverziókat és egyéb általános célú
eszközöket.

DDD Szabály:
    Csak Interface + Factory exportáltak.
    Az implementációk (HardwareInfo) és utility függvények (trace, decorators)
    NEM exportáltak - közvetlenül a megfelelő modulból kell importálni őket.

Példa:
    >>> from neural_ai.core.utils import HardwareFactory
    >>> hw = HardwareFactory.create()
    >>> # Ha trace kell:
    >>> from neural_ai.core.utils.decorators import trace

## Importok

```python
from neural_ai.core.utils.exceptions import HardwareDetectionError
from neural_ai.core.utils.exceptions import UtilError
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
```

## Konstansok

- **`__all__`**
: `['HardwareInterface', 'HardwareFactory', 'UtilError', 'HardwareDetectionError']`


---

**Forrásfájl:** [`neural_ai/core/utils/__init__.py`](../../neural_ai/core/utils/__init__.py)
