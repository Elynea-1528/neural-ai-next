"""ConfigManagerFactory tesztek.

Ez a modul tartalmazza a ConfigManagerFactory osztály tesztjeit, amelyek ellenőrzik
a szinkron és aszinkron konfiguráció kezelők létrehozását, regisztrálását és
életciklusuk kezelését.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces.async_config_interface import (
    AsyncConfigManagerInterface,
)
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces import LoggerInterface


class DummyConfigManager(ConfigManagerInterface):
    """Dummy konfiguráció kezelő teszteléshez."""

    def __init__(self, filename: str | None = None) -> None:
        self._filename = filename
        self.data: dict[str, Any] = {}

    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése."""
        key = ".".join(keys)
        return self.data.get(key, default)

    def get_section(self, section: str) -> dict[str, Any]:
        """Szekció lekérése."""
        return {k: v for k, v in self.data.items() if k.startswith(section + ".")}

    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása."""
        key = ".".join(keys)
        self.data[key] = value

    def save(self, filename: str | None = None) -> None:
        """Mentés."""
        pass

    def load(self, filename: str) -> None:
        """Betöltés."""
        self._filename = filename

    def load_directory(self, path: str) -> None:
        """Mappa betöltése."""
        pass

    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Validálás."""
        return True, None


class DummyAsyncConfigManager(AsyncConfigManagerInterface):
    """Dummy aszinkron konfiguráció kezelő teszteléshez."""

    def __init__(
        self,
        filename: str | None = None,
        session: AsyncSession | None = None,
        logger: "LoggerInterface | None" = None,
    ) -> None:
        self._filename = filename
        self.session = session
        self._logger = logger
        self.data: dict[str, Any] = {}

    async def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése."""
        key = ".".join(keys)
        return self.data.get(key, default)

    async def get_section(self, section: str) -> dict[str, Any]:
        """Szekció lekérése."""
        return {k: v for k, v in self.data.items() if k.startswith(section + ".")}

    async def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása."""
        key = ".".join(keys)
        self.data[key] = value

    async def save(self, filename: str | None = None) -> None:
        """Mentés."""
        pass

    async def load(self, filename: str) -> None:
        """Betöltés."""
        self._filename = filename

    async def load_directory(self, path: str) -> None:
        """Mappa betöltése."""
        pass

    async def validate(
        self, schema: dict[str, Any]
    ) -> tuple[bool, dict[str, str] | None]:
        """Validálás."""
        return True, None

    def add_listener(self, callback: Any) -> None:
        """Listener hozzáadása."""
        pass

    def remove_listener(self, callback: Any) -> None:
        """Listener eltávolítása."""
        pass

    async def start_hot_reload(self, interval: float = 5.0) -> None:
        """Hot reload indítása."""
        pass

    async def stop_hot_reload(self) -> None:
        """Hot reload leállítása."""
        pass

    async def get_all(self, category: str | None = None) -> dict[str, Any]:
        """Összes konfiguráció lekérdezése."""
        return self.data

    async def set_with_metadata(
        self,
        key: str,
        value: Any,
        category: str = "system",
        description: str | None = None,
        is_active: bool = True,
    ) -> None:
        """Konfiguráció beállítása metaadatokkal."""
        self.data[key] = value

    async def delete(self, key: str) -> bool:
        """Konfiguráció törlése."""
        if key in self.data:
            del self.data[key]
            return True
        return False


