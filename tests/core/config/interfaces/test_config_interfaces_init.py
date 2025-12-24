"""Tesztek a konfiguráció interfészek __init__ moduljához.

Ez a modul tartalmazza a neural_ai.core.config.interfaces csomag
__init__.py fájljának tesztjeit.
"""

import pytest

from neural_ai.core.config.interfaces import (
    ConfigManagerFactoryInterface,
    ConfigManagerInterface,
)


class TestImports:
    """Importálási tesztesetek."""

    def test_config_manager_interface_import(self) -> None:
        """Teszteli a ConfigManagerInterface importját."""
        assert ConfigManagerInterface is not None
        assert hasattr(ConfigManagerInterface, "__abstractmethods__")

    def test_config_manager_factory_interface_import(self) -> None:
        """Teszteli a ConfigManagerFactoryInterface importját."""
        assert ConfigManagerFactoryInterface is not None
        assert hasattr(ConfigManagerFactoryInterface, "__abstractmethods__")

    def test_all_list_contents(self) -> None:
        """Teszteli a __all__ lista tartalmát."""
        from neural_ai.core.config.interfaces import __all__ as interfaces_all

        expected_exports = ["ConfigManagerInterface", "ConfigManagerFactoryInterface"]
        assert len(interfaces_all) == len(expected_exports)
        assert set(interfaces_all) == set(expected_exports)


class TestInterfaceStructure:
    """Interfész struktúra tesztesetek."""

    def test_config_manager_interface_is_abstract(self) -> None:
        """Teszteli, hogy a ConfigManagerInterface absztrakt osztály-e."""
        with pytest.raises(TypeError):
            ConfigManagerInterface()  # type: ignore

    def test_factory_interface_is_abstract(self) -> None:
        """Teszteli, hogy a ConfigManagerFactoryInterface absztrakt osztály-e."""
        with pytest.raises(TypeError):
            ConfigManagerFactoryInterface()  # type: ignore

    def test_config_manager_interface_methods(self) -> None:
        """Teszteli a ConfigManagerInterface metódusait."""
        abstract_methods = ConfigManagerInterface.__abstractmethods__
        expected_methods = {
            "__init__",
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "validate",
        }
        assert expected_methods.issubset(abstract_methods)

    def test_factory_interface_methods(self) -> None:
        """Teszteli a ConfigManagerFactoryInterface metódusait."""
        abstract_methods = ConfigManagerFactoryInterface.__abstractmethods__
        expected_methods = {
            "register_manager",
            "get_manager",
            "create_manager",
        }
        assert expected_methods.issubset(abstract_methods)
