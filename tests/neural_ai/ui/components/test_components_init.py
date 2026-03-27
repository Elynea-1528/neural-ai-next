"""Unit tesztek a neural_ai.ui.components.__init__ modulhoz."""

import neural_ai.ui.components as components_module


class TestComponentsInit:
    """Tesztek a neural_ai.ui.components.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(components_module, "__all__")
        assert isinstance(components_module.__all__, list)

    def test_all_exports_base_widget(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a BaseWidget-et."""
        assert "BaseWidget" in components_module.__all__

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 1 elemet tartalmaz."""
        assert len(components_module.__all__) == 1

    def test_base_widget_importable(self) -> None:
        """Teszteli, hogy a BaseWidget importálható."""
        assert hasattr(components_module, "BaseWidget")

    def test_base_widget_is_class(self) -> None:
        """Teszteli, hogy a BaseWidget osztály."""
        from neural_ai.ui.components.base_widget import BaseWidget

        assert components_module.BaseWidget is BaseWidget

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert components_module.__doc__ is not None
        assert len(components_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert components_module.__doc__ is not None
        assert "UI komponensek" in components_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in components_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in components_module.__all__:
            assert hasattr(components_module, name)
