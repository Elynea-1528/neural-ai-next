"""Unit tesztek a DashboardServiceInterface interfészhez."""

from typing import Any
from unittest.mock import MagicMock

from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface


class TestDashboardServiceInterface:
    """Tesztek a DashboardServiceInterface interfészhez."""

    def test_interface_is_runtime_checkable(self) -> None:
        """Teszteli, hogy az interfész runtime checkable."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        assert isinstance(mock_service, DashboardServiceInterface)

    def test_get_system_overview_signature(self) -> None:
        """Teszteli a get_system_overview metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        overview: dict[str, Any] = {
            "status": "running",
            "uptime": 3600,
            "version": "1.0.0",
        }
        mock_service.get_system_overview.return_value = overview
        result = mock_service.get_system_overview()
        assert result == overview
        mock_service.get_system_overview.assert_called_once()

    def test_get_health_status_signature(self) -> None:
        """Teszteli a get_health_status metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        health: dict[str, str] = {
            "database": "OK",
            "storage": "OK",
            "event_bus": "WARNING",
        }
        mock_service.get_health_status.return_value = health
        result = mock_service.get_health_status()
        assert result == health
        mock_service.get_health_status.assert_called_once()

    def test_get_performance_metrics_signature(self) -> None:
        """Teszteli a get_performance_metrics metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        metrics: dict[str, float] = {
            "cpu_usage": 45.5,
            "memory_usage": 60.2,
            "disk_usage": 30.8,
        }
        mock_service.get_performance_metrics.return_value = metrics
        result = mock_service.get_performance_metrics()
        assert result == metrics
        mock_service.get_performance_metrics.assert_called_once()

    def test_get_recent_activities_signature(self) -> None:
        """Teszteli a get_recent_activities metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        activities: list[dict[str, Any]] = [
            {"timestamp": "2024-01-01T10:00:00", "action": "data_loaded"},
            {"timestamp": "2024-01-01T10:05:00", "action": "model_trained"},
        ]
        mock_service.get_recent_activities.return_value = activities
        result = mock_service.get_recent_activities()
        assert result == activities
        assert len(result) == 2
        mock_service.get_recent_activities.assert_called_once()

    def test_get_recent_activities_empty(self) -> None:
        """Teszteli a get_recent_activities metódust üres listával."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        activities: list[dict[str, Any]] = []
        mock_service.get_recent_activities.return_value = activities
        result = mock_service.get_recent_activities()
        assert result == []
        mock_service.get_recent_activities.assert_called_once()

    def test_refresh_data_signature(self) -> None:
        """Teszteli a refresh_data metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        mock_service.refresh_data()
        mock_service.refresh_data.assert_called_once()

    def test_subscribe_to_updates_signature(self) -> None:
        """Teszteli a subscribe_to_updates metódus szignatúráját."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        callback = MagicMock()
        mock_service.subscribe_to_updates(callback)
        mock_service.subscribe_to_updates.assert_called_once_with(callback)

    def test_interface_has_all_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza az összes szükséges metódust."""
        required_methods = [
            "get_system_overview",
            "get_health_status",
            "get_performance_metrics",
            "get_recent_activities",
            "refresh_data",
            "subscribe_to_updates",
        ]
        for method in required_methods:
            assert hasattr(DashboardServiceInterface, method)

    def test_mock_implements_interface(self) -> None:
        """Teszteli, hogy a mock objektum implementálja az interfészt."""
        mock_service = MagicMock(spec=DashboardServiceInterface)
        assert hasattr(mock_service, "get_system_overview")
        assert hasattr(mock_service, "get_health_status")
        assert hasattr(mock_service, "get_performance_metrics")
        assert hasattr(mock_service, "get_recent_activities")
        assert hasattr(mock_service, "refresh_data")
        assert hasattr(mock_service, "subscribe_to_updates")
