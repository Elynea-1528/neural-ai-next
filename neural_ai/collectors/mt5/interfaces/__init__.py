"""MT5 Collector interfészek.

Ez a csomag tartalmazza az MT5 Collector komponens interfészeit.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

from .collector_interface import CollectorInterface
from .data_validator_interface import DataValidatorInterface

__all__ = [
    "CollectorInterface",
    "DataValidatorInterface",
]
