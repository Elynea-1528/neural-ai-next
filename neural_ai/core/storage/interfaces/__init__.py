"""Storage komponens interfészek.

Ez a csomag a tárolási réteg interfészeit tartalmazza, amelyek a különböző
tárolási megoldások egységes kezelését teszik lehetővé.

Az interfészek lehetővé teszik a függőség injektálást, ami a komponensek
laza csatolását és egyszerű tesztelését eredményezi.

Elérhető interfészek:
    - StorageInterface: Alapvető tárolási műveletek (mentés, betöltés, törlés)
    - StorageFactoryInterface: Tároló objektumok létrehozásáért felelős gyártó

Példa:
    >>> from neural_ai.core.storage.interfaces import StorageInterface
    >>> from neural_ai.core.config import ConfigInterface
    >>> from neural_ai.core.logger import LoggerInterface
    >>>
    >>> class MyStorage(StorageInterface):
    ...     def __init__(
    ...         self,
    ...         config: ConfigInterface,
    ...         logger: LoggerInterface
    ...     ):
    ...         self._config = config
    ...         self._logger = logger
    ...
    ...     def save(self, data: bytes, path: str) -> None:
    ...         # Implementáció
    ...         pass
"""

from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

__all__ = ["StorageInterface", "StorageFactoryInterface"]
