"""Tesztek a core.events.__init__.py exportjaihoz.

Ez a modul ellenőrzi, hogy a core.events csomag megfelelően exportálja-e
a szükséges osztályokat és függvényeket.
"""

from neural_ai.core.events import (
    EventBusFactory,
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)


class TestEventsInitExports:
    """Teszteli a core.events.__init__.py exportjait."""

    def test_event_bus_factory_exported(self) -> None:
        """Teszteli, hogy az EventBusFactory elérhető-e."""
        assert EventBusFactory is not None
        from neural_ai.core.events.factory import EventBusFactory as Factory

        assert EventBusFactory is Factory

    def test_event_type_exported(self) -> None:
        """Teszteli, hogy az EventType elérhető-e."""
        assert EventType is not None
        from neural_ai.core.events.interfaces.event_models import EventType as ET

        assert EventType is ET

    def test_market_data_event_exported(self) -> None:
        """Teszteli, hogy a MarketDataEvent elérhető-e."""
        assert MarketDataEvent is not None
        from neural_ai.core.events.interfaces.event_models import MarketDataEvent as MDE

        assert MarketDataEvent is MDE

    def test_trade_event_exported(self) -> None:
        """Teszteli, hogy a TradeEvent elérhető-e."""
        assert TradeEvent is not None
        from neural_ai.core.events.interfaces.event_models import TradeEvent as TE

        assert TradeEvent is TE

    def test_signal_event_exported(self) -> None:
        """Teszteli, hogy a SignalEvent elérhető-e."""
        assert SignalEvent is not None
        from neural_ai.core.events.interfaces.event_models import SignalEvent as SE

        assert SignalEvent is SE

    def test_system_log_event_exported(self) -> None:
        """Teszteli, hogy a SystemLogEvent elérhető-e."""
        assert SystemLogEvent is not None
        from neural_ai.core.events.interfaces.event_models import SystemLogEvent as SLE

        assert SystemLogEvent is SLE

    def test_order_event_exported(self) -> None:
        """Teszteli, hogy az OrderEvent elérhető-e."""
        assert OrderEvent is not None
        from neural_ai.core.events.interfaces.event_models import OrderEvent as OE

        assert OrderEvent is OE

    def test_position_event_exported(self) -> None:
        """Teszteli, hogy a PositionEvent elérhető-e."""
        assert PositionEvent is not None
        from neural_ai.core.events.interfaces.event_models import PositionEvent as PE

        assert PositionEvent is PE

    def test_all_imports_in_all_list(self) -> None:
        """Teszteli, hogy minden import szerepel-e a __all__ listában."""
        from neural_ai.core.events import __all__ as events_all

        expected_exports = [
            "EventBusFactory",
            "EventType",
            "MarketDataEvent",
            "TradeEvent",
            "SignalEvent",
            "SystemLogEvent",
            "OrderEvent",
            "PositionEvent",
        ]

        for export in expected_exports:
            assert export in events_all, f"{export} nincs benne a __all__ listában"

    def test_import_from_package_root(self) -> None:
        """Teszteli, hogy a csomag gyökeréből lehet-e importálni."""
        # Ez a teszt ellenőrzi, hogy a "from neural_ai.core.events import ..." működik-e
        from neural_ai.core import events

        assert hasattr(events, "EventBusFactory")
        assert hasattr(events, "EventType")
        assert hasattr(events, "MarketDataEvent")
        assert hasattr(events, "TradeEvent")
        assert hasattr(events, "SignalEvent")
        assert hasattr(events, "SystemLogEvent")
        assert hasattr(events, "OrderEvent")
        assert hasattr(events, "PositionEvent")
