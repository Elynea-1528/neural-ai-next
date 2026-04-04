"""Unit tesztek a factory modulhoz.

# pyright: reportUnknownVariableType=false, reportUnknownArgumentType=false
# Mock dict type inference hibák.

Ez a modul teszteli a UIServiceFactory osztály funkcióit.
"""

from unittest.mock import MagicMock

import pytest

from neural_ai.core.config.interfaces.types import UIConfig
from neural_ai.ui.factory import UIServiceFactory


class TestUIServiceFactoryInit:
    """Tesztek a UIServiceFactory inicializálásához."""

    def test_init_creates_instance(self) -> None:
        """Ellenőrzi, hogy a UIServiceFactory létrehozható."""
        # Act
        factory = UIServiceFactory()

        # Assert
        assert factory._bridge is None  # pyright: ignore[reportPrivateUsage]
        assert factory._config is None  # pyright: ignore[reportPrivateUsage]
        assert factory.logger is None  # type: ignore
        assert factory._core_components is None
        assert factory._services == {}


class TestUIServiceFactoryInitialize:
    """Tesztek a UIServiceFactory.initialize metódushoz."""

    def test_initialize_with_dict_config(self) -> None:
        """Ellenőrzi, hogy az initialize dict config-gal működik."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config_dict = {  # pyright: ignore[reportUnknownVariableType]
            "theme": "light",
            "refresh_rate": 5,
            "navigation": {"default_page": "home"},
            "data_service": {"jforex": {}},
            "dashboard": {"refresh_rate": 5},
            "ai_service": {"model_path": "/path/to/model"},
            "strategy": {"backtest_enabled": True},
            "live_ops": {"auto_reconnect": False},
        }

        # Act
        factory.initialize(
            bridge=mock_bridge,
            config=config_dict,  # pyright: ignore[reportUnknownArgumentType]
            logger=mock_logger,
            core_components=mock_core,
        )

        # Assert
        assert factory._initialized is True  # pyright: ignore[reportPrivateUsage]
        assert factory._bridge == mock_bridge  # pyright: ignore[reportPrivateUsage]
        assert factory.logger == mock_logger  # type: ignore
        assert factory._core_components == mock_core  # pyright: ignore[reportPrivateUsage]
        assert isinstance(factory._config, UIConfig)  # pyright: ignore[reportPrivateUsage]

    def test_initialize_with_uiconfig(self) -> None:
        """Ellenőrzi, hogy az initialize UIConfig-gal működik."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
            "navigation": {"default_page": "home"},
            "data_service": {"jforex": {}},
            "dashboard": {"refresh_rate": 5},
            "ai_service": {"model_path": "/path/to/model"},
            "strategy": {"backtest_enabled": True},
            "live_ops": {"auto_reconnect": False},
        })

        # Act
        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Assert
        assert factory._initialized is True  # pyright: ignore[reportPrivateUsage]
        assert factory._bridge == mock_bridge  # pyright: ignore[reportPrivateUsage]
        assert factory._config == config  # pyright: ignore[reportPrivateUsage]


class TestUIServiceFactoryGetNavigationService:
    """Tesztek a get_navigation_service metódushoz."""

    def test_get_navigation_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_navigation_service()

    def test_get_navigation_service_success(self) -> None:
        """Ellenőrzi, hogy a navigation service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_navigation_service()

        # Assert
        assert service is not None


class TestUIServiceFactoryGetDataService:
    """Tesztek a get_data_service metódushoz."""

    def test_get_data_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_data_service()

    def test_get_data_service_success(self) -> None:
        """Ellenőrzi, hogy a data service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_data_service()

        # Assert
        assert service is not None


class TestUIServiceFactoryGetDashboardService:
    """Tesztek a get_dashboard_service metódushoz."""

    def test_get_dashboard_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_dashboard_service()

    def test_get_dashboard_service_success(self) -> None:
        """Ellenőrzi, hogy a dashboard service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_dashboard_service()

        # Assert
        assert service is not None


class TestUIServiceFactoryGetAIService:
    """Tesztek a get_ai_service metódushoz."""

    def test_get_ai_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_ai_service()

    def test_get_ai_service_success(self) -> None:
        """Ellenőrzi, hogy az AI service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_ai_service()

        # Assert
        assert service is not None


class TestUIServiceFactoryGetStrategyService:
    """Tesztek a get_strategy_service metódushoz."""

    def test_get_strategy_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_strategy_service()

    def test_get_strategy_service_success(self) -> None:
        """Ellenőrzi, hogy a strategy service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_strategy_service()

        # Assert
        assert service is not None


class TestUIServiceFactoryGetLiveOpsService:
    """Tesztek a get_live_ops_service metódushoz."""

    def test_get_live_ops_service_raises_error_when_not_initialized(self) -> None:
        """Ellenőrzi, hogy hiba dobódik, ha nincs inicializálva."""
        # Arrange
        factory = UIServiceFactory()

        # Act & Assert
        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_live_ops_service()

    def test_get_live_ops_service_success(self) -> None:
        """Ellenőrzi, hogy a live ops service lekérhető."""
        # Arrange
        factory = UIServiceFactory()
        mock_bridge = MagicMock()
        mock_logger = MagicMock()
        mock_core = MagicMock()
        config = UIConfig.model_validate({
            "theme": "light",
            "refresh_rate": 5,
        })

        factory.initialize(
            bridge=mock_bridge,
            config=config,
            logger=mock_logger,
            core_components=mock_core,
        )

        # Act
        service = factory.get_live_ops_service()

        # Assert
        assert service is not None
