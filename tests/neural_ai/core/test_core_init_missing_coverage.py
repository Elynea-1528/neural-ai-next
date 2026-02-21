"""Tesztek a neural_ai.core.__init__.py hiányzó coverage ágaihoz.

Ez a tesztmodul kiegészíti a test_core_init.py-t, és a következő
hiányzó ágakat fedi le:
- Storage inicializálási hiba (144-147)
- JForex Live Feed inicializálás (200-202)
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core import bootstrap_core


class TestBootstrapCoreStorageError:
    """Tesztek a bootstrap_core storage hibakezelésére."""

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.utils.factory.HardwareFactory")
    @patch("neural_ai.core.db.factory.DatabaseFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.data.storage.factory.StorageFactory")
    def test_bootstrap_core_storage_init_failure(
        self,
        mock_storage_factory: MagicMock,
        mock_event_factory: MagicMock,
        mock_db_factory: MagicMock,
        mock_hardware_factory: MagicMock,
        mock_logger_factory: MagicMock,
        mock_config_factory: MagicMock,
        mock_di_container: MagicMock,
    ) -> None:
        """Teszteli a bootstrap_core függvényt storage inicializálási hiba esetén.

        Ez a teszt lefedi a 144-147 sorokat (storage exception handling).
        """
        # Mock beállítások
        mock_container = MagicMock()
        mock_di_container.return_value = mock_container

        mock_hardware = MagicMock()
        mock_hardware_factory.get_hardware_info.return_value = mock_hardware

        mock_config = MagicMock()
        mock_config.get.side_effect = lambda key, *args: {
            "logging": {"level": "INFO", "format": "json"},
            "storage": {"type": "parquet", "base_path": "/tmp/test"},
        }.get(key, {})
        mock_config_factory.create_manager.return_value = mock_config

        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_db_factory_instance = MagicMock()
        mock_database = MagicMock()
        mock_db_factory_instance.create_manager.return_value = mock_database
        mock_db_factory.return_value = mock_db_factory_instance

        mock_event_factory_instance = MagicMock()
        mock_event_bus = MagicMock()
        mock_event_factory_instance.create_from_config.return_value = mock_event_bus
        mock_event_factory.return_value = mock_event_factory_instance

        # Storage factory dobjon hibát
        mock_storage_factory.get_storage.side_effect = RuntimeError("Storage init failed")

        # Bootstrap hívás - várjuk a hibát
        with pytest.raises(RuntimeError, match="Storage init failed"):
            bootstrap_core()

        # Ellenőrizzük, hogy a logger.critical hívódott
        mock_logger.critical.assert_called_once()
        assert "Storage init failed" in str(mock_logger.critical.call_args)


class TestBootstrapCoreJForexLiveFeed:
    """Tesztek a bootstrap_core JForex Live Feed inicializálására."""

    @patch("neural_ai.core.base.implementations.di_container.DIContainer")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.core.utils.factory.HardwareFactory")
    @patch("neural_ai.core.db.factory.DatabaseFactory")
    @patch("neural_ai.core.events.factory.EventBusFactory")
    @patch("neural_ai.data.storage.factory.StorageFactory")
    @patch("neural_ai.core.system.factory.SystemComponentFactory")
    @patch("neural_ai.data.ingestion.market_data_persister.MarketDataPersister")
    @patch("neural_ai.collectors.jforex.factory.JForexFactory")
    def test_bootstrap_core_jforex_live_feed_enabled(
        self,
        mock_jforex_factory: MagicMock,
        mock_persister: MagicMock,
        mock_system_factory: MagicMock,
        mock_storage_factory: MagicMock,
        mock_event_factory: MagicMock,
        mock_db_factory: MagicMock,
        mock_hardware_factory: MagicMock,
        mock_logger_factory: MagicMock,
        mock_config_factory: MagicMock,
        mock_di_container: MagicMock,
    ) -> None:
        """Teszteli a bootstrap_core függvényt JForex Live Feed engedélyezve esetén.

        Ez a teszt lefedi a 200-202 sorokat (JForex live feed init).
        """
        # Mock beállítások
        mock_container = MagicMock()
        mock_di_container.return_value = mock_container

        mock_hardware = MagicMock()
        mock_hardware_factory.get_hardware_info.return_value = mock_hardware

        mock_config = MagicMock()
        def mock_get(key: str, subkey: str | None = None) -> dict:
            data = {
                "logging": {"level": "INFO", "format": "json"},
                "storage": {"type": "parquet", "base_path": "/tmp/test"},
                "collectors": {
                    "jforex_live": {
                        "enabled": True,
                        "host": "localhost",
                        "tick_port": 5555,
                        "command_port": 5556,
                    }
                },
            }
            if subkey:
                return data.get(key, {}).get(subkey, {})
            return data.get(key, {})

        mock_config.get.side_effect = mock_get
        mock_config.get_section.side_effect = lambda key: {
            "ingestion": {
                "buffer_size": 1000,
                "flush_interval": 60,
            }
        }.get(key, {})
        mock_config_factory.create_manager.return_value = mock_config

        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_db_factory_instance = MagicMock()
        mock_database = MagicMock()
        mock_db_factory_instance.create_manager.return_value = mock_database
        mock_db_factory.return_value = mock_db_factory_instance

        mock_event_factory_instance = MagicMock()
        mock_event_bus = MagicMock()
        mock_event_factory_instance.create_from_config.return_value = mock_event_bus
        mock_event_factory.return_value = mock_event_factory_instance

        mock_storage = MagicMock()
        mock_storage_factory.get_storage.return_value = mock_storage

        mock_health_monitor = MagicMock()
        mock_system_factory.create_health_monitor.return_value = mock_health_monitor

        mock_live_feed = MagicMock()
        mock_jforex_factory.create_live_feed.return_value = mock_live_feed

        # Bootstrap hívás
        result = bootstrap_core()

        # Ellenőrizzük, hogy a JForex Live Feed létrejött
        mock_jforex_factory.create_live_feed.assert_called_once_with(
            mock_config, mock_logger, mock_event_bus
        )

        # Ellenőrizzük, hogy a logger.info hívódott a JForex inicializálásról
        info_calls = [str(call) for call in mock_logger.info.call_args_list]
        assert any("JForex Live Feed inicializálva" in call for call in info_calls)

        # Ellenőrizzük, hogy a CoreComponents visszatért
        assert result is not None
