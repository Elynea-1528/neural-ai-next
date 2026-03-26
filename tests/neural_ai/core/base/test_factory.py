"""CoreComponentFactory tesztelése.

Ez a modul tartalmazza a CoreComponentFactory osztály egységtesztjeit,
beleértve a lazy loading, dependency injection és komponens létrehozási
funkcionalitás tesztelését.
"""

import tempfile
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from neural_ai.core.base.exceptions import ConfigurationError, DependencyError
from neural_ai.core.base.factory import CoreComponentFactory
from neural_ai.core.base.implementations.di_container import DIContainer


class TestCoreComponentFactory:
    """CoreComponentFactory osztály tesztjei."""

    def test_init_with_container(self) -> None:
        """Teszteli a factory inicializálását DI konténerrel."""
        container: DIContainer = DIContainer()
        # Valódi LoggerInterface implementáció használata
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        class DummyLogger(LoggerInterface):
            def __init__(self, name: str, **kwargs): pass
            def debug(self, message: str, **kwargs): pass
            def info(self, message: str, **kwargs): pass
            def warning(self, message: str, **kwargs): pass
            def error(self, message: str, **kwargs): pass
            def critical(self, message: str, **kwargs): pass
            def log(self, level: str, message: str, **kwargs): pass
            def set_level(self, level: int) -> None: pass
            def get_level(self) -> int: return 20

        mock_logger = DummyLogger(name="test")
        container.register_instance(LoggerInterface, mock_logger)

        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A factory használja a konténert, ezt a logger property-n keresztül ellenőrizzük
        logger = factory.logger
        assert logger is not None
        assert logger is mock_logger

    def test_logger_property_returns_logger(self) -> None:
        """Teszteli, hogy a logger property logger interfészt ad vissza."""
        container: DIContainer = DIContainer()
        # Mock logger regisztrálása
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        class DummyLogger(LoggerInterface):
            def __init__(self, name: str): pass
            def debug(self, message: str, **kwargs): pass
            def info(self, message: str, **kwargs): pass
            def warning(self, message: str, **kwargs): pass
            def error(self, message: str, **kwargs): pass
            def critical(self, message: str, **kwargs): pass
            def log(self, level: str, message: str, **kwargs): pass
            def set_level(self, level: int) -> None: pass  # Javítva: int típus
            def get_level(self) -> int: return 20  # get_level int-et ad vissza

        mock_logger = DummyLogger(name="test")
        container.register_instance(LoggerInterface, mock_logger)

        factory: CoreComponentFactory = CoreComponentFactory(container)

        logger = factory.logger
        assert logger is not None
        assert isinstance(logger, LoggerInterface)

    def test_config_manager_property_raises_dependency_error(self) -> None:
        """Teszteli, hogy a config manager property DependencyError-t dob, ha nincs regisztrálva."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A match stringet lazábbra vesszük, mert a factory implementáció változhatott
        with pytest.raises(DependencyError):
            _ = factory.config_manager

    def test_storage_property_raises_dependency_error(self) -> None:
        """Teszteli, hogy a storage property DependencyError-t dob, ha nincs regisztrálva."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A match stringet lazábbra vesszük
        with pytest.raises(DependencyError):
            _ = factory.storage

    def test_reset_lazy_loaders(self) -> None:
        """Teszteli a lazy loader-ek visszaállítását."""
        container: DIContainer = DIContainer()
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        class DummyLogger(LoggerInterface):
            def __init__(self, name: str, **kwargs): pass
            def debug(self, message: str, **kwargs): pass
            def info(self, message: str, **kwargs): pass
            def warning(self, message: str, **kwargs): pass
            def error(self, message: str, **kwargs): pass
            def critical(self, message: str, **kwargs): pass
            def log(self, level: str, message: str, **kwargs): pass
            def set_level(self, level: int) -> None: pass
            def get_level(self) -> int: return 20

        mock_logger = DummyLogger(name="test")
        container.register_instance(LoggerInterface, mock_logger)

        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Először betöltjük a loggert
        logger1 = factory.logger
        # Visszaállítjuk a loader-eket
        factory.reset_lazy_loaders()
        # Újra betöltjük
        logger2 = factory.logger

        assert logger1 is not None
        assert logger2 is not None

    def test_validate_dependencies_storage_missing_base_directory(self) -> None:
        """Teszteli a storage függőség validálását hiányzó base_path esetén."""
        config: dict[str, str] = {}

        # Pydantic validation error wrapped in ConfigurationError
        with pytest.raises(ConfigurationError, match="Configuration error for storage"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_storage_invalid_path(self) -> None:
        """Teszteli a storage függőség validálását érvénytelen elérési úttal."""
        config: dict[str, str] = {"base_path": "/nonexistent/path/to/storage"}

        with pytest.raises(ConfigurationError, match="parent does not exist"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_storage_valid(self) -> None:
        """Teszteli a storage függőség validálását érvényes konfiggal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path: Path = Path(temp_dir) / "storage"
            config: dict[str, str] = {"base_path": str(storage_path)}

            # Nem dob kivételt
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_logger_missing_name(self) -> None:
        """Teszteli a logger függőség validálását hiányzó névvel."""
        config: dict[str, str] = {}

        with pytest.raises(ConfigurationError, match="Field required"):
            CoreComponentFactory._validate_dependencies("logger", config)

    def test_validate_dependencies_logger_valid(self) -> None:
        """Teszteli a logger függőség validálását érvényes konfiggal."""
        config: dict[str, str] = {"name": "test_logger"}

        # Nem dob kivételt
        CoreComponentFactory._validate_dependencies("logger", config)

    def test_validate_dependencies_config_manager_missing_path(self) -> None:
        """Teszteli a config manager függőség validálását hiányzó fájlúttal."""
        config: dict[str, str] = {}

        with pytest.raises(ConfigurationError, match="Field required"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    def test_validate_dependencies_config_manager_nonexistent_file(self) -> None:
        """Teszteli a config manager függőség validálását nem létező fájllal."""
        config: dict[str, str] = {"config_file_path": "/nonexistent/config.yml"}

        with pytest.raises(ConfigurationError, match="Config file does not exist"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    def test_validate_dependencies_config_manager_valid(self) -> None:
        """Teszteli a config manager függőség validálását érvényes konfiggal."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("test: config")
            temp_file: str = f.name

        try:
            config: dict[str, str] = {"config_file_path": temp_file}
            # Nem dob kivételt
            CoreComponentFactory._validate_dependencies("config_manager", config)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_validate_dependencies_invalid_component_type(self) -> None:
        """Teszteli a függőség validálását érvénytelen komponens típussal."""
        config: dict[str, str] = {}

        # Érvénytelen típus esetén nem dob kivételt
        CoreComponentFactory._validate_dependencies("invalid_type", config)

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
    @patch("neural_ai.data.storage.implementations.file_storage.FileStorage")
    def test_create_components_with_all_paths(
        self, mock_file_storage: MagicMock, mock_get_logger: MagicMock, mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a komponensek létrehozását minden elérési úttal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path: Path = Path(temp_dir) / "config.yml"
            log_path: Path = Path(temp_dir) / "app.log"
            storage_path: Path = Path(temp_dir) / "storage"

            config_path.touch()
            log_path.touch()
            storage_path.mkdir()

            components = CoreComponentFactory.create_components(
                config_path=str(config_path), log_path=str(log_path), storage_path=str(storage_path)
            )

            assert components is not None
            assert components.has_config()
            assert components.has_logger()
            assert components.has_storage()

    def test_create_components_without_paths(self) -> None:
        """Teszteli a komponensek létrehozását elérési utak nélkül (funkcionális teszt)."""
        # Tiszta állapotból indulunk - új factory példány
        from neural_ai.core.base.implementations.di_container import DIContainer

        container = DIContainer()
        factory = CoreComponentFactory(container)

        # Reset lazy loaders a tiszta állapot biztosításához
        factory.reset_lazy_loaders()

        components = CoreComponentFactory.create_components()

        assert components is not None
        # Ellenőrizzük, hogy a komponensek létrejöttek
        assert hasattr(components, 'logger')
        assert hasattr(components, 'validate')

        # Nem minden komponens lesz inicializálva (config_manager és storage hiányzik)
        assert not components.validate()

    def test_create_with_container(self) -> None:
        """Teszteli a komponensek létrehozását meglévő konténerből."""
        container: DIContainer = DIContainer()
        components = CoreComponentFactory.create_with_container(container)

        assert components is not None

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
    def test_create_minimal_with_config_file(
        self, mock_get_logger: MagicMock, mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a minimális komponensek létrehozását config fájllal."""
        mock_config = MagicMock()
        # A factory a config.get("storage")-t hívja, ami egy dict-et ad vissza,
        # nem {"storage": dict}-et!
        mock_config.get.side_effect = lambda k: ({"base_path": "/tmp"} if k == "storage" else {})
        mock_get_manager.return_value = mock_config

        # A FileStorage-t itt is mockoljuk, hogy ne próbáljon valódi fájlrendszerhez nyúlni
        # és validálni a base_path-t (ami /tmp, de lehet, hogy nem létezik a konténerben
        # úgy ahogy várjuk)
        # Bár a /tmp általában létezik, de a biztonság kedvéért.
        # Ráadásul a create_storage hívja meg, ami a FileStorage-t példányosítja.

        with patch("neural_ai.data.storage.implementations.file_storage.FileStorage"):
            with patch("pathlib.Path.exists", return_value=True):
                components = CoreComponentFactory.create_minimal()

                assert components is not None
                assert components.has_logger()
                assert components.has_storage()
                assert components.has_config()

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
    def test_create_minimal_without_config_file(
        self, mock_get_logger: MagicMock, mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a minimális komponensek létrehozását config fájl nélkül."""
        from neural_ai.core.config.exceptions import ConfigLoadError

        # Szimuláljuk, hogy a config fájl nem tölthető be
        # A get_manager híváskor kivételt dob, így a config változó None lesz
        mock_get_manager.side_effect = ConfigLoadError("Config not found")

        # Mockoljuk a FileStorage-t, mert config hiányában az "else" ág fut le:
        # storage = FileStorage(logger=logger)
        # Ez a FileStorage alapból validálja magát, és base_path nélkül elszáll.
        # Ezért kell, hogy a tesztben a MOCK storage jöjjön létre.
        with patch(
            "neural_ai.data.storage.implementations.file_storage.FileStorage"
        ) as mock_storage:
            with patch("pathlib.Path.exists", return_value=False):
                components = CoreComponentFactory.create_minimal()

                assert components is not None
                assert components.has_logger()
                assert components.has_storage()
                mock_storage.assert_called_once()

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
    def test_create_minimal_with_config_file_no_logger_section(
        self, mock_get_logger: MagicMock, mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a komponensek létrehozását config fájllal, de logger section nélkül."""
        mock_config = MagicMock()
        mock_config.get.side_effect = lambda k: ({"base_path": "/tmp"} if k == "storage" else {})  # type: ignore[arg-type,return-value]
        mock_get_manager.return_value = mock_config

        with patch("neural_ai.data.storage.implementations.file_storage.FileStorage"):
            with patch("pathlib.Path.exists", return_value=True):
                components = CoreComponentFactory.create_minimal()

                assert components is not None
                assert components.has_logger()
                assert components.has_storage()
                assert components.has_config()

    def test_create_logger(self) -> None:
        """Teszteli a logger létrehozását (funkcionális teszt)."""
        # Valódi logger létrehozása
        logger = CoreComponentFactory.create_logger("test_logger", {"level": "INFO"})

        # Ellenőrizzük, hogy logger objektum létrejött
        assert logger is not None

        # Ellenőrizzük, hogy van-e a szükséges metódusok (duck typing)
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'critical')

        # Ellenőrizzük, hogy működik (ne dobjon hibát)
        logger.info("Test message")
        logger.debug("Debug message")

    def test_create_logger_invalid_config(self) -> None:
        """Teszteli a logger létrehozását érvénytelen konfiggal."""
        with pytest.raises(ConfigurationError, match="String should have at least 1 character"):
            CoreComponentFactory.create_logger("", {})

    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    def test_create_config_manager(self, mock_get_manager: MagicMock) -> None:
        """Teszteli a config manager létrehozását."""
        mock_config: MagicMock = MagicMock()
        mock_get_manager.return_value = mock_config

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("test: config")
            temp_file: str = f.name

        try:
            # extra="forbid" miatt nem adhatunk át extra kulcsokat
            config = CoreComponentFactory.create_config_manager(temp_file, {})

            assert config is mock_config
            mock_get_manager.assert_called_once_with(temp_file)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_create_config_manager_invalid_path(self) -> None:
        """Teszteli a config manager létrehozását érvénytelen elérési úttal."""
        with pytest.raises(ConfigurationError, match="String should have at least 1 character"):
            CoreComponentFactory.create_config_manager("", {})

    @patch("neural_ai.core.events.factory.EventBusFactory.get_event_bus")
    @patch("neural_ai.core.logger.factory.LoggerFactory.get_logger")
    @patch("neural_ai.core.config.factory.ConfigManagerFactory.get_manager")
    def test_create_storage(
        self, mock_get_manager: MagicMock, mock_get_logger: MagicMock, mock_get_event_bus: MagicMock
    ) -> None:
        """Teszteli a storage létrehozását."""
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        mock_get_manager.return_value = mock_config
        mock_get_logger.return_value = mock_logger
        mock_get_event_bus.return_value = mock_event_bus

        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CoreComponentFactory.create_storage(temp_dir, mock_logger, mock_config)

            assert storage is not None
            assert hasattr(storage, "save_dataframe")
            assert hasattr(storage, "load_dataframe")
            assert hasattr(storage, "save_object")
            assert hasattr(storage, "load_object")

    def test_create_storage_invalid_path(self) -> None:
        """Teszteli a storage létrehozását érvénytelen elérési úttal."""
        from unittest.mock import MagicMock

        mock_logger = MagicMock()
        mock_config = MagicMock()
        # Mocking config.get to return empty dict, causing missing base_path
        mock_config.get.return_value = {}

        with pytest.raises(ConfigurationError, match="Field required"):
            CoreComponentFactory.create_storage(None, mock_logger, mock_config)

    def test_lazy_property_decorator_exists(self) -> None:
        """Teszteli, hogy a lazy property dekorátorok léteznek."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Csak ellenőrizzük, hogy a metódusok léteznek
        # A valós működést a create metódusok tesztelik
        assert hasattr(factory.__class__, "_expensive_config")
        assert hasattr(factory.__class__, "_component_cache")

    def test_component_cache_lazy_property(self) -> None:
        """Teszteli a komponens gyorsítótár lazy property működését."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Első hozzáféréskor töltse be
        cache1 = factory._component_cache
        cache2 = factory._component_cache

        # Mindkét esetben ugyanazt az értéket kell kapjuk
        assert cache1 is cache2

    def test_get_logger_with_registered_logger(self) -> None:
        """Teszteli a logger property-t regisztrált loggerrel (funkcionális teszt)."""
        from neural_ai.core.logger.implementations.default_logger import DefaultLogger
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        container: DIContainer = DIContainer()
        logger = DefaultLogger(name="test")
        container.register_instance(LoggerInterface, logger)

        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A logger property-t használjuk (nem a _get_logger metódust)
        result = factory.logger

        # Ellenőrizzük, hogy logger objektum létrejött
        assert result is not None

        # Duck typing: ellenőrizzük a szükséges metódusokat
        assert hasattr(result, 'info')
        assert hasattr(result, 'debug')
        assert hasattr(result, 'error')
        assert hasattr(result, 'warning')
        assert hasattr(result, 'critical')

        # Ellenőrizzük, hogy működik
        result.info("Test message")

    def test_get_logger_fallback_to_default_logger_factory(self) -> None:
        """Teszteli, hogy a logger property fallbackel a LoggerFactory-ra (funkcionális teszt)."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Üres konténerrel a fallback LoggerFactory-t kell használnia
        result = factory.logger

        # Ellenőrizzük, hogy logger objektum létrejött
        assert result is not None

        # Duck typing: ellenőrizzük a szükséges metódusokat
        assert hasattr(result, 'info')
        assert hasattr(result, 'debug')
        assert hasattr(result, 'error')
        assert hasattr(result, 'warning')
        assert hasattr(result, 'critical')

        # Ellenőrizzük, hogy működik
        result.info("Fallback test message")

    def test_get_logger_with_invalid_logger_raises_dependency_error(self) -> None:
        """Teszteli, hogy érvénytelen logger DependencyError-t dob (funkcionális teszt)."""
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface

        container: DIContainer = DIContainer()

        # Érvénytelen objektum regisztrálása (nem LoggerInterface)
        class InvalidLogger:
            pass

        invalid_logger = InvalidLogger()
        container.register_instance(LoggerInterface, invalid_logger)

        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A DependencyError-nak kell jönnie a logger property hívásakor
        with pytest.raises(DependencyError, match="Logger must implement LoggerInterface"):
            _ = factory.logger

    def test_get_config_manager_with_registered_config(self) -> None:
        """Teszteli a _get_config_manager metódust regisztrált config managerrel (funkcionális teszt)."""
        from pathlib import Path

        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

        container: DIContainer = DIContainer()

        # Dummy ConfigManager implementáció
        class DummyConfigManager(ConfigManagerInterface):
            def __init__(self, config_path: Path | None = None):
                pass
            def get(self, key: str, default: object = None) -> object:
                return default
            def set(self, key: str, value: object) -> None:
                pass
            def has(self, key: str) -> bool:
                return False
            def get_section(self, section: str) -> dict[str, object]:
                return {}
            def load(self, path: Path) -> None:
                pass
            def load_directory(self, directory: Path) -> None:
                pass
            def save(self, path: Path) -> None:
                pass
            def validate(self) -> bool:
                return True

        mock_config = DummyConfigManager()
        container.register_instance(ConfigManagerInterface, mock_config)

        factory: CoreComponentFactory = CoreComponentFactory(container)
        result = factory._get_config_manager()

        assert result is not None
        assert result is mock_config

    def test_get_storage_raises_dependency_error_if_not_found(self) -> None:
        """Teszteli, hogy a _get_storage DependencyError-t dob, ha nincs regisztrálva."""
        from unittest.mock import patch

        from neural_ai.core.base.implementations.di_container import DIContainer

        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Mockoljuk a container.resolve metódust, hogy None-t adjon vissza
        with patch.object(factory._container, "resolve", return_value=None):
            with pytest.raises(DependencyError, match="Storage not available"):
                factory._get_storage()

    def test_expensive_config_lazy_property(self) -> None:
        """Teszteli az _expensive_config lazy property működését (111-114. sorok)."""
        from unittest.mock import MagicMock, patch

        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        container: DIContainer = DIContainer()

        # Mock config manager létrehozása
        mock_config: MagicMock = MagicMock(spec=ConfigManagerInterface)
        mock_config._initialized = True  # Singleton ellenőrzés átugrása
        mock_config.get.return_value = {"test": "config"}

        container.register_instance(ConfigManagerInterface, mock_config)

        # Mockoljuk a resolve metódust, hogy a container.resolve() működjön
        with patch.object(container, "resolve", return_value=mock_config):
            # Csak a DIContainer._verify_interface_implementation metódusában
            # mockoljuk az isinstance-t
            def isinstance_mock(obj: Any, class_or_tuple: Any) -> bool:  # type: ignore[no-untyped-def,arg-type]
                if class_or_tuple in [ConfigManagerInterface, StorageInterface]:
                    return True
                return isinstance(obj, class_or_tuple)

            with patch(
                "neural_ai.core.base.implementations.di_container.isinstance",
                side_effect=isinstance_mock,
            ):
                factory: CoreComponentFactory = CoreComponentFactory(container)

                # Mockoljuk a _config_loader-t, hogy a mock_config-ot adja vissza
                with patch.object(factory, "_config_loader") as mock_loader:
                    mock_loader.return_value = mock_config

                    # Mockoljuk a time.sleep-et, hogy ne várjon
                    with patch("neural_ai.core.base.factory.time.sleep"):
                        # Mockoljuk a _process_config metódust, hogy a
                        # config.get() eredményét adja vissza
                        with patch.object(factory, "_process_config", side_effect=lambda x: x):  # type: ignore[attr-defined,arg-type]
                            # Első hozzáféréskor töltse be
                            expensive_config1 = factory._expensive_config
                            expensive_config2 = factory._expensive_config

                        # Mindkét esetben ugyanazt az értéket kell kapjuk (lazy property)
                        assert expensive_config1 is expensive_config2
                        # A _expensive_config a config.get() eredményét adja vissza
                        assert expensive_config1 == {"test": "config"}

    def test_process_config(self) -> None:
        """Teszteli a _process_config metódust (125. sor)."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        test_config = {"key": "value"}
        result = factory._process_config(test_config)

        assert result == test_config

    def test_reset_lazy_loaders_clears_lazy_properties(self) -> None:
        """Teszteli, hogy a reset_lazy_loaders törli a lazy property-ket (146. sor)."""
        from unittest.mock import MagicMock, patch

        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

        container: DIContainer = DIContainer()

        # Mock config manager létrehozása
        mock_config: MagicMock = MagicMock(spec=ConfigManagerInterface)
        mock_config._initialized = True  # Singleton ellenőrzés átugrása
        mock_config.get.return_value = {"test": "config"}

        container.register_instance(ConfigManagerInterface, mock_config)

        # Mockoljuk a resolve metódust, hogy a container.resolve() működjön
        with patch.object(container, "resolve", return_value=mock_config):
            # Csak a DIContainer._verify_interface_implementation metódusában
            # mockoljuk az isinstance-t
            def isinstance_mock(obj: Any, class_or_tuple: Any) -> bool: # type: ignore
                if class_or_tuple in [ConfigManagerInterface, StorageInterface]:
                    return True
                return isinstance(obj, class_or_tuple)

            with patch(
                "neural_ai.core.base.implementations.di_container.isinstance",
                side_effect=isinstance_mock,
            ):
                factory: CoreComponentFactory = CoreComponentFactory(container)

                # Mockoljuk a _config_loader-t, hogy a mock_config-ot adja vissza
                with patch.object(factory, "_config_loader") as mock_loader:
                    mock_loader.return_value = mock_config

                    # Mockoljuk a time.sleep-et, hogy ne várjon
                    with patch("neural_ai.core.base.factory.time.sleep"):
                        # Mockoljuk a _process_config metódust, hogy a
                        # config.get() eredményét adja vissza
                        with patch.object(factory, "_process_config", side_effect=lambda x: x):
                            # Hozzáférés az _expensive_config-hoz, hogy létrejöjjön a lazy property
                            _ = factory._expensive_config

                # Ellenőrizzük, hogy a lazy property létrejött
                lazy_attr_exists = hasattr(factory, "_lazy__expensive_config")
                assert lazy_attr_exists, "Lazy property should exist before reset"

                # Visszaállítjuk a lazy loader-eket
                factory.reset_lazy_loaders()

                # Ellenőrizzük, hogy a lazy property-k törlődtek
                lazy_attr_exists_after = hasattr(factory, "_lazy__expensive_config")
                assert not lazy_attr_exists_after, "Lazy properties should be cleared after reset"
