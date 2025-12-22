"""Tesztelő modul a neural_ai.core.config.implementations csomaghoz.

Ez a modul tartalmazza a konfigurációkezelő implementációk teszteléséhez
szükséges teszteseteket.
"""

import sys
from importlib import import_module
from unittest import TestCase

from neural_ai.core.config.implementations import ConfigManagerFactory, YAMLConfigManager


class TestInit(TestCase):
    """Tesztosztály a modul inicializálásának ellenőrzéséhez."""

    def test_module_import(self) -> None:
        """Teszteli, hogy a modul sikeresen importálható-e."""
        # Ellenőrizzük, hogy a modul létezik-e
        try:
            import_module("neural_ai.core.config.implementations")
        except ImportError as e:
            self.fail(f"A modul importálása sikertelen: {e}")

    def test_all_exports(self) -> None:
        """Teszteli, hogy minden exportált osztály elérhető-e."""
        # Ellenőrizzük az __all__ listában szereplő osztályokat
        from neural_ai.core.config.implementations import __all__ as module_all

        for export_name in module_all:
            with self.subTest(export=export_name):
                self.assertTrue(
                    hasattr(sys.modules[__name__.rsplit(".", 1)[0]], export_name),
                    f"Az {export_name} nincs exportálva helyesen",
                )

    def test_config_manager_factory_available(self) -> None:
        """Teszteli, hogy a ConfigManagerFactory elérhető-e."""
        self.assertIsNotNone(ConfigManagerFactory)
        self.assertTrue(callable(ConfigManagerFactory.get_manager))

    def test_yaml_config_manager_available(self) -> None:
        """Teszteli, hogy a YAMLConfigManager elérhető-e."""
        self.assertIsNotNone(YAMLConfigManager)
        self.assertTrue(hasattr(YAMLConfigManager, "__init__"))

    def test_factory_has_methods(self) -> None:
        """Teszteli, hogy a factory osztály rendelkezik-e szükséges metódusokkal."""
        factory_methods = [
            "get_manager",
            "register_manager",
            "get_supported_extensions",
            "create_manager",
        ]

        for method_name in factory_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(ConfigManagerFactory, method_name),
                    f"A {method_name} metódus hiányzik a ConfigManagerFactory-ből",
                )

    def test_yaml_manager_has_methods(self) -> None:
        """Teszteli, hogy a YAMLConfigManager rendelkezik-e szükséges metódusokkal."""
        manager_methods = [
            "get",
            "set",
            "save",
            "load",
            "validate",
            "get_section",
        ]

        for method_name in manager_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(YAMLConfigManager, method_name),
                    f"A {method_name} metódus hiányzik a YAMLConfigManager-ből",
                )
