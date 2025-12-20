"""MT5 Collector komponens.

Ez a csomag tartalmazza az MT5 Collector komponens összes osztályát és interfészét.

Author: Neural AI Team
Date: 2025-12-16
Version: 1.0.0
"""

# Import exceptions from error_handler and new MT5 exceptions
from .data_validator import DataValidator
from .dlq import DeadLetterQueue
from .error_handler import (
    CollectorError,
    ConfigurationError,
    DataQualityError,
    ErrorHandler,
    ValidationError,
)
from .exceptions import (
    MT5ConnectionError,
    MT5DataValidationError,
    MT5Exception,
    MT5InitializationError,
    MT5TimeoutError,
)

# Import implementations
from .implementations.collector_factory import CollectorFactory
from .implementations.mt5_collector import MT5Collector
from .implementations.storage.collector_storage import CollectorStorage

# Import interfaces
from .interfaces.collector_interface import CollectorInterface
from .interfaces.data_validator_interface import DataValidatorInterface

__all__ = [
    # Exceptions
    "CollectorError",
    "ValidationError",
    "ConfigurationError",
    "DataQualityError",
    "MT5Exception",
    "MT5ConnectionError",
    "MT5TimeoutError",
    "MT5DataValidationError",
    "MT5InitializationError",
    # Interfaces
    "CollectorInterface",
    "DataValidatorInterface",
    # Implementations
    "CollectorFactory",
    "MT5Collector",
    # DLQ
    "DeadLetterQueue",
    # Legacy components
    "DataValidator",
    "ErrorHandler",
    "CollectorStorage",
]
