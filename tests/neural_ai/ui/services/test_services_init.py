"""Unit tesztek a neural_ai.ui.services __init__.py modulhoz."""

import neural_ai.ui.services as services_module


class TestServicesInit:
    """Tesztek a services __init__.py modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszt: A modul rendelkezik __all__ attribútummal."""
        assert hasattr(services_module, "__all__")
        assert isinstance(services_module.__all__, list)

    def test_all_exports_correct_services(self) -> None:
        """Teszt: Az __all__ lista tartalmazza az összes service-t."""
        expected_services = [
            "NavigationService",
            "DashboardService",
            "DataService",
            "AIService",
            "StrategyService",
            "LiveOpsService",
        ]
        assert set(services_module.__all__) == set(expected_services)

    def test_navigation_service_importable(self) -> None:
        """Teszt: NavigationService importálható."""
        assert hasattr(services_module, "NavigationService")
        from neural_ai.ui.services import NavigationService

        assert NavigationService is not None

    def test_dashboard_service_importable(self) -> None:
        """Teszt: DashboardService importálható."""
        assert hasattr(services_module, "DashboardService")
        from neural_ai.ui.services import DashboardService

        assert DashboardService is not None

    def test_data_service_importable(self) -> None:
        """Teszt: DataService importálható."""
        assert hasattr(services_module, "DataService")
        from neural_ai.ui.services import DataService

        assert DataService is not None

    def test_ai_service_importable(self) -> None:
        """Teszt: AIService importálható."""
        assert hasattr(services_module, "AIService")
        from neural_ai.ui.services import AIService

        assert AIService is not None

    def test_strategy_service_importable(self) -> None:
        """Teszt: StrategyService importálható."""
        assert hasattr(services_module, "StrategyService")
        from neural_ai.ui.services import StrategyService

        assert StrategyService is not None

    def test_live_ops_service_importable(self) -> None:
        """Teszt: LiveOpsService importálható."""
        assert hasattr(services_module, "LiveOpsService")
        from neural_ai.ui.services import LiveOpsService

        assert LiveOpsService is not None

    def test_all_services_are_classes(self) -> None:
        """Teszt: Minden exportált service osztály."""
        from neural_ai.ui.services import (
            AIService,
            DashboardService,
            DataService,
            LiveOpsService,
            NavigationService,
            StrategyService,
        )

        services = [
            NavigationService,
            DashboardService,
            DataService,
            AIService,
            StrategyService,
            LiveOpsService,
        ]

        for service in services:
            assert isinstance(service, type), f"{service} nem osztály"
