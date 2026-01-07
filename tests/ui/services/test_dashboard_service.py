"""Dashboard Service tesztek."""

from typing import Any
from unittest.mock import MagicMock

import pytest

from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthStatus,
    SystemHealth,
)
from neural_ai.ui.services.dashboard_service import DashboardService


class TestDashboardService:
    """Dashboard Service tesztek osztálya."""

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridge létrehozása."""
        bridge = MagicMock()
        bridge.core = MagicMock()
        bridge.core.health_monitor = MagicMock()
        return bridge

    @pytest.fixture
    def mock_system_health(self) -> SystemHealth:
        """Mock SystemHealth létrehozása."""
        components = [
            ComponentHealth(
                name="core",
                status=ComponentStatus.HEALTHY,
                message="Komponens egészséges",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="database",
                status=ComponentStatus.WARNING,
                message="Lassú válaszidő",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="storage",
                status=ComponentStatus.CRITICAL,
                message="Lemez megtelt",
                timestamp=None,  # type: ignore
            ),
        ]
        return SystemHealth(
            overall_status=HealthStatus.DEGRADED,
            message="Figyelmeztetés állapotú komponensek: 1",
            timestamp=None,  # type: ignore
            components=components,
            system_metrics={"cpu_percent": 45.2},
        )

    def test_init(self, mock_bridge: MagicMock) -> None:
        """Teszteli a Dashboard Service inicializálását."""
        service = DashboardService(mock_bridge)

        assert service._bridge == mock_bridge
        assert service._cached_data == {}
        assert service._subscribers == []

    def test_get_health_status_with_available_monitor(
        self, mock_bridge: MagicMock, mock_system_health: SystemHealth
    ) -> None:
        """Teszteli az egészségügyi állapot lekérdezését, ha a monitor elérhető."""
        # Mock a health monitor check_health metódusát
        mock_bridge.core.health_monitor.check_health.return_value = mock_system_health

        service = DashboardService(mock_bridge)
        result = service.get_health_status()

        # Ellenőrizzük, hogy a metódus meghívódott
        mock_bridge.core.health_monitor.check_health.assert_called_once()

        # Ellenőrizzük az eredményt
        expected = {
            "core": "OK",
            "database": "WARNING",
            "storage": "ERROR",
            "system": "DEGRADED",
        }
        assert result == expected

        # Ellenőrizzük, hogy a gyorsítótárba mentés megtörtént
        assert service._cached_data["health"] == expected

    def test_get_health_status_without_core(self, mock_bridge: MagicMock) -> None:
        """Teszteli az egészségügyi állapot lekérdezését, ha a core nem elérhető."""
        mock_bridge.core = None

        service = DashboardService(mock_bridge)
        result = service.get_health_status()

        expected = {"system": "UNKNOWN"}
        assert result == expected

    def test_get_health_status_without_health_monitor(self, mock_bridge: MagicMock) -> None:
        """Teszteli az egészségügyi állapot lekérdezését, ha a health monitor nem elérhető."""
        mock_bridge.core.health_monitor = None

        service = DashboardService(mock_bridge)
        result = service.get_health_status()

        expected = {"system": "UNKNOWN"}
        assert result == expected

    def test_get_health_status_all_status_types(self, mock_bridge: MagicMock) -> None:
        """Teszteli az összes állapot típus leképezését."""
        components = [
            ComponentHealth(
                name="healthy",
                status=ComponentStatus.HEALTHY,
                message="OK",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="warning",
                status=ComponentStatus.WARNING,
                message="WARNING",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="critical",
                status=ComponentStatus.CRITICAL,
                message="CRITICAL",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="unknown",
                status=ComponentStatus.UNKNOWN,
                message="UNKNOWN",
                timestamp=None,  # type: ignore
            ),
            ComponentHealth(
                name="offline",
                status=ComponentStatus.OFFLINE,
                message="OFFLINE",
                timestamp=None,  # type: ignore
            ),
        ]

        system_health = SystemHealth(
            overall_status=HealthStatus.OK,
            message="Minden komponens egészséges",
            timestamp=None,  # type: ignore
            components=components,
        )

        mock_bridge.core.health_monitor.check_health.return_value = system_health

        service = DashboardService(mock_bridge)
        result = service.get_health_status()

        expected = {
            "healthy": "OK",
            "warning": "WARNING",
            "critical": "ERROR",
            "unknown": "UNKNOWN",
            "offline": "OFFLINE",
            "system": "OK",
        }
        assert result == expected

    def test_get_system_overview(self, mock_bridge: MagicMock) -> None:
        """Teszteli a rendszer áttekintő adatok lekérdezését."""
        mock_system_info = {
            "version": "6.0.0",
            "status": "running",
            "components": {"core": "OK", "database": "OK"},
        }
        mock_bridge.get_system_info.return_value = mock_system_info

        service = DashboardService(mock_bridge)
        result = service.get_system_overview()

        assert "system_info" in result
        assert "last_update" in result
        assert "components" in result
        assert result["system_info"] == mock_system_info

        # Ellenőrizzük, hogy a gyorsítótárba mentés megtörtént
        assert service._cached_data["overview"] == result

    def test_get_performance_metrics_with_resources(self, mock_bridge: MagicMock) -> None:
        """Teszteli a teljesítmény metrikák lekérdezését resources adatokkal."""
        mock_system_info = {
            "resources": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4,
            }
        }
        mock_bridge.get_system_info.return_value = mock_system_info

        service = DashboardService(mock_bridge)
        result = service.get_performance_metrics()

        assert result["cpu_usage"] == 45.2
        assert result["memory_usage"] == 67.8
        assert result["disk_usage"] == 23.4
        assert "network_io" in result
        assert "disk_io" in result
        assert "response_time" in result

        # Ellenőrizzük, hogy a gyorsítótárba mentés megtörtént
        assert service._cached_data["metrics"] == result

    def test_get_performance_metrics_without_resources(self, mock_bridge: MagicMock) -> None:
        """Teszteli a teljesítmény metrikák lekérdezését resources adatok nélkül."""
        mock_bridge.get_system_info.return_value = {}

        service = DashboardService(mock_bridge)
        result = service.get_performance_metrics()

        # Ellenőrizzük, hogy a fallback értékeket használja
        assert result["cpu_usage"] == 45.2
        assert result["memory_usage"] == 67.8
        assert result["disk_usage"] == 23.4

    def test_get_recent_activities(self, mock_bridge: MagicMock) -> None:
        """Teszteli a legutóbbi tevékenységek lekérdezését."""
        service = DashboardService(mock_bridge)
        result = service.get_recent_activities()

        assert isinstance(result, list)
        assert len(result) == 4

        # Ellenőrizzük az első tevékenységet
        first_activity = result[0]
        assert first_activity["type"] == "INFO"
        assert first_activity["message"] == "Rendszer indítva"
        assert first_activity["component"] == "core"

        # Ellenőrizzük, hogy a gyorsítótárba mentés megtörtént
        assert service._cached_data["activities"] == result

    def test_refresh_data(self, mock_bridge: MagicMock) -> None:
        """Teszteli a dashboard adatok frissítését."""
        service = DashboardService(mock_bridge)

        # Töltsük fel a gyorsítótárat
        service._cached_data = {
            "overview": {"test": "data"},
            "health": {"core": "OK"},
            "metrics": {"cpu": 45.2},
            "activities": [{"test": "activity"}],
        }

        # Mock a feliratkozókat
        mock_callback = MagicMock()
        service._subscribers = [mock_callback]

        service.refresh_data()

        # Ellenőrizzük, hogy a gyorsítótár kiürült
        assert service._cached_data == {}

        # Ellenőrizzük, hogy a feliratkozókat értesítettük
        mock_callback.assert_called_once()
        call_args = mock_callback.call_args[0][0]
        assert call_args["type"] == "refresh"
        assert "timestamp" in call_args

    def test_subscribe_to_updates(self, mock_bridge: MagicMock) -> None:
        """Teszteli a feliratkozást dashboard frissítésekre."""
        service = DashboardService(mock_bridge)

        # Mock callback függvény
        mock_callback = MagicMock()

        service.subscribe_to_updates(mock_callback)

        # Ellenőrizzük, hogy a feliratkozó hozzáadásra került
        assert len(service._subscribers) == 1
        assert service._subscribers[0] == mock_callback

    def test_notify_subscribers(self, mock_bridge: MagicMock) -> None:
        """Teszteli a feliratkozók értesítését."""
        service = DashboardService(mock_bridge)

        # Mock callback függvények
        mock_callback1 = MagicMock()
        mock_callback2 = MagicMock()
        service._subscribers = [mock_callback1, mock_callback2]

        test_data = {"type": "test", "data": "test_value"}
        service._notify_subscribers(test_data)

        # Ellenőrizzük, hogy minden feliratkozót értesítettünk
        mock_callback1.assert_called_once_with(test_data)
        mock_callback2.assert_called_once_with(test_data)

    def test_notify_subscribers_with_exception(self, mock_bridge: MagicMock) -> None:
        """Teszteli a feliratkozók értesítését, ha egy callback hibát dob."""
        service = DashboardService(mock_bridge)

        # Mock callback, ami hibát dob
        def failing_callback(data: dict[str, Any]) -> None:
            raise ValueError("Test error")

        mock_callback = MagicMock()
        service._subscribers = [failing_callback, mock_callback]

        # A metódusnak nem szabad hibát dobnia, még ha egy callback hibás is
        test_data = {"type": "test"}
        service._notify_subscribers(test_data)

        # Ellenőrizzük, hogy a második callback még mindig meghívódott
        mock_callback.assert_called_once_with(test_data)

    def test_cached_data_persistence(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy az adatok tényleg gyorsítótárazásra kerülnek."""
        mock_bridge.get_system_info.return_value = {"test": "data"}

        service = DashboardService(mock_bridge)

        # Első hívás
        result1 = service.get_system_overview()

        # Módosítjuk a mock-ot, hogy lássuk, a második hívás nem használja
        mock_bridge.get_system_info.return_value = {"different": "data"}

        # Második hívás - a gyorsítótárazott adatot kell visszaadnia
        result2 = service.get_system_overview()

        assert result1 == result2
        assert result1["system_info"]["test"] == "data"
