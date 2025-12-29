# collectors/jforex/interfaces/tick_data.py

Tick Data Model for JForex Collector.

## Osztályok

### `TickData`

Tick data model for JForex market data.
    
    Represents a single tick (bid/ask price pair) from Dukascopy.
    
    Attributes:
        timestamp: UTC timestamp of the tick
        symbol: Trading symbol (e.g., 'EURUSD')
        bid: Bid price (5 decimal places for forex)
        ask: Ask price (5 decimal places for forex)
        source: Data source identifier (default: 'jforex')


## Függvények

### `spread`

Calculate spread in pips.
        
        Returns:
            Spread in pips (1 pip = 0.0001 for most forex pairs)

### `mid_price`

Calculate mid price (average of bid and ask).
        
        Returns:
            Mid price rounded to 5 decimal places


---

**Forrásfájl:** [`collectors/jforex/interfaces/tick_data.py`](../../../neural_ai/collectors/jforex/interfaces/tick_data.py)
