"""Unit tesztek a JForex Downloader Interface-hez."""

from datetime import datetime
from typing import TYPE_CHECKING

import pytest

from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader

if TYPE_CHECKING:
    from neural_ai.collectors.jforex.interfaces.tick_data import TickData


class ConcreteDownloader(IJForexDownloader):
    """Teszt implementáció az IJForexDownloader interfészhez."""

    async def download_tick_data(self, symbol: str, date: datetime) -> list["TickData"]:
        """Teszt implementáció."""
        return []

    async def get_available_dates(
        self, symbol: str, start_date: datetime, end_date: datetime
    ) -> list[datetime]:
        """Teszt implementáció."""
        return []

    def validate_bi5_data(self, data: bytes) -> bool:
        """Teszt implementáció."""
        return True

    async def close(self) -> None:
        """Teszt implementáció."""
        pass


class TestIJForexDownloader:
    """Tesztek az IJForexDownloader interfészhez."""

    def test_interface_is_abstract(self) -> None:
        """Ellenőrzi, hogy az interfész absztrakt osztály."""
        # Arrange & Act & Assert
        with pytest.raises(TypeError):
            IJForexDownloader()  # type: ignore[abstract]

    def test_concrete_implementation_can_be_instantiated(self) -> None:
        """Ellenőrzi, hogy konkrét implementáció példányosítható."""
        # Arrange & Act
        downloader = ConcreteDownloader()

        # Assert
        assert isinstance(downloader, IJForexDownloader)

    @pytest.mark.asyncio
    async def test_download_tick_data_signature(self) -> None:
        """Ellenőrzi a download_tick_data metódus szignatúráját."""
        # Arrange
        downloader = ConcreteDownloader()
        symbol = "EURUSD"
        date = datetime(2024, 3, 20)

        # Act
        result = await downloader.download_tick_data(symbol, date)

        # Assert
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_get_available_dates_signature(self) -> None:
        """Ellenőrzi a get_available_dates metódus szignatúráját."""
        # Arrange
        downloader = ConcreteDownloader()
        symbol = "EURUSD"
        start_date = datetime(2024, 3, 20)
        end_date = datetime(2024, 3, 21)

        # Act
        result = await downloader.get_available_dates(symbol, start_date, end_date)

        # Assert
        assert isinstance(result, list)

    def test_validate_bi5_data_signature(self) -> None:
        """Ellenőrzi a validate_bi5_data metódus szignatúráját."""
        # Arrange
        downloader = ConcreteDownloader()
        data = b"\x00\x01\x02"

        # Act
        result = downloader.validate_bi5_data(data)

        # Assert
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_close_signature(self) -> None:
        """Ellenőrzi a close metódus szignatúráját."""
        # Arrange
        downloader = ConcreteDownloader()

        # Act & Assert
        await downloader.close()  # Nem dob kivételt

    def test_interface_has_all_required_methods(self) -> None:
        """Ellenőrzi, hogy az interfész tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = [
            "download_tick_data",
            "get_available_dates",
            "validate_bi5_data",
            "close",
        ]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(IJForexDownloader, method_name)
            assert callable(getattr(IJForexDownloader, method_name))
