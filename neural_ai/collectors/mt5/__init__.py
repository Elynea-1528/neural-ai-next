"""MetaTrader 5 adatgyűjtő komponens.

Ez a modul biztosítja a kapcsolatot a MetaTrader 5 platformmal és az onnan származó
pénzügyi adatok gyűjtését, validálását és tárolását.

Főbb komponensek:
- MT5Collector: Fő adatgyűjtő osztály
- MT5Connection: MT5 kapcsolatkezelő
- DataValidator: Adatvalidátor
- Különböző kivételosztályok
"""

from .collector import (
    ConfigurationError,
    DataFetchError,
    MT5Collector,
    MT5CollectorError,
    MT5ConnectionError,
    ValidationError,
)
from .connection import MT5Connection
from .validator import DataValidator

__all__ = [
    "MT5Collector",
    "MT5Connection",
    "DataValidator",
    "MT5CollectorError",
    "MT5ConnectionError",
    "DataFetchError",
    "ValidationError",
    "ConfigurationError",
]
