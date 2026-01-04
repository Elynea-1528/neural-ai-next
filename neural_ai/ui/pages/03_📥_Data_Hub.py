"""Data Hub Page - Adatkezelő központ."""

from typing import Dict, Any, Optional
from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface


class DataHubPage(PageInterface):
    """Data Hub oldal."""

    def __init__(self, bridge: CoreBridgeInterface, **kwargs: Any) -> None:
        self._bridge = bridge
        self._loaded = False
        self._title = "📥 Data Hub"

    def render(self) -> str:
        return f"# {self._title}\n\nAdatok betöltése, szűrése és kezelése."

    def on_navigate_to(self, params: Optional[Dict[str, Any]] = None) -> None:
        self._loaded = True

    def on_navigate_from(self) -> None:
        pass

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_loaded(self) -> bool:
        return self._loaded