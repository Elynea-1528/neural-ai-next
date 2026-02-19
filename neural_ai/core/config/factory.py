"""Konfiguráció kezelő factory implementáció.

Ez a modul implementálja a ConfigManagerFactory osztályt, amely felelős a különböző
konfiguráció kezelők (YAML, dinamikus adatbázis-alapú) létrehozásáért és életciklusuk
kezeléséért. A factory támogatja a szinkron és aszinkron konfiguráció kezelőket is.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import ValidationError

from neural_ai.core.config.exceptions.config_error import (
    ConfigLoadError,
    ConfigValidationError,
)
from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import (
    ConfigManagerFactoryInterface,
)
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.utils.decorators import trace

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
        _logger: Logger interfész a naplózáshoz.
    """

    _manager_types: dict[str, type[ConfigManagerInterface]] = {}
    _async_manager_types: dict[str, type[AsyncConfigManagerInterface]] = {}
    _logger: LoggerInterface | None = None

    @classmethod
    @trace
    def _lazy_load_implementations(cls) -> None:
        """Lazy betölti a konkrét implementációkat a körkörös importok elkerülésére.

        Ez a metódus biztosítja, hogy a konkrét implementációk csak akkor kerüljenek
        betöltésre, amikor valóban szükség van rájuk.
        """
        if cls._logger is None:
            from neural_ai.core.logger.factory import LoggerFactory

            cls._logger = LoggerFactory.get_logger(__name__)
            cls._logger.info(
                "ConfigManagerFactory inicializálva", component="ConfigManagerFactory"
            )

        if not cls._manager_types:
            # YAML konfiguráció kezelő lazy betöltése
            from neural_ai.core.config.implementations.yaml_config_manager import (
                YAMLConfigManager,
            )

            cls._manager_types.update(
                {
                    ".yml": YAMLConfigManager,
                    ".yaml": YAMLConfigManager,
                }
            )

        if not cls._async_manager_types:
            # Dinamikus konfiguráció kezelő lazy betöltése
            from neural_ai.core.config.implementations.dynamic_config_manager import (
                DynamicConfigManager,
            )

            cls._async_manager_types.update(
                {
                    "dynamic": DynamicConfigManager,
                    "database": DynamicConfigManager,
                }
            )

    @classmethod
    @trace
    def register_manager(cls, extension: str, manager_class: type[ConfigManagerInterface]) -> None:
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

        # Type checking is handled by static analysis, runtime checks are redundant for internal use
        # but kept for robustness if called dynamically
        if not isinstance(manager_class, type):  # type: ignore
            raise TypeError("A manager_class-nak egy osztálynak kell lennie")

        if not extension.startswith("."):
            extension = f".{extension}"

        cls._manager_types[extension] = manager_class

    @classmethod
    @trace
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

        # Type checking is handled by static analysis
        if not isinstance(manager_class, type):  # type: ignore
            raise TypeError("A manager_class-nak egy osztálynak kell lennie")

        cls._async_manager_types[manager_type] = manager_class

    @classmethod
    @trace
    def get_manager(
        cls,
        filename: str | Path,
        manager_type: str | None = None,
        logger: "LoggerInterface | None" = None,
    ) -> ConfigManagerInterface:
        """Megfelelő szinkron konfiguráció kezelő létrehozása.

        A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a
        megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

        Args:
            filename: Konfigurációs fájl teljes neve (elérési úttal együtt)
            manager_type: Opcionális kezelő típus azonosító
            logger: Logger interfész a naplózásra (opcionális)

        Returns:
            ConfigManagerInterface: A létrehozott konfiguráció kezelő példány

        Raises:
            ConfigLoadError: Ha nem található megfelelő kezelő
            ConfigValidationError: Ha a konfiguráció validációja sikertelen
            ValueError: Ha a fájlnév kiterjesztése nem regisztrált
        """
        try:
            cls._lazy_load_implementations()
            filename_str = str(filename)

            # Ha explicit módon meg van adva a típus
            if manager_type:
                ext = f".{manager_type}" if not manager_type.startswith(".") else manager_type
                if ext in cls._manager_types:
                    manager_class = cls._manager_types[ext]
                    return manager_class(filename=filename_str, logger=logger)
                raise ConfigLoadError(f"Ismeretlen konfig kezelő típus: {manager_type}")

            # Fájl kiterjesztés alapján
            ext = Path(filename_str).suffix.lower()
            if ext in cls._manager_types:
                manager_class = cls._manager_types[ext]
                return manager_class(filename=filename_str, logger=logger)

            # Alapértelmezett: YAML
            if not ext:
                return cls._manager_types[".yaml"](filename=filename_str, logger=logger)

            raise ConfigLoadError(
                f"Nem található konfig kezelő a következő kiterjesztéshez: {ext}. "
                f"Támogatott kiterjesztések: {list(cls._manager_types.keys())}"
            )

        except ValidationError as e:
            # Pydantic ValidationError → ConfigValidationError konverzió
            raise ConfigValidationError(
                f"Konfiguráció validációs hiba: {e}",
                field_path=str(filename),
                invalid_value=None,
            ) from e

    @classmethod
    @trace
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
            ConfigValidationError: Ha a konfiguráció validációja sikertelen
            ValueError: Ha a session nincs megadva, ahol az szükséges
        """
        try:
            cls._lazy_load_implementations()

            if manager_type not in cls._async_manager_types:
                raise ConfigLoadError(
                    f"Ismeretlen aszinkron konfig kezelő típus: {manager_type}. "
                    f"Támogatott típusok: {list(cls._async_manager_types.keys())}"
                )

            manager_class = cls._async_manager_types[manager_type]

            # Dependency Injection: session és logger átadása
            return manager_class(filename=None, session=session, logger=logger, **kwargs)

        except ValidationError as e:
            # Pydantic ValidationError → ConfigValidationError konverzió
            raise ConfigValidationError(
                f"Aszinkron konfiguráció validációs hiba: {e}",
                field_path=manager_type,
                invalid_value=None,
            ) from e

    @classmethod
    @trace
    def create_manager(
        cls, manager_type: str, *args: object, **kwargs: dict[str, object]
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
            ConfigValidationError: Ha a konfiguráció validációja sikertelen
        """
        try:
            cls._lazy_load_implementations()

            # Normalize the manager type
            if not manager_type.startswith("."):
                manager_type = f".{manager_type}"

            if manager_type in cls._manager_types:
                manager_class = cls._manager_types[manager_type]
                # Típusbiztonság: cast-oljuk az argumentumokat
                from typing import cast

                return manager_class(*cast(tuple[str, ...], args), **cast(dict[str, Any], kwargs))

            raise ConfigLoadError(f"Ismeretlen konfig kezelő típus: {manager_type}")

        except ValidationError as e:
            # Pydantic ValidationError → ConfigValidationError konverzió
            raise ConfigValidationError(
                f"Konfiguráció létrehozási validációs hiba: {e}",
                field_path=manager_type,
                invalid_value=None,
            ) from e

    @classmethod
    @trace
    def get_supported_extensions(cls) -> list[str]:
        """Támogatott fájl kiterjesztések lekérése.

        Returns:
            list[str]: A támogatott kiterjesztések listája
        """
        cls._lazy_load_implementations()
        return list(cls._manager_types.keys())

    @classmethod
    @trace
    def get_supported_async_types(cls) -> list[str]:
        """Támogatott aszinkron konfiguráció kezelő típusok lekérése.

        Returns:
            list[str]: A támogatott aszinkron típusok listája
        """
        cls._lazy_load_implementations()
        return list(cls._async_manager_types.keys())
