"""ConfigManagerInterface tesztelése."""

from typing import Any

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class TestConfigManagerInterface:
    """ConfigManagerInterface tesztosztály.

    Ez az osztály az interfész összes metódusának helyes definícióját ellenőrzi.
    """

    def test_init_method_signature(self) -> None:
        """__init__ metódus szignatúrájának ellenőrzése."""
        # Ellenőrizzük, hogy az __init__ metódus létezik-e és helyes-e a szignatúrája
        sig = ConfigManagerInterface.__init__.__annotations__
        assert "filename" in sig
        assert sig["filename"] == str | None
        assert sig["return"] is None

    def test_get_method_signature(self) -> None:
        """get metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.get.__annotations__
        assert "default" in sig
        assert sig["return"] is Any

    def test_get_section_method_signature(self) -> None:
        """get_section metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.get_section.__annotations__
        assert "section" in sig
        assert sig["section"] is str
        assert sig["return"] == dict[str, Any]

    def test_set_method_signature(self) -> None:
        """set metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.set.__annotations__
        assert "value" in sig
        assert sig["value"] is Any
        assert sig["return"] is None

    def test_save_method_signature(self) -> None:
        """save metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.save.__annotations__
        assert "filename" in sig
        assert sig["filename"] == str | None
        assert sig["return"] is None

    def test_load_method_signature(self) -> None:
        """load metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.load.__annotations__
        assert "filename" in sig
        assert sig["filename"] is str
        assert sig["return"] is None

    def test_validate_method_signature(self) -> None:
        """validate metódus szignatúrájának ellenőrzése."""
        sig = ConfigManagerInterface.validate.__annotations__
        assert "schema" in sig
        assert sig["schema"] == dict[str, Any]
        assert sig["return"] == tuple[bool, dict[str, str] | None]

    def test_cannot_instantiate_interface(self) -> None:
        """Az interfész nem példányosítható közvetlenül."""
        with pytest.raises(TypeError):
            ConfigManagerInterface()  # type: ignore

    def test_all_abstract_methods_present(self) -> None:
        """Összes absztrakt metódus jelen van."""
        abstract_methods = {"__init__", "get", "get_section", "set", "save", "load", "validate"}
        for method_name in abstract_methods:
            assert hasattr(ConfigManagerInterface, method_name)
            method = getattr(ConfigManagerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__")
            assert method.__isabstractmethod__ is True
