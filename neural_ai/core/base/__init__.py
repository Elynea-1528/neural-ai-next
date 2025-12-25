"""Neural AI core komponensek alap modulja.

Ez a modul tartalmazza a core komponensek közös alapjait és a
dependency injection megvalósításához szükséges infrastruktúrát.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.base.factory import CoreComponentFactory
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.base.implementations.di_container import DIContainer

from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.component_bundle import CoreComponents
from neural_ai.core.base.implementations.di_container import DIContainer

__all__ = ["DIContainer", "CoreComponents", "CoreComponentFactory"]
