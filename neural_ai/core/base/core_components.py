"""Core komponensek gyűjtemény."""

from dataclasses import dataclass
from typing import Optional

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


@dataclass
class CoreComponents:
    """Core komponensek gyűjteménye.

    Ez az osztály tartalmazza a rendszer core komponenseinek referenciáit
    és biztosítja a központi hozzáférést hozzájuk.
    """

    config: Optional[ConfigManagerInterface] = None
    logger: Optional[LoggerInterface] = None
    storage: Optional[StorageInterface] = None

    def has_config(self) -> bool:
        """Ellenőrzi, hogy van-e config komponens.

        Returns:
            bool: True ha van config komponens, False ha nincs
        """
        return self.config is not None

    def has_logger(self) -> bool:
        """Ellenőrzi, hogy van-e logger komponens.

        Returns:
            bool: True ha van logger komponens, False ha nincs
        """
        return self.logger is not None

    def has_storage(self) -> bool:
        """Ellenőrzi, hogy van-e storage komponens.

        Returns:
            bool: True ha van storage komponens, False ha nincs
        """
        return self.storage is not None

    def validate(self) -> bool:
        """Ellenőrzi, hogy minden szükséges komponens megvan-e.

        Returns:
            bool: True ha minden komponens megvan, False ha valamelyik hiányzik
        """
        return all([self.has_config(), self.has_logger(), self.has_storage()])
