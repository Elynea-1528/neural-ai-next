"""Tick Data Model for JForex Collector."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TickData:
    """Tick data model for JForex market data.
    
    Represents a single tick (bid/ask price pair) from Dukascopy.
    
    Attributes:
        timestamp: UTC timestamp of the tick
        symbol: Trading symbol (e.g., 'EURUSD')
        bid: Bid price (5 decimal places for forex)
        ask: Ask price (5 decimal places for forex)
        source: Data source identifier (default: 'jforex')
    """
    
    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    source: str = "jforex"
    
    @property
    def spread(self) -> float:
        """Calculate spread in pips.
        
        Returns:
            Spread in pips (1 pip = 0.0001 for most forex pairs)
        """
        return round((self.ask - self.bid) * 10000, 1)
    
    @property
    def mid_price(self) -> float:
        """Calculate mid price (average of bid and ask).
        
        Returns:
            Mid price rounded to 5 decimal places
        """
        return round((self.bid + self.ask) / 2, 5)