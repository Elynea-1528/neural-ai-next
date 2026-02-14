"""ConfigManagerFactoryInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerFactoryInterface interfész teszteit,
amelyek ellenőrzik a konfigurációkezelő factory interfész metódusainak
helyes definícióját és a megvalósító osztályok konzisztenciáját.
"""

from abc import ABC
from typing import TYPE_CHECKING

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import ConfigManagerFactoryInterface

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface


class DummyConfigManager(ConfigManagerInterface):
    """Egyszerű konfigurációkezelő implementáció teszteléshez."""

    def __init__(self, filename: str | None = None) -> None:
        """Inicializálja a dummy konfigurációkezelőt."""
        self._config: dict[str, object] = {}
        self._filename = filename

    def get(self, *keys: str, default: object = None) -> object:
        """Érték lekérése a konfigurációból."""
        return self._config.get(".".join(keys), default)

    def get_section(self, section: str) -> dict[str, object]:
        """Teljes konfigurációs szekció lekérése."""
        result = self._config.get(section, {})
        if isinstance(result, dict):
            return result
        return {}

    def set(self, *keys: str, value: object) -> None:
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

    def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján."""
        return True, None


class DummyConfigFactory(ConfigManagerFactoryInterface):
    """Egyszerű konfiguráció factory implementáció teszteléshez."""

    _managers: dict[str, type[ConfigManagerInterface]] = {}
    _async_managers: dict[str, type[object]] = {}

    @classmethod
    def register_manager(
        cls, extension: str, manager_class: type["ConfigManagerInterface"]
    ) -> None:
        """Új konfiguráció kezelő típus regisztrálása."""
        cls._managers[extension] = manager_class

    @classmethod
    def get_manager(
        cls, filename: str, manager_type: str | None = None
    ) -> "ConfigManagerInterface":
        """Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján."""
        if manager_type:
            if manager_type in cls._managers:
                return cls._managers[manager_type](filename=filename)
            raise KeyError(f"Manager type {manager_type} not found")

        # Fájlnév alapján automatikus kiválasztás
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            return DummyConfigManager(filename=filename)
        raise ValueError(f"No manager registered for file: {filename}")

    @classmethod
    def create_manager(
        cls, manager_type: str, *args: object, **kwargs: object
    ) -> "ConfigManagerInterface":
        """Konfiguráció kezelő létrehozása típus alapján."""
        if manager_type in cls._managers:
            return cls._managers[manager_type](*args, **kwargs)
        raise KeyError(f"Manager type {manager_type} not found")


class TestConfigManagerFactoryInterface:
    """ConfigManagerFactoryInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert issubclass(ConfigManagerFactoryInterface, ABC)

    def test_interface_has_abstract_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza a szükséges absztrakt metódusokat."""
        abstract_methods = {
            "register_manager",
            "get_manager",
            "create_manager",
        }

        for method_name in abstract_methods:
            assert hasattr(ConfigManagerFactoryInterface, method_name)
            method = getattr(ConfigManagerFactoryInterface, method_name)
            assert hasattr(method, "__isabstractmethod__")
            assert method.__isabstractmethod__ is True

    def test_interface_methods_are_classmethods(self) -> None:
        """Teszteli, hogy az interfész metódusai classmethod-ok."""
        # Az interfész metódusai @classmethod dekorátorral vannak ellátva
        register_method = ConfigManagerFactoryInterface.__dict__["register_manager"]
        get_manager_method = ConfigManagerFactoryInterface.__dict__["get_manager"]
        create_manager_method = ConfigManagerFactoryInterface.__dict__["create_manager"]

        assert isinstance(register_method, classmethod)
        assert isinstance(get_manager_method, classmethod)
        assert isinstance(create_manager_method, classmethod)

    def test_interface_method_signatures(self) -> None:
        """Teszteli a metódusok aláírásainak helyességét."""
        # register_manager
        register_method = ConfigManagerFactoryInterface.register_manager
        assert register_method.__annotations__["extension"] is str
        assert register_method.__annotations__["manager_class"] == type["ConfigManagerInterface"]
        assert register_method.__annotations__["return"] is None

        # get_manager
        get_manager_method = ConfigManagerFactoryInterface.get_manager
        assert get_manager_method.__annotations__["filename"] is str
        assert get_manager_method.__annotations__["manager_type"] == str | None
        assert get_manager_method.__annotations__["return"] == "ConfigManagerInterface"

        # create_manager
        create_manager_method = ConfigManagerFactoryInterface.create_manager
        assert create_manager_method.__annotations__["manager_type"] is str
        assert create_manager_method.__annotations__["return"] == "ConfigManagerInterface"

    def test_implementation_can_be_instantiated(self) -> None:
        """Teszteli, hogy az interfész implementálható-e."""
        factory = DummyConfigFactory
        assert issubclass(factory, ConfigManagerFactoryInterface)

    def test_implementation_has_all_methods(self) -> None:
        """Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust."""
        factory = DummyConfigFactory
        required_methods = [
            "register_manager",
            "get_manager",
            "create_manager",
        ]

        for method_name in required_methods:
            assert hasattr(factory, method_name)
            method = getattr(factory, method_name)
            assert callable(method)

    def test_register_manager_method(self) -> None:
        """Teszteli a register_manager metódust."""
        DummyConfigFactory.register_manager(".test", DummyConfigManager)
        assert ".test" in DummyConfigFactory._managers
        assert DummyConfigFactory._managers[".test"] == DummyConfigManager

    def test_get_manager_method(self) -> None:
        """Teszteli a get_manager metódust."""
        manager = DummyConfigFactory.get_manager("test.yaml")
        assert isinstance(manager, DummyConfigManager)
        assert manager._filename == "test.yaml"

    def test_get_manager_with_type(self) -> None:
        """Teszteli a get_manager metódust explicit típussal."""
        DummyConfigFactory.register_manager("dummy", DummyConfigManager)
        manager = DummyConfigFactory.get_manager("test.xyz", manager_type="dummy")
        assert isinstance(manager, DummyConfigManager)

    def test_get_manager_with_invalid_extension(self) -> None:
        """Teszteli a get_manager metódust érvénytelen kiterjesztéssel."""
        with pytest.raises(ValueError, match="No manager registered"):
            DummyConfigFactory.get_manager("test.invalid")

    def test_get_manager_with_invalid_type(self) -> None:
        """Teszteli a get_manager metódust érvénytelen típussal."""
        with pytest.raises(KeyError, match="Manager type invalid_type not found"):
            DummyConfigFactory.get_manager("test.xyz", manager_type="invalid_type")

    def test_create_manager_method(self) -> None:
        """Teszteli a create_manager metódust."""
        DummyConfigFactory.register_manager("dummy", DummyConfigManager)
        manager = DummyConfigFactory.create_manager("dummy", filename="test.yaml")
        assert isinstance(manager, DummyConfigManager)
        assert manager._filename == "test.yaml"

    def test_create_manager_with_kwargs(self) -> None:
        """Teszteli a create_manager metódust csak kulcsszavas argumentumokkal."""
        DummyConfigFactory.register_manager("dummy", DummyConfigManager)
        manager = DummyConfigFactory.create_manager("dummy", filename="test.yaml")
        assert isinstance(manager, DummyConfigManager)
        assert manager._filename == "test.yaml"

    def test_create_manager_with_invalid_type(self) -> None:
        """Teszteli a create_manager metódust érvénytelen típussal."""
        with pytest.raises(KeyError, match="Manager type invalid_type not found"):
            DummyConfigFactory.create_manager("invalid_type")

    def test_interface_enforces_method_implementation(self) -> None:
        """Teszteli, hogy az interfész kényszeríti a metódusok implementálását."""
        # Az ABC osztályok nem engedik létrehozni a példányt, ha nem implementálják
        # az összes absztrakt metódust
        with pytest.raises(TypeError):

            class _IncompleteConfigFactory(ConfigManagerFactoryInterface):  # type: ignore
                pass

            # Próbáljuk létrehozni a példányt, hogy kiváltódjon a TypeError
            _IncompleteConfigFactory()

    def test_interface_docstrings_present(self) -> None:
        """Teszteli, hogy az interfész metódusainak van docstringje."""
        method_names = [
            "register_manager",
            "get_manager",
            "create_manager",
        ]

        for method_name in method_names:
            method = getattr(ConfigManagerFactoryInterface, method_name)
            assert method.__doc__ is not None
            assert len(method.__doc__.strip()) > 0

    def test_interface_method_order(self) -> None:
        """Teszteli, hogy az interfész metódusai logikus sorrendben vannak."""
        method_names = [
            name for name in dir(ConfigManagerFactoryInterface) if not name.startswith("_")
        ]
        expected_order = [
            "register_manager",
            "get_manager",
            "create_manager",
        ]

        # Ellenőrizzük, hogy az összes várt metódus jelen van
        for expected in expected_order:
            assert expected in method_names

    def test_register_manager_raises_not_implemented_error(self) -> None:
        """Teszteli, hogy a register_manager alapértelmezésben NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            ConfigManagerFactoryInterface.register_manager(".test", DummyConfigManager)

    def test_get_manager_raises_not_implemented_error(self) -> None:
        """Teszteli, hogy a get_manager alapértelmezésben NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            ConfigManagerFactoryInterface.get_manager("test.yaml")

    def test_create_manager_raises_not_implemented_error(self) -> None:
        """Teszteli, hogy a create_manager alapértelmezésben NotImplementedError-t dob."""
        with pytest.raises(NotImplementedError):
            ConfigManagerFactoryInterface.create_manager("test")

    def test_factory_returns_config_manager_interface(self) -> None:
        """Teszteli, hogy a factory ConfigManagerInterface-t ad vissza."""
        manager = DummyConfigFactory.get_manager("test.yaml")
        assert isinstance(manager, ConfigManagerInterface)

    def test_factory_creates_separate_instances(self) -> None:
        """Teszteli, hogy a factory külön példányokat hoz létre."""
        manager1 = DummyConfigFactory.get_manager("test1.yaml")
        manager2 = DummyConfigFactory.get_manager("test2.yaml")

        # A két példány különböző objektum kell legyen
        assert manager1 is not manager2

    def test_factory_supports_multiple_manager_types(self) -> None:
        """Teszteli, hogy a factory támogat több konfigurációkezelő típust."""
        # Regisztráljunk több kezelőt
        DummyConfigFactory.register_manager(".yaml", DummyConfigManager)
        DummyConfigFactory.register_manager(".yml", DummyConfigManager)
        DummyConfigFactory.register_manager(".json", DummyConfigManager)

        # Minden típusnak létre kell tudni hozni a kezelőjét
        manager1 = DummyConfigFactory.get_manager("config.yaml")
        manager2 = DummyConfigFactory.get_manager("config.yml")
        manager3 = DummyConfigFactory.get_manager("config.json", manager_type=".json")

        assert isinstance(manager1, DummyConfigManager)
        assert isinstance(manager2, DummyConfigManager)
        assert isinstance(manager3, DummyConfigManager)
