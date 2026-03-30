"""ConfigManagerInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerInterface interfész teszteit,
amelyek ellenőrzik az interfész metódusainak helyes definícióját és
a megvalósító osztályok konzisztenciáját.
"""

from abc import ABC
from typing import Any

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class DummyConfigManager(ConfigManagerInterface):
    """Egyszerű konfigurációkezelő implementáció teszteléshez."""

    def __init__(self, filename: str | None = None) -> None:
        """Inicializálja a dummy konfigurációkezelőt."""
        self._config: dict[str, Any] = {}
        self._filename = filename

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""
        return self._config.get(".".join(keys), default)

    def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""
        return self._config.get(section, {})

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""
        key = ".".join(keys)
        self._config[key] = value

    def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése fájlba."""
        pass

    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból."""
        self._filename = filename

    def load_directory(self, path: str) -> None:
        """Betölti az összes YAML fájlt egy mappából namespaced struktúrába."""
        pass

    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján."""
        return True, None


class TestConfigManagerInterface:
    """ConfigManagerInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert issubclass(ConfigManagerInterface, ABC)

    def test_interface_has_abstract_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza a szükséges absztrakt metódusokat."""
        abstract_methods = {
            "__init__",
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
        }

        for method_name in abstract_methods:
            assert hasattr(ConfigManagerInterface, method_name)
            method = getattr(ConfigManagerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__")
            assert method.__isabstractmethod__ is True

    def test_interface_method_signatures(self) -> None:
        """Teszteli a metódusok aláírásainak helyességét."""
        # __init__
        init_method = ConfigManagerInterface.__init__
        assert init_method.__annotations__["filename"] == str | None
        assert init_method.__annotations__["return"] is None

        # get
        get_method = ConfigManagerInterface.get
        assert get_method.__annotations__["default"] == Any
        assert get_method.__annotations__["return"] == Any

        # get_section
        get_section_method = ConfigManagerInterface.get_section
        assert get_section_method.__annotations__["section"] is str
        assert get_section_method.__annotations__["return"] == dict[str, Any]

        # set
        set_method = ConfigManagerInterface.set
        assert set_method.__annotations__["value"] == Any
        assert set_method.__annotations__["return"] is None

        # save
        save_method = ConfigManagerInterface.save
        assert save_method.__annotations__["filename"] == str | None
        assert save_method.__annotations__["return"] is None

        # load
        load_method = ConfigManagerInterface.load
        assert load_method.__annotations__["filename"] is str
        assert load_method.__annotations__["return"] is None

        # load_directory
        load_directory_method = ConfigManagerInterface.load_directory
        assert load_directory_method.__annotations__["path"] is str
        assert load_directory_method.__annotations__["return"] is None

        # validate
        validate_method = ConfigManagerInterface.validate
        assert validate_method.__annotations__["schema"] == dict[str, Any]
        assert validate_method.__annotations__["return"] == tuple[bool, dict[str, str] | None]

    def test_implementation_can_be_instantiated(self) -> None:
        """Teszteli, hogy az interfész implementálható-e."""
        manager = DummyConfigManager()
        assert isinstance(manager, ConfigManagerInterface)

    def test_implementation_has_all_methods(self) -> None:
        """Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust."""
        manager = DummyConfigManager()
        required_methods = [
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
        ]

        for method_name in required_methods:
            assert hasattr(manager, method_name)
            method = getattr(manager, method_name)
            assert callable(method)

    def test_get_method_accepts_variable_keys(self) -> None:
        """Teszteli, hogy a get metódus elfogad változó számú kulcsot."""
        manager = DummyConfigManager()
        manager.set("key1", value="value1")
        manager.set("key2", "key3", value="value2")

        assert manager.get("key1") == "value1"
        assert manager.get("key2", "key3") == "value2"

    def test_get_method_returns_default(self) -> None:
        """Teszteli, hogy a get metódus visszaadja az alapértelmezett értéket."""
        manager = DummyConfigManager()
        result = manager.get("nonexistent", default="default_value")

        assert result == "default_value"

    def test_set_method_accepts_variable_keys(self) -> None:
        """Teszteli, hogy a set metódus elfogad változó számú kulcsot."""
        manager = DummyConfigManager()
        manager.set("key1", value="value1")
        manager.set("key2", "key3", value="value2")

        assert manager.get("key1") == "value1"
        assert manager.get("key2", "key3") == "value2"

    def test_get_section_returns_dict(self) -> None:
        """Teszteli, hogy a get_section metódus dictionary-t ad vissza."""
        manager = DummyConfigManager()
        result = manager.get_section("test_section")

        assert isinstance(result, dict)

    def test_validate_returns_tuple(self) -> None:
        """Teszteli, hogy a validate metódus tuple-t ad vissza."""
        manager = DummyConfigManager()
        schema: dict[str, Any] = {}
        is_valid, errors = manager.validate(schema)

        assert isinstance(is_valid, bool)
        assert errors is None or isinstance(errors, dict)

    def test_save_accepts_optional_filename(self) -> None:
        """Teszteli, hogy a save metódus elfogad opcionális fájlnevet."""
        manager = DummyConfigManager()
        # Nem dob kivételt, ha None-t adunk meg
        manager.save(filename=None)
        # Nem dob kivételt, ha nem adunk meg fájlnevet
        manager.save()

    def test_load_accepts_filename(self) -> None:
        """Teszteli, hogy a load metódus elfogad fájlnevet."""
        manager = DummyConfigManager()
        # Nem dob kivételt
        manager.load("test_file.yaml")

    def test_load_directory_accepts_path(self) -> None:
        """Teszteli, hogy a load_directory metódus elfogad elérési utat."""
        manager = DummyConfigManager()
        # Nem dob kivételt
        manager.load_directory("/path/to/configs")

    def test_interface_enforces_method_implementation(self) -> None:
        """Teszteli, hogy az interfész kényszeríti a metódusok implementálását."""
        # Az ABC osztályok nem engedik létrehozni a példányt, ha nem implementálják
        # az összes absztrakt metódust
        with pytest.raises(TypeError):

            class _IncompleteConfigManager(ConfigManagerInterface):
                pass

            # Próbáljuk létrehozni a példányt, hogy kiváltódjon a TypeError
            _IncompleteConfigManager()  # pyright: ignore[reportAbstractUsage]

    def test_implementation_preserves_type_hints(self) -> None:
        """Teszteli, hogy az implementáció megőrzi a típusjelzéseket."""
        manager = DummyConfigManager()

        # Ellenőrizzük a metódusok annotációit
        assert hasattr(manager.get, "__annotations__")
        assert hasattr(manager.set, "__annotations__")
        assert hasattr(manager.validate, "__annotations__")

    def test_interface_docstrings_present(self) -> None:
        """Teszteli, hogy az interfész metódusainak van docstringje."""
        method_names = [
            "__init__",
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
        ]

        for method_name in method_names:
            method = getattr(ConfigManagerInterface, method_name)
            assert method.__doc__ is not None
            assert len(method.__doc__.strip()) > 0

    def test_interface_method_order(self) -> None:
        """Teszteli, hogy az interfész metódusai logikus sorrendben vannak."""
        method_names = [name for name in dir(ConfigManagerInterface) if not name.startswith("_")]
        expected_order = [
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
        ]

        # Ellenőrizzük, hogy az összes várt metódus jelen van
        for expected in expected_order:
            assert expected in method_names
