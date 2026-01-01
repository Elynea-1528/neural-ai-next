"""JForex Collector module for Dukascopy .bi5 data download."""

from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader

__all__ = [
    "JForexFactory",
    "IJForexDownloader",
]
