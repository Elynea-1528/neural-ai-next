"""Dashboard Service implementáció.

Ez a modul implementálja a dashboard szolgáltatást, amely
a fő irányítópult adatait és állapotát kezeli.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from neural_ai.core.system.interfaces.health_interface import (
    ComponentStatus,
    SystemHealth,
)
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface

if TYPE_CHECKING:
    pass


class DashboardService(DashboardServiceInterface):
    """Dashboard Service - Fő irányítópult kezeléséért felelős.

    Ez az osztály implementálja a dashboard adatok lekérdezését és
    kezelését végző metódusokat.
    """

    def __init__(self, logger: Any, config: dict[str, Any], core_components: Any) -> None:
        """A Dashboard Service inicializálása.

        Args:
            logger: A logger példány
            config: A szolgáltatás konfiguráció
            core_components: A core komponensek
        """
        self._logger = logger
        self._config = config
        self._core_components = core_components
        self._cached_data: dict[str, Any] = {}
        self._subscribers: list[Callable[[dict[str, Any]], None]] = []

    def get_system_overview(self) -> dict[str, Any]:
        """Rendszer áttekintő adatok lekérdezése.

        Returns:
            Dict[str, Any]: A rendszer aktuális állapota
        """
        # Gyorsítótár ellenőrzése
        if "overview" in self._cached_data:
            return self._cached_data["overview"]

        # Lekérdezzük a rendszerinformációt a core_components-en keresztül
        system_info = self._core_components.get_system_info()

        overview = {
            "system_info": system_info,
            "last_update": "2026-01-04T19:13:00Z",
            "components": {
                "core": "OK",
                "database": "OK",
                "event_bus": "OK",
                "collectors": "OK",
                "processors": "OK",
            },
        }

        self._cached_data["overview"] = overview
        return overview

    def get_health_status(self) -> dict[str, str]:
        """Rendszer egészségügyi állapotának lekérdezése.

        A metódus a valós HealthMonitor komponenst kérdezi le a backend
        rendszerből, és leképezi a komponens állapotokat UI-barát formátumba.

        Returns:
            Dict[str, str]: A komponensek állapota (OK/WARNING/ERROR/CRITICAL/UNKNOWN)
        """
        # Fallback, ha a core_components vagy a health monitor nem elérhető
        if not self._core_components.core or not self._core_components.core.health_monitor:
            return {"system": "UNKNOWN"}

        # Valós lekérdezés a HealthMonitor-ból
        health: SystemHealth = self._core_components.core.health_monitor.check_health()

        # Mapping (ComponentHealth -> UI String)
        status_map: dict[str, str] = {}
        for comp in health.components:
            # Enum to String mapping
            if comp.status == ComponentStatus.HEALTHY:
                status_str = "OK"
            elif comp.status == ComponentStatus.WARNING:
                status_str = "WARNING"
            elif comp.status == ComponentStatus.CRITICAL:
                status_str = "ERROR"
            elif comp.status == ComponentStatus.UNKNOWN:
                status_str = "UNKNOWN"
            elif comp.status == ComponentStatus.OFFLINE:
                status_str = "OFFLINE"
            else:
                status_str = "UNKNOWN"

            status_map[comp.name] = status_str

        # Hozzáadjuk a rendszer általános állapotát is
        status_map["system"] = health.overall_status.value.upper()

        self._cached_data["health"] = status_map
        return status_map

    def get_performance_metrics(self) -> dict[str, float]:
        """Teljesítmény metrikák lekérdezése.

        Returns:
            Dict[str, float]: A rendszer teljesítményadatok
        """
        system_info = self._core_components.get_system_info()

        if "resources" in system_info:
            resources = system_info["resources"]
            metrics = {
                "cpu_usage": resources.get("cpu_usage", 0.0),
                "memory_usage": resources.get("memory_usage", 0.0),
                "disk_usage": resources.get("disk_usage", 0.0),
                "network_io": 1234.5,  # Mock adat
                "disk_io": 567.8,  # Mock adat
                "response_time": 12.3,  # Mock adat
            }
        else:
            # Fallback mock adatok
            metrics = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4,
                "network_io": 1234.5,
                "disk_io": 567.8,
                "response_time": 12.3,
            }

        self._cached_data["metrics"] = metrics
        return metrics

    def get_recent_activities(self) -> list[dict[str, Any]]:
        """Legutóbbi tevékenységek lekérdezése.

        Returns:
            List[Dict[str, Any]]: A tevékenységek listája
        """
        activities = [
            {
                "timestamp": "2026-01-04T19:10:00Z",
                "type": "INFO",
                "message": "Rendszer indítva",
                "component": "core",
            },
            {
                "timestamp": "2026-01-04T19:11:00Z",
                "type": "SUCCESS",
                "message": "Adatbázis kapcsolat létrejött",
                "component": "database",
            },
            {
                "timestamp": "2026-01-04T19:12:00Z",
                "type": "WARNING",
                "message": "Adatgyűjtő lelassult",
                "component": "collectors",
            },
            {
                "timestamp": "2026-01-04T19:13:00Z",
                "type": "INFO",
                "message": "UI inicializálva",
                "component": "ui",
            },
        ]

        self._cached_data["activities"] = activities
        return activities

    def refresh_data(self) -> None:
        """Dashboard adatok frissítése."""
        # Töröljük a gyorsítótárazott adatokat
        self._cached_data.clear()

        # Értesítjük a feliratkozókat
        self._notify_subscribers({"type": "refresh", "timestamp": "2026-01-04T19:13:00Z"})

    def subscribe_to_updates(self, callback: Callable[[dict[str, Any]], None]) -> None:
        """Feliratkozás dashboard frissítésekre.

        Args:
            callback: A hívandó callback függvény
        """
        self._subscribers.append(callback)

    def _notify_subscribers(self, data: dict[str, Any]) -> None:
        """Értesítés küldése a feliratkozóknak.

        Args:
            data: Az értesítés adatai
        """
        for callback in self._subscribers:
            try:
                callback(data)
            except Exception as e:
                # Hiba esetén csak logoljuk, ne állítsuk le a rendszert
                print(f"Hiba a callback hívásakor: {e}")