class TestRegisterManager:
    """Teszt osztály a register_manager metódushoz."""

    def test_register_manager_success(self) -> None:
        """Sikeres konfiguráció kezelő regisztráció."""
        # Arrange
        extension = ".dummy"
        manager_class = DummyConfigManager

        # Act
        ConfigManagerFactory.register_manager(extension, manager_class)

        # Assert
        assert extension in ConfigManagerFactory.get_supported_extensions()

        # Cleanup
        ConfigManagerFactory._manager_types.pop(extension, None)

    def test_register_manager_without_dot(self) -> None:
        """Konfiguráció kezelő regisztráció pont nélküli kiterjesztéssel."""
        # Arrange
        extension = "dummy"
        manager_class = DummyConfigManager

        # Act
        ConfigManagerFactory.register_manager(extension, manager_class)

        # Assert
        assert ".dummy" in ConfigManagerFactory.get_supported_extensions()

        # Cleanup
        ConfigManagerFactory._manager_types.pop(".dummy", None)

    def test_register_manager_empty_extension(self) -> None:
        """Hibaüzenet üres kiterjesztés esetén."""
        # Arrange
        extension = ""
        manager_class = DummyConfigManager

        # Act & Assert
        with pytest.raises(ValueError, match="Az extension nem lehet üres"):
            ConfigManagerFactory.register_manager(extension, manager_class)

    def test_register_manager_invalid_class(self) -> None:
        """Hibaüzenet érvénytelen osztály esetén."""
        # Arrange
        extension = ".invalid"
        manager_class = str  # Nem ConfigManagerInterface

        # Act & Assert
        with pytest.raises(
            TypeError,
            match="A manager_class-nak implementálnia kell a ConfigManagerInterface-t",
        ):
            ConfigManagerFactory.register_manager(extension, manager_class)


class TestRegisterAsyncManager:
    """Teszt osztály a register_async_manager metódushoz."""

    def test_register_async_manager_success(self) -> None:
        """Sikeres aszinkron konfiguráció kezelő regisztráció."""
        # Arrange
        manager_type = "dummy_async"
        manager_class = DummyAsyncConfigManager

        # Act
        ConfigManagerFactory.register_async_manager(manager_type, manager_class)

        # Assert
        assert manager_type in ConfigManagerFactory.get_supported_async_types()

        # Cleanup
        ConfigManagerFactory._async_manager_types.pop(manager_type, None)

    def test_register_async_manager_empty_type(self) -> None:
        """Hibaüzenet üres típus esetén."""
        # Arrange
        manager_type = ""
        manager_class = DummyAsyncConfigManager

        # Act & Assert
        with pytest.raises(ValueError, match="A manager_type nem lehet üres"):
            ConfigManagerFactory.register_async_manager(manager_type, manager_class)

    def test_register_async_manager_invalid_class(self) -> None:
        """Hibaüzenet érvénytelen osztály esetén."""
        # Arrange
        manager_type = "invalid_async"
        manager_class = str  # Nem AsyncConfigManagerInterface

        # Act & Assert
        with pytest.raises(
            TypeError,
            match="A manager_class-nak implementálnia kell az AsyncConfigManagerInterface-t",
        ):
            ConfigManagerFactory.register_async_manager(manager_type, manager_class)


class TestCreateManager:
    """Teszt osztály a create_manager metódushoz."""

    def test_create_manager_success(self) -> None:
        """Sikeres konfiguráció kezelő létrehozása."""
        # Act
        manager = ConfigManagerFactory.create_manager(
            ".yaml", filename=None
        )

        # Assert
        assert isinstance(manager, ConfigManagerInterface)

    def test_create_manager_without_dot(self) -> None:
        """Konfiguráció kezelő létrehozása pont nélküli típussal."""
        # Act
        manager = ConfigManagerFactory.create_manager(
            "yaml", filename=None
        )

        # Assert
        assert isinstance(manager, ConfigManagerInterface)

    def test_create_manager_with_args(self) -> None:
        """Konfiguráció kezelő létrehozása pozícionális argumentumokkal."""
        # Act
        manager = ConfigManagerFactory.create_manager(
            ".yaml", None
        )

        # Assert
        assert isinstance(manager, ConfigManagerInterface)

    def test_create_manager_invalid_type(self) -> None:
        """Hibaüzenet érvénytelen típus esetén."""
        # Act & Assert
        with pytest.raises(
            ConfigLoadError, match="Ismeretlen konfig kezelő típus"
        ):
            ConfigManagerFactory.create_manager(".invalid")


