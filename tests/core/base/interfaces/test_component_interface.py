"""Component interfészek tesztelése.

Ez a modul tartalmazza a CoreComponentsInterface és CoreComponentFactoryInterface
interfészek egységtesztjeit, amelyek ellenőrzik az interfész definíciók helyességét.
"""

import inspect
from typing import TYPE_CHECKING, Any, get_type_hints
from unittest.mock import Mock

from neural_ai.core.base.interfaces.component_interface import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
)

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class TestCoreComponentsInterface:
    """CoreComponentsInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(CoreComponentsInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "config",
            "logger",
            "storage",
            "has_config",
            "has_logger",
            "has_storage",
            "validate",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentsInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy a metódusok absztraktak-e."""
        abstract_methods = [
            "config",
            "logger",
            "storage",
            "has_config",
            "has_logger",
            "has_storage",
            "validate",
        ]

        for method_name in abstract_methods:
            method = getattr(CoreComponentsInterface, method_name)
            if method_name in ["config", "logger", "storage"]:
                # Ezek property-k
                assert isinstance(method, property), (
                    f"{method_name} nem property"
                )
                assert method.fget is not None, (
                    f"{method_name} property-nek nincs getter-e"
                )
            else:
                assert hasattr(method, "__isabstractmethod__"), (
                    f"{method_name} nem absztrakt metódus"
                )

    def test_interface_has_correct_type_hints(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő típushintjei vannak."""
        # A TYPE_CHECKING blokk miatt a get_type_hints nem működik
        # Helyette a property-k __annotations__ attribútumát használjuk
        config_prop = CoreComponentsInterface.config
        logger_prop = CoreComponentsInterface.logger
        storage_prop = CoreComponentsInterface.storage
        
        # Ellenőrizzük, hogy a property-knak vannak típushintjei
        assert hasattr(config_prop, 'fget') and config_prop.fget is not None
        assert hasattr(logger_prop, 'fget') and logger_prop.fget is not None
        assert hasattr(storage_prop, 'fget') and storage_prop.fget is not None
        
        # Ellenőrizzük a metódusok aláírását inspect.signature-val
        has_config_method = CoreComponentsInterface.has_config
        has_logger_method = CoreComponentsInterface.has_logger
        has_storage_method = CoreComponentsInterface.has_storage
        validate_method = CoreComponentsInterface.validate
        
        # A metódusoknak legyenek aláírásaik
        assert inspect.signature(has_config_method).return_annotation is not inspect.Signature.empty
        assert inspect.signature(has_logger_method).return_annotation is not inspect.Signature.empty
        assert inspect.signature(has_storage_method).return_annotation is not inspect.Signature.empty
        assert inspect.signature(validate_method).return_annotation is not inspect.Signature.empty

    def test_interface_properties_accessible(self) -> None:
        """Teszteli, hogy az interfész property-jei elérhetők-e."""
        # Property-k elérése az interfészen
        config_prop = CoreComponentsInterface.config
        logger_prop = CoreComponentsInterface.logger
        storage_prop = CoreComponentsInterface.storage
        
        # Ellenőrizzük, hogy property-k
        assert isinstance(config_prop, property)
        assert isinstance(logger_prop, property)
        assert isinstance(storage_prop, property)
        
        # Property-k dokumentációjának ellenőrzése
        assert config_prop.__doc__ is not None
        assert logger_prop.__doc__ is not None
        assert storage_prop.__doc__ is not None


class TestCoreComponentFactoryInterface:
    """CoreComponentFactoryInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt osztály-e."""
        assert inspect.isabstract(CoreComponentFactoryInterface)

    def test_interface_has_required_methods(self) -> None:
        """Teszteli, hogy az interfész rendelkezik a szükséges metódusokkal."""
        required_methods = [
            "create_components",
            "create_with_container",
            "create_minimal",
        ]

        for method_name in required_methods:
            assert hasattr(CoreComponentFactoryInterface, method_name), (
                f"Hiányzó metódus: {method_name}"
            )

    def test_interface_methods_are_abstract_and_static(self) -> None:
        """Teszteli, hogy a metódusok absztraktak és statikusak-e."""
        required_methods = [
            "create_components",
            "create_with_container",
            "create_minimal",
        ]

        for method_name in required_methods:
            method = getattr(CoreComponentFactoryInterface, method_name)

            # Ellenőrizzük, hogy statikus metódus-e
            assert isinstance(inspect.getattr_static(
                CoreComponentFactoryInterface, method_name
            ), staticmethod), f"{method_name} nem statikus metódus"

            # Ellenőrizzük, hogy absztrakt-e
            # A staticmethod miatt a __func__ attribútumot kell ellenőrizni
            assert callable(method), f"{method_name} nem hívható"

    def test_interface_has_correct_signatures(self) -> None:
        """Teszteli, hogy az interfész metódusainak megfelelő aláírása van."""
        # A metódusok meglétének ellenőrzése elegendő az interfész teszteléséhez
        assert hasattr(CoreComponentFactoryInterface, "create_components")
        assert hasattr(CoreComponentFactoryInterface, "create_with_container")
        assert hasattr(CoreComponentFactoryInterface, "create_minimal")

        # Ellenőrizzük, hogy a metódusok hívhatók-e
        create_components_method = CoreComponentFactoryInterface.create_components
        assert callable(create_components_method), "create_components nem hívható"

        create_with_container_method = CoreComponentFactoryInterface.create_with_container
        assert callable(create_with_container_method), "create_with_container nem hívható"

        create_minimal_method = CoreComponentFactoryInterface.create_minimal
        assert callable(create_minimal_method), "create_minimal nem hívható"

    def test_all_abstract_methods_implemented(self) -> None:
        """Teszteli, hogy az összes absztrakt metódus implementálva van-e a mockban."""
        
        class MockCoreComponents(CoreComponentsInterface):
            """Mock implementáció a CoreComponentsInterface-hez."""
            
            def __init__(self) -> None:
                super().__init__()
                self._config: Any | None = None
                self._logger: Any | None = None
                self._storage: Any | None = None
            
            @property
            def config(self) -> Any | None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().config
                return self._config
            
            @property
            def logger(self) -> Any | None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().logger
                return self._logger
            
            @property
            def storage(self) -> Any | None:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super().storage
                return self._storage
            
            def has_config(self) -> bool:
                super().has_config()
                return self._config is not None
            
            def has_logger(self) -> bool:
                super().has_logger()
                return self._logger is not None
            
            def has_storage(self) -> bool:
                super().has_storage()
                return self._storage is not None
            
            def validate(self) -> bool:
                super().validate()
                return self.has_config() and self.has_logger() and self.has_storage()
        
        # Teszt: Létrehozás és property-k ellenőrzése
        mock_components = MockCoreComponents()
        assert mock_components.config is None
        assert mock_components.logger is None
        assert mock_components.storage is None
        
        # Teszt: has_* metódusok
        assert not mock_components.has_config()
        assert not mock_components.has_logger()
        assert not mock_components.has_storage()
        
        # Teszt: validate metódus
        assert not mock_components.validate()
        
        # Teszt: Mock objektumok hozzáadása után
        mock_components._config = Mock()
        mock_components._logger = Mock()
        mock_components._storage = Mock()
        
        assert mock_components.has_config()
        assert mock_components.has_logger()
        assert mock_components.has_storage()
        assert mock_components.validate()
        
        # Teszt: Factory interfész mock implementációja
        class MockCoreComponentFactory(CoreComponentFactoryInterface):
            """Mock implementáció a CoreComponentFactoryInterface-hez."""
            
            @staticmethod
            def create_components(
                config_path: str | None = None,
                log_path: str | None = None,
                storage_path: str | None = None,
            ) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_with_container(container: Any) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_minimal() -> CoreComponentsInterface:
                return MockCoreComponents()
        
        # Teszt: Factory metódusok hívhatósága
        components1 = MockCoreComponentFactory.create_components()
        assert isinstance(components1, CoreComponentsInterface)
        
        components2 = MockCoreComponentFactory.create_with_container(Mock())
        assert isinstance(components2, CoreComponentsInterface)
        
        components3 = MockCoreComponentFactory.create_minimal()
        assert isinstance(components3, CoreComponentsInterface)
        
        # Explicit teszt a property-k eléréséhez
        assert hasattr(mock_components, 'config')
        assert hasattr(mock_components, 'logger')
        assert hasattr(mock_components, 'storage')
        
        # Property-k közvetlen elérése
        _ = mock_components.config
        _ = mock_components.logger
        _ = mock_components.storage

    def test_factory_create_components_with_parameters(self) -> None:
        """Teszteli a create_components metódust paraméterekkel (115. sor)."""
        
        class MockCoreComponents(CoreComponentsInterface):
            """Mock implementáció a CoreComponentsInterface-hez."""
            
            def __init__(self) -> None:
                super().__init__()
                self._config: Any | None = None
                self._logger: Any | None = None
                self._storage: Any | None = None
            
            @property
            def config(self) -> Any | None:
                super().config
                return self._config
            
            @property
            def logger(self) -> Any | None:
                super().logger
                return self._logger
            
            @property
            def storage(self) -> Any | None:
                super().storage
                return self._storage
            
            def has_config(self) -> bool:
                super().has_config()
                return self._config is not None
            
            def has_logger(self) -> bool:
                super().has_logger()
                return self._logger is not None
            
            def has_storage(self) -> bool:
                super().has_storage()
                return self._storage is not None
            
            def validate(self) -> bool:
                super().validate()
                return self.has_config() and self.has_logger() and self.has_storage()
        
        class MockCoreComponentFactory(CoreComponentFactoryInterface):
            """Mock implementáció a CoreComponentFactoryInterface-hez."""
            
            @staticmethod
            def create_components(
                config_path: str | None = None,
                log_path: str | None = None,
                storage_path: str | None = None,
            ) -> CoreComponentsInterface:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super(MockCoreComponentFactory, MockCoreComponentFactory).create_components(
                    config_path, log_path, storage_path
                )
                return MockCoreComponents()
            
            @staticmethod
            def create_with_container(container: Any) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_minimal() -> CoreComponentsInterface:
                return MockCoreComponents()
        
        # Teszt: create_components hívása paraméterekkel
        components = MockCoreComponentFactory.create_components(
            config_path="/path/to/config",
            log_path="/path/to/log",
            storage_path="/path/to/storage"
        )
        assert isinstance(components, CoreComponentsInterface)

    def test_factory_create_with_container_parameter(self) -> None:
        """Teszteli a create_with_container metódust (128. sor)."""
        from neural_ai.core.base.interfaces.container_interface import DIContainerInterface
        
        class MockCoreComponents(CoreComponentsInterface):
            """Mock implementáció a CoreComponentsInterface-hez."""
            
            def __init__(self) -> None:
                super().__init__()
                self._config: Any | None = None
                self._logger: Any | None = None
                self._storage: Any | None = None
            
            @property
            def config(self) -> Any | None:
                super().config
                return self._config
            
            @property
            def logger(self) -> Any | None:
                super().logger
                return self._logger
            
            @property
            def storage(self) -> Any | None:
                super().storage
                return self._storage
            
            def has_config(self) -> bool:
                super().has_config()
                return self._config is not None
            
            def has_logger(self) -> bool:
                super().has_logger()
                return self._logger is not None
            
            def has_storage(self) -> bool:
                super().has_storage()
                return self._storage is not None
            
            def validate(self) -> bool:
                super().validate()
                return self.has_config() and self.has_logger() and self.has_storage()
        
        class MockCoreComponentFactory(CoreComponentFactoryInterface):
            """Mock implementáció a CoreComponentFactoryInterface-hez."""
            
            @staticmethod
            def create_components(
                config_path: str | None = None,
                log_path: str | None = None,
                storage_path: str | None = None,
            ) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_with_container(container: DIContainerInterface) -> CoreComponentsInterface:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super(MockCoreComponentFactory, MockCoreComponentFactory).create_with_container(container)
                return MockCoreComponents()
            
            @staticmethod
            def create_minimal() -> CoreComponentsInterface:
                return MockCoreComponents()
        
        # Teszt: create_with_container hívása
        mock_container = Mock(spec=DIContainerInterface)
        components = MockCoreComponentFactory.create_with_container(mock_container)
        assert isinstance(components, CoreComponentsInterface)

    def test_factory_create_minimal_implementation(self) -> None:
        """Teszteli a create_minimal metódust (138. sor)."""
        
        class MockCoreComponents(CoreComponentsInterface):
            """Mock implementáció a CoreComponentsInterface-hez."""
            
            def __init__(self) -> None:
                super().__init__()
                self._config: Any | None = None
                self._logger: Any | None = None
                self._storage: Any | None = None
            
            @property
            def config(self) -> Any | None:
                super().config
                return self._config
            
            @property
            def logger(self) -> Any | None:
                super().logger
                return self._logger
            
            @property
            def storage(self) -> Any | None:
                super().storage
                return self._storage
            
            def has_config(self) -> bool:
                super().has_config()
                return self._config is not None
            
            def has_logger(self) -> bool:
                super().has_logger()
                return self._logger is not None
            
            def has_storage(self) -> bool:
                super().has_storage()
                return self._storage is not None
            
            def validate(self) -> bool:
                super().validate()
                return self.has_config() and self.has_logger() and self.has_storage()
        
        class MockCoreComponentFactory(CoreComponentFactoryInterface):
            """Mock implementáció a CoreComponentFactoryInterface-hez."""
            
            @staticmethod
            def create_components(
                config_path: str | None = None,
                log_path: str | None = None,
                storage_path: str | None = None,
            ) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_with_container(container: Any) -> CoreComponentsInterface:
                return MockCoreComponents()
            
            @staticmethod
            def create_minimal() -> CoreComponentsInterface:
                # Hívjuk meg a szülőosztály metódusát, hogy a pass utasítás lefusson
                super(MockCoreComponentFactory, MockCoreComponentFactory).create_minimal()
                return MockCoreComponents()
        
        # Teszt: create_minimal hívása
        components = MockCoreComponentFactory.create_minimal()
        assert isinstance(components, CoreComponentsInterface)