"""JForex Live Feed Tests.

# pyright: reportArgumentType=false, reportPrivateUsage=false
# Async test fixture és protected member access hibák.

Ez a modul tartalmazza a JForexLiveFeed osztály tesztjeit.
"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import zmq

from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed
from neural_ai.core.events.interfaces.event_models import MarketDataEvent


class TestJForexLiveFeed:
    """JForexLiveFeed osztály tesztjei."""

    @pytest.fixture
    def mock_logger(self) -> MagicMock:
        """Mock logger létrehozása."""
        logger = MagicMock()
        logger.info = MagicMock()
        logger.warning = MagicMock()
        logger.error = MagicMock()
        logger.debug = MagicMock()
        return logger

    @pytest.fixture
    def mock_event_bus(self) -> AsyncMock:
        """Mock event bus létrehozása."""
        event_bus = AsyncMock()
        event_bus.publish = AsyncMock()
        return event_bus

    @pytest.fixture
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

    @pytest.fixture
    def live_feed(
        self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config: MagicMock
    ) -> JForexLiveFeed:
        """JForexLiveFeed példány létrehozása."""
        return JForexLiveFeed(logger=mock_logger, event_bus=mock_event_bus, config=mock_config)

    @pytest.mark.asyncio
    async def test_start_success(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None:
        """Teszteli a start metódus sikeres futását."""
        with patch("zmq.asyncio.Context") as mock_context:
            mock_socket = MagicMock()
            mock_context.return_value.socket.return_value = mock_socket

            await live_feed.start()

            # Ellenőrizzük, hogy a socket létrejött és csatlakozott
            mock_context.assert_called_once()
            mock_socket.connect.assert_called_once_with("tcp://127.0.0.1:5555")
            mock_socket.setsockopt_string.assert_called_once_with(zmq.SUBSCRIBE, "")

            # Ellenőrizzük, hogy futási állapot beállításra került
            assert live_feed.is_running() is True
            assert live_feed._listen_task is not None

            # Naplózás ellenőrzése
            mock_logger.info.assert_called()

    @pytest.mark.asyncio
    async def test_start_when_already_running(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy a start metódus figyelmeztet, ha már fut a feed."""
        live_feed._running = True

        await live_feed.start()

        # Ellenőrizzük, hogy warning lett naplózva
        mock_logger.warning.assert_called_once_with("jforex_live_feed_already_running")

    @pytest.mark.asyncio
    async def test_stop_success(self, live_feed: JForexLiveFeed, mock_logger: MagicMock) -> None:
        """Teszteli a stop metódus sikeres futását."""
        # Elindítjuk a feedet
        with patch("zmq.asyncio.Context"):
            await live_feed.start()

        # Leállítjuk
        await live_feed.stop()

        # Ellenőrizzük, hogy leállt
        assert live_feed.is_running() is False
        assert live_feed._listen_task is None
        assert live_feed._socket is None
        assert live_feed._context is None

        # Naplózás ellenőrzése
        mock_logger.info.assert_called()

    @pytest.mark.asyncio
    async def test_stop_when_not_running(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy a stop metódus nem csinál semmit, ha nem fut a feed."""
        live_feed._running = False

        await live_feed.stop()

        # Ellenőrizzük, hogy nem volt naplózás
        mock_logger.info.assert_not_called()

    @pytest.mark.asyncio
    async def test_process_tick_data_success(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock, mock_logger: MagicMock
    ) -> None:
        """Teszteli a tick adatok feldolgozását."""
        # Tick adatok létrehozása (timestamp milliszekundumban)
        tick_data = {
            "symbol": "EURUSD",
            "timestamp": 1735729200000,  # 2025-01-01 12:00:00 UTC milliszekundumban
            "bid": 1.10000,
            "ask": 1.10010,
            "volume": 1000,
        }

        await live_feed._process_tick_data(tick_data)

        # Ellenőrizzük, hogy az esemény publikálva lett
        mock_event_bus.publish.assert_called_once()
        call_args = mock_event_bus.publish.call_args

        # Az első argumentum a topic
        assert call_args[0][0] == "market_data"

        # A második argumentum a MarketDataEvent
        event = call_args[0][1]
        assert isinstance(event, MarketDataEvent)
        assert event.symbol == "EURUSD"
        assert event.bid == 1.10000
        assert event.ask == 1.10010
        assert event.source == "jforex"

    @pytest.mark.asyncio
    async def test_process_tick_data_error(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli a hibakezelést tick adatok feldolgozásakor."""
        # Érvénytelen tick adatok
        invalid_data = {
            "symbol": "EURUSD",
            "timestamp": "invalid_timestamp",  # Érvénytelen időbélyeg
            "bid": "invalid_bid",  # Érvénytelen bid
            "ask": 1.10010,
        }

        await live_feed._process_tick_data(invalid_data)

        # Ellenőrizzük, hogy hiba lett naplózva
        mock_logger.error.assert_called_once()

    @pytest.mark.asyncio
    async def test_listen_loop_processes_tick(
        self, live_feed: JForexLiveFeed, mock_event_bus: AsyncMock
    ) -> None:
        """Teszteli, hogy a listen loop feldolgozza a tick üzeneteket."""
        # Tick üzenet létrehozása (timestamp milliszekundumban)
        tick_message = json.dumps(
            {
                "symbol": "EURUSD",
                "timestamp": 1735729200000,  # 2025-01-01 12:00:00 UTC milliszekundumban
                "bid": 1.10000,
                "ask": 1.10010,
                "volume": 1000,
            }
        )

        with patch.object(live_feed, "_socket") as mock_socket:
            # Beállítjuk a socket recv_string metódusát, hogy egyszer adjon
            # vissza üzenetet, majd dobjon CancelledErrort
            call_count = 0

            async def mock_recv():
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return tick_message
                else:
                    raise asyncio.CancelledError()

            mock_socket.recv_string = mock_recv

            # Indítjuk a listen loopot
            live_feed._running = True
            task = asyncio.create_task(live_feed._listen_loop())

            # Várunk, hogy a loop feldolgozza az üzenetet, de max 1 másodpercig
            try:
                await asyncio.wait_for(task, timeout=1.0)
            except (TimeoutError, asyncio.CancelledError):
                pass
            finally:
                live_feed._running = False
                if not task.done():
                    task.cancel()

            # Ellenőrizzük, hogy az esemény publikálva lett
            mock_event_bus.publish.assert_called()

    def test_is_running_returns_correct_state(self, live_feed: JForexLiveFeed) -> None:
        """Teszteli, hogy az is_running metódus helyes állapotot adja vissza."""
        # Kezdetben nem fut
        assert live_feed.is_running() is False

        # Futási állapot beállítása
        live_feed._running = True
        assert live_feed.is_running() is True

        # Visszaállítás
        live_feed._running = False
        assert live_feed.is_running() is False

    @pytest.fixture
    def mock_config_empty(self) -> MagicMock:
        """Mock config létrehozása üres configgal."""
        config = MagicMock()
        config.get.return_value = {}
        return config

    @pytest.fixture
    def live_feed_empty_config(
        self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config_empty: MagicMock
    ) -> JForexLiveFeed:
        """JForexLiveFeed példány létrehozása üres configgal."""
        return JForexLiveFeed(
            logger=mock_logger, event_bus=mock_event_bus, config=mock_config_empty
        )

    def test_init_with_empty_config_logs_warning(
        self, live_feed_empty_config: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy üres config esetén warning log jelenik meg."""
        # Az inicializálás során warningnak kell lennie
        mock_logger.warning.assert_called_once_with(
            "jforex_live_config_missing - Using defaults (5555)"
        )

    @pytest.fixture
    def mock_config_with_data(self) -> MagicMock:
        """Mock config létrehozása config adatokkal."""
        config = MagicMock()

        def mock_get(section, key=None, **kwargs):
            if section == "collectors" and key == "jforex_live":
                return {
                    "host": "127.0.0.1",
                    "tick_port": 5555,
                    "command_port": 5556,
                }
            return None

        config.get.side_effect = mock_get
        return config

    @pytest.fixture
    def live_feed_with_config(
        self, mock_logger: MagicMock, mock_event_bus: AsyncMock, mock_config_with_data: MagicMock
    ) -> JForexLiveFeed:
        """JForexLiveFeed példány létrehozása config adatokkal."""
        return JForexLiveFeed(
            logger=mock_logger, event_bus=mock_event_bus, config=mock_config_with_data
        )

    def test_init_with_config_logs_debug(
        self, live_feed_with_config: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy config adatok esetén debug log jelenik meg."""
        # Az inicializálás során debug log-nak kell lennie
        mock_logger.debug.assert_called_once()

    @pytest.mark.asyncio
    async def test_start_raises_exception_on_zmq_failure(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy start exception-t dob ZMQ hiba esetén."""
        with patch("zmq.asyncio.Context", side_effect=Exception("ZMQ Error")):
            with pytest.raises(Exception, match="ZMQ Error"):
                await live_feed.start()

            # Ellenőrizzük, hogy error log lett írva
            mock_logger.error.assert_called_once()
            # És stop lett hívva
            assert not live_feed.is_running()

    @pytest.mark.asyncio
    async def test_listen_loop_handles_socket_none(
        self, live_feed: JForexLiveFeed, mock_logger: MagicMock
    ) -> None:
        """Teszteli, hogy listen loop kezeli, ha socket None."""
        # Socket None-ra állítása
        live_feed._socket = None
        live_feed._running = True

        # Rövid időre futtatjuk a loop-ot
        task = asyncio.create_task(live_feed._listen_loop())
        await asyncio.sleep(0.2)  # Várunk egy kicsit, hogy lefusson a sleep

        # Leállítjuk
        live_feed._running = False
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        # Nem szabad error-t logolni, mert csak sleep volt
        mock_logger.error.assert_not_called()
