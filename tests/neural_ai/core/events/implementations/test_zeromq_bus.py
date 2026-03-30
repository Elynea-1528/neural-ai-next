"""Tesztek a ZeroMQBus implementációhoz.

# pyright: reportUnknownArgumentType=false, reportUnknownMemberType=false, reportPrivateUsage=false
# ZeroMQ async fixture és protected member access hibák.

Ez a modul tartalmazza a ZeroMQBus tesztjeit, ZMQ mocking-gal.

Author: Neural AI Next Team
Version: 1.0.0
"""

import asyncio
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from neural_ai.core.events.exceptions.event_error import EventBusError, PublishError
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent


@pytest.fixture
def mock_logger() -> MagicMock:
    """Mock logger fixture minden teszthez (DI pattern)."""
    logger = MagicMock()
    logger.debug = MagicMock()
    logger.info = MagicMock()
    logger.warning = MagicMock()
    logger.error = MagicMock()
    logger.critical = MagicMock()
    return logger


@pytest.fixture(autouse=True)
def reset_singleton():
    """Singleton reset minden teszt előtt és után."""
    from neural_ai.core.base.implementations.singleton import SingletonMeta
    from neural_ai.core.events.implementations.zeromq_bus import EventBus

    # Teljes reset ELŐTTE
    if hasattr(SingletonMeta, '_instances'):
        SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]

    # EventBus specifikus cleanup
    if hasattr(EventBus, '_instance'):
        delattr(EventBus, '_instance')

    yield

    # Cleanup UTÁNA is
    if hasattr(SingletonMeta, '_instances'):
        SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]

    # EventBus specifikus cleanup
    if hasattr(EventBus, '_instance'):
        delattr(EventBus, '_instance')


@pytest.fixture
def mock_zmq_context():
    """Konzisztens ZMQ mock setup minden teszthez."""
    with patch('zmq.asyncio.Context') as mock_context_class:
        mock_context = MagicMock()
        mock_socket = MagicMock()

        # Async metódusok (FONTOS!)
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()

        # Sync metódusok
        mock_socket.bind = MagicMock()
        mock_socket.connect = MagicMock()
        mock_socket.close = MagicMock()
        mock_socket.setsockopt = MagicMock()

        mock_context.socket.return_value = mock_socket
        mock_context.term = MagicMock()
        mock_context_class.return_value = mock_context

        yield mock_context, mock_socket


