"""ConfigManagerFactoryInterface tesztelése.

Ez a modul tartalmazza a ConfigManagerFactoryInterface interfész
teszteseteit, amelyek ellenőrzik a factory mintázat megfelelő működését.
"""

from abc import ABC

import pytest

from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.interfaces.factory_interface import (
    ConfigManagerFactoryInterface,
)


class TestConfigManagerFactoryInterface:
    """ConfigManagerFactoryInterface interfész tesztesetei."""

    def test_register_manager_abstract(self) -> None:
        """Teszteli, hogy a register_manager metódus absztrakt."""
        with pytest.raises(TypeError):
            # Absztrakt osztályt nem lehet példányosítani
            ConfigManagerFactoryInterface()  # type: ignore

        # Ellenőrizzük, hogy az interfész tartalmazza az absztrakt metódust
        assert hasattr(ConfigManagerFactoryInterface, "register_manager")
        method = ConfigManagerFactoryInterface.register_manager
        assert hasattr(method, "__isabstractmethod__")

    def test_get_manager_abstract(self) -> None:
        """Teszteli, hogy a get_manager metódus absztrakt."""
        # Ellenőrizzük, hogy az interfész tartalmazza az absztrakt metódust
        assert hasattr(ConfigManagerFactoryInterface, "get_manager")
        method = ConfigManagerFactoryInterface.get_manager
        assert hasattr(method, "__isabstractmethod__")

    def test_create_manager_abstract(self) -> None:
        """Teszteli, hogy a create_manager metódus absztrakt."""
        # Ellenőrizzük, hogy az interfész tartalmazza az absztrakt metódust
        assert hasattr(ConfigManagerFactoryInterface, "create_manager")
        method = ConfigManagerFactoryInterface.create_manager
        assert hasattr(method, "__isabstractmethod__")

    def test_interface_inheritance(self) -> None:
        """Teszteli, hogy az interfész ABC-ből származik."""
        assert issubclass(ConfigManagerFactoryInterface, ABC)

    def test_interface_methods_callable(self) -> None:
        """Teszteli, hogy az interfész metódusai hívhatóak."""
        # register_manager ellenőrzése
        register_method = ConfigManagerFactoryInterface.register_manager
        assert callable(register_method)

        # get_manager ellenőrzése
        get_method = ConfigManagerFactoryInterface.get_manager
        assert callable(get_method)

        # create_manager ellenőrzése
        create_method = ConfigManagerFactoryInterface.create_manager
        assert callable(create_method)


class ConcreteFactory(ConfigManagerFactoryInterface):
    """Konkrét implementáció a teszteléshez."""

    _managers: dict[str, type[ConfigManagerInterface]] = {}
    _manager_types: dict[str, type[ConfigManagerInterface]] = {}

    @classmethod
    def register_manager(cls, extension: str, manager_class: type[ConfigManagerInterface]) -> None:
        """Manager regisztrálása.

        Args:
            extension: A fájl kiterjesztése
            manager_class: A manager osztály típusa

        Raises:
            ValueError: Ha az extension érvénytelen
            TypeError: Ha a manager_class nem típus
        """
        if not extension:
            raise ValueError("Az extension nem lehet üres string.")
        if not isinstance(manager_class, type):
            raise TypeError("A manager_class-nak típusnak kell lennie.")
        cls._managers[extension] = manager_class

    @classmethod
    def get_manager(cls, filename: str, manager_type: str | None = None) -> ConfigManagerInterface:
        """Manager létrehozása.

        Args:
            filename: A konfigurációs fájl neve
            manager_type: Opcionális manager típus

        Returns:
            ConfigManagerInterface: A létrehozott manager

        Raises:
            ValueError: Ha a fájlnév érvénytelen
            KeyError: Ha a manager típus nem létezik
        """
        if manager_type:
            if manager_type not in cls._manager_types:
                raise KeyError(f"Ismeretlen manager típus: {manager_type}")
            return cls._manager_types[manager_type]()

        # Fájlnév alapján kiterjesztés kinyerése
        if "." not in filename:
            raise ValueError(f"A fájlnévnek tartalmaznia kell kiterjesztést: {filename}")
        extension = "." + filename.split(".")[-1]
        if extension not in cls._managers:
            raise ValueError(f"Nem regisztrált kiterjesztés: {extension}")
        return cls._managers[extension]()

    @classmethod
    def create_manager(
        cls, manager_type: str, *args: object, **kwargs: object
    ) -> ConfigManagerInterface:
        """Manager létrehozása típus alapján.

        Args:
            manager_type: A manager típusa
            *args: Pozícionális argumentumok
            **kwargs: Kulcsszavas argumentumok

        Returns:
            ConfigManagerInterface: A létrehozott manager

        Raises:
            KeyError: Ha a manager típus nem létezik
        """
        if manager_type not in cls._manager_types:
            raise KeyError(f"Ismeretlen manager típus: {manager_type}")
        return cls._manager_types[manager_type](*args, **kwargs)

    @classmethod
    def clear_registrations(cls) -> None:
        """Regisztrációk törlése a teszteléshez."""
        cls._managers.clear()
        cls._manager_types.clear()


