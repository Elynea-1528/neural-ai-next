"""Base komponens interfészek.

Ez a modul tartalmazza a Neural AI Next base komponens rendszerének
összes interfészét és absztrakt osztályát.
"""

from neural_ai.core.base.interfaces.component_interface import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
)
from neural_ai.core.base.interfaces.container_interface import (
    DIContainerInterface,
    LazyComponentInterface,
)

__all__ = [
    "DIContainerInterface",
    "LazyComponentInterface",
    "CoreComponentsInterface",
    "CoreComponentFactoryInterface",
]
