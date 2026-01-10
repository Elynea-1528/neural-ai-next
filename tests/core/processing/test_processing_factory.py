"""Processing Factory unit tesztek."""

import pytest

from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.core.processing.factory import (
    create_dimension_processor,
    create_time_alignment_service,
)
from neural_ai.core.processing.implementations.time_alignment_service import TimeAlignmentService
from neural_ai.core.processing.interfaces.dimension_processor_interface import IDimensionProcessor
from neural_ai.core.processing.interfaces.time_alignment_interface import ITimeAlignmentService


class TestProcessingFactory:
    """Processing Factory unit teszt osztály."""

    def test_create_time_alignment_service(self):
        """Teszteli a create_time_alignment_service függvényt."""
        service = create_time_alignment_service()

        assert isinstance(service, TimeAlignmentService)
        assert isinstance(service, ITimeAlignmentService)

    def test_create_dimension_processor_d1(self):
        """Teszteli a create_dimension_processor függvényt D1 dimenzióval."""
        processor = create_dimension_processor(1)

        assert isinstance(processor, D01PriceProcessor)
        assert isinstance(processor, IDimensionProcessor)
        assert processor.dimension_id == 1

    def test_create_dimension_processor_invalid_id(self):
        """Teszteli a create_dimension_processor függvényt érvénytelen ID-val."""
        with pytest.raises(ValueError, match="Ismeretlen dimenzió ID: 999"):
            create_dimension_processor(999)

    def test_create_dimension_processor_negative_id(self):
        """Teszteli a create_dimension_processor függvényt negatív ID-val."""
        with pytest.raises(ValueError, match="Ismeretlen dimenzió ID: -1"):
            create_dimension_processor(-1)

    def test_create_dimension_processor_zero_id(self):
        """Teszteli a create_dimension_processor függvényt 0 ID-val."""
        with pytest.raises(ValueError, match="Ismeretlen dimenzió ID: 0"):
            create_dimension_processor(0)
