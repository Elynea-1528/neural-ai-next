"""Test Tick Pipeline szkript teszt modul.

Ez a modul tartalmazza a test_tick_pipeline.py szkript tesztjeit.
"""

from unittest.mock import MagicMock, patch

from scripts.test_tick_pipeline import validate_tick_pipeline


class TestValidateTickPipeline:
    """Test Tick Pipeline szkript tesztek."""

    def test_validate_tick_pipeline_success(self):
        """Teszt sikeres tick pipeline validáció."""
        # Mock-oljuk a factory-kat, hogy ne legyen külső függőség
        with (
            patch(
                "neural_ai.processors.resampler_service.factory.ResamplerServiceFactory"
            ) as mock_factory,
            patch("neural_ai.processors.factory.create_dimension_processor") as mock_create,
        ):
            mock_resampler = MagicMock()
            mock_factory.get_instance.return_value = mock_resampler
            # Mock resample - sikeres eredmény
            from datetime import datetime

            import polars as pl

            mock_resample_df = pl.DataFrame(
                {
                    "timestamp": [datetime(2024, 1, 1, 12, 0, 0)],
                    "bid": [1.05],
                    "ask": [1.051],
                    "bid_volume": [50],
                    "ask_volume": [50],
                    "mid_close": [1.0505],
                    "spread": [0.001],
                    "tick_volume": [1],
                }
            )

            async def mock_resample(*args, **kwargs):
                return mock_resample_df

            mock_resampler.resample.side_effect = mock_resample

            mock_processor = MagicMock()
            mock_create.return_value = mock_processor
            mock_d1_df = pl.DataFrame(
                {
                    "timestamp": [datetime(2024, 1, 1, 12, 0, 0)],
                    "bid": [1.05],
                    "ask": [1.051],
                    "bid_volume": [50],
                    "ask_volume": [50],
                    "log_return": [0.0],
                }
            )

            async def mock_process(*args, **kwargs):
                return mock_d1_df

            mock_processor.process.side_effect = mock_process

            with patch("builtins.print"):
                result = validate_tick_pipeline()

            assert result is True

    def test_validate_tick_pipeline_resample_failure(self):
        """Teszt resample hiba esetén."""
        # Mock-oljuk a DataFrame.with_columns metódust, hogy hibát dobjon
        with patch("polars.DataFrame.with_columns") as mock_with_columns:
            mock_with_columns.side_effect = Exception("Resample hiba")

            with patch("builtins.print"):
                result = validate_tick_pipeline()

            assert result is False

    def test_validate_tick_pipeline_d1_failure(self):
        """Teszt D1 processor hiba esetén."""
        # Mock-oljuk a _validate_d1_processor függvényt, hogy None-t adjon vissza
        with patch("scripts.test_tick_pipeline._validate_d1_processor") as mock_validate:
            mock_validate.return_value = None

            with patch("builtins.print"):
                result = validate_tick_pipeline()

        assert result is False

    def test_validate_tick_pipeline_validation_failure(self):
        """Teszt validációs hiba esetén."""
        # Mock-oljuk a _validate_resample függvényt, hogy None-t adjon vissza
        with patch("scripts.test_tick_pipeline._validate_resample") as mock_validate:
            mock_validate.return_value = None

            with patch("builtins.print"):
                result = validate_tick_pipeline()

        assert result is False

    def test_validate_tick_pipeline_validation_errors(self):
        """Teszt különböző validációs hibák esetén."""
        # Mock-oljuk a _generate_test_tick_data függvényt, hogy hibát dobjon
        with patch("scripts.test_tick_pipeline._generate_test_tick_data") as mock_generate:
            mock_generate.side_effect = Exception("Data generation hiba")

            with patch("builtins.print"):
                result = validate_tick_pipeline()

        assert result is False
