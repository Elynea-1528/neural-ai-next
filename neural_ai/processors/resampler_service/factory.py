"""ResamplerService Factory - A ResamplerService létrehozásáért felelős."""

from typing import TYPE_CHECKING

from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.processors.resampler_service.implementations.resampler_service import (
    ResamplerService,
)
from neural_ai.processors.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class ResamplerServiceFactory:
    """Factory osztály a ResamplerService létrehozásához és kezeléséhez."""

    @staticmethod
    def create(
        storage: "StorageInterface",
        logger: "LoggerInterface",
    ) -> ResamplerInterface:
        """ResamplerService példány létrehozása.

        Args:
            storage: A tárolási interfész példány
            logger: A naplózási interfész

        Returns:
            ResamplerInterface: A létrehozott ResamplerService példány
        """
        return ResamplerService(storage=storage, logger=logger)

    @classmethod
    def get_instance(cls) -> ResamplerInterface:
        """ResamplerService példány lekérdezése a DI konténerből.

        Returns:
            ResamplerInterface: A ResamplerService példány

        Raises:
            ComponentNotFoundError: Ha a komponens nem található a konténerben
        """
        from neural_ai.core.logger.factory import LoggerFactory

        container = DIContainer()

        # A komponens neve, amivel regisztrálva van
        component_name = "ResamplerService"

        try:
            # Megpróbáljuk lekérni a meglévő példányt
            instance = container.get(component_name)
            return instance  # type: ignore
        except Exception:
            # Ha nem létezik, létrehozzuk és regisztráljuk
            from neural_ai.data.storage.factory import StorageFactory

            storage = StorageFactory.get_storage(storage_type="parquet")
            logger = LoggerFactory.get_logger(__name__)
            instance = cls.create(storage=storage, logger=logger)
            container.register(component_name, instance)
            return instance
