"""JForex Collector Factory."""

from typing import TYPE_CHECKING, cast

from pydantic import ValidationError

from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed
from neural_ai.core.config.interfaces.types import JForexConfig, JForexLiveConfig

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
        # Import here to avoid circular dependencies
        import aiohttp

        from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader

        # Get JForex configuration
        jforex_config_raw = config.get("jforex")
        raw_data: dict[str, object] = (
            cast(dict[str, object], jforex_config_raw)
            if isinstance(jforex_config_raw, dict)
            else {}
        )

        try:
            jforex_config = JForexConfig.model_validate(raw_data)
        except ValidationError as e:
            logger.error("jforex_config_validation_error", error=str(e))
            jforex_config = JForexConfig.model_validate({})

        # Create HTTP client with timeout
        timeout_value = 30
        if jforex_config.download and jforex_config.download.timeout:
            timeout_value = jforex_config.download.timeout

        timeout = aiohttp.ClientTimeout(total=timeout_value)
        http_client = aiohttp.ClientSession(timeout=timeout)

        # Get additional configuration options
        retry_attempts = 3
        if jforex_config.download and jforex_config.download.max_retries:
            retry_attempts = jforex_config.download.max_retries

        # Storage path is handled by storage subsystem, used here for logging
        storage_base_path = "data/tick"
        # Validation and max download size are legacy/internal defaults
        validation_enabled = True
        max_download_size_mb = 50

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
            base_url=jforex_config.base_url or "default",
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
        # Import here to avoid circular dependencies
        from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed

        # Get JForex live configuration
        live_config_raw = config.get("jforex_live")
        raw_data: dict[str, object] = (
            cast(dict[str, object], live_config_raw) if isinstance(live_config_raw, dict) else {}
        )

        try:
            live_config = JForexLiveConfig.model_validate(raw_data)
        except ValidationError as e:
            logger.error("jforex_live_config_validation_error", error=str(e))
            live_config = JForexLiveConfig.model_validate({})

        # Check if live feed is enabled
        enabled = live_config.enabled or False

        if not enabled:
            logger.warning(
                "jforex_live_feed_disabled",
                _message="JForex live feed is disabled in configuration",
            )

        # Create live feed instance
        live_feed = JForexLiveFeed(logger=logger, event_bus=event_bus, config=config)

        logger.info(
            "jforex_live_feed_created",
            host=live_config.host or "127.0.0.1",
            tick_port=live_config.tick_port or 5555,
            enabled=enabled,
        )

        return live_feed
