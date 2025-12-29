"""JForex Collector Factory."""

from typing import TYPE_CHECKING
from neural_ai.collectors.jforex.interfaces.downloader_interface import IJForexDownloader

if TYPE_CHECKING:
    from neural_ai.core.base.interfaces import IConfig, ILogger
    from neural_ai.core.events.interfaces import IEventBus


class JForexFactory:
    """Factory for creating JForex Collector components.
    
    Provides dependency injection for JForex downloader instances.
    """
    
    @staticmethod
    def create_downloader(
        config: "IConfig",
        logger: "ILogger",
        event_bus: "IEventBus"
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