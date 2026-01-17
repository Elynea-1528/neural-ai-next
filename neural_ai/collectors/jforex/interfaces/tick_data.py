"""Tick Data Model for JForex Collector."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TickData:
    """Tick adat modell JForex piaci adatokhoz.

    Egyetlen tick-et reprezentál (bid/ask ár pár) a Dukascopy-tól.

    Attributes:
        timestamp: Tick UTC időbélyege
        symbol: Kereskedelmi szimbólum (pl. 'EURUSD')
        bid: Bid ár (5 tizedesjeggyel forexhez)
        ask: Ask ár (5 tizedesjeggyel forexhez)
        ask_volume: Ask volume (opcionális, 20-bájtos formátumhoz)
        bid_volume: Bid volume (opcionális, 20-bájtos formátumhoz)
        source: Adatforrás azonosító (alapértelmezett: 'jforex')
    """

    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    ask_volume: float | None = None
    bid_volume: float | None = None
    source: str = "jforex"

    @property
    def spread(self) -> float:
        """Spread kiszámítása pip-ben.

        Returns:
            Spread pip-ben (1 pip = 0.0001 a legtöbb forex párnál)
        """
        return round((self.ask - self.bid) * 10000, 1)

    @property
    def mid_price(self) -> float:
        """Mid ár kiszámítása (bid és ask átlaga).

        Returns:
            Mid ár, 5 tizedesjegyre kerekítve
        """
        return round((self.bid + self.ask) / 2, 5)
