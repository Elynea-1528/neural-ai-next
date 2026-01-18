"""JForex Collector Factory."""

from typing import TYPE_CHECKING, TypedDict, cast

from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed


class JForexConfig(TypedDict, total=False):
    """JForex konfiguráció séma."""

    base_url: str
    timeout: int
    retry_attempts: int
    storage_base_path: str
    validation_enabled: bool
    max_download_size_mb: int


class JForexLiveConfig(TypedDict, total=False):
    """JForex live feed konfiguráció séma."""

    host: str
    tick_port: int
    command_port: int
    enabled: bool


if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class JForexFactory:
    """Factory JForex Collector komponensek létrehozására.

    Dependency injection-t biztosít a JForex letöltő példányokhoz.
    """

    @staticmethod
    def create_downloader(
        config: "ConfigManagerInterface",
        logger: "LoggerInterface",
        event_bus: "EventBusInterface | None",
        storage: "StorageInterface",
    ) -> IJForexDownloader:
        """JForex letöltő példány létrehozása DI-vel.

        Args:
            config: Konfiguráció kezelő példány
            logger: Logger példány
            event_bus: Event bus piaci adatok publikálására
            storage: Storage interfész adat perzisztenciához

        Returns:
            JForex letöltő példány, ami megvalósítja az IJForexDownloader-t
        """
        from neural_ai.core.logger.factory import LoggerFactory

        logger = LoggerFactory.get_logger(__name__)
        # Import here to avoid circular dependencies
        import aiohttp

        from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader

        # Get JForex configuration
        jforex_config_raw = config.get("jforex")
        if jforex_config_raw is None:
            jforex_config = cast(JForexConfig, {})
        else:
            jforex_config = cast(JForexConfig, jforex_config_raw)

        # Create HTTP client with timeout
        timeout_value = jforex_config.get("timeout", 30) if jforex_config else 30
        timeout = aiohttp.ClientTimeout(total=timeout_value)
        http_client = aiohttp.ClientSession(timeout=timeout)

        # Get additional configuration options
        retry_attempts = jforex_config.get("retry_attempts", 3) if jforex_config else 3
        storage_base_path = (
            jforex_config.get("storage_base_path", "data/tick") if jforex_config else "data/tick"
        )
        validation_enabled = (
            jforex_config.get("validation_enabled", True) if jforex_config else True
        )
        max_download_size_mb = (
            jforex_config.get("max_download_size_mb", 50) if jforex_config else 50
        )

        # Create downloader instance
        downloader = Bi5Downloader(
            logger=logger,
            event_bus=event_bus,
            config=config,
            http_client=http_client,
            storage=storage,
        )

        logger.info(
            "jforex_downloader_created",
            base_url=jforex_config.get("base_url", "default"),
            timeout=timeout_value,
            retry_attempts=retry_attempts,
            storage_base_path=storage_base_path,
            validation_enabled=validation_enabled,
            max_download_size_mb=max_download_size_mb,
        )

        return downloader

    @staticmethod
    def create_live_feed(
        config: "ConfigManagerInterface", logger: "LoggerInterface", event_bus: "EventBusInterface"
    ) -> ILiveFeed:
        """JForex live feed példány létrehozása DI-vel.

        Args:
            config: Konfiguráció kezelő példány
            logger: Logger példány
            event_bus: Event bus piaci adatok publikálására

        Returns:
            JForex live feed példány, ami megvalósítja az ILiveFeed-et
        """
        from neural_ai.core.logger.factory import LoggerFactory

        logger = LoggerFactory.get_logger(__name__)
        # Import here to avoid circular dependencies
        from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed

        # Get JForex live configuration
        try:
            live_config_raw = config.get("jforex_live")
            if live_config_raw is None:
                live_config = cast(JForexLiveConfig, {})
            else:
                live_config = cast(JForexLiveConfig, live_config_raw)
        except KeyError:
            live_config = cast(JForexLiveConfig, {})

        # Check if live feed is enabled
        enabled = live_config.get("enabled", False) if live_config else False

        if not enabled:
            logger.warning(
                "jforex_live_feed_disabled",
                _message="JForex live feed is disabled in configuration",
            )

        # Create live feed instance
        live_feed = JForexLiveFeed(logger=logger, event_bus=event_bus, config=config)

        logger.info(
            "jforex_live_feed_created",
            host=live_config.get("host", "127.0.0.1"),
            tick_port=live_config.get("tick_port", 5555),
            enabled=enabled,
        )

        return live_feed
