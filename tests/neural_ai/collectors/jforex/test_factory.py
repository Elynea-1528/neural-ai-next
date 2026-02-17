"""JForexFactory tesztek."""

from unittest.mock import ANY, MagicMock, patch

from neural_ai.collectors.jforex.factory import JForexFactory


class TestJForexFactory:
    """JForexFactory tesztek."""

    @patch("neural_ai.collectors.jforex.implementations.bi5_downloader.Bi5Downloader")
    @patch("aiohttp.ClientSession")
    def test_create_downloader_valid_config(
        self, mock_session: MagicMock, mock_downloader: MagicMock
    ) -> None:
        """Teszteli a downloader létrehozását érvényes konfiggal."""
        mock_config = MagicMock()
        # JForexConfig structure: {"jforex": {"download": {"timeout": 30}, ...}}
        mock_config.get.return_value = {
            "download": {"timeout": 30, "max_retries": 3},
            "base_url": "https://datafeed.dukascopy.com",
        }

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        downloader = JForexFactory.create_downloader(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus, storage=mock_storage
        )

        assert downloader is not None
        mock_downloader.assert_called_once()

    @patch("neural_ai.collectors.jforex.implementations.bi5_downloader.Bi5Downloader")
    @patch("aiohttp.ClientSession")
    def test_create_downloader_invalid_config(
        self, mock_session: MagicMock, mock_downloader: MagicMock
    ) -> None:
        """Teszteli a downloader létrehozását érvénytelen konfiggal (defaults)."""
        mock_config = MagicMock()
        # Invalid config: timeout < 1
        mock_config.get.return_value = {"download": {"timeout": -5}}

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        # A factory elkapja a ValidationError-t és logolja, majd default configgal létrehozza
        downloader = JForexFactory.create_downloader(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus, storage=mock_storage
        )

        assert downloader is not None
        mock_logger.error.assert_called_with("jforex_config_validation_error", error=ANY)

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_valid_config(self, mock_live_feed: MagicMock) -> None:
        """Teszteli a live feed létrehozását érvényes konfiggal."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"enabled": True, "host": "localhost", "tick_port": 1234}

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        assert live_feed is not None
        mock_live_feed.assert_called_once()

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_invalid_port(self, mock_live_feed: MagicMock) -> None:
        """Teszteli a live feed létrehozását érvénytelen porttal."""
        mock_config = MagicMock()
        mock_config.get.return_value = {
            "enabled": True,
            "tick_port": 99999,  # Invalid port > 65535
        }

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Fallback to default
        assert live_feed is not None
        mock_logger.error.assert_called_with("jforex_live_config_validation_error", error=ANY)

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_disabled_config(self, mock_live_feed: MagicMock) -> None:
        """Teszteli a live feed létrehozását disabled konfiggal."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"enabled": False, "host": "localhost", "tick_port": 1234}

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Ha disabled, akkor warning log, de nem dobunk kivételt
        assert live_feed is not None
        mock_logger.warning.assert_called()

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_missing_config(self, mock_live_feed: MagicMock) -> None:
        """Teszteli a live feed létrehozását hiányzó konfiggal."""
        mock_config = MagicMock()
        mock_config.get.return_value = None

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Graceful handling: default config
        assert live_feed is not None

    @patch("neural_ai.collectors.jforex.implementations.bi5_downloader.Bi5Downloader")
    @patch("aiohttp.ClientSession")
    def test_create_downloader_none_config(
        self, mock_session: MagicMock, mock_downloader: MagicMock
    ) -> None:
        """Teszteli a downloader létrehozását None konfiggal."""
        mock_config = MagicMock()
        mock_config.get.return_value = None

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        downloader = JForexFactory.create_downloader(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus, storage=mock_storage
        )

        # Graceful handling: default config
        assert downloader is not None

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_empty_host(self, mock_live_feed: MagicMock) -> None:
        """Teszteli a live feed létrehozását üres host stringgel."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"enabled": True, "host": "", "tick_port": 1234}

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Pydantic validáció hiba → fallback to default
        assert live_feed is not None
        mock_logger.error.assert_called_with("jforex_live_config_validation_error", error=ANY)

    @patch("neural_ai.collectors.jforex.implementations.bi5_downloader.Bi5Downloader")
    @patch("aiohttp.ClientSession")
    def test_create_downloader_returns_correct_interface(
        self, mock_session: MagicMock, mock_downloader: MagicMock
    ) -> None:
        """Teszteli, hogy a downloader a helyes interface-t implementálja."""
        mock_config = MagicMock()
        mock_config.get.return_value = {
            "download": {"timeout": 30, "max_retries": 3},
            "base_url": "https://datafeed.dukascopy.com",
        }

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()
        mock_storage = MagicMock()

        downloader = JForexFactory.create_downloader(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus, storage=mock_storage
        )

        # Interface típus ellenőrzés (mock)
        assert downloader is mock_downloader.return_value

    @patch("neural_ai.collectors.jforex.implementations.live_feed.JForexLiveFeed")
    def test_create_live_feed_returns_correct_interface(self, mock_live_feed: MagicMock) -> None:
        """Teszteli, hogy a live feed a helyes interface-t implementálja."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"enabled": True, "host": "localhost", "tick_port": 1234}

        mock_logger = MagicMock()
        mock_event_bus = MagicMock()

        live_feed = JForexFactory.create_live_feed(
            config=mock_config, logger=mock_logger, event_bus=mock_event_bus
        )

        # Interface típus ellenőrzés (mock)
        assert live_feed is mock_live_feed.return_value
