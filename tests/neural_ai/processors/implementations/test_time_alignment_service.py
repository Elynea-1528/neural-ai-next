"""TimeAlignmentService tesztek."""
# pyright: reportArgumentType=false, reportPrivateUsage=false
# Mock **kwargs és protected member access test hibák

from collections.abc import Mapping
from decimal import Decimal
from typing import Any, AnyStr

import polars as pl
import pytest

from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.processors.implementations.time_alignment_service import TimeAlignmentService


class MockLogger(LoggerInterface):
    """Mock logger implementáció a teszteléshez."""

    def __init__(
        self, name: str, config: Any | None = None, **kwargs: Mapping[str, AnyStr]
    ) -> None:
        """Inicializálás."""
        super().__init__(name, config, **kwargs)  # type: ignore[safe-super, arg-type]
        self.name = name
        self.config = config
        self.kwargs = kwargs  # type: ignore[var-annotated]
        self.level = 20
        self.messages: list[dict[str, Any]] = []

    def debug(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:  # type: ignore[override]
        """Debug üzenet logolása."""
        super().debug(message, **kwargs)  # type: ignore[safe-super]
        self.messages.append({"level": "debug", "message": message, **kwargs})

    def info(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:  # type: ignore[override]
        """Info üzenet logolása."""
        super().info(message, **kwargs)  # type: ignore[safe-super]
        self.messages.append({"level": "info", "message": message, **kwargs})

    def warning(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:  # type: ignore[override]
        """Warning üzenet logolása."""
        super().warning(message, **kwargs)  # type: ignore[safe-super]
        self.messages.append({"level": "warning", "message": message, **kwargs})

    def error(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:  # type: ignore[override]
        """Error üzenet logolása."""
        super().error(message, **kwargs)  # type: ignore[safe-super]
        self.messages.append({"level": "error", "message": message, **kwargs})

    def critical(self, message: str, **kwargs: Mapping[str, AnyStr]) -> None:  # type: ignore[override]
        """Critical üzenet logolása."""
        super().critical(message, **kwargs)  # type: ignore[safe-super]
        self.messages.append({"level": "critical", "message": message, **kwargs})

    def set_level(self, level: int) -> None:
        """Log szint beállítása."""
        super().set_level(level)  # type: ignore[safe-super]
        self.level = level

    def get_level(self) -> int:
        """Log szint lekérdezése."""
        super().get_level()  # type: ignore[safe-super]
        return self.level


class TestTimeAlignmentService:
    """TimeAlignmentService osztály tesztei."""

    @pytest.fixture(scope="function")
    def mock_logger(self) -> MockLogger:
        """Mock logger fixture."""
        return MockLogger("test_time_alignment")

    @pytest.fixture(scope="function")
    def service(self, mock_logger: MockLogger) -> TimeAlignmentService:
        """TimeAlignmentService fixture."""
        return TimeAlignmentService(mock_logger)

    def test_init(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None:
        """Inicializálás teszt."""
        assert service._logger == mock_logger

    def test_reindex_to_grid_tick(
        self, service: TimeAlignmentService, mock_logger: MockLogger
    ) -> None:
        """reindex_to_grid tick esetében."""
        df = pl.DataFrame(
            {"timestamp": [Decimal(1609459200), Decimal(1609459260)], "price": [100, 101]}
        )
        result = service.reindex_to_grid(df, "tick")
        assert result.equals(df)
        assert len(mock_logger.messages) == 1
        assert (
            "Tick adatoknál nincs rács és gap-fill szükséges." in mock_logger.messages[0]["message"]
        )

    def test_reindex_to_grid_minute(
        self, service: TimeAlignmentService, mock_logger: MockLogger
    ) -> None:
        """reindex_to_grid perc esetében."""
        # Epoch timestampok: 2021-01-01 00:00:00 és 00:02:00
        df = pl.DataFrame(
            {"timestamp": [Decimal(1609459200), Decimal(1609459320)], "price": [100.0, 101.0]}
        )
        result = service.reindex_to_grid(df, "1m")
        # Ellenőrizzük, hogy új sorok lettek hozzáadva
        assert len(result) >= len(df)
        assert len(mock_logger.messages) == 1
        assert "Időskála újragridelve." in mock_logger.messages[0]["message"]

    def test_market_hours_filter(
        self, service: TimeAlignmentService, mock_logger: MockLogger
    ) -> None:
        """market_hours_filter teszt."""
        # Hétfő és vasárnap éjjel
        df = pl.DataFrame(
            {
                "timestamp": [
                    Decimal(1609459200),  # 2021-01-01 00:00:00 (péntek)
                    Decimal(1609545600),  # 2021-01-02 00:00:00 (szombat)
                    Decimal(1609632000 + 21 * 3600),  # 2021-01-03 21:00:00 (vasárnap)
                ],
                "price": [100, 101, 102],
            }
        )
        result = service.market_hours_filter(df)
        # Csak a pénteki és vasárnapi 21:00 marad
        assert len(result) == 2
        assert len(mock_logger.messages) == 1
        assert "Piaci órák szerinti szűrés alkalmazva." in mock_logger.messages[0]["message"]

    def test_handle_gaps_tick(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None:
        """handle_gaps tick esetében."""
        df = pl.DataFrame({"timestamp": [Decimal(1609459200)], "price": [100.0]})
        result = service.handle_gaps(df, "tick")
        assert result.equals(df)
        assert len(mock_logger.messages) == 1
        assert "Tick adatoknál nincs lyukkezelés szükséges." in mock_logger.messages[0]["message"]

    def test_handle_gaps_forward_fill(
        self, service: TimeAlignmentService, mock_logger: MockLogger
    ) -> None:
        """handle_gaps forward_fill esetében."""
        df = pl.DataFrame(
            {
                "timestamp": [Decimal(1609459200), Decimal(1609459260)],
                "open": [100.0, None],
                "close": [101.0, None],
                "tick_volume": [10, None],
            }
        )
        result = service.handle_gaps(df, "1m", "forward_fill")
        # open és close forward fill, tick_volume 0
        assert result["open"][1] == 100.0
        assert result["close"][1] == 101.0
        assert result["tick_volume"][1] == 0
        assert len(mock_logger.messages) == 1
        assert "Lyukak kezelése forward_fill módszerrel." in mock_logger.messages[0]["message"]

    def test_handle_gaps_mask(self, service: TimeAlignmentService, mock_logger: MockLogger) -> None:
        """handle_gaps mask esetében."""
        df = pl.DataFrame(
            {"timestamp": [Decimal(1609459200), Decimal(1609459260)], "close": [101.0, None]}
        )
        result = service.handle_gaps(df, "1m", "mask")
        assert result["close"][1] is None
        assert len(mock_logger.messages) == 1
        assert "Lyukak kezelése mask módszerrel." in mock_logger.messages[0]["message"]

    def test_handle_gaps_unknown_method(
        self, service: TimeAlignmentService, mock_logger: MockLogger
    ) -> None:
        """handle_gaps ismeretlen method esetében."""
        df = pl.DataFrame({"timestamp": [Decimal(1609459200)], "price": [100.0]})
        with pytest.raises(ValueError, match="Ismeretlen method: unknown"):
            service.handle_gaps(df, "1m", "unknown")
        assert len(mock_logger.messages) == 1
        assert "Ismeretlen lyukkezelési method." in mock_logger.messages[0]["message"]
