"""Test Tick Pipeline szkript teszt modul.

Ez a modul tartalmazza a test_tick_pipeline.py szkript tesztjeit.
"""

from unittest.mock import MagicMock, patch

import pytest

from scripts.test_tick_pipeline import validate_tick_pipeline


class TestValidateTickPipeline:
    """Test Tick Pipeline szkript tesztek."""

    @pytest.mark.asyncio
    async def test_validate_tick_pipeline_success(self):
        """Teszt sikeres tick pipeline validáció."""
        # A függvényt mock-ok nélkül teszteljük, mivel mock komponenseket használ belül
        with patch("builtins.print"):  # Elfogjuk a print hívásokat
            result = await validate_tick_pipeline()

        assert result is True

    @pytest.mark.asyncio
    async def test_validate_tick_pipeline_resample_failure(self):
        """Teszt resample hiba esetén."""
        # Mock-oljuk a ResamplerServiceFactory.create-ot, hogy hibát dobjon
        with patch(
            "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory"
        ) as mock_factory:
            mock_resampler = MagicMock()
            mock_factory.create.return_value = mock_resampler
            mock_resampler.resample.side_effect = Exception("Resample hiba")

            with patch("builtins.print"):
                result = await validate_tick_pipeline()

        assert result is False

    @pytest.mark.asyncio
    async def test_validate_tick_pipeline_d1_failure(self):
        """Teszt D1 processor hiba esetén."""
        # Mock-oljuk a create_dimension_processor-t, hogy hibát dobjon
        with patch("neural_ai.core.processing.factory.create_dimension_processor") as mock_create:
            mock_processor = MagicMock()
            mock_create.return_value = mock_processor
            mock_processor.process.side_effect = Exception("D1 hiba")

            with patch("builtins.print"):
                result = await validate_tick_pipeline()

        assert result is False

    @pytest.mark.asyncio
    async def test_validate_tick_pipeline_validation_failure(self):
        """Teszt validációs hiba esetén."""
        # Mock-oljuk a ResamplerServiceFactory-t, hogy rossz eredményt adjon
        with patch(
            "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory"
        ) as mock_factory:
            mock_resampler = MagicMock()
            mock_factory.create.return_value = mock_resampler
            # Rossz DataFrame visszaadás (hiányzó oszlopokkal)
            import polars as pl

            bad_df = pl.DataFrame({"timestamp": [1, 2, 3]})  # Hiányzó szükséges oszlopok
            mock_resampler.resample.return_value = bad_df

            with patch("builtins.print"):
                result = await validate_tick_pipeline()

        assert result is False

    @pytest.mark.asyncio
    async def test_validate_tick_pipeline_validation_errors(self):
        """Teszt különböző validációs hibák esetén."""
        from datetime import datetime

        import pandas as pd
        import polars as pl

        # Mock adatok
        date_range = pd.date_range(
            start=datetime(2024, 1, 1, 12, 0, 0), end=datetime(2024, 1, 1, 12, 0, 10), freq="1s"
        )

        # Mock resample - rossz adatokkal
        bad_resample_df = pl.DataFrame(
            {
                "timestamp": date_range[:5],  # Rövidebb len
                "bid": [1.05] * 5,
                "ask": [1.051] * 5,
                "bid_volume": [50] * 5,
                "ask_volume": [50] * 5,
                "mid_close": [1.05] * 5,
                "spread": [0.001] * 5,
                "tick_volume": [2] * 5,  # Nem 1 minden sorban
            }
        )

        # Mock d1 result - rossz adatokkal
        bad_d1_df = pl.DataFrame(
            {
                "timestamp": date_range[:5],
                # Hiányzó log_return
                "upper_shadow": [0.01] * 5,  # Nem null
                "lower_shadow": [0.01] * 5,  # Nem null
            }
        )

        with (
            patch(
                "neural_ai.core.processing.resampler_service.factory.ResamplerServiceFactory"
            ) as mock_factory,
            patch("neural_ai.core.processing.factory.create_dimension_processor") as mock_create,
        ):
            mock_resampler = MagicMock()
            mock_factory.create.return_value = mock_resampler
            mock_resampler.resample.return_value = bad_resample_df

            mock_processor = MagicMock()
            mock_create.return_value = mock_processor
            mock_processor.process.return_value = bad_d1_df

            with patch("builtins.print"):
                result = await validate_tick_pipeline()

        assert result is False  # Validációs hibák miatt False
