"""Tesztelési modul a neural_ai.core.base.__init__ modulhoz.

Ez a modul tartalmazza a neural_ai.core.base modulban exportált osztályok
és függvények teszteléséhez szükséges teszteket.
"""

import sys
import unittest
from typing import TYPE_CHECKING

# A TYPE_CHECKING blokk tesztelése
if TYPE_CHECKING:
    from neural_ai.core.base.factory import CoreComponentFactory
    from neural_ai.core.base.implementations.component_bundle import CoreComponents
    from neural_ai.core.base.implementations.di_container import DIContainer

# Normál importok
from neural_ai.core.base import CoreComponentFactory, CoreComponents, DIContainer


class TestInitModule(unittest.TestCase):
    """Tesztosztály a neural_ai.core.base.__init__ modul funkcionalitásához."""

    def test_all_imports_available(self) -> None:
        """Teszteli, hogy minden szükséges osztály elérhető-e az importálás után."""
        # Ellenőrizzük, hogy a modulban elérhetőek-e az exportált osztályok
        self.assertTrue(hasattr(sys.modules["neural_ai.core.base"], "DIContainer"))
        self.assertTrue(hasattr(sys.modules["neural_ai.core.base"], "CoreComponents"))
        self.assertTrue(hasattr(sys.modules["neural_ai.core.base"], "CoreComponentFactory"))

    def test_all_list_contains_all_exports(self) -> None:
        """Teszteli, hogy a __all__ lista tartalmazza-e az összes exportálandó elemet."""
        from neural_ai.core.base import __all__ as module_all

        expected_exports = ["DIContainer", "CoreComponents", "CoreComponentFactory"]
        self.assertEqual(set(module_all), set(expected_exports))

    def test_dicontainer_class_importable(self) -> None:
        """Teszteli, hogy a DIContainer osztály importálható-e."""
        self.assertIsNotNone(DIContainer)
        self.assertTrue(callable(DIContainer))

    def test_core_components_class_importable(self) -> None:
        """Teszteli, hogy a CoreComponents osztály importálható-e."""
        self.assertIsNotNone(CoreComponents)
        self.assertTrue(callable(CoreComponents))

    def test_core_component_factory_class_importable(self) -> None:
        """Teszteli, hogy a CoreComponentFactory osztály importálható-e."""
        self.assertIsNotNone(CoreComponentFactory)
        self.assertTrue(callable(CoreComponentFactory))

    def test_type_checking_block_exists(self) -> None:
        """Teszteli, hogy a TYPE_CHECKING blokk létezik-e a forráskódban."""
        import inspect

        import neural_ai.core.base

        source = inspect.getsource(neural_ai.core.base)
        self.assertIn("TYPE_CHECKING", source)
        self.assertIn("if TYPE_CHECKING:", source)


if __name__ == "__main__":
    unittest.main()