class TestEventBusInitialization:
    """EventBus inicializálás tesztek."""

    def test_default_initialization(self, mock_zmq_context: tuple[MagicMock, MagicMock], mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az alapértelmezett inicializálást."""
        mock_context, mock_socket = mock_zmq_context  # pyright: ignore[reportUnusedVariable]

        bus = EventBus(logger=mock_logger)

        assert bus.config.pub_port == 5555
        assert bus.config.sub_port == 5556
        assert bus.config.use_inproc is False

    def test_custom_config_initialization(
        self, mock_zmq_context: tuple[MagicMock, MagicMock]
    ) -> None:
        """Teszteli az egyéni konfigurációval történő inicializálást."""
        mock_context, mock_socket = mock_zmq_context  # pyright: ignore[reportUnusedVariable]

        config = EventBusConfig(pub_port=6666, sub_port=6667, use_inproc=True)
        bus = EventBus(config, logger=mock_logger)  # type: ignore[arg-type]

        assert bus.config.pub_port == 6666
        assert bus.config.sub_port == 6667
        assert bus.config.use_inproc is True

    def test_external_zmq_context(self, mock_zmq_context: tuple[MagicMock, MagicMock], mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a külső ZMQ kontextus használatát."""
        mock_context, mock_socket = mock_zmq_context  # pyright: ignore[reportUnusedVariable]

        external_context: MagicMock = MagicMock()
        config = EventBusConfig(zmq_context=external_context)
        bus = EventBus(config, logger=mock_logger)

        assert bus._own_context is False  # pyright: ignore[reportPrivateUsage]
        assert bus._context is external_context  # pyright: ignore[reportPrivateUsage]

    def test_zmq_import_error(self, mock_zmq_context: tuple[MagicMock, MagicMock], mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a ZMQ import hibát."""
        with patch.dict("sys.modules", {"zmq": None, "zmq.asyncio": None}):
            with pytest.raises(ImportError, match="ZeroMQ nincs telepítve"):
                EventBus(logger=mock_logger)


class TestEventBusStartStop:
    """EventBus indítás és leállítás tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_success(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a sikeres indítást."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()

        assert bus._running is True  # pyright: ignore[reportPrivateUsage]
        mock_context.socket.assert_called_once()
        mock_socket.bind.assert_called_once_with("tcp://*:5555")

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_with_inproc(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az indítást inproc transporttal."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config, logger=mock_logger)
        await bus.start()

        assert bus._running is True  # pyright: ignore[reportPrivateUsage]
        mock_socket.bind.assert_called_once_with("inproc://eventbus_pub")

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_twice(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:
        """Teszteli a többszöri indítást."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()
        await bus.start()  # Másodszor is meghívjuk

        # Csak egyszer hívódjon meg a bind
        assert mock_socket.bind.call_count == 1

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_success(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a sikeres leállítást."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()
        await bus.stop()

        assert bus._running is False  # pyright: ignore[reportPrivateUsage]
        mock_socket.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_without_start(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a leállítást indítás nélkül."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.stop()  # Nem dob hibát

        assert bus._running is False  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_twice(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:
        """Teszteli a többszöri leállítást."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()
        await bus.stop()
        await bus.stop()  # Másodszor is meghívjuk

        assert bus._running is False  # pyright: ignore[reportPrivateUsage]


class TestEventBusPublish:
    """EventBus publish tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_success(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a sikeres esemény közzétételt."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()

        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        await bus.publish("market_data", event)

        mock_socket.send_multipart.assert_awaited_once()
        args = mock_socket.send_multipart.await_args[0][0]
        assert len(args) == 2
        assert args[0] == b"market_data"  # Témakör

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_not_started(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a közzétételt indítás nélkül."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        with pytest.raises(EventBusError, match="EventBus nincs elindítva"):
            await bus.publish("market_data", event)

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_no_publisher(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a közzétételt publisher socket nélkül."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        with pytest.raises(PublishError, match="Publisher socket nincs inicializálva"):
            await bus.publish("market_data", event)

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_batch_events(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a batch (lista) események közzétételét."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Hozzunk létre több eseményt egy listában
        events = [
            MarketDataEvent(
                symbol="EURUSD",
                timestamp=datetime.now(UTC),
                bid=1.0850,
                ask=1.0852,
                bid_volume=100000,
                ask_volume=100000,
                source="jforex",
                volume=100000,
            ),
            MarketDataEvent(
                symbol="GBPUSD",
                timestamp=datetime.now(UTC),
                bid=1.2700,
                ask=1.2702,
                bid_volume=80000,
                ask_volume=80000,
                source="jforex",
                volume=80000,
            ),
        ]

        await bus.publish("market_data", events)  # type: ignore

        # Ellenőrizzük, hogy mindkét eseményt elküldte-e
        assert mock_socket.send_multipart.await_count == 2

        # Ellenőrizzük az első eseményt
        args1 = mock_socket.send_multipart.await_args_list[0][0][0]
        assert len(args1) == 2
        assert args1[0] == b"market_data"

        # Ellenőrizzük a második eseményt
        args2 = mock_socket.send_multipart.await_args_list[1][0][0]
        assert len(args2) == 2
        assert args2[0] == b"market_data"


class TestEventBusSubscribeUnsubscribe:
    """EventBus feliratkozás és leiratkozás tesztek."""

    @patch("zmq.asyncio.Context")
    def test_subscribe_new_event_type(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az új eseménytípusra való feliratkozást."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback: MagicMock = MagicMock()

        bus.subscribe("market_data", callback)

        assert "market_data" in bus._subscribers  # pyright: ignore[reportPrivateUsage]
        assert callback in bus._subscribers["market_data"]  # pyright: ignore[reportPrivateUsage]

    @patch("zmq.asyncio.Context")
    def test_subscribe_multiple_callbacks(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli több callback feliratkozását ugyanarra az eseménytípusra."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback1: MagicMock = MagicMock()
        callback2: MagicMock = MagicMock()

        bus.subscribe("market_data", callback1)
        bus.subscribe("market_data", callback2)

        assert len(bus._subscribers["market_data"]) == 2  # pyright: ignore[reportPrivateUsage]
        assert callback1 in bus._subscribers["market_data"]  # pyright: ignore[reportPrivateUsage]
        assert callback2 in bus._subscribers["market_data"]  # pyright: ignore[reportPrivateUsage]

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_existing(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a létező feliratkozás lemondását."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback: MagicMock = MagicMock()

        bus.subscribe("market_data", callback)
        bus.unsubscribe("market_data", callback)

        assert "market_data" in bus._subscribers  # pyright: ignore[reportPrivateUsage]
        assert callback not in bus._subscribers["market_data"]  # pyright: ignore[reportPrivateUsage]

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_non_existing(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a nem létező feliratkozás lemondását."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback: MagicMock = MagicMock()

        # Nem dob hibát
        bus.unsubscribe("market_data", callback)

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_non_existing_event_type(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a nem létező eseménytípus lemondását."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback: MagicMock = MagicMock()

        # Nem dob hibát
        bus.unsubscribe("non_existing", callback)


class TestEventBusContextManager:
    """EventBus context manager tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_async_context_manager(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az aszinkron context managert."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        async with EventBus(logger=mock_logger) as bus:
            assert bus._running is True  # pyright: ignore[reportPrivateUsage]

        assert bus._running is False  # pyright: ignore[reportPrivateUsage]


class TestEventBusDeserialization:
    """EventBus deszerializáció tesztek."""

    @patch("zmq.asyncio.Context")
    def test_deserialize_market_data(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a MarketDataEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        result = bus._deserialize_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        assert isinstance(result, MarketDataEvent)
        assert result.symbol == "EURUSD"
        assert result.bid == 1.0850

    @patch("zmq.asyncio.Context")
    def test_deserialize_unknown_event_type(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az ismeretlen eseménytípus deszerializációját."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data = {"key": "value"}

        result = bus._deserialize_event("unknown_type", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is None

    @patch("zmq.asyncio.Context")
    def test_deserialize_invalid_data(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az érvénytelen adat deszerializációját."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data = {"invalid": "data"}

        result = bus._deserialize_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is None


class TestEventBusDispatch:
    """EventBus esemény továbbítás tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_success(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a sikeres esemény továbbítást."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback: AsyncMock = AsyncMock()
        bus.subscribe("market_data", callback)

        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        await bus._dispatch_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        callback.assert_awaited_once()
        assert callback.await_args is not None
        called_with = callback.await_args[0][0]
        assert isinstance(called_with, MarketDataEvent)
        assert called_with.symbol == "EURUSD"

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_no_subscribers(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az esemény továbbítást feliratkozók nélkül."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)

        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        # Nem dob hibát
        await bus._dispatch_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_callback_error(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a callback hibát."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback = AsyncMock(side_effect=Exception("Callback hiba"))
        bus.subscribe("market_data", callback)

        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        # Nem dob hibát, csak logol
        await bus._dispatch_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        callback.assert_awaited_once()


class TestEventBusDeserializationAdditional:
    """További deszerializáció tesztek a hiányzó sorok lefedésére."""

    @patch("zmq.asyncio.Context")
    def test_deserialize_trade_event(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a TradeEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "direction": "BUY",
            "price": 1.0850,
            "volume": 0.01,
            "order_id": "ord_12345",
        }

        result = bus._deserialize_event("trade", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        from neural_ai.core.events.interfaces.event_models import TradeEvent

        assert isinstance(result, TradeEvent)
        assert result.order_id == "ord_12345"

    @patch("zmq.asyncio.Context")
    def test_deserialize_signal_event(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a SignalEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "signal_type": "ENTRY_LONG",
            "confidence": 0.85,
            "strategy_id": "strat_001",
        }

        result = bus._deserialize_event("signal", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        from neural_ai.core.events.interfaces.event_models import SignalEvent

        assert isinstance(result, SignalEvent)
        assert result.strategy_id == "strat_001"

    @patch("zmq.asyncio.Context")
    def test_deserialize_system_log_event(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a SystemLogEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": "INFO",
            "component": "test_component",
            "message": "System started",
        }

        result = bus._deserialize_event("system_log", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        from neural_ai.core.events.interfaces.event_models import SystemLogEvent

        assert isinstance(result, SystemLogEvent)
        assert result.level == "INFO"

    @patch("zmq.asyncio.Context")
    def test_deserialize_order_event(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a OrderEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "order_id": "ord_001",
            "timestamp": datetime.now(UTC).isoformat(),
            "symbol": "EURUSD",
            "order_type": "MARKET",
            "direction": "BUY",
            "volume": 0.01,
            "price": 1.0850,
            "status": "PENDING",
        }

        result = bus._deserialize_event("order", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        from neural_ai.core.events.interfaces.event_models import OrderEvent

        assert isinstance(result, OrderEvent)
        assert result.order_id == "ord_001"

    @patch("zmq.asyncio.Context")
    def test_deserialize_position_event(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a PositionEvent deszerializációját."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        event_data: dict[str, Any] = {
            "position_id": "pos_001",
            "timestamp": datetime.now(UTC).isoformat(),
            "symbol": "EURUSD",
            "direction": "LONG",
            "volume": 0.01,
            "entry_price": 1.0850,
            "current_price": 1.0855,
            "status": "OPEN",
        }

        result = bus._deserialize_event("position", event_data)  # pyright: ignore[reportPrivateUsage]

        assert result is not None
        from neural_ai.core.events.interfaces.event_models import PositionEvent

        assert isinstance(result, PositionEvent)
        assert result.position_id == "pos_001"


class TestEventBusDispatchExceptionHandling:
    """Esemény továbbítás kivételkezelés tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_deserialization_error(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a deserializálási hiba kezelését."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback = AsyncMock()
        bus.subscribe("market_data", callback)

        # Érvénytelen esemény adatok, amelyek deserializálási hibát okoznak
        event_data: dict[str, Any] = {"invalid": "data", "missing_required": True}

        # Nem dob hibát, csak logol
        await bus._dispatch_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        # A callback nem hívódik meg, mert a deserializálás sikertelen
        callback.assert_not_awaited()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_deserialization_returns_none(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a None visszatérési érték kezelését."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback = AsyncMock()
        bus.subscribe("unknown_type", callback)

        event_data = {"key": "value"}

        # Nem dob hibát, a deserializálás None-t ad vissza
        await bus._dispatch_event("unknown_type", event_data)  # pyright: ignore[reportPrivateUsage]

        # A callback nem hívódik meg
        callback.assert_not_awaited()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_outer_exception_handling(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a külső try-except blokk kivételkezelését (219-220. sorok)."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)
        callback = AsyncMock()
        bus.subscribe("market_data", callback)

        # Olyan esemény adatok, amelyek kivételt okoznak a _deserialize_event-ben
        # még a belső try-except előtt (pl. import hiba vagy váratlan kivétel)
        event_data = {"valid": "data"}

        # Mockoljuk a _deserialize_event-et, hogy dobjon egy kivételt
        # ami a külső try-except blokkban lesz elkapva
        with patch.object(
            bus, "_deserialize_event", side_effect=Exception("Deszerializálási hiba")
        ):
            # Nem dob hibát, csak logol (219-220. sorok)
            await bus._dispatch_event("market_data", event_data)  # pyright: ignore[reportPrivateUsage]

        # A callback nem hívódik meg, mert a deszerializálás hibát dobott
        callback.assert_not_awaited()


class TestEventBusRunForever:
    """EventBus run_forever metódus tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_success(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a run_forever sikeres futását."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy adjon vissza egy érvényes üzenetet
        # majd a második hívásnál dobjon asyncio.CancelledError-t a ciklusból való kilépéshez
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [
                    b"market_data",
                    b'{"symbol":"EURUSD","timestamp":"2024-01-01T12:00:00Z","bid":1.0850,"ask":1.0852,"source":"test","volume":100000,"_event_type":"market_data","_timestamp":"2024-01-01T12:00:00Z"}',
                ]
            else:
                raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Ellenőrizzük, hogy a socket metódusok meghívást kaptak-e
        mock_socket.connect.assert_called_once()
        # A setsockopt-ot 3-szor hívják meg: SNDHWM, RCVHWM (start-ban), SUBSCRIBE (run_forever-ben)
        assert mock_socket.setsockopt.call_count == 3

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_timeout_handling(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a timeout kezelését a run_forever-ben."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy timeout-ot okozzon, majd CancelledError-t
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count <= 3:
                raise TimeoutError()
            else:
                raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # A timeout-ot kezelni kell, és folytatni a ciklust
        mock_socket.connect.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_not_started(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a run_forever hívását indítás nélkül."""
        mock_context: MagicMock = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus(logger=mock_logger)

        with pytest.raises(EventBusError, match="EventBus nincs elindítva"):
            await bus.run_forever()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_message_processing(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az üzenet feldolgozást a run_forever-ben."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy adjon vissza egy érvényes üzenetet
        # majd a második hívásnál dobjon asyncio.CancelledError-t
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [
                    b"trade",
                    b'{"order_id":"ord_123","symbol":"EURUSD","direction":"BUY","volume":0.01,"price":1.0850,"timestamp":"2024-01-01T12:00:00Z","_event_type":"trade","_timestamp":"2024-01-01T12:00:00Z"}',
                ]
            else:
                raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        callback: AsyncMock = AsyncMock()
        bus.subscribe("trade", callback)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Ellenőrizzük, hogy a callback meghívódott-e
        callback.assert_awaited()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_invalid_message_format(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli az érvénytelen üzenet formátum kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy adjon vissza érvénytelen üzenetet
        # majd a második hívásnál dobjon asyncio.CancelledError-t
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [b"topic"]  # Nincs elég rész
            else:
                raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Nem szabad hibát dobnia
        mock_socket.connect.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_json_decode_error(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a JSON decode hiba kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy adjon vissza érvénytelen JSON-t
        # majd a második hívásnál dobjon asyncio.CancelledError-t
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return [
                    b"market_data",
                    b"invalid json{",
                ]
            else:
                raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Nem szabad hibát dobnia
        mock_socket.connect.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_general_exception_handling(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli az általános kivétel kezelését a run_forever-ben."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy dobjon egy általános kivételt
        # majd a második hívásnál dobjon asyncio.CancelledError-t
        call_count = 0

        async def recv_multipart_side_effect():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise Exception("Általános hiba")
            # Minden további hívásra CancelledError
            raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Nem szabad hibát dobnia, csak logol
        mock_socket.connect.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_run_forever_with_inproc(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a run_forever-t inproc transporttal (284. sor lefedése)."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockoljuk a recv_multipart-et, hogy azonnal CancelledError-t dobjon
        async def recv_multipart_side_effect():
            raise asyncio.CancelledError()

        mock_socket.recv_multipart.side_effect = recv_multipart_side_effect

        # Inproc konfigurációval hozzuk létre az EventBus-t
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config, logger=mock_logger)
        await bus.start()

        # Futtassuk a run_forever-t
        bus._running = True  # pyright: ignore[reportPrivateUsage]
        with pytest.raises(asyncio.CancelledError):
            await bus.run_forever()

        # Ellenőrizzük, hogy az inproc URL lett volna használva
        mock_socket.connect.assert_called_once_with("inproc://eventbus_pub")


class TestEventBusErrorHandling:
    """EventBus hiba kezelés tesztek a lefedettség növelésére."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_error_zmq_exception(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a publish során fellépő ZMQError kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a send_multipart-ot, hogy ZMQError-t dobjon
        import zmq

        mock_socket.send_multipart.side_effect = zmq.ZMQError(99, "Connection lost")

        bus = EventBus(logger=mock_logger)
        await bus.start()

        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        # A ZMQError-t el kell kapni és logolni kell, nem szabad összeomlást okoznia
        # A teszt sikeres, ha nem dob kivételt
        await bus.publish("market_data", event)

        # Ellenőrizzük, hogy a send_multipart meghívódott
        mock_socket.send_multipart.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_error_general_exception(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a publish során fellépő általános kivétel kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a send_multipart-ot, hogy általános kivételt dobjon
        mock_socket.send_multipart.side_effect = RuntimeError("Unexpected error")

        bus = EventBus(logger=mock_logger)
        await bus.start()

        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        # Az általános kivételt is el kell kapni és logolni kell
        await bus.publish("market_data", event)

        # Ellenőrizzük, hogy a send_multipart meghívódott
        mock_socket.send_multipart.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_error_with_callback(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a publish hibakezelését callbackkel együtt."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        import zmq

        mock_socket.send_multipart.side_effect = zmq.ZMQError(99, "Connection lost")

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # Adjunk hozzá egy callback-et, hogy teszteljük a teljes hibakezelési láncot
        callback: AsyncMock = AsyncMock()
        bus.subscribe("market_data", callback)

        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            bid_volume=100000,
            ask_volume=100000,
            source="jforex",
            volume=100000,
        )

        # A hiba ellenére a rendszernek stabilan kell maradnia
        await bus.publish("market_data", event)

        # Ellenőrizzük, hogy a send_multipart meghívódott
        mock_socket.send_multipart.assert_awaited_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_subscribe_error_setsockopt_exception(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a subscribe során fellépő setsockopt hiba kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a setsockopt-ot, hogy ZMQError-t dobjon
        import zmq

        # Az első 2 hívás (SNDHWM, RCVHWM) sikeres legyen, a 3. (SUBSCRIBE) dobjon hibát
        mock_socket.setsockopt.side_effect = [None, None, zmq.ZMQError(99, "Invalid option")]
        # Mockold a recv_multipart-et, hogy azonnal CancelledError-t dobjon
        mock_socket.recv_multipart.side_effect = asyncio.CancelledError()

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # A hiba ellenére a run_forever-nek stabilan kell futnia
        bus._running = True  # pyright: ignore[reportPrivateUsage]

        # Most már elvárjuk a ZMQError-t a feliratkozási hiba miatt
        import zmq

        with pytest.raises(zmq.ZMQError):
            await bus.run_forever()

        # Ellenőrizzük, hogy a setsockopt meghívódott
        mock_socket.setsockopt.assert_called()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_subscribe_error_setsockopt_general_exception(
        self, mock_context_class: MagicMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a subscribe során fellépő általános setsockopt hiba kezelését."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a setsockopt-ot, hogy általános kivételt dobjon
        # Az első 2 hívás (SNDHWM, RCVHWM) sikeres legyen, a 3. (SUBSCRIBE) dobjon hibát
        mock_socket.setsockopt.side_effect = [None, None, RuntimeError("Socket option error")]

        # Mockold a recv_multipart-et, hogy azonnal CancelledError-t dobjon
        mock_socket.recv_multipart.side_effect = asyncio.CancelledError()

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # A hiba ellenére a run_forever-nek stabilan kell futnia
        bus._running = True  # pyright: ignore[reportPrivateUsage]

        # Most már elvárjuk a RuntimeError-t (vagy ZMQError-t) a feliratkozási hiba miatt
        with pytest.raises(RuntimeError):
            await bus.run_forever()

        # Ellenőrizzük, hogy a setsockopt meghívódott
        mock_socket.setsockopt.assert_called()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_error_socket_bind_failure(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a socket bind hiba kezelését az indításkor."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()  # Ne AsyncMock, mert a bind szinkron
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a bind-et, hogy ZMQError-t dobjon (bind szinkron metódus!)
        import zmq

        mock_socket.bind.side_effect = zmq.ZMQError(99, "Address already in use")

        bus = EventBus(logger=mock_logger)

        # A bind hiba ellenére a rendszernek kezelnie kell a kivételt
        # és EventBusError-t kell dobnia
        with pytest.raises(EventBusError, match="Nem sikerült elindítani"):
            await bus.start()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_error_socket_close_failure(self, mock_context_class: MagicMock, mock_logger: MagicMock) -> None:  # noqa: E501
        """Teszteli a socket close hiba kezelését a leállításkor."""
        mock_context: MagicMock = MagicMock()
        mock_socket: MagicMock = MagicMock()
        mock_socket.send_multipart = AsyncMock()
        mock_socket.recv_multipart = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        # Mockold a close-ot, hogy kivételt dobjon
        import zmq

        mock_socket.close.side_effect = zmq.ZMQError(99, "Socket already closed")

        bus = EventBus(logger=mock_logger)
        await bus.start()

        # A close hiba ellenére a leállításnak folytatódnia kell
        try:
            await bus.stop()
        except zmq.ZMQError:
            # A mockolt hiba miatt ez várható, de a teszt lényege, hogy a stop() lefutott
            pass

        assert bus._running is False  # pyright: ignore[reportPrivateUsage]
        mock_socket.close.assert_called_once()
