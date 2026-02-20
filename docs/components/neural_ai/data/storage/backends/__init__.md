# neural_ai/data/storage/backends/__init__.py

Storage Backends Modul.

Ez a modul tartalmazza a tárolási backend-ek implementációit különböző
DataFrame könyvtárakhoz (Polars, Pandas). A backend-ek a Parquet formátumot
használják a hatékony adattároláshoz és támogatják a chunkolást és
aszinkron műveleteket.

## Importok

```python
from neural_ai.data.storage.backends.base import DataFrameType
from neural_ai.data.storage.backends.base import StorageBackend
from neural_ai.data.storage.backends.pandas_backend import PandasBackend
from neural_ai.data.storage.backends.polars_backend import PolarsBackend
```

## Konstansok

- **`__all__`**
: `['DataFrameType', 'StorageBackend', 'PandasBackend', 'PolarsBackend']`


---

**Forrásfájl:** [`neural_ai/data/storage/backends/__init__.py`](../../neural_ai/data/storage/backends/__init__.py)
