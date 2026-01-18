"""UI Application tesztelése.

Ez a modul tartalmazza a neural_ai.ui.app modul teszteit.
"""

from typing import Any
from unittest.mock import Mock, patch

import pytest

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.ui.app import UIApplication
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface


class TestUIApplication:
    """UIApplication osztály tesztei."""

    def test_init_default_values(self) -> None:
        """Teszteli az alapértelmezett értékekkel történő inicializálást."""
        app = UIApplication()

        assert app.config == {}
        assert app.logger is None
        assert app.bridge is None
        assert app.factory is None
        assert app.navigation is None
        assert app.is_running is False

    def test_init_with_parameters(self) -> None:
        """Teszteli a paraméterekkel történő inicializálást."""
        config: dict[str, Any] = {"theme": "dark", "debug": True}
        logger = Mock(spec=LoggerInterface)

        app = UIApplication(config=config, logger=logger)

        assert app.config == config
        assert app.logger == logger
        assert app.bridge is None
        assert app.factory is None
        assert app.navigation is None
        assert app.is_running is False

    def test_initialize_success(self) -> None:
        """Teszteli a sikeres inicializálást."""
        logger = Mock(spec=LoggerInterface)
        app = UIApplication(logger=logger)

        with (
            patch("neural_ai.ui.app.CoreBridge") as mock_bridge_class,
            patch("neural_ai.ui.app.UIServiceFactory") as mock_factory_class,
        ):
            mock_bridge = Mock()
            mock_factory = Mock()
            mock_navigation = Mock(spec=NavigationServiceInterface)

            mock_bridge_class.return_value = mock_bridge
            mock_factory_class.return_value = mock_factory
            mock_factory.get_navigation_service.return_value = mock_navigation

            result = app.initialize()

            assert result is True
            assert app.bridge == mock_bridge
            assert app.factory == mock_factory
            assert app.navigation == mock_navigation
            mock_bridge.initialize.assert_called_once()
            mock_factory.initialize.assert_called_once_with(mock_bridge)
            logger.info.assert_called()

    def test_initialize_without_logger(self) -> None:
        """Teszteli a sikeres inicializálást logger nélkül."""
        app = UIApplication()

        with (
            patch("neural_ai.ui.app.CoreBridge") as mock_bridge_class,
            patch("neural_ai.ui.app.UIServiceFactory") as mock_factory_class,
        ):
            mock_bridge = Mock()
            mock_factory = Mock()
            mock_navigation = Mock(spec=NavigationServiceInterface)

            mock_bridge_class.return_value = mock_bridge
            mock_factory_class.return_value = mock_factory
            mock_factory.get_navigation_service.return_value = mock_navigation

            result = app.initialize()

            assert result is True
            assert app.bridge == mock_bridge
            assert app.factory == mock_factory
            assert app.navigation == mock_navigation

    def test_initialize_failure(self) -> None:
        """Teszteli a sikertelen inicializálást."""
        logger = Mock(spec=LoggerInterface)
        app = UIApplication(logger=logger)

        with patch("neural_ai.ui.app.CoreBridge") as mock_bridge_class:
            mock_bridge_class.side_effect = Exception("Hiba történt")

            result = app.initialize()

            assert result is False
            assert app.bridge is None
            assert app.factory is None
            assert app.navigation is None
            logger.error.assert_called_once()

    def test_run_success(self) -> None:
        """Teszteli a sikeres indítást."""
        app = UIApplication()
        app.factory = Mock()
        app.navigation = Mock(spec=NavigationServiceInterface)
        app.logger = Mock(spec=LoggerInterface)

        app.run()

        assert app.is_running is True
        app.logger.info.assert_called_once()

    def test_run_not_initialized(self) -> None:
        """Teszteli a hibát, ha az alkalmazás nincs inicializálva."""
        app = UIApplication()

        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.run()

    def test_stop(self) -> None:
        """Teszteli a leállítást."""
        logger = Mock(spec=LoggerInterface)
        app = UIApplication(logger=logger)
        app.is_running = True

        app.stop()

        assert app.is_running is False
        logger.info.assert_called_once()

    def test_get_navigation_service_success(self) -> None:
        """Teszteli a Navigation Service sikeres lekérdezését."""
        mock_navigation = Mock(spec=NavigationServiceInterface)
        app = UIApplication()
        app.navigation = mock_navigation

        result = app.get_navigation_service()

        assert result == mock_navigation

    def test_get_navigation_service_not_initialized(self) -> None:
        """Teszteli a hibát, ha a Navigation Service nincs inicializálva."""
        app = UIApplication()

        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.get_navigation_service()

    def test_get_factory_success(self) -> None:
        """Teszteli a Factory sikeres lekérdezését."""
        mock_factory = Mock()
        app = UIApplication()
        app.factory = mock_factory

        result = app.get_factory()

        assert result == mock_factory

    def test_get_factory_not_initialized(self) -> None:
        """Teszteli a hibát, ha a Factory nincs inicializálva."""
        app = UIApplication()

        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.get_factory()

    def test_is_running_property(self) -> None:
        """Teszteli az is_running property-t."""
        app = UIApplication()

        assert app.is_running is False

        app.is_running = True
        assert app.is_running is True

        app.is_running = False
        assert app.is_running is False

    def test_is_initialized_property(self) -> None:
        """Teszteli az is_initialized property-t."""
        app = UIApplication()

        assert app.is_initialized is False

        app.factory = Mock()
        app.navigation = Mock(spec=NavigationServiceInterface)
        assert app.is_initialized is True

        app.factory = None
        assert app.is_initialized is False

        app.factory = Mock()
        app.navigation = None
        assert app.is_initialized is False

    def test_type_hints_get_navigation_service(self) -> None:
        """Teszteli, hogy a get_navigation_service metódus típusjelölése helyes."""
        # Ez a teszt ellenőrzi, hogy a forward reference helyesen van-e használva
        import inspect

        from neural_ai.ui.app import UIApplication

        signature = inspect.signature(UIApplication.get_navigation_service)
        return_annotation = signature.return_annotation

        # A visszatérési típusnak stringként kell lennie (forward reference)
        assert return_annotation == "NavigationServiceInterface"
