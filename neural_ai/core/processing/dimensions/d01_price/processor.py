"""D01PriceProcessor - Alap adatok processzor."""

from typing import TYPE_CHECKING

from neural_ai.core.processing.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    import polars as pl


class D01PriceProcessor(IDimensionProcessor):
    """D1 - Alap adatok (Base Data) processzor.

    Feladata az alap pénzügyi adatok biztosítása és validálása.
    Kiválasztja és visszaadja a timestamp, open, high, low, close,
    tick_volume, spread és real_volume oszlopokat.
    """

    def process(self, df: "pl.DataFrame") -> "pl.DataFrame":
        """Polars Expr alapú dimenzió számítás.

        Args:
            df: Bemeneti Polars DataFrame (már time-aligned OHLCV adatok)

        Returns:
            Polars DataFrame az alap adatokkal
        """
        return df.select(
            ["timestamp", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"]
        )

    @property
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: 1 (D1 dimenzió)
        """
        return 1
