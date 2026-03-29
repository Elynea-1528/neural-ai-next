"""Unit tesztek a neural_ai.core.system.__init__ modulhoz."""

import neural_ai.core.system as system_module
from neural_ai.core.system.factory import SystemComponentFactory
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
    SystemHealth,
)


class TestSystemInit:
    """Tesztek a system __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(system_module, "__all__")
        assert isinstance(system_module.__all__, list)

    def test_all_exports_system_component_factory(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a SystemComponentFactory-t."""
        assert "SystemComponentFactory" in system_module.__all__

    def test_all_exports_health_monitor_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthMonitorInterface-t."""
        assert "HealthMonitorInterface" in system_module.__all__

    def test_all_exports_health_check_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthCheckInterface-t."""
        assert "HealthCheckInterface" in system_module.__all__

    def test_all_exports_component_health(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a ComponentHealth-t."""
        assert "ComponentHealth" in system_module.__all__

    def test_all_exports_component_status(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a ComponentStatus-t."""
        assert "ComponentStatus" in system_module.__all__

    def test_all_exports_health_status(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthStatus-t."""
        assert "HealthStatus" in system_module.__all__

    def test_all_exports_system_health(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a SystemHealth-t."""
        assert "SystemHealth" in system_module.__all__

    def test_system_component_factory_is_correct_class(self) -> None:
        """Teszteli, hogy a SystemComponentFactory a helyes osztály."""
        assert system_module.SystemComponentFactory is SystemComponentFactory

    def test_health_monitor_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthMonitorInterface a helyes osztály."""
        assert system_module.HealthMonitorInterface is HealthMonitorInterface

    def test_health_check_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthCheckInterface a helyes osztály."""
        assert system_module.HealthCheckInterface is HealthCheckInterface

    def test_component_health_is_correct_class(self) -> None:
        """Teszteli, hogy a ComponentHealth a helyes osztály."""
        assert system_module.ComponentHealth is ComponentHealth

    def test_component_status_is_correct_class(self) -> None:
        """Teszteli, hogy a ComponentStatus a helyes osztály."""
        assert system_module.ComponentStatus is ComponentStatus

    def test_health_status_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthStatus a helyes osztály."""
        assert system_module.HealthStatus is HealthStatus

    def test_system_health_is_correct_class(self) -> None:
        """Teszteli, hogy a SystemHealth a helyes osztály."""
        assert system_module.SystemHealth is SystemHealth

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert system_module.__doc__ is not None
        assert len(system_module.__doc__) > 0

    def test_docstring_mentions_system(self) -> None:
        """Teszteli, hogy a docstring említi a rendszer komponenseket."""
        assert system_module.__doc__ is not None
        assert "rendszer" in system_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in system_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in system_module.__all__:
            assert hasattr(system_module, name)

    def test_health_monitor_interface_is_abstract(self) -> None:
        """Teszteli, hogy a HealthMonitorInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(system_module.HealthMonitorInterface, ABCMeta)

    def test_health_check_interface_is_abstract(self) -> None:
        """Teszteli, hogy a HealthCheckInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(system_module.HealthCheckInterface, ABCMeta)

    def test_component_status_is_enum(self) -> None:
        """Teszteli, hogy a ComponentStatus enum."""
        from enum import Enum

        assert issubclass(system_module.ComponentStatus, Enum)

    def test_health_status_is_enum(self) -> None:
        """Teszteli, hogy a HealthStatus enum."""
        from enum import Enum

        assert issubclass(system_module.HealthStatus, Enum)

    def test_all_count(self) -> None:
        """Teszteli, hogy az __all__ 7 elemet tartalmaz."""
        assert len(system_module.__all__) == 7
