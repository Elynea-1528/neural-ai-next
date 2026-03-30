"""Unit tesztek a LiveOpsPage osztályhoz."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

# LiveOpsPage nincs exportálva a pages __init__.py-ban, közvetlenül importáljuk
# Dinamikus import az emoji-s fájlnévhez
test_file_path = Path(__file__)
project_root = test_file_path.parent.parent.parent.parent.parent
live_ops_file = project_root / "neural_ai" / "ui" / "pages" / "06_⚡_Live_Ops.py"
spec = importlib.util.spec_from_file_location("live_ops_module", live_ops_file)
if spec and spec.loader:
    live_ops_module = importlib.util.module_from_spec(spec)
    # Regisztráljuk a modult a sys.modules-ban, hogy a patch működjön
    sys.modules["live_ops_module"] = live_ops_module
    spec.loader.exec_module(live_ops_module)
    LiveOpsPage = live_ops_module.LiveOpsPage


class TestLiveOpsPage:
    """Tesztek a LiveOpsPage osztályhoz."""

    def test_initialization(self) -> None:
        """Teszteli a LiveOpsPage inicializálását."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        assert page._bridge is mock_bridge
        assert page._loaded is False
        assert page._title == "⚡ Live Ops"

    def test_initialization_with_kwargs(self) -> None:
        """Teszteli a LiveOpsPage inicializálását kwargs-szal."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge, custom_param="value")
        assert page._bridge is mock_bridge
        assert page._loaded is False

    def test_title_property(self) -> None:
        """Teszteli a title property-t."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        assert page.title == "⚡ Live Ops"

    def test_is_loaded_property_initial(self) -> None:
        """Teszteli az is_loaded property kezdeti értékét."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        assert page.is_loaded is False

    def test_is_loaded_property_after_navigate(self) -> None:
        """Teszteli az is_loaded property-t navigálás után."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        page.on_navigate_to()
        assert page.is_loaded is True

    def test_render(self) -> None:
        """Teszteli a render metódust."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        # A render metódus üres ebben az implementációban
        page.render()

    def test_on_navigate_to_without_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterek nélkül."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True

    def test_on_navigate_to_with_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterekkel."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        params: dict[str, object] = {"mode": "trading"}
        page.on_navigate_to(params)
        assert page.is_loaded is True

    def test_on_navigate_from(self) -> None:
        """Teszteli az on_navigate_from metódust."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        page.on_navigate_to()
        page.on_navigate_from()
        # on_navigate_from nem változtatja meg az állapotot ebben az implementációban

    def test_multiple_navigate_cycles(self) -> None:
        """Teszteli a többszöri navigálást."""
        mock_bridge = MagicMock()
        page = LiveOpsPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True
        page.on_navigate_from()
        assert page.is_loaded is True
        page.on_navigate_to()
        assert page.is_loaded is True
