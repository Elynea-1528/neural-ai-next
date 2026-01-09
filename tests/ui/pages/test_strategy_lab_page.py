"""Tesztelési modul a Strategy Lab oldalhoz.

Ez a modul tartalmazza a StrategyLabPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását.
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
        """Teszteli, hogy a navigálás visszaállítja az állapotot.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        strategy_lab_page._loaded = True
        strategy_lab_page._candles = MagicMock()

        strategy_lab_page.on_navigate_to()

        assert strategy_lab_page._loaded is False
        assert strategy_lab_page._candles is None

    def test_on_navigate_to_with_params(self, strategy_lab_page: StrategyLabPage) -> None:
        """Teszteli a navigációt paraméterekkel.

        Args:
            strategy_lab_page: A tesztelendő oldal példány.
        """
        params: dict[str, str] | None = {"key": "value"}
        strategy_lab_page.on_navigate_to(params)

        assert strategy_lab_page._loaded is False
        assert strategy_lab_page._candles is None

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
