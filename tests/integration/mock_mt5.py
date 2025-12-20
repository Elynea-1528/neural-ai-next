"""Mock MT5 implementation for integration testing.

Provides a complete simulation of MT5 API without requiring actual MT5 installation.
"""

import random
from datetime import datetime, timedelta
from typing import Any


class MockMT5:
    """Mock MT5 API for testing purposes."""

    def __init__(self):
        """Inicializálja a Mock MT5 példányt."""
        self._initialized = False
        self._connected = False
        self._symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]
        self._timeframes = {
            1: "M1",
            5: "M5",
            15: "M15",
            30: "M30",
            60: "H1",
            240: "H4",
            1440: "D1",
            10080: "W1",
        }
        self._last_error = None

    def initialize(  # nosec B107
        self, path: str = "", login: int = 0, password: str = "", server: str = "Demo"
    ) -> bool:
        """Initialize mock MT5."""
        self._initialized = True
        self._connected = True
        self._last_error = None
        return True

    def shutdown(self) -> None:
        """Shutdown mock MT5."""
        self._initialized = False
        self._connected = False

    def initialized(self) -> bool:
        """Check if MT5 is initialized."""
        return self._initialized

    def terminal_info(self):
        """Get terminal info."""
        if not self._initialized:
            return None

        class TerminalInfo:
            connected = self._connected
            community_account = True
            community_connection = True

        return TerminalInfo()

    def symbols_get(self, symbol: str | None = None) -> list[Any] | None:
        """Get symbols."""
        if not self._initialized:
            return None

        class SymbolInfo:
            def __init__(self, name):
                self.name = name
                self.currency_base = "EUR"
                self.currency_profit = "USD"
                self.currency_margin = "USD"
                self.digits = 5
                self.trade_mode = 0

        if symbol:
            if symbol in self._symbols:
                return [SymbolInfo(symbol)]
            return None

        return [SymbolInfo(s) for s in self._symbols]

    def copy_rates_from_pos(
        self, symbol: str, timeframe: int, start_pos: int, count: int
    ) -> list[dict[str, Any]] | None:
        """Copy rates from position."""
        if not self._initialized:
            return None

        if symbol not in self._symbols:
            self._last_error = "Invalid symbol"
            return None

        # Generate mock data
        now = datetime.now()
        rates = []

        for i in range(count):
            time_offset = (start_pos + i) * timeframe
            timestamp = now - timedelta(minutes=time_offset)

            # Generate realistic price data
            base_price = 1.1000 + random.uniform(-0.1, 0.1)  # nosec B311

            rate = {
                "time": int(timestamp.timestamp()),
                "open": base_price,
                "high": base_price + random.uniform(0.0001, 0.0010),  # nosec B311
                "low": base_price - random.uniform(0.0001, 0.0010),  # nosec B311
                "close": base_price + random.uniform(-0.0005, 0.0005),  # nosec B311
                "tick_volume": random.randint(100, 1000),  # nosec B311
                "spread": random.randint(1, 10),  # nosec B311
                "real_volume": random.randint(1000, 10000),  # nosec B311
            }

            rates.append(rate)

        return rates

    def copy_ticks_from(
        self, symbol: str, from_date: datetime, count: int
    ) -> list[dict[str, Any]] | None:
        """Copy ticks from date."""
        if not self._initialized:
            return None

        if symbol not in self._symbols:
            self._last_error = "Invalid symbol"
            return None

        # Generate mock tick data
        ticks = []
        base_price = 1.1000

        for i in range(count):
            timestamp = from_date + timedelta(milliseconds=i * 100)

            tick = {
                "time": int(timestamp.timestamp()),
                "bid": base_price + random.uniform(-0.0005, 0.0005),  # nosec B311
                "ask": base_price + random.uniform(0.0001, 0.0010),  # nosec B311
                "last": base_price + random.uniform(-0.0002, 0.0002),  # nosec B311
                "volume": random.randint(1, 100),  # nosec B311
                "time_msc": int(timestamp.timestamp() * 1000),
                "flags": 0,
            }

            ticks.append(tick)

        return ticks

    def last_error(self):
        """Get last error."""
        return self._last_error
