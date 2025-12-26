"""EventBus interfész a Neural AI Next rendszerhez.

Ez a modul definiálja az EventBus interfészt, amely biztosítja
az eseményvezérelt architektúra alapjait.

Author: Neural AI Next Team
Version: 1.0.0
"""

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pydantic import BaseModel


# Típus aliasok a jobb olvashatóság érdekében
EventCallback = Callable[["BaseModel"], Any]


@dataclass
class EventBusConfig:
    """EventBus konfiguráció.

    Attributes:
        zmq_context: ZeroMQ kontextus (opcionális, létrejön ha nincs megadva)
        pub_port: Publisher port (alapértelmezett: 5555)
        sub_port: Subscriber port (alapértelmezett: 5556)
        use_inproc: Használjon inproc transportot teszteléshez (alapértelmezett: False)
    """
    zmq_context: Any = None
    pub_port: int = 5555
    sub_port: int = 5556
    use_inproc: bool = False


class EventBusInterface(ABC):
    """EventBus interfész.

    Ez az interfész definiálja az eseménybusz alapvető műveleteit:
    - Események közzététele
    - Feliratkozás eseményekre
    - Leiratkozás eseményekről
    - Bus indítása és leállítása
    """

    @property
    @abstractmethod
    def config(self) -> EventBusConfig:
        """Visszaadja az EventBus konfigurációját.

        Returns:
            Az EventBus konfigurációja
        """
        pass

    @abstractmethod
    async def start(self) -> None:
        """Elindítja az EventBus-t és létrehozza a socketeket."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Leállítja az EventBus-t és felszabadítja az erőforrásokat."""
        pass

    @abstractmethod
    async def publish(self, event_type: str, event: "BaseModel") -> None:
        """Esemény közzététele a buszon.

        Args:
            event_type: Az esemény típusa (pl. 'market_data', 'trade')
            event: Az esemény objektum (Pydantic BaseModel)

        Raises:
            EventBusError: Ha az EventBus nincs elindítva
            PublishError: Ha a publisher socket nincs inicializálva
        """
        pass

    @abstractmethod
    def subscribe(self, event_type: str, callback: EventCallback) -> None:
        """Feliratkozás eseménytípusra.

        Args:
            event_type: Az esemény típusa, amire feliratkozunk
            callback: A callback függvény, amely az eseményt fogadja

        Note:
            A callback-nek aszinkronnak kell lennie (async def)
        """
        pass

    @abstractmethod
    def unsubscribe(self, event_type: str, callback: EventCallback) -> None:
        """Leiratkozás eseménytípusról.

        Args:
            event_type: Az esemény típusa
            callback: A callback függvény, amelyet eltávolítunk
        """
        pass

    @abstractmethod
    async def run_forever(self) -> None:
        """Eseménybusz örök futás (blokkoló).

        Ez a metódus egy végtelen ciklusban fogadja az eseményeket
        és továbbítja azokat a feliratkozóknak.

        Note:
            Ez egy blokkoló metódus, csak teszteléshez vagy külön task-ként használd
        """
        pass