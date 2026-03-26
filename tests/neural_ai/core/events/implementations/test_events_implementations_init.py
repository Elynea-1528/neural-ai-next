"""Tesztek a core.events.implementations.__init__.py exportjaihoz.

Ez a modul ellenőrzi, hogy a core.events.implementations csomag megfelelően exportálja-e
a szükséges osztályokat.
"""

from neural_ai.core.events.implementations import EventBus, EventBusConfig
from neural_ai.core.events.implementations.zeromq_bus import (
    EventBus as ZMQEventBus,
)
from neural_ai.core.events.implementations.zeromq_bus import (
    EventBusConfig as ZMQEventBusConfig,
)


class TestImplementationsInitExports:
    """Teszteli a core.events.implementations.__init__.py exportjait."""

    def test_event_bus_exported(self) -> None:
        """Teszteli, hogy az EventBus elérhető-e."""
        assert EventBus is not None
        assert EventBus is ZMQEventBus

    def test_event_bus_config_exported(self) -> None:
        """Teszteli, hogy az EventBusConfig elérhető-e."""
        assert EventBusConfig is not None
        assert EventBusConfig is ZMQEventBusConfig

    def test_all_imports_in_all_list(self) -> None:
        """Teszteli, hogy minden import szerepel-e a __all__ listában."""
        from neural_ai.core.events.implementations import __all__ as impl_all

        expected_exports = [
            "EventBus",
            "EventBusConfig",
        ]

        for export in expected_exports:
            assert export in impl_all, f"{export} nincs benne a __all__ listában"

    def test_import_from_implementations_package(self) -> None:
        """Teszteli, hogy a implementations csomagból lehet-e importálni."""
        from neural_ai.core.events import implementations

        assert hasattr(implementations, "EventBus")
        assert hasattr(implementations, "EventBusConfig")
