"""Unit tesztek a neural_ai.collectors.__init__ modulhoz."""

import neural_ai.collectors as collectors_module
from neural_ai.collectors.jforex.factory import JForexFactory


class TestCollectorsInit:
    """Tesztek a neural_ai.collectors.__init__ modulhoz."""

    def test_module_has_all_attribute(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(collectors_module, "__all__")
        assert isinstance(collectors_module.__all__, list)

    def test_all_exports_jforex_factory(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a JForexFactory-t."""
        assert "JForexFactory" in collectors_module.__all__

    def test_all_exports_count(self) -> None:
        """Teszteli, hogy az __all__ pontosan 1 elemet tartalmaz."""
        assert len(collectors_module.__all__) == 1

    def test_jforex_factory_importable(self) -> None:
        """Teszteli, hogy a JForexFactory importálható."""
        assert hasattr(collectors_module, "JForexFactory")

    def test_jforex_factory_is_correct_class(self) -> None:
        """Teszteli, hogy a JForexFactory a helyes osztály."""
        assert collectors_module.JForexFactory is JForexFactory

    def test_module_docstring_exists(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert collectors_module.__doc__ is not None
        assert len(collectors_module.__doc__) > 0

    def test_module_docstring_contains_description(self) -> None:
        """Teszteli, hogy a docstring tartalmaz leírást."""
        assert collectors_module.__doc__ is not None
        assert "Collectors" in collectors_module.__doc__

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in collectors_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_are_accessible(self) -> None:
        """Teszteli, hogy az __all__-ban szereplő elemek elérhetők."""
        for name in collectors_module.__all__:
            assert hasattr(collectors_module, name)

    def test_all_exports_are_classes(self) -> None:
        """Teszteli, hogy az összes export osztály."""
        assert isinstance(collectors_module.JForexFactory, type)
