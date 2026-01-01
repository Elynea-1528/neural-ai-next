"""Live Feed Interface for JForex Live Data Collection.

Ez az interfész definiálja a JForex live adatfolyam fogadásához szükséges metódusokat.
Az implementációk ezt az interfészt használják a ZMQ-alapú tick fogadáshoz.
"""

from abc import ABC, abstractmethod


class ILiveFeed(ABC):
    """Absztrakt osztály a JForex live adatfolyam kezeléséhez.

    Ez az interfész felelős a Java Bridge-el (NeuralBridgeStrategy) való kommunikációért
    ZMQ socketeken keresztül. A start() metódus indítja el a tick fogadást, a stop() pedig
    leállítja azt.
    """

    @abstractmethod
    async def start(self) -> None:
        """Indítja a live adatfolyam fogadását.

        Létrehozza a ZMQ SUB socketet, csatlakozik a megadott portra, és elindítja
        a háttérfolyamatot (_listen_loop) a tickek folyamatos fogadásához.

        Raises:
            LiveFeedError: Ha a csatlakozás vagy a fogadás során hiba történik.
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Leállítja a live adatfolyam fogadását.

        Megszünteti a ZMQ kapcsolatot és leállítja a háttérfolyamatot.
        """
        pass

    @abstractmethod
    def is_running(self) -> bool:
        """Visszaadja, hogy a live feed jelenleg fut-e.

        Returns:
            bool: True, ha a feed fut, False egyébként.
        """
        pass
