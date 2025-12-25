"""Core komponens interfészek.

Ez a modul tartalmazza a core komponensekhez kapcsolódó interfészeket.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from neural_ai.core.base.interfaces.container_interface import DIContainerInterface

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class CoreComponentsInterface(ABC):
    """Core komponensek interfész.

    Ez az interfész definiálja a core komponensek gyűjteményének
    alapvető funkcionalitását és hozzáférését.
    """

    @property
    @abstractmethod
    def config(self) -> "ConfigManagerInterface | None":
        """Konfiguráció kezelő komponens.

        Returns:
            A konfiguráció kezelő komponens vagy None
        """
        pass

    @property
    @abstractmethod
    def logger(self) -> "LoggerInterface | None":
        """Logger komponens.

        Returns:
            A logger komponens vagy None
        """
        pass

    @property
    @abstractmethod
    def storage(self) -> "StorageInterface | None":
        """Storage komponens.

        Returns:
            A storage komponens vagy None
        """
        pass

    @abstractmethod
    def has_config(self) -> bool:
        """Ellenőrzi, hogy van-e konfigurációs komponens.

        Returns:
            True ha van konfigurációs komponens, különben False
        """
        pass

    @abstractmethod
    def has_logger(self) -> bool:
        """Ellenőrzi, hogy van-e logger komponens.

        Returns:
            True ha van logger komponens, különben False
        """
        pass

    @abstractmethod
    def has_storage(self) -> bool:
        """Ellenőrzi, hogy van-e storage komponens.

        Returns:
            True ha van storage komponens, különben False
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

        Returns:
            True ha minden komponens elérhető, különben False
        """
        pass


class CoreComponentFactoryInterface(ABC):
    """Core komponens factory interfész.

    Ez az interfész definiálja a core komponensek létrehozásáért
    és inicializálásáért felelős factory osztály alapvető funkcionalitását.
    """

    @staticmethod
    @abstractmethod
    def create_components(
        config_path: str | None = None,
        log_path: str | None = None,
        storage_path: str | None = None,
    ) -> CoreComponentsInterface:
        """Core komponensek létrehozása és inicializálása.

        Args:
            config_path: Konfiguráció útvonala (opcionális)
            log_path: Log fájl útvonala (opcionális)
            storage_path: Storage alap útvonal (opcionális)

        Returns:
            Az inicializált komponensek
        """
        pass

    @staticmethod
    @abstractmethod
    def create_with_container(container: DIContainerInterface) -> CoreComponentsInterface:
        """Core komponensek létrehozása meglévő konténerből.

        Args:
            container: A dependency injection konténer

        Returns:
            Az inicializált komponensek
        """
        pass

    @staticmethod
    @abstractmethod
    def create_minimal() -> CoreComponentsInterface:
        """Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

        Returns:
            Az alapértelmezett komponensek
        """
        pass
