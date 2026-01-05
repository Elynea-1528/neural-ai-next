"""Core Bridge tesztelése."""

from unittest.mock import Mock, patch

import pytest

from neural_ai.ui.core_bridge import CoreBridge


class TestCoreBridge:
    """CoreBridge osztály tesztjei."""

    def setup_method(self):
        """Tesztelés előtti inicializálás."""
        # Reseteljük a Singleton-t minden teszt előtt
        CoreBridge._instance = None

    def test_singleton_pattern(self):
        """Teszteli, hogy a Singleton minta helyesen működik-e."""
        # Két példány létrehozása
        bridge1 = CoreBridge()
        bridge2 = CoreBridge()

        # Ellenőrizzük, hogy ugyanaz a példány
        assert bridge1 is bridge2
        assert bridge1.get_instance() is bridge2.get_instance()

    def test_initial_state(self):
        """Teszteli a kezdeti állapotot."""
        bridge = CoreBridge()

        assert bridge._core is None
        assert bridge._connected is False

    def test_initialize_success(self):
        """Teszteli a sikeres inicializálást."""
        bridge = CoreBridge()

        # Mockoljuk a bootstrap_core függvényt
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_logger = Mock()
            mock_core.logger = mock_logger
            mock_bootstrap.return_value = mock_core

            # Inicializálás
            bridge.initialize()

            # Ellenőrzések
            assert bridge._core is mock_core
            assert bridge._connected is True
            mock_bootstrap.assert_called_once()
            mock_logger.info.assert_called_once_with("Core Bridge inicializálva")

    def test_initialize_failure(self):
        """Teszteli a sikertelen inicializálást."""
        bridge = CoreBridge()

        # Mockoljuk a bootstrap_core függvényt, hogy kivételt dobjon
        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_bootstrap.side_effect = Exception("Bootstrap hiba")

            # Inicializálás kivételt dob
            with pytest.raises(Exception, match="Bootstrap hiba"):
                bridge.initialize()

    def test_get_parquet_storage_success(self):
        """Teszteli a parquet storage sikeres lekérését."""
        bridge = CoreBridge()

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_logger = Mock()
            mock_storage = Mock()
            mock_core.logger = mock_logger
            mock_core.storage = mock_storage
            mock_bootstrap.return_value = mock_core

            bridge.initialize()

            # Komponens lekérése - a valós implementáció a core storage-át adja vissza
            result = bridge.get_component("parquet_storage")

            # Ellenőrzések
            assert result is mock_storage

    def test_send_command_connected(self):
        """Teszteli a parancs küldést csatlakoztatott állapotban."""
        bridge = CoreBridge()

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_logger = Mock()
            mock_core.logger = mock_logger
            mock_bootstrap.return_value = mock_core

            bridge.initialize()

            # Parancs küldése
            result = bridge.send_command("test_command", {"param": "value"})

            # Ellenőrzések - a valós implementáció adott vissza értéket
            assert result is not None
            assert result["command"] == "test_command"
            assert result["params"] == {"param": "value"}
            assert result["status"] == "success"

    def test_get_system_info_connected(self):
        """Teszteli a rendszerinformáció lekérését csatlakoztatott állapotban."""
        bridge = CoreBridge()

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_logger = Mock()
            mock_core.logger = mock_logger
            mock_bootstrap.return_value = mock_core

            bridge.initialize()

            # Rendszerinformáció lekérése
            result = bridge.get_system_info()

            # Ellenőrzések - a valós implementáció adott vissza értéket
            assert result is not None
            assert "version" in result
            assert "status" in result
            assert "components" in result

    def test_core_property(self):
        """Teszteli a core property-t."""
        bridge = CoreBridge()

        with patch("neural_ai.core.bootstrap_core") as mock_bootstrap:
            mock_core = Mock()
            mock_logger = Mock()
            mock_core.logger = mock_logger
            mock_bootstrap.return_value = mock_core

            bridge.initialize()

            # Core property ellenőrzése
            assert bridge.core is mock_core
