"""Unit tesztek a Resampler Exception osztályokhoz."""

import pytest

from neural_ai.core.base.exceptions.base_error import NeuralAIException
from neural_ai.processors.resampler_service.exceptions.resampler_error import (
    DataLoadError,
    InvalidTimeframeError,
    ResamplerError,
    ResamplingError,
)


class TestResamplerError:
    """Tesztek a ResamplerError alap kivételhez."""

    def test_resampler_error_is_neural_ai_exception(self) -> None:
        """Ellenőrzi, hogy ResamplerError a NeuralAIException leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(ResamplerError, NeuralAIException)

    def test_resampler_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy ResamplerError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(ResamplerError):
            raise ResamplerError("Teszt hiba")

    def test_resampler_error_with_message(self) -> None:
        """Ellenőrzi, hogy ResamplerError üzenettel dobható."""
        # Arrange
        message = "Resampler hiba történt"

        # Act & Assert
        with pytest.raises(ResamplerError) as exc_info:
            raise ResamplerError(message)

        assert str(exc_info.value) == message

    def test_resampler_error_with_details(self) -> None:
        """Ellenőrzi, hogy ResamplerError részletekkel dobható."""
        # Arrange
        message = "Resampler hiba"
        details = "Részletes hibainformáció"

        # Act
        error = ResamplerError(message, details=details)

        # Assert
        assert error.details == details
        assert error.component == "ResamplerService"

    def test_resampler_error_with_original_error(self) -> None:
        """Ellenőrzi, hogy ResamplerError eredeti hibával dobható."""
        # Arrange
        message = "Resampler hiba"
        original = ValueError("Eredeti hiba")

        # Act
        error = ResamplerError(message, original_error=original)

        # Assert
        assert error.original_error == original


class TestDataLoadError:
    """Tesztek a DataLoadError kivételhez."""

    def test_data_load_error_is_resampler_error(self) -> None:
        """Ellenőrzi, hogy DataLoadError a ResamplerError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(DataLoadError, ResamplerError)

    def test_data_load_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy DataLoadError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(DataLoadError):
            raise DataLoadError("EURUSD", "2024-03-20", "2024-03-21")

    def test_data_load_error_with_parameters(self) -> None:
        """Ellenőrzi, hogy DataLoadError paraméterekkel dobható."""
        # Arrange
        symbol = "EURUSD"
        start = "2024-03-20"
        end = "2024-03-21"

        # Act
        error = DataLoadError(symbol, start, end)

        # Assert
        assert symbol in str(error)
        assert error.details is not None
        assert start in error.details
        assert end in error.details

    def test_data_load_error_with_original_error(self) -> None:
        """Ellenőrzi, hogy DataLoadError eredeti hibával dobható."""
        # Arrange
        original = OSError("Fájl nem található")

        # Act
        error = DataLoadError("EURUSD", "2024-03-20", "2024-03-21", original_error=original)

        # Assert
        assert error.original_error == original


class TestResamplingError:
    """Tesztek a ResamplingError kivételhez."""

    def test_resampling_error_is_resampler_error(self) -> None:
        """Ellenőrzi, hogy ResamplingError a ResamplerError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(ResamplingError, ResamplerError)

    def test_resampling_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy ResamplingError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(ResamplingError):
            raise ResamplingError("EURUSD", "1m")

    def test_resampling_error_with_parameters(self) -> None:
        """Ellenőrzi, hogy ResamplingError paraméterekkel dobható."""
        # Arrange
        symbol = "EURUSD"
        timeframe = "1m"

        # Act
        error = ResamplingError(symbol, timeframe)

        # Assert
        assert symbol in str(error)
        assert error.details is not None
        assert timeframe in error.details

    def test_resampling_error_with_original_error(self) -> None:
        """Ellenőrzi, hogy ResamplingError eredeti hibával dobható."""
        # Arrange
        original = ValueError("Érvénytelen adat")

        # Act
        error = ResamplingError("EURUSD", "1m", original_error=original)

        # Assert
        assert error.original_error == original


class TestInvalidTimeframeError:
    """Tesztek az InvalidTimeframeError kivételhez."""

    def test_invalid_timeframe_error_is_resampler_error(self) -> None:
        """Ellenőrzi, hogy InvalidTimeframeError a ResamplerError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(InvalidTimeframeError, ResamplerError)

    def test_invalid_timeframe_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy InvalidTimeframeError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(InvalidTimeframeError):
            raise InvalidTimeframeError("invalid")

    def test_invalid_timeframe_error_with_timeframe(self) -> None:
        """Ellenőrzi, hogy InvalidTimeframeError időkerettel dobható."""
        # Arrange
        timeframe = "invalid_timeframe"

        # Act
        error = InvalidTimeframeError(timeframe)

        # Assert
        assert timeframe in str(error)
        assert error.details is not None
        assert "Pandas offset" in error.details

    def test_invalid_timeframe_error_caught_as_resampler_error(self) -> None:
        """Ellenőrzi, hogy InvalidTimeframeError elkapható ResamplerError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(ResamplerError):
            raise InvalidTimeframeError("invalid")
