"""D02SupportProcessor Factory - A Support/Resistance processzor létrehozásáért felelős."""

from typing import TYPE_CHECKING

from neural_ai.processors.dimensions.d02_support.implementations.support_processor import (
    D02SupportProcessor,
)
from neural_ai.processors.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class D02SupportFactory:
    """Factory osztály a D02SupportProcessor létrehozásához."""

    @staticmethod
    def create(config: "ConfigManagerInterface", logger: "LoggerInterface") -> IDimensionProcessor:
        """D02SupportProcessor példány létrehozása.

        Args:
            config: Konfigurációs menedzser interfész
            logger: Logger interfész

        Returns:
            IDimensionProcessor: A D02SupportProcessor példány
        """
        return D02SupportProcessor(config, logger)
