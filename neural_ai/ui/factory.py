"""UI Service Factory - A UI szolgáltatások gyártója.

Ez a modul implementálja a UI szolgáltatások létrehozását és kezelését
Dependency Injection minta szerint.
"""

from typing import TYPE_CHECKING, Any, TypedDict, cast

from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

# TypedDict definíciók config kezeléshez - OPERATION TOTAL RECALL
DateRange = TypedDict("DateRange", {"start": str, "end": str})
JForexConfig = TypedDict("JForexConfig", {"symbols": list[str], "date_range": DateRange})
DataServiceConfig = TypedDict("DataServiceConfig", {"jforex": JForexConfig})
UIFactoryConfig = TypedDict("UIFactoryConfig", {"data_service": DataServiceConfig})

if TYPE_CHECKING:
    pass


class UIServiceFactory(metaclass=SingletonMeta):
    """UI Service Factory - A UI szolgáltatások gyártója.

    Ez az osztály felelős a UI szolgáltatások létrehozásáért és
    kezeléséért Singleton minta szerint, Dependency Injectionnel.
    """

    def __init__(self) -> None:
        """A UI Service Factory inicializálása."""
        self._bridge: CoreBridgeInterface | None = None
        self._config: UIFactoryConfig | None = None
        self._logger: Any = None
        self._core_components: Any = None
        self._services: dict[str, Any] = {}
        self._initialized: bool = False

    def initialize(self, bridge: "CoreBridgeInterface", config: UIFactoryConfig, logger: Any, core_components: Any) -> None:
        """A factory inicializálása a függőségekkel.

        Args:
            bridge: A backend bridge példány
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek
        """
        self._bridge = bridge
        self._config = config
        self._logger = logger
        self._core_components = core_components
        self._initialized = True

    def get_navigation_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> NavigationServiceInterface:
        """Navigation Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            NavigationServiceInterface: A Navigation Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        nav_config = cast(dict[str, Any], config.get("navigation", {}))

        if "navigation" not in self._services:
            from neural_ai.ui.services.navigation_service import NavigationService

            self._services["navigation"] = NavigationService(logger, nav_config, core_components)

        return self._services["navigation"]

    def get_dashboard_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> DashboardServiceInterface:
        """Dashboard Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            DashboardServiceInterface: A Dashboard Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        dash_config = cast(dict[str, Any], config.get("dashboard", {}))

        if "dashboard" not in self._services:
            from neural_ai.ui.services.dashboard_service import DashboardService

            self._services["dashboard"] = DashboardService(logger, dash_config, core_components)

        return self._services["dashboard"]

    def get_data_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> DataServiceInterface:
        """Data Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            DataServiceInterface: A Data Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        data_config = cast(DataServiceConfig, config.get("data_service", {}))

        if "data" not in self._services:
            from neural_ai.ui.services.data_service import DataService

            self._services["data"] = DataService(logger, data_config, core_components)

        return self._services["data"]

    def get_ai_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> AIServiceInterface:
        """AI Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            AIServiceInterface: Az AI Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        ai_config = cast(dict[str, Any], config.get("ai_service", {}))

        if "ai" not in self._services:
            from neural_ai.ui.services.ai_service import AIService

            self._services["ai"] = AIService(logger, ai_config, core_components)

        return self._services["ai"]

    def get_strategy_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> StrategyServiceInterface:
        """Strategy Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            StrategyServiceInterface: A Strategy Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        strategy_config = cast(dict[str, Any], config.get("strategy", {}))

        if "strategy" not in self._services:
            from neural_ai.ui.services.strategy_service import StrategyService

            self._services["strategy"] = StrategyService(logger, strategy_config, core_components)

        return self._services["strategy"]

    def get_live_ops_service(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> LiveOpsServiceInterface:
        """Live Ops Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            LiveOpsServiceInterface: A Live Ops Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Cast config TypedDict-re - OPERATION TOTAL RECALL
        live_ops_config = cast(dict[str, Any], config.get("live_ops", {}))

        if "live_ops" not in self._services:
            from neural_ai.ui.services.live_ops_service import LiveOpsService

            self._services["live_ops"] = LiveOpsService(logger, live_ops_config, core_components)

        return self._services["live_ops"]

    def get_all_services(self, config: UIFactoryConfig, logger: Any, core_components: Any) -> dict[str, Any]:
        """Az összes szolgáltatás lekérdezése.

        Args:
            config: A UI factory konfiguráció
            logger: A logger példány
            core_components: A core komponensek

        Returns:
            Dict[str, Any]: Az összes szolgáltatás példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Biztosítjuk, hogy minden szolgáltatás létrejöjjön
        _ = self.get_navigation_service(config, logger, core_components)
        _ = self.get_dashboard_service(config, logger, core_components)
        _ = self.get_data_service(config, logger, core_components)
        _ = self.get_ai_service(config, logger, core_components)
        _ = self.get_strategy_service(config, logger, core_components)
        _ = self.get_live_ops_service(config, logger, core_components)

        return self._services.copy()

    @property
    def is_initialized(self) -> bool:
        """A factory inicializáltságát ellenőrző property.

        Returns:
            bool: True, ha a factory inicializálva van, egyébként False
        """
        return self._initialized

    def reset(self) -> None:
        """A factory visszaállítása alapállapotba."""
        self._services.clear()
        self._initialized = False
        self._bridge = None