class TestGetAsyncManager:
    """Teszt osztály a get_async_manager metódushoz."""

    @pytest.mark.asyncio
    async def test_get_async_manager_success(self) -> None:
        """Sikeres aszinkron konfiguráció kezelő létrehozása."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_logger = MagicMock()

        # Act
        manager = await ConfigManagerFactory.get_async_manager(
            manager_type="dynamic",
            session=mock_session,
            logger=mock_logger,
        )

        # Assert
        assert isinstance(manager, AsyncConfigManagerInterface)
        assert manager.session == mock_session
        assert manager._logger == mock_logger

    @pytest.mark.asyncio
    async def test_get_async_manager_without_logger(self) -> None:
        """Aszinkron konfiguráció kezelő létrehozása logger nélkül."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        # Act
        manager = await ConfigManagerFactory.get_async_manager(
            manager_type="dynamic",
            session=mock_session,
        )

        # Assert
        assert isinstance(manager, AsyncConfigManagerInterface)
        assert manager.session == mock_session
        assert manager._logger is None

    @pytest.mark.asyncio
    async def test_get_async_manager_invalid_type(self) -> None:
        """Hibaüzenet érvénytelen típus esetén."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        # Act & Assert
        with pytest.raises(
            ConfigLoadError, match="Ismeretlen aszinkron konfig kezelő típus"
        ):
            await ConfigManagerFactory.get_async_manager(
                manager_type="invalid",
                session=mock_session,
            )


class TestGetSupportedExtensions:
    """Teszt osztály a get_supported_extensions metódushoz."""

    def test_get_supported_extensions(self) -> None:
        """Támogatott kiterjesztések lekérése."""
        # Act
        extensions = ConfigManagerFactory.get_supported_extensions()

        # Assert
        assert isinstance(extensions, list)
        assert ".yaml" in extensions
        assert ".yml" in extensions
        assert all(isinstance(ext, str) for ext in extensions)


class TestGetSupportedAsyncTypes:
    """Teszt osztály a get_supported_async_types metódushoz."""

    def test_get_supported_async_types(self) -> None:
        """Támogatott aszinkron típusok lekérése."""
        # Act
        async_types = ConfigManagerFactory.get_supported_async_types()

        # Assert
        assert isinstance(async_types, list)
        assert "dynamic" in async_types
        assert "database" in async_types
        assert all(isinstance(t, str) for t in async_types)


class TestLazyLoading:
    """Teszt osztály a lazy loading mechanizmus ellenőrzéséhez."""

    def test_lazy_load_implementations(self) -> None:
        """Lazy loading ellenőrzése."""
        # Arrange
        # Töröljük a meglévő típusokat
        original_manager_types = ConfigManagerFactory._manager_types.copy()
        original_async_types = ConfigManagerFactory._async_manager_types.copy()
        ConfigManagerFactory._manager_types.clear()
        ConfigManagerFactory._async_manager_types.clear()

        # Act
        # A get_supported_extensions hívja a _lazy_load_implementations-t
        extensions = ConfigManagerFactory.get_supported_extensions()

        # Assert
        assert ".yaml" in extensions
        assert ".yml" in extensions
        assert len(ConfigManagerFactory._manager_types) > 0

        # Act
        # A get_supported_async_types is hívja a _lazy_load_implementations-t
        async_types = ConfigManagerFactory.get_supported_async_types()

        # Assert
        assert "dynamic" in async_types
        assert "database" in async_types
        assert len(ConfigManagerFactory._async_manager_types) > 0

        # Cleanup
        ConfigManagerFactory._manager_types.update(original_manager_types)
        ConfigManagerFactory._async_manager_types.update(original_async_types)


class TestIntegration:
    """Integrációs tesztek a factory teljes funkcionalitásához."""

    def test_register_and_use_custom_manager(self) -> None:
        """Egyéni kezelő regisztrálása és használata."""
        # Arrange
        extension = ".custom"
        manager_class = DummyConfigManager

        # Act
        ConfigManagerFactory.register_manager(extension, manager_class)
        manager = ConfigManagerFactory.create_manager(extension, filename=None)

        # Assert
        assert isinstance(manager, DummyConfigManager)

        # Cleanup
        ConfigManagerFactory._manager_types.pop(extension, None)

    @pytest.mark.asyncio
    async def test_register_and_use_custom_async_manager(self) -> None:
        """Egyéni aszinkron kezelő regisztrálása és használata."""
        # Arrange
        manager_type = "custom_async"
        manager_class = DummyAsyncConfigManager
        mock_session = AsyncMock(spec=AsyncSession)

        # Act
        ConfigManagerFactory.register_async_manager(manager_type, manager_class)
        manager = await ConfigManagerFactory.get_async_manager(
            manager_type=manager_type,
            session=mock_session,
        )

        # Assert
        assert isinstance(manager, DummyAsyncConfigManager)
        assert manager.session == mock_session

        # Cleanup
        ConfigManagerFactory._async_manager_types.pop(manager_type, None)

    def test_yaml_manager_functionality(self) -> None:
        """YAML kezelő funkcionalitásának ellenőrzése."""
        # Arrange
        manager = ConfigManagerFactory.create_manager(".yaml", filename=None)

        # Act & Assert
        assert hasattr(manager, "get")
        assert hasattr(manager, "set")
        assert hasattr(manager, "save")
        assert hasattr(manager, "load")
        assert callable(manager.get)
        assert callable(manager.set)
        assert callable(manager.save)
        assert callable(manager.load)

    @pytest.mark.asyncio
    async def test_dynamic_manager_functionality(self) -> None:
        """Dinamikus kezelő funkcionalitásának ellenőrzése."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        manager = await ConfigManagerFactory.get_async_manager(
            manager_type="dynamic",
            session=mock_session,
        )

        # Act & Assert
        assert hasattr(manager, "get")
        assert hasattr(manager, "set")
        assert hasattr(manager, "start_hot_reload")
        assert hasattr(manager, "stop_hot_reload")
        assert callable(manager.get)
        assert callable(manager.set)
        assert callable(manager.start_hot_reload)
        assert callable(manager.stop_hot_reload)


