"""Unit tesztek a dashboard_service modulhoz.

# pyright: reportUnknownArgumentType=false
# Mock config dict type inference hibák.

Ez a modul teszteli a DashboardService osztály funkcióit.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthStatus,
    SystemHealth,
)
from neural_ai.ui.services.dashboard_service import DashboardService


class TestDashboardServiceInit:
    """Tesztek a DashboardService inicializálásához."""

    def test_init_creates_instance(self) -> None:
        """Ellenőrzi, hogy a DashboardService létrehozható."""
        # Arrange
        mock_logger = MagicMock()
        mock_config = {}
        mock_core = MagicMock()

        # Act
        service = DashboardService(  # pyright: ignore[reportUnknownArgumentType]
            logger=mock_logger,
            config=mock_config,
            core_components=mock_core,
        )

        # Assert
        assert service._logger == mock_logger  # type: ignore
        assert service._config == mock_config  # type: ignore
        assert service._core_components == mock_core  # type: ignore
        assert service._cached_data == {}  # type: ignore
        assert service._subscribers == []  # type: ignore


class TestDashboardServiceGetSystemOverview:
    """Tesztek a get_system_overview metódushoz."""

    def test_get_system_overview_returns_data(self) -> None:
        """Ellenőrzi, hogy a system overview adatokat ad vissza."""
        # Arrange
        mock_core = MagicMock()
        mock_core.get_system_info.return_value = {"version": "1.0.0"}
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_system_overview()

        # Assert
        assert "system_info" in result
        assert "last_update" in result
        assert "components" in result
        mock_core.get_system_info.assert_called_once()

    def test_get_system_overview_uses_cache(self) -> None:
        """Ellenőrzi, hogy a system overview cache-t használ."""
        # Arrange
        mock_core = MagicMock()
        mock_core.get_system_info.return_value = {"version": "1.0.0"}
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result1 = service.get_system_overview()
        result2 = service.get_system_overview()

        # Assert
        assert result1 == result2
        mock_core.get_system_info.assert_called_once()  # Csak egyszer hívódik


class TestDashboardServiceGetHealthStatus:
    """Tesztek a get_health_status metódushoz."""

    def test_get_health_status_returns_unknown_when_no_health_monitor(self) -> None:
        """Ellenőrzi, hogy UNKNOWN-t ad vissza, ha nincs health monitor."""
        # Arrange
        mock_core = MagicMock()
        mock_core.core = None
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_health_status()

        # Assert
        assert result == {"system": "UNKNOWN"}

    def test_get_health_status_returns_status_map(self) -> None:
        """Ellenőrzi, hogy a health status térképet ad vissza."""
        # Arrange
        mock_health_monitor = MagicMock()
        mock_health = SystemHealth(
            overall_status=HealthStatus.OK,
            message="System OK",
            timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
            components=[
                ComponentHealth(
                    name="database",
                    status=ComponentStatus.HEALTHY,
                    message="OK",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
                ComponentHealth(
                    name="event_bus",
                    status=ComponentStatus.WARNING,
                    message="Slow",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
            ],
        )
        mock_health_monitor.check_health = AsyncMock(return_value=mock_health)

        mock_core = MagicMock()
        mock_core.core.health_monitor = mock_health_monitor
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_health_status()

        # Assert
        assert result["database"] == "OK"
        assert result["event_bus"] == "WARNING"
        assert result["system"] == "OK"

    def test_get_health_status_maps_all_statuses(self) -> None:
        """Ellenőrzi, hogy minden ComponentStatus helyesen leképeződik."""
        # Arrange
        mock_health_monitor = MagicMock()
        mock_health = SystemHealth(
            overall_status=HealthStatus.CRITICAL,
            message="System Critical",
            timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
            components=[
                ComponentHealth(
                    name="comp1",
                    status=ComponentStatus.HEALTHY,
                    message="OK",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
                ComponentHealth(
                    name="comp2",
                    status=ComponentStatus.WARNING,
                    message="Warning",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
                ComponentHealth(
                    name="comp3",
                    status=ComponentStatus.CRITICAL,
                    message="Critical",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
                ComponentHealth(
                    name="comp4",
                    status=ComponentStatus.UNKNOWN,
                    message="Unknown",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
                ComponentHealth(
                    name="comp5",
                    status=ComponentStatus.OFFLINE,
                    message="Offline",
                    timestamp=datetime.fromisoformat("2026-01-04T19:13:00"),
                ),
            ],
        )
        mock_health_monitor.check_health = AsyncMock(return_value=mock_health)

        mock_core = MagicMock()
        mock_core.core.health_monitor = mock_health_monitor
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_health_status()

        # Assert
        assert result["comp1"] == "OK"
        assert result["comp2"] == "WARNING"
        assert result["comp3"] == "ERROR"
        assert result["comp4"] == "UNKNOWN"
        assert result["comp5"] == "OFFLINE"
        assert result["system"] == "CRITICAL"


class TestDashboardServiceGetPerformanceMetrics:
    """Tesztek a get_performance_metrics metódushoz."""

    def test_get_performance_metrics_returns_data_from_system_info(self) -> None:
        """Ellenőrzi, hogy a performance metrics adatokat ad vissza."""
        # Arrange
        mock_core = MagicMock()
        mock_core.get_system_info.return_value = {
            "resources": {
                "cpu_usage": 45.2,
                "memory_usage": 67.8,
                "disk_usage": 23.4,
            }
        }
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_performance_metrics()

        # Assert
        assert result["cpu_usage"] == 45.2
        assert result["memory_usage"] == 67.8
        assert result["disk_usage"] == 23.4
        assert "network_io" in result
        assert "disk_io" in result
        assert "response_time" in result

    def test_get_performance_metrics_returns_fallback_when_no_resources(self) -> None:
        """Ellenőrzi, hogy fallback adatokat ad vissza, ha nincs resources."""
        # Arrange
        mock_core = MagicMock()
        mock_core.get_system_info.return_value = {}
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )

        # Act
        result = service.get_performance_metrics()

        # Assert
        assert "cpu_usage" in result
        assert "memory_usage" in result
        assert "disk_usage" in result
        assert "network_io" in result
        assert "disk_io" in result
        assert "response_time" in result


class TestDashboardServiceGetRecentActivities:
    """Tesztek a get_recent_activities metódushoz."""

    def test_get_recent_activities_returns_list(self) -> None:
        """Ellenőrzi, hogy a recent activities listát ad vissza."""
        # Arrange
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act
        result = service.get_recent_activities()

        # Assert
        assert isinstance(result, list)
        assert len(result) > 0
        assert "timestamp" in result[0]
        assert "type" in result[0]
        assert "message" in result[0]
        assert "component" in result[0]


class TestDashboardServiceRefreshData:
    """Tesztek a refresh_data metódushoz."""

    def test_refresh_data_clears_cache(self) -> None:
        """Ellenőrzi, hogy a refresh_data törli a cache-t."""
        # Arrange
        mock_core = MagicMock()
        mock_core.get_system_info.return_value = {"version": "1.0.0"}
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=mock_core,
        )
        service.get_system_overview()  # Cache-be tesz adatokat

        # Act
        service.refresh_data()

        # Assert
        assert service._cached_data == {}  # type: ignore

    def test_refresh_data_notifies_subscribers(self) -> None:
        """Ellenőrzi, hogy a refresh_data értesíti a feliratkozókat."""
        # Arrange
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_callback = MagicMock()
        service.subscribe_to_updates(mock_callback)

        # Act
        service.refresh_data()

        # Assert
        mock_callback.assert_called_once()
        call_args = mock_callback.call_args[0][0]
        assert call_args["type"] == "refresh"
        assert "timestamp" in call_args


class TestDashboardServiceSubscribeToUpdates:
    """Tesztek a subscribe_to_updates metódushoz."""

    def test_subscribe_to_updates_adds_callback(self) -> None:
        """Ellenőrzi, hogy a feliratkozás hozzáadja a callback-et."""
        # Arrange
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_callback = MagicMock()

        # Act
        service.subscribe_to_updates(mock_callback)

        # Assert
        assert mock_callback in service._subscribers  # type: ignore

    def test_subscribe_callback_handles_exception(self) -> None:
        """Ellenőrzi, hogy a callback kivétel esetén sem állítja le a rendszert."""
        # Arrange
        service = DashboardService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        def failing_callback(data: dict[str, object]) -> None:
            raise RuntimeError("Test error")

        service.subscribe_to_updates(failing_callback)

        # Act & Assert (nem dob kivételt)
        service.refresh_data()
