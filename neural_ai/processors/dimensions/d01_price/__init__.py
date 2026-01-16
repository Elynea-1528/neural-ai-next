"""D01 Price Dimension Processzor modul."""

from neural_ai.processors.dimensions.d01_price.factory import D01PriceFactory
from neural_ai.processors.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

__all__ = ["D01PriceFactory", "IDimensionProcessor"]
