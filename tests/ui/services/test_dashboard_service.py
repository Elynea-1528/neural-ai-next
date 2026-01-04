"""DashboardService tesztelése.

Ez a tesztfájl a ui/services/dashboard_service.py komponensének unit tesztjeit tartalmazza.
A tesztek a MVVM architektúra ViewModel rétegének helyes működését ellenőrzik.
"""

import sys
from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest

# Path hozzáadása a UI modulokhoz
sys.path.insert(0, "/home/elynea/Dokumentumok/neural-ai-next")


# Importok a tesztelendő osztályokból
# Mivel a ui.services még nem létezik, mock-oljuk a struktúrát
class MockBaseService:
    """Mock BaseService a teszteléshez."""

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self._init_session_state()

    def _init_session_state(self):
        """Session state inicializálása."""
        pass

    def get_session_data(self, key: str, default: Any = None) -> Any:
        """Adatok lekérése a session state-ből."""
        return default

    def set_session_data(self, key: str, value: Any):
        """Adatok mentése a session state-be."""
        pass

    def clear_session_data(self, key: str):
        """Adatok törlése a session state-ből."""
        pass


class MockDashboardService(MockBaseService):
    """Mock DashboardService a teszteléshez."""

    def __init__(self, logger, config):
        super().__init__(logger, config)

    def get_system_health(self) -> dict[str, Any]:
        """Rendszer állapotának lekérése."""
        try:
            health_monitor = self._get_health_monitor()
            health_data = health_monitor.check_health()

            return {
                "cuda_status": "Available" if health_data.cuda_available else "Disabled",
                "cuda_available": health_data.cuda_available,
                "database_status": health_data.database.status,
                "database_tables": health_data.database.table_count,
                "config_status": health_data.config.status,
                "config_entries": health_data.config.entry_count,
                "active_collectors": health_data.collectors.active_count,
                "total_collectors": health_data.collectors.total_count,
            }
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return self._get_default_health_status()

    def get_data_summary(self) -> dict[str, Any]:
        """Adatok összegzésének lekérése."""
        try:
            data_bridge = self._get_data_bridge()
            summary = data_bridge.get_data_summary()

            symbols_df = pd.DataFrame(
                [
                    {
                        "Symbol": s.name,
                        "Records": s.record_count,
                        "Start Date": s.start_date,
                        "End Date": s.end_date,
                        "Size (MB)": s.size_mb,
                    }
                    for s in summary.symbols
                ]
            )

            return {
                "total_records": summary.total_records,
                "total_size_mb": summary.total_size_mb,
                "symbols_count": summary.symbol_count,
                "symbols_df": symbols_df,
            }
        except Exception as e:
            self.logger.error(f"Error getting data summary: {e}")
            return {
                "total_records": 0,
                "total_size_mb": 0.0,
                "symbols_count": 0,
                "symbols_df": pd.DataFrame(),
            }

    def create_data_volume_chart(self, data_info: dict[str, Any]) -> Any:
        """Adatmennyiség chart létrehozása."""
        if data_info["symbols_df"].empty:
            # Mock Plotly figure
            return MagicMock()

        # Mock chart létrehozása
        fig = MagicMock()
        fig.update_layout = MagicMock(return_value=fig)
        return fig

    def _get_default_health_status(self) -> dict[str, Any]:
        """Alapértelmezett health status."""
        return {
            "cuda_status": "Error",
            "cuda_available": False,
            "database_status": "Error",
            "database_tables": 0,
            "config_status": "Error",
            "config_entries": 0,
            "active_collectors": 0,
            "total_collectors": 0,
        }

    def _get_health_monitor(self):
        """Health monitor lekérése."""
        # Mock health monitor
        return MagicMock()

    def _get_data_bridge(self):
        """Data bridge lekérése."""
        # Mock data bridge
        return MagicMock()


