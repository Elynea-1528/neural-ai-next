"""Base komponens interfészek.

Ez a modul tartalmazza a Neural AI Next base komponens rendszerének
alapvető interfészeit és absztrakt osztályait.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class DIContainerInterface(ABC):
    """Dependency injection konténer interfész.

    Ez az interfész definiálja a dependency injection konténer alapvető
    funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.
    """

    @abstractmethod
    def register_instance(self, interface: Any, instance: Any) -> None:
        """Komponens példány regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a példányt regisztráljuk
            instance: A regisztrálandó példány
        """
        pass

    @abstractmethod
    def register_factory(self, interface: Any, factory: Callable[[], Any]) -> None:
        """Factory függvény regisztrálása a konténerben.

        Args:
            interface: Az interfész típusa, amihez a factory-t regisztráljuk
            factory: A factory függvény, ami létrehozza az implementációt
        """
        pass

    @abstractmethod
    def resolve(self, interface: Any) -> Any | None:
        """Függőség feloldása a konténerből.

        Args:
            interface: Az interfész típusa, amit fel szeretnénk oldani

        Returns:
            A regisztrált példány vagy None ha nem található
        """
        pass

    @abstractmethod
    def register_lazy(self, component_name: str, factory_func: Callable[[], Any]) -> None:
        """Lusta betöltésű komponens regisztrálása.

        Args:
            component_name: A komponens neve
            factory_func: A komponens létrehozásához használt factory függvény

        Raises:
            ValueError: Ha a komponens név érvénytelen vagy a factory függvény nem hívható
        """
        pass

    @abstractmethod
    def get(self, component_name: str) -> Any:
        """Komponens példány lekérése (lusta betöltéssel).

        Args:
            component_name: A lekérendő komponens neve

        Returns:
            A komponens példánya

        Raises:
            ComponentNotFoundError: Ha a komponens nem található
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Konténer ürítése."""
        pass


class CoreComponentsInterface(ABC):
    """Core komponensek interfész.

    Ez az interfész definiálja a core komponensek gyűjteményének
    alapvető funkcionalitását és hozzáférését.
    """

    @property
    @abstractmethod
    def config(self) -> Any | None:
        """Konfiguráció kezelő komponens.

        Returns:
            A konfiguráció kezelő komponens vagy None
        """
        pass

    @property
    @abstractmethod
    def logger(self) -> Any | None:
        """Logger komponens.

        Returns:
            A logger komponens vagy None
        """
        pass

    @property
    @abstractmethod
    def storage(self) -> Any | None:
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


class LazyComponentInterface(ABC):
    """Lusta betöltésű komponens interfész.

    Ez az interfész definiálja a lusta (lazy) betöltésű komponensek
    alapvető funkcionalitását.
    """

    @abstractmethod
    def get(self) -> Any:
        """Komponens példány lekérése (lusta betöltéssel).

        Returns:
            A komponens példánya
        """
        pass

    @property
    @abstractmethod
    def is_loaded(self) -> bool:
        """Ellenőrzi, hogy a komponens betöltődött-e már.

        Returns:
            True, ha a komponens már betöltődött, egyébként False
        """
        pass
