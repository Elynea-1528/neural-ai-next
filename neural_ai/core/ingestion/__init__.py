"""Ingestion komponensek.

Ez a modul a rendszer adatbetöltési (ingestion) komponenseit tartalmazza,
beleértve a MarketDataPersister-t, amely felelős a bejövő market data
eventek bufferezéséért és időzített mentéséért a Parquet tárolóba.

Author: Neural AI Next Team
Version: 1.0.0
"""

from neural_ai.core.ingestion.market_data_persister import MarketDataPersister

__all__ = ["MarketDataPersister"]
