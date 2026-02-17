"""Tests for JForex collector __init__.py exports."""

from neural_ai.collectors.jforex import IJForexDownloader, JForexFactory


class TestJForexCollectorInit:
    """Test cases for JForex collector exports."""

    def test_jforexfactory_exported(self) -> None:
        """Test that JForexFactory is exported."""
        assert JForexFactory is not None
        assert hasattr(JForexFactory, "create_downloader")
        assert hasattr(JForexFactory, "create_live_feed")

    def test_ijforexdownloader_exported(self) -> None:
        """Test that IJForexDownloader is exported."""
        assert IJForexDownloader is not None
        assert hasattr(IJForexDownloader, "__abstractmethods__")
