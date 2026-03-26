"""Tesztek a core.events.exceptions.__init__.py exportjaihoz.

Ez a modul ellenőrzi, hogy a core.events.exceptions csomag megfelelően exportálja-e
a szükséges kivételeket.
"""

from neural_ai.core.events.exceptions import EventBusError, PublishError, SubscriberError
from neural_ai.core.events.exceptions.event_error import (
    EventBusError as EError,
)
from neural_ai.core.events.exceptions.event_error import (
    PublishError as PError,
)
from neural_ai.core.events.exceptions.event_error import (
    SubscriberError as SError,
)


class TestExceptionsInitExports:
    """Teszteli a core.events.exceptions.__init__.py exportjait."""

    def test_event_bus_error_exported(self) -> None:
        """Teszteli, hogy az EventBusError elérhető-e."""
        assert EventBusError is not None
        assert EventBusError is EError

    def test_publish_error_exported(self) -> None:
        """Teszteli, hogy a PublishError elérhető-e."""
        assert PublishError is not None
        assert PublishError is PError

    def test_subscriber_error_exported(self) -> None:
        """Teszteli, hogy a SubscriberError elérhető-e."""
        assert SubscriberError is not None
        assert SubscriberError is SError

    def test_all_imports_in_all_list(self) -> None:
        """Teszteli, hogy minden import szerepel-e a __all__ listában."""
        from neural_ai.core.events.exceptions import __all__ as exceptions_all

        expected_exports = [
            "EventBusError",
            "PublishError",
            "SubscriberError",
        ]

        for export in expected_exports:
            assert export in exceptions_all, f"{export} nincs benne a __all__ listában"

    def test_import_from_exceptions_package(self) -> None:
        """Teszteli, hogy az exceptions csomagból lehet-e importálni."""
        from neural_ai.core.events import exceptions

        assert hasattr(exceptions, "EventBusError")
        assert hasattr(exceptions, "PublishError")
        assert hasattr(exceptions, "SubscriberError")
