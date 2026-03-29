"""Unit tesztek a neural_ai.core.system.exceptions.__init__ modulhoz."""

import neural_ai.core.system.exceptions as exceptions_module
from neural_ai.core.system.exceptions.health_error import (
    ComponentNotFoundError,
    HealthCheckError,
    HealthError,
    HealthMonitorError,
)


class TestSystemExceptionsInit:
    """Tesztek a system exceptions __init__.py modulhoz."""

    def test_module_has_all(self) -> None:
        """Teszteli, hogy a modul rendelkezik __all__ attribútummal."""
        assert hasattr(exceptions_module, "__all__")
        assert isinstance(exceptions_module.__all__, list)

    def test_all_exports_health_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthError-t."""
        assert "HealthError" in exceptions_module.__all__

    def test_all_exports_health_monitor_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthMonitorError-t."""
        assert "HealthMonitorError" in exceptions_module.__all__

    def test_all_exports_health_check_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a HealthCheckError-t."""
        assert "HealthCheckError" in exceptions_module.__all__

    def test_all_exports_component_not_found_error(self) -> None:
        """Teszteli, hogy az __all__ tartalmazza a ComponentNotFoundError-t."""
        assert "ComponentNotFoundError" in exceptions_module.__all__

    def test_health_error_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthError a helyes osztály."""
        assert exceptions_module.HealthError is HealthError

    def test_health_monitor_error_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthMonitorError a helyes osztály."""
        assert exceptions_module.HealthMonitorError is HealthMonitorError

    def test_health_check_error_is_correct_class(self) -> None:
        """Teszteli, hogy a HealthCheckError a helyes osztály."""
        assert exceptions_module.HealthCheckError is HealthCheckError

    def test_component_not_found_error_is_correct_class(self) -> None:
        """Teszteli, hogy a ComponentNotFoundError a helyes osztály."""
        assert exceptions_module.ComponentNotFoundError is ComponentNotFoundError

    def test_module_has_docstring(self) -> None:
        """Teszteli, hogy a modul rendelkezik docstring-gel."""
        assert exceptions_module.__doc__ is not None
        assert len(exceptions_module.__doc__) > 0

    def test_docstring_mentions_health(self) -> None:
        """Teszteli, hogy a docstring említi az egészségügyi komponenst."""
        assert exceptions_module.__doc__ is not None
        assert "egészség" in exceptions_module.__doc__.lower()

    def test_no_private_exports(self) -> None:
        """Teszteli, hogy nincsenek privát exportok az __all__-ban."""
        for name in exceptions_module.__all__:
            assert not name.startswith("_")

    def test_all_exports_exist(self) -> None:
        """Teszteli, hogy az __all__-ban felsorolt elemek léteznek."""
        for name in exceptions_module.__all__:
            assert hasattr(exceptions_module, name)

    def test_all_exports_are_exception_classes(self) -> None:
        """Teszteli, hogy az összes export Exception osztály."""
        assert issubclass(exceptions_module.HealthError, Exception)
        assert issubclass(exceptions_module.HealthMonitorError, Exception)
        assert issubclass(exceptions_module.HealthCheckError, Exception)
        assert issubclass(exceptions_module.ComponentNotFoundError, Exception)

    def test_health_monitor_error_inherits_from_health_error(self) -> None:
        """Teszteli, hogy a HealthMonitorError a HealthError leszármazottja."""
        assert issubclass(exceptions_module.HealthMonitorError, exceptions_module.HealthError)

    def test_health_check_error_inherits_from_health_error(self) -> None:
        """Teszteli, hogy a HealthCheckError a HealthError leszármazottja."""
        assert issubclass(exceptions_module.HealthCheckError, exceptions_module.HealthError)

    def test_component_not_found_error_inherits_from_health_error(self) -> None:
        """Teszteli, hogy a ComponentNotFoundError a HealthError leszármazottja."""
        assert issubclass(
            exceptions_module.ComponentNotFoundError, exceptions_module.HealthError
        )

    def test_all_count(self) -> None:
        """Teszteli, hogy az __all__ 4 elemet tartalmaz."""
        assert len(exceptions_module.__all__) == 4
