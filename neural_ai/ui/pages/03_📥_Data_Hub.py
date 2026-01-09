"""Data Hub Page - Adatkezelő központ."""

import asyncio
from datetime import UTC, datetime, time
from typing import TYPE_CHECKING, Any

import streamlit as st

from neural_ai.ui.interfaces.page_interface import PageInterface

if TYPE_CHECKING:
    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
    from neural_ai.ui.interfaces.data_service_interface import DataServiceInterface


class DataHubPage(PageInterface):
    """Data Hub oldal.

    Ez az oldal felelős az adatok kezeléséért, letöltéséért és megjelenítéséért
    a DataService segítségével, amely a UIServiceFactory-n keresztül érhető el.
    """

    def __init__(self, bridge: "CoreBridgeInterface", **kwargs: Any) -> None:
        """A Data Hub oldal inicializálása.

        Args:
            bridge: A CoreBridge példány, amelyen keresztül elérjük a backendet
            **kwargs: További opcionális argumentumok
        """
        self._bridge = bridge
        self._loaded = False
        self._title = "📥 Data Hub"
        self._data_service: DataServiceInterface | None = None

    def render(self) -> None:
        """Az oldal megjelenítése Streamlit segítségével."""
        try:
            st.title(self._title)

            # Adatszolgáltatás lekérdezése a factory-n keresztül
            if self._data_service is None:
                from neural_ai.ui.factory import UIServiceFactory

                factory = UIServiceFactory()
                if not factory.is_initialized:
                    st.error("A UI Service Factory nincs inicializálva")
                    return

                self._data_service = factory.get_data_service()

            # Oldalsáv menü
            menu_options = [
                "Adatok listázása",
                "Történelmi adatok letöltése",
                "Adatok exportálása",
            ]
            selected_menu = st.sidebar.selectbox("Menü", menu_options)

            if selected_menu == "Adatok listázása":
                self._render_data_listing()
            elif selected_menu == "Történelmi adatok letöltése":
                self._render_download_history()
            elif selected_menu == "Adatok exportálása":
                self._render_data_export()

        except Exception as e:
            st.error("Váratlan hiba történt a Data Hub oldal megjelenítése során.")
            st.exception(e)

    def _render_data_listing(self) -> None:
        """Elérhető adatok listázásának megjelenítése.

        A metódus lekéri a konfigurált szimbólumokat a DataService segítségével,
        és legördülő menüben felajánlja azokat szűréshez. Ezután a kiválasztott
        szűrővel listázza az elérhető adatokat.

        A metódus a következőket jeleníti meg:
        - Szimbólum szűrő legördülő menü
        - Adatok frissítése gomb
        - Az elérhető adatok DataFrame táblázatban
        - Összesítő metrikák (összes rekord, méret, adatforrások)
        """
        st.header("📊 Elérhető adatok listázása")

        # Szimbólumok lekérése a DataService-ből
        if self._data_service is None:
            st.error("Adatszolgáltatás nem érhető el")
            return

        try:
            symbols = self._data_service.get_configured_symbols()
        except Exception as e:
            st.error(f"Hiba történt a szimbólumok lekérdezése során: {e}")
            symbols = ["EURUSD"]  # Fallback érték

        # Szimbólum szűrés
        symbol_filter = st.selectbox(
            "Szimbólum szűrése",
            options=[None] + symbols,
            format_func=lambda x: "Összes" if x is None else x,
        )

        if st.button("Adatok frissítése", type="primary"):
            try:
                with st.spinner("Adatok betöltése..."):
                    if self._data_service is None:
                        st.error("Adatszolgáltatás nem érhető el")
                        return

                    # Adatok lekérdezése a DataService segítségével
                    data_df = self._data_service.list_available_data(symbol_filter)

                    if data_df.empty:
                        st.warning("Nincsenek elérhető adatok a kiválasztott szűrővel.")
                    else:
                        st.dataframe(data_df, use_container_width=True)

                        # Összesítő információk
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric(
                                "Összes rekord",
                                f"{data_df['records'].sum():,}",
                            )
                        with col2:
                            st.metric(
                                "Összes méret",
                                f"{data_df['size_gb'].sum():.2f} GB",
                            )
                        with col3:
                            st.metric(
                                "Adatforrások",
                                data_df["source_id"].nunique(),
                            )

            except Exception as e:
                st.error(f"Hiba történt az adatok betöltése során: {str(e)}")

    def _render_download_history(self) -> None:
        """Történelmi adatok letöltésének megjelenítése.

        A metódus lekéri a konfigurált szimbólumokat a DataService segítségével,
        és legördülő menüben felajánlja azokat a felhasználónak. Ezután dátum
        tartományt kér be, és indítja el a történelmi adatok letöltését.

        A metódus a következőket jeleníti meg:
        - Szimbólum választó legördülő menü (az "ALL" opcióval)
        - Kezdő és záró dátum választók (alapértelmezett értékekkel a configból)
        - Letöltés indítása gomb
        - Letöltési eredmények és statisztikák
        """
        st.header("📥 Történelmi adatok letöltése")

        # Szimbólumok lekérése a DataService-ből
        if self._data_service is None:
            st.error("Adatszolgáltatás nem érhető el")
            return

        try:
            symbols = self._data_service.get_configured_symbols()
        except Exception as e:
            st.error(f"Hiba történt a szimbólumok lekérdezése során: {e}")
            symbols = ["EURUSD"]  # Fallback érték

        # Alapértelmezett dátumtartomány lekérése a configból
        try:
            default_start, default_end = self._data_service.get_default_date_range()
            default_start_date = default_start.date()
            default_end_date = default_end.date()
        except Exception:
            # Fallback, ha nem sikerül lekérni a configból
            default_start_date = datetime.now().date().replace(day=1)
            default_end_date = datetime.now().date()

        # Bemeneti mezők
        col1, col2 = st.columns(2)

        with col1:
            # Szimbólum választó az "ALL" opcióval
            symbol = st.selectbox(
                "Szimbólum",
                options=["ALL"] + symbols,
            )

        with col2:
            start_date = st.date_input(
                "Kezdő dátum",
                value=default_start_date,
                max_value=datetime.now().date(),
            )

        end_date = st.date_input(
            "Záró dátum",
            value=default_end_date,
            max_value=datetime.now().date(),
        )

        if st.button("Letöltés indítása", type="primary"):
            if start_date > end_date:
                st.error("A kezdő dátum nem lehet későbbi, mint a záró dátum")
                return

            try:
                # Spinner üzenet testreszabása az "ALL" esetére
                if symbol == "ALL":
                    spinner_text = "Tömeges letöltés folyamatban... Ez eltarthat egy ideig."
                else:
                    spinner_text = "Adatok letöltése folyamatban..."

                with st.spinner(spinner_text):
                    if self._data_service is None:
                        st.error("Adatszolgáltatás nem érhető el")
                        return

                    # Aszinkron letöltés indítása
                    start_dt = datetime.combine(start_date, time.min).replace(tzinfo=UTC)
                    end_dt = datetime.combine(end_date, time.max).replace(tzinfo=UTC)

                    # Aszinkron metódus futtatása
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(
                        self._data_service.download_history(symbol, start_dt, end_dt)
                    )
                    loop.close()

                    # Eredmények megjelenítése
                    if result["status"] == "downloaded":
                        st.success("✅ Az összes adat sikeresen letöltve!")

                        # Letöltési információk
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Letöltött rekordok", f"{result['records']:,}")
                        with col2:
                            st.metric("Méret", f"{result['size_mb']:.2f} MB")
                        with col3:
                            st.metric("Státusz", result["status"])

                        # További információk
                        with st.expander("Részletes információk"):
                            st.json(result)

                    elif result["status"] == "partial":
                        st.warning(
                            f"⚠️ Részleges letöltés: "
                            f"{result['successful_dates']}/{result['total_days']} nap sikeres"
                        )
                        st.info(
                            f"Sikertelen napok: {result['failed_dates']}. "
                            "Ellenőrizze a naplófájlokat további információkért."
                        )
                    else:
                        st.error("❌ A letöltés sikertelen. Ellenőrizze a naplófájlokat.")

            except Exception as e:
                st.error(f"Hiba történt a letöltés során: {str(e)}")

    def _render_data_export(self) -> None:
        """Adatok exportálásának megjelenítése."""
        st.header("📤 Adatok exportálása")

        # Exportálási beállítások
        export_format = st.selectbox(
            "Export formátum",
            options=["parquet", "csv", "json"],
        )

        source = st.selectbox(
            "Adatforrás",
            options=["tick_data", "ohlc_data", "market_data"],
        )

        destination = st.text_input(
            "Cél útvonal",
            value=f"/data/export/{source}.{export_format}",
        )

        if st.button("Exportálás indítása", type="primary"):
            try:
                with st.spinner("Adatok exportálása..."):
                    if self._data_service is None:
                        st.error("Adatszolgáltatás nem érhető el")
                        return

                    # Adatok betöltése
                    data_chunks: list[dict[str, Any]] = []
                    for chunk in self._data_service.load_data(source, chunk_size=1000):
                        data_chunks.extend(chunk)

                    if not data_chunks:
                        st.warning("Nincsenek exportálandó adatok")
                        return

                    # Exportálás
                    success = self._data_service.export_data(
                        data_chunks, export_format, destination
                    )

                    if success:
                        st.success(
                            f"✅ {len(data_chunks)} rekord sikeresen exportálva "
                            f"{export_format} formátumban"
                        )
                    else:
                        st.error("❌ Az exportálás sikertelen")

            except Exception as e:
                st.error(f"Hiba történt az exportálás során: {str(e)}")

    def on_navigate_to(self, params: dict[str, Any] | None = None) -> None:
        """Az oldalra navigáláskor meghívott metódus.

        Args:
            params: Opcionális navigációs paraméterek
        """
        self._loaded = True

    def on_navigate_from(self) -> None:
        """Az oldalról navigáláskor meghívott metódus."""
        pass

    @property
    def title(self) -> str:
        """Az oldal címe.

        Returns:
            str: Az oldal címe
        """
        return self._title

    @property
    def is_loaded(self) -> bool:
        """Az oldal betöltöttségi állapota.

        Returns:
            bool: True, ha az oldal betöltődött, egyébként False
        """
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = DataHubPage(bridge)
    page.render()
