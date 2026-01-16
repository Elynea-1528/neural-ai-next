"""Navigation Service interfész definíciója.

Ez az interfész definiálja a navigációs szolgáltatás szerződését,
amely az oldalak közötti navigációt kezeli.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Optional, Protocol, runtime_checkable

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.page_interface import PageInterface


@runtime_checkable
class NavigationServiceInterface(Protocol):
    """Navigation Service interfész - Oldalak közötti navigációért felelős.
    
    Ez az interfész definiálja a navigációs logikát kezelő metódusokat.
    """

    def navigate_to(self, page_name: str, params: dict[str, Any] | None = None) -> None:
        """Navigálás egy adott oldalra.
        
        Args:
            page_name: A céloldal neve
            params: Navigációs paraméterek
        """
        ...

    def go_back(self) -> None:
        """Visszalépés az előző oldalra.
        """
        ...

    def get_current_page(self) -> Optional["PageInterface"]:
        """Az aktuális oldal lekérdezése.
        
        Returns:
            Optional[PageInterface]: Az aktuális oldal vagy None
        """
        ...

    def get_page_history(self) -> list[str]:
        """A navigációs előzmények lekérdezése.
        
        Returns:
            list[str]: Az oldalnevek listája
        """
        ...

    def register_page(self, page_name: str, page: "PageInterface") -> None:
        """Oldal regisztrálása a navigációs rendszerben.
        
        Args:
            page_name: Az oldal neve
            page: Az oldal példánya
        """
        ...

    def subscribe(self, callback: Callable[[str, dict[str, Any]], None]) -> None:
        """Feliratkozás navigációs eseményekre.
        
        Args:
            callback: A hívandó callback függvény
        """
        ...
