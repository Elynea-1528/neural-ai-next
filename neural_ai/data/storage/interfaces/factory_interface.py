"""Tárolási factory interfész a különböző tárolási megoldások létrehozásához.

Ez az interfész egy gyártó (factory) mintát definiál, amely lehetővé teszi a tárolási
implementációk dinamikus regisztrálását és példányosítását. Az interfész segítségével
a rendszer függetlenítetté válik a konkrét tárolási osztályoktól.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class StorageFactoryInterface(ABC):
    """Tárolási factory interfész a tárolási implementációk gyártásához.

    Ez egy absztrakt alaposztály, amely meghatározza a tárolási factory-k
    alapvető viselkedését. A konkrét implementációknak ezt az interfészt kell
    megvalósítaniuk a saját factory osztályaikban.
    """

    @classmethod
    @abstractmethod
    def register_storage(
        cls,
        storage_type: str,
        storage_class: "type[StorageInterface]",
    ) -> None:
        """Új tárolási típus regisztrálása a factory számára.

        Args:
            storage_type: A tárolási típus egyedi azonosítója (pl. 'file', 's3').
            storage_class: A tárolási osztály, amely megvalósítja a StorageInterface-t.

        Raises:
            NotImplementedError: Ha az alosztály nem valósítja meg ezt a metódust.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_storage(
        cls,
        logger: "LoggerInterface | None" = None,
        config: "ConfigManagerInterface | None" = None,
        event_bus: "EventBusInterface | None" = None,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        hardware: "HardwareInterface | None" = None,
        **kwargs: object,
    ) -> "StorageInterface":
        """Tárolási példány létrehozása a megadott típus alapján.

        Args:
            logger: A naplózásért felelős interfész (opcionális, alapértelmezett: új példány).
            config: A konfigurációért felelős interfész (opcionális, alapértelmezett: új példány).
            event_bus: Az eseménybusz interfész (opcionális, alapértelmezett: új példány).
            storage_type: A kért tárolási típus azonosítója. Alapértelmezett: 'file'.
            base_path: Az alap könyvtár útvonala a fájl alapú tároláshoz.
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális).
            **kwargs: További, a tárolási implementáció specifikus paraméterek.

        Returns:
            StorageInterface: Egy inicializált tárolási példány.

        Raises:
            NotImplementedError: Ha az alosztály nem valósítja meg ezt a metódust.
            KeyError: Ha a megadott tárolási típus nincs regisztrálva.
            ValueError: Ha a megadott paraméterek érvénytelenek.
        """
        raise NotImplementedError
