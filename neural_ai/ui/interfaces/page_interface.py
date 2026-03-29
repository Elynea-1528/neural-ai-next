"""Page interfész definíciója.

Ez az interfész definiálja az oldal komponensek szerződését.
"""

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


@runtime_checkable
class PageInterface(Protocol):
    """Page interfész - Oldal komponensek alapja.

    Ez az interfész definiálja az oldalak által implementálandó metódusokat.
    """

    def __init__(self, bridge: "CoreBridgeInterface", **kwargs: object) -> None:
        """Oldal inicializálása.

        Args:
            bridge: A backend bridge példány
            **kwargs: További paraméterek
        """
        ...

    def render(self) -> object:
        """Az oldal tartalmának renderelése.

        Returns:
            Any: A renderelt tartalom
        """
        ...

    def on_navigate_to(self, params: dict[str, object] | None = None) -> None:
        """Akció, amikor az oldalra navigálnak.

        Args:
            params: Navigációs paraméterek
        """
        ...

    def on_navigate_from(self) -> None:
        """Akció, amikor elnavigálnak az oldalról."""
        ...

    @property
    def title(self) -> str:
        """Az oldal címét visszaadó property.

        Returns:
            str: Az oldal címe
        """
        ...

    @property
    def is_loaded(self) -> bool:
        """Az oldal betöltöttségi állapotát ellenőrző property.

        Returns:
            bool: True, ha az oldal betöltött, egyébként False
        """
        ...
