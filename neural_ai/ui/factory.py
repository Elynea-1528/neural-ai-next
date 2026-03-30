"""UI Service Factory - A UI szolgáltatások gyártója.

Ez a modul implementálja a UI szolgáltatások létrehozását és kezelését
Dependency Injection minta szerint.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from neural_ai.core.base.implementations.singleton import SingletonMeta
from neural_ai.core.config.interfaces.types import (
    AIServiceConfig,
    DashboardConfig,
    DataServiceConfig,
    LiveOpsConfig,
    NavigationConfig,
    StrategyConfig,
    UIConfig,
)
from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class UIServiceFactory(metaclass=SingletonMeta):
    """UI Service Factory - A UI szolgáltatások gyártója.

    Ez az osztály felelős a UI szolgáltatások létrehozásáért és
    kezeléséért Singleton minta szerint, Dependency Injectionnel.
    """

    def __init__(self) -> None:
        """A UI Service Factory inicializálása."""
        self._bridge: CoreBridgeInterface | None = None
        self._config: UIConfig | None = None
        self.logger: LoggerInterface | None = None  # Public - factory pattern
        self._core_components: Any = None
        self._services: dict[str, Any] = {}
        self._initialized: bool = False

    def initialize(
        self,
        bridge: CoreBridgeInterface,
        config: dict[str, Any] | UIConfig,
        logger: Any,
        core_components: Any,
    ) -> None:
        """A factory inicializálása a függőségekkel.

        Args:
            bridge: A backend bridge példány
            config: A UI factory konfiguráció (dict vagy UIConfig)
            logger: A logger példány
            core_components: A core komponensek
        """
        if isinstance(config, dict):
            validated_config = UIConfig.model_validate(config)
        else:
            validated_config = config

        self._bridge = bridge
        self._config = validated_config
        self.logger = logger  # Public - factory pattern
        self._core_components = core_components
        self._initialized = True

    def get_navigation_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> NavigationServiceInterface:
        """Navigation Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            NavigationServiceInterface: A Navigation Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        nav_config = (
            final_config.navigation
            if final_config
            else NavigationConfig.model_validate({})
        )

        if "navigation" not in self._services:
            from neural_ai.ui.services.navigation_service import NavigationService

            self._services["navigation"] = NavigationService(
                final_logger, nav_config.model_dump() if nav_config else {}, final_components
            )

        return cast(NavigationServiceInterface, self._services["navigation"])  # pyright: ignore[reportUnusedImport]

    def get_dashboard_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> DashboardServiceInterface:
        """Dashboard Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            DashboardServiceInterface: A Dashboard Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        dash_config = final_config.dashboard if final_config else DashboardConfig.model_validate({})

        if "dashboard" not in self._services:
            from neural_ai.ui.services.dashboard_service import DashboardService

            self._services["dashboard"] = DashboardService(
                final_logger, dash_config.model_dump() if dash_config else {}, final_components
            )

        return cast(DashboardServiceInterface, self._services["dashboard"])  # pyright: ignore[reportUnusedImport]

    def get_data_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> DataServiceInterface:
        """Data Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            DataServiceInterface: A Data Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        data_config = (
            final_config.data_service
            if final_config
            else DataServiceConfig.model_validate({})
        )

        if "data" not in self._services:
            from neural_ai.ui.services.data_service import DataService

            self._services["data"] = DataService(final_logger, data_config, final_components)

        return cast(DataServiceInterface, self._services["data"])  # pyright: ignore[reportUnusedImport]

    def get_ai_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> AIServiceInterface:
        """AI Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            AIServiceInterface: Az AI Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        ai_config = final_config.ai_service if final_config else AIServiceConfig.model_validate({})

        if "ai" not in self._services:
            from neural_ai.ui.services.ai_service import AIService

            self._services["ai"] = AIService(
                final_logger,
                ai_config.model_dump() if ai_config else {},
                final_components,
            )

        return cast(AIServiceInterface, self._services["ai"])  # pyright: ignore[reportUnusedImport]

    def get_strategy_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> StrategyServiceInterface:
        """Strategy Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            StrategyServiceInterface: A Strategy Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        strategy_config = (
            final_config.strategy
            if final_config
            else StrategyConfig.model_validate({})
        )

        if "strategy" not in self._services:
            from neural_ai.ui.services.strategy_service import StrategyService

            self._services["strategy"] = StrategyService(
                final_logger,
                strategy_config.model_dump() if strategy_config else {},
                final_components,
            )

        return cast(StrategyServiceInterface, self._services["strategy"])  # pyright: ignore[reportUnusedImport]

    def get_live_ops_service(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> LiveOpsServiceInterface:
        """Live Ops Service példány lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            LiveOpsServiceInterface: A Live Ops Service példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Használjuk a tárolt értékeket ha nem adtak paramétert
        final_config = config if config is not None else self._config
        final_logger = logger if logger is not None else self.logger
        final_components = core_components if core_components is not None else self._core_components

        if final_config is None or final_logger is None or final_components is None:
            raise RuntimeError("Factory nincs inicializálva megfelelő függőségekkel")

        # Pydantic property elérés - cast() helyett
        live_ops_config = (
            final_config.live_ops
            if final_config
            else LiveOpsConfig.model_validate({})
        )

        if "live_ops" not in self._services:
            from neural_ai.ui.services.live_ops_service import LiveOpsService

            self._services["live_ops"] = LiveOpsService(
                final_logger,
                live_ops_config.model_dump() if live_ops_config else {},
                final_components,
            )

        return cast(LiveOpsServiceInterface, self._services["live_ops"])  # pyright: ignore[reportUnusedImport]

    def get_all_services(
        self,
        config: UIConfig | None = None,
        logger: Any | None = None,
        core_components: Any | None = None,
    ) -> dict[str, Any]:
        """Az összes szolgáltatás lekérdezése.

        Args:
            config: A UI factory konfiguráció (opcionális, fallback: self._config)
            logger: A logger példány (opcionális, fallback: self.logger)
            core_components: A core komponensek (opcionális, fallback: self._core_components)

        Returns:
            Dict[str, Any]: Az összes szolgáltatás példány
        """
        if not self._initialized or self._bridge is None:
            raise RuntimeError("Factory nincs inicializálva")

        # Biztosítjuk, hogy minden szolgáltatás létrejöjjön
        # (Paraméterek nélkül hívjuk, mert a metódusok használják a tárolt értékeket)
        _ = self.get_navigation_service()
        _ = self.get_dashboard_service()
        _ = self.get_data_service()
        _ = self.get_ai_service()
        _ = self.get_strategy_service()
        _ = self.get_live_ops_service()

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
