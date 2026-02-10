"""BaseDimensionProcessor - Absztrakt alap osztály minden dimenzió processzor számára."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from neural_ai.processors.interfaces.dimension_processor_interface import (
    IDimensionProcessor,
)

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class BaseDimensionProcessor(IDimensionProcessor, ABC):
    """Absztrakt alap osztály minden dimenzió processzor számára.

    Ez az osztály biztosítja a Dependency Injection támogatást és az alapvető
    konfigurációs kezelést minden dimenzió processzor számára.
    """

    def __init__(self, config: "ConfigManagerInterface", logger: "LoggerInterface") -> None:
        """Inicializálja a dimenzió processzort DI-val.

        Args:
            config: Konfigurációs menedzser interfész
            logger: Logger interfész
        """
        self.config = config
        self.logger = logger

        # Konfiguráció betöltése dimenzió alapján (pl. "processors.d01")
        section = f"processors.d{self.dimension_id:02d}"
        self.dim_config: dict[str, Any] = (
            config.get("processors", f"d{self.dimension_id:02d}") or {}
        )

        if not self.dim_config:
            self.logger.warning(
                f"Nincs konfiguráció definiálva a(z) {section} szekcióban. "
                f"Alapértelmezett értékek használata."
            )

    @property
    @abstractmethod
    def dimension_id(self) -> int:
        """Dimenzió azonosító (1-15).

        Returns:
            int: A dimenzió egyedi azonosítója
        """
        pass
