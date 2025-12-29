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
            
        Returns:
            JForex downloader instance implementing IJForexDownloader


---

**Forrásfájl:** [`collectors/jforex/factory.py`](../../../neural_ai/collectors/jforex/factory.py)
