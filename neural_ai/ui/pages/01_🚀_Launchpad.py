"""Launchpad Page - Az alkalmazás indítólapja.

Ez a modul implementálja a fő indítólapot, amely a rendszer
áttekintését és gyors elérést nyújt a különböző funkciókhoz.
"""

from typing import Any

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface


class LaunchpadPage(PageInterface):
    """Launchpad Page - Az alkalmazás indítólapja.

    Ez az osztály implementálja a fő indítólapot, amely a rendszer
    áttekintését és gyors elérést biztosít a különböző funkciókhoz.
    """

    def __init__(self, bridge: CoreBridgeInterface, **kwargs: Any) -> None:
        """A Launchpad oldal inicializálása.

        Args:
            bridge: A backend bridge példány
            **kwargs: További paraméterek
        """
        self._bridge = bridge
        self._loaded = False
        self._title = "🚀 Launchpad"

    def render(self) -> str:
        """Az oldal tartalmának renderelése.

        Returns:
            str: A renderelt tartalom
        """
        content = f"""
        # {self._title}
        
        ## Rendszer Áttekintés
        
        - **Státusz**: Aktív
        - **Verzió**: 6.0.0
        - **Utolsó frissítés**: 2026-01-04 19:35
        
        ## Gyors Elérés
        
        ### 🛠️ Dev Center
        - Konfiguráció kezelése
        - Naplók megtekintése
        - Rendszer állapot monitorozása
        
        ### 📥 Data Hub
        - Adatok betöltése és kezelése
        - Adatok szűrése és exportálása
        - Big Data támogatás
        
        ### 🧠 AI Lab
        - Modellek kezelése
        - Inferencia futtatása
        - Tanítás monitorozása
        
        ### 🪲 Strategy Lab
        - Stratégiák létrehozása
        - Backtestelés
        - Paraméter optimalizálás
        
        ### ⚡ Live Ops
        - Valós idejű kereskedés
        - Pozíciók kezelése
        - Teljesítmény elemzés
        """
        return content

    def on_navigate_to(self, params: dict[str, Any] | None = None) -> None:
        """Akció, amikor az oldalra navigálnak.

        Args:
            params: Navigációs paraméterek
        """
        self._loaded = True
        print(f"Navigálva a(z) {self._title} oldalra")

    def on_navigate_from(self) -> None:
        """Akció, amikor elnavigálnak az oldalról."""
        print(f"Elnavigálva a(z) {self._title} oldalról")

    @property
    def title(self) -> str:
        """Az oldal címét visszaadó property.

        Returns:
            str: Az oldal címe
        """
        return self._title

    @property
    def is_loaded(self) -> bool:
        """Az oldal betöltöttségi állapotát ellenőrző property.

        Returns:
            bool: True, ha az oldal betöltött, egyébként False
        """
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = LaunchpadPage(bridge)
    print(page.render())
