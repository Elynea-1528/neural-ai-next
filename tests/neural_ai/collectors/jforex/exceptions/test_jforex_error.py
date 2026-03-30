"""Unit tesztek a JForex Exception osztályokhoz."""

import pytest

from neural_ai.collectors.jforex.exceptions.jforex_error import (
    DataNotAvailableError,
    DecodeError,
    DownloadError,
    JForexError,
)


class TestJForexError:
    """Tesztek a JForexError alap kivételhez."""

    def test_jforex_error_is_exception(self) -> None:
        """Ellenőrzi, hogy JForexError az Exception leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(JForexError, Exception)

    def test_jforex_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy JForexError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(JForexError):
            raise JForexError("Teszt hiba")

    def test_jforex_error_with_message(self) -> None:
        """Ellenőrzi, hogy JForexError üzenettel dobható."""
        # Arrange
        message = "Teszt hiba üzenet"

        # Act & Assert
        with pytest.raises(JForexError) as exc_info:
            raise JForexError(message)

        assert str(exc_info.value) == message


class TestDownloadError:
    """Tesztek a DownloadError kivételhez."""

    def test_download_error_is_jforex_error(self) -> None:
        """Ellenőrzi, hogy DownloadError a JForexError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(DownloadError, JForexError)

    def test_download_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy DownloadError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(DownloadError):
            raise DownloadError("Letöltési hiba")

    def test_download_error_with_message(self) -> None:
        """Ellenőrzi, hogy DownloadError üzenettel dobható."""
        # Arrange
        message = "Hálózati hiba történt"

        # Act & Assert
        with pytest.raises(DownloadError) as exc_info:
            raise DownloadError(message)

        assert str(exc_info.value) == message

    def test_download_error_caught_as_jforex_error(self) -> None:
        """Ellenőrzi, hogy DownloadError elkapható JForexError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(JForexError):
            raise DownloadError("Letöltési hiba")


class TestDecodeError:
    """Tesztek a DecodeError kivételhez."""

    def test_decode_error_is_jforex_error(self) -> None:
        """Ellenőrzi, hogy DecodeError a JForexError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(DecodeError, JForexError)

    def test_decode_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy DecodeError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(DecodeError):
            raise DecodeError("Dekódolási hiba")

    def test_decode_error_with_message(self) -> None:
        """Ellenőrzi, hogy DecodeError üzenettel dobható."""
        # Arrange
        message = "LZMA dekompresszió sikertelen"

        # Act & Assert
        with pytest.raises(DecodeError) as exc_info:
            raise DecodeError(message)

        assert str(exc_info.value) == message

    def test_decode_error_caught_as_jforex_error(self) -> None:
        """Ellenőrzi, hogy DecodeError elkapható JForexError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(JForexError):
            raise DecodeError("Dekódolási hiba")


class TestDataNotAvailableError:
    """Tesztek a DataNotAvailableError kivételhez."""

    def test_data_not_available_error_is_jforex_error(self) -> None:
        """Ellenőrzi, hogy DataNotAvailableError a JForexError leszármazottja."""
        # Arrange & Act & Assert
        assert issubclass(DataNotAvailableError, JForexError)

    def test_data_not_available_error_can_be_raised(self) -> None:
        """Ellenőrzi, hogy DataNotAvailableError dobható."""
        # Arrange & Act & Assert
        with pytest.raises(DataNotAvailableError):
            raise DataNotAvailableError("Adat nem elérhető")

    def test_data_not_available_error_with_message(self) -> None:
        """Ellenőrzi, hogy DataNotAvailableError üzenettel dobható."""
        # Arrange
        message = "Hétvégén nincs adat"

        # Act & Assert
        with pytest.raises(DataNotAvailableError) as exc_info:
            raise DataNotAvailableError(message)

        assert str(exc_info.value) == message

    def test_data_not_available_error_caught_as_jforex_error(self) -> None:
        """Ellenőrzi, hogy DataNotAvailableError elkapható JForexError-ként."""
        # Arrange & Act & Assert
        with pytest.raises(JForexError):
            raise DataNotAvailableError("Adat nem elérhető")
