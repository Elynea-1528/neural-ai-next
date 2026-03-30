"""Unit tesztek a core_bridge modulhoz.

Ez a modul teszteli a CoreBridge osztály funkcióit.
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.ui.core_bridge import CoreBridge


class TestCoreBridgeInit:
    """Tesztek a CoreBridge inicializálásához."""

    def test_init_creates_instance(self) -> None:
        """Ellenőrzi, hogy a CoreBridge létrehozható."""
        # Act
        bridge = CoreBridge()

        # Assert
        assert bridge._core is None
        assert bridge._connected is False
        assert bridge._strategy_service is None

    def test_get_instance_returns_self(self) -> None:
        """Ellenőrzi, hogy a get_instance visszaadja a példányt."""
        # Arrange
        bridge = CoreBridge()

        # Act
        result = bridge.get_instance()

        # Assert
        assert result == bridge


class TestCoreBridgeInitialize:
    """Tesztek a CoreBridge.initialize metódushoz."""

    @patch("neural_ai.core.bootstrap_core")
    def test_initialize_success(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy az initialize sikeresen inicializálja a bridge-t."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()

        # Act
        bridge.initialize()

        # Assert
        assert bridge._connected is True
        assert bridge._core == mock_core
        mock_bootstrap.assert_called_once()
        mock_core.logger.info.assert_called()

    @patch("neural_ai.core.bootstrap_core")
    def test_initialize_calls_strategy_service_init(
        self, mock_bootstrap: MagicMock
    ) -> None:
        """Ellenőrzi, hogy az initialize meghívja a strategy service inicializálást."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()

        # Act
        with patch.object(bridge, "_initialize_strategy_service") as mock_init_strategy:
            bridge.initialize()

        # Assert
        mock_init_strategy.assert_called_once()


class TestCoreBridgeGetComponent:
    """Tesztek a CoreBridge.get_component metódushoz."""

    def test_get_component_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy a get_component hibát dob inicializálás nélkül."""
        # Arrange
        bridge = CoreBridge()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Core Bridge nincs inicializálva"):
            bridge.get_component("parquet_storage")

    @patch("neural_ai.core.bootstrap_core")
    def test_get_component_parquet_storage(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a get_component visszaadja a parquet storage-t."""
        # Arrange
        mock_core = MagicMock()
        mock_storage = MagicMock()
        mock_core.storage = mock_storage
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.get_component("parquet_storage")

        # Assert
        assert result == mock_storage

    @patch("neural_ai.core.bootstrap_core")
    def test_get_component_config(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a get_component visszaadja a config-ot."""
        # Arrange
        mock_core = MagicMock()
        mock_config = MagicMock()
        mock_core.config = mock_config
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.get_component("config")

        # Assert
        assert result == mock_config

    @patch("neural_ai.core.bootstrap_core")
    def test_get_component_logger(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a get_component visszaadja a logger-t."""
        # Arrange
        mock_core = MagicMock()
        mock_logger = MagicMock()
        mock_core.logger = mock_logger
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.get_component("logger")

        # Assert
        assert result == mock_logger

    @patch("neural_ai.core.bootstrap_core")
    def test_get_component_unknown_type(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a get_component None-t ad vissza ismeretlen típusra."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.get_component("unknown_type")

        # Assert
        assert result is None
        mock_core.logger.warning.assert_called_once()


class TestCoreBridgeSendCommand:
    """Tesztek a CoreBridge.send_command metódushoz."""

    def test_send_command_returns_error_when_not_connected(self) -> None:
        """Ellenőrzi, hogy a send_command hibát ad vissza kapcsolat nélkül."""
        # Arrange
        bridge = CoreBridge()

        # Act
        result = bridge.send_command("test_command", {})

        # Assert
        assert result == {"error": "Bridge not connected"}

    @patch("neural_ai.core.bootstrap_core")
    def test_send_command_success(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a send_command sikeresen küld parancsot."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.send_command("test_command", {"param1": "value1"})

        # Assert
        assert result["command"] == "test_command"
        assert result["params"] == {"param1": "value1"}
        assert result["status"] == "success"
        mock_core.logger.info.assert_called()


class TestCoreBridgeGetSystemInfo:
    """Tesztek a CoreBridge.get_system_info metódushoz."""

    def test_get_system_info_returns_error_when_not_connected(self) -> None:
        """Ellenőrzi, hogy a get_system_info hibát ad vissza kapcsolat nélkül."""
        # Arrange
        bridge = CoreBridge()

        # Act
        result = bridge.get_system_info()

        # Assert
        assert result == {"error": "Bridge not connected"}

    @patch("neural_ai.core.bootstrap_core")
    def test_get_system_info_success(self, mock_bootstrap: MagicMock) -> None:
        """Ellenőrzi, hogy a get_system_info visszaadja a rendszerinformációt."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_core.database = MagicMock()
        mock_core.event_bus = MagicMock()
        mock_core.storage = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()
        bridge.initialize()

        # Act
        result = bridge.get_system_info()

        # Assert
        assert result["version"] == "6.0.0"
        assert result["status"] == "running"
        assert "components" in result
        assert "resources" in result
        mock_core.logger.info.assert_called()


class TestCoreBridgeProperties:
    """Tesztek a CoreBridge property-khez."""

    def test_is_connected_default_false(self) -> None:
        """Ellenőrzi, hogy az is_connected alapértelmezetten False."""
        # Arrange
        bridge = CoreBridge()

        # Act & Assert
        assert bridge.is_connected is False

    @patch("neural_ai.core.bootstrap_core")
    def test_is_connected_true_after_initialize(
        self, mock_bootstrap: MagicMock
    ) -> None:
        """Ellenőrzi, hogy az is_connected True az initialize után."""
        # Arrange
        mock_core = MagicMock()
        mock_core.logger = MagicMock()
        mock_bootstrap.return_value = mock_core

        bridge = CoreBridge()

        # Act
        bridge.initialize()

        # Assert
        assert bridge.is_connected is True

    def test_core_property_default_none(self) -> None:
        """Ellenőrzi, hogy a core property alapértelmezetten None."""
        # Arrange
        bridge = CoreBridge()

        # Act & Assert
        assert bridge.core is None

    def test_core_property_setter(self) -> None:
        """Ellenőrzi, hogy a core property setter működik."""
        # Arrange
        bridge = CoreBridge()
        mock_core = MagicMock()

        # Act
        bridge.core = mock_core

        # Assert
        assert bridge.core == mock_core

    def test_connected_property_setter(self) -> None:
        """Ellenőrzi, hogy a connected property setter működik."""
        # Arrange
        bridge = CoreBridge()

        # Act
        bridge.connected = True

        # Assert
        assert bridge.connected is True

    def test_strategy_service_property_default_none(self) -> None:
        """Ellenőrzi, hogy a strategy_service property alapértelmezetten None."""
        # Arrange
        bridge = CoreBridge()

        # Act & Assert
        assert bridge.strategy_service is None

    def test_strategy_service_property_setter(self) -> None:
        """Ellenőrzi, hogy a strategy_service property setter működik."""
        # Arrange
        bridge = CoreBridge()
        mock_service = MagicMock()

        # Act
        bridge.strategy_service = mock_service

        # Assert
        assert bridge.strategy_service == mock_service
