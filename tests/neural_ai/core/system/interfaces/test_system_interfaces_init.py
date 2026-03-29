"""Unit tesztek a neural_ai.core.system.interfaces.__init__ modulhoz."""

import neural_ai.core.system.interfaces as interfaces_module
from neural_ai.core.system.interfaces.health_interface import (
    ComponentHealth,
    ComponentStatus,
    HealthCheckInterface,
    HealthMonitorInterface,
    HealthStatus,
    SystemHealth,
)


class TestSystemInterfacesInit:
    """Tesztek a system interfaces __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(interfaces_module, "__all__")
        assert isinstance(interfaces_module.__all__, list)

    def test_all_exports_component_health(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a ComponentHealth-t."""
        assert "ComponentHealth" in interfaces_module.__all__

    def test_all_exports_component_status(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a ComponentStatus-t."""
        assert "ComponentStatus" in interfaces_module.__all__

    def test_all_exports_health_check_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthCheckInterface-t."""
        assert "HealthCheckInterface" in interfaces_module.__all__

    def test_all_exports_health_monitor_interface(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthMonitorInterface-t."""
        assert "HealthMonitorInterface" in interfaces_module.__all__

    def test_all_exports_health_status(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthStatus-t."""
        assert "HealthStatus" in interfaces_module.__all__

    def test_all_exports_system_health(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a SystemHealth-t."""
        assert "SystemHealth" in interfaces_module.__all__

    def test_component_health_is_correct_class(self) -> None:
        """Teszteli, hogy a ComponentHealth a helyes osztály."""
        assert interfaces_module.ComponentHealth is ComponentHealth

    def test_component_status_is_correct_class(self) -> None:
        """Teszteli, hogy a ComponentStatus a helyes osztály."""
        assert interfaces_module.ComponentStatus is ComponentStatus

    def test_health_check_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthCheckInterface a helyes osztály."""
        assert interfaces_module.HealthCheckInterface is HealthCheckInterface

    def test_health_monitor_interface_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthMonitorInterface a helyes osztály."""
        assert interfaces_module.HealthMonitorInterface is HealthMonitorInterface

    def test_health_status_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthStatus a helyes osztály."""
        assert interfaces_module.HealthStatus is HealthStatus

    def test_system_health_is_correct_class(self) -> None:
        """Teszteli, hogy a SystemHealth a helyes osztály."""
        assert interfaces_module.SystemHealth is SystemHealth

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert interfaces_module.__doc__ is not None
        assert len(interfaces_module.__doc__) > 0

    def test_docstring_mentions_health(self) -> None:
        """Teszteli, hogy a docstring említi az egészségügyi komponenst."""
        assert interfaces_module.__doc__ is not None
        assert "egészség" in interfaces_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in interfaces_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in interfaces_module.__all__:
            assert hasattr(interfaces_module, name)

    def test_health_check_interface_is_abstract(self) -> None:
        """Teszteli, hogy a HealthCheckInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.HealthCheckInterface, ABCMeta)

    def test_health_monitor_interface_is_abstract(self) -> None:
        """Teszteli, hogy a HealthMonitorInterface absztrakt osztály."""
        from abc import ABCMeta

        assert isinstance(interfaces_module.HealthMonitorInterface, ABCMeta)

    def test_component_status_is_enum(self) -> None:
        """Teszteli, hogy a ComponentStatus enum."""
        from enum import Enum

        assert issubclass(interfaces_module.ComponentStatus, Enum)

    def test_health_status_is_enum(self) -> None:
        """Teszteli, hogy a HealthStatus enum."""
        from enum import Enum

        assert issubclass(interfaces_module.HealthStatus, Enum)

    def test_all_count(self) -> None:
        """Teszteli, hogy az __all__ 6 elemet tartalmaz."""
        assert len(interfaces_module.__all__) == 6
