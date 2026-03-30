"""Unit tesztek a Health Exception osztályokhoz."""

import pytest

from neural_ai.core.system.exceptions.health_error import (
    ComponentNotFoundError,
    HealthCheckError,
    HealthError,
    HealthMonitorError,
)


class TestHealthError:
    """Tesztek a HealthError alap kivételhez."""

    def test_health_error_is_exception(self) -> None:
        """Ellenőrzi, hogy HealthError az Exception leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(HealthError, Exception)

    def test_health_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy HealthError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(HealthError):
            raise HealthError("Teszt hiba")

    def test_health_error_with_message(self) -> None:
        """Ellenőrzi, hogy HealthError üzenettel dobható."""
        # Arrange
        message = "Rendszer egészségügyi hiba"

        # Act & Assert
        with pytest.raises(HealthError) as exc_info:
            raise HealthError(message)

        assert str(exc_info.value) == message


class TestHealthMonitorError:
    """Tesztek a HealthMonitorError kivételhez."""

    def test_health_monitor_error_is_health_error(self) -> None:
        """Ellenőrzi, hogy HealthMonitorError a HealthError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(HealthMonitorError, HealthError)

    def test_health_monitor_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy HealthMonitorError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(HealthMonitorError):
            raise HealthMonitorError("Monitor hiba")

    def test_health_monitor_error_with_message(self) -> None:
        """Ellenőrzi, hogy HealthMonitorError üzenettel dobható."""
        # Arrange
        message = "HealthMonitor inicializálási hiba"

        # Act & Assert
        with pytest.raises(HealthMonitorError) as exc_info:
            raise HealthMonitorError(message)

        assert str(exc_info.value) == message

    def test_health_monitor_error_caught_as_health_error(self) -> None:
        """Ellenőrzi, hogy HealthMonitorError elkapható HealthError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(HealthError):
            raise HealthMonitorError("Monitor hiba")


class TestHealthCheckError:
    """Tesztek a HealthCheckError kivételhez."""

    def test_health_check_error_is_health_error(self) -> None:
        """Ellenőrzi, hogy HealthCheckError a HealthError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(HealthCheckError, HealthError)

    def test_health_check_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy HealthCheckError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(HealthCheckError):
            raise HealthCheckError("Ellenőrzési hiba")

    def test_health_check_error_with_message(self) -> None:
        """Ellenőrzi, hogy HealthCheckError üzenettel dobható."""
        # Arrange
        message = "Egészségügyi ellenőrzés sikertelen"

        # Act & Assert
        with pytest.raises(HealthCheckError) as exc_info:
            raise HealthCheckError(message)

        assert str(exc_info.value) == message

    def test_health_check_error_caught_as_health_error(self) -> None:
        """Ellenőrzi, hogy HealthCheckError elkapható HealthError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(HealthError):
            raise HealthCheckError("Ellenőrzési hiba")


class TestComponentNotFoundError:
    """Tesztek a ComponentNotFoundError kivételhez."""

    def test_component_not_found_error_is_health_monitor_error(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError a HealthMonitorError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(ComponentNotFoundError, HealthMonitorError)

    def test_component_not_found_error_is_health_error(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError a HealthError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(ComponentNotFoundError, HealthError)

    def test_component_not_found_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(ComponentNotFoundError):
            raise ComponentNotFoundError("Komponens nem található")

    def test_component_not_found_error_with_message(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError üzenettel dobható."""
        # Arrange
        message = "A 'database' komponens nem található"

        # Act & Assert
        with pytest.raises(ComponentNotFoundError) as exc_info:
            raise ComponentNotFoundError(message)

        assert str(exc_info.value) == message

    def test_component_not_found_error_caught_as_health_monitor_error(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError elkapható HealthMonitorError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(HealthMonitorError):
            raise ComponentNotFoundError("Komponens nem található")

    def test_component_not_found_error_caught_as_health_error(self) -> None:
        """Ellenőrzi, hogy ComponentNotFoundError elkapható HealthError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(HealthError):
            raise ComponentNotFoundError("Komponens nem található")
