"""Tesztek a ZeroMQBus implementációhoz.

Ez a modul tartalmazza a ZeroMQBus tesztjeit, ZMQ mocking-gal.

Author: Neural AI Next Team
Version: 1.0.0
"""

from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from neural_ai.core.events.exceptions.event_error import EventBusError, PublishError
from neural_ai.core.events.implementations.zeromq_bus import EventBus
from neural_ai.core.events.interfaces.event_bus_interface import EventBusConfig
from neural_ai.core.events.interfaces.event_models import MarketDataEvent


@pytest.fixture(autouse=True)
def reset_singleton():
    """Singleton reset minden teszt előtt."""
    # Mentsük el az eredeti _instances szótárt
    from neural_ai.core.base.implementations.singleton import SingletonMeta
    original_instances = getattr(SingletonMeta, "_instances", {}).copy()

    yield

    # Állítsuk vissza az eredeti állapotot
    SingletonMeta._instances = original_instances


class TestEventBusInitialization:
    """EventBus inicializálás tesztek."""

    @patch("zmq.asyncio.Context")
    def test_default_initialization(self, mock_context_class: MagicMock) -> None:
        """Teszteli az alapértelmezett inicializálást."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()

        assert bus.config.pub_port == 5555
        assert bus.config.sub_port == 5556
        assert bus.config.use_inproc is False

    @patch("zmq.asyncio.Context")
    def test_custom_config_initialization(self, mock_context_class: MagicMock) -> None:
        """Teszteli az egyéni konfigurációval történő inicializálást."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        config = EventBusConfig(pub_port=6666, sub_port=6667, use_inproc=True)
        bus = EventBus(config)

        assert bus.config.pub_port == 6666
        assert bus.config.sub_port == 6667
        assert bus.config.use_inproc is True

    @patch("zmq.asyncio.Context")
    def test_external_zmq_context(self, mock_context_class: MagicMock) -> None:
        """Teszteli a külső ZMQ kontextus használatát."""
        external_context = MagicMock()
        config = EventBusConfig(zmq_context=external_context)
        bus = EventBus(config)

        assert bus._own_context is False
        assert bus._context is external_context

    def test_zmq_import_error(self) -> None:
        """Teszteli a ZMQ import hibát."""
        with patch.dict("sys.modules", {"zmq": None, "zmq.asyncio": None}):
            with pytest.raises(ImportError, match="ZeroMQ nincs telepítve"):
                EventBus()


class TestEventBusStartStop:
    """EventBus indítás és leállítás tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_success(self, mock_context_class: MagicMock) -> None:
        """Teszteli a sikeres indítást."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.start()

        assert bus._running is True
        mock_context.socket.assert_called_once()
        mock_socket.bind.assert_called_once_with("tcp://*:5555")

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_with_inproc(self, mock_context_class: MagicMock) -> None:
        """Teszteli az indítást inproc transporttal."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config)
        await bus.start()

        assert bus._running is True
        mock_socket.bind.assert_called_once_with("inproc://eventbus_pub")

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_start_twice(self, mock_context_class: MagicMock) -> None:
        """Teszteli a többszöri indítást."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.start()
        await bus.start()  # Másodszor is meghívjuk

        # Csak egyszer hívódjon meg a bind
        assert mock_socket.bind.call_count == 1

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_success(self, mock_context_class: MagicMock) -> None:
        """Teszteli a sikeres leállítást."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.start()
        await bus.stop()

        assert bus._running is False
        mock_socket.close.assert_called_once()

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_without_start(self, mock_context_class: MagicMock) -> None:
        """Teszteli a leállítást indítás nélkül."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.stop()  # Nem dob hibát

        assert bus._running is False

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_stop_twice(self, mock_context_class: MagicMock) -> None:
        """Teszteli a többszöri leállítást."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.start()
        await bus.stop()
        await bus.stop()  # Másodszor is meghívjuk

        assert bus._running is False


class TestEventBusPublish:
    """EventBus publish tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_success(self, mock_context_class: MagicMock) -> None:
        """Teszteli a sikeres esemény közzétételt."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        bus = EventBus()
        await bus.start()

        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
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
    async def test_publish_not_started(self, mock_context_class: MagicMock) -> None:
        """Teszteli a közzétételt indítás nélkül."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            source="jforex",
            volume=100000,
        )

        with pytest.raises(EventBusError, match="EventBus nincs elindítva"):
            await bus.publish("market_data", event)

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_publish_no_publisher(self, mock_context_class: MagicMock) -> None:
        """Teszteli a közzétételt publisher socket nélkül."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        bus._running = True  # Elindítva, de nincs publisher
        event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0852,
            source="jforex",
            volume=100000,
        )

        with pytest.raises(PublishError, match="Publisher socket nincs inicializálva"):
            await bus.publish("market_data", event)


class TestEventBusSubscribeUnsubscribe:
    """EventBus feliratkozás és leiratkozás tesztek."""

    @patch("zmq.asyncio.Context")
    def test_subscribe_new_event_type(self, mock_context_class: MagicMock) -> None:
        """Teszteli az új eseménytípusra való feliratkozást."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = MagicMock()

        bus.subscribe("market_data", callback)

        assert "market_data" in bus._subscribers
        assert callback in bus._subscribers["market_data"]

    @patch("zmq.asyncio.Context")
    def test_subscribe_multiple_callbacks(self, mock_context_class: MagicMock) -> None:
        """Teszteli több callback feliratkozását ugyanarra az eseménytípusra."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback1 = MagicMock()
        callback2 = MagicMock()

        bus.subscribe("market_data", callback1)
        bus.subscribe("market_data", callback2)

        assert len(bus._subscribers["market_data"]) == 2
        assert callback1 in bus._subscribers["market_data"]
        assert callback2 in bus._subscribers["market_data"]

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_existing(self, mock_context_class: MagicMock) -> None:
        """Teszteli a létező feliratkozás lemondását."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = MagicMock()

        bus.subscribe("market_data", callback)
        bus.unsubscribe("market_data", callback)

        assert "market_data" in bus._subscribers
        assert callback not in bus._subscribers["market_data"]

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_non_existing(self, mock_context_class: MagicMock) -> None:
        """Teszteli a nem létező feliratkozás lemondását."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = MagicMock()

        # Nem dob hibát
        bus.unsubscribe("market_data", callback)

    @patch("zmq.asyncio.Context")
    def test_unsubscribe_non_existing_event_type(
        self, mock_context_class: MagicMock
    ) -> None:
        """Teszteli a nem létező eseménytípus lemondását."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = MagicMock()

        # Nem dob hibát
        bus.unsubscribe("non_existing", callback)


