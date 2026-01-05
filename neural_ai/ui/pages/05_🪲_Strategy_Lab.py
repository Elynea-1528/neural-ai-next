"""Strategy Lab Page - Stratégia fejlesztő labor."""

from typing import Any

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface


class StrategyLabPage(PageInterface):
    """Strategy Lab oldal."""

    def __init__(self, bridge: CoreBridgeInterface, **kwargs: Any) -> None:
        self._bridge = bridge
        self._loaded = False
        self._title = "🪲 Strategy Lab"

    def render(self) -> str:
        return f"# {self._title}\n\nKereskedési stratégiák létrehozása és tesztelése."

    def on_navigate_to(self, params: dict[str, Any] | None = None) -> None:
        self._loaded = True

    def on_navigate_from(self) -> None:
        pass

    @property
    def title(self) -> str:
        return self._title

    @property
    def is_loaded(self) -> bool:
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = StrategyLabPage(bridge)
    print(page.render())