class MockConfigManager(ConfigManagerInterface):
    """Mock konfiguráció manager a teszteléshez."""

    def __init__(self, filename: str | None = None) -> None:
        """Inicializálás."""
        self.filename = filename

    def load(self, filename: str) -> None:
        """Fájl betöltése."""
        pass

    def get(self, *keys: str, default: object = None) -> object:
        """Érték lekérése."""
        return default

    def get_section(self, section: str) -> dict[str, object]:
        """Szekció lekérése."""
        return {}

    def set(self, *keys: str, value: object) -> None:
        """Érték beállítása."""
        pass

    def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése."""
        pass

    def validate(self, schema: dict[str, object]) -> tuple[bool, dict[str, str] | None]:
        """Séma validálás."""
        return True, None


class TestConcreteFactory:
    """Konkrét factory implementáció tesztelése."""

    def setup_method(self) -> None:
        """Teszt előtti beállítások."""
        ConcreteFactory.clear_registrations()

    def teardown_method(self) -> None:
        """Teszt utáni takarítás."""
        ConcreteFactory.clear_registrations()

    def test_register_manager_valid(self) -> None:
        """Teszteli a manager regisztrációt érvényes adatokkal."""
        ConcreteFactory.register_manager(".yml", MockConfigManager)

        assert ".yml" in ConcreteFactory._managers
        assert ConcreteFactory._managers[".yml"] is MockConfigManager

    def test_register_manager_invalid_extension(self) -> None:
        """Teszteli a manager regisztrációt érvénytelen kiterjesztéssel."""
        with pytest.raises(ValueError, match="nem lehet üres"):
            ConcreteFactory.register_manager("", MockConfigManager)

    def test_register_manager_invalid_class(self) -> None:
        """Teszteli a manager regisztrációt érvénytelen osztállyal."""
        with pytest.raises(TypeError, match="típusnak kell lennie"):
            ConcreteFactory.register_manager(".yml", "not_a_class")  # type: ignore

    def test_get_manager_by_extension(self) -> None:
        """Teszteli a manager létrehozását kiterjesztés alapján."""
        ConcreteFactory.register_manager(".yml", MockConfigManager)

        result = ConcreteFactory.get_manager("config.yml")

        assert isinstance(result, MockConfigManager)

    def test_get_manager_invalid_extension(self) -> None:
        """Teszteli a manager létrehozását érvénytelen kiterjesztéssel."""
        with pytest.raises(ValueError, match="A fájlnévnek tartalmaznia kell kiterjesztést"):
            ConcreteFactory.get_manager("config")

    def test_get_manager_unregistered_extension(self) -> None:
        """Teszteli a manager létrehozását nem regisztrált kiterjesztéssel."""
        with pytest.raises(ValueError, match="Nem regisztrált kiterjesztés"):
            ConcreteFactory.get_manager("config.xyz")

    def test_create_manager_with_args(self) -> None:
        """Teszteli a manager létrehozását argumentumokkal."""
        ConcreteFactory._manager_types["test"] = MockConfigManager

        result = ConcreteFactory.create_manager("test", "test_file.yml")

        assert isinstance(result, MockConfigManager)
        assert result.filename == "test_file.yml"

    def test_create_manager_invalid_type(self) -> None:
        """Teszteli a manager létrehozását érvénytelen típussal."""
        with pytest.raises(KeyError, match="Ismeretlen manager típus"):
            ConcreteFactory.create_manager("nonexistent")

    def test_clear_registrations(self) -> None:
        """Teszteli a regisztrációk törlését."""
        ConcreteFactory.register_manager(".yml", MockConfigManager)
        ConcreteFactory._manager_types["test"] = MockConfigManager

        assert ".yml" in ConcreteFactory._managers
        assert "test" in ConcreteFactory._manager_types

        ConcreteFactory.clear_registrations()

        assert ".yml" not in ConcreteFactory._managers
        assert "test" not in ConcreteFactory._manager_types
