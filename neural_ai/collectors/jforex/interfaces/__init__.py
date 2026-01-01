"""JForex Collector Interfaces.

Ez a csomag tartalmazza a JForex adatgyűjtő komponensek interfészeit.
"""

from .downloader_interface import IJForexDownloader
from .live_interface import ILiveFeed
from .tick_data import TickData

__all__ = [
    "IJForexDownloader",
    "ILiveFeed",
    "TickData",
]