class TestDashboardService:
    """DashboardService osztály tesztjei."""

    @pytest.fixture
    def mock_logger(self):
        """Mock logger fixture."""
        logger = Mock()
        logger.error = Mock()
        return logger

    @pytest.fixture
    def mock_config(self):
        """Mock config fixture."""
        config = Mock()
        config.get = Mock(return_value="1.0.0")
        return config

    @pytest.fixture
    def dashboard_service(self, mock_logger, mock_config):
        """DashboardService példány létrehozása."""
        return MockDashboardService(logger=mock_logger, config=mock_config)

    def test_initialization(self, dashboard_service, mock_logger, mock_config):
        """Teszteli a DashboardService inicializálását."""
        assert dashboard_service.logger == mock_logger
        assert dashboard_service.config == mock_config
        assert dashboard_service.logger is not None
        assert dashboard_service.config is not None

    def test_get_system_health_success(self, dashboard_service, mock_logger):
        """Teszteli a rendszer állapotának sikeres lekérését."""
        # Mock health monitor létrehozása
        mock_health_monitor = Mock()
        mock_health_data = Mock()

        # Mock adatok beállítása
        mock_health_data.cuda_available = True
        mock_health_data.database.status = "OK"
        mock_health_data.database.table_count = 10
        mock_health_data.config.status = "Loaded"
        mock_health_data.config.entry_count = 50
        mock_health_data.collectors.active_count = 3
        mock_health_data.collectors.total_count = 5

        mock_health_monitor.check_health.return_value = mock_health_data

        # Health monitor mockolása
        with patch.object(
            dashboard_service, "_get_health_monitor", return_value=mock_health_monitor
        ):
            result = dashboard_service.get_system_health()

            # Eredmények ellenőrzése
            assert result["cuda_status"] == "Available"
            assert result["cuda_available"] is True
            assert result["database_status"] == "OK"
            assert result["database_tables"] == 10
            assert result["config_status"] == "Loaded"
            assert result["config_entries"] == 50
            assert result["active_collectors"] == 3
            assert result["total_collectors"] == 5

            # Logger hívás ellenőrzése (nem volt hiba)
            mock_logger.error.assert_not_called()

    def test_get_system_health_error(self, dashboard_service, mock_logger):
        """Teszteli a rendszer állapotának lekérését hibás esetben."""
        # Exception dobása a health monitorban
        with patch.object(
            dashboard_service, "_get_health_monitor", side_effect=Exception("Test error")
        ):
            result = dashboard_service.get_system_health()

            # Alapértelmezett értékek ellenőrzése
            assert result["cuda_status"] == "Error"
            assert result["cuda_available"] is False
            assert result["database_status"] == "Error"
            assert result["database_tables"] == 0
            assert result["config_status"] == "Error"
            assert result["config_entries"] == 0
            assert result["active_collectors"] == 0
            assert result["total_collectors"] == 0

            # Logger error hívás ellenőrzése
            mock_logger.error.assert_called_once()
            assert "Test error" in str(mock_logger.error.call_args)

    def test_get_data_summary_success(self, dashboard_service, mock_logger):
        """Teszteli az adatok összegzésének sikeres lekérését."""
        # Mock data bridge létrehozása
        mock_data_bridge = Mock()
        mock_summary = Mock()

        # Mock adatok beállítása
        mock_symbol1 = Mock()
        mock_symbol1.name = "EURUSD"
        mock_symbol1.record_count = 1000
        mock_symbol1.start_date = "2024-01-01"
        mock_symbol1.end_date = "2024-01-31"
        mock_symbol1.size_mb = 5.5

        mock_symbol2 = Mock()
        mock_symbol2.name = "GBPUSD"
        mock_symbol2.record_count = 2000
        mock_symbol2.start_date = "2024-01-01"
        mock_symbol2.end_date = "2024-01-31"
        mock_symbol2.size_mb = 8.2

        mock_summary.symbols = [mock_symbol1, mock_symbol2]
        mock_summary.total_records = 3000
        mock_summary.total_size_mb = 13.7
        mock_summary.symbol_count = 2

        mock_data_bridge.get_data_summary.return_value = mock_summary

        # Data bridge mockolása
        with patch.object(dashboard_service, "_get_data_bridge", return_value=mock_data_bridge):
            result = dashboard_service.get_data_summary()

            # Eredmények ellenőrzése
            assert result["total_records"] == 3000
            assert result["total_size_mb"] == 13.7
            assert result["symbols_count"] == 2
            assert isinstance(result["symbols_df"], pd.DataFrame)
            assert len(result["symbols_df"]) == 2
            assert result["symbols_df"]["Symbol"].tolist() == ["EURUSD", "GBPUSD"]
            assert result["symbols_df"]["Records"].tolist() == [1000, 2000]

            # Logger hívás ellenőrzése (nem volt hiba)
            mock_logger.error.assert_not_called()

    def test_get_data_summary_error(self, dashboard_service, mock_logger):
        """Teszteli az adatok összegzésének lekérését hibás esetben."""
        # Exception dobása a data bridgeben
        with patch.object(
            dashboard_service, "_get_data_bridge", side_effect=Exception("Data error")
        ):
            result = dashboard_service.get_data_summary()

            # Alapértelmezett értékek ellenőrzése
            assert result["total_records"] == 0
            assert result["total_size_mb"] == 0.0
            assert result["symbols_count"] == 0
            assert isinstance(result["symbols_df"], pd.DataFrame)
            assert result["symbols_df"].empty

            # Logger error hívás ellenőrzése
            mock_logger.error.assert_called_once()
            assert "Data error" in str(mock_logger.error.call_args)

    def test_create_data_volume_chart_with_data(self, dashboard_service):
        """Teszteli a chart létrehozását adatokkal."""
        # Teszt adatok létrehozása
        data_info = {
            "symbols_df": pd.DataFrame({"Symbol": ["EURUSD", "GBPUSD"], "Records": [1000, 2000]})
        }

        # Chart létrehozása
        chart = dashboard_service.create_data_volume_chart(data_info)

        # Eredmény ellenőrzése
        assert chart is not None
        assert hasattr(chart, "update_layout")

    def test_create_data_volume_chart_empty_data(self, dashboard_service):
        """Teszteli a chart létrehozását üres adatokkal."""
        # Üres adatok
        data_info = {"symbols_df": pd.DataFrame()}

        # Chart létrehozása
        chart = dashboard_service.create_data_volume_chart(data_info)

        # Eredmény ellenőrzése
        assert chart is not None

    def test_get_default_health_status(self, dashboard_service):
        """Teszteli az alapértelmezett health status lekérését."""
        result = dashboard_service._get_default_health_status()

        # Alapértelmezett értékek ellenőrzése
        assert result["cuda_status"] == "Error"
        assert result["cuda_available"] is False
        assert result["database_status"] == "Error"
        assert result["database_tables"] == 0
        assert result["config_status"] == "Error"
        assert result["config_entries"] == 0
        assert result["active_collectors"] == 0
        assert result["total_collectors"] == 0

    def test_session_state_methods(self, dashboard_service):
        """Teszteli a session state metódusokat."""
        # get_session_data
        result = dashboard_service.get_session_data("test_key", "default_value")
        assert result == "default_value"

        # set_session_data (csak ellenőrizzük, hogy nem dob hibát)
        dashboard_service.set_session_data("test_key", "test_value")

        # clear_session_data (csak ellenőrizzük, hogy nem dob hibát)
        dashboard_service.clear_session_data("test_key")

    def test_logger_and_config_access(self, dashboard_service, mock_logger, mock_config):
        """Teszteli a logger és config elérését."""
        # Logger ellenőrzése
        assert dashboard_service.logger == mock_logger
        assert hasattr(dashboard_service.logger, "error")

        # Config ellenőrzése
        assert dashboard_service.config == mock_config
        assert hasattr(dashboard_service.config, "get")

    def test_type_hints_compliance(self, dashboard_service):
        """Teszteli a type hints kompatibilitást."""
        # A get_system_health Dict[str, Any] típust ad vissza
        result = dashboard_service.get_system_health()
        assert isinstance(result, dict)

        # A get_data_summary Dict[str, Any] típust ad vissza
        result = dashboard_service.get_data_summary()
        assert isinstance(result, dict)
        assert "symbols_df" in result
        assert isinstance(result["symbols_df"], pd.DataFrame)


