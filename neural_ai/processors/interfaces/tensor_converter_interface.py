"""Tensor konverter interfész modul."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np


class ITensorConverter(ABC):
    """Tensor konverter interfész."""

    @abstractmethod
    def convert_to_tensor(self, data: "np.ndarray") -> "np.ndarray":
        """Adatok konvertálása tensor formátumba."""
        pass
