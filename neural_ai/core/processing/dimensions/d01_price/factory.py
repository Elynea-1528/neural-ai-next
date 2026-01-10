"""D01PriceProcessor Factory - Az alap adatok processzor létrehozásáért felelős."""

from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.core.processing.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)


class D01PriceFactory:
    """Factory osztály a D01PriceProcessor létrehozásához."""

    @staticmethod
    def create() -> IDimensionProcessor:
        """D01PriceProcessor példány létrehozása.

        Returns:
            IDimensionProcessor: A D01PriceProcessor példány
        """
        return D01PriceProcessor()
