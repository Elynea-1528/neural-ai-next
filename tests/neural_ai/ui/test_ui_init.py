"""Unit tesztek a neural_ai.ui.__init__ modulhoz."""

import neural_ai.ui as ui_module


class TestUIInit:
    """Tesztek a neural_ai.ui.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(ui_module, "__all__")
        assert isinstance(ui_module.__all__, list)

    def test_all_exports_ui_service_factory(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a UIServiceFactory-t."""
        assert "UIServiceFactory" in ui_module.__all__

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 1 elemet tartalmaz."""
        assert len(ui_module.__all__) == 1

    def test_ui_service_factory_importable(self) -> None:
        """Teszteli, hogy a UIServiceFactory importálható."""
        assert hasattr(ui_module, "UIServiceFactory")

    def test_ui_service_factory_is_class(self) -> None:
        """Teszteli, hogy a UIServiceFactory osztály."""
        from neural_ai.ui.factory import UIServiceFactory

        assert ui_module.UIServiceFactory is UIServiceFactory

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert ui_module.__doc__ is not None
        assert len(ui_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert ui_module.__doc__ is not None
        assert "UI modul" in ui_module.__doc__
        assert "Neural AI Next" in ui_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in ui_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in ui_module.__all__:
            assert hasattr(ui_module, name)