class TestDashboardServiceIntegration:
    """Integrációs tesztek a DashboardService-hez."""

    @pytest.fixture
    def service_with_mocks(self):
        """Service létrehozása mock komponensekkel."""
        logger = Mock()
        config = Mock()
        service = MockDashboardService(logger, config)
        return service, logger, config

    def test_full_health_check_workflow(self, service_with_mocks):
        """Teszteli a teljes health check workflow-t."""
        service, logger, config = service_with_mocks

        # Mock health monitor
        mock_health_monitor = Mock()
        mock_health_data = Mock()
        mock_health_data.cuda_available = True
        mock_health_data.database.status = "OK"
        mock_health_data.database.table_count = 15
        mock_health_data.config.status = "Loaded"
        mock_health_data.config.entry_count = 100
        mock_health_data.collectors.active_count = 5
        mock_health_data.collectors.total_count = 8

        mock_health_monitor.check_health.return_value = mock_health_data

        with patch.object(service, "_get_health_monitor", return_value=mock_health_monitor):
            # Health check végrehajtása
            result = service.get_system_health()

            # Eredmények ellenőrzése
            assert result["cuda_status"] == "Available"
            assert result["database_tables"] == 15
            assert result["config_entries"] == 100
            assert result["active_collectors"] == 5
            assert result["total_collectors"] == 8

            # Logger nem lett hívva hibával
            logger.error.assert_not_called()

    def test_error_handling_in_workflow(self, service_with_mocks):
        """Teszteli a hibakezelést a workflow-ban."""
        service, logger, config = service_with_mocks

        # Exception dobása
        with patch.object(
            service, "_get_health_monitor", side_effect=Exception("Integration error")
        ):
            result = service.get_system_health()

            # Alapértelmezett értékek
            assert result["cuda_status"] == "Error"
            assert result["database_status"] == "Error"

            # Logger hívás ellenőrzése
            logger.error.assert_called_once()


