"""
Komponens sablon a Neural-AI-Next projekthez.

Ez a fájl egy általános komponens implementációs sablont tartalmaz,
amelyet új komponensek létrehozásakor lehet alapul venni.
"""

import logging
from typing import Any, Dict, List, Optional, Union  # noqa: F401 - Sablon részeként szerepel

import numpy as np  # noqa: F401 - Sablon részeként szerepel

from neural_ai.core.config import ConfigManagerFactory  # noqa: F401 - Sablon részeként szerepel
from neural_ai.core.logger import LoggerInterface


class ComponentTemplate:
    """Alap template komponens osztály."""

    def __init__(self, config: Dict[str, Any], logger: LoggerInterface = None):
        """
        ComponentTemplate inicializálása.

        Args:
            config: Komponens konfigurációja
            logger: Logger példány
        """
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("ComponentTemplate inicializálva")

    def run(self) -> Dict[str, Any]:
        """
        Komponens futtatása.

        Returns:
            Dict[str, Any]: Komponens kimenete
        """
        self.logger.info("ComponentTemplate futtatása")
        return {"status": "success"}


class ComponentName:
    """
    Komponens leírása.

    A komponens felelőssége részletesen kifejtve. Ide írd a komponens
    funkcióinak, céljának és használati módjának általános leírását.

    Attributes:
        config: A komponens konfigurációja
        logger: Logger példány
        dependencies: Egyéb függőségek leírása
    """

    def __init__(self, config: Dict[str, Any], logger=None):
        """
        Inicializálja a komponenst.

        Args:
            config: Komponens konfigurációja
            logger: Logger példány vagy None (ekkor alapértelmezett logger jön létre)
        """
        self.config = config
        self.logger = logger or LoggerFactory.get_logger(__name__)

        # Konfigurációs értékek kiolvasása
        self.parameter1 = config.get("parameter1", "default_value")
        self.parameter2 = config.get("parameter2", 100)

        # Függőségek inicializálása
        self._init_dependencies()

        self.logger.info(
            f"{self.__class__.__name__} initialized with "
            f"parameter1={self.parameter1}, parameter2={self.parameter2}"
        )

    def _init_dependencies(self):
        """Belső függőségek inicializálása."""
        # Példa: storage inicializálása
        # storage_config = self.config.get("storage", {})
        # self.storage = StorageFactory.get_storage(storage_config)
        pass

    def main_method(self, input_data: Any) -> Any:
        """
        Fő komponens metódus.

        Args:
            input_data: Bemeneti adatok

        Returns:
            Feldolgozott kimeneti adatok

        Raises:
            ComponentException: Hiba esetén
        """
        self.logger.debug(f"Processing input data: {input_data}")

        try:
            # Feldolgozás implementációja
            result = self._process(input_data)

            self.logger.info(f"Successfully processed data, result shape: {len(result)}")
            return result

        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            raise ComponentException(f"Processing failed: {str(e)}") from e

    def _process(self, data: Any) -> Any:
        """
        Belső feldolgozó metódus.

        Args:
            data: Feldolgozandó adatok

        Returns:
            Feldolgozott adatok
        """
        # Implementáció...
        return data


class ComponentException(Exception):
    """A komponens specifikus kivétele."""

    pass


# Factory példa
class ComponentNameFactory:
    """Factory osztály a komponens létrehozásához."""

    @staticmethod
    def create_component(config: Dict[str, Any], logger=None) -> ComponentName:
        """
        Létrehoz egy új komponens példányt.

        Args:
            config: Komponens konfiguráció
            logger: Opcionális logger példány

        Returns:
            ComponentName: Új komponens példány
        """
        return ComponentName(config, logger)
