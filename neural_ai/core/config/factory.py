"""Konfiguráció kezelő factory implementáció.

Ez a modul implementálja a ConfigManagerFactory osztályt, amely felelős a különböző
konfiguráció kezelők (YAML, dinamikus adatbázis-alapú) létrehozásáért és életciklusuk
kezeléséért. A factory támogatja a szinkron és aszinkron konfiguráció kezelőket is.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import (
    ConfigManagerFactoryInterface,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from neural_ai.core.logger.interfaces import LoggerInterface


class ConfigManagerFactory(ConfigManagerFactoryInterface):
    """Factory osztály konfiguráció kezelők létrehozásához.

    Ez az osztály felelős a különböző típusú konfiguráció kezelők létrehozásáért,
    regisztrálásáért és életciklusuk kezeléséért. Támogatja a szinkron (YAML fájl)
    és aszinkron (adatbázis-alapú dinamikus) konfiguráció kezelőket is.

    A factory alkalmazza a Dependency Injection elvet, és csak interfészeken keresztül
    kommunikál a konkrét implementációkkal.

    Attributes:
        _manager_types: Regisztrált szinkron konfiguráció kezelő típusok.
        _async_manager_types: Regisztrált aszinkron konfiguráció kezelő típusok.
    """

    _manager_types: dict[str, type[ConfigManagerInterface]] = {}
    _async_manager_types: dict[str, type[AsyncConfigManagerInterface]] = {}

    @classmethod
    def _lazy_load_implementations(cls) -> None:
        """Lazy betölti a konkrét implementációkat a körkörös importok elkerülésére.

        Ez a metódus biztosítja, hogy a konkrét implementációk csak akkor kerüljenek
        betöltésre, amikor valóban szükség van rájuk.
        """
        if not cls._manager_types:
            # YAML konfiguráció kezelő lazy betöltése
            from neural_ai.core.config.implementations.yaml_config_manager import (
                YAMLConfigManager,
            )

            cls._manager_types.update({
                ".yml": YAMLConfigManager,
                ".yaml": YAMLConfigManager,
            })

        if not cls._async_manager_types:
            # Dinamikus konfiguráció kezelő lazy betöltése
            from neural_ai.core.config.implementations.dynamic_config_manager import (
                DynamicConfigManager,
            )

            cls._async_manager_types.update({
                "dynamic": DynamicConfigManager,
                "database": DynamicConfigManager,
            })

    @classmethod
    def register_manager(
        cls, extension: str, manager_class: type[ConfigManagerInterface]
    ) -> None:
        """Új szinkron konfiguráció kezelő típus regisztrálása.

        Args:
            extension: A kezelt fájl kiterjesztése (pl: ".yml", ".json")
            manager_class: A kezelő osztály, amely implementálja a ConfigManagerInterface-t

        Raises:
            ValueError: Ha az extension vagy manager_class érvénytelen
            TypeError: Ha a manager_class nem megfelelő típusú
        """
        if not extension:
            raise ValueError("Az extension nem lehet üres")

        if not extension.startswith("."):
            extension = f".{extension}"

        if not isinstance(manager_class, type):
            raise TypeError(f"Érvénytelen manager_class: {manager_class}")

        if not issubclass(manager_class, ConfigManagerInterface):
            raise TypeError(
                f"A manager_class-nak implementálnia kell a "
                f"ConfigManagerInterface-t: {manager_class}"
            )

        cls._manager_types[extension] = manager_class

    @classmethod
    def register_async_manager(
        cls, manager_type: str, manager_class: type[AsyncConfigManagerInterface]
    ) -> None:
        """Új aszinkron konfiguráció kezelő típus regisztrálása.

        Args:
            manager_type: A kezelő típusának azonosítója (pl: "dynamic", "database")
            manager_class: A kezelő osztály, amely implementálja az AsyncConfigManagerInterface-t

        Raises:
            ValueError: Ha a manager_type érvénytelen
            TypeError: Ha a manager_class nem megfelelő típusú
        """
        if not manager_type:
            raise ValueError("A manager_type nem lehet üres")

        if not isinstance(manager_class, type):
            raise TypeError(f"Érvénytelen manager_class: {manager_class}")

        if not issubclass(manager_class, AsyncConfigManagerInterface):
            raise TypeError(
                f"A manager_class-nak implementálnia kell az "
                f"AsyncConfigManagerInterface-t: {manager_class}"
            )

        cls._async_manager_types[manager_type] = manager_class

    @classmethod
    def get_manager(
        cls, filename: str | Path, manager_type: str | None = None
    ) -> ConfigManagerInterface:
        """Megfelelő szinkron konfiguráció kezelő létrehozása.

        A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a
        megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

        Args:
            filename: Konfigurációs fájl teljes neve (elérési úttal együtt)
            manager_type: Opcionális kezelő típus azonosító

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
            ValueError: Ha a fájlnév kiterjesztése nem regisztrált
        """
        cls._lazy_load_implementations()
        filename_str = str(filename)

        # Ha explicit módon meg van adva a típus
        if manager_type:
            ext = f".{manager_type}" if not manager_type.startswith(".") else manager_type
            if ext in cls._manager_types:
                manager_class = cls._manager_types[ext]
                return manager_class(filename=filename_str)
            raise ConfigLoadError(f"Ismeretlen konfig kezelő típus: {manager_type}")

        # Fájl kiterjesztés alapján
        ext = Path(filename_str).suffix.lower()
        if ext in cls._manager_types:
            manager_class = cls._manager_types[ext]
            return manager_class(filename=filename_str)

        # Alapértelmezett: YAML
        if not ext:
            return cls._manager_types[".yaml"](filename=filename_str)

        raise ConfigLoadError(
            f"Nem található konfig kezelő a következő kiterjesztéshez: {ext}. "
            f"Támogatott kiterjesztések: {list(cls._manager_types.keys())}"
        )

    @classmethod
    async def get_async_manager(
        cls,
        manager_type: str,
        session: "AsyncSession",
        logger: "LoggerInterface | None" = None,
        **kwargs: Any,
    ) -> AsyncConfigManagerInterface:
        """Aszinkron konfiguráció kezelő létrehozása.

        A metódus explicit típusmegadással hozza létre az aszinkron konfiguráció kezelőt,
        lehetővé téve a paraméterek átadását a konstruktornak.

        Args:
            manager_type: A kért kezelő típus azonosítója (pl: "dynamic", "database")
            session: Az adatbázis session (kötelező a DynamicConfigManager-hez)
            logger: Logger interfész a naplózásra (opcionális)
            **kwargs: További kulcsszavas argumentumok a kezelő konstruktorának

        Returns:
            AsyncConfigManagerInterface: A létrehozott aszinkron konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha a megadott manager_type nem létezik
            ValueError: Ha a session nincs megadva, ahol az szükséges
        """
        cls._lazy_load_implementations()

        if manager_type not in cls._async_manager_types:
            raise ConfigLoadError(
                f"Ismeretlen aszinkron konfig kezelő típus: {manager_type}. "
                f"Támogatott típusok: {list(cls._async_manager_types.keys())}"
            )

        manager_class = cls._async_manager_types[manager_type]

        # Dependency Injection: session és logger átadása
        return manager_class(filename=None, session=session, logger=logger, **kwargs)

    @classmethod
    def create_manager(
        cls, manager_type: str, *args: Any, **kwargs: Any
    ) -> ConfigManagerInterface:
        """Szinkron konfiguráció kezelő létrehozása típus alapján.

        A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt,
        lehetővé téve a paraméterek átadását a konstruktornak.

        Args:
            manager_type: A kért kezelő típus azonosítója
            *args: Pozícionális argumentumok a kezelő konstruktorának
            **kwargs: Kulcsszavas argumentumok a kezelő konstruktorának

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha a megadott manager_type nem létezik
        """
        cls._lazy_load_implementations()

        # Normalize the manager type
        if not manager_type.startswith("."):
            manager_type = f".{manager_type}"

        if manager_type in cls._manager_types:
            manager_class = cls._manager_types[manager_type]
            return manager_class(*args, **kwargs)

        raise ConfigLoadError(f"Ismeretlen konfig kezelő típus: {manager_type}")

    @classmethod
    def get_supported_extensions(cls) -> list[str]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            list[str]: A támogatott kiterjesztések listája
        """
        cls._lazy_load_implementations()
        return list(cls._manager_types.keys())

    @classmethod
    def get_supported_async_types(cls) -> list[str]:
        """Támogatott aszinkron konfiguráció kezelő típusok lekérése.

        Returns:
            list[str]: A támogatott aszinkron típusok listája
        """
        cls._lazy_load_implementations()
        return list(cls._async_manager_types.keys())