class TestEventBusContextManager:
    """EventBus context manager tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_async_context_manager(self, mock_context_class: MagicMock) -> None:
        """Teszteli az aszinkron context managert."""
        mock_context = MagicMock()
        mock_socket = AsyncMock()
        mock_context.socket.return_value = mock_socket
        mock_context_class.return_value = mock_context

        async with EventBus() as bus:
            assert bus._running is True

        assert bus._running is False


class TestEventBusDeserialization:
    """EventBus deszerializáció tesztek."""

    @patch("zmq.asyncio.Context")
    def test_deserialize_market_data(self, mock_context_class: MagicMock) -> None:
        """Teszteli a MarketDataEvent deszerializációját."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        event_data = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        result = bus._deserialize_event("market_data", event_data)

        assert result is not None
        assert isinstance(result, MarketDataEvent)
        assert result.symbol == "EURUSD"
        assert result.bid == 1.0850

    @patch("zmq.asyncio.Context")
    def test_deserialize_unknown_event_type(
        self, mock_context_class: MagicMock
    ) -> None:
        """Teszteli az ismeretlen eseménytípus deszerializációját."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        event_data = {"key": "value"}

        result = bus._deserialize_event("unknown_type", event_data)

        assert result is None

    @patch("zmq.asyncio.Context")
    def test_deserialize_invalid_data(self, mock_context_class: MagicMock) -> None:
        """Teszteli az érvénytelen adat deszerializációját."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        event_data = {"invalid": "data"}

        result = bus._deserialize_event("market_data", event_data)

        assert result is None


class TestEventBusDispatch:
    """EventBus esemény továbbítás tesztek."""

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_success(self, mock_context_class: MagicMock) -> None:
        """Teszteli a sikeres esemény továbbítást."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = AsyncMock()
        bus.subscribe("market_data", callback)

        event_data = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        await bus._dispatch_event("market_data", event_data)

        callback.assert_awaited_once()
        assert callback.await_args is not None
        called_with = callback.await_args[0][0]
        assert isinstance(called_with, MarketDataEvent)
        assert called_with.symbol == "EURUSD"

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_no_subscribers(
        self, mock_context_class: MagicMock
    ) -> None:
        """Teszteli az esemény továbbítást feliratkozók nélkül."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()

        event_data = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        # Nem dob hibát
        await bus._dispatch_event("market_data", event_data)

    @pytest.mark.asyncio
    @patch("zmq.asyncio.Context")
    async def test_dispatch_event_callback_error(
        self, mock_context_class: MagicMock
    ) -> None:
        """Teszteli a callback hibát."""
        mock_context = MagicMock()
        mock_context_class.return_value = mock_context

        bus = EventBus()
        callback = AsyncMock(side_effect=Exception("Callback hiba"))
        bus.subscribe("market_data", callback)

        event_data = {
            "symbol": "EURUSD",
            "timestamp": datetime.now(UTC).isoformat(),
            "bid": 1.0850,
            "ask": 1.0852,
            "source": "jforex",
            "volume": 100000,
        }

        # Nem dob hibát, csak logol
        await bus._dispatch_event("market_data", event_data)

        callback.assert_awaited_once()
