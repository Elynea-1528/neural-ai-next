"""UI interfészek csomagja.

Ez a csomag tartalmazza az összes UI szolgáltatás interfészét,
amelyeket a különböző UI komponensek implementálnak.
"""

from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.dashboard_service_interface import DashboardServiceInterface
from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface
from neural_ai.ui.interfaces.live_ops_service_interface import LiveOpsServiceInterface
from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

__all__ = [
    "CoreBridgeInterface",
    "PageInterface",
    "NavigationServiceInterface",
    "DashboardServiceInterface",
    "DataServiceInterface",
    "AIServiceInterface",
    "StrategyServiceInterface",
    "LiveOpsServiceInterface",
]
