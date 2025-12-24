"""Tesztek az esemény modellekhez.

Ez a modul tartalmazza az összes esemény típus tesztjeit,
biztosítva a Pydantic modellek helyes működését.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from neural_ai.core.events.events import (
    EventType,
    MarketDataEvent,
    OrderEvent,
    PositionEvent,
    SignalEvent,
    SystemLogEvent,
    TradeEvent,
)


class TestEventType:
    """EventType enumeráció tesztjei."""

    def test_event_type_values(self):
        """Teszteli az EventType értékeit."""
        assert EventType.MARKET_DATA == "market_data"
        assert EventType.TRADE == "trade"
        assert EventType.SIGNAL == "signal"
        assert EventType.SYSTEM_LOG == "system_log"
        assert EventType.ORDER == "order"
        assert EventType.POSITION == "position"


class TestMarketDataEvent:
    """MarketDataEvent tesztjei."""

    def test_valid_market_data_event(self):
        """Teszteli az érvényes MarketDataEvent létrehozását."""
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0851,
            volume=1000000,
            source="mt5",
        )

        assert event.symbol == "EURUSD"
        assert event.bid == 1.0850
        assert event.ask == 1.0851
        assert event.volume == 1000000
        assert event.source == "mt5"

    def test_market_data_event_without_volume(self):
        """Teszteli a MarketDataEvent-et volume nélkül."""
        event = MarketDataEvent(
            symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=1.0851, source="jforex"
        )

        assert event.volume is None
        assert event.source == "jforex"

    def test_invalid_source_raises_error(self):
        """Teszteli az érvénytelen forrás hibajelzését."""
        with pytest.raises(ValidationError) as exc_info:
            MarketDataEvent(
                symbol="EURUSD",
                timestamp=datetime.now(UTC),
                bid=1.0850,
                ask=1.0851,
                source="invalid_source",
            )

        assert "Érvénytelen forrás" in str(exc_info.value)

    def test_bid_must_be_positive(self):
        """Teszteli, hogy a bid-nek pozitívnak kell lennie."""
        with pytest.raises(ValidationError):
            MarketDataEvent(
                symbol="EURUSD", timestamp=datetime.now(UTC), bid=-1.0, ask=1.0851, source="mt5"
            )

    def test_ask_must_be_positive(self):
        """Teszteli, hogy az ask-nek pozitívnak kell lennie."""
        with pytest.raises(ValidationError):
            MarketDataEvent(
                symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=-1.0, source="mt5"
            )


class TestTradeEvent:
    """TradeEvent tesztjei."""

    def test_valid_trade_event(self):
        """Teszteli az érvényes TradeEvent létrehozását."""
        event = TradeEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            direction="BUY",
            price=1.0850,
            volume=0.01,
            order_id="order_123",
        )

        assert event.symbol == "EURUSD"
        assert event.direction == "BUY"
        assert event.price == 1.0850
        assert event.volume == 0.01
        assert event.order_id == "order_123"
        assert event.strategy_id is None

    def test_trade_event_with_strategy_id(self):
        """Teszteli a TradeEvent-et strategy_id-val."""
        event = TradeEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            direction="SELL",
            price=1.0850,
            volume=0.01,
            order_id="order_456",
            strategy_id="strategy_momentum",
        )

        assert event.strategy_id == "strategy_momentum"

    def test_invalid_direction_raises_error(self):
        """Teszteli az érvénytelen irány hibajelzését."""
        with pytest.raises(ValidationError) as exc_info:
            TradeEvent(
                symbol="EURUSD",
                timestamp=datetime.now(UTC),
                direction="INVALID",
                price=1.0850,
                volume=0.01,
                order_id="order_789",
            )

        assert "Érvénytelen irány" in str(exc_info.value)


class TestSignalEvent:
    """SignalEvent tesztjei."""

    def test_valid_signal_event(self):
        """Teszteli az érvényes SignalEvent létrehozását."""
        event = SignalEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            signal_type="ENTRY_LONG",
            confidence=0.85,
            strategy_id="strategy_001",
        )

        assert event.symbol == "EURUSD"
        assert event.signal_type == "ENTRY_LONG"
        assert event.confidence == 0.85
        assert event.strategy_id == "strategy_001"

    def test_signal_event_with_prices(self):
        """Teszteli a SignalEvent-et árakkal."""
        event = SignalEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            signal_type="EXIT_SHORT",
            confidence=0.75,
            strategy_id="strategy_002",
            price=1.0850,
            target_price=1.0900,
            stop_loss=1.0800,
        )

        assert event.price == 1.0850
        assert event.target_price == 1.0900
        assert event.stop_loss == 1.0800

    def test_confidence_must_be_between_0_and_1(self):
        """Teszteli, hogy a confidence 0 és 1 között legyen."""
        with pytest.raises(ValidationError):
            SignalEvent(
                symbol="EURUSD",
                timestamp=datetime.now(UTC),
                signal_type="ENTRY_LONG",
                confidence=1.5,
                strategy_id="strategy_003",
            )

    def test_invalid_signal_type_raises_error(self):
        """Teszteli az érvénytelen jelzés típus hibajelzését."""
        with pytest.raises(ValidationError):
            SignalEvent(
                symbol="EURUSD",
                timestamp=datetime.now(UTC),
                signal_type="INVALID_SIGNAL",
                confidence=0.5,
                strategy_id="strategy_004",
            )


class TestSystemLogEvent:
    """SystemLogEvent tesztjei."""

    def test_valid_system_log_event(self):
        """Teszteli az érvényes SystemLogEvent létrehozását."""
        event = SystemLogEvent(
            timestamp=datetime.now(UTC),
            level="INFO",
            component="EventBus",
            message="EventBus elindítva",
        )

        assert event.level == "INFO"
        assert event.component == "EventBus"
        assert event.message == "EventBus elindítva"
        assert event.extra_data is None

    def test_system_log_event_with_extra_data(self):
        """Teszteli a SystemLogEvent-et extra adatokkal."""
        extra_data = {"key": "value", "count": 42}
        event = SystemLogEvent(
            timestamp=datetime.now(UTC),
            level="ERROR",
            component="Database",
            message="Connection failed",
            extra_data=extra_data,
        )

        assert event.extra_data == extra_data

    def test_invalid_log_level_raises_error(self):
        """Teszteli az érvénytelen log szint hibajelzését."""
        with pytest.raises(ValidationError):
            SystemLogEvent(
                timestamp=datetime.now(UTC),
                level="INVALID",
                component="Test",
                message="Test message",
            )


class TestOrderEvent:
    """OrderEvent tesztjei."""

    def test_valid_order_event(self):
        """Teszteli az érvényes OrderEvent létrehozását."""
        event = OrderEvent(
            order_id="order_123",
            timestamp=datetime.now(UTC),
            symbol="EURUSD",
            order_type="MARKET",
            direction="BUY",
            volume=0.01,
            status="PENDING",
        )

        assert event.order_id == "order_123"
        assert event.order_type == "MARKET"
        assert event.direction == "BUY"
        assert event.volume == 0.01
        assert event.status == "PENDING"
        assert event.price is None

    def test_limit_order_event_with_price(self):
        """Teszteli a limit order event-et árfeltétellel."""
        event = OrderEvent(
            order_id="order_456",
            timestamp=datetime.now(UTC),
            symbol="EURUSD",
            order_type="LIMIT",
            direction="SELL",
            volume=0.02,
            price=1.0900,
            status="PENDING",
        )

        assert event.order_type == "LIMIT"
        assert event.price == 1.0900

    def test_invalid_order_type_raises_error(self):
        """Teszteli az érvénytelen rendelés típus hibajelzését."""
        with pytest.raises(ValidationError):
            OrderEvent(
                order_id="order_789",
                timestamp=datetime.now(UTC),
                symbol="EURUSD",
                order_type="INVALID",
                direction="BUY",
                volume=0.01,
                status="PENDING",
            )

    def test_invalid_status_raises_error(self):
        """Teszteli az érvénytelen állapot hibajelzését."""
        with pytest.raises(ValidationError):
            OrderEvent(
                order_id="order_999",
                timestamp=datetime.now(UTC),
                symbol="EURUSD",
                order_type="MARKET",
                direction="BUY",
                volume=0.01,
                status="INVALID",
            )


class TestPositionEvent:
    """PositionEvent tesztjei."""

    def test_valid_position_event(self):
        """Teszteli az érvényes PositionEvent létrehozását."""
        event = PositionEvent(
            position_id="pos_123",
            timestamp=datetime.now(UTC),
            symbol="EURUSD",
            direction="LONG",
            volume=0.01,
            entry_price=1.0850,
            current_price=1.0860,
            status="OPEN",
        )

        assert event.position_id == "pos_123"
        assert event.direction == "LONG"
        assert event.volume == 0.01
        assert event.entry_price == 1.0850
        assert event.current_price == 1.0860
        assert event.status == "OPEN"
        assert event.profit_loss is None

    def test_position_event_with_profit_loss(self):
        """Teszteli a PositionEvent-et profit/loss értékkel."""
        event = PositionEvent(
            position_id="pos_456",
            timestamp=datetime.now(UTC),
            symbol="EURUSD",
            direction="SHORT",
            volume=0.02,
            entry_price=1.0850,
            current_price=1.0840,
            profit_loss=20.0,
            status="CLOSED",
        )

        assert event.direction == "SHORT"
        assert event.profit_loss == 20.0
        assert event.status == "CLOSED"

    def test_invalid_direction_raises_error(self):
        """Teszteli az érvénytelen irány hibajelzését."""
        with pytest.raises(ValidationError):
            PositionEvent(
                position_id="pos_789",
                timestamp=datetime.now(UTC),
                symbol="EURUSD",
                direction="INVALID",
                volume=0.01,
                entry_price=1.0850,
                current_price=1.0860,
                status="OPEN",
            )

    def test_invalid_status_raises_error(self):
        """Teszteli az érvénytelen állapot hibajelzését."""
        with pytest.raises(ValidationError):
            PositionEvent(
                position_id="pos_999",
                timestamp=datetime.now(UTC),
                symbol="EURUSD",
                direction="LONG",
                volume=0.01,
                entry_price=1.0850,
                current_price=1.0860,
                status="INVALID",
            )
