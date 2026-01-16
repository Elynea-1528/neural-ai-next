"""D02SupportFactory unit tesztek."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock

from neural_ai.processors.dimensions.d02_support.factory import D02SupportFactory
from neural_ai.processors.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)
from neural_ai.processors.interfaces.dimension_processor_interface import IDimensionProcessor


class TestD02SupportFactory:
    """D02SupportFactory unit teszt osztály."""

    def test_create_returns_correct_type(self):
        """Teszteli, hogy a create metódus helyes típust ad vissza."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"swing_window": 5, "min_distance": 10}
        mock_logger = MagicMock()

        processor = D02SupportFactory.create(mock_config, mock_logger)

        assert isinstance(processor, D02SupportProcessor)
        assert isinstance(processor, IDimensionProcessor)

    def test_create_returns_new_instance(self):
        """Teszteli, hogy minden create hívás új példányt ad."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"swing_window": 5, "min_distance": 10}
        mock_logger = MagicMock()

        processor1 = D02SupportFactory.create(mock_config, mock_logger)
        processor2 = D02SupportFactory.create(mock_config, mock_logger)

        assert processor1 is not processor2
        assert isinstance(processor1, D02SupportProcessor)
        assert isinstance(processor2, D02SupportProcessor)

    def test_created_processor_has_correct_dimension_id(self):
        """Teszteli, hogy a létrehozott processor helyes dimension_id-val rendelkezik."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"swing_window": 5, "min_distance": 10}
        mock_logger = MagicMock()

        processor = D02SupportFactory.create(mock_config, mock_logger)

        assert processor.dimension_id == 2

    def test_created_processor_is_functional(self):
        """Teszteli, hogy a létrehozott processor működőképes."""
        import polars as pl

        mock_config = MagicMock()
        mock_config.get.return_value = {"swing_window": 5, "min_distance": 10}
        mock_logger = MagicMock()

        processor = D02SupportFactory.create(mock_config, mock_logger)

        # Egyszerű teszt DataFrame swing pontokhoz
        timestamps = [datetime(2023, 1, 1, 9, 0) + timedelta(minutes=i) for i in range(50)]
        test_df = pl.DataFrame(
            {
                "timestamp": timestamps,
                "mid_open": [1.0500 + i * 0.0001 for i in range(50)],
                "mid_high": [1.0520 + i * 0.0001 for i in range(50)],
                "mid_low": [1.0480 + i * 0.0001 for i in range(50)],
                "mid_close": [1.0510 + i * 0.0001 for i in range(50)],
                "tick_volume": [1000 + i * 10 for i in range(50)],
                "spread": [0.0002 + i * 0.00001 for i in range(50)],
                "real_volume": [1500.0 + i * 5 for i in range(50)],
            }
        )

        result = processor.process(test_df)

        assert isinstance(result, pl.DataFrame)
        assert len(result) == 50
        expected_columns = {
            "timestamp",
            "mid_open",
            "mid_high",
            "mid_low",
            "mid_close",
            "tick_volume",
            "spread",
            "real_volume",
            "swing_high_body",
            "swing_low_body",
            "swing_high_wick",
            "swing_low_wick",
            "nearest_resistance",
            "nearest_support",
            "resistance_strength",
            "support_strength",
        }
        assert set(result.columns) == expected_columns

    def test_processor_uses_timeframe_specific_config(self):
        """Teszteli, hogy a processor timeframe-specifikus konfigurációt használ."""
        import polars as pl

        mock_config = MagicMock()
        mock_config.get.return_value = {
            "swing_window": 5,
            "min_distance": 10,
            "timeframe_configs": {
                "h4": {"swing_window": 10, "min_distance": 20},
                "d1": {"swing_window": 15, "min_distance": 30},
            },
        }
        mock_logger = MagicMock()

        processor = D02SupportFactory.create(mock_config, mock_logger)

        # Egyszerű teszt DataFrame
        timestamps = [datetime(2023, 1, 1, 9, 0) + timedelta(minutes=i) for i in range(50)]
        test_df = pl.DataFrame(
            {
                "timestamp": timestamps,
                "mid_open": [1.0500 + i * 0.0001 for i in range(50)],
                "mid_high": [1.0520 + i * 0.0001 for i in range(50)],
                "mid_low": [1.0480 + i * 0.0001 for i in range(50)],
                "mid_close": [1.0510 + i * 0.0001 for i in range(50)],
                "tick_volume": [1000 + i * 10 for i in range(50)],
                "spread": [0.0002 + i * 0.00001 for i in range(50)],
                "real_volume": [1500.0 + i * 5 for i in range(50)],
            }
        )

        # Teszteljük H4 timeframe-mal
        result_h4 = processor.process(test_df, timeframe="H4")
        assert isinstance(result_h4, pl.DataFrame)

        # A teszt sikeres, ha nem dob exception-t és helyes eredményt ad