class TestErrorHandling:
    """Hibakezelési tesztek."""

    def test_config_load_error_message(self) -> None:
        """ConfigLoadError hibaüzenet ellenőrzése."""
        # Act & Assert
        with pytest.raises(ConfigLoadError) as exc_info:
            ConfigManagerFactory.create_manager(".invalid")

        assert "Ismeretlen konfig kezelő típus" in str(exc_info.value)

    def test_value_error_message(self) -> None:
        """ValueError hibaüzenet ellenőrzése."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            ConfigManagerFactory.register_manager("", DummyConfigManager)

        assert "nem lehet üres" in str(exc_info.value)

    def test_type_error_message(self) -> None:
        """TypeError hibaüzenet ellenőrzése."""
        # Act & Assert
        with pytest.raises(TypeError) as exc_info:
            ConfigManagerFactory.register_manager(".invalid", str)

        assert "implementálnia kell a ConfigManagerInterface-t" in str(exc_info.value)


class TestTypeSafety:
    """Típusbiztonsági tesztek."""

    def test_return_type_create_manager(self) -> None:
        """create_manager visszatérési típusának ellenőrzése."""
        # Act
        manager = ConfigManagerFactory.create_manager(".yaml", filename=None)

        # Assert
        assert isinstance(manager, ConfigManagerInterface)
        assert hasattr(manager, "get")
        assert hasattr(manager, "set")
        assert hasattr(manager, "save")
        assert hasattr(manager, "load")

    @pytest.mark.asyncio
    async def test_return_type_get_async_manager(self) -> None:
        """get_async_manager visszatérési típusának ellenőrzése."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        # Act
        manager = await ConfigManagerFactory.get_async_manager(
            manager_type="dynamic",
            session=mock_session,
        )

        # Assert
        assert isinstance(manager, AsyncConfigManagerInterface)
        assert hasattr(manager, "get")
        assert hasattr(manager, "set")
        assert hasattr(manager, "start_hot_reload")
        assert hasattr(manager, "stop_hot_reload")

    def test_extension_normalization(self) -> None:
        """Kiterjesztés normalizálásának ellenőrzése."""
        # Arrange
        extension = "test"
        manager_class = DummyConfigManager

        # Act
        ConfigManagerFactory.register_manager(extension, manager_class)

        # Assert
        assert ".test" in ConfigManagerFactory.get_supported_extensions()
        assert "test" not in ConfigManagerFactory.get_supported_extensions()

        # Cleanup
        ConfigManagerFactory._manager_types.pop(".test", None)


