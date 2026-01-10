from neural_ai.core.processing.implementations.time_alignment_service import TimeAlignmentService
from neural_ai.core.processing.interfaces.time_alignment_interface import ITimeAlignmentService


def create_time_alignment_service() -> ITimeAlignmentService:
    """TimeAlignmentService factory függvény."""
    return TimeAlignmentService()
