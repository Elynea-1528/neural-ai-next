"""D01PriceProcessor Factory - Az alap adatok processzor létrehozásáért felelős."""

from typing import TYPE_CHECKING

from neural_ai.core.processing.dimensions.d01_price.processor import D01PriceProcessor
from neural_ai.core.processing.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class D01PriceFactory:
    """Factory osztály a D01PriceProcessor létrehozásához."""

    @staticmethod
    def create(config: "ConfigManagerInterface", logger: "LoggerInterface") -> IDimensionProcessor:
        """D01PriceProcessor példány létrehozása.

        Args:
            config: Konfigurációs menedzser interfész
            logger: Logger interfész

        Returns:
            IDimensionProcessor: A D01PriceProcessor példány
        """
        return D01PriceProcessor(config, logger)
