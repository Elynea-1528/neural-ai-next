"""Tesztek a core.events.interfaces.__init__.py exportjaihoz.

Ez a modul ellenőrzi, hogy a core.events.interfaces csomag megfelelően exportálja-e
a szükséges interfészeket és modelleket.
"""

from neural_ai.core.events.interfaces import (
    EventBusConfig,
    EventBusInterface,
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)
from neural_ai.core.events.interfaces.event_bus_interface import (
    EventBusConfig as IEventBusConfig,
)
from neural_ai.core.events.interfaces.event_bus_interface import (
    EventBusInterface as IEventBusInterface,
)
from neural_ai.core.events.interfaces.event_models import (
    EventType as EType,
)
from neural_ai.core.events.interfaces.event_models import (
    MarketDataEvent as MDE,
)
from neural_ai.core.events.interfaces.event_models import (
    OrderEvent as OE,
)
from neural_ai.core.events.interfaces.event_models import (
    PositionEvent as PE,
)
from neural_ai.core.events.interfaces.event_models import (
    SignalEvent as SE,
)
from neural_ai.core.events.interfaces.event_models import (
    SystemLogEvent as SLE,
)
from neural_ai.core.events.interfaces.event_models import (
    TradeEvent as TE,
)


class TestInterfacesInitExports:
    """Teszteli a core.events.interfaces.__init__.py exportjait."""

    def test_event_bus_interface_exported(self) -> None:
        """Teszteli, hogy az EventBusInterface elérhető-e."""
        assert EventBusInterface is not None
        assert EventBusInterface is IEventBusInterface

    def test_event_bus_config_exported(self) -> None:
        """Teszteli, hogy az EventBusConfig elérhető-e."""
        assert EventBusConfig is not None
        assert EventBusConfig is IEventBusConfig

    def test_event_type_exported(self) -> None:
        """Teszteli, hogy az EventType elérhető-e."""
        assert EventType is not None
        assert EventType is EType

    def test_market_data_event_exported(self) -> None:
        """Teszteli, hogy a MarketDataEvent elérhető-e."""
        assert MarketDataEvent is not None
        assert MarketDataEvent is MDE

    def test_trade_event_exported(self) -> None:
        """Teszteli, hogy a TradeEvent elérhető-e."""
        assert TradeEvent is not None
        assert TradeEvent is TE

    def test_signal_event_exported(self) -> None:
        """Teszteli, hogy a SignalEvent elérhető-e."""
        assert SignalEvent is not None
        assert SignalEvent is SE

    def test_system_log_event_exported(self) -> None:
        """Teszteli, hogy a SystemLogEvent elérhető-e."""
        assert SystemLogEvent is not None
        assert SystemLogEvent is SLE

    def test_order_event_exported(self) -> None:
        """Teszteli, hogy az OrderEvent elérhető-e."""
        assert OrderEvent is not None
        assert OrderEvent is OE

    def test_position_event_exported(self) -> None:
        """Teszteli, hogy a PositionEvent elérhető-e."""
        assert PositionEvent is not None
        assert PositionEvent is PE

    def test_all_imports_in_all_list(self) -> None:
        """Teszteli, hogy minden import szerepel-e a __all__ listában."""
        from neural_ai.core.events.interfaces import __all__ as interfaces_all

        expected_exports = [
            "EventBusInterface",
            "EventBusConfig",
            "EventType",
            "MarketDataEvent",
            "TradeEvent",
            "SignalEvent",
            "SystemLogEvent",
            "OrderEvent",
            "PositionEvent",
        ]

        for export in expected_exports:
            assert export in interfaces_all, f"{export} nincs benne a __all__ listában"

    def test_import_from_interfaces_package(self) -> None:
        """Teszteli, hogy az interfaces csomagból lehet-e importálni."""
        from neural_ai.core.events import interfaces

        assert hasattr(interfaces, "EventBusInterface")
        assert hasattr(interfaces, "EventBusConfig")
        assert hasattr(interfaces, "EventType")
        assert hasattr(interfaces, "MarketDataEvent")
        assert hasattr(interfaces, "TradeEvent")
        assert hasattr(interfaces, "SignalEvent")
        assert hasattr(interfaces, "SystemLogEvent")
        assert hasattr(interfaces, "OrderEvent")
        assert hasattr(interfaces, "PositionEvent")
