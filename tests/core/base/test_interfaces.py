"""Interfész tesztelése a base modulban.

Ez a modul a neural_ai.core.base.interfaces modulban található interfészek
tesztelését végzi.
"""

import inspect
import pytest
from abc import ABC

from neural_ai.core.base.interfaces import (
    DIContainerInterface,
    CoreComponentsInterface,
    CoreComponentFactoryInterface,
    LazyComponentInterface,
)


class TestDIContainerInterface:
    """DIContainerInterface tesztelése."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            DIContainerInterface()  # type: ignore

    def test_interface_has_register_instance_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_instance metódussal."""
        assert hasattr(DIContainerInterface, "register_instance")
        method = getattr(DIContainerInterface, "register_instance")
        assert callable(method)

    def test_register_instance_is_abstract(self) -> None:
        """Teszteli, hogy a register_instance metódus absztrakt."""
        method = getattr(DIContainerInterface, "register_instance")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_register_factory_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_factory metódussal."""
        assert hasattr(DIContainerInterface, "register_factory")
        method = getattr(DIContainerInterface, "register_factory")
        assert callable(method)

    def test_register_factory_is_abstract(self) -> None:
        """Teszteli, hogy a register_factory metódus absztrakt."""
        method = getattr(DIContainerInterface, "register_factory")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_resolve_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik resolve metódussal."""
        assert hasattr(DIContainerInterface, "resolve")
        method = getattr(DIContainerInterface, "resolve")
        assert callable(method)

    def test_resolve_is_abstract(self) -> None:
        """Teszteli, hogy a resolve metódus absztrakt."""
        method = getattr(DIContainerInterface, "resolve")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_register_lazy_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik register_lazy metódussal."""
        assert hasattr(DIContainerInterface, "register_lazy")
        method = getattr(DIContainerInterface, "register_lazy")
        assert callable(method)

    def test_register_lazy_is_abstract(self) -> None:
        """Teszteli, hogy a register_lazy metódus absztrakt."""
        method = getattr(DIContainerInterface, "register_lazy")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_get_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik get metódussal."""
        assert hasattr(DIContainerInterface, "get")
        method = getattr(DIContainerInterface, "get")
        assert callable(method)

    def test_get_is_abstract(self) -> None:
        """Teszteli, hogy a get metódus absztrakt."""
        method = getattr(DIContainerInterface, "get")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_clear_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik clear metódussal."""
        assert hasattr(DIContainerInterface, "clear")
        method = getattr(DIContainerInterface, "clear")
        assert callable(method)

    def test_clear_is_abstract(self) -> None:
        """Teszteli, hogy a clear metódus absztrakt."""
        method = getattr(DIContainerInterface, "clear")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True


class TestCoreComponentsInterface:
    """CoreComponentsInterface tesztelése."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            CoreComponentsInterface()  # type: ignore

    def test_interface_has_config_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik config property-vel."""
        assert hasattr(CoreComponentsInterface, "config")
        prop = getattr(CoreComponentsInterface, "config")
        assert isinstance(prop, property)

    def test_config_property_is_abstract(self) -> None:
        """Teszteli, hogy a config property absztrakt."""
        prop = getattr(CoreComponentsInterface, "config")
        assert hasattr(prop.fget, "__isabstractmethod__")
        assert prop.fget.__isabstractmethod__ is True

    def test_interface_has_logger_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik logger property-vel."""
        assert hasattr(CoreComponentsInterface, "logger")
        prop = getattr(CoreComponentsInterface, "logger")
        assert isinstance(prop, property)

    def test_logger_property_is_abstract(self) -> None:
        """Teszteli, hogy a logger property absztrakt."""
        prop = getattr(CoreComponentsInterface, "logger")
        assert hasattr(prop.fget, "__isabstractmethod__")
        assert prop.fget.__isabstractmethod__ is True

    def test_interface_has_storage_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik storage property-vel."""
        assert hasattr(CoreComponentsInterface, "storage")
        prop = getattr(CoreComponentsInterface, "storage")
        assert isinstance(prop, property)

    def test_storage_property_is_abstract(self) -> None:
        """Teszteli, hogy a storage property absztrakt."""
        prop = getattr(CoreComponentsInterface, "storage")
        assert hasattr(prop.fget, "__isabstractmethod__")
        assert prop.fget.__isabstractmethod__ is True

    def test_interface_has_has_config_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_config metódussal."""
        assert hasattr(CoreComponentsInterface, "has_config")
        method = getattr(CoreComponentsInterface, "has_config")
        assert callable(method)

    def test_has_config_is_abstract(self) -> None:
        """Teszteli, hogy a has_config metódus absztrakt."""
        method = getattr(CoreComponentsInterface, "has_config")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_has_logger_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_logger metódussal."""
        assert hasattr(CoreComponentsInterface, "has_logger")
        method = getattr(CoreComponentsInterface, "has_logger")
        assert callable(method)

    def test_has_logger_is_abstract(self) -> None:
        """Teszteli, hogy a has_logger metódus absztrakt."""
        method = getattr(CoreComponentsInterface, "has_logger")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_has_storage_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik has_storage metódussal."""
        assert hasattr(CoreComponentsInterface, "has_storage")
        method = getattr(CoreComponentsInterface, "has_storage")
        assert callable(method)

    def test_has_storage_is_abstract(self) -> None:
        """Teszteli, hogy a has_storage metódus absztrakt."""
        method = getattr(CoreComponentsInterface, "has_storage")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_validate_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik validate metódussal."""
        assert hasattr(CoreComponentsInterface, "validate")
        method = getattr(CoreComponentsInterface, "validate")
        assert callable(method)

    def test_validate_is_abstract(self) -> None:
        """Teszteli, hogy a validate metódus absztrakt."""
        method = getattr(CoreComponentsInterface, "validate")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True


class TestCoreComponentFactoryInterface:
    """CoreComponentFactoryInterface tesztelése."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            CoreComponentFactoryInterface()  # type: ignore

    def test_interface_has_create_components_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_components metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_components")
        method = getattr(CoreComponentFactoryInterface, "create_components")
        assert callable(method)

    def test_create_components_is_abstract(self) -> None:
        """Teszteli, hogy a create_components metódus absztrakt."""
        method = getattr(CoreComponentFactoryInterface, "create_components")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_create_components_is_static(self) -> None:
        """Teszteli, hogy a create_components metódus statikus."""
        assert isinstance(inspect.getattr_static(CoreComponentFactoryInterface, "create_components"), staticmethod)

    def test_interface_has_create_with_container_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_with_container metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_with_container")
        method = getattr(CoreComponentFactoryInterface, "create_with_container")
        assert callable(method)

    def test_create_with_container_is_abstract(self) -> None:
        """Teszteli, hogy a create_with_container metódus absztrakt."""
        method = getattr(CoreComponentFactoryInterface, "create_with_container")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_create_with_container_is_static(self) -> None:
        """Teszteli, hogy a create_with_container metódus statikus."""
        assert isinstance(inspect.getattr_static(CoreComponentFactoryInterface, "create_with_container"), staticmethod)

    def test_interface_has_create_minimal_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik create_minimal metódussal."""
        assert hasattr(CoreComponentFactoryInterface, "create_minimal")
        method = getattr(CoreComponentFactoryInterface, "create_minimal")
        assert callable(method)

    def test_create_minimal_is_abstract(self) -> None:
        """Teszteli, hogy a create_minimal metódus absztrakt."""
        method = getattr(CoreComponentFactoryInterface, "create_minimal")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_create_minimal_is_static(self) -> None:
        """Teszteli, hogy a create_minimal metódus statikus."""
        assert isinstance(inspect.getattr_static(CoreComponentFactoryInterface, "create_minimal"), staticmethod)


class TestLazyComponentInterface:
    """LazyComponentInterface tesztelése."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész absztrakt."""
        with pytest.raises(TypeError):
            LazyComponentInterface()  # type: ignore

    def test_interface_has_get_method(self) -> None:
        """Teszteli, hogy az interfész rendelkezik get metódussal."""
        assert hasattr(LazyComponentInterface, "get")
        method = getattr(LazyComponentInterface, "get")
        assert callable(method)

    def test_get_is_abstract(self) -> None:
        """Teszteli, hogy a get metódus absztrakt."""
        method = getattr(LazyComponentInterface, "get")
        assert hasattr(method, "__isabstractmethod__")
        assert method.__isabstractmethod__ is True

    def test_interface_has_is_loaded_property(self) -> None:
        """Teszteli, hogy az interfész rendelkezik is_loaded property-vel."""
        assert hasattr(LazyComponentInterface, "is_loaded")
        prop = getattr(LazyComponentInterface, "is_loaded")
        assert isinstance(prop, property)

    def test_is_loaded_property_is_abstract(self) -> None:
        """Teszteli, hogy a is_loaded property absztrakt."""
        prop = getattr(LazyComponentInterface, "is_loaded")
        assert hasattr(prop.fget, "__isabstractmethod__")
        assert prop.fget.__isabstractmethod__ is True


class TestInterfacesIntegration:
    """Interfészek integrációs tesztelése."""

    def test_all_interfaces_are_abc(self) -> None:
        """Teszteli, hogy minden interfész ABC."""
        interfaces: list[type[ABC]] = [
            DIContainerInterface,
            CoreComponentsInterface,
            CoreComponentFactoryInterface,
            LazyComponentInterface,
        ]
        for interface in interfaces:
            assert issubclass(interface, ABC), f"{interface.__name__} should be a subclass of ABC"

    def test_interfaces_have_proper_method_signatures(self) -> None:
        """Teszteli, hogy az interfészek metódusainak megfelelő a szignatúrájuk."""
        # DIContainerInterface ellenőrzése
        assert hasattr(DIContainerInterface, "__annotations__")
        
        # CoreComponentsInterface ellenőrzése
        assert hasattr(CoreComponentsInterface, "__annotations__")
        
        # CoreComponentFactoryInterface ellenőrzése
        assert hasattr(CoreComponentFactoryInterface, "__annotations__")
        
        # LazyComponentInterface ellenőrzése
        assert hasattr(LazyComponentInterface, "__annotations__")

