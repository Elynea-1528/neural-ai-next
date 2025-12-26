"""Interfaces modul tesztjei.

Ez a modul tartalmazza a neural_ai.core.base.interfaces modul
egységtesztjeit.
"""

import inspect
from abc import ABC

import pytest

from neural_ai.core.base.interfaces import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface,
    DIContainerInterface,
    LazyComponentInterface,
)


class TestDIContainerInterface:
    """DIContainerInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt-e."""
        with pytest.raises(TypeError):
            DIContainerInterface()  # type: ignore

    def test_interface_has_register_instance_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_instance metódussal."""
        assert hasattr(DIContainerInterface, "register_instance")
        method = DIContainerInterface.register_instance
        assert callable(method)

    def test_interface_has_register_factory_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_factory metódussal."""
        assert hasattr(DIContainerInterface, "register_factory")
        method = DIContainerInterface.register_factory
        assert callable(method)

    def test_interface_has_resolve_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik resolve metódussal."""
        assert hasattr(DIContainerInterface, "resolve")
        method = DIContainerInterface.resolve
        assert callable(method)

    def test_interface_has_register_lazy_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_lazy metódussal."""
        assert hasattr(DIContainerInterface, "register_lazy")
        method = DIContainerInterface.register_lazy
        assert callable(method)

    def test_interface_has_get_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik get metódussal."""
        assert hasattr(DIContainerInterface, "get")
        method = DIContainerInterface.get
        assert callable(method)

    def test_interface_has_clear_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik clear metódussal."""
        assert hasattr(DIContainerInterface, "clear")
        method = DIContainerInterface.clear
        assert callable(method)


class TestCoreComponentsInterface:
    """CoreComponentsInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt-e."""
        with pytest.raises(TypeError):
            CoreComponentsInterface()  # type: ignore

    def test_interface_has_config_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik config property-vel."""
        assert hasattr(CoreComponentsInterface, "config")
        # Property ellenőrzése
        assert isinstance(CoreComponentsInterface.config, property)

    def test_interface_has_logger_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik logger property-vel."""
        assert hasattr(CoreComponentsInterface, "logger")
        assert isinstance(CoreComponentsInterface.logger, property)

    def test_interface_has_storage_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik storage property-vel."""
        assert hasattr(CoreComponentsInterface, "storage")
        assert isinstance(CoreComponentsInterface.storage, property)

    def test_interface_has_has_config_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_config metódussal."""
        assert hasattr(CoreComponentsInterface, "has_config")
        method = CoreComponentsInterface.has_config
        assert callable(method)

    def test_interface_has_has_logger_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_logger metódussal."""
        assert hasattr(CoreComponentsInterface, "has_logger")
        method = CoreComponentsInterface.has_logger
        assert callable(method)

    def test_interface_has_has_storage_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_storage metódussal."""
        assert hasattr(CoreComponentsInterface, "has_storage")
        method = CoreComponentsInterface.has_storage
        assert callable(method)

    def test_interface_has_validate_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik validate metódussal."""
        assert hasattr(CoreComponentsInterface, "validate")
        method = CoreComponentsInterface.validate
        assert callable(method)


class TestCoreComponentFactoryInterface:
    """CoreComponentFactoryInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt-e."""
        with pytest.raises(TypeError):
            CoreComponentFactoryInterface()  # type: ignore

    def test_interface_has_create_components_static_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_components statikus metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_components")
        method = CoreComponentFactoryInterface.create_components
        assert callable(method)
        # Statikus metódus ellenőrzése
        assert isinstance(
            inspect.getattr_static(CoreComponentFactoryInterface, "create_components"), staticmethod
        )

    def test_interface_has_create_with_container_static_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_with_container statikus metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_with_container")
        method = CoreComponentFactoryInterface.create_with_container
        assert callable(method)
        # Statikus metódus ellenőrzése
        assert isinstance(
            inspect.getattr_static(CoreComponentFactoryInterface, "create_with_container"),
            staticmethod,
        )

    def test_interface_has_create_minimal_static_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_minimal statikus metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_minimal")
        method = CoreComponentFactoryInterface.create_minimal
        assert callable(method)
        # Statikus metódus ellenőrzése
        assert isinstance(
            inspect.getattr_static(CoreComponentFactoryInterface, "create_minimal"), staticmethod
        )


class TestLazyComponentInterface:
    """LazyComponentInterface interfész tesztjei."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt-e."""
        with pytest.raises(TypeError):
            LazyComponentInterface()  # type: ignore

    def test_interface_has_get_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik get metódussal."""
        assert hasattr(LazyComponentInterface, "get")
        method = LazyComponentInterface.get
        assert callable(method)

    def test_interface_has_is_loaded_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik is_loaded property-vel."""
        assert hasattr(LazyComponentInterface, "is_loaded")
        assert isinstance(LazyComponentInterface.is_loaded, property)


