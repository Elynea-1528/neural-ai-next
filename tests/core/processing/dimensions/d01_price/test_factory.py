"""D01PriceFactory unit tesztek."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from neural_ai.core.processing.dimensions.d01_price.factory import D01PriceFactory
from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.core.processing.interfaces.dimension_processor_interface import IDimensionProcessor


class TestD01PriceFactory:
    """D01PriceFactory unit teszt osztály."""

    def test_create_returns_correct_type(self):
        """Teszteli, hogy a create metódus helyes típust ad vissza."""
        mock_config = MagicMock()
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_logger = MagicMock()

        processor = D01PriceFactory.create(mock_config, mock_logger)

        assert isinstance(processor, D01PriceProcessor)
        assert isinstance(processor, IDimensionProcessor)

    def test_create_returns_new_instance(self):
        """Teszteli, hogy minden create hívás új példányt ad."""
        mock_config = MagicMock()
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_logger = MagicMock()

        processor1 = D01PriceFactory.create(mock_config, mock_logger)
        processor2 = D01PriceFactory.create(mock_config, mock_logger)

        assert processor1 is not processor2
        assert isinstance(processor1, D01PriceProcessor)
        assert isinstance(processor2, D01PriceProcessor)

    def test_created_processor_has_correct_dimension_id(self):
        """Teszteli, hogy a létrehozott processor helyes dimension_id-val rendelkezik."""
        mock_config = MagicMock()
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_logger = MagicMock()

        processor = D01PriceFactory.create(mock_config, mock_logger)

        assert processor.dimension_id == 1

    def test_created_processor_is_functional(self):
        """Teszteli, hogy a létrehozott processor működőképes."""
        import polars as pl

        mock_config = MagicMock()
        mock_config.get_section.return_value = {"z_score_window": 60, "calc_shadows": True}
        mock_logger = MagicMock()

        processor = D01PriceFactory.create(mock_config, mock_logger)

        # Egyszerű teszt DataFrame (nagyobb dataset a Z-score-hoz)
        timestamps = [
            datetime(2023, 1, 1, 9, 0) + timedelta(minutes=i) for i in range(80)
        ]  # 80 sor a rolling window-hez
        test_df = pl.DataFrame(
            {
                "timestamp": timestamps,
                "mid_open": [1.0500 + i * 0.0001 for i in range(80)],
                "mid_high": [1.0520 + i * 0.0001 for i in range(80)],
                "mid_low": [1.0480 + i * 0.0001 for i in range(80)],
                "mid_close": [1.0510 + i * 0.0001 for i in range(80)],
                "tick_volume": [1000 + i * 10 for i in range(80)],
                "spread": [0.0002 + i * 0.00001 for i in range(80)],
                "real_volume": [1500.0 + i * 5 for i in range(80)],
            }
        )

        result = processor.process(test_df)

        assert isinstance(result, pl.DataFrame)
        assert len(result) == 80
        expected_columns = {
            "timestamp",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "log_return",
            "rolling_z_score",
            "upper_shadow",
            "lower_shadow",
        }
        assert set(result.columns) == expected_columns
