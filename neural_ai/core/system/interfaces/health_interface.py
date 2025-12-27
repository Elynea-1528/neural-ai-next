"""Rendszer egészségügyi monitorozás interfészei.

Ez a modul a rendszer egészségügyi állapotának monitorozásához szükséges
interfészeket definiálja, beleértve a komponens állapotokat, erőforrás-használatot
és rendszer metrikákat.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ComponentStatus(Enum):
    """Komponens állapot enum.

    A rendszer komponenseinek állapotát definiálja.
    """
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    OFFLINE = "offline"


class HealthStatus(Enum):
    """Rendszer egészségügyi állapot enum.

    A teljes rendszer egészségügyi állapotát definiálja.
    """
    OK = "ok"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class ComponentHealth:
    """Komponens egészségügyi információi.

    Egy adott komponens egészségügyi állapotát és metrikáit tartalmazza.

    Attributes:
        name: A komponens neve
        status: A komponens állapota (ComponentStatus enum)
        message: Részletes üzenet vagy hiba
        timestamp: Az állapot ellenőrzésének időpontja
        metrics: Opcionális metrikák (pl. response time, error rate)
    """
    name: str
    status: ComponentStatus
    message: str
    timestamp: datetime
    metrics: dict[str, float] | None = None


@dataclass
class SystemHealth:
    """Rendszer egészségügyi információi.

    A teljes rendszer egészségügyi állapotát és komponenseinek állapotát tartalmazza.

    Attributes:
        overall_status: A rendszer általános állapota (HealthStatus enum)
        message: Részletes üzenet
        timestamp: Az ellenőrzés időpontja
        components: A komponensek egészségügyi információi
        system_metrics: Rendszer szintű metrikák (CPU, memória, stb.)
    """
    overall_status: HealthStatus
    message: str
    timestamp: datetime
    components: list[ComponentHealth]
    system_metrics: dict[str, float] | None = None


class HealthMonitorInterface(ABC):
    """Rendszer egészségügyi monitorozás interfész.

    Ez az interfész definiálja a rendszer egészségügyi állapotának
    monitorozásához szükséges metódusokat.
    """

    @abstractmethod
    def check_health(self) -> SystemHealth:
        """Ellenőrzi a teljes rendszer egészségügyi állapotát.

        A metódus összegyűjti az összes komponens és a rendszer
        egészségügyi információit, majd összesíti azokat.

        Returns:
            SystemHealth: A rendszer teljes egészségügyi állapota
        """
        pass

    @abstractmethod
    def check_component(self, component_name: str) -> ComponentHealth:
        """Ellenőrzi egy adott komponens egészségügyi állapotát.

        Args:
            component_name: A komponens neve

        Returns:
            ComponentHealth: A komponens egészségügyi információi

        Raises:
            ValueError: Ha a komponens nem létezik
        """
        pass

    @abstractmethod
    def get_registered_components(self) -> list[str]:
        """Visszaadja a monitorozott komponensek listáját.

        Returns:
            list[str]: A monitorozott komponensek nevei
        """
        pass

    @abstractmethod
    def register_component(self, component_name: str) -> None:
        """Regisztrál egy új komponenst a monitorozásra.

        Args:
            component_name: A komponens neve
        """
        pass

    @abstractmethod
    def unregister_component(self, component_name: str) -> None:
        """Eltávolít egy komponenst a monitorozás alól.

        Args:
            component_name: A komponens neve
        """
        pass


class HealthCheckInterface(ABC):
    """Egyedi egészségügyi ellenőrzés interfész.

    Ez az interfész egy specifikus egészségügyi ellenőrzést definiál,
    amelyet a HealthMonitorInterface implementációk használhatnak.
    """

    @abstractmethod
    def check(self) -> ComponentHealth:
        """Végrehajtja az egészségügyi ellenőrzést.

        Returns:
            ComponentHealth: Az ellenőrzés eredménye
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Visszaadja az ellenőrzés nevét.

        Returns:
            str: Az ellenőrzés neve
        """
        pass
