# collectors/jforex/factory.py

JForex Collector Factory.

## Osztályok

### `JForexFactory`

Factory for creating JForex Collector components.

    Provides dependency injection for JForex downloader instances.


## Függvények

### `create_downloader`

Create a JForex downloader instance with DI.

        Args:
            config: Configuration manager instance
            logger: Logger instance
            event_bus: Event bus for publishing market data
            storage: Storage interface for data persistence

        Returns:
            JForex downloader instance implementing IJForexDownloader

### `create_live_feed`

Create a JForex live feed instance with DI.

        Args:
            config: Configuration manager instance
            logger: Logger instance
            event_bus: Event bus for publishing market data

        Returns:
            JForex live feed instance implementing ILiveFeed


---

**Forrásfájl:** [`collectors/jforex/factory.py`](../../../neural_ai/collectors/jforex/factory.py)
