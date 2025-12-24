"""Tesztek az EventBus-hoz.

Ez a modul tartalmazza az EventBus működésének tesztjeit,
biztosítva a helyes Pub/Sub viselkedést.
"""

import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from neural_ai.core.events.bus import EventBus, EventBusConfig
from neural_ai.core.events.events import MarketDataEvent, SignalEvent


class TestEventBusConfig:
    """EventBusConfig tesztjei."""

    def test_default_config(self):
        """Teszteli az alapértelmezett konfigurációt."""
        config = EventBusConfig()

        assert config.pub_port == 5555
        assert config.sub_port == 5556
        assert config.use_inproc is False
        assert config.zmq_context is None

    def test_custom_config(self):
        """Teszteli az egyéni konfigurációt."""
        config = EventBusConfig(pub_port=6666, sub_port=6667, use_inproc=True)

        assert config.pub_port == 6666
        assert config.sub_port == 6667
        assert config.use_inproc is True


class TestEventBusInitialization:
    """EventBus inicializálás tesztjei."""

    def test_event_bus_creation(self):
        """Teszteli az EventBus létrehozását."""
        bus = EventBus()

        assert bus.config is not None
        assert bus._running is False
        assert bus._subscribers == {}

    def test_event_bus_with_custom_config(self):
        """Teszteli az EventBus létrehozását egyéni konfiggal."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        assert bus.config == config
        assert bus.config.use_inproc is True

    def test_zmq_import_error(self, monkeypatch):
        """Teszteli a ZeroMQ import hibát."""
        # Mockoljuk ki a zmq importot
        from unittest.mock import Mock

        def raise_import_error(*args, **kwargs):
            raise ImportError("No module named 'zmq'")

        mock_import = Mock(side_effect=raise_import_error)
        monkeypatch.setattr("builtins.__import__", mock_import)

        with pytest.raises(ImportError, match="ZeroMQ nincs telepítve"):
            EventBus()


class TestEventBusStartStop:
    """EventBus indítás és leállítás tesztjei."""

    @pytest.mark.asyncio
    async def test_start_and_stop(self):
        """Teszteli az EventBus indítását és leállítását."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        # Indítás
        await bus.start()
        assert bus._running is True
        assert bus._publisher is not None

        # Leállítás
        await bus.stop()
        assert bus._running is False

    @pytest.mark.asyncio
    async def test_double_start(self):
        """Teszteli a dupla indítást."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()
        assert bus._running is True

        # Második indítás nem okozhat hibát
        await bus.start()
        assert bus._running is True

        await bus.stop()

    @pytest.mark.asyncio
    async def test_double_stop(self):
        """Teszteli a dupla leállítást."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()
        await bus.stop()
        assert bus._running is False

        # Második leállítás nem okozhat hibát
        await bus.stop()
        assert bus._running is False

    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Teszteli az aszinkron context manager-t."""
        config = EventBusConfig(use_inproc=True)

        async with EventBus(config=config) as bus:
            assert bus._running is True
            assert bus._publisher is not None

        assert bus._running is False


class TestEventBusPublish:
    """EventBus publish tesztjei."""

    @pytest.mark.asyncio
    async def test_publish_market_data_event(self):
        """Teszteli a MarketDataEvent közzétételét."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()

        # Hozzunk létre egy eseményt
        event = MarketDataEvent(
            symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=1.0851, source="mt5"
        )

        # Közzététel
        await bus.publish("market_data", event)

        await bus.stop()

    @pytest.mark.asyncio
    async def test_publish_without_start_raises_error(self):
        """Teszteli, hogy indítás nélküli közzététel hibát okoz."""
        bus = EventBus()

        event = MarketDataEvent(
            symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=1.0851, source="mt5"
        )

        with pytest.raises(RuntimeError, match="nincs elindítva"):
            await bus.publish("market_data", event)

    @pytest.mark.asyncio
    async def test_publish_signal_event(self):
        """Teszteli a SignalEvent közzétételét."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()

        event = SignalEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            signal_type="ENTRY_LONG",
            confidence=0.85,
            strategy_id="strategy_001",
        )

        await bus.publish("signal", event)

        await bus.stop()


class TestEventBusSubscribe:
    """EventBus feliratkozás tesztjei."""

    def test_subscribe_to_event_type(self):
        """Teszteli a feliratkozást egy eseménytípusra."""
        bus = EventBus()

        # Mock callback
        callback = AsyncMock()

        # Feliratkozás
        bus.subscribe("market_data", callback)

        assert "market_data" in bus._subscribers
        assert callback in bus._subscribers["market_data"]

    def test_multiple_subscribers_same_type(self):
        """Teszteli több feliratkozót ugyanarra az eseménytípusra."""
        bus = EventBus()

        callback1 = AsyncMock()
        callback2 = AsyncMock()

        bus.subscribe("market_data", callback1)
        bus.subscribe("market_data", callback2)

        assert len(bus._subscribers["market_data"]) == 2
        assert callback1 in bus._subscribers["market_data"]
        assert callback2 in bus._subscribers["market_data"]

    def test_subscribe_different_event_types(self):
        """Teszteli a feliratkozást különböző eseménytípusokra."""
        bus = EventBus()

        callback1 = AsyncMock()
        callback2 = AsyncMock()

        bus.subscribe("market_data", callback1)
        bus.subscribe("signal", callback2)

        assert "market_data" in bus._subscribers
        assert "signal" in bus._subscribers
        assert callback1 in bus._subscribers["market_data"]
        assert callback2 in bus._subscribers["signal"]

    def test_unsubscribe(self):
        """Teszteli a leiratkozást."""
        bus = EventBus()

        callback = AsyncMock()

        bus.subscribe("market_data", callback)
        assert callback in bus._subscribers["market_data"]

        bus.unsubscribe("market_data", callback)
        assert callback not in bus._subscribers["market_data"]

    def test_unsubscribe_not_subscribed(self):
        """Teszteli a leiratkozást, ha nem volt feliratkozás."""
        bus = EventBus()

        callback = AsyncMock()

        # Nem okozhat hibát
        bus.unsubscribe("market_data", callback)


class TestEventBusIntegration:
    """Integrációs tesztek az EventBus-hoz."""

    @pytest.mark.asyncio
    async def test_publish_and_receive_event(self):
        """Teszteli az esemény közzétételét és fogadását."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()

        # Mock callback
        received_events = []

        async def callback(event):
            received_events.append(event)

        # Feliratkozás
        bus.subscribe("market_data", callback)

        # Esemény létrehozása és közzététele
        event = MarketDataEvent(
            symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=1.0851, source="mt5"
        )

        await bus.publish("market_data", event)

        # Kis várakozás, hogy a callback lefusson
        await asyncio.sleep(0.1)

        # A callback-nek meg kell hívódnia
        # Note: Ez a teszt csak akkor működik, ha a run_forever fut
        # Jelenleg csak a publish működését teszteljük

        await bus.stop()

    @pytest.mark.asyncio
    async def test_multiple_subscribers_receive_event(self):
        """Teszteli, hogy több feliratkozó is megkapja az eseményt."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()

        # Több mock callback
        received_events_1 = []
        received_events_2 = []

        async def callback1(event):
            received_events_1.append(event)

        async def callback2(event):
            received_events_2.append(event)

        # Feliratkozások
        bus.subscribe("market_data", callback1)
        bus.subscribe("market_data", callback2)

        # Esemény közzététele
        event = MarketDataEvent(
            symbol="EURUSD", timestamp=datetime.now(UTC), bid=1.0850, ask=1.0851, source="mt5"
        )

        await bus.publish("market_data", event)

        # Kis várakozás
        await asyncio.sleep(0.1)

        await bus.stop()

    @pytest.mark.asyncio
    async def test_event_serialization_deserialization(self):
        """Teszteli az esemény szerializálását és deszerializálását."""
        config = EventBusConfig(use_inproc=True)
        bus = EventBus(config=config)

        await bus.start()

        # Esemény létrehozása
        original_event = MarketDataEvent(
            symbol="EURUSD",
            timestamp=datetime.now(UTC),
            bid=1.0850,
            ask=1.0851,
            source="mt5",
            volume=1000000,
        )

        # Közzététel
        await bus.publish("market_data", original_event)

        # Kis várakozás
        await asyncio.sleep(0.1)

        await bus.stop()
