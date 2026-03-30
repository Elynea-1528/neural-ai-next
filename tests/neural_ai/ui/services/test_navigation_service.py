"""Unit tesztek a navigation_service modulhoz.

# pyright: reportUnknownArgumentType=false
# Mock config dict type inference hibák.

Ez a modul teszteli a NavigationService osztály funkcióit.
"""

from unittest.mock import MagicMock

import pytest

from neural_ai.ui.interfaces.page_interface import PageInterface
from neural_ai.ui.services.navigation_service import NavigationService


class TestNavigationServiceInit:
    """Tesztek a NavigationService inicializálásához."""

    def test_init_creates_instance(self) -> None:
        """Ellenőrzi, hogy a NavigationService létrehozható."""
        # Arrange
        mock_logger = MagicMock()
        mock_config: dict[str, str] = {}
        mock_core = MagicMock()

        # Act
        service = NavigationService(  # pyright: ignore[reportUnknownArgumentType]
            logger=mock_logger,
            config=mock_config,  # type: ignore[arg-type]
            core_components=mock_core,
        )

        # Assert
        assert service._logger == mock_logger  # pyright: ignore[reportPrivateUsage]
        assert service._config == mock_config  # pyright: ignore[reportPrivateUsage]
        assert service._core_components == mock_core  # pyright: ignore[reportPrivateUsage]
        assert service._pages == {}  # pyright: ignore[reportPrivateUsage]
        assert service._history == []  # pyright: ignore[reportPrivateUsage]
        assert service._current_page is None  # pyright: ignore[reportPrivateUsage]
        assert service._subscribers == []  # pyright: ignore[reportPrivateUsage]


class TestNavigationServiceRegisterPage:
    """Tesztek a register_page metódushoz."""

    def test_register_page_adds_page(self) -> None:
        """Ellenőrzi, hogy az oldal regisztrálása működik."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page = MagicMock(spec=PageInterface)

        # Act
        service.register_page("home", mock_page)

        # Assert
        assert "home" in service._pages  # pyright: ignore[reportPrivateUsage]
        assert service._pages["home"] == mock_page  # pyright: ignore[reportPrivateUsage]

    def test_register_first_page_sets_current(self) -> None:
        """Ellenőrzi, hogy az első oldal automatikusan aktuális lesz."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page = MagicMock(spec=PageInterface)

        # Act
        service.register_page("home", mock_page)

        # Assert
        assert service._current_page == "home"  # pyright: ignore[reportPrivateUsage]
        assert service._history == ["home"]  # pyright: ignore[reportPrivateUsage]


