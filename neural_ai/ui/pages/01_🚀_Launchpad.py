"""Launchpad Page - Az alkalmazás indítólapja.

Ez a modul implementálja a fő indítólapot, amely a rendszer
áttekintését és gyors elérést nyújt a különböző funkciókhoz.
"""

from typing import TYPE_CHECKING

import streamlit as st

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
from neural_ai.ui.interfaces.page_interface import PageInterface

if TYPE_CHECKING:
    pass


class LaunchpadPage(PageInterface):
    """Launchpad Page - Az alkalmazás indítólapja.

    Ez az osztály implementálja a fő indítólapot, amely a rendszer
    áttekintését és gyors elérést biztosít a különböző funkciókhoz
    vizuális kártyák formájában.
    """

    def __init__(
        self, bridge: CoreBridgeInterface, logger: "LoggerInterface", **kwargs: str | None
    ) -> None:
        """A Launchpad oldal inicializálása.

        Args:
            bridge: A backend bridge példány, amely biztosítja a kapcsolatot
                a core rendszerrel.
            logger: Logger interfész a logoláshoz.
            **kwargs: Opcionális kulcsszó argumentumok, amelyek további
                konfigurációt adhatnak meg.
        """
        self._bridge = bridge
        self._logger = logger
        self._loaded = False
        self._title = "🚀 Launchpad"

    def render(self) -> None:
        """Az oldal tartalmának renderelése.

        Létrehozza a vizuális kártyákat a különböző modulokhoz, amelyek
        kerettel ellátott container-ekben jelennek meg. Minden kártya
        tartalmaz egy rövid leírást és egy linket a megfelelő oldalra.
        """
        st.title(self._title)
        st.markdown("### Gyors Elérés")

        # Első sor: Data Hub és Dev Center
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.subheader("📥 Data Hub")
                st.write("Történelmi adatok letöltése és elemzése.")
                st.page_link(
                    "pages/03_📥_Data_Hub.py",
                    label="Megnyitás",
                    icon="👉",
                    help="Adatletöltés és kezelés",
                )

        with col2:
            with st.container(border=True):
                st.subheader("🛠️ Dev Center")
                st.write("Konfigurációk és naplók kezelése.")
                st.page_link(
                    "pages/02_🛠️_Dev_Center.py",
                    label="Megnyitás",
                    icon="👉",
                    help="Konfiguráció és naplók",
                )

        # Második sor: Live Ops és AI Lab
        col3, col4 = st.columns(2)

        with col3:
            with st.container(border=True):
                st.subheader("⚡ Live Ops")
                st.write("Valós idejű kereskedés és monitorozás.")
                st.page_link(
                    "pages/06_⚡_Live_Ops.py",
                    label="Megnyitás",
                    icon="👉",
                    help="Valós idejű kereskedés",
                )

        with col4:
            with st.container(border=True):
                st.subheader("🧠 AI Lab")
                st.write("Neurális hálók és modellek kezelése.")
                st.page_link(
                    "pages/04_🧠_AI_Lab.py",
                    label="Megnyitás",
                    icon="👉",
                    help="Modellek kezelése",
                )

        # Harmadik sor: Strategy Lab
        col5, _ = st.columns(2)

        with col5:
            with st.container(border=True):
                st.subheader("🪲 Strategy Lab")
                st.write("Stratégiák fejlesztése és backtestelés.")
                st.page_link(
                    "pages/05_🪲_Strategy_Lab.py",
                    label="Megnyitás",
                    icon="👉",
                    help="Stratégiák és backtest",
                )

        st.divider()
        st.markdown("""
        ## Rendszer Áttekintés

        - **Státusz**: Aktív
        - **Verzió**: 6.0.0
        - **Utolsó frissítés**: 2026-01-04 19:35
        """)

    def on_navigate_to(self, params: dict[str, str] | None = None) -> None:
        """Akció, amikor az oldalra navigálnak.

        Args:
            params: Navigációs paraméterek dictionary formájában, vagy None
                ha nincsenek paraméterek.
        """
        self._loaded = True
        self._logger.info("Oldalra navigálás", extra={"page_title": self._title})

    def on_navigate_from(self) -> None:
        """Akció, amikor elnavigálnak az oldalról.

        Ezt a metódust akkor hívja a rendszer, amikor a felhasználó
        elhagyja ezt az oldalt és egy másikra navigál.
        """
        self._logger.info("Oldal elhagyása", extra={"page_title": self._title})

    @property
    def title(self) -> str:
        """Az oldal címét visszaadó property.

        Returns:
            str: Az oldal címe.
        """
        return self._title

    @property
    def is_loaded(self) -> bool:
        """Az oldal betöltöttségi állapotát ellenőrző property.

        Returns:
            bool: True, ha az oldal betöltött, egyébként False.
        """
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = LaunchpadPage(bridge)
    page.render()
