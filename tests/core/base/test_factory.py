"""CoreComponentFactory tesztelése.

Ez a modul tartalmazza a CoreComponentFactory osztály egységtesztjeit,
beleértve a lazy loading, dependency injection és komponens létrehozási
funkcionalitás tesztelését.
"""

import tempfile
from pathlib import Path
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
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # A factory használja a konténert, ezt a logger property-n keresztül ellenőrizzük
        logger = factory.logger
        assert logger is not None
        # Megjegyzés: A _container protected, de a működés a lényeg

    def test_logger_property_returns_logger(self) -> None:
        """Teszteli, hogy a logger property logger interfészt ad vissza."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        logger = factory.logger
        assert logger is not None
        assert hasattr(logger, 'debug')
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'warning')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'critical')

    def test_config_manager_property_raises_dependency_error(self) -> None:
        """Teszteli, hogy a config manager property DependencyError-t dob, ha nincs regisztrálva."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        with pytest.raises(DependencyError, match="ConfigManager not available"):
            _ = factory.config_manager

    def test_storage_property_raises_dependency_error(self) -> None:
        """Teszteli, hogy a storage property DependencyError-t dob, ha nincs regisztrálva."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        with pytest.raises(DependencyError, match="Storage not available"):
            _ = factory.storage

    def test_reset_lazy_loaders(self) -> None:
        """Teszteli a lazy loader-ek visszaállítását."""
        container: DIContainer = DIContainer()
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
        """Teszteli a storage függőség validálását hiányzó base_directory esetén."""
        config: dict[str, str] = {}

        with pytest.raises(ConfigurationError, match="Storage base_directory not configured"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_storage_invalid_path(self) -> None:
        """Teszteli a storage függőség validálását érvénytelen elérési úttal."""
        config: dict[str, str] = {"base_directory": "/nonexistent/path/to/storage"}

        with pytest.raises(ConfigurationError, match="parent does not exist"):
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_storage_valid(self) -> None:
        """Teszteli a storage függőség validálását érvényes konfiggal."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage_path: Path = Path(temp_dir) / "storage"
            config: dict[str, str] = {"base_directory": str(storage_path)}

            # Nem dob kivételt
            CoreComponentFactory._validate_dependencies("storage", config)

    def test_validate_dependencies_logger_missing_name(self) -> None:
        """Teszteli a logger függőség validálását hiányzó névvel."""
        config: dict[str, str] = {}

        with pytest.raises(ConfigurationError, match="Logger name not configured"):
            CoreComponentFactory._validate_dependencies("logger", config)

    def test_validate_dependencies_logger_valid(self) -> None:
        """Teszteli a logger függőség validálását érvényes konfiggal."""
        config: dict[str, str] = {"name": "test_logger"}

        # Nem dob kivételt
        CoreComponentFactory._validate_dependencies("logger", config)

    def test_validate_dependencies_config_manager_missing_path(self) -> None:
        """Teszteli a config manager függőség validálását hiányzó fájlúttal."""
        config: dict[str, str] = {}

        with pytest.raises(ConfigurationError, match="Config file path not configured"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    def test_validate_dependencies_config_manager_nonexistent_file(self) -> None:
        """Teszteli a config manager függőség validálását nem létező fájllal."""
        config: dict[str, str] = {"config_file_path": "/nonexistent/config.yml"}

        with pytest.raises(ConfigurationError, match="Config file does not exist"):
            CoreComponentFactory._validate_dependencies("config_manager", config)

    def test_validate_dependencies_config_manager_valid(self) -> None:
        """Teszteli a config manager függőség validálását érvényes konfiggal."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
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

    @patch('neural_ai.core.config.factory.ConfigManagerFactory.get_manager')
    @patch('neural_ai.core.logger.factory.LoggerFactory.get_logger')
    @patch('neural_ai.core.storage.implementations.file_storage.FileStorage')
    def test_create_components_with_all_paths(
        self,
        mock_file_storage: MagicMock,
        mock_get_logger: MagicMock,
        mock_get_manager: MagicMock
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
                config_path=str(config_path),
                log_path=str(log_path),
                storage_path=str(storage_path)
            )

            assert components is not None
            assert components.has_config()
            assert components.has_logger()
            assert components.has_storage()

    def test_create_components_without_paths(self) -> None:
        """Teszteli a komponensek létrehozását elérési utak nélkül."""
        components = CoreComponentFactory.create_components()

        assert components is not None
        # Nem minden komponens lesz inicializálva
        assert not components.validate()

    def test_create_with_container(self) -> None:
        """Teszteli a komponensek létrehozását meglévő konténerből."""
        container: DIContainer = DIContainer()
        components = CoreComponentFactory.create_with_container(container)

        assert components is not None

    @patch('neural_ai.core.config.factory.ConfigManagerFactory.get_manager')
    @patch('neural_ai.core.logger.factory.LoggerFactory.get_logger')
    def test_create_minimal_with_config_file(
        self,
        mock_get_logger: MagicMock,
        mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a minimális komponensek létrehozását config fájllal."""
        with patch('pathlib.Path.exists', return_value=True):
            components = CoreComponentFactory.create_minimal()

            assert components is not None
            assert components.has_logger()
            assert components.has_storage()

    @patch('neural_ai.core.logger.factory.LoggerFactory.get_logger')
    def test_create_minimal_without_config_file(
        self,
        mock_get_logger: MagicMock
    ) -> None:
        """Teszteli a minimális komponensek létrehozását config fájl nélkül."""
        with patch('pathlib.Path.exists', return_value=False):
            components = CoreComponentFactory.create_minimal()

            assert components is not None
            assert components.has_logger()
            assert components.has_storage()

    @patch('neural_ai.core.logger.factory.LoggerFactory.get_logger')
    def test_create_logger(
        self,
        mock_get_logger: MagicMock
    ) -> None:
        """Teszteli a logger létrehozását."""
        mock_logger: MagicMock = MagicMock()
        mock_get_logger.return_value = mock_logger

        logger = CoreComponentFactory.create_logger("test_logger", {"level": "INFO"})

        assert logger is mock_logger
        mock_get_logger.assert_called_once_with(
            name="test_logger",
            config={"name": "test_logger", "level": "INFO"}
        )

    def test_create_logger_invalid_config(self) -> None:
        """Teszteli a logger létrehozását érvénytelen konfiggal."""
        with pytest.raises(ConfigurationError, match="Logger name not configured"):
            CoreComponentFactory.create_logger("", {})

    @patch('neural_ai.core.config.factory.ConfigManagerFactory.get_manager')
    def test_create_config_manager(
        self,
        mock_get_manager: MagicMock
    ) -> None:
        """Teszteli a config manager létrehozását."""
        mock_config: MagicMock = MagicMock()
        mock_get_manager.return_value = mock_config

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
            f.write("test: config")
            temp_file: str = f.name

        try:
            config = CoreComponentFactory.create_config_manager(temp_file, {"key": "value"})

            assert config is mock_config
            mock_get_manager.assert_called_once_with(temp_file)
        finally:
            Path(temp_file).unlink(missing_ok=True)

    def test_create_config_manager_invalid_path(self) -> None:
        """Teszteli a config manager létrehozását érvénytelen elérési úttal."""
        with pytest.raises(ConfigurationError, match="Config file path not configured"):
            CoreComponentFactory.create_config_manager("", {})

    def test_create_storage(self) -> None:
        """Teszteli a storage létrehozását."""
        with tempfile.TemporaryDirectory() as temp_dir:
            storage = CoreComponentFactory.create_storage(temp_dir, {"key": "value"})

            assert storage is not None
            assert hasattr(storage, 'save_dataframe')
            assert hasattr(storage, 'load_dataframe')
            assert hasattr(storage, 'save_object')
            assert hasattr(storage, 'load_object')

    def test_create_storage_invalid_path(self) -> None:
        """Teszteli a storage létrehozását érvénytelen elérési úttal."""
        with pytest.raises(ConfigurationError, match="Storage base_directory not configured"):
            CoreComponentFactory.create_storage("", {})

    def test_lazy_property_decorator_exists(self) -> None:
        """Teszteli, hogy a lazy property dekorátorok léteznek."""
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)

        # Csak ellenőrizzük, hogy a metódusok léteznek
        # A valós működést a create metódusok tesztelik
        assert hasattr(factory.__class__, '_expensive_config')
        assert hasattr(factory.__class__, '_component_cache')

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
        """Teszteli a _get_logger metódust regisztrált loggerrel (58-59. sorok)."""
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        from neural_ai.core.logger.implementations.default_logger import DefaultLogger
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        logger = DefaultLogger(name="test")
        # Regisztráljuk a loggert a konténerbe
        container.register_instance(LoggerInterface, logger)
        
        factory: CoreComponentFactory = CoreComponentFactory(container)
        
        # Mockoljuk a resolve metódust, hogy biztosan visszaadja a loggert
        with patch.object(factory._container, 'resolve', return_value=logger):
            # Közvetlenül hívjuk meg a _get_logger metódust
            result = factory._get_logger()
        
        assert result is not None
        assert isinstance(result, LoggerInterface)
        # A regisztrált logger-t kapjuk vissza (ugyanaz a típus)
        assert type(result) == type(logger)
    
    def test_get_logger_with_invalid_logger_raises_assertion_error(self) -> None:
        """Teszteli a _get_logger metódust érvénytelen loggerrel (58-59. sorok assertje)."""
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        # Mock objektum, ami nem implementálja a LoggerInterface-t
        invalid_logger = MagicMock()
        
        factory: CoreComponentFactory = CoreComponentFactory(container)
        
        # Mockoljuk a resolve metódust, hogy visszaadja az érvénytelen loggert
        with patch.object(factory._container, 'resolve', return_value=invalid_logger):
            # Az assert-nek el kell buknia, mert a logger nem implementálja az interfészt
            with pytest.raises(AssertionError, match="Logger must implement LoggerInterface"):
                factory._get_logger()

    def test_get_config_manager_with_registered_config(self) -> None:
        """Teszteli a _get_config_manager metódust regisztrált config managerrel (74-77. sorok)."""
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)
        
        # Mock config manager létrehozása, ami implementálja az interfészt
        mock_config = MagicMock(spec=ConfigManagerInterface)
        
        # Mockoljuk a factory _container.resolve metódusát
        with patch.object(factory._container, 'resolve', return_value=mock_config):
            # Mockoljuk az isinstance-t, hogy mindig True-t adjon vissza
            with patch('neural_ai.core.base.implementations.di_container.isinstance', return_value=True):
                # Közvetlenül hívjuk meg a _get_config_manager metódust
                result = factory._get_config_manager()
        
        assert result is not None
        assert result is mock_config

    def test_get_storage_with_registered_storage(self) -> None:
        """Teszteli a _get_storage metódust regisztrált storagel (87-88. sorok)."""
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        factory: CoreComponentFactory = CoreComponentFactory(container)
        
        # Mock storage létrehozása, ami implementálja az interfészt
        mock_storage: MagicMock = MagicMock(spec=StorageInterface)
        
        # Mockoljuk a factory _container.resolve metódusát
        with patch.object(factory._container, 'resolve', return_value=mock_storage):
            # Mockoljuk az isinstance-t, hogy mindig True-t adjon vissza
            with patch('neural_ai.core.base.implementations.di_container.isinstance', return_value=True):
                # Közvetlenül hívjuk meg a _get_storage metódust
                result = factory._get_storage()
        
        assert result is not None
        assert result is mock_storage

    def test_expensive_config_lazy_property(self) -> None:
        """Teszteli az _expensive_config lazy property működését (111-114. sorok)."""
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        
        # Mock config manager létrehozása
        mock_config: MagicMock = MagicMock(spec=ConfigManagerInterface)
        mock_config._initialized = True  # Singleton ellenőrzés átugrása
        mock_config.get.return_value = {"test": "config"}
        
        container.register_instance(ConfigManagerInterface, mock_config)
        
        # Mockoljuk a resolve metódust, hogy a container.resolve() működjön
        with patch.object(container, 'resolve', return_value=mock_config):
            # Csak a DIContainer._verify_interface_implementation metódusában mockoljuk az isinstance-t
            def isinstance_mock(obj, class_or_tuple) -> bool:
                if class_or_tuple in [ConfigManagerInterface, StorageInterface]:
                    return True
                return isinstance(obj, class_or_tuple)
            
            with patch('neural_ai.core.base.implementations.di_container.isinstance', side_effect=isinstance_mock):
                factory: CoreComponentFactory = CoreComponentFactory(container)
                
                # Mockoljuk a _config_loader-t, hogy a mock_config-ot adja vissza
                with patch.object(factory, '_config_loader') as mock_loader:
                    mock_loader.return_value = mock_config
                    
                    # Mockoljuk a time.sleep-et, hogy ne várjon
                    with patch('neural_ai.core.base.factory.time.sleep'):
                        # Mockoljuk a _process_config metódust, hogy a config.get() eredményét adja vissza
                        with patch.object(factory, '_process_config', side_effect=lambda x: x):
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
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        from unittest.mock import MagicMock, patch
        
        container: DIContainer = DIContainer()
        
        # Mock config manager létrehozása
        mock_config: MagicMock = MagicMock(spec=ConfigManagerInterface)
        mock_config._initialized = True  # Singleton ellenőrzés átugrása
        mock_config.get.return_value = {"test": "config"}
        
        container.register_instance(ConfigManagerInterface, mock_config)
        
        # Mockoljuk a resolve metódust, hogy a container.resolve() működjön
        with patch.object(container, 'resolve', return_value=mock_config):
            # Csak a DIContainer._verify_interface_implementation metódusában mockoljuk az isinstance-t
            def isinstance_mock(obj, class_or_tuple) -> bool:
                if class_or_tuple in [ConfigManagerInterface, StorageInterface]:
                    return True
                return isinstance(obj, class_or_tuple)
            
            with patch('neural_ai.core.base.implementations.di_container.isinstance', side_effect=isinstance_mock):
                factory: CoreComponentFactory = CoreComponentFactory(container)
                
                # Mockoljuk a _config_loader-t, hogy a mock_config-ot adja vissza
                with patch.object(factory, '_config_loader') as mock_loader:
                    mock_loader.return_value = mock_config
                    
                    # Mockoljuk a time.sleep-et, hogy ne várjon
                    with patch('neural_ai.core.base.factory.time.sleep'):
                        # Mockoljuk a _process_config metódust, hogy a config.get() eredményét adja vissza
                        with patch.object(factory, '_process_config', side_effect=lambda x: x):
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
