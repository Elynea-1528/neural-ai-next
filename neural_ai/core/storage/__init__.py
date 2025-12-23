"""Neural AI storage komponens.

Ez a modul a storage komponens fő exportjait tartalmazza, beleértve a FileStorage
és StorageFactory osztályokat, valamint a hozzájuk tartozó interfészeket és típusokat.

A modul támogatja a függőség injektálást (Dependency Injection) a logger és config
komponensek számára, így elkerülve a körkörös importproblémákat.
"""

from importlib import metadata
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.implementations.file_storage import FileStorage
    from neural_ai.core.storage.implementations.storage_factory import StorageFactory
    from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

from neural_ai.core.storage.implementations import FileStorage, StorageFactory

# Dinamikus verzióbetöltés a pyproject.toml-ból
try:
    _version: str = metadata.version("neural-ai-next")
except metadata.PackageNotFoundError:
    # Fallback verzió, ha a csomag nincs telepítve
    _version = "1.0.0"

__version__: Final[str] = _version

# Konfigurációs séma verzió - a 10. fejezet szerint
__schema_version__: Final[str] = "1.0"

__all__: Final[list[str]] = [
    # Verzióinformációk
    "__version__",
    "__schema_version__",
    # Implementációk
    "FileStorage",
    "StorageFactory",
    # Interfészek
    "StorageInterface",
    "StorageFactoryInterface",
    # Típusok
    "LoggerInterface",
    "ConfigManagerInterface",
]
