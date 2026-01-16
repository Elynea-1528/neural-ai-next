"""Időszinkronizációs interfész modul."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


class ITimeAlignmentService(ABC):
    """Időszinkronizációs szolgáltatás interfész - tökéletes időskála biztosítása."""

    @abstractmethod
    def reindex_to_grid(self, df: "pl.DataFrame", timeframe: str) -> "pl.DataFrame":
        """Tökéletes időskála generálása minden timeframe-re."""
        pass

    @abstractmethod
    def handle_gaps(
        self, df: "pl.DataFrame", timeframe: str, method: str = "forward_fill"
    ) -> "pl.DataFrame":
        """Lyukak kezelése az adatokban."""
        pass
