"""
Dashboard Service implementáció.

Ez a modul implementálja a dashboard szolgáltatást, amely
a fő irányítópult adatait és állapotát kezeli.
"""

from typing import Dict, Any, List, Callable
from typing import TYPE_CHECKING

from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class DashboardService(DashboardServiceInterface):
    """
    Dashboard Service - Fő irányítópult kezeléséért felelős.
    
    Ez az osztály implementálja a dashboard adatok lekérdezését és
    kezelését végző metódusokat.
    """

    def __init__(self, bridge: "CoreBridgeInterface") -> None:
        """
        A Dashboard Service inicializálása.
        
        Args:
            bridge: A backend bridge példány
        """
        self._bridge = bridge
        self._cached_data: Dict[str, Any] = {}
        self._subscribers: List[Callable[[Dict[str, Any]], None]] = []

    def get_system_overview(self) -> Dict[str, Any]:
        """
        Rendszer áttekintő adatok lekérdezése.
        
        Returns:
            Dict[str, Any]: A rendszer aktuális állapota
        """
        # Lekérdezzük a rendszerinformációt a bridgen keresztül
        system_info = self._bridge.get_system_info()
        
        overview = {
            "system_info": system_info,
            "last_update": "2026-01-04T19:13:00Z",
            "components": {
                "core": "OK",
                "database": "OK",
                "event_bus": "OK",
                "collectors": "OK",
                "processors": "OK"
            }
        }
        
        self._cached_data["overview"] = overview
        return overview

    def get_health_status(self) -> Dict[str, str]:
        """
        Rendszer egészségügyi állapotának lekérdezése.
        
        Returns:
            Dict[str, str]: A komponensek állapota (OK/ERROR/WARNING)
        """
        health_status = {
            "core": "OK",
            "database": "OK",
            "event_bus": "OK",
            "collectors": "WARNING",
            "processors": "OK",
            "storage": "OK",
            "ui": "OK"
        }
        
        # Valós implementációban a bridgen keresztül ellenőriznénk
        # az egyes komponensek állapotát
        
        self._cached_data["health"] = health_status
        return health_status

    def get_performance_metrics(self) -> Dict[str, float]:
        """
        Teljesítmény metrikák lekérdezése.
        
        Returns:
            Dict[str, float]: A rendszer teljesítményadatok
        """
        system_info = self._bridge.get_system_info()
        
        if "resources" in system_info:
            resources = system_info["resources"]
            metrics = {
                "cpu_usage": resources.get("cpu_usage", 0.0),
                "memory_usage": resources.get("memory_usage", 0.0),
                "disk_usage": resources.get("disk_usage", 0.0),
                "network_io": 1234.5,  # Mock adat
                "disk_io": 567.8,      # Mock adat
                "response_time": 12.3   # Mock adat
            }
        else:
            # Fallback mock adatok
            metrics = {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4,
                "network_io": 1234.5,
                "disk_io": 567.8,
                "response_time": 12.3
            }
        
        self._cached_data["metrics"] = metrics
        return metrics

    def get_recent_activities(self) -> List[Dict[str, Any]]:
        """
        Legutóbbi tevékenységek lekérdezése.
        
        Returns:
            List[Dict[str, Any]]: A tevékenységek listája
        """
        activities = [
            {
                "timestamp": "2026-01-04T19:10:00Z",
                "type": "INFO",
                "message": "Rendszer indítva",
                "component": "core"
            },
            {
                "timestamp": "2026-01-04T19:11:00Z",
                "type": "SUCCESS",
                "message": "Adatbázis kapcsolat létrejött",
                "component": "database"
            },
            {
                "timestamp": "2026-01-04T19:12:00Z",
                "type": "WARNING",
                "message": "Adatgyűjtő lelassult",
                "component": "collectors"
            },
            {
                "timestamp": "2026-01-04T19:13:00Z",
                "type": "INFO",
                "message": "UI inicializálva",
                "component": "ui"
            }
        ]
        
        self._cached_data["activities"] = activities
        return activities

    def refresh_data(self) -> None:
        """
        Dashboard adatok frissítése.
        """
        # Töröljük a gyorsítótárazott adatokat
        self._cached_data.clear()
        
        # Értesítjük a feliratkozókat
        self._notify_subscribers({
            "type": "refresh",
            "timestamp": "2026-01-04T19:13:00Z"
        })

    def subscribe_to_updates(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Feliratkozás dashboard frissítésekre.
        
        Args:
            callback: A hívandó callback függvény
        """
        self._subscribers.append(callback)

    def _notify_subscribers(self, data: Dict[str, Any]) -> None:
        """
        Értesítés küldése a feliratkozóknak.
        
        Args:
            data: Az értesítés adatai
        """
        for callback in self._subscribers:
            try:
                callback(data)
            except Exception as e:
                # Hiba esetén csak logoljuk, ne állítsuk le a rendszert
                print(f"Hiba a callback hívásakor: {e}")