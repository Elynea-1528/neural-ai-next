"""
JForex Collector Interfaces.

Ez a csomag tartalmazza a JForex adatgyűjtő komponensek interfészeit.
"""

from .live_interface import ILiveFeed

__all__ = [
    'ILiveFeed',
]