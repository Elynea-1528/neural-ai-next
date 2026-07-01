"""JForex Live Feed Integration Tests.

# pyright: reportArgumentType=false, reportPrivateUsage=false
# Async test fixture és protected member access hibák.

Ez a modul tartalmazza a JForexLiveFeed integrációs tesztjeit.
A tesztek a valós JForexLiveFeed logikát használják, de a ZMQ socketet mock-olják.
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import zmq

from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent


class TestJForexLiveFeedIntegration:
    """JForexLiveFeed integrációs tesztjei."""

    @pytest.fixture(scope="function")
    def mock_logger(self) -> MagicMock:
        """Mock logger létrehozása."""
        logger = MagicMock()
        logger.info = MagicMock()
        logger.warning = MagicMock()
        logger.error = MagicMock()
        logger.debug = MagicMock()
        return logger

    @pytest.fixture(scope="function")
    def mock_event_bus(self) -> AsyncMock:
        """Mock event bus létrehozása."""
        event_bus = AsyncMock()
        event_bus.publish = AsyncMock()
        return event_bus

    @pytest.fixture(scope="function")
    def mock_config(self) -> MagicMock:
        """Mock config létrehozása."""
        config = MagicMock()
        config.get.return_value = {
            "enabled": True,
            "host": "127.0.0.1",
            "tick_port": 5555,
            "command_port": 5556,
        }
        return config

    @pytest.fixture(scope="function")
    def live_feed(
        self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config: MagicMock
    ) -> JForexLiveFeed:
        """JForexLiveFeed példány létrehozása (VALÓS, NEM mock)."""
        return JForexLiveFeed(logger=mock_logger, event_bus=mock_event_bus, config=mock_config)

    @pytest.mark.asyncio
    async def test_valid_json_creates_market_data_event(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy érvényes JSON input MarketDataEvent-et hoz létre."""
        tick_data = {
            "symbol": "EURUSD",
            "timestamp": 1735729200000,  # ms
            "bid": 1.10000,
            "ask": 1.10010,
            "volume": 1000,
        }

        await live_feed._process_tick_data(tick_data)  # pyright: ignore[reportPrivateUsage, reportArgumentType]

        # Ellenőrizzük, hogy az esemény publikálva lett
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args

        # Topic ellenőrzés
        assert call_args[0][0] == "market_data"

        # MarketDataEvent ellenőrzés
        event = call_args[0][1]
        assert isinstance(event, MarketDataEvent)
        assert event.symbol == "EURUSD"
        assert event.bid == 1.10000
        assert event.ask == 1.10010
        assert event.source == "jforex"

    @pytest.mark.asyncio
    async def test_invalid_json_handles_gracefully(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy hibás JSON string gracefully kezelődik."""
        invalid_json = "not a json string"

        # Simuláljuk a listen loop JSON parse hibát
        with patch.object(live_feed, "_socket") as mock_socket:

            async def mock_recv():
                return invalid_json

            mock_socket.recv_string = mock_recv
            live_feed._running = True  # pyright: ignore[reportPrivateUsage]

            # Egy iterációt futtatunk
            task = asyncio.create_task(live_feed._listen_loop())  # pyright: ignore[reportPrivateUsage]
            await asyncio.sleep(0.1)

            live_feed._running = False  # pyright: ignore[reportPrivateUsage]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Ellenőrizzük, hogy error log lett írva
        mock_logger.error.assert_called()

    @pytest.mark.asyncio
    async def test_missing_required_fields(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy hiányzó kötelező mezők esetén error log történik."""
        incomplete_data = {"timestamp": 1735729200000, "bid": 1.10000}

        await live_feed._process_tick_data(incomplete_data)  # type: ignore[arg-type]

        # Ellenőrizzük, hogy error log lett írva
        mock_logger.error.assert_called()
        # Az esemény NEM lett publikálva
        mock_event_bus.publish.assert_not_called()

    @pytest.mark.asyncio
    async def test_negative_bid_price(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy negatív bid ár Pydantic validáció hibát okoz."""
        bad_data = {
            "symbol": "EURUSD",
            "timestamp": 1735729200000,
            "bid": -1.0,
            "ask": 1.10010,
        }

        await live_feed._process_tick_data(bad_data)  # pyright: ignore[reportPrivateUsage, reportArgumentType]

        # Ellenőrizzük, hogy error log lett írva (Pydantic validáció hiba)
        mock_logger.error.assert_called()
        # Az esemény NEM lett publikálva
        mock_event_bus.publish.assert_not_called()

    @pytest.mark.asyncio
    async def test_multiple_ticks_sequential(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock
    ) -> None:
        """Teszteli, hogy több tick egymás után feldolgozható."""
        ticks = [
            {
                "symbol": "EURUSD",
                "timestamp": 1735729200000,
                "bid": 1.10000,
                "ask": 1.10010,
                "volume": 100,
            },
            {
                "symbol": "GBPUSD",
                "timestamp": 1735729201000,
                "bid": 1.27000,
                "ask": 1.27010,
                "volume": 200,
            },
        ]

        for tick in ticks:
            await live_feed._process_tick_data(tick)  # pyright: ignore[reportPrivateUsage, reportArgumentType]

        # Ellenőrizzük, hogy mindkét esemény publikálva lett
        assert mock_event_bus.publish.call_count == 2

        # Első event ellenőrzés
        first_call = mock_event_bus.publish.call_args_list[0]
        first_event = first_call[0][1]
        assert first_event.symbol == "EURUSD"
        assert first_event.bid == 1.10000

        # Második event ellenőrzés
        second_call = mock_event_bus.publish.call_args_list[1]
        second_event = second_call[0][1]
        assert second_event.symbol == "GBPUSD"
        assert second_event.bid == 1.27000

    @pytest.mark.asyncio
    async def test_zmq_socket_mock_full_flow(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock
    ) -> None:
        """Teszteli a teljes flowt: ZMQ context → socket → recv_string → MarketDataEvent."""
        tick_message = json.dumps(
            {
                "symbol": "EURUSD",
                "timestamp": 1735729200000,
                "bid": 1.10000,
                "ask": 1.10010,
                "volume": 1000,
            }
        )

        with patch("zmq.asyncio.Context") as mock_context_class:
            mock_context = MagicMock()
            mock_socket = MagicMock()
            mock_context_class.return_value = mock_context
            mock_context.socket.return_value = mock_socket

            # Socket recv_string mock
            call_count = 0

            async def mock_recv():
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return tick_message
                else:
                    raise asyncio.CancelledError()

            mock_socket.recv_string = mock_recv

            # Live feed indítása
            await live_feed.start()

            # Rövid várakozás
            await asyncio.sleep(0.2)

            # Live feed leállítása
            await live_feed.stop()

        # Ellenőrizzük, hogy az esemény publikálva lett MarketDataEvent-tel
        mock_event_bus.publish.assert_called()
        call_args = mock_event_bus.publish.call_args
        event = call_args[0][1]
        assert isinstance(event, MarketDataEvent)
        assert event.symbol == "EURUSD"

    @pytest.mark.asyncio
    async def test_reconnect_on_socket_error(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy socket ZMQError esetén a listen loop nem crashel, hanem logol."""
        with patch.object(live_feed, "_socket") as mock_socket:

            async def mock_recv():
                raise zmq.ZMQError("Socket error")  # type: ignore[arg-type]

            mock_socket.recv_string = mock_recv
            live_feed._running = True  # pyright: ignore[reportPrivateUsage]

            # Egy iterációt futtatunk
            task = asyncio.create_task(live_feed._listen_loop())  # pyright: ignore[reportPrivateUsage]
            await asyncio.sleep(0.1)

            live_feed._running = False  # pyright: ignore[reportPrivateUsage]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        # Ellenőrizzük, hogy error log lett írva
        mock_logger.error.assert_called()

    @pytest.mark.asyncio
    async def test_event_bus_publish_called_with_correct_topic(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock
    ) -> None:
        """Teszteli, hogy az event bus publish mindig 'market_data' topickal hívódik."""
        tick_data = {
            "symbol": "EURUSD",
            "timestamp": 1735729200000,
            "bid": 1.10000,
            "ask": 1.10010,
            "volume": 1000,
        }

        await live_feed._process_tick_data(tick_data)  # pyright: ignore[reportPrivateUsage, reportArgumentType]

        # Ellenőrizzük, hogy a topic 'market_data'
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args
        assert call_args[0][0] == "market_data"
