"""Konfiguráció kezelő factory interfész definíciója.

Ez az interfész egy gyártó (factory) mintát valósít meg a konfiguráció kezelők
létrehozásához. Lehetővé teszi különböző konfigurációs formátumok kezelését
és a kezelők dinamikus regisztrációját.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class ConfigManagerFactoryInterface(ABC):
    """Konfiguráció kezelő factory interfész.

    Ez az absztrakt osztály definiálja a konfiguráció kezelő gyártó alapvető
    műveleteit, beleértve a kezelők regisztrációját és létrehozását.
    """

    @classmethod
    @abstractmethod
    def register_manager(
        cls, extension: str, manager_class: type["ConfigManagerInterface"]
    ) -> None:
        """Új konfiguráció kezelő típus regisztrálása.

        A metódus lehetővé teszi egy adott fájlkiterjesztéshez tartozó konfiguráció
        kezelő osztály regisztrációját. Ezt követően a gyár képes lesz automatikusan
        kiválasztani a megfelelő kezelőt a fájlnév alapján.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml", ".yaml", ".json")
            manager_class: A kezelő osztály, amely implementálja a ConfigManagerInterface-t

        Raises:
            ValueError: Ha az extension vagy manager_class érvénytelen
            TypeError: Ha a manager_class nem megfelelő típusú
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_manager(
        cls, filename: str, manager_type: str | None = None
    ) -> "ConfigManagerInterface":
        """Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján.

        A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a
        megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

        Args:
            filename: Konfigurációs fájl teljes neve (elérési úttal együtt)
            manager_type: Opcionális kezelő típus azonosító

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ValueError: Ha a fájlnév kiterjesztése nem regisztrált
            KeyError: Ha a megadott manager_type nem létezik
            RuntimeError: Ha a kezelő létrehozása sikertelen
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def create_manager(
        cls, manager_type: str, *args: object, **kwargs: object
    ) -> "ConfigManagerInterface":
        """Konfiguráció kezelő létrehozása típus alapján.

        A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt,
        lehetővé téve a paraméterek átadását a konstruktornak.

        Args:
            manager_type: A kért kezelő típus azonosítója
            *args: Pozícionális argumentumok a kezelő konstruktorának
            **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            KeyError: Ha a megadott manager_type nem létezik
            TypeError: Ha a paraméterek nem kompatibilisek a kezelő konstruktorával
            RuntimeError: Ha a kezelő létrehozása sikertelen
        """
        raise NotImplementedError