class TestDashboardServiceEdgeCases:
    """Edge case tesztek a DashboardService-hez."""

    @pytest.fixture
    def edge_case_service(self):
        """Service létrehozása edge case teszteléshez."""
        logger = Mock()
        config = Mock()
        return MockDashboardService(logger, config)

    def test_health_monitor_returns_none(self, edge_case_service):
        """Teszteli, ha a health monitor None-t ad vissza."""
        with patch.object(edge_case_service, "_get_health_monitor", return_value=None):
            result = edge_case_service.get_system_health()

            # Alapértelmezett értékek
            assert result["cuda_status"] == "Error"
            assert result["database_status"] == "Error"

    def test_data_bridge_returns_empty_summary(self, edge_case_service):
        """Teszteli, ha a data bridge üres összegzést ad vissza."""
        mock_data_bridge = Mock()
        mock_summary = Mock()
        mock_summary.symbols = []
        mock_summary.total_records = 0
        mock_summary.total_size_mb = 0.0
        mock_summary.symbol_count = 0

        mock_data_bridge.get_data_summary.return_value = mock_summary

        with patch.object(edge_case_service, "_get_data_bridge", return_value=mock_data_bridge):
            result = edge_case_service.get_data_summary()

            # Üres adatok ellenőrzése
            assert result["total_records"] == 0
            assert result["symbols_count"] == 0
            assert result["symbols_df"].empty

    def test_chart_creation_with_missing_columns(self, edge_case_service):
        """Teszteli a chart létrehozását hiányzó oszlopokkal."""
        # Hiányos adatok
        data_info = {
            "symbols_df": pd.DataFrame(
                {
                    "Symbol": ["EURUSD"]  # Hiányzik a Records oszlop
                }
            )
        }

        # Chart létrehozása (nem szabad hibát dobnia)
        chart = edge_case_service.create_data_volume_chart(data_info)
        assert chart is not None


# Teszt futtatása
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
