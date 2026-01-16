"""Dashboard Service interfész definíciója.

Ez az interfész definiálja a dashboard szolgáltatás szerződését,
amely a fő irányítópult adatait és állapotát kezeli.
"""

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    pass


@runtime_checkable
class DashboardServiceInterface(Protocol):
    """Dashboard Service interfész - Fő irányítópult kezeléséért felelős.

    Ez az interfész definiálja a dashboard adatok lekérdezését és
    kezelését végző metódusokat.
    """

    def get_system_overview(self) -> dict[str, Any]:
        """Rendszer áttekintő adatok lekérdezése.

        Returns:
            Dict[str, Any]: A rendszer aktuális állapota
        """
        ...

    def get_health_status(self) -> dict[str, str]:
        """Rendszer egészségügyi állapotának lekérdezése.

        Returns:
            Dict[str, str]: A komponensek állapota (OK/ERROR/WARNING)
        """
        ...

    def get_performance_metrics(self) -> dict[str, float]:
        """Teljesítmény metrikák lekérdezése.

        Returns:
            Dict[str, float]: A rendszer teljesítményadatok
        """
        ...

    def get_recent_activities(self) -> list[dict[str, Any]]:
        """Legutóbbi tevékenységek lekérdezése.

        Returns:
            List[Dict[str, Any]]: A tevékenységek listája
        """
        ...

    def refresh_data(self) -> None:
        """Dashboard adatok frissítése."""
        ...

    def subscribe_to_updates(self, callback: Any) -> None:
        """Feliratkozás dashboard frissítésekre.

        Args:
            callback: A hívandó callback függvény
        """
        ...
