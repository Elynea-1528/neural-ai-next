"""Storage Backends Modul.

Ez a modul tartalmazza a tárolási backend-ek implementációit különböző
DataFrame könyvtárakhoz (Polars, Pandas). A backend-ek a Parquet formátumot
használják a hatékony adattároláshoz és támogatják a chunkolást és
aszinkron műveleteket.
"""

from neural_ai.core.storage.backends.base import DataFrameType, StorageBackend
from neural_ai.core.storage.backends.pandas_backend import PandasBackend
from neural_ai.core.storage.backends.polars_backend import PolarsBackend

__all__ = [
    "DataFrameType",
    "StorageBackend",
    "PandasBackend",
    "PolarsBackend",
]
