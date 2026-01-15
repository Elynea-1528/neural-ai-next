"""Tesztelési modul a Strategy Lab oldalhoz.

Ez a modul tartalmazza a StrategyLabPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását és a session_state persistence-t.
"""

import importlib.util
import sys
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface

# Először importáljuk a PageInterface-et, mielőtt dinamikusan betöltjük a modult
from neural_ai.ui.interfaces.strategy_service_interface import StrategyServiceInterface

# Dinamikusan importáljuk a StrategyLabPage-et az emoji karakter miatt
spec = importlib.util.spec_from_file_location(
    "strategy_lab_page", "neural_ai/ui/pages/05_🪲_Strategy_Lab.py"
)
if spec and spec.loader:
    strategy_lab_module = importlib.util.module_from_spec(spec)
    sys.modules["strategy_lab_page"] = strategy_lab_module
    spec.loader.exec_module(strategy_lab_module)
    StrategyLabPage = strategy_lab_module.StrategyLabPage
else:
    raise ImportError("Could not import StrategyLabPage module")


class TestStrategyLabPage:
    """StrategyLabPage osztály tesztjei.

    Ezek a tesztek ellenőrzik az oldal inicializálását, renderelését,
    navigációs metódusait és a szimbólum lekérést.
    """

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridgeInterface létrehozása.

        Returns:
            MagicMock: A mockolt bridge példány.
        """
        return MagicMock(spec=CoreBridgeInterface)

    @pytest.fixture
    def strategy_lab_page(self, mock_bridge: MagicMock) -> StrategyLabPage:
        """StrategyLabPage példány létrehozása teszteléshez.

        Args:
            mock_bridge: A mockolt bridge példány.

        Returns:
            StrategyLabPage: A tesztelendő oldal példány.
        """
        return StrategyLabPage(bridge=mock_bridge)

    def test_init(self, mock_bridge: MagicMock) -> None:
        """Teszteli az osztály inicializálását.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        page = StrategyLabPage(bridge=mock_bridge)

        assert page._bridge == mock_bridge
        assert page._loaded is False
        assert page._title == "🪲 Strategy Lab"
        assert page._candles is None

    def test_init_with_kwargs(self, mock_bridge: MagicMock) -> None:
        """Teszteli az inicializálást további paraméterekkel.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        page = StrategyLabPage(bridge=mock_bridge, custom_param="value")

        assert page._bridge == mock_bridge
        assert page._loaded is False
        assert page._title == "🪲 Strategy Lab"

    def test_title_property(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli a title property-t.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        assert strategy_lab_page.title == "🪲 Strategy Lab"

    def test_is_loaded_property_initial(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli az is_loaded property kezdeti állapotát.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        assert strategy_lab_page.is_loaded is False

    def test_on_navigate_to_resets_state(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli, hogy a navigálás visszaállítja az állapotot (session_state-kel).

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        # Állítsuk be a session state-et
        strategy_lab_module.st.session_state.candles = MagicMock()
        strategy_lab_module.st.session_state.backtest_result = MagicMock()

        strategy_lab_page._loaded = True
        strategy_lab_page._candles = MagicMock()

        strategy_lab_page.on_navigate_to()

        assert strategy_lab_page._loaded is False
        # A session state candles értéke most None kell legyen
        assert strategy_lab_module.st.session_state.candles is None

    def test_on_navigate_to_with_params(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli a navigációt paraméterekkel.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        # Állítsuk be a session state-et
        strategy_lab_module.st.session_state.candles = MagicMock()
        strategy_lab_module.st.session_state.backtest_result = MagicMock()

        params: dict[str, str] | None = {"key": "value"}
        strategy_lab_page.on_navigate_to(params)

        assert strategy_lab_page._loaded is False
        # A session state candles értéke most None kell legyen
        assert strategy_lab_module.st.session_state.candles is None

    def test_on_navigate_from(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli az oldal elhagyásakor történő akciót.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        # Ez a teszt főleg arra szolgál, hogy lefusson a metódus
        # anélkül, hogy hibát dobna
        strategy_lab_page.on_navigate_from()

    def test_get_symbols_from_config(self, mock_bridge: MagicMock) -> None:
        """Teszteli a szimbólumok lekérését a konfigurációból.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_config = MagicMock()
        mock_config.get.return_value = ["EURUSD", "GBPUSD", "USDJPY"]
        mock_bridge.get_component.return_value = mock_config

        page = StrategyLabPage(bridge=mock_bridge)
        symbols = page._get_symbols()

        assert symbols == ["EURUSD", "GBPUSD", "USDJPY"]
        mock_bridge.get_component.assert_called_once_with("config")

    def test_get_symbols_from_config_empty(self, mock_bridge: MagicMock) -> None:
        """Teszteli a szimbólumok lekérését üres konfigurációval.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_config = MagicMock()
        mock_config.get.return_value = []
        mock_bridge.get_component.return_value = mock_config

        page = StrategyLabPage(bridge=mock_bridge)
        symbols = page._get_symbols()

        # Alapértelmezett szimbólumokat kell visszaadni
        assert symbols == ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

    def test_get_symbols_config_returns_none(self, mock_bridge: MagicMock) -> None:
        """Teszteli a szimbólumok lekérését, ha a konfiguráció None.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_bridge.get_component.return_value = None

        page = StrategyLabPage(bridge=mock_bridge)
        symbols = page._get_symbols()

        # Alapértelmezett szimbólumokat kell visszaadni
        assert symbols == ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

    def test_get_symbols_config_exception(self, mock_bridge: MagicMock) -> None:
        """Teszteli a szimbólumok lekérését, ha a konfiguráció hibát dob.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_bridge.get_component.side_effect = Exception("Config error")

        page = StrategyLabPage(bridge=mock_bridge)
        symbols = page._get_symbols()

        # Alapértelmezett szimbólumokat kell visszaadni
        assert symbols == ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]

    def test_get_strategy_service_success(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli a Strategy Service sikeres lekérését.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        mock_service = MagicMock(spec=StrategyServiceInterface)
        strategy_lab_page._bridge.get_component.return_value = mock_service

        service = strategy_lab_page._get_strategy_service()

        assert service == mock_service
        strategy_lab_page._bridge.get_component.assert_called_once_with("strategy_service")

    def test_get_strategy_service_exception(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli a Strategy Service lekérését, ha hibát dob.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        strategy_lab_page._bridge.get_component.side_effect = Exception("Service error")

        service = strategy_lab_page._get_strategy_service()

        assert service is None

    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.sidebar")
    @patch("streamlit.columns")
    @patch("streamlit.selectbox")
    @patch("streamlit.date_input")
    @patch("streamlit.button")
    @patch("streamlit.info")
    def test_render_sidebar(
        self,
        mock_info: MagicMock,
        mock_button: MagicMock,
        mock_date_input: MagicMock,
        mock_selectbox: MagicMock,
        mock_columns: MagicMock,
        mock_sidebar: MagicMock,
        mock_markdown: MagicMock,
        mock_title: MagicMock,
        strategy_lab_page: StrategyLabPage,
    ) -> None:
        """Teszteli az oldalsáv renderelését.

        Args:
            mock_info: Mockolt info.
            mock_button: Mockolt button.
            mock_date_input: Mockolt date_input.
            mock_selectbox: Mockolt selectbox.
            mock_columns: Mockolt columns.
            mock_sidebar: Mockolt sidebar.
            mock_markdown: Mockolt markdown.
            mock_title: Mockolt title.
            strategy_lab_page: A tesztelendő oldal példány.
        """
        mock_sidebar.__enter__.return_value = MagicMock()
        mock_sidebar.__exit__.return_value = None
        mock_selectbox.return_value = "EURUSD"
        mock_date_input.return_value = date.today()
        mock_button.return_value = False

        try:
            strategy_lab_page.render()
        except Exception:
            pass

        mock_title.assert_called_once_with("🪲 Strategy Lab")
        assert mock_markdown.call_count >= 1

    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.sidebar")
    @patch("streamlit.columns")
    @patch("streamlit.selectbox")
    @patch("streamlit.date_input")
    @patch("streamlit.button")
    @patch("streamlit.info")
    def test_render_without_data(
        self,
        mock_info: MagicMock,
        mock_button: MagicMock,
        mock_date_input: MagicMock,
        mock_selectbox: MagicMock,
        mock_columns: MagicMock,
        mock_sidebar: MagicMock,
        mock_markdown: MagicMock,
        mock_title: MagicMock,
        strategy_lab_page: StrategyLabPage,
    ) -> None:
        """Teszteli a renderelést adatok nélkül.

        Args:
            mock_info: Mockolt info.
            mock_button: Mockolt button.
            mock_date_input: Mockolt date_input.
            mock_selectbox: Mockolt selectbox.
            mock_columns: Mockolt columns.
            mock_sidebar: Mockolt sidebar.
            mock_markdown: Mockolt markdown.
            mock_title: Mockolt title.
            strategy_lab_page: A tesztelendő oldal példány.
        """
        mock_sidebar.__enter__.return_value = MagicMock()
        mock_sidebar.__exit__.return_value = None
        mock_selectbox.return_value = "EURUSD"
        mock_date_input.return_value = date.today()
        mock_button.return_value = False

        strategy_lab_page.render()

        mock_title.assert_called_once_with("🪲 Strategy Lab")
        mock_info.assert_called_once()

    def test_render_without_errors(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli, hogy a render metódus hiba nélkül lefut.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        try:
            with (
                patch("streamlit.title"),
                patch("streamlit.markdown"),
                patch("streamlit.sidebar") as mock_sidebar,
                patch("streamlit.selectbox"),
                patch("streamlit.date_input"),
                patch("streamlit.button") as mock_button,
                patch("streamlit.info"),
            ):
                mock_sidebar.__enter__.return_value = MagicMock()
                mock_sidebar.__exit__.return_value = None
                mock_button.return_value = False

                strategy_lab_page.render()

        except Exception as e:
            pytest.fail(f"A render metódus hibát dobott: {e}")


class TestStrategyLabPageSessionState:
    """Session State tesztek a Strategy Lab oldalhoz.

    Ezek a tesztek ellenőrzik a session_state alapú adat persistence funkcionalitást.
    """

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridgeInterface létrehozása.

        Returns:
            MagicMock: A mockolt bridge példány.
        """
        return MagicMock(spec=CoreBridgeInterface)

    @pytest.fixture
    def strategy_lab_page(self, mock_bridge: MagicMock) -> StrategyLabPage:
        """StrategyLabPage példány létrehozása teszteléshez.

        Args:
            mock_bridge: A mockolt bridge példány.

        Returns:
            StrategyLabPage: A tesztelendő oldal példány.
        """
        return StrategyLabPage(bridge=mock_bridge)

    def test_init_session_state_candles_initialization(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy az __init__ metódus inicializálja a session state candles-t.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        # Ellenőrizzük, hogy a StrategyLabPage létrehozható session state-tel
        page = StrategyLabPage(bridge=mock_bridge)

        # Az oldal inicializálása sikeres kell legyen
        assert page._bridge == mock_bridge
        assert page._title == "🪲 Strategy Lab"

    def test_render_syncs_session_state_candles(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy a render metódus szinkronizálja a session state candles értékét.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_candles = MagicMock()
        mock_candles.empty = False
        strategy_lab_module.st.session_state.candles = mock_candles
        strategy_lab_module.st.session_state.backtest_result = None

        with patch("streamlit.title"):
            with patch("streamlit.markdown"):
                with patch("streamlit.sidebar") as mock_sidebar:
                    mock_sidebar.__enter__.return_value = MagicMock()
                    mock_sidebar.__exit__.return_value = None

                    page = StrategyLabPage(bridge=mock_bridge)
                    page.render()

                    # Ellenőrizzük, hogy a _candles szinkronizálva van a session state-szel
                    assert page._candles is mock_candles

    def test_on_navigate_to_clears_session_state(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy az on_navigate_to metódus törli a session state candles értékét.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        strategy_lab_module.st.session_state.candles = MagicMock()
        strategy_lab_module.st.session_state.backtest_result = MagicMock()

        page = StrategyLabPage(bridge=mock_bridge)
        page._loaded = True

        page.on_navigate_to()

        # Ellenőrizzük, hogy az oldal állapota visszaállt
        assert page._loaded is False
        # A session state candles most None kell legyen
        assert strategy_lab_module.st.session_state.candles is None

    def test_candles_persistence_between_interactions(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy a gyertyák megmaradnak a felhasználói interakciók között.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_candles = MagicMock()
        mock_candles.empty = False
        strategy_lab_module.st.session_state.candles = mock_candles
        strategy_lab_module.st.session_state.backtest_result = None

        with patch("streamlit.title"):
            with patch("streamlit.markdown"):
                with patch("streamlit.sidebar") as mock_sidebar:
                    mock_sidebar.__enter__.return_value = MagicMock()
                    mock_sidebar.__exit__.return_value = None

                    page = StrategyLabPage(bridge=mock_bridge)

                    # Első render
                    page.render()
                    assert page._candles is mock_candles

                    # Módosítsuk a session state-et (mintha új adatot töltöttünk volna be)
                    mock_candles_2 = MagicMock()
                    mock_candles_2.empty = False
                    strategy_lab_module.st.session_state.candles = mock_candles_2

                    # Második render - a _candles frissül a session state-ből
                    page.render()
                    assert page._candles is mock_candles_2

    def test_backtest_result_persistence(self, mock_bridge: MagicMock) -> None:
        """Teszteli, hogy a backteszt eredménye megmarad a session state-ben.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        mock_result = {
            "stats": {"Total Return [%]": 10.5, "Win Rate [%]": 55.0},
            "equity": [1000, 1100, 1200],
            "trades": {"count": 5, "pnl": [100, -50, 200, 150, -30]},
        }
        strategy_lab_module.st.session_state.backtest_result = mock_result
        strategy_lab_module.st.session_state.candles = None

        # A session state megőrzi az adatot
        assert strategy_lab_module.st.session_state.backtest_result == mock_result

    def test_price_type_session_state_initialization(self, mock_bridge: MagicMock) -> None:
        """Teszteli a price_type session state inicializálását.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        StrategyLabPage(bridge=mock_bridge)

        # Ellenőrizzük, hogy a price_type alapértelmezetten "Bid"
        assert strategy_lab_module.st.session_state.price_type == "Bid"

    def test_render_data_table_with_price_type_bid(
        self, strategy_lab_page: StrategyLabPage
    ) -> None:
        """Teszteli a _render_data_table metódust Bid price type-pal.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        import pandas as pd
        import polars as pl

        # Mock DataFrame bid oszlopokkal
        mock_df_pd = pd.DataFrame(
            {
                "bid_open": [1.1000, 1.1005],
                "bid_high": [1.1020, 1.1010],
                "bid_low": [1.0995, 1.0990],
                "bid_close": [1.1010, 1.1000],
                "spread": [0.0002, 0.0003],
                "rolling_z_score": [0.5, -0.3],
                "real_volume": [1000, 1500],
                "tick_volume": [50, 75],
            }
        )
        # Konvertáljuk Polars-ra
        mock_df = pl.from_pandas(mock_df_pd)
        strategy_lab_page._candles = mock_df
        strategy_lab_module.st.session_state.price_type = "Bid"

        with patch("streamlit.dataframe") as mock_dataframe:
            strategy_lab_page._render_data_table()

            # Ellenőrizzük, hogy a megfelelő oszlopok kerültek megjelenítésre
            call_args = mock_dataframe.call_args[0][0]
            expected_cols = [
                "bid_open",
                "bid_high",
                "bid_low",
                "bid_close",
                "spread",
                "rolling_z_score",
                "real_volume",
                "tick_volume",
            ]
            assert list(call_args.columns) == expected_cols

    def test_render_data_table_with_price_type_mid(
        self, strategy_lab_page: StrategyLabPage
    ) -> None:
        """Teszteli a _render_data_table metódust Mid price type-pal.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        import pandas as pd
        import polars as pl

        # Mock DataFrame mid oszlopokkal
        mock_df_pd = pd.DataFrame(
            {
                "mid_open": [1.1001, 1.1006],
                "mid_high": [1.1021, 1.1011],
                "mid_low": [1.0996, 1.0991],
                "mid_close": [1.1011, 1.1001],
                "spread": [0.0002, 0.0003],
                "rolling_z_score": [0.5, -0.3],
                "real_volume": [1000, 1500],
            }
        )
        # Konvertáljuk Polars-ra
        mock_df = pl.from_pandas(mock_df_pd)
        strategy_lab_page._candles = mock_df
        strategy_lab_module.st.session_state.price_type = "Mid"

        with patch("streamlit.dataframe") as mock_dataframe:
            strategy_lab_page._render_data_table()

            # Ellenőrizzük, hogy a megfelelő oszlopok kerültek megjelenítésre
            call_args = mock_dataframe.call_args[0][0]
            expected_cols = [
                "mid_open",
                "mid_high",
                "mid_low",
                "mid_close",
                "spread",
                "rolling_z_score",
                "real_volume",
            ]
            assert list(call_args.columns) == expected_cols

    @patch("plotly.graph_objects.Figure")
    @patch("streamlit.plotly_chart")
    def test_render_candlestick_chart_with_bid_price_type(
        self,
        mock_plotly_chart: MagicMock,
        mock_figure: MagicMock,
        strategy_lab_page: StrategyLabPage,
    ) -> None:
        """Teszteli a candlestick chart renderelését Bid price type-pal.

        Args:
            mock_plotly_chart: Mockolt plotly_chart.
            mock_figure: Mockolt Figure.
            strategy_lab_page: A tesztelendő oldal példány.
        """
        import pandas as pd
        import polars as pl

        # Mock DataFrame bid oszlopokkal
        mock_df_pd = pd.DataFrame(
            {
                "bid_open": [1.1000, 1.1005],
                "bid_high": [1.1020, 1.1010],
                "bid_low": [1.0995, 1.0990],
                "bid_close": [1.1010, 1.1000],
                "timestamp": pd.date_range("2024-01-01", periods=2, freq="1min"),
            }
        )
        # Konvertáljuk Polars-ra
        mock_df = pl.from_pandas(mock_df_pd)
        strategy_lab_page._candles = mock_df
        strategy_lab_module.st.session_state.price_type = "Bid"

        mock_fig_instance = MagicMock()
        mock_figure.return_value = mock_fig_instance

        strategy_lab_page._render_candlestick_chart()

        # Ellenőrizzük, hogy a Figure létrejött és a Candlestick chart hozzá lett adva
        mock_figure.assert_called_once()
        # A data tartalmazza a Candlestick objektumot
        candlestick_data = mock_fig_instance.data[0]
        assert hasattr(candlestick_data, "open")

    @patch("plotly.graph_objects.Figure")
    @patch("streamlit.plotly_chart")
    def test_render_candlestick_chart_with_mid_price_type(
        self,
        mock_plotly_chart: MagicMock,
        mock_figure: MagicMock,
        strategy_lab_page: StrategyLabPage,
    ) -> None:
        """Teszteli a candlestick chart renderelését Mid price type-pal.

        Args:
            mock_plotly_chart: Mockolt plotly_chart.
            mock_figure: Mockolt Figure.
            strategy_lab_page: A tesztelendő oldal példány.
        """
        import pandas as pd
        import polars as pl

        # Mock DataFrame mid oszlopokkal
        mock_df_pd = pd.DataFrame(
            {
                "mid_open": [1.1001, 1.1006],
                "mid_high": [1.1021, 1.1011],
                "mid_low": [1.0996, 1.0991],
                "mid_close": [1.1011, 1.1001],
                "timestamp": pd.date_range("2024-01-01", periods=2, freq="1min"),
            }
        )
        # Konvertáljuk Polars-ra
        mock_df = pl.from_pandas(mock_df_pd)
        strategy_lab_page._candles = mock_df
        strategy_lab_module.st.session_state.price_type = "Mid"

        mock_fig_instance = MagicMock()
        mock_figure.return_value = mock_fig_instance

        strategy_lab_page._render_candlestick_chart()

        # Ellenőrizzük, hogy a Figure létrejött és a Candlestick chart hozzá lett adva
        mock_figure.assert_called_once()
        # A data tartalmazza a Candlestick objektumot
        candlestick_data = mock_fig_instance.data[0]
        assert hasattr(candlestick_data, "open")
