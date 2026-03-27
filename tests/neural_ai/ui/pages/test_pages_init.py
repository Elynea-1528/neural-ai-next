"""Unit tesztek a neural_ai.ui.pages.__init__ modulhoz."""

from unittest.mock import MagicMock, patch

import neural_ai.ui.pages as pages_module


class TestPagesInit:
    """Tesztek a neural_ai.ui.pages.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(pages_module, "__all__")
        assert isinstance(pages_module.__all__, list)

    def test_all_exports_create_launchpad_page(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a create_launchpad_page-t."""
        assert "create_launchpad_page" in pages_module.__all__

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 1 elemet tartalmaz."""
        assert len(pages_module.__all__) == 1

    def test_create_launchpad_page_importable(self) -> None:
        """Teszteli, hogy a create_launchpad_page importálható."""
        assert hasattr(pages_module, "create_launchpad_page")

    def test_create_launchpad_page_is_callable(self) -> None:
        """Teszteli, hogy a create_launchpad_page hívható."""
        assert callable(pages_module.create_launchpad_page)

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert pages_module.__doc__ is not None
        assert len(pages_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert pages_module.__doc__ is not None
        assert "UI oldalak" in pages_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in pages_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in pages_module.__all__:
            assert hasattr(pages_module, name)

    def test_create_launchpad_page_with_mocks(self) -> None:
        """Teszteli a create_launchpad_page függvényt mock objektumokkal."""
        logger = MagicMock()
        config = MagicMock()

        mock_bridge = MagicMock()
        mock_page = MagicMock()

        with (
            patch("neural_ai.ui.pages.CoreBridge", return_value=mock_bridge),
            patch("importlib.util.spec_from_file_location") as mock_spec_from_file,
            patch("importlib.util.module_from_spec") as mock_module_from_spec,
        ):
            # Mock spec és loader
            mock_spec = MagicMock()
            mock_loader = MagicMock()
            mock_spec.loader = mock_loader
            mock_spec_from_file.return_value = mock_spec

            # Mock module
            mock_module = MagicMock()
            mock_module.LaunchpadPage = MagicMock(return_value=mock_page)
            mock_module_from_spec.return_value = mock_module

            result = pages_module.create_launchpad_page(logger, config)

            # Ellenőrzések
            mock_bridge.initialize.assert_called_once()
            assert result is mock_page
