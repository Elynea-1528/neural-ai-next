"""Tesztek az EventModel-ekhez.

Ez a modul tartalmazza az összes eseménymodell tesztjeit,
beleértve a validációt és a szerializációt.

Author: Neural AI Next Team
Version: 1.0.0
"""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from neural_ai.core.events.interfaces.event_models import (
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)


class TestEventType:
    """EventType enumeráció tesztei."""

    def test_event_type_values(self) -> None:
        """Teszteli az EventType értékeit."""
        assert EventType.MARKET_DATA == "market_data"
        assert EventType.TRADE == "trade"
        assert EventType.SIGNAL == "signal"
        assert EventType.SYSTEM_LOG == "system_log"
        assert EventType.ORDER == "order"
        assert EventType.POSITION == "position"


class TestMarketDataEvent:
    """MarketDataEvent tesztek."""

    def test_valid_market_data_event(self) -> None:
        """Teszteli az érvényes MarketDataEvent létrehozását."""
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            bid=1.0850,
            ask=1.0852,
            source="jforex",
            volume=100000,
        )
        assert event.symbol == "EURUSD"
        assert event.bid == 1.0850
        assert event.ask == 1.0852
        assert event.volume == 100000
        assert event.source == "jforex"

    def test_market_data_event_without_volume(self) -> None:
        """Teszteli a MarketDataEvent létrehozását volume nélkül."""
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            bid=1.0850,
            ask=1.0852,
            source="mt5",
            volume=None,
        )
        assert event.volume is None

    def test_market_data_event_invalid_source(self) -> None:
        """Teszteli az érvénytelen forrást."""
        with pytest.raises(ValidationError) as exc_info:
            MarketDataEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                bid=1.0850,
                ask=1.0852,
                source="invalid_source",
                volume=None,
            )
        assert "Érvénytelen forrás" in str(exc_info.value)

    def test_market_data_event_invalid_bid(self) -> None:
        """Teszteli az érvénytelen bid értéket."""
        with pytest.raises(ValidationError):
            MarketDataEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                bid=-1.0,
                ask=1.0852,
                source="jforex",
                volume=None,
            )

    def test_market_data_event_invalid_ask(self) -> None:
        """Teszteli az érvénytelen ask értéket."""
        with pytest.raises(ValidationError):
            MarketDataEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                bid=1.0850,
                ask=-1.0,
                source="jforex",
                volume=None,
            )


class TestTradeEvent:
    """TradeEvent tesztek."""

    def test_valid_trade_event(self) -> None:
        """Teszteli az érvényes TradeEvent létrehozását."""
        event = TradeEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            direction="BUY",
            price=1.0850,
            volume=0.01,
            order_id="order_123",
            strategy_id="strategy_456",
        )
        assert event.symbol == "EURUSD"
        assert event.direction == "BUY"
        assert event.price == 1.0850
        assert event.volume == 0.01
        assert event.order_id == "order_123"
        assert event.strategy_id == "strategy_456"

    def test_trade_event_without_strategy_id(self) -> None:
        """Teszteli a TradeEvent létrehozását strategy_id nélkül."""
        event = TradeEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            direction="SELL",
            price=1.0850,
            volume=0.01,
            order_id="order_123",
        )
        assert event.strategy_id is None

    def test_trade_event_invalid_direction(self) -> None:
        """Teszteli az érvénytelen irányt."""
        with pytest.raises(ValidationError) as exc_info:
            TradeEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                direction="INVALID",
                price=1.0850,
                volume=0.01,
                order_id="order_123",
            )
        assert "Érvénytelen irány" in str(exc_info.value)

    def test_trade_event_invalid_price(self) -> None:
        """Teszteli az érvénytelen árat."""
        with pytest.raises(ValidationError):
            TradeEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                direction="BUY",
                price=-1.0,
                volume=0.01,
                order_id="order_123",
            )


class TestSignalEvent:
    """SignalEvent tesztek."""

    def test_valid_signal_event(self) -> None:
        """Teszteli az érvényes SignalEvent létrehozását."""
        event = SignalEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            signal_type="ENTRY_LONG",
            confidence=0.85,
            strategy_id="strategy_123",
            price=1.0850,
            target_price=1.0900,
            stop_loss=1.0800,
        )
        assert event.symbol == "EURUSD"
        assert event.signal_type == "ENTRY_LONG"
        assert event.confidence == 0.85
        assert event.strategy_id == "strategy_123"
        assert event.price == 1.0850
        assert event.target_price == 1.0900
        assert event.stop_loss == 1.0800

    def test_signal_event_without_prices(self) -> None:
        """Teszteli a SignalEvent létrehozását árak nélkül."""
        event = SignalEvent(
            symbol="EURUSD",
            timestamp=datetime.now(timezone.utc),
            signal_type="EXIT_SHORT",
            confidence=0.75,
            strategy_id="strategy_123",
            price=None,
            target_price=None,
            stop_loss=None,
        )
        assert event.price is None
        assert event.target_price is None
        assert event.stop_loss is None

    def test_signal_event_invalid_signal_type(self) -> None:
        """Teszteli az érvénytelen jelzés típust."""
        with pytest.raises(ValidationError) as exc_info:
            SignalEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                signal_type="INVALID",
                confidence=0.85,
                strategy_id="strategy_123",
                price=None,
                target_price=None,
                stop_loss=None,
            )
        assert "Érvénytelen jelzés típus" in str(exc_info.value)

    def test_signal_event_invalid_confidence(self) -> None:
        """Teszteli az érvénytelen konfidenciát."""
        with pytest.raises(ValidationError):
            SignalEvent(
                symbol="EURUSD",
                timestamp=datetime.now(timezone.utc),
                signal_type="ENTRY_LONG",
                confidence=1.5,
                strategy_id="strategy_123",
                price=None,
                target_price=None,
                stop_loss=None,
            )