class TestInterfacesIntegration:
    """Interfészek integrációs tesztjei."""

    def test_all_interfaces_are_abc_subclasses(self) -> None:
        """Teszteli, hogy minden interfész ABC leszármazott."""
        interfaces: list[type] = [
            DIContainerInterface,
            CoreComponentsInterface,
            CoreComponentFactoryInterface,
            LazyComponentInterface,
        ]
        for interface in interfaces:
            assert issubclass(interface, ABC), f"{interface.__name__} nem ABC leszármazott"

    def test_all_interface_methods_are_abstract(self) -> None:
        """Teszteli, hogy minden interfész metódus absztrakt."""
        interfaces: list[type] = [
            DIContainerInterface,
            CoreComponentsInterface,
            CoreComponentFactoryInterface,
            LazyComponentInterface,
        ]

        for interface in interfaces:
            for name in dir(interface):
                if name.startswith("_"):
                    continue
                attr = getattr(interface, name)
                if callable(attr):
                    # Abstract method check
                    assert hasattr(attr, "__isabstractmethod__"), (
                        f"{interface.__name__}.{name} nem absztrakt metódus"
                    )

    def test_interface_method_signatures(self) -> None:
        """Teszteli az interfész metódusok aláírásait és docstringjeit."""
        interfaces: list[type] = [
            DIContainerInterface,
            CoreComponentsInterface,
            CoreComponentFactoryInterface,
            LazyComponentInterface,
        ]

        for interface in interfaces:
            for name in dir(interface):
                if name.startswith("_"):
                    continue
                attr = getattr(interface, name)
                if callable(attr):
                    # Docstring ellenőrzése
                    assert attr.__doc__ is not None, (
                        f"{interface.__name__}.{name} metódusnak nincs docstringje"
                    )
                    assert len(attr.__doc__.strip()) > 0, (
                        f"{interface.__name__}.{name} metódus docstringje üres"
                    )
                    # Signature ellenőrzése
                    sig = inspect.signature(attr)
                    assert sig is not None, (
                        f"{interface.__name__}.{name} metódusnak nincs signature-je"
                    )


