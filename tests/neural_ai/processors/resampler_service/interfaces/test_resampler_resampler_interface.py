"""Unit tesztek a Resampler Interface-hez."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pandas as pd
import polars as pl
import pytest

from neural_ai.processors.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)

if TYPE_CHECKING:
    pass


class ConcreteResampler(ResamplerInterface):
    """Teszt implementáció a ResamplerInterface interfészhez."""

    async def resample(
        self,
        symbol: str,
        start: datetime,
        end: datetime,
        timeframe: str = "1m",
        return_type: str = "polars",
    ) -> pl.DataFrame | pd.DataFrame:
        """Teszt implementáció - üres DataFrame-et ad vissza."""
        if return_type == "polars":
            return pl.DataFrame(
                {
                    "timestamp": [],
                    "open": [],
                    "high": [],
                    "low": [],
                    "close": [],
                    "volume": [],
                }
            )
        else:
            return pd.DataFrame(
                {
                    "timestamp": [],
                    "open": [],
                    "high": [],
                    "low": [],
                    "close": [],
                    "volume": [],
                }
            )


class TestResamplerInterface:
    """Tesztek a ResamplerInterface interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ResamplerInterface()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        resampler = ConcreteResampler()

        # Assert
        assert isinstance(resampler, ResamplerInterface)

    @pytest.mark.asyncio
    async def test_resample_signature_with_polars(self) -> None:
        """Ellenőrzi a resample metódus szignatúráját Polars visszatérési típussal."""
        # Arrange
        resampler = ConcreteResampler()
        symbol = "EURUSD"
        start = datetime(2024, 3, 20, 0, 0, 0, tzinfo=UTC)
        end = datetime(2024, 3, 20, 1, 0, 0, tzinfo=UTC)

        # Act
        result = await resampler.resample(symbol, start, end, return_type="polars")

        # Assert
        assert isinstance(result, pl.DataFrame)

    @pytest.mark.asyncio
    async def test_resample_signature_with_pandas(self) -> None:
        """Ellenőrzi a resample metódus szignatúráját Pandas visszatérési típussal."""
        # Arrange
        resampler = ConcreteResampler()
        symbol = "EURUSD"
        start = datetime(2024, 3, 20, 0, 0, 0, tzinfo=UTC)
        end = datetime(2024, 3, 20, 1, 0, 0, tzinfo=UTC)

        # Act
        result = await resampler.resample(symbol, start, end, return_type="pandas")

        # Assert
        assert isinstance(result, pd.DataFrame)

    @pytest.mark.asyncio
    async def test_resample_with_custom_timeframe(self) -> None:
        """Ellenőrzi a resample metódust egyedi időkerettel."""
        # Arrange
        resampler = ConcreteResampler()
        symbol = "EURUSD"
        start = datetime(2024, 3, 20, 0, 0, 0, tzinfo=UTC)
        end = datetime(2024, 3, 20, 1, 0, 0, tzinfo=UTC)
        timeframe = "5m"

        # Act
        result = await resampler.resample(symbol, start, end, timeframe=timeframe)

        # Assert
        assert isinstance(result, (pl.DataFrame, pd.DataFrame))

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["resample"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(ResamplerInterface, method_name)
            assert callable(getattr(ResamplerInterface, method_name))

    @pytest.mark.asyncio
    async def test_resample_default_parameters(self) -> None:
        """Ellenőrzi a resample metódust alapértelmezett paraméterekkel."""
        # Arrange
        resampler = ConcreteResampler()
        symbol = "EURUSD"
        start = datetime(2024, 3, 20, 0, 0, 0, tzinfo=UTC)
        end = datetime(2024, 3, 20, 1, 0, 0, tzinfo=UTC)

        # Act
        result = await resampler.resample(symbol, start, end)

        # Assert
        assert isinstance(result, pl.DataFrame)  # Alapértelmezett: polars
