"""Strategy Lab Page - Stratégia fejlesztő labor.

Ez a modul implementálja a Strategy Lab oldalt, ahol a felhasználók
interaktív módon vizsgálhatják a gyertyadiagramokat és stratégiákat.
"""

from datetime import date
from typing import TYPE_CHECKING, Any

import polars as pl
import streamlit as st

from neural_ai.ui.interfaces.page_interface import PageInterface

if TYPE_CHECKING:
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
        self._candles: pl.DataFrame | None = None

        # Session state inicializálása a backtesztekhez és gyertyákhoz
        if "backtest_result" not in st.session_state:
            st.session_state.backtest_result = None
        if "candles" not in st.session_state:
            st.session_state.candles = None
        if "price_type" not in st.session_state:
            st.session_state.price_type = "Bid"
        if "show_body_swings" not in st.session_state:
            st.session_state.show_body_swings = False
        if "show_wick_swings" not in st.session_state:
            st.session_state.show_wick_swings = False
        if "d2_analysis" not in st.session_state:
            st.session_state.d2_analysis = None

    def render(self) -> None:
        """A Strategy Lab oldal megjelenítése."""
        st.title(self._title)
        st.markdown("Kereskedési stratégiák létrehozása és tesztelése.")

        # Session state szinkronizálása a local változókkal
        self._candles = st.session_state.candles

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

            # Ár típus választó (Bid / Mid)
            price_type_options = ["Bid", "Mid"]
            selected_price_type = st.radio(
                "Price Type",
                options=price_type_options,
                index=price_type_options.index(st.session_state.price_type),
                help="Válassza ki az ár típust (Bid vagy Mid)",
                horizontal=True,
            )
            st.session_state.price_type = selected_price_type

            # "Load & Visualize" gomb
            if st.button(
                "📥 Load & Visualize",
                type="primary",
                help="Betölti és megjeleníti a kiválasztott adatokat",
            ):
                self._load_and_visualize(selected_symbol, selected_date, selected_timeframe)

            st.divider()

            # Piaci Szerkezet (D2) Expander
            with st.expander("📈 Piaci Szerkezet (D2)", expanded=False):
                st.markdown("**Swing Pontok Megjelenítése**")

                show_body_swings = st.checkbox(
                    "Show Body Swings",
                    value=st.session_state.show_body_swings,
                    help="Body alapú support és resistance szintek megjelenítése",
                )
                st.session_state.show_body_swings = show_body_swings

                show_wick_swings = st.checkbox(
                    "Show Wick Swings",
                    value=st.session_state.show_wick_swings,
                    help="Wick alapú support és resistance szintek megjelenítése",
                )
                st.session_state.show_wick_swings = show_wick_swings

            st.divider()

            # Stratégia paraméterek Expander
            with st.expander("⚙️ Stratégia Paraméterek", expanded=False):
                st.markdown("**SMA Kereszt Stratégia**")

                fast_period = st.slider(
                    "Fast SMA Periódus",
                    min_value=2,
                    max_value=100,
                    value=10,
                    step=1,
                    help="A gyors mozgóátlag periódusa",
                )

                slow_period = st.slider(
                    "Slow SMA Periódus",
                    min_value=5,
                    max_value=200,
                    value=50,
                    step=1,
                    help="A lassú mozgóátlag periódusa",
                )

                initial_capital = st.number_input(
                    "Kezdeti Tőke",
                    min_value=100.0,
                    value=10000.0,
                    step=100.0,
                    help="A backteszt kezdeti tőkéje",
                )

                # "🚀 Futtatás (VectorBT)" gomb
                if st.button(
                    "🚀 Futtatás (VectorBT)",
                    type="primary",
                    help="Elindítja a VectorBT backtesztet a kiválasztott paraméterekkel",
                ):
                    if self._candles is not None and not self._candles.is_empty():
                        self._run_backtest(
                            selected_symbol,
                            selected_date.strftime("%Y-%m-%d"),
                            selected_timeframe,
                            fast_period,
                            slow_period,
                            initial_capital,
                        )
                    else:
                        st.warning("Először töltsön be adatokat a 'Load & Visualize' gombbal!")

    def _render_main_area(self) -> None:
        """Fő terület megjelenítése diagrammal és táblázattal."""
        if self._candles is not None and not self._candles.is_empty():
            st.subheader("📈 Gyertya Diagram")

            # Backtest jelek átadása a chartnak, ha léteznek
            signals = None
            if st.session_state.backtest_result is not None:
                signals = st.session_state.backtest_result.get("signals")

            self._render_candlestick_chart(signals=signals)

            st.subheader("📋 Adatok")
            self._render_data_table()

            # Backtest eredmények megjelenítése
            if st.session_state.backtest_result is not None:
                self._render_backtest_results()

        elif self._loaded and (self._candles is None or self._candles.is_empty()):
            st.warning("Nincs elérhető adat a kiválasztott paraméterekhez.")
        else:
            st.info(
                "Válasszon szimbólumot, dátumot és időskálát, "
                "majd kattintson a 'Load & Visualize' gombra."
            )

    def _render_backtest_results(self) -> None:
        """Backtest eredmények megjelenítése."""
        result = st.session_state.backtest_result

        if "error" in result and result["error"]:
            st.error(f"Backtest hiba: {result['error']}")
            return

        st.divider()
        st.subheader("📊 Backteszt Eredmények")

        stats = result.get("stats", {})
        equity = result.get("equity", [])
        trades = result.get("trades", {})

        # 1. Metrikák megjelenítése
        if stats:
            col1, col2, col3, col4 = st.columns(4)

            # VectorBT statisztikák normálása
            total_return = stats.get("Total Return [%]", 0.0)
            win_rate = stats.get("Win Rate [%]", 0.0)
            max_drawdown = stats.get("Max Drawdown [%]", 0.0)
            total_trades = stats.get("Total Trades", 0)

            with col1:
                st.metric(
                    label="Total Return",
                    value=f"{total_return:.2f}%",
                    delta_color="normal" if total_return >= 0 else "inverse",
                )
            with col2:
                st.metric(label="Win Rate", value=f"{win_rate:.2f}%")
            with col3:
                st.metric(label="Max Drawdown", value=f"{max_drawdown:.2f}%")
            with col4:
                st.metric(label="Összes Kereskedés", value=total_trades)

        # 2. Equity Chart megjelenítése
        if equity:
            st.subheader("💰 Equity Görbe")
            equity_df = {"Equity": equity}
            st.line_chart(equity_df, height=300)

        # 3. Trade List megjelenítése
        if trades and trades.get("count", 0) > 0:
            st.subheader("🔢 Kereskedések Listája")
            st.write(f"**Összes kereskedés:** {trades.get('count', 0)}")

            # P&L lista
            pnl_list = trades.get("pnl", [])
            if pnl_list:
                trades_data = {"P&L": pnl_list, "Időtartam (bar)": trades.get("duration", [])}
                st.dataframe(trades_data, width="stretch")

    def _prepare_data_for_view(self, df: "pl.DataFrame", price_type: str) -> "pl.DataFrame":
        """Adatok előkészítése megjelenítéshez - oszlopok átnevezése price_type alapján.

        Args:
            df: Az eredeti DataFrame
            price_type: Az ár típus ('Bid' vagy 'Mid')

        Returns:
            DataFrame: Az átnevezett oszlopokkal rendelkező DataFrame
        """
        df = df.copy()
        prefix = f"{price_type.lower()}_"  # "bid_" vagy "mid_"

        rename_map = {
            f"{prefix}open": "open",
            f"{prefix}high": "high",
            f"{prefix}low": "low",
            f"{prefix}close": "close",
        }

        # Csak akkor nevezzük át, ha léteznek az oszlopok
        valid_map = {k: v for k, v in rename_map.items() if k in df.columns}
        df = df.rename(columns=valid_map)
        return df

    def _render_candlestick_chart(self, signals: dict[str, list[int]] | None = None) -> None:
        """Interaktív Plotly candlestick chart megjelenítése jelekkel."""
        import plotly.graph_objects as go

        if self._candles is None or self._candles.is_empty():
            return

        # Polars DataFrame konvertálása Pandas-ra megjelenítéshez
        df_pd = self._candles.to_pandas()
        # Adatok előkészítése oszlop-átnevezéssel
        price_type = st.session_state.price_type
        df = self._prepare_data_for_view(df_pd, price_type)

        # Ellenőrzés, hogy az átnevezés sikeres volt-e
        required_cols = ["open", "high", "low", "close"]
        if not all(col in df.columns for col in required_cols):
            st.error(
                f"Az adatokban nem található OHLC oszlop a kiválasztott {price_type} típusnál."
            )
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
                    name=f"{price_type} OHLC",
                    increasing_line_color="#26a69a",
                    decreasing_line_color="#ef5350",
                )
            ]
        )

        # Belépési és kilépési jelek hozzáadása
        if signals:
            entries = signals.get("entries", [])
            exits = signals.get("exits", [])

            # Belépési jelek (zöld nyilak)
            if entries:
                entry_dates = [df["date"].iloc[i] for i in entries if i < len(df)]
                entry_prices = [df["close"].iloc[i] for i in entries if i < len(df)]
                fig.add_trace(
                    go.Scatter(
                        x=entry_dates,
                        y=entry_prices,
                        mode="markers",
                        name="Belépés",
                        marker={
                            "symbol": "triangle-up",
                            "size": 12,
                            "color": "#00FF00",
                            "line": {"width": 1, "color": "#00FF00"},
                        },
                    )
                )

            # Kilépési jelek (piros nyilak)
            if exits:
                exit_dates = [df["date"].iloc[i] for i in exits if i < len(df)]
                exit_prices = [df["close"].iloc[i] for i in exits if i < len(df)]
                fig.add_trace(
                    go.Scatter(
                        x=exit_dates,
                        y=exit_prices,
                        mode="markers",
                        name="Kilépés",
                        marker={
                            "symbol": "triangle-down",
                            "size": 12,
                            "color": "#FF0000",
                            "line": {"width": 1, "color": "#FF0000"},
                        },
                    )
                )

        # D2 swing pontok hozzáadása, ha aktívak a checkboxok és van elemzés
        if (
            st.session_state.show_body_swings or st.session_state.show_wick_swings
        ) and st.session_state.d2_analysis is not None:
            d2_df = (
                st.session_state.d2_analysis.to_pandas()
                if hasattr(st.session_state.d2_analysis, "to_pandas")
                else st.session_state.d2_analysis
            )

            # Body swings kirajzolása
            if st.session_state.show_body_swings:
                # Resistance Body (piros kör)
                if "resistance_body" in d2_df.columns:
                    valid_resistance_body = d2_df["resistance_body"].dropna()
                    if not valid_resistance_body.empty:
                        resistance_dates = [
                            df["date"].iloc[i] for i in valid_resistance_body.index if i < len(df)
                        ]
                        resistance_values = valid_resistance_body.values
                        fig.add_trace(
                            go.Scatter(
                                x=resistance_dates,
                                y=resistance_values,
                                mode="markers",
                                name="Resistance Body",
                                marker={
                                    "symbol": "circle",
                                    "size": 8,
                                    "color": "#FF0000",
                                    "line": {"width": 1, "color": "#FF0000"},
                                },
                            )
                        )

                # Support Body (zöld kör)
                if "support_body" in d2_df.columns:
                    valid_support_body = d2_df["support_body"].dropna()
                    if not valid_support_body.empty:
                        support_dates = [
                            df["date"].iloc[i] for i in valid_support_body.index if i < len(df)
                        ]
                        support_values = valid_support_body.values
                        fig.add_trace(
                            go.Scatter(
                                x=support_dates,
                                y=support_values,
                                mode="markers",
                                name="Support Body",
                                marker={
                                    "symbol": "circle",
                                    "size": 8,
                                    "color": "#00FF00",
                                    "line": {"width": 1, "color": "#00FF00"},
                                },
                            )
                        )

            # Wick swings kirajzolása
            if st.session_state.show_wick_swings:
                # Resistance Wick (piros X)
                if "resistance_wick" in d2_df.columns:
                    valid_resistance_wick = d2_df["resistance_wick"].dropna()
                    if not valid_resistance_wick.empty:
                        resistance_wick_dates = [
                            df["date"].iloc[i] for i in valid_resistance_wick.index if i < len(df)
                        ]
                        resistance_wick_values = valid_resistance_wick.values
                        fig.add_trace(
                            go.Scatter(
                                x=resistance_wick_dates,
                                y=resistance_wick_values,
                                mode="markers",
                                name="Resistance Wick",
                                marker={
                                    "symbol": "x-thin",
                                    "size": 10,
                                    "color": "#FF0000",
                                    "line": {"width": 2, "color": "#FF0000"},
                                },
                            )
                        )

                # Support Wick (zöld X)
                if "support_wick" in d2_df.columns:
                    valid_support_wick = d2_df["support_wick"].dropna()
                    if not valid_support_wick.empty:
                        support_wick_dates = [
                            df["date"].iloc[i] for i in valid_support_wick.index if i < len(df)
                        ]
                        support_wick_values = valid_support_wick.values
                        fig.add_trace(
                            go.Scatter(
                                x=support_wick_dates,
                                y=support_wick_values,
                                mode="markers",
                                name="Support Wick",
                                marker={
                                    "symbol": "x-thin",
                                    "size": 10,
                                    "color": "#00FF00",
                                    "line": {"width": 2, "color": "#00FF00"},
                                },
                            )
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

        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True})

    def _render_data_table(self) -> None:
        """Az első 10 sor megjelenítése táblázatban Spread és Z-Score oszlopokkal."""
        if self._candles is not None and not self._candles.is_empty():
            # Polars DataFrame konvertálása Pandas-ra megjelenítéshez
            df = self._candles.to_pandas()
            # Oszlopnevek normalizálása
            df.columns = [col.lower() for col in df.columns]

            # Price type alapján OHLC oszlopok kiválasztása megjelenítéshez
            price_type = st.session_state.price_type
            if price_type == "Mid":
                ohlc_cols = ["mid_open", "mid_high", "mid_low", "mid_close"]
            else:
                ohlc_cols = ["bid_open", "bid_high", "bid_low", "bid_close"]
                if not all(col in df.columns for col in ohlc_cols):
                    ohlc_cols = ["open", "high", "low", "close"]

            # Megjelenítendő oszlopok: OHLC, spread, z-score, volume
            display_cols = []
            display_cols.extend(ohlc_cols)

            # Spread oszlop hozzáadása, ha létezik
            if "spread" in df.columns:
                display_cols.append("spread")

            # Z-Score oszlop hozzáadása (rolling_z_score)
            if "rolling_z_score" in df.columns:
                display_cols.append("rolling_z_score")

            # Volume oszlop hozzáadása
            volume_cols = ["real_volume", "tick_volume"]
            for col in volume_cols:
                if col in df.columns:
                    display_cols.append(col)

            # Csak a meglévő oszlopokat tartjuk meg
            available_cols = [col for col in display_cols if col in df.columns]

            # Az első 10 sor megjelenítése
            st.dataframe(df[available_cols].head(10), width="stretch")

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
                    result: pl.DataFrame | None = asyncio.run(
                        strategy_service.get_candles(symbol, date_str, timeframe)
                    )
                    st.session_state.candles = result
                    self._loaded = True
                    # Backtest eredmények törlése új adat betöltésekor
                    st.session_state.backtest_result = None

                    # Automatikus piaci szerkezet elemzés (D2)
                    try:
                        d2_result = asyncio.run(
                            strategy_service.analyze_market_structure(
                                symbol, date_str, timeframe, result
                            )
                        )
                        st.session_state.d2_analysis = d2_result
                    except Exception as e:
                        st.warning(f"D2 elemzés sikertelen: {str(e)}")
                        st.session_state.d2_analysis = None

                    st.success(f"Sikeres betöltés: {symbol} - {date_str}")
                    # Oldal újrarajzolása a friss adatokkal
                    st.rerun()
                else:
                    st.error("Strategy Service nem elérhető.")
            except Exception as e:
                st.error(f"Hiba az adatok betöltésekor: {str(e)}")
                self._candles = None

    def _run_backtest(
        self,
        symbol: str,
        date: str,
        timeframe: str,
        fast_period: int,
        slow_period: int,
        initial_capital: float,
    ) -> None:
        """VectorBT backteszt futtatása.

        Args:
            symbol: A kiválasztott szimbólum
            date: A kiválasztott dátum
            timeframe: A kiválasztott idősík
            fast_period: A gyors SMA periódusa
            slow_period: A lassú SMA periódusa
            initial_capital: A kezdeti tőke
        """
        import asyncio

        with st.spinner("Backteszt futtatása (VectorBT)..."):
            try:
                strategy_service = self._get_strategy_service()
                if strategy_service is not None and hasattr(strategy_service, "run_sma_backtest"):
                    result: dict[str, Any] = asyncio.run(
                        strategy_service.run_sma_backtest(
                            symbol,
                            date,
                            timeframe,
                            fast_period,
                            slow_period,
                            initial_capital,
                            self._candles,
                        )
                    )
                    st.session_state.backtest_result = result
                    st.success("Backteszt befejezve!")
                else:
                    st.error("Strategy Service vagy a run_sma_backtest metódus nem elérhető.")
            except Exception as e:
                st.error(f"Hiba a backteszt futtatása közben: {str(e)}")
                st.session_state.backtest_result = None

    def _get_strategy_service(self) -> "StrategyServiceInterface | None":
        """Strategy Service példány lekérése.

        Returns:
            StrategyServiceInterface: A Strategy Service vagy None
        """
        try:
            return self._bridge.get_component("strategy_service")
        except Exception:
            return None

    def on_navigate_to(self, params: "dict[str, Any] | None" = None) -> None:
        """Navigálás az oldalra.

        Args:
            params: Opcionális navigációs paraméterek
        """
        self._loaded = False
        st.session_state.candles = None
        st.session_state.backtest_result = None

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
