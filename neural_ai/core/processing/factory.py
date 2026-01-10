"""Processing Factory - Feldolgozási komponensek factory függvényei."""

from neural_ai.core.processing.dimensions.d01_price.factory import D01PriceFactory
from neural_ai.core.processing.implementations.time_alignment_service import TimeAlignmentService
from neural_ai.core.processing.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.core.processing.interfaces.time_alignment_interface import ITimeAlignmentService


def create_time_alignment_service() -> ITimeAlignmentService:
    """TimeAlignmentService factory függvény."""
    return TimeAlignmentService()


def create_dimension_processor(dimension_id: int) -> IDimensionProcessor:
    """Dimension processor factory függvény.

    Args:
        dimension_id: A dimenzió azonosítója (1-15)

    Returns:
        IDimensionProcessor: A megfelelő dimenzió processor példány

    Raises:
        ValueError: Ha ismeretlen dimenzió ID-t adnak meg
    """
    if dimension_id == 1:
        return D01PriceFactory.create()
    else:
        raise ValueError(f"Ismeretlen dimenzió ID: {dimension_id}")
