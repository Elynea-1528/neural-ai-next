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
