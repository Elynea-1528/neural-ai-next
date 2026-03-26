"""Tests for JForex interfaces __init__.py exports."""

from neural_ai.collectors.jforex.interfaces import IJForexDownloader, ILiveFeed, TickData


class TestJForexInterfacesInit:
    """Test cases for JForex interfaces exports."""

    def test_ijforexdownloader_exported(self) -> None:
        """Test that IJForexDownloader is exported."""
        assert IJForexDownloader is not None
        assert hasattr(IJForexDownloader, "__abstractmethods__")

    def test_ilivefeed_exported(self) -> None:
        """Test that ILiveFeed is exported."""
        assert ILiveFeed is not None
        assert hasattr(ILiveFeed, "__abstractmethods__")

    def test_tickdata_exported(self) -> None:
        """Test that TickData is exported."""
        assert TickData is not None
        # TickData is a Pydantic model, not an ABC
        assert hasattr(TickData, "__dataclass_fields__")
