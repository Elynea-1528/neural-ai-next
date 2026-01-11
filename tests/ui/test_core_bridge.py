"""Core Bridge tesztesetek - teljes lefedettség biztosítása."""

from unittest.mock import Mock, call, patch

import pytest

from neural_ai.ui.core_bridge import CoreBridge


class TestCoreBridge:
    """CoreBridge osztály tesztelése."""

    @classmethod
    def setup_method(cls):
        """Reset singleton for test isolation."""
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        SingletonMeta._instance = None

    @classmethod
    def teardown_method(cls):
        """Clean up after each test."""
        bridge = CoreBridge()
        bridge._core = None
        bridge._connected = False
        bridge._strategy_service = None

    def test_singleton_pattern(self):
        """Singleton minta tesztelése."""
        bridge1 = CoreBridge()
        bridge2 = CoreBridge()

        assert bridge1 is bridge2
        assert bridge1.get_instance() is bridge1

    def test_initialization(self):
        """Inicializálás tesztelése."""
        bridge = CoreBridge()

        # Inicializálás előtt
        assert not bridge._connected
        assert bridge._core is None
        assert not bridge.is_connected

        # Mock bootstrap_core
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_core.logger = Mock()
            mock_bootstrap.return_value = mock_core

            bridge.initialize()

            assert bridge._connected
            assert bridge._core is mock_core
            assert bridge.is_connected
            mock_bootstrap.assert_called_once()
            mock_core.logger.info.assert_called_once_with("Core Bridge inicializálva")

    def test_initialization_strategy_service(self):
        """Strategy Service inicializálás tesztelése."""
        bridge = CoreBridge()

        with (
            patch("neural_ai.core.bootstrap_core") as mock_bootstrap,
            patch(
                "neural_ai.ui.services.strategy_service.StrategyService"
            ) as mock_strategy_service,
        ):
            mock_core = Mock()
            mock_core.logger = Mock()
            mock_bootstrap.return_value = mock_core
            mock_strategy = Mock()
            mock_strategy_service.return_value = mock_strategy

            bridge.initialize()

            mock_strategy_service.assert_called_once_with(bridge)
            assert bridge._strategy_service is mock_strategy
            mock_core.logger.debug.assert_called_once_with("Strategy Service inicializálva")

    def test_initialization_strategy_service_error(self):
        """Strategy Service inicializálási hiba tesztelése."""
        bridge = CoreBridge()

        with (
            patch("neural_ai.core.bootstrap_core") as mock_bootstrap,
            patch(
                "neural_ai.ui.services.strategy_service.StrategyService"
            ) as mock_strategy_service,
        ):
            mock_core = Mock()
            mock_core.logger = Mock()
            mock_bootstrap.return_value = mock_core
            mock_strategy_service.side_effect = Exception("Init error")

            bridge.initialize()

            mock_core.logger.error.assert_called_once()
            assert bridge._strategy_service is None

    def test_get_component_not_initialized(self):
        """Komponens lekérés inicializálatlan bridge esetén."""
        bridge = CoreBridge()

        with pytest.raises(RuntimeError, match="Core Bridge nincs inicializálva"):
            bridge.get_component("parquet_storage")

    def test_get_component_parquet_storage(self):
        """Parquet storage komponens lekérés tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_storage = Mock()
        mock_core.storage = mock_storage
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_component("parquet_storage")

        assert result is mock_storage
        mock_core.logger.debug.assert_called_once_with("Parquet storage komponens lekérve")

    def test_get_component_parquet_storage_none(self):
        """Parquet storage None esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_core.storage = None
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_component("parquet_storage")

        assert result is None

    def test_get_component_bi5_downloader(self):
        """BI5 downloader komponens létrehozás tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_config = Mock()
        mock_logger = Mock()
        mock_storage = Mock()
        mock_core.config = mock_config
        mock_core.logger = mock_logger
        mock_core.storage = mock_storage

        bridge._core = mock_core
        bridge._connected = True

        mock_downloader = Mock()
        with patch("neural_ai.collectors.jforex.factory.JForexFactory") as mock_factory:
            mock_factory.create_downloader.return_value = mock_downloader

            result = bridge.get_component("bi5_downloader")

            assert result is mock_downloader
            mock_factory.create_downloader.assert_called_once_with(
                config=mock_config, logger=mock_logger, event_bus=None, storage=mock_storage
            )
            mock_core.logger.debug.assert_has_calls(
                [
                    call("Parquet storage komponens lekérve"),
                    call("BI5 downloader komponens létrehozva"),
                ]
            )

    def test_get_component_bi5_downloader_missing_deps(self):
        """BI5 downloader hiányzó függőségekkel."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_core.config = None
        bridge._core = mock_core
        bridge._connected = True

        with patch("neural_ai.collectors.jforex.factory.JForexFactory"):
            result = bridge.get_component("bi5_downloader")

            assert result is None
            mock_core.logger.error.assert_called_once()

    def test_get_component_strategy_service(self):
        """Strategy Service komponens lekérés tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_strategy = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = True
        bridge._strategy_service = mock_strategy

        result = bridge.get_component("strategy_service")

        assert result is mock_strategy
        mock_core.logger.debug.assert_called_once_with("Strategy Service komponens lekérve")

    def test_get_component_strategy_service_none(self):
        """Strategy Service None esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = True
        bridge._strategy_service = None

        with patch(
            "neural_ai.ui.services.strategy_service.StrategyService",
            side_effect=Exception("Service error"),
        ):
            result = bridge.get_component("strategy_service")

            assert result is None
            mock_core.logger.warning.assert_called_once_with(
                "Strategy Service komponens nem elérhető"
            )

    def test_get_component_config(self):
        """Config komponens lekérés tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_config = Mock()
        mock_core.config = mock_config
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_component("config")

        assert result is mock_config

    def test_get_component_config_none(self):
        """Config None esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_core.config = None
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_component("config")

        assert result is None

    def test_get_component_unknown(self):
        """Ismeretlen komponens típus tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_component("unknown")

        assert result is None
        mock_core.logger.warning.assert_called_once_with("Ismeretlen komponens típus: unknown")

    def test_send_command_connected(self):
        """Parancs küldés csatlakoztatott bridge esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.send_command("test_command", {"param": "value"})

        expected = {
            "command": "test_command",
            "params": {"param": "value"},
            "status": "success",
            "timestamp": "2026-01-04T19:10:00Z",
        }
        assert result == expected
        mock_core.logger.info.assert_called_once_with("Parancs küldése: test_command")
        mock_core.logger.debug.assert_called_once()

    def test_send_command_not_connected(self):
        """Parancs küldés nem csatlakoztatott bridge esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = False

        result = bridge.send_command("test_command", {"param": "value"})

        assert result == {"error": "Bridge not connected"}

    def test_get_system_info_connected(self):
        """Rendszerinformáció lekérés csatlakoztatott bridge esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        mock_core.database = Mock()
        mock_core.event_bus = Mock()
        mock_core.storage = Mock()
        bridge._core = mock_core
        bridge._connected = True

        result = bridge.get_system_info()

        assert result["version"] == "6.0.0"
        assert result["status"] == "running"
        assert "components" in result
        assert "resources" in result
        mock_core.logger.info.assert_called_once_with("Rendszerinformáció lekérdezése")

    def test_get_system_info_not_connected(self):
        """Rendszerinformáció lekérés nem csatlakoztatott bridge esetén."""
        bridge = CoreBridge()

        mock_core = Mock()
        mock_core.logger = Mock()
        bridge._core = mock_core
        bridge._connected = False

        result = bridge.get_system_info()

        assert result == {"error": "Bridge not connected"}

    def test_core_property(self):
        """Core property tesztelése."""
        bridge = CoreBridge()

        mock_core = Mock()
        bridge._core = mock_core

        assert bridge.core is mock_core

    def test_is_connected_property(self):
        """is_connected property tesztelése."""
        bridge = CoreBridge()

        assert not bridge.is_connected
        bridge._connected = True
        assert bridge.is_connected
