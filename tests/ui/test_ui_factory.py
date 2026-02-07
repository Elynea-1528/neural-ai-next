"""Tesztek a UI Service Factory számára."""

from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from neural_ai.core.config.interfaces.types import UIConfig
from neural_ai.ui.factory import UIServiceFactory
from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface


class TestUIServiceFactory:
    """A UIServiceFactory tesztosztálya."""

    def setup_method(self) -> None:
        """Tesztelés előtti beállítások."""
        # Singleton reset a teszteléshez
        factory = UIServiceFactory()
        factory.reset()

    def teardown_method(self) -> None:
        """Tesztelés utáni takarítás."""
        # Singleton reset a takarításhoz
        factory = UIServiceFactory()
        factory.reset()

    def test_factory_initialization(self) -> None:
        """A factory inicializálásának tesztelése."""
        factory = UIServiceFactory()

        assert factory.is_initialized is False
        # A Singleton miatt a belső állapotot nem ellenőrizzük közvetlenül

    def test_initialize_with_bridge(self) -> None:
        """A factory inicializálásának tesztelése bridge-el."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)

        factory.initialize(mock_bridge, {}, Mock(), Mock())

        assert factory.is_initialized is True

    def test_get_navigation_service_before_initialization(self) -> None:
        """Navigation service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_navigation_service()

    def test_get_navigation_service_after_initialization(self) -> None:
        """Navigation service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_navigation_service()

        assert isinstance(service, NavigationServiceInterface)

    def test_get_dashboard_service_before_initialization(self) -> None:
        """Dashboard service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_dashboard_service()

    def test_get_dashboard_service_after_initialization(self) -> None:
        """Dashboard service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_dashboard_service()

        assert isinstance(service, DashboardServiceInterface)

    def test_get_data_service_before_initialization(self) -> None:
        """Data service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_data_service()

    def test_get_data_service_after_initialization(self) -> None:
        """Data service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_data_service()

        assert isinstance(service, DataServiceInterface)

    def test_get_ai_service_before_initialization(self) -> None:
        """AI service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_ai_service()

    def test_get_ai_service_after_initialization(self) -> None:
        """AI service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_ai_service()

        assert isinstance(service, AIServiceInterface)

    def test_get_strategy_service_before_initialization(self) -> None:
        """Strategy service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_strategy_service()

    def test_get_strategy_service_after_initialization(self) -> None:
        """Strategy service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_strategy_service()

        assert isinstance(service, StrategyServiceInterface)

    def test_get_live_ops_service_before_initialization(self) -> None:
        """Live Ops service lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_live_ops_service()

    def test_get_live_ops_service_after_initialization(self) -> None:
        """Live Ops service lekérdezése inicializálás után."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        service = factory.get_live_ops_service()

        assert isinstance(service, LiveOpsServiceInterface)

    def test_get_all_services(self) -> None:
        """Az összes szolgáltatás lekérdezésének tesztelése."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        services = factory.get_all_services()

        assert isinstance(services, dict)
        assert "navigation" in services
        assert "dashboard" in services
        assert "data" in services
        assert "ai" in services
        assert "strategy" in services
        assert "live_ops" in services
        assert len(services) == 6

    def test_get_all_services_before_initialization(self) -> None:
        """Összes szolgáltatás lekérdezése inicializálás előtt."""
        factory = UIServiceFactory()

        with pytest.raises(RuntimeError, match="Factory nincs inicializálva"):
            factory.get_all_services()

    def test_is_initialized_property(self) -> None:
        """Az is_initialized property tesztelése."""
        factory = UIServiceFactory()

        assert factory.is_initialized is False

        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        assert factory.is_initialized is True

    def test_reset_method(self) -> None:
        """A reset metódus tesztelése."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        # Létrehozunk néhány szolgáltatást
        factory.get_navigation_service()
        factory.get_data_service()

        assert factory.is_initialized is True

        factory.reset()

        assert factory.is_initialized is False

    def test_singleton_pattern(self) -> None:
        """A Singleton minta tesztelése."""
        factory1 = UIServiceFactory()
        factory2 = UIServiceFactory()

        assert factory1 is factory2

        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory1.initialize(mock_bridge, {}, Mock(), Mock())

        assert factory2.is_initialized is True

    def test_data_service_compatibility(self) -> None:
        """DataService kompatibilitás ellenőrzése a factory-val."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        # Lekérjük a DataService-t
        data_service = factory.get_data_service()

        # Ellenőrizzük, hogy a DataService implementálja-e a szükséges interfészt
        assert isinstance(data_service, DataServiceInterface)

    def test_service_caching(self) -> None:
        """Szolgáltatások gyorsítótárazásának tesztelése."""
        factory = UIServiceFactory()
        mock_bridge = Mock(spec=CoreBridgeInterface)
        factory.initialize(mock_bridge, {}, Mock(), Mock())

        # Lekérjük a szolgáltatást kétszer
        service1 = factory.get_data_service()
        service2 = factory.get_data_service()

        # Ellenőrizzük, hogy ugyanaz a példány lett-e visszaadva
        assert service1 is service2


class TestUIConfigValidation:
    """UIConfig Pydantic validáció tesztek."""

    def test_valid_ui_config(self) -> None:
        """Érvényes UI konfiguráció tesztelése."""
        config = UIConfig(
            theme="dark",
            refresh_rate=5,
        )
        assert config.theme == "dark"
        assert config.refresh_rate == 5

    def test_invalid_theme_raises_error(self) -> None:
        """Érvénytelen téma ValidationError-t dob."""
        with pytest.raises(ValidationError):
            UIConfig(theme="invalid_theme")

    def test_negative_refresh_rate_raises_error(self) -> None:
        """Negatív refresh_rate ValidationError-t dob."""
        with pytest.raises(ValidationError):
            UIConfig(refresh_rate=-1)

    def test_zero_refresh_rate_raises_error(self) -> None:
        """Nulla refresh_rate ValidationError-t dob."""
        with pytest.raises(ValidationError):
            UIConfig(refresh_rate=0)

    def test_factory_validates_config(self) -> None:
        """Factory Pydantic validációt végez."""
        from unittest.mock import Mock

        from neural_ai.ui.factory import UIServiceFactory

        factory = UIServiceFactory()
        mock_bridge = Mock()

        # Érvénytelen config
        with pytest.raises(ValidationError):
            factory.initialize(
                bridge=mock_bridge,
                config={"theme": "invalid"},
                logger=Mock(),
                core_components=Mock(),
            )

    def test_default_values(self) -> None:
        """Alapértelmezett értékek tesztelése."""
        config = UIConfig()
        assert config.theme == "light"
        assert config.refresh_rate is None

    def test_nested_config_validation(self) -> None:
        """Beágyazott konfiguráció validálása."""
        config = UIConfig(
            data_service={
                "jforex": {
                    "symbols": ["EURUSD", "GBPUSD"],
                    "date_range": {
                        "start": "2024-01-01",
                        "end": "2024-12-31"
                    }
                }
            }
        )
        assert config.data_service is not None
        assert config.data_service.jforex is not None
        assert config.data_service.jforex.symbols == ["EURUSD", "GBPUSD"]
        assert config.data_service.jforex.date_range is not None
        assert config.data_service.jforex.date_range.start == "2024-01-01"
