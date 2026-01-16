"""Dimenzió processzor interfész modul."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


class IDimensionProcessor(ABC):
    """Absztrakt interfész minden dimenzió processzor számára."""

    @abstractmethod
    def process(self, df: "pl.DataFrame") -> "pl.DataFrame":
        """Polars Expr alapú dimenzió számítás."""
        pass

    @property
    @abstractmethod
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15)."""
        pass
