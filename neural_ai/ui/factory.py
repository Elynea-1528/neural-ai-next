"""
UI Service Factory - A UI szolgáltatások gyártója.

Ez a modul implementálja a UI szolgáltatások létrehozását és kezelését
Dependency Injection minta szerint.
"""

from typing import Dict, Any, Optional, TYPE_CHECKING

from neural_ai.core.base.implementations.singleton import SingletonMeta

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
    from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
    from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
    from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
    from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
    from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface
    from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface


class UIServiceFactory(metaclass=SingletonMeta):
    """
    UI Service Factory - A UI szolgáltatások gyártója.
    
    Ez az osztály felelős a UI szolgáltatások létrehozásáért és
    kezeléséért Singleton minta szerint, Dependency Injectionnel.
    """

    def __init__(self) -> None:
        """A UI Service Factory inicializálása."""
        self._bridge: Optional["CoreBridgeInterface"] = None
        self._services: Dict[str, Any] = {}
        self._initialized: bool = False

    def initialize(self, bridge: "CoreBridgeInterface") -> None:
        """
        A factory inicializálása a backend bridge-el.
        
        Args:
            bridge: A backend bridge példány
        """
        self._bridge = bridge
        self._initialized = True

    def get_navigation_service(self) -> NavigationServiceInterface:
        """
        Navigation Service példány lekérdezése.
        
        Returns:
            NavigationServiceInterface: A Navigation Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        if "navigation" not in self._services:
            from neural_ai.ui.services.navigation_service import NavigationService
            self._services["navigation"] = NavigationService(self._bridge)

        return self._services["navigation"]

    def get_dashboard_service(self) -> DashboardServiceInterface:
        """
        Dashboard Service példány lekérdezése.
        
        Returns:
            DashboardServiceInterface: A Dashboard Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        if "dashboard" not in self._services:
            from neural_ai.ui.services.dashboard_service import DashboardService
            self._services["dashboard"] = DashboardService(self._bridge)

        return self._services["dashboard"]

    def get_data_service(self) -> DataServiceInterface:
        """
        Data Service példány lekérdezése.
        
        Returns:
            DataServiceInterface: A Data Service példány
        """
        if not self._initialized:
            raise RuntimeError("Factory nincs inicializálva")

        if "data" not in self._services:
            from neural_ai.ui.services.data_service import DataService
            self._services["data"] = DataService(self._bridge)

        return self._services["data"]

    def get_ai_service(self) -> AIServiceInterface:
        """
        AI Service példány lekérdezése.
        
        Returns:
            AIServiceInterface: Az AI Service példány
        """
        if not self._initialized:
            raise RuntimeError("Factory nincs inicializálva")

        if "ai" not in self._services:
            from neural_ai.ui.services.ai_service import AIService
            self._services["ai"] = AIService(self._bridge)

        return self._services["ai"]

    def get_strategy_service(self) -> StrategyServiceInterface:
        """
        Strategy Service példány lekérdezése.
        
        Returns:
            StrategyServiceInterface: A Strategy Service példány
        """
        if not self._initialized:
            raise RuntimeError("Factory nincs inicializálva")

        if "strategy" not in self._services:
            from neural_ai.ui.services.strategy_service import StrategyService
            self._services["strategy"] = StrategyService(self._bridge)

        return self._services["strategy"]

    def get_live_ops_service(self) -> LiveOpsServiceInterface:
        """
        Live Ops Service példány lekérdezése.
        
        Returns:
            LiveOpsServiceInterface: A Live Ops Service példány
        """
        if not self._initialized:
            raise RuntimeError("Factory nincs inicializálva")

        if "live_ops" not in self._services:
            from neural_ai.ui.services.live_ops_service import LiveOpsService
            self._services["live_ops"] = LiveOpsService(self._bridge)

        return self._services["live_ops"]

    def get_all_services(self) -> Dict[str, Any]:
        """
        Az összes szolgáltatás lekérdezése.
        
        Returns:
            Dict[str, Any]: Az összes szolgáltatás példány
        """
        if not self._initialized:
            raise RuntimeError("Factory nincs inicializálva")

        # Biztosítjuk, hogy minden szolgáltatás létrejöjjön
        _ = self.get_navigation_service()
        _ = self.get_dashboard_service()
        _ = self.get_data_service()
        _ = self.get_ai_service()
        _ = self.get_strategy_service()
        _ = self.get_live_ops_service()

        return self._services.copy()

    @property
    def is_initialized(self) -> bool:
        """
        A factory inicializáltságát ellenőrző property.
        
        Returns:
            bool: True, ha a factory inicializálva van, egyébként False
        """
        return self._initialized

    def reset(self) -> None:
        """
        A factory visszaállítása alapállapotba.
        """
        self._services.clear()
        self._initialized = False
        self._bridge = None