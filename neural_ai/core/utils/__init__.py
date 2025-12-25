"""Core segédfunkciók és utility osztályok.

Ez a csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit,
beleértve a hardver detekciót, típuskonverziókat és egyéb általános célú
eszközöket.
"""

from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

__all__ = [
    "HardwareFactory",
    "HardwareInterface",
]
