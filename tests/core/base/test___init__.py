"""Tesztek a neural_ai.core.base modulhoz.

Ez a tesztmodul ellenőrzi a neural_ai.core.base modul
alapvető funkcionalitását és importjait.
"""

import pytest

from neural_ai.core.base import CoreComponentFactory, CoreComponents, DIContainer


class TestBaseModuleImports:
    """Tesztosztály a base modul importjainak ellenőrzéséhez."""

    def test_dicontainer_import(self) -> None:
        """Teszteli, hogy a DIContainer importálható-e."""
        assert DIContainer is not None
        assert hasattr(DIContainer, "__init__")

    def test_core_components_import(self) -> None:
        """Teszteli, hogy a CoreComponents importálható-e."""
        assert CoreComponents is not None
        assert hasattr(CoreComponents, "__init__")

    def test_core_component_factory_import(self) -> None:
        """Teszteli, hogy a CoreComponentFactory importálható-e."""
        assert CoreComponentFactory is not None
        assert hasattr(CoreComponentFactory, "__init__")

    def test_all_dunder_variable(self) -> None:
        """Teszteli, hogy a __all__ változó helyesen van-e definiálva."""
        from neural_ai.core.base import __all__ as base_all

        expected_exports = ["DIContainer", "CoreComponents", "CoreComponentFactory"]
        assert base_all == expected_exports

        # Ellenőrizzük, hogy minden exportált név létező objektum
        for name in base_all:
            assert hasattr(__import__("neural_ai.core.base", fromlist=[name]), name)

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modulnak van-e docstringje."""
        import neural_ai.core.base

        assert neural_ai.core.base.__doc__ is not None
        assert len(neural_ai.core.base.__doc__) > 0
        assert "Neural AI" in neural_ai.core.base.__doc__


class TestBaseModuleFunctionality:
    """Tesztosztály a base modul funkcionalitásának ellenőrzéséhez."""

    def test_dicontainer_singleton_pattern(self) -> None:
        """Teszteli a DIContainer singleton viselkedését."""
        container1 = DIContainer()
        container2 = DIContainer()

        # Singleton pattern miatt ugyanazt az példányt kell kapnunk
        assert container1 is container2

    def test_core_components_initialization(self) -> None:
        """Teszteli a CoreComponents inicializálását."""
        components = CoreComponents()
        assert components is not None

        # Alapvető attribútumok ellenőrzése
        assert hasattr(components, "container")
        assert hasattr(components, "factory")

    def test_factory_creation(self) -> None:
        """Teszteli a CoreComponentFactory létrehozását."""
        container = DIContainer()
        factory = CoreComponentFactory(container)
        assert factory is not None
        assert hasattr(factory, "create_component")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
