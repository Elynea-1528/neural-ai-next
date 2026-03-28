"""Unit tesztek a PageInterface interfészhez."""

from unittest.mock import MagicMock

from neural_ai.ui.interfaces.page_interface import PageInterface


class TestPageInterface:
    """Tesztek a PageInterface interfészhez."""

    def test_interface_is_runtime_checkable(self) -> None:
        """Teszteli, hogy az interfész runtime checkable."""
        mock_page = MagicMock(spec=PageInterface)
        assert isinstance(mock_page, PageInterface)

    def test_render_signature(self) -> None:
        """Teszteli a render metódus szignatúráját."""
        mock_page = MagicMock(spec=PageInterface)
        mock_content = MagicMock()
        mock_page.render.return_value = mock_content
        result = mock_page.render()
        assert result is mock_content
        mock_page.render.assert_called_once()

    def test_on_navigate_to_with_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterekkel."""
        mock_page = MagicMock(spec=PageInterface)
        params: dict[str, object] = {"id": "123", "mode": "view"}
        mock_page.on_navigate_to(params)
        mock_page.on_navigate_to.assert_called_once_with(params)

    def test_on_navigate_to_without_params(self) -> None:
        """Teszteli az on_navigate_to metódust paraméterek nélkül."""
        mock_page = MagicMock(spec=PageInterface)
        mock_page.on_navigate_to()
        mock_page.on_navigate_to.assert_called_once()

    def test_on_navigate_from_signature(self) -> None:
        """Teszteli az on_navigate_from metódus szignatúráját."""
        mock_page = MagicMock(spec=PageInterface)
        mock_page.on_navigate_from()
        mock_page.on_navigate_from.assert_called_once()

    def test_title_property(self) -> None:
        """Teszteli a title property-t."""
        mock_page = MagicMock(spec=PageInterface)
        mock_page.title = "Test Page"
        assert mock_page.title == "Test Page"

    def test_is_loaded_property_true(self) -> None:
        """Teszteli az is_loaded property-t, amikor True."""
        mock_page = MagicMock(spec=PageInterface)
        mock_page.is_loaded = True
        assert mock_page.is_loaded is True

    def test_is_loaded_property_false(self) -> None:
        """Teszteli az is_loaded property-t, amikor False."""
        mock_page = MagicMock(spec=PageInterface)
        mock_page.is_loaded = False
        assert mock_page.is_loaded is False

    def test_interface_has_all_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza az összes szükséges metódust."""
        required_methods = [
            "__init__",
            "render",
            "on_navigate_to",
            "on_navigate_from",
        ]
        for method in required_methods:
            assert hasattr(PageInterface, method)

    def test_interface_has_properties(self) -> None:
        """Teszteli, hogy az interfész tartalmazza a property-ket."""
        assert hasattr(PageInterface, "title")
        assert hasattr(PageInterface, "is_loaded")

    def test_mock_implements_interface(self) -> None:
        """Teszteli, hogy a mock objektum implementálja az interfészt."""
        mock_page = MagicMock(spec=PageInterface)
        assert hasattr(mock_page, "render")
        assert hasattr(mock_page, "on_navigate_to")
        assert hasattr(mock_page, "on_navigate_from")
        assert hasattr(mock_page, "title")
        assert hasattr(mock_page, "is_loaded")
