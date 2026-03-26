"""Neural AI core komponensek alap modulja.

Ez a modul tartalmazza a core komponensek közös alapjait és a
dependency injection megvalósításához szükséges infrastruktúrát.
"""

from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.interfaces import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
    DIContainerInterface,
    LazyComponentInterface,
)

__all__ = [
    "CoreComponentFactory",
    "CoreComponentFactoryInterface",
    "CoreComponentsInterface",
    "DIContainerInterface",
    "LazyComponentInterface",
]
