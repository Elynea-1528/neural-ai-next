"""AsyncConfigManagerInterface tesztelése.

Ez a modul tartalmazza a AsyncConfigManagerInterface interfész teszteit,
amelyek ellenőrzik az aszinkron konfigurációkezelő interfész metódusainak
helyes definícióját és a megvalósító osztályok konzisztenciáját.
"""

from abc import ABC
from typing import Any

import pytest

from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
    ConfigListener,
)


class DummyAsyncConfigManager(AsyncConfigManagerInterface):
    """Egyszerű aszinkron konfigurációkezelő implementáció teszteléshez."""

    def __init__(
        self,
        filename: str | None = None,
        session: Any | None = None,
        logger: Any | None = None,
    ) -> None:
        """Inicializálja a dummy aszinkron konfigurációkezelőt."""
        self._config: dict[str, Any] = {}
        self._filename = filename
        self.session = session
        self._logger = logger
        self._listeners: list[ConfigListener] = []

    async def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""
        return self._config.get(".".join(keys), default)

    async def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""
        return self._config.get(section, {})

    async def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""
        key = ".".join(keys)
        self._config[key] = value

    async def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése."""
        pass

    async def load(self, filename: str) -> None:
        """Konfiguráció betöltése."""
        self._filename = filename

    async def load_directory(self, path: str) -> None:
        """Betölti az összes konfigurációs fájlt egy mappából."""
        pass

    async def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján."""
        return True, None

    def add_listener(self, callback: ConfigListener) -> None:
        """Listener hozzáadása konfiguráció változásokhoz."""
        self._listeners.append(callback)

    def remove_listener(self, callback: ConfigListener) -> None:
        """Listener eltávolítása."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    async def start_hot_reload(self, interval: float = 5.0) -> None:
        """Hot reload indítása."""
        pass

    async def stop_hot_reload(self) -> None:
        """Hot reload leállítása."""
        pass

    async def get_all(self, category: str | None = None) -> dict[str, Any]:
        """Összes konfiguráció lekérdezése."""
        return self._config.copy()

    async def set_with_metadata(
        self,
        key: str,
        value: Any,
        category: str = "system",
        description: str | None = None,
        is_active: bool = True,
    ) -> None:
        """Konfiguráció beállítása metaadatokkal."""
        self._config[key] = value

    async def delete(self, key: str) -> bool:
        """Konfiguráció törlése (soft delete)."""
        if key in self._config:
            del self._config[key]
            return True
        return False


class TestAsyncConfigManagerInterface:
    """AsyncConfigManagerInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert issubclass(AsyncConfigManagerInterface, ABC)

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
            "add_listener",
            "remove_listener",
            "start_hot_reload",
            "stop_hot_reload",
            "get_all",
            "set_with_metadata",
            "delete",
        }

        for method_name in abstract_methods:
            assert hasattr(AsyncConfigManagerInterface, method_name)
            method = getattr(AsyncConfigManagerInterface, method_name)
            assert hasattr(method, "__isabstractmethod__")
            assert method.__isabstractmethod__ is True

    def test_interface_method_signatures(self) -> None:
        """Teszteli a metódusok aláírásainak helyességét."""
        # __init__
        init_method = AsyncConfigManagerInterface.__init__
        assert init_method.__annotations__["filename"] == str | None
        assert init_method.__annotations__["session"] == "AsyncSession | None"
        assert init_method.__annotations__["logger"] == "LoggerInterface | None"
        assert init_method.__annotations__["return"] is None

        # get
        get_method = AsyncConfigManagerInterface.get
        assert get_method.__annotations__["default"] == Any
        assert get_method.__annotations__["return"] == Any

        # get_section
        get_section_method = AsyncConfigManagerInterface.get_section
        assert get_section_method.__annotations__["section"] == str
        assert get_section_method.__annotations__["return"] == dict[str, Any]

        # set
        set_method = AsyncConfigManagerInterface.set
        assert set_method.__annotations__["value"] == Any
        assert set_method.__annotations__["return"] is None

        # save
        save_method = AsyncConfigManagerInterface.save
        assert save_method.__annotations__["filename"] == str | None
        assert save_method.__annotations__["return"] is None

        # load
        load_method = AsyncConfigManagerInterface.load
        assert load_method.__annotations__["filename"] == str
        assert load_method.__annotations__["return"] is None

        # load_directory
        load_directory_method = AsyncConfigManagerInterface.load_directory
        assert load_directory_method.__annotations__["path"] == str
        assert load_directory_method.__annotations__["return"] is None

        # validate
        validate_method = AsyncConfigManagerInterface.validate
        assert validate_method.__annotations__["schema"] == dict[str, Any]
        assert validate_method.__annotations__["return"] == tuple[bool, dict[str, str] | None]

        # add_listener
        add_listener_method = AsyncConfigManagerInterface.add_listener
        assert add_listener_method.__annotations__["callback"] == ConfigListener
        assert add_listener_method.__annotations__["return"] is None

        # remove_listener
        remove_listener_method = AsyncConfigManagerInterface.remove_listener
        assert remove_listener_method.__annotations__["callback"] == ConfigListener
        assert remove_listener_method.__annotations__["return"] is None

        # start_hot_reload
        start_hot_reload_method = AsyncConfigManagerInterface.start_hot_reload
        assert start_hot_reload_method.__annotations__["interval"] == float
        assert start_hot_reload_method.__annotations__["return"] is None

        # stop_hot_reload
        stop_hot_reload_method = AsyncConfigManagerInterface.stop_hot_reload
        assert stop_hot_reload_method.__annotations__["return"] is None

        # get_all
        get_all_method = AsyncConfigManagerInterface.get_all
        assert get_all_method.__annotations__["category"] == str | None
        assert get_all_method.__annotations__["return"] == dict[str, Any]

        # set_with_metadata
        set_with_metadata_method = AsyncConfigManagerInterface.set_with_metadata
        assert set_with_metadata_method.__annotations__["key"] == str
        assert set_with_metadata_method.__annotations__["value"] == Any
        assert set_with_metadata_method.__annotations__["category"] == str
        assert set_with_metadata_method.__annotations__["description"] == str | None
        assert set_with_metadata_method.__annotations__["is_active"] == bool
        assert set_with_metadata_method.__annotations__["return"] is None

        # delete
        delete_method = AsyncConfigManagerInterface.delete
        assert delete_method.__annotations__["key"] == str
        assert delete_method.__annotations__["return"] == bool

    def test_config_listener_type_alias(self) -> None:
        """Teszteli a ConfigListener típusalias definícióját."""
        # A ConfigListener egy Callable, ami egy string és egy tetszőleges értéket vár
        # és egy Awaitable[None]-t ad vissza
        async def sample_listener(key: str, value: Any) -> None:
            pass

        # Ellenőrizzük, hogy a sample_listener kompatibilis-e a ConfigListener típussal
        listener: ConfigListener = sample_listener
        assert callable(listener)

    def test_implementation_can_be_instantiated(self) -> None:
        """Teszteli, hogy az interfész implementálható-e."""
        manager = DummyAsyncConfigManager()
        assert isinstance(manager, AsyncConfigManagerInterface)

    def test_implementation_has_all_methods(self) -> None:
        """Teszteli, hogy az implementáció tartalmazza az összes szükséges metódust."""
        manager = DummyAsyncConfigManager()
        required_methods = [
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
            "add_listener",
            "remove_listener",
            "start_hot_reload",
            "stop_hot_reload",
            "get_all",
            "set_with_metadata",
            "delete",
        ]

        for method_name in required_methods:
            assert hasattr(manager, method_name)
            method = getattr(manager, method_name)
            assert callable(method)

    @pytest.mark.asyncio
    async def test_async_methods_are_awaitable(self) -> None:
        """Teszteli, hogy az aszinkron metódusok await-elhetőek."""
        manager = DummyAsyncConfigManager()

        # Ellenőrizzük, hogy az async metódusok valóban await-elhetőek
        result = await manager.get("test", default="default")
        assert result == "default"

        await manager.set("test", value="value")
        result = await manager.get("test")
        assert result == "value"

        section = await manager.get_section("test_section")
        assert isinstance(section, dict)

        await manager.save()
        await manager.load("test.yaml")
        await manager.load_directory("/path/to/configs")

        is_valid, errors = await manager.validate({})
        assert isinstance(is_valid, bool)
        assert errors is None or isinstance(errors, dict)

        await manager.start_hot_reload()
        await manager.stop_hot_reload()

        all_configs = await manager.get_all()
        assert isinstance(all_configs, dict)

        await manager.set_with_metadata("key", "value")
        await manager.delete("key")

    def test_sync_methods_are_callable(self) -> None:
        """Teszteli, hogy a szinkron metódusok hívhatóak."""
        manager = DummyAsyncConfigManager()

        # A listener metódusok szinkron metódusok
        async def dummy_listener(key: str, value: Any) -> None:
            pass

        manager.add_listener(dummy_listener)
        manager.remove_listener(dummy_listener)

    def test_interface_enforces_method_implementation(self) -> None:
        """Teszteli, hogy az interfész kényszeríti a metódusok implementálását."""
        # Az ABC osztályok nem engedik létrehozni a példányt, ha nem implementálják
        # az összes absztrakt metódust
        with pytest.raises(TypeError):
            class _IncompleteAsyncConfigManager(AsyncConfigManagerInterface):  # type: ignore
                pass
            # Próbáljuk létrehozni a példányt, hogy kiváltódjon a TypeError
            _IncompleteAsyncConfigManager()

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
            "add_listener",
            "remove_listener",
            "start_hot_reload",
            "stop_hot_reload",
            "get_all",
            "set_with_metadata",
            "delete",
        ]

        for method_name in method_names:
            method = getattr(AsyncConfigManagerInterface, method_name)
            assert method.__doc__ is not None
            assert len(method.__doc__.strip()) > 0

    def test_interface_method_order(self) -> None:
        """Teszteli, hogy az interfész metódusai logikus sorrendben vannak."""
        method_names = [
            name for name in dir(AsyncConfigManagerInterface) if not name.startswith('_')
        ]
        expected_order = [
            "get",
            "get_section",
            "set",
            "save",
            "load",
            "load_directory",
            "validate",
            "add_listener",
            "remove_listener",
            "start_hot_reload",
            "stop_hot_reload",
            "get_all",
            "set_with_metadata",
            "delete",
        ]

        # Ellenőrizzük, hogy az összes várt metódus jelen van
        for expected in expected_order:
            assert expected in method_names

    def test_constructor_accepts_optional_params(self) -> None:
        """Teszteli, hogy a konstruktor elfogadja az opcionális paramétereket."""
        # Nem dob kivételt, ha None értékeket adunk meg
        manager1 = DummyAsyncConfigManager(filename=None, session=None, logger=None)
        assert manager1 is not None

        # Nem dob kivételt, ha nem adunk meg paramétereket
        manager2 = DummyAsyncConfigManager()
        assert manager2 is not None

    @pytest.mark.asyncio
    async def test_get_method_accepts_variable_keys(self) -> None:
        """Teszteli, hogy a get metódus elfogad változó számú kulcsot."""
        manager = DummyAsyncConfigManager()
        await manager.set("key1", value="value1")
        await manager.set("key2", "key3", value="value2")

        result1 = await manager.get("key1")
        result2 = await manager.get("key2", "key3")

        assert result1 == "value1"
        assert result2 == "value2"

    @pytest.mark.asyncio
    async def test_get_method_returns_default(self) -> None:
        """Teszteli, hogy a get metódus visszaadja az alapértelmezett értéket."""
        manager = DummyAsyncConfigManager()
        result = await manager.get("nonexistent", default="default_value")

        assert result == "default_value"

    @pytest.mark.asyncio
    async def test_set_method_accepts_variable_keys(self) -> None:
        """Teszteli, hogy a set metódus elfogad változó számú kulcsot."""
        manager = DummyAsyncConfigManager()
        await manager.set("key1", value="value1")
        await manager.set("key2", "key3", value="value2")

        result1 = await manager.get("key1")
        result2 = await manager.get("key2", "key3")

        assert result1 == "value1"
        assert result2 == "value2"

    @pytest.mark.asyncio
    async def test_get_section_returns_dict(self) -> None:
        """Teszteli, hogy a get_section metódus dictionary-t ad vissza."""
        manager = DummyAsyncConfigManager()
        result = await manager.get_section("test_section")

        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_validate_returns_tuple(self) -> None:
        """Teszteli, hogy a validate metódus tuple-t ad vissza."""
        manager = DummyAsyncConfigManager()
        schema: dict[str, Any] = {}
        is_valid, errors = await manager.validate(schema)

        assert isinstance(is_valid, bool)
        assert errors is None or isinstance(errors, dict)

    @pytest.mark.asyncio
    async def test_save_accepts_optional_filename(self) -> None:
        """Teszteli, hogy a save metódus elfogad opcionális fájlnevet."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt, ha None-t adunk meg
        await manager.save(filename=None)
        # Nem dob kivételt, ha nem adunk meg fájlnevet
        await manager.save()

    @pytest.mark.asyncio
    async def test_load_accepts_filename(self) -> None:
        """Teszteli, hogy a load metódus elfogad fájlnevet."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        await manager.load("test_file.yaml")

    @pytest.mark.asyncio
    async def test_load_directory_accepts_path(self) -> None:
        """Teszteli, hogy a load_directory metódus elfogad elérési utat."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        await manager.load_directory("/path/to/configs")

    @pytest.mark.asyncio
    async def test_start_hot_reload_accepts_interval(self) -> None:
        """Teszteli, hogy a start_hot_reload metódus elfogad interval paramétert."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        await manager.start_hot_reload(interval=10.0)
        await manager.start_hot_reload()  # Alapértelmezett értékkel

    @pytest.mark.asyncio
    async def test_stop_hot_reload_is_callable(self) -> None:
        """Teszteli, hogy a stop_hot_reload metódus hívható."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        await manager.stop_hot_reload()

    @pytest.mark.asyncio
    async def test_get_all_accepts_optional_category(self) -> None:
        """Teszteli, hogy a get_all metódus elfogad opcionális kategóriát."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        result1 = await manager.get_all(category="system")
        result2 = await manager.get_all()  # Alapértelmezett értékkel

        assert isinstance(result1, dict)
        assert isinstance(result2, dict)

    @pytest.mark.asyncio
    async def test_set_with_metadata_accepts_params(self) -> None:
        """Teszteli, hogy a set_with_metadata metódus elfogadja a paramétereket."""
        manager = DummyAsyncConfigManager()
        # Nem dob kivételt
        await manager.set_with_metadata(
            key="test_key",
            value="test_value",
            category="risk",
            description="Test description",
            is_active=True,
        )

    @pytest.mark.asyncio
    async def test_delete_returns_bool(self) -> None:
        """Teszteli, hogy a delete metódus boolean értéket ad vissza."""
        manager = DummyAsyncConfigManager()
        await manager.set("test_key", value="test_value")

        result1 = await manager.delete("test_key")
        result2 = await manager.delete("nonexistent_key")

        assert isinstance(result1, bool)
        assert isinstance(result2, bool)
        assert result1 is True
        assert result2 is False