class TestInterfacesImplementation:
    """Interfészek implementációs tesztjei a 100% coverage eléréséhez."""

    def test_di_container_implementation(self) -> None:
        """Teszteli a DIContainerInterface implementációját."""

        class ConcreteDIContainer(DIContainerInterface):
            """Konkrét DI konténer implementáció."""

            def __init__(self) -> None:
                self.instances: dict[object, object] = {}
                self.factories: dict[object, object] = {}
                self.lazy_components: dict[str, object] = {}

            def register_instance(self, interface: object, instance: object) -> None:
                self.instances[interface] = instance

            def register_factory(self, interface: object, factory: object) -> None:
                self.factories[interface] = factory

            def resolve(self, interface: object) -> object | None:  # type: ignore
                return self.instances.get(interface)

            def register_lazy(self, component_name: str, factory_func: object) -> None:
                self.lazy_components[component_name] = factory_func

            def get(self, component_name: str) -> object:
                factory = self.lazy_components.get(component_name)
                if factory and callable(factory):
                    return factory()
                raise KeyError(f"Component {component_name} not found")

            def clear(self) -> None:
                self.instances.clear()
                self.factories.clear()
                self.lazy_components.clear()

        container = ConcreteDIContainer()

        # Teszt: register_instance
        test_instance = "test"
        container.register_instance(str, test_instance)
        assert container.resolve(str) == test_instance

        # Teszt: register_factory
        def factory() -> str:
            return "from_factory"

        container.register_factory(int, factory)

        # Teszt: register_lazy és get
        def lazy_factory() -> str:
            return "lazy_loaded"

        container.register_lazy("lazy_test", lazy_factory)
        assert container.get("lazy_test") == "lazy_loaded"

        # Teszt: clear
        container.clear()
        assert container.resolve(str) is None
        with pytest.raises(KeyError):
            container.get("lazy_test")

        # Property-k használata a coverage érdekében
        assert hasattr(container, "instances")
        assert hasattr(container, "factories")
        assert hasattr(container, "lazy_components")

        # Factory metódus meghívása a coverage érdekében
        factory_result = container.resolve(int)
        assert factory_result is None  # Nincs regisztrálva factory

    def test_core_components_implementation(self) -> None:
        """Teszteli a CoreComponentsInterface implementációját."""

        # Mock interfészek a teszteléshez
        class MockConfig:
            pass

        class MockLogger:
            pass

        class MockStorage:
            pass

        class ConcreteCoreComponents(CoreComponentsInterface):
            """Konkrét core komponensek implementáció."""

            def __init__(
                self,
                config: MockConfig | None = None,
                logger: MockLogger | None = None,
                storage: MockStorage | None = None,
            ) -> None:
                self._config = config
                self._logger = logger
                self._storage = storage

            @property
            def config(self) -> MockConfig | None:  # type: ignore
                return self._config

            @property
            def logger(self) -> MockLogger | None:  # type: ignore
                return self._logger

            @property
            def storage(self) -> MockStorage | None:  # type: ignore
                return self._storage

            def has_config(self) -> bool:
                return self._config is not None

            def has_logger(self) -> bool:
                return self._logger is not None

            def has_storage(self) -> bool:
                return self._storage is not None

            def validate(self) -> bool:
                return self.has_config() and self.has_logger() and self.has_storage()

        # Teszt: Üres komponensek
        empty_components = ConcreteCoreComponents()
        assert empty_components.config is None
        assert empty_components.logger is None
        assert empty_components.storage is None
        assert not empty_components.has_config()
        assert not empty_components.has_logger()
        assert not empty_components.has_storage()
        assert not empty_components.validate()

        # Teszt: Teljes komponensek
        mock_config = MockConfig()
        mock_logger = MockLogger()
        mock_storage = MockStorage()
        full_components = ConcreteCoreComponents(
            config=mock_config, logger=mock_logger, storage=mock_storage
        )
        assert full_components.config is mock_config
        assert full_components.logger is mock_logger
        assert full_components.storage is mock_storage
        assert full_components.has_config()
        assert full_components.has_logger()
        assert full_components.has_storage()
        assert full_components.validate()

    def test_lazy_component_implementation(self) -> None:
        """Teszteli a LazyComponentInterface implementációját."""

        class ConcreteLazyComponent(LazyComponentInterface):
            """Konkrét lusta komponens implementáció."""

            def __init__(self, factory_func: object) -> None:
                self._factory_func = factory_func
                self._loaded = False
                self._instance: object | None = None

            @property
            def is_loaded(self) -> bool:
                return self._loaded

            def get(self) -> object:
                if not self._loaded:
                    if callable(self._factory_func):
                        self._instance = self._factory_func()
                    self._loaded = True
                return self._instance

        # Teszt: Lusta betöltés
        def create_heavy_object() -> str:
            return "heavy_object_data"

        lazy_component = ConcreteLazyComponent(create_heavy_object)

        # Kezdetben nincs betöltve
        assert not lazy_component.is_loaded

        # Első hozzáféréskor betöltődik
        result = lazy_component.get()
        assert result == "heavy_object_data"
        assert lazy_component.is_loaded

        # Második hozzáféréskor már nem hívódik meg a factory
        result2 = lazy_component.get()
        assert result2 == result

    def test_core_component_factory_implementation(self) -> None:
        """Teszteli a CoreComponentFactoryInterface implementációját."""

        # Mock osztályok a teszteléshez
        class MockComponents(CoreComponentsInterface):
            """Mock komponensek."""

            def __init__(self) -> None:
                self._config = None
                self._logger = None
                self._storage = None

            @property
            def config(self) -> None:  # type: ignore
                return self._config

            @property
            def logger(self) -> None:  # type: ignore
                return self._logger

            @property
            def storage(self) -> None:  # type: ignore
                return self._storage

            def has_config(self) -> bool:
                return False

            def has_logger(self) -> bool:
                return False

            def has_storage(self) -> bool:
                return False

            def validate(self) -> bool:
                return False

        class MockContainer(DIContainerInterface):
            """Mock DI konténer."""

            def __init__(self) -> None:
                self.instances: dict[object, object] = {}
                self.factories: dict[object, object] = {}
                self.lazy_components: dict[str, object] = {}

            def register_instance(self, interface: object, instance: object) -> None:
                self.instances[interface] = instance

            def register_factory(self, interface: object, factory: object) -> None:
                self.factories[interface] = factory

            def resolve(self, interface: object) -> object | None:  # type: ignore
                return self.instances.get(interface)

            def register_lazy(self, component_name: str, factory_func: object) -> None:
                self.lazy_components[component_name] = factory_func

            def get(self, component_name: str) -> object:
                factory = self.lazy_components.get(component_name)
                if factory and callable(factory):
                    return factory()
                raise KeyError(f"Component {component_name} not found")

            def clear(self) -> None:
                self.instances.clear()
                self.factories.clear()
                self.lazy_components.clear()

        class ConcreteCoreComponentFactory(CoreComponentFactoryInterface):
            """Konkrét core komponens factory implementáció."""

            @staticmethod
            def create_components(
                config_path: str | None = None,
                log_path: str | None = None,
                storage_path: str | None = None,
            ) -> CoreComponentsInterface:
                """Core komponensek létrehozása és inicializálása."""
                return MockComponents()

            @staticmethod
            def create_with_container(container: DIContainerInterface) -> CoreComponentsInterface:
                """Core komponensek létrehozása meglévő konténerből."""
                return MockComponents()

            @staticmethod
            def create_minimal() -> CoreComponentsInterface:
                """Minimális core komponens készlet létrehozása."""
                return MockComponents()

        factory = ConcreteCoreComponentFactory()
        mock_container = MockContainer()

        # Teszt: create_components
        components1 = factory.create_components(
            config_path="test_config.yaml", log_path="test_log.txt", storage_path="test_storage"
        )
        assert isinstance(components1, CoreComponentsInterface)

        # Teszt: create_with_container
        components2 = factory.create_with_container(mock_container)
        assert isinstance(components2, CoreComponentsInterface)

        # Teszt: create_minimal
        components3 = factory.create_minimal()
        assert isinstance(components3, CoreComponentsInterface)

        # Teszt: Statikus metódusok hívása az interfészen keresztül
        components4 = ConcreteCoreComponentFactory.create_components()
        assert isinstance(components4, CoreComponentsInterface)

        components5 = ConcreteCoreComponentFactory.create_with_container(mock_container)
        assert isinstance(components5, CoreComponentsInterface)

        components6 = ConcreteCoreComponentFactory.create_minimal()
        assert isinstance(components6, CoreComponentsInterface)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
