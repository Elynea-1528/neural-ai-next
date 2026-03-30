"""Unit tesztek a JForex TickData modellhez."""

from datetime import UTC, datetime

from neural_ai.collectors.jforex.interfaces.tick_data import TickData


class TestTickData:
    """Tesztek a TickData dataclass-hoz."""

    def test_tick_data_creation_with_required_fields(self) -> None:
        """Ellenőrzi, hogy TickData létrehozható kötelező mezőkkel."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        symbol = "EURUSD"
        bid = 1.08500
        ask = 1.08520

        # Act
        tick = TickData(timestamp=timestamp, symbol=symbol, bid=bid, ask=ask)

        # Assert
        assert tick.timestamp == timestamp
        assert tick.symbol == symbol
        assert tick.bid == bid
        assert tick.ask == ask
        assert tick.ask_volume is None
        assert tick.bid_volume is None
        assert tick.source == "jforex"

    def test_tick_data_creation_with_all_fields(self) -> None:
        """Ellenőrzi, hogy TickData létrehozható minden mezővel."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        symbol = "EURUSD"
        bid = 1.08500
        ask = 1.08520
        ask_volume = 1000000.0
        bid_volume = 1500000.0
        source = "custom_source"

        # Act
        tick = TickData(
            timestamp=timestamp,
            symbol=symbol,
            bid=bid,
            ask=ask,
            ask_volume=ask_volume,
            bid_volume=bid_volume,
            source=source,
        )

        # Assert
        assert tick.timestamp == timestamp
        assert tick.symbol == symbol
        assert tick.bid == bid
        assert tick.ask == ask
        assert tick.ask_volume == ask_volume
        assert tick.bid_volume == bid_volume
        assert tick.source == source

    def test_spread_calculation(self) -> None:
        """Ellenőrzi a spread számítást pip-ben."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)

        # Act
        spread = tick.spread

        # Assert
        assert spread == 2.0  # 20 pips = 0.0020 * 10000

    def test_spread_calculation_with_larger_spread(self) -> None:
        """Ellenőrzi a spread számítást nagyobb spread esetén."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08550)

        # Act
        spread = tick.spread

        # Assert
        assert spread == 5.0  # 50 pips

    def test_mid_price_calculation(self) -> None:
        """Ellenőrzi a mid ár számítást."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)

        # Act
        mid_price = tick.mid_price

        # Assert
        assert mid_price == 1.08510  # (1.08500 + 1.08520) / 2

    def test_mid_price_rounding(self) -> None:
        """Ellenőrzi a mid ár kerekítését 5 tizedesjegyre."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08501, ask=1.08522)

        # Act
        mid_price = tick.mid_price

        # Assert
        assert mid_price == 1.08512  # Kerekítve 5 tizedesjegyre

    def test_tick_data_is_dataclass(self) -> None:
        """Ellenőrzi, hogy TickData dataclass."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)

        # Act & Assert
        assert hasattr(tick, "__dataclass_fields__")

    def test_tick_data_equality(self) -> None:
        """Ellenőrzi, hogy két azonos TickData egyenlő."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick1 = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)
        tick2 = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)

        # Act & Assert
        assert tick1 == tick2

    def test_tick_data_inequality(self) -> None:
        """Ellenőrzi, hogy két különböző TickData nem egyenlő."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick1 = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08520)
        tick2 = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08501, ask=1.08520)

        # Act & Assert
        assert tick1 != tick2

    def test_spread_with_zero_spread(self) -> None:
        """Ellenőrzi a spread számítást nulla spread esetén."""
        # Arrange
        timestamp = datetime(2024, 3, 20, 10, 30, 0, tzinfo=UTC)
        tick = TickData(timestamp=timestamp, symbol="EURUSD", bid=1.08500, ask=1.08500)

        # Act
        spread = tick.spread

        # Assert
        assert spread == 0.0
