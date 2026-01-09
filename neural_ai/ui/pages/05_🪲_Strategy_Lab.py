"""Strategy Lab Page - Stratégia fejlesztő labor.

Ez a modul implementálja a Strategy Lab oldalt, ahol a felhasználók
interaktív módon vizsgálhatják a gyertyadiagramokat és stratégiákat.
"""

from datetime import date
from typing import TYPE_CHECKING, Any

import streamlit as st

from neural_ai.ui.interfaces.page_interface import PageInterface

if TYPE_CHECKING:
    from pandas import DataFrame

    from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface
    from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface


class StrategyLabPage(PageInterface):
    """Strategy Lab oldal - Interaktív stratégia vizualizáció.

    Ez az osztály implementálja a Strategy Lab felületét, amely lehetővé
    teszi a felhasználók számára a gyertyadiagramok megjelenítését és
    a stratégiák tesztelését.
    """

    def __init__(self, bridge: "CoreBridgeInterface", **kwargs: Any) -> None:
        """A Strategy Lab oldal inicializálása.

        Args:
            bridge: A backend bridge példány
            **kwargs: További opcionális paraméterek
        """
        self._bridge = bridge
        self._loaded = False
        self._title = "🪲 Strategy Lab"
        self._candles: DataFrame | None = None

    def render(self) -> None:
        """A Strategy Lab oldal megjelenítése."""
        st.title(self._title)
        st.markdown("Kereskedési stratégiák létrehozása és tesztelése.")

        self._render_sidebar()
        self._render_main_area()

    def _render_sidebar(self) -> None:
        """Oldalsáv megjelenítése szűrőkkel és beállításokkal."""
        with st.sidebar:
            st.header("📊 Beállítások")

            # Szimbólum választó a konfigurációból
            symbols = self._get_symbols()
            selected_symbol = st.selectbox(
                "Szimbólum",
                options=symbols,
                index=0 if symbols else 0,
                help="Válassza ki a megjeleníteni kívánt devizapárt",
            )

            # Dátum választó (nap)
            selected_date = st.date_input(
                "Dátum", value=date.today(), help="Válassza ki a megjeleníteni kívánt napot"
            )

            # Idősík választó
            timeframe_options = ["1m", "5m", "15m", "1h"]
            selected_timeframe = st.selectbox(
                "Idősík",
                options=timeframe_options,
                index=0,
                help="Válassza ki a gyertyák időkeretét",
            )

            # "Load & Visualize" gomb
            if st.button(
                "📥 Load & Visualize",
                type="primary",
                help="Betölti és megjeleníti a kiválasztott adatokat",
            ):
                self._load_and_visualize(selected_symbol, selected_date, selected_timeframe)

    def _render_main_area(self) -> None:
        """Fő terület megjelenítése diagrammal és táblázattal."""
        if self._candles is not None and not self._candles.empty:
            st.subheader("📈 Gyertya Diagram")
            self._render_candlestick_chart()

            st.subheader("📋 Adatok")
            self._render_data_table()
        elif self._loaded and (self._candles is None or self._candles.empty):
            st.warning("Nincs elérhető adat a kiválasztott paraméterekhez.")
        else:
            st.info(
                "Válasszon szimbólumot, dátumot és időskálát, "
                "majd kattintson a 'Load & Visualize' gombra."
            )

    def _render_candlestick_chart(self) -> None:
        """Interaktív Plotly candlestick chart megjelenítése."""
        import plotly.graph_objects as go

        if self._candles is None or self._candles.empty:
            return

        # Oszlopnevek normalizálása (kisbetűsítés)
        df = self._candles.copy()
        df.columns = [col.lower() for col in df.columns]

        # OHLC oszlopok keresése
        ohlc_columns = ["open", "high", "low", "close"]
        if not all(col in df.columns for col in ohlc_columns):
            st.error("Az adatokban nem található OHLC oszlop.")
            return

        # Dátum oszlop kezelése
        if "timestamp" in df.columns:
            df["date"] = df["timestamp"]
        elif "datetime" in df.columns:
            df["date"] = df["datetime"]
        elif "date" not in df.columns:
            df["date"] = df.index if hasattr(df.index, "__iter__") else range(len(df))

        # Plotly candlestick chart létrehozása
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["date"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name="OHLC",
                    increasing_line_color="#26a69a",
                    decreasing_line_color="#ef5350",
                )
            ]
        )

        # Chart formázása
        fig.update_layout(
            title="Candlestick Chart",
            xaxis_title="Idő",
            yaxis_title="Ár",
            template="plotly_dark",
            height=500,
            xaxis_rangeslider_visible=False,
            dragmode="zoom",
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_data_table(self) -> None:
        """Az első 10 sor megjelenítése táblázatban."""
        if self._candles is not None and not self._candles.empty:
            st.dataframe(self._candles.head(10), use_container_width=True)

    def _get_symbols(self) -> list[str]:
        """Szimbólumok lekérése a konfigurációból.

        Returns:
            List[str]: Az elérhető szimbólumok listája
        """
        try:
            config = self._bridge.get_component("config")
            if config is not None:
                symbols = config.get("symbols", default=[])
                if symbols:
                    return symbols
        except Exception:
            pass

        # Alapértelmezett szimbólumok, ha a konfig nem elérhető
        return ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

    def _load_and_visualize(self, symbol: str, selected_date: date, timeframe: str) -> None:
        """Adatok betöltése és vizualizálása.

        Args:
            symbol: A kiválasztott szimbólum
            selected_date: A kiválasztott dátum
            timeframe: A kiválasztott idősík
        """
        import asyncio

        with st.spinner("Adatok betöltése..."):
            try:
                strategy_service = self._get_strategy_service()
                if strategy_service is not None:
                    date_str = selected_date.strftime("%Y-%m-%d")
                    result: DataFrame | None = asyncio.run(
                        strategy_service.get_candles(symbol, date_str, timeframe)
                    )
                    self._candles = result
                    self._loaded = True
                    st.success(f"Sikeres betöltés: {symbol} - {date_str}")
                else:
                    st.error("Strategy Service nem elérhető.")
            except Exception as e:
                st.error(f"Hiba az adatok betöltésekor: {str(e)}")
                self._candles = None

    def _get_strategy_service(self) -> "StrategyServiceInterface | None":
        """Strategy Service példány lekérése.

        Returns:
            StrategyServiceInterface: A Strategy Service vagy None
        """
        try:
            return self._bridge.get_component("strategy_service")
        except Exception:
            return None

    def on_navigate_to(self, params: dict[str, Any] | None = None) -> None:
        """Navigálás az oldalra.

        Args:
            params: Opcionális navigációs paraméterek
        """
        self._loaded = False
        self._candles = None

    def on_navigate_from(self) -> None:
        """Navigálás az oldalról."""
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
        """Az oldal betöltött állapota.

        Returns:
            bool: True, ha az oldal betöltött
        """
        return self._loaded


# Indító blokk az oldal aktiválásához
if __name__ == "__main__":
    from neural_ai.ui.core_bridge import CoreBridge

    bridge = CoreBridge()
    page = StrategyLabPage(bridge)
    page.render()