class TestNavigationServiceNavigateTo:
    """Tesztek a navigate_to metódushoz."""

    def test_navigate_to_raises_error_for_unknown_page(self) -> None:
        """Ellenőrzi, hogy hiba dobódik ismeretlen oldalra navigáláskor."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Oldal nem található: unknown"):
            service.navigate_to("unknown")

    def test_navigate_to_calls_on_navigate_from_on_current_page(self) -> None:
        """Ellenőrzi, hogy az aktuális oldal on_navigate_from metódusa meghívódik."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)

        # Act
        service.navigate_to("page2")

        # Assert
        mock_page1.on_navigate_from.assert_called_once()

    def test_navigate_to_calls_on_navigate_to_on_new_page(self) -> None:
        """Ellenőrzi, hogy az új oldal on_navigate_to metódusa meghívódik."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)

        # Act
        service.navigate_to("page2", {"param": "value"})

        # Assert
        mock_page2.on_navigate_to.assert_called_once_with({"param": "value"})

    def test_navigate_to_updates_history(self) -> None:
        """Ellenőrzi, hogy a navigáció frissíti az előzményeket."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)

        # Act
        service.navigate_to("page2")

        # Assert
        assert service._history == ["page1", "page2"]  # pyright: ignore[reportPrivateUsage]
        assert service._current_page == "page2"  # pyright: ignore[reportPrivateUsage]

    def test_navigate_to_notifies_subscribers(self) -> None:
        """Ellenőrzi, hogy a navigáció értesíti a feliratkozókat."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)

        mock_callback = MagicMock()
        service.subscribe(mock_callback)

        # Act
        service.navigate_to("page2", {"param": "value"})

        # Assert
        mock_callback.assert_called_once_with("page2", {"param": "value"})


class TestNavigationServiceGoBack:
    """Tesztek a go_back metódushoz."""

    def test_go_back_does_nothing_when_no_history(self) -> None:
        """Ellenőrzi, hogy a go_back nem csinál semmit, ha nincs előzmény."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page)

        # Act
        service.go_back()

        # Assert
        assert service._current_page == "page1"  # pyright: ignore[reportPrivateUsage]
        assert service._history == ["page1"]  # pyright: ignore[reportPrivateUsage]

    def test_go_back_navigates_to_previous_page(self) -> None:
        """Ellenőrzi, hogy a go_back visszanavigál az előző oldalra."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)
        service.navigate_to("page2")

        # Act
        service.go_back()

        # Assert
        assert service._current_page == "page1"  # pyright: ignore[reportPrivateUsage]
        assert service._history == ["page1"]  # pyright: ignore[reportPrivateUsage]
        mock_page1.on_navigate_to.assert_called()

    def test_go_back_notifies_subscribers(self) -> None:
        """Ellenőrzi, hogy a go_back értesíti a feliratkozókat."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)
        service.navigate_to("page2")

        mock_callback = MagicMock()
        service.subscribe(mock_callback)

        # Act
        service.go_back()

        # Assert
        mock_callback.assert_called_once_with("page1", {})


class TestNavigationServiceGetCurrentPage:
    """Tesztek a get_current_page metódushoz."""

    def test_get_current_page_returns_none_when_no_page(self) -> None:
        """Ellenőrzi, hogy None-t ad vissza, ha nincs aktuális oldal."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act
        result = service.get_current_page()

        # Assert
        assert result is None

    def test_get_current_page_returns_current_page(self) -> None:
        """Ellenőrzi, hogy az aktuális oldalt adja vissza."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page = MagicMock(spec=PageInterface)
        service.register_page("home", mock_page)

        # Act
        result = service.get_current_page()

        # Assert
        assert result == mock_page


class TestNavigationServiceGetPageHistory:
    """Tesztek a get_page_history metódushoz."""

    def test_get_page_history_returns_copy(self) -> None:
        """Ellenőrzi, hogy az előzmények másolatát adja vissza."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page1 = MagicMock(spec=PageInterface)
        mock_page2 = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page1)
        service.register_page("page2", mock_page2)
        service.navigate_to("page2")

        # Act
        history = service.get_page_history()

        # Assert
        assert history == ["page1", "page2"]
        assert history is not service._history  # pyright: ignore[reportPrivateUsage]


class TestNavigationServiceSubscribe:
    """Tesztek a subscribe metódushoz."""

    def test_subscribe_adds_callback(self) -> None:
        """Ellenőrzi, hogy a feliratkozás hozzáadja a callback-et."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_callback = MagicMock()

        # Act
        service.subscribe(mock_callback)

        # Assert
        assert mock_callback in service._subscribers  # pyright: ignore[reportPrivateUsage]

    def test_subscribe_callback_handles_exception(self) -> None:
        """Ellenőrzi, hogy a callback kivétel esetén sem állítja le a rendszert."""
        # Arrange
        service = NavigationService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        mock_page = MagicMock(spec=PageInterface)
        service.register_page("page1", mock_page)

        def failing_callback(page_name: str, params: dict[str, object]) -> None:
            raise RuntimeError("Test error")

        service.subscribe(failing_callback)

        # Act & Assert (nem dob kivételt)
        service.navigate_to("page1")
