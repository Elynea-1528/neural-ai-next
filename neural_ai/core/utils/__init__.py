"""Core segédfunkciók és utility osztályok.

Ez a csomag tartalmazza a Neural AI Next rendszer alapvető segédfunkcióit,
beleértve a hardver detekciót, típuskonverziókat és egyéb általános célú
eszközöket.

DDD Szabály:
    Csak Interface + Factory exportáltak.
    Az implementációk (HardwareInfo) és utility függvények (trace, decorators)
    NEM exportáltak - közvetlenül a megfelelő modulból kell importálni őket.

Példa:
    >>> from neural_ai.core.utils import HardwareFactory
    >>> hw = HardwareFactory.create()
    >>> # Ha trace kell:
    >>> from neural_ai.core.utils.decorators import trace
"""

from neural_ai.core.utils.exceptions import HardwareDetectionError, UtilError
from neural_ai.core.utils.factory import HardwareFactory
from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

__all__ = [
    # Interface
    "HardwareInterface",
    # Factory
    "HardwareFactory",
    # Exceptions
    "UtilError",
    "HardwareDetectionError",
]
