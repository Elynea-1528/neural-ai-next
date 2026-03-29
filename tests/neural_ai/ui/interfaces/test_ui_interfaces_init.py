"""Unit tesztek a neural_ai.ui.interfaces.__init__ modulhoz."""

import neural_ai.ui.interfaces as interfaces_module


class TestInterfacesInit:
    """Tesztek a neural_ai.ui.interfaces.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(interfaces_module, "__all__")
        assert isinstance(interfaces_module.__all__, list)

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 8 elemet tartalmaz."""
        assert len(interfaces_module.__all__) == 8

    def test_all_exports_core_bridge_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a CoreBridgeInterface-t."""
        assert "CoreBridgeInterface" in interfaces_module.__all__

    def test_all_exports_page_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a PageInterface-t."""
        assert "PageInterface" in interfaces_module.__all__

    def test_all_exports_navigation_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a NavigationServiceInterface-t."""
        assert "NavigationServiceInterface" in interfaces_module.__all__

    def test_all_exports_dashboard_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a DashboardServiceInterface-t."""
        assert "DashboardServiceInterface" in interfaces_module.__all__

    def test_all_exports_data_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a DataServiceInterface-t."""
        assert "DataServiceInterface" in interfaces_module.__all__

    def test_all_exports_ai_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a AIServiceInterface-t."""
        assert "AIServiceInterface" in interfaces_module.__all__

    def test_all_exports_strategy_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a StrategyServiceInterface-t."""
        assert "StrategyServiceInterface" in interfaces_module.__all__

    def test_all_exports_live_ops_service_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a LiveOpsServiceInterface-t."""
        assert "LiveOpsServiceInterface" in interfaces_module.__all__

    def test_core_bridge_interface_importable(self) -> None:
        """Teszteli, hogy a CoreBridgeInterface importálható."""
        assert hasattr(interfaces_module, "CoreBridgeInterface")

    def test_page_interface_importable(self) -> None:
        """Teszteli, hogy a PageInterface importálható."""
        assert hasattr(interfaces_module, "PageInterface")

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert interfaces_module.__doc__ is not None
        assert len(interfaces_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert interfaces_module.__doc__ is not None
        assert "UI interfészek" in interfaces_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in interfaces_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in interfaces_module.__all__:
            assert hasattr(interfaces_module, name)

    def test_all_interfaces_are_classes(self) -> None:
        """Teszteli, hogy az összes export osztály."""
        from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
        from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
        from neural_ai.ui.interfaces.dashboard_service_interface import (
            DashboardServiceInterface,
        )
        from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
        from neural_ai.ui.interfaces.live_ops_service_interface import (
            LiveOpsServiceInterface,
        )
        from neural_ai.ui.interfaces.navigation_service_interface import (
            NavigationServiceInterface,
        )
        from neural_ai.ui.interfaces.page_interface import PageInterface
        from neural_ai.ui.interfaces.strategy_service_interface import (
            StrategyServiceInterface,
        )

        assert interfaces_module.CoreBridgeInterface is CoreBridgeInterface
        assert interfaces_module.PageInterface is PageInterface
        assert interfaces_module.NavigationServiceInterface is NavigationServiceInterface
        assert interfaces_module.DashboardServiceInterface is DashboardServiceInterface
        assert interfaces_module.DataServiceInterface is DataServiceInterface
        assert interfaces_module.AIServiceInterface is AIServiceInterface
        assert interfaces_module.StrategyServiceInterface is StrategyServiceInterface
        assert interfaces_module.LiveOpsServiceInterface is LiveOpsServiceInterface
