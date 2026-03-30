"""Unit tesztek az app modulhoz.

Ez a modul teszteli a UIApplication osztály funkcióit.
"""

from unittest.mock import MagicMock, patch

import pytest

from neural_ai.ui.app import UIApplication


class TestUIApplicationInit:
    """Tesztek a UIApplication inicializálásához."""

    def test_init_without_parameters(self) -> None:
        """Ellenőrzi, hogy a UIApplication létrehozható paraméterek nélkül."""
        # Act
        app = UIApplication()

        # Assert
        assert app._config == {}  # pyright: ignore[reportPrivateUsage]
        assert app._logger is None  # pyright: ignore[reportPrivateUsage]
        assert app._bridge is None  # pyright: ignore[reportPrivateUsage]
        assert app._factory is None  # pyright: ignore[reportPrivateUsage]
        assert app._navigation is None  # pyright: ignore[reportPrivateUsage]
        assert app._core_components is None  # pyright: ignore[reportPrivateUsage]
        assert app._running is False  # pyright: ignore[reportPrivateUsage]
        assert app._init_error is None  # pyright: ignore[reportPrivateUsage]

    def test_init_with_config(self) -> None:
        """Ellenőrzi, hogy a UIApplication létrehozható konfigurációval."""
        # Arrange
        config = {"ui": {"theme": "dark"}}

        # Act
        app = UIApplication(config=config)

        # Assert
        assert app._config == config  # pyright: ignore[reportPrivateUsage]
        assert app._logger is None  # pyright: ignore[reportPrivateUsage]

    def test_init_with_logger(self) -> None:
        """Ellenőrzi, hogy a UIApplication létrehozható loggerrel."""
        # Arrange
        mock_logger = MagicMock()

        # Act
        app = UIApplication(logger=mock_logger)

        # Assert
        assert app._logger == mock_logger  # pyright: ignore[reportPrivateUsage]


class TestUIApplicationInitialize:
    """Tesztek a UIApplication.initialize metódushoz."""

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_initialize_success(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy az initialize sikeresen inicializálja az alkalmazást."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()

        # Act
        result = app.initialize()

        # Assert
        assert result is True
        assert app._logger == mock_logger  # pyright: ignore[reportPrivateUsage]
        assert app._bridge == mock_bridge  # pyright: ignore[reportPrivateUsage]
        assert app._factory == mock_factory  # pyright: ignore[reportPrivateUsage]
        assert app._navigation == mock_navigation  # pyright: ignore[reportPrivateUsage]
        mock_bridge.initialize.assert_called_once()
        mock_factory.initialize.assert_called_once()

    @patch("neural_ai.ui.app.CoreBridge")
    def test_initialize_with_existing_logger(
        self, mock_core_bridge: MagicMock
    ) -> None:
        """Ellenőrzi, hogy az initialize használja a meglévő loggert."""
        # Arrange
        mock_logger = MagicMock()
        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        app = UIApplication(logger=mock_logger)

        # Act
        with patch("neural_ai.ui.app.UIServiceFactory"):
            result = app.initialize()

        # Assert
        assert result is True
        assert app._logger == mock_logger  # pyright: ignore[reportPrivateUsage]
        mock_logger.info.assert_called()

    @patch("neural_ai.ui.app.CoreBridge")
    def test_initialize_handles_exception(self, mock_core_bridge: MagicMock) -> None:
        """Ellenőrzi, hogy az initialize kezeli a kivételeket."""
        # Arrange
        mock_core_bridge.side_effect = Exception("Test error")
        mock_logger = MagicMock()
        app = UIApplication(logger=mock_logger)

        # Act
        result = app.initialize()

        # Assert
        assert result is False
        assert app._init_error is not None  # pyright: ignore[reportPrivateUsage]
        assert str(app._init_error) == "Test error"  # pyright: ignore[reportPrivateUsage]
        mock_logger.error.assert_called_once()


class TestUIApplicationRun:
    """Tesztek a UIApplication.run metódushoz."""

    def test_run_without_initialization_raises_error(self) -> None:
        """Ellenőrzi, hogy a run hibát dob inicializálás nélkül."""
        # Arrange
        app = UIApplication()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.run()

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_run_success(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a run sikeresen elindítja az alkalmazást."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()

        # Act
        app.run()

        # Assert
        assert app._running is True  # pyright: ignore[reportPrivateUsage]
        mock_logger.info.assert_any_call("UI alkalmazás elindítva")


class TestUIApplicationStop:
    """Tesztek a UIApplication.stop metódushoz."""

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_stop_success(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a stop sikeresen leállítja az alkalmazást."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()
        app.run()

        # Act
        app.stop()

        # Assert
        assert app._running is False  # pyright: ignore[reportPrivateUsage]
        mock_logger.info.assert_any_call("UI alkalmazás leállítva")


class TestUIApplicationGetters:
    """Tesztek a UIApplication getter metódusokhoz."""

    def test_get_navigation_service_without_initialization_raises_error(self) -> None:
        """Ellenőrzi, hogy a get_navigation_service hibát dob inicializálás nélkül."""
        # Arrange
        app = UIApplication()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.get_navigation_service()

    def test_get_factory_without_initialization_raises_error(self) -> None:
        """Ellenőrzi, hogy a get_factory hibát dob inicializálás nélkül."""
        # Arrange
        app = UIApplication()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Alkalmazás nincs inicializálva"):
            app.get_factory()

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_get_navigation_service_success(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a get_navigation_service visszaadja a navigation service-t."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()

        # Act
        result = app.get_navigation_service()

        # Assert
        assert result == mock_navigation

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_get_factory_success(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a get_factory visszaadja a factory-t."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()

        # Act
        result = app.get_factory()

        # Assert
        assert result == mock_factory


class TestUIApplicationProperties:
    """Tesztek a UIApplication property-khez."""

    def test_is_running_default_false(self) -> None:
        """Ellenőrzi, hogy az is_running alapértelmezetten False."""
        # Arrange
        app = UIApplication()

        # Act & Assert
        assert app.is_running is False

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_is_running_true_after_run(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy az is_running True a run után."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()

        # Act
        app.run()

        # Assert
        assert app.is_running is True

    @patch("neural_ai.ui.app.UIServiceFactory")
    @patch("neural_ai.ui.app.CoreBridge")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    def test_is_running_false_after_stop(
        self,
        mock_logger_factory: MagicMock,
        mock_core_bridge: MagicMock,
        mock_ui_service_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy az is_running False a stop után."""
        # Arrange
        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        mock_bridge = MagicMock()
        mock_core_bridge.return_value = mock_bridge

        mock_factory = MagicMock()
        mock_ui_service_factory.return_value = mock_factory

        mock_navigation = MagicMock()
        mock_factory.get_navigation_service.return_value = mock_navigation

        app = UIApplication()
        app.initialize()
        app.run()

        # Act
        app.stop()

        # Assert
        assert app.is_running is False
