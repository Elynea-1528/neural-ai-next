"""JForex Collector Interfaces.

Ez a csomag tartalmazza a JForex adatgyűjtő komponensek interfészeit.
"""

from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.collectors.jforex.interfaces.tick_data import TickData

__all__ = [
    "IJForexDownloader",
    "ILiveFeed",
    "TickData",
]