class TestEdgeCases:
    """Edge case tesztek."""

    def test_empty_filename(self) -> None:
        """Üres fájlnév kezelése."""
        # Act
        manager = ConfigManagerFactory.create_manager(".yaml", filename="")

        # Assert
        assert isinstance(manager, ConfigManagerInterface)
        # A YAMLConfigManager nem állítja be az üres stringet
        assert manager._filename is None or manager._filename == ""

    def test_none_filename(self) -> None:
        """None fájlnév kezelése."""
        # Act
        manager = ConfigManagerFactory.create_manager(".yaml", filename=None)

        # Assert
        assert isinstance(manager, ConfigManagerInterface)
        assert manager._filename is None

    def test_whitespace_in_extension(self) -> None:
        """Szóközt tartalmazó kiterjesztés kezelése."""
        # Arrange
        extension = " .test "
        manager_class = DummyConfigManager

        # Act
        ConfigManagerFactory.register_manager(extension, manager_class)
        extensions = ConfigManagerFactory.get_supported_extensions()

        # Assert
        # A whitespace-t tartalmazó extension is benne van
        assert ". .test " in extensions or ".test" in extensions

        # Cleanup
        ConfigManagerFactory._manager_types.pop(". .test ", None)
        ConfigManagerFactory._manager_types.pop(".test", None)


class TestPerformance:
    """Teljesítmény tesztek."""

    def test_multiple_manager_creation(self) -> None:
        """Több kezelő gyors létrehozása."""
        import time

        # Arrange
        start_time = time.time()

        # Act
        for i in range(100):
            manager = ConfigManagerFactory.create_manager(".yaml", filename=None)
            assert manager is not None

        # Assert
        end_time = time.time()
        elapsed_time = end_time - start_time
        # 100 kezelő létrehozása ne tartson túl sokáig
        assert elapsed_time < 1.0  # 1 másodpercnél kevesebb

    def test_lazy_loading_performance(self) -> None:
        """Lazy loading teljesítmény ellenőrzése."""
        import time

        # Arrange
        # Töröljük a cache-t
        original_types = ConfigManagerFactory._manager_types.copy()
        ConfigManagerFactory._manager_types.clear()

        start_time = time.time()

        # Act
        # Az első hívás betölti a implementációkat
        extensions = ConfigManagerFactory.get_supported_extensions()

        first_call_time = time.time() - start_time

        # A második hívás már a cache-ből jön
        start_time = time.time()
        extensions2 = ConfigManagerFactory.get_supported_extensions()
        second_call_time = time.time() - start_time

        # Assert
        assert extensions == extensions2
        # A második hívásnak gyorsabbnak kell lennie
        assert second_call_time <= first_call_time

        # Cleanup
        ConfigManagerFactory._manager_types.update(original_types)


class TestThreadSafety:
    """Szálbiztonsági tesztek."""

    def test_concurrent_access(self) -> None:
        """Egyidejű hozzáférés ellenőrzése."""
        import threading

        # Arrange
        results: list[ConfigManagerInterface] = []
        errors: list[Exception] = []

        def create_manager(index: int) -> None:
            try:
                manager = ConfigManagerFactory.create_manager(".yaml", filename=None)
                results.append(manager)
            except Exception as e:
                errors.append(e)

        # Act
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_manager, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Assert
        assert len(errors) == 0
        assert len(results) == 10
        assert all(isinstance(manager, ConfigManagerInterface) for manager in results)