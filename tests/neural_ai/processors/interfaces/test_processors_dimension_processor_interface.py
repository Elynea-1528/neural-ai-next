"""Unit tesztek a Dimension Processor Interface-hez."""

from typing import TYPE_CHECKING

import polars as pl
import pytest

from neural_ai.processors.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    pass


class ConcreteDimensionProcessor(IDimensionProcessor):
    """Teszt implementáció az IDimensionProcessor interfészhez."""

    def __init__(self, dim_id: int = 1) -> None:
        """Inicializálja a teszt processzort."""
        self._dim_id = dim_id

    def process(self, df: pl.DataFrame) -> pl.DataFrame:
        """Teszt implementáció - visszaadja az eredeti DataFrame-et."""
        return df

    @property
    def dimension_id(self) -> int:
        """Teszt implementáció - visszaadja a dimenzió azonosítót."""
        return self._dim_id


class TestIDimensionProcessor:
    """Tesztek az IDimensionProcessor interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            IDimensionProcessor()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        processor = ConcreteDimensionProcessor()

        # Assert
        assert isinstance(processor, IDimensionProcessor)

    def test_process_signature(self) -> None:
        """Ellenőrzi a process metódus szignatúráját."""
        # Arrange
        processor = ConcreteDimensionProcessor()
        df = pl.DataFrame({"price": [1.0, 2.0, 3.0]})

        # Act
        result = processor.process(df)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_dimension_id_property(self) -> None:
        """Ellenőrzi a dimension_id property működését."""
        # Arrange
        dim_id = 5
        processor = ConcreteDimensionProcessor(dim_id=dim_id)

        # Act
        result = processor.dimension_id

        # Assert
        assert isinstance(result, int)
        assert result == dim_id

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["process", "dimension_id"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(IDimensionProcessor, method_name)

    def test_process_with_empty_dataframe(self) -> None:
        """Ellenőrzi a process metódust üres DataFrame-mel."""
        # Arrange
        processor = ConcreteDimensionProcessor()
        df = pl.DataFrame()

        # Act
        result = processor.process(df)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_dimension_id_range(self) -> None:
        """Ellenőrzi, hogy a dimension_id 1-15 tartományban van."""
        # Arrange & Act
        for dim_id in range(1, 16):
            processor = ConcreteDimensionProcessor(dim_id=dim_id)

            # Assert
            assert 1 <= processor.dimension_id <= 15
