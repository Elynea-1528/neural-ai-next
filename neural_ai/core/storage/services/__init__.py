"""Storage services modul.

Ez a modul a tárolási szolgáltatásokat tartalmazza, amelyek összekötik
az EventBus-t a Storage-al.

Author: Neural AI Next Team
Version: 1.0.0
"""

from neural_ai.core.storage.services.market_data_persister import MarketDataPersister

__all__ = [
    "MarketDataPersister",
]