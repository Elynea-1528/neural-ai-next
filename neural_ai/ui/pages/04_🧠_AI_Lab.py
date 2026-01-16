"""AI Lab Page - Mesterséges intelligencia labor."""

from typing import Any

import streamlit as st

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface


class AILabPage(PageInterface):
    """AI Lab oldal."""

    def __init__(self, bridge: CoreBridgeInterface, **kwargs: Any) -> None:
        """A AI Lab oldal inicializálása.

        Args:
            bridge: A backend bridge példány
            **kwargs: További opcionális paraméterek
        """
        self._bridge = bridge
        self._loaded = False
        self._title = "🧠 AI Lab"

    def render(self) -> None:
        """A AI Lab oldal megjelenítése."""
        st.title(self._title)
        st.markdown("AI modellek kezelése és futtatása.")

    def on_navigate_to(self, params: dict[str, Any] | None = None) -> None:
        """Navigálás az oldalra.

        Args:
            params: Opcionális navigációs paraméterek
        """
        self._loaded = True

    def on_navigate_from(self) -> None:
        """Navigálás az oldalról."""

    @property
    def title(self) -> str:
        """Az oldal címe.

        Returns:
            str: Az oldal címe
        """
        return self._title

    @property
    def is_loaded(self) -> bool:
        """Az oldal betöltött állapota.

        Returns:
            bool: True, ha az oldal betöltött
        """
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = AILabPage(bridge)
    page.render()