class TestSystemLogEvent:
    """SystemLogEvent tesztek."""

    def test_valid_system_log_event(self) -> None:
        """Teszteli az érvényes SystemLogEvent létrehozását."""
        event = SystemLogEvent(
            timestamp=datetime.now(timezone.utc),
            level="INFO",
            component="EventBus",
            message="EventBus elindítva",
            extra_data={"key": "value"},
        )
        assert event.level == "INFO"
        assert event.component == "EventBus"
        assert event.message == "EventBus elindítva"
        assert event.extra_data == {"key": "value"}

    def test_system_log_event_without_extra_data(self) -> None:
        """Teszteli a SystemLogEvent létrehozását extra_data nélkül."""
        event = SystemLogEvent(
            timestamp=datetime.now(timezone.utc),
            level="ERROR",
            component="Collector",
            message="Hiba történt",
            extra_data=None,
        )
        assert event.extra_data is None

    def test_system_log_event_invalid_level(self) -> None:
        """Teszteli az érvénytelen log szintet."""
        with pytest.raises(ValidationError) as exc_info:
            SystemLogEvent(
                timestamp=datetime.now(timezone.utc),
                level="INVALID",
                component="EventBus",
                message="Üzenet",
                extra_data=None,
            )
        assert "Érvénytelen log szint" in str(exc_info.value)


class TestOrderEvent:
    """OrderEvent tesztek."""

    def test_valid_order_event(self) -> None:
        """Teszteli az érvényes OrderEvent létrehozását."""
        event = OrderEvent(
            order_id="order_123",
            timestamp=datetime.now(timezone.utc),
            symbol="EURUSD",
            order_type="MARKET",
            direction="BUY",
            volume=0.01,
            price=None,
            status="PENDING",
        )
        assert event.order_id == "order_123"
        assert event.symbol == "EURUSD"
        assert event.order_type == "MARKET"
        assert event.direction == "BUY"
        assert event.volume == 0.01
        assert event.price is None
        assert event.status == "PENDING"

    def test_order_event_with_price(self) -> None:
        """Teszteli az OrderEvent létrehozását árrésztvevővel."""
        event = OrderEvent(
            order_id="order_456",
            timestamp=datetime.now(timezone.utc),
            symbol="EURUSD",
            order_type="LIMIT",
            direction="SELL",
            volume=0.02,
            price=1.0900,
            status="FILLED",
        )
        assert event.price == 1.0900

    def test_order_event_invalid_order_type(self) -> None:
        """Teszteli az érvénytelen rendelés típust."""
        with pytest.raises(ValidationError) as exc_info:
            OrderEvent(
                order_id="order_123",
                timestamp=datetime.now(timezone.utc),
                symbol="EURUSD",
                order_type="INVALID",
                direction="BUY",
                volume=0.01,
                price=None,
                status="PENDING",
            )
        assert "Érvénytelen rendelés típus" in str(exc_info.value)

    def test_order_event_invalid_status(self) -> None:
        """Teszteli az érvénytelen állapotot."""
        with pytest.raises(ValidationError) as exc_info:
            OrderEvent(
                order_id="order_123",
                timestamp=datetime.now(timezone.utc),
                symbol="EURUSD",
                order_type="MARKET",
                direction="BUY",
                volume=0.01,
                price=None,
                status="INVALID",
            )
        assert "Érvénytelen állapot" in str(exc_info.value)


class TestPositionEvent:
    """PositionEvent tesztek."""

    def test_valid_position_event(self) -> None:
        """Teszteli az érvényes PositionEvent létrehozását."""
        event = PositionEvent(
            position_id="position_123",
            timestamp=datetime.now(timezone.utc),
            symbol="EURUSD",
            direction="LONG",
            volume=0.01,
            entry_price=1.0850,
            current_price=1.0860,
            profit_loss=10.0,
            status="OPEN",
        )
        assert event.position_id == "position_123"
        assert event.symbol == "EURUSD"
        assert event.direction == "LONG"
        assert event.volume == 0.01
        assert event.entry_price == 1.0850
        assert event.current_price == 1.0860
        assert event.profit_loss == 10.0
        assert event.status == "OPEN"

    def test_position_event_without_profit_loss(self) -> None:
        """Teszteli a PositionEvent létrehozását profit_loss nélkül."""
        event = PositionEvent(
            position_id="position_456",
            timestamp=datetime.now(timezone.utc),
            symbol="EURUSD",
            direction="SHORT",
            volume=0.02,
            entry_price=1.0850,
            current_price=1.0840,
            profit_loss=None,
            status="CLOSED",
        )
        assert event.profit_loss is None

    def test_position_event_invalid_direction(self) -> None:
        """Teszteli az érvénytelen irányt."""
        with pytest.raises(ValidationError) as exc_info:
            PositionEvent(
                position_id="position_123",
                timestamp=datetime.now(timezone.utc),
                symbol="EURUSD",
                direction="INVALID",
                volume=0.01,
                entry_price=1.0850,
                current_price=1.0860,
                profit_loss=None,
                status="OPEN",
            )
        assert "Érvénytelen irány" in str(exc_info.value)

    def test_position_event_invalid_status(self) -> None:
        """Teszteli az érvénytelen állapotot."""
        with pytest.raises(ValidationError) as exc_info:
            PositionEvent(
                position_id="position_123",
                timestamp=datetime.now(timezone.utc),
                symbol="EURUSD",
                direction="LONG",
                volume=0.01,
                entry_price=1.0850,
                current_price=1.0860,
                profit_loss=None,
                status="INVALID",
            )
        assert "Érvénytelen állapot" in str(exc_info.value)