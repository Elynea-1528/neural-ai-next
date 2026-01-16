"""Navigation Service implementáció.

Ez a modul implementálja a navigációs szolgáltatást, amely
az oldalak közötti navigációt kezeli.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.ui.interfaces.page_interface import PageInterface

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class NavigationService(NavigationServiceInterface):
    """Navigation Service - Oldalak közötti navigációért felelős.

    Ez az osztály implementálja a navigációs logikát kezelő metódusokat,
    és nyilvántartja a navigációs előzményeket.
    """

    def __init__(self, bridge: "CoreBridgeInterface") -> None:
        """A Navigation Service inicializálása.

        Args:
            bridge: A backend bridge példány
        """
        self._bridge = bridge
        self._pages: dict[str, PageInterface] = {}
        self._history: list[str] = []
        self._current_page: str | None = None
        self._subscribers: list[Callable[[str, dict[str, Any]], None]] = []

    def navigate_to(
        self,
        page_name: str,
        params: dict[str, Any] | None = None
    ) -> None:
        """Navigálás egy adott oldalra.

        Args:
            page_name: A céloldal neve
            params: Navigációs paraméterek
        """
        if page_name not in self._pages:
            raise ValueError(f"Oldal nem található: {page_name}")

        # Elnavigálás az aktuális oldalról
        if self._current_page:
            current_page = self._pages[self._current_page]
            current_page.on_navigate_from()

        # Navigáció az új oldalra
        self._history.append(page_name)
        self._current_page = page_name

        new_page = self._pages[page_name]
        new_page.on_navigate_to(params)

        # Értesítés a feliratkozóknak
        self._notify_subscribers(page_name, params or {})

    def go_back(self) -> None:
        """Visszalépés az előző oldalra."""
        if len(self._history) < 2:
            return  # Nincs hova visszamenni

        # Eltávolítjuk az aktuális oldalt
        self._history.pop()

        # Visszanavigálunk az előzőre
        previous_page = self._history[-1]
        self._current_page = previous_page

        page = self._pages[previous_page]
        page.on_navigate_to()

        # Értesítés a feliratkozóknak
        self._notify_subscribers(previous_page, {})

    def get_current_page(self) -> PageInterface | None:
        """Az aktuális oldal lekérdezése.

        Returns:
            Optional[PageInterface]: Az aktuális oldal vagy None
        """
        if self._current_page:
            return self._pages.get(self._current_page)
        return None

    def get_page_history(self) -> list[str]:
        """A navigációs előzmények lekérdezése.

        Returns:
            List[str]: Az oldalnevek listája
        """
        return self._history.copy()

    def register_page(
        self,
        page_name: str,
        page: PageInterface
    ) -> None:
        """Oldal regisztrálása a navigációs rendszerben.

        Args:
            page_name: Az oldal neve
            page: Az oldal példánya
        """
        self._pages[page_name] = page

        # Ha ez az első oldal, állítsuk be aktuálisnak
        if not self._current_page:
            self._current_page = page_name
            self._history.append(page_name)

    def subscribe(
        self,
        callback: Callable[[str, dict[str, Any]], None]
    ) -> None:
        """Feliratkozás navigációs eseményekre.

        Args:
            callback: A hívandó callback függvény
        """
        self._subscribers.append(callback)

    def _notify_subscribers(
        self,
        page_name: str,
        params: dict[str, Any]
    ) -> None:
        """Értesítés küldése a feliratkozóknak.

        Args:
            page_name: Az oldal neve
            params: A navigációs paraméterek
        """
        for callback in self._subscribers:
            try:
                callback(page_name, params)
            except Exception as e:
                # Hiba esetén csak logoljuk, ne állítsuk le a rendszert
                print(f"Hiba a callback hívásakor: {e}")
