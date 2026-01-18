"""Base komponensek implementációi.

Ez a modul tartalmazza a Neural AI Next base komponens rendszerének
összes implementációját, beleértve a DI konténert, lusta betöltést,
singleton mintát és komponens gyűjteményeket.
"""

from neural_ai.core.base.implementations.di_container import DIContainer, LazyComponent
from neural_ai.core.base.implementations.lazy_loader import LazyLoader, lazy_property
from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.logger.factory import LoggerFactory

__all__ = [
    "DIContainer",
    "LazyComponent",
    "LazyLoader",
    "lazy_property",
    "SingletonMeta",
]

_logger = LoggerFactory.get_logger("neural_ai.core.base.implementations")
_logger.info(
    "Base implementations module initialized",
    extra={"module": "neural_ai.core.base.implementations"},
)
