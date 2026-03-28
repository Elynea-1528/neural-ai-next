"""Unit tesztek a NavigationServiceInterface interfészhez."""

from unittest.mock import MagicMock

from neural_ai.ui.interfaces.navigation_service_interface import NavigationServiceInterface


class TestNavigationServiceInterface:
    """Tesztek a NavigationServiceInterface interfészhez."""

    def test_interface_is_runtime_checkable(self) -> None:
        """Teszteli, hogy az interfész runtime checkable."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        assert isinstance(mock_service, NavigationServiceInterface)

    def test_navigate_to_with_params(self) -> None:
        """Teszteli a navigate_to metódust paraméterekkel."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        params: dict[str, object] = {"id": "123", "mode": "edit"}
        mock_service.navigate_to("data_hub", params)
        mock_service.navigate_to.assert_called_once_with("data_hub", params)

    def test_navigate_to_without_params(self) -> None:
        """Teszteli a navigate_to metódust paraméterek nélkül."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        mock_service.navigate_to("launchpad")
        mock_service.navigate_to.assert_called_once_with("launchpad")

    def test_go_back_signature(self) -> None:
        """Teszteli a go_back metódus szignatúráját."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        mock_service.go_back()
        mock_service.go_back.assert_called_once()

    def test_get_current_page_returns_page(self) -> None:
        """Teszteli a get_current_page metódust, amikor oldalt ad vissza."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        mock_page = MagicMock()
        mock_service.get_current_page.return_value = mock_page
        result = mock_service.get_current_page()
        assert result is mock_page
        mock_service.get_current_page.assert_called_once()

    def test_get_current_page_returns_none(self) -> None:
        """Teszteli a get_current_page metódust, amikor None-t ad vissza."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        mock_service.get_current_page.return_value = None
        result = mock_service.get_current_page()
        assert result is None
        mock_service.get_current_page.assert_called_once()

    def test_get_page_history_signature(self) -> None:
        """Teszteli a get_page_history metódus szignatúráját."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        history: list[str] = ["launchpad", "data_hub", "strategy_lab"]
        mock_service.get_page_history.return_value = history
        result = mock_service.get_page_history()
        assert result == history
        assert len(result) == 3
        mock_service.get_page_history.assert_called_once()

    def test_get_page_history_empty(self) -> None:
        """Teszteli a get_page_history metódust üres listával."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        history: list[str] = []
        mock_service.get_page_history.return_value = history
        result = mock_service.get_page_history()
        assert result == []
        mock_service.get_page_history.assert_called_once()

    def test_register_page_signature(self) -> None:
        """Teszteli a register_page metódus szignatúráját."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        mock_page = MagicMock()
        mock_service.register_page("custom_page", mock_page)
        mock_service.register_page.assert_called_once_with("custom_page", mock_page)

    def test_subscribe_signature(self) -> None:
        """Teszteli a subscribe metódus szignatúráját."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        callback = MagicMock()
        mock_service.subscribe(callback)
        mock_service.subscribe.assert_called_once_with(callback)

    def test_interface_has_all_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza az összes szükséges metódust."""
        required_methods = [
            "navigate_to",
            "go_back",
            "get_current_page",
            "get_page_history",
            "register_page",
            "subscribe",
        ]
        for method in required_methods:
            assert hasattr(NavigationServiceInterface, method)

    def test_mock_implements_interface(self) -> None:
        """Teszteli, hogy a mock objektum implementálja az interfészt."""
        mock_service = MagicMock(spec=NavigationServiceInterface)
        assert hasattr(mock_service, "navigate_to")
        assert hasattr(mock_service, "go_back")
        assert hasattr(mock_service, "get_current_page")
        assert hasattr(mock_service, "get_page_history")
        assert hasattr(mock_service, "register_page")
        assert hasattr(mock_service, "subscribe")
