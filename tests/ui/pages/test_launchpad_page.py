"""Tesztelési modul a Launchpad oldalhoz.

Ez a modul tartalmazza a LaunchpadPage osztály egységtesztjeit,
amelyek ellenőrzik az oldal alapvető funkcionalitását.
"""

import importlib.util
import sys
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface

# Dinamikusan importáljuk a LaunchpadPage-et az emoji karakter miatt
spec = importlib.util.spec_from_file_location(
    "launchpad_page", "neural_ai/ui/pages/01_🚀_Launchpad.py"
)
if spec and spec.loader:
    launchpad_module = importlib.util.module_from_spec(spec)
    sys.modules["launchpad_page"] = launchpad_module
    spec.loader.exec_module(launchpad_module)
    LaunchpadPage = launchpad_module.LaunchpadPage
else:
    raise ImportError("Could not import LaunchpadPage module")


class TestLaunchpadPage:
    """LaunchpadPage osztály tesztjei.

    Ezek a tesztek ellenőrzik az oldal inicializálását, renderelését
    és navigációs metódusait.
    """

    @pytest.fixture
    def mock_bridge(self) -> MagicMock:
        """Mock CoreBridgeInterface létrehozása.

        Returns:
            MagicMock: A mockolt bridge példány.
        """
        return MagicMock(spec=CoreBridgeInterface)

    @pytest.fixture
    def launchpad_page(self, mock_bridge: MagicMock) -> LaunchpadPage:
        """LaunchpadPage példány létrehozása teszteléshez.

        Args:
            mock_bridge: A mockolt bridge példány.

        Returns:
            LaunchpadPage: A tesztelendő oldal példány.
        """
        return LaunchpadPage(bridge=mock_bridge)

    def test_init(self, mock_bridge: MagicMock) -> None:
        """Teszteli az osztály inicializálását.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        page = LaunchpadPage(bridge=mock_bridge)

        assert page._bridge == mock_bridge
        assert page._loaded is False
        assert page._title == "🚀 Launchpad"

    def test_init_with_kwargs(self, mock_bridge: MagicMock) -> None:
        """Teszteli az inicializálást további paraméterekkel.

        Args:
            mock_bridge: A mockolt bridge példány.
        """
        page = LaunchpadPage(bridge=mock_bridge, custom_param="value")

        assert page._bridge == mock_bridge
        assert page._loaded is False
        assert page._title == "🚀 Launchpad"

    def test_title_property(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli a title property-t.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        assert launchpad_page.title == "🚀 Launchpad"

    def test_is_loaded_property_initial(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli az is_loaded property kezdeti állapotát.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        assert launchpad_page.is_loaded is False

    def test_is_loaded_property_after_navigation(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli az is_loaded property-t navigáció után.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        launchpad_page.on_navigate_to()
        assert launchpad_page.is_loaded is True

    def test_on_navigate_to_with_params(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli a navigációt paraméterekkel.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        params: dict[str, str] | None = {"key": "value"}
        launchpad_page.on_navigate_to(params)

        assert launchpad_page.is_loaded is True

    def test_on_navigate_to_without_params(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli a navigációt paraméterek nélkül.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        launchpad_page.on_navigate_to()

        assert launchpad_page.is_loaded is True

    def test_on_navigate_from(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli az oldal elhagyásakor történő akciót.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        # Ez a teszt főleg arra szolgál, hogy lefusson a metódus
        # anélkül, hogy hibát dobna
        launchpad_page.on_navigate_from()

    @patch("streamlit.title")
    @patch("streamlit.markdown")
    @patch("streamlit.columns")
    @patch("streamlit.container")
    @patch("streamlit.subheader")
    @patch("streamlit.write")
    @patch("streamlit.page_link")
    @patch("streamlit.divider")
    def test_render(
        self,
        mock_divider: MagicMock,
        mock_page_link: MagicMock,
        mock_write: MagicMock,
        mock_subheader: MagicMock,
        mock_container: MagicMock,
        mock_columns: MagicMock,
        mock_markdown: MagicMock,
        mock_title: MagicMock,
        launchpad_page: LaunchpadPage,
    ) -> None:
        """Teszteli az oldal renderelését.

        Args:
            mock_divider: Mockolt divider.
            mock_page_link: Mockolt page_link.
            mock_write: Mockolt write.
            mock_subheader: Mockolt subheader.
            mock_container: Mockolt container.
            mock_columns: Mockolt columns.
            mock_markdown: Mockolt markdown.
            mock_title: Mockolt title.
            launchpad_page: A tesztelendő oldal példány.
        """
        # Mockoljuk a columns hívásokat, hogy tuple-t adjon vissza
        mock_columns.return_value = (MagicMock(), MagicMock())

        # Mockoljuk a container context managerét
        mock_container.return_value.__enter__.return_value = MagicMock()

        launchpad_page.render()

        # Ellenőrizzük, hogy a főbb Streamlit függvények meghívásra kerültek
        mock_title.assert_called_once_with("🚀 Launchpad")
        assert mock_markdown.call_count >= 2  # Legalább 2 alkalommal hívódik meg
        assert mock_columns.call_count == 3  # 3 sorban vannak kártyák
        assert mock_container.call_count == 5  # 5 kártya container
        assert mock_subheader.call_count == 5  # 5 alcím
        assert mock_write.call_count == 5  # 5 leírás
        assert mock_page_link.call_count == 5  # 5 link
        mock_divider.assert_called_once()

    def test_render_without_errors(self, launchpad_page: LaunchpadPage) -> None:
        """Teszteli, hogy a render metódus hiba nélkül lefut.

        Args:
            launchpad_page: A tesztelendő oldal példány.
        """
        # Ez a teszt arra szolgál, hogy a render metódus hiba nélkül lefusson
        # a lehető legtermészetesebb környezetben
        try:
            with (
                patch("streamlit.title"),
                patch("streamlit.markdown"),
                patch("streamlit.columns") as mock_columns,
                patch("streamlit.container") as mock_container,
                patch("streamlit.subheader"),
                patch("streamlit.write"),
                patch("streamlit.page_link"),
                patch("streamlit.divider"),
            ):
                # Beállítjuk a mockokat a helyes viselkedéshez
                mock_columns.return_value = (MagicMock(), MagicMock())
                mock_container.return_value.__enter__.return_value = MagicMock()

                launchpad_page.render()

        except Exception as e:
            pytest.fail(f"A render metódus hibát dobott: {e}")
