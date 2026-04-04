"""Unit tesztek a BaseDimensionProcessor osztályhoz."""

from unittest.mock import MagicMock

import polars as pl
import pytest

from neural_ai.processors.dimensions.base import BaseDimensionProcessor


class ConcreteDimensionProcessor(BaseDimensionProcessor):
    """Teszt implementáció a BaseDimensionProcessor osztályhoz."""

    def __init__(self, config: MagicMock, logger: MagicMock, dim_id: int = 1) -> None:
        """Inicializálja a teszt processzort."""
        self._dim_id = dim_id
        super().__init__(config, logger)

    @property
    def dimension_id(self) -> int:
        """Teszt implementáció - visszaadja a dimenzió azonosítót."""
        return self._dim_id

    def process(self, df: pl.DataFrame) -> pl.DataFrame:
        """Teszt implementáció - visszaadja az eredeti DataFrame-et."""
        return df


class TestBaseDimensionProcessor:
    """Tesztek a BaseDimensionProcessor osztályhoz."""

    def test_base_dimension_processor_is_abstract(self) -> None:
        """Ellenőrzi, hogy a BaseDimensionProcessor absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            BaseDimensionProcessor(MagicMock(), MagicMock())  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {"enabled": True}
        mock_logger = MagicMock()

        # Act
        processor = ConcreteDimensionProcessor(mock_config, mock_logger)

        # Assert
        assert isinstance(processor, BaseDimensionProcessor)
        assert processor.config == mock_config
        assert processor.logger == mock_logger

    def test_initialization_loads_config(self) -> None:
        """Ellenőrzi, hogy az inicializálás betölti a konfigurációt."""
        # Arrange
        mock_config = MagicMock()
        expected_config = {"enabled": True, "param": "value"}
        mock_config.get.return_value = expected_config
        mock_logger = MagicMock()

        # Act
        processor = ConcreteDimensionProcessor(mock_config, mock_logger, dim_id=5)

        # Assert
        # A dim_config ProcessorConfig objektum, extra mezőkkel
        assert processor.dim_config.enabled is True
        assert processor.dim_config.param == "value"
        mock_config.get.assert_called_once_with("processors", "d05")

    def test_initialization_with_missing_config(self) -> None:
        """Ellenőrzi, hogy az inicializálás kezeli a hiányzó konfigurációt."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = None
        mock_logger = MagicMock()

        # Act
        processor = ConcreteDimensionProcessor(mock_config, mock_logger, dim_id=3)

        # Assert
        # A dim_config ProcessorConfig objektum, üres mezőkkel (None értékek)
        assert processor.dim_config.required_timeframes is None
        assert processor.dim_config.z_score_window is None
        mock_logger.warning.assert_called_once()
        warning_message = mock_logger.warning.call_args[0][0]
        assert "processors.d03" in warning_message

    def test_dimension_id_property(self) -> None:
        """Ellenőrzi a dimension_id property működését."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        dim_id = 7

        # Act
        processor = ConcreteDimensionProcessor(mock_config, mock_logger, dim_id=dim_id)

        # Assert
        assert processor.dimension_id == dim_id

    def test_process_method_exists(self) -> None:
        """Ellenőrzi, hogy a process metódus létezik."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()
        processor = ConcreteDimensionProcessor(mock_config, mock_logger)
        df = pl.DataFrame({"price": [1.0, 2.0, 3.0]})

        # Act
        result = processor.process(df)

        # Assert
        assert isinstance(result, pl.DataFrame)

    def test_config_section_format(self) -> None:
        """Ellenőrzi, hogy a konfiguráció szekció formátuma helyes."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()

        # Act
        ConcreteDimensionProcessor(mock_config, mock_logger, dim_id=1)

        # Assert
        mock_config.get.assert_called_once_with("processors", "d01")

    def test_config_section_format_double_digit(self) -> None:
        """Ellenőrzi, hogy a konfiguráció szekció formátuma helyes kétjegyű dimenzióknál."""
        # Arrange
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        mock_logger = MagicMock()

        # Act
        ConcreteDimensionProcessor(mock_config, mock_logger, dim_id=15)

        # Assert
        mock_config.get.assert_called_once_with("processors", "d15")
