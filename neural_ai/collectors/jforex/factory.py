"""JForex Collector Factory."""

from typing import TYPE_CHECKING
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader
from neural_ai.collectors.jforex.interfaces.live_interface import ILiveFeed

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class JForexFactory:
    """Factory for creating JForex Collector components.
    
    Provides dependency injection for JForex downloader instances.
    """
    
    @staticmethod
    def create_downloader(
        config: "ConfigManagerInterface",
        logger: "LoggerInterface",
        event_bus: "EventBusInterface"
    ) -> IJForexDownloader:
        """Create a JForex downloader instance with DI.
        
        Args:
            config: Configuration manager instance
            logger: Logger instance
            event_bus: Event bus for publishing market data
            
        Returns:
            JForex downloader instance implementing IJForexDownloader
        """
        # Import here to avoid circular dependencies
        from neural_ai.collectors.jforex.implementations.bi5_downloader import Bi5Downloader
        import aiohttp
        
        # Get JForex configuration
        try:
            jforex_config = config.get("jforex", {}) or {}
        except (KeyError, ValueError, AttributeError):
            jforex_config = {}
        
        # Create HTTP client with timeout
        timeout_value = jforex_config.get("timeout", 30) if jforex_config else 30
        timeout = aiohttp.ClientTimeout(total=timeout_value)
        http_client = aiohttp.ClientSession(timeout=timeout)
        
        # Create downloader instance
        downloader = Bi5Downloader(
            logger=logger,
            event_bus=event_bus,
            config=config,
            http_client=http_client
        )
        
        logger.info(
            "jforex_downloader_created",
            base_url=jforex_config.get("base_url", "default")
        )
        
        return downloader
    
    @staticmethod
    def create_live_feed(
        config: "ConfigManagerInterface",
        logger: "LoggerInterface",
        event_bus: "EventBusInterface"
    ) -> ILiveFeed:
        """Create a JForex live feed instance with DI.
        
        Args:
            config: Configuration manager instance
            logger: Logger instance
            event_bus: Event bus for publishing market data
            
        Returns:
            JForex live feed instance implementing ILiveFeed
        """
        # Import here to avoid circular dependencies
        from neural_ai.collectors.jforex.implementations.live_feed import JForexLiveFeed
        
        # Get JForex live configuration
        try:
            live_config = config.get("jforex_live", {}) or {}
        except (KeyError, ValueError, AttributeError):
            live_config = {}
        
        # Check if live feed is enabled
        enabled = live_config.get("enabled", False) if live_config else False
        
        if not enabled:
            logger.warning(
                "jforex_live_feed_disabled",
                _message="JForex live feed is disabled in configuration"
            )
        
        # Create live feed instance
        live_feed = JForexLiveFeed(
            logger=logger,
            event_bus=event_bus,
            config=config
        )
        
        logger.info(
            "jforex_live_feed_created",
            host=live_config.get("host", "127.0.0.1"),
            tick_port=live_config.get("tick_port", 5555),
            enabled=enabled
        )
        
        return live_feed