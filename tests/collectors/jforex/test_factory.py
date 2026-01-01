"""JForex Factory tests."""

from unittest.mock import MagicMock, patch

from neural_ai.collectors.jforex.factory import JForexFactory
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed


class TestJForexFactory:
    """Test cases for JForexFactory."""

    def test_create_downloader_returns_downloader_interface(self) -> None:
        """Test that create_downloader returns an IJForexDownloader instance."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        mock_config.get.return_value = {"timeout": 30}

        # Act
        with patch("aiohttp.ClientSession"):
            downloader = JForexFactory.create_downloader(
                config=mock_config,
                logger=mock_logger,
                event_bus=mock_event_bus,
                storage=mock_storage,
            )

        # Assert
        assert isinstance(downloader, IJForexDownloader)
        mock_logger.info.assert_called_once()

    def test_create_downloader_passes_storage_to_bi5downloader(self) -> None:
        """Test that create_downloader passes storage to Bi5Downloader constructor."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        mock_config.get.return_value = {"timeout": 30}

        # Act
        with patch(
            "neural_ai.collectors.jforex.implementations.bi5_downloader.Bi5Downloader"
        ) as mock_bi5_class:
            with patch("aiohttp.ClientSession"):
                JForexFactory.create_downloader(
                    config=mock_config,
                    logger=mock_logger,
                    event_bus=mock_event_bus,
                    storage=mock_storage,
                )

        # Assert
        call_args = mock_bi5_class.call_args
        assert call_args is not None
        assert call_args.kwargs["storage"] is mock_storage

    def test_create_downloader_handles_config_exception(self) -> None:
        """Test that create_downloader handles config exceptions gracefully."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        # First call (factory): jforex config, second call (Bi5Downloader.__init__): jforex.base_url
        mock_config.get.side_effect = [
            {},  # jforex config returns empty dict
            "https://www.dukascopy.com/datafeed",  # jforex.base_url for Bi5Downloader
        ]

        # Act
        with patch("aiohttp.ClientSession"):
            downloader = JForexFactory.create_downloader(
                config=mock_config,
                logger=mock_logger,
                event_bus=mock_event_bus,
                storage=mock_storage,
            )

        # Assert
        assert isinstance(downloader, IJForexDownloader)
        assert mock_config.get.call_count == 2

    def test_create_live_feed_returns_live_interface(self) -> None:
        """Test that create_live_feed returns an ILiveFeed instance."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        mock_config.get.return_value = {"enabled": True}

        # Act
        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Assert
        assert isinstance(live_feed, ILiveFeed)
        mock_logger.info.assert_called_once()

    def test_create_live_feed_logs_warning_when_disabled(self) -> None:
        """Test that create_live_feed logs warning when disabled in config."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        mock_config.get.return_value = {"enabled": False}

        # Act
        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Assert
        assert isinstance(live_feed, ILiveFeed)
        mock_logger.warning.assert_called_once()

    def test_create_live_feed_handles_config_exception(self) -> None:
        """Test that create_live_feed handles config exceptions gracefully."""
        # Arrange
        mock_config = MagicMock()
        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        mock_config.get.side_effect = KeyError("jforex_live config not found")

        # Act
        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Assert
        assert isinstance(live_feed, ILiveFeed)
        mock_logger.warning.assert_called_once()
