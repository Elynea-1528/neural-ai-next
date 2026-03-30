"""Unit tesztek a Time Alignment Interface-hez."""

from typing import TYPE_CHECKING

import polars as pl
import pytest

from neural_ai.processors.interfaces.time_alignment_interface import (
    ITimeAlignmentService,
)

if TYPE_CHECKING:
    pass


class ConcreteTimeAlignmentService(ITimeAlignmentService):
    """Teszt implementáció az ITimeAlignmentService interfészhez."""

    def reindex_to_grid(self, df: pl.DataFrame, timeframe: str) -> pl.DataFrame:
        """Teszt implementáció - visszaadja az eredeti DataFrame-et."""
        return df

    def handle_gaps(
        self, df: pl.DataFrame, timeframe: str, method: str = "forward_fill"
    ) -> pl.DataFrame:
        """Teszt implementáció - visszaadja az eredeti DataFrame-et."""
        return df


class TestITimeAlignmentService:
    """Tesztek az ITimeAlignmentService interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            ITimeAlignmentService()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        service = ConcreteTimeAlignmentService()

        # Assert
        assert isinstance(service, ITimeAlignmentService)

    def test_reindex_to_grid_signature(self) -> None:
        """Ellenőrzi a reindex_to_grid metódus szignatúráját."""
        # Arrange
        service = ConcreteTimeAlignmentService()
        df = pl.DataFrame({"timestamp": [1, 2, 3], "price": [1.0, 2.0, 3.0]})
        timeframe = "1h"

        # Act
        result = service.reindex_to_grid(df, timeframe)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_handle_gaps_signature(self) -> None:
        """Ellenőrzi a handle_gaps metódus szignatúráját."""
        # Arrange
        service = ConcreteTimeAlignmentService()
        df = pl.DataFrame({"timestamp": [1, 2, 3], "price": [1.0, 2.0, 3.0]})
        timeframe = "1h"

        # Act
        result = service.handle_gaps(df, timeframe)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_handle_gaps_with_custom_method(self) -> None:
        """Ellenőrzi a handle_gaps metódust egyedi metódussal."""
        # Arrange
        service = ConcreteTimeAlignmentService()
        df = pl.DataFrame({"timestamp": [1, 2, 3], "price": [1.0, 2.0, 3.0]})
        timeframe = "1h"
        method = "interpolate"

        # Act
        result = service.handle_gaps(df, timeframe, method=method)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["reindex_to_grid", "handle_gaps"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(ITimeAlignmentService, method_name)
            assert callable(getattr(ITimeAlignmentService, method_name))

    def test_reindex_to_grid_with_empty_dataframe(self) -> None:
        """Ellenőrzi a reindex_to_grid metódust üres DataFrame-mel."""
        # Arrange
        service = ConcreteTimeAlignmentService()
        df = pl.DataFrame()
        timeframe = "1h"

        # Act
        result = service.reindex_to_grid(df, timeframe)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_handle_gaps_with_default_method(self) -> None:
        """Ellenőrzi a handle_gaps metódust alapértelmezett metódussal."""
        # Arrange
        service = ConcreteTimeAlignmentService()
        df = pl.DataFrame({"timestamp": [1, 2, 3], "price": [1.0, 2.0, 3.0]})
        timeframe = "1h"

        # Act
        result = service.handle_gaps(df, timeframe)

        # Assert
        assert isinstance(result, pl.DataFrame)
