"""Unit tesztek az AILabPage osztályhoz."""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# AILabPage nincs exportálva a pages __init__.py-ban, közvetlenül importáljuk
# Dinamikus import az emoji-s fájlnévhez
test_file_path = Path(__file__)
project_root = test_file_path.parent.parent.parent.parent.parent
ai_lab_file = project_root / "neural_ai" / "ui" / "pages" / "04_🧠_AI_Lab.py"
spec = importlib.util.spec_from_file_location("ai_lab_module", ai_lab_file)
if spec and spec.loader:
    ai_lab_module = importlib.util.module_from_spec(spec)
    # Regisztráljuk a modult a sys.modules-ban, hogy a patch működjön
    sys.modules["ai_lab_module"] = ai_lab_module
    spec.loader.exec_module(ai_lab_module)
    AILabPage = ai_lab_module.AILabPage  # type: ignore


class TestAILabPage:
    """Tesztek az AILabPage osztályhoz."""

    def test_initialization(self) -> None:
        """Teszteli az AILabPage inicializálását."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        assert page._bridge is mock_bridge  # type: ignore
        assert page._loaded is False  # type: ignore
        assert page._title == "🧠 AI Lab"  # type: ignore

    def test_initialization_with_kwargs(self) -> None:
        """Teszteli az AILabPage inicializálását kwargs-szal."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge, custom_param="value")
        assert page._bridge is mock_bridge  # type: ignore
        assert page._loaded is False  # type: ignore

    def test_title_property(self) -> None:
        """Teszteli a title property-t."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        assert page.title == "🧠 AI Lab"

    def test_is_loaded_property_initial(self) -> None:
        """Teszteli az is_loaded property kezdeti értékét."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        assert page.is_loaded is False

    def test_is_loaded_property_after_navigate(self) -> None:
        """Teszteli az is_loaded property-t navigálás után."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        page.on_navigate_to()
        assert page.is_loaded is True

    @patch("ai_lab_module.st")
    def test_render(self, mock_st: MagicMock) -> None:
        """Teszteli a render metódust."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        page.render()
        mock_st.title.assert_called_once_with("🧠 AI Lab")
        mock_st.markdown.assert_called_once_with("AI modellek kezelése és futtatása.")

    def test_on_navigate_to_without_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterek nélkül."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True

    def test_on_navigate_to_with_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterekkel."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        params: dict[str, object] = {"model": "gpt-4"}
        page.on_navigate_to(params)
        assert page.is_loaded is True

    def test_on_navigate_from(self) -> None:
        """Teszteli az on_navigate_from metódust."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        page.on_navigate_to()
        page.on_navigate_from()
        # on_navigate_from nem változtatja meg az állapotot ebben az implementációban

    def test_multiple_navigate_cycles(self) -> None:
        """Teszteli a többszöri navigálást."""
        mock_bridge = MagicMock()
        page = AILabPage(mock_bridge)
        assert page.is_loaded is False
        page.on_navigate_to()
        assert page.is_loaded is True
        page.on_navigate_from()
        assert page.is_loaded is True
        page.on_navigate_to()
        assert page.is_loaded is True
