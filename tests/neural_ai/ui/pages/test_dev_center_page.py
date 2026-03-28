"""Unit tesztek a DevCenterPage osztályhoz."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# A teszt fájl helye: tests/neural_ai/ui/pages/test_dev_center_page.py
# A cél fájl helye: neural_ai/ui/pages/02_🛠️_Dev_Center.py
test_file_path = Path(__file__)
project_root = test_file_path.parent.parent.parent.parent.parent
dev_center_file = project_root / "neural_ai" / "ui" / "pages" / "02_🛠️_Dev_Center.py"
spec = importlib.util.spec_from_file_location("dev_center_module", dev_center_file)
if spec and spec.loader:
    dev_center_module = importlib.util.module_from_spec(spec)
    # Regisztráljuk a modult a sys.modules-ban, hogy a patch működjön
    sys.modules["dev_center_module"] = dev_center_module
    spec.loader.exec_module(dev_center_module)
    DevCenterPage = dev_center_module.DevCenterPage  # type: ignore


class TestDevCenterPage:
    """Tesztek a DevCenterPage osztályhoz."""

    def test_initialization(self) -> None:
        """Teszteli a DevCenterPage inicializálását."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        assert page._bridge is mock_bridge  # type: ignore
        assert page._loaded is False  # type: ignore
        assert page._title == "🛠️ Dev Center"  # type: ignore

    def test_initialization_with_kwargs(self) -> None:
        """Teszteli a DevCenterPage inicializálását kwargs-szal."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge, custom_param="value")
        assert page._bridge is mock_bridge  # type: ignore
        assert page._loaded is False  # type: ignore

    def test_title_property(self) -> None:
        """Teszteli a title property-t."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        assert page.title == "🛠️ Dev Center"

    def test_is_loaded_property_initial(self) -> None:
        """Teszteli az is_loaded property kezdeti értékét."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        assert page.is_loaded is False

    def test_is_loaded_property_after_navigate(self) -> None:
        """Teszteli az is_loaded property-t navigálás után."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        page.on_navigate_to()
        assert page.is_loaded is True

    @patch("dev_center_module.st")
    def test_render(self, mock_st: MagicMock) -> None:
        """Teszteli a render metódust."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        page.render()
        mock_st.title.assert_called_once_with("🛠️ Dev Center")
        mock_st.markdown.assert_called_once_with("Fejlesztői eszközök és konfigurációk.")

    def test_on_navigate_to_without_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterek nélkül."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True

    def test_on_navigate_to_with_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterekkel."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        params: dict[str, object] = {"mode": "debug"}
        page.on_navigate_to(params)
        assert page.is_loaded is True

    def test_on_navigate_from(self) -> None:
        """Teszteli az on_navigate_from metódust."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        page.on_navigate_to()
        page.on_navigate_from()
        # on_navigate_from nem változtatja meg az állapotot ebben az implementációban

    def test_multiple_navigate_cycles(self) -> None:
        """Teszteli a többszöri navigálást."""
        mock_bridge = MagicMock()
        page = DevCenterPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True
        page.on_navigate_from()
        assert page.is_loaded is True
        page.on_navigate_to()
        assert page.is_loaded is True
