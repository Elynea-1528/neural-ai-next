"""Neural AI core komponensek alap modulja.

Ez a modul tartalmazza a core komponensek közös alapjait és a
dependency injection megvalósításához szükséges infrastruktúrát.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.base.container import DIContainer
    from neural_ai.core.base.core_components import CoreComponents
    from neural_ai.core.base.factory import CoreComponentFactory

from neural_ai.core.base.container import DIContainer
from neural_ai.core.base.core_components import CoreComponents
from neural_ai.core.base.factory import CoreComponentFactory

__all__ = ["DIContainer", "CoreComponents", "CoreComponentFactory"]
