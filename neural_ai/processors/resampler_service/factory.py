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
    from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class ResamplerServiceFactory:
    """Factory osztály a ResamplerService létrehozásához és kezeléséhez."""

    @staticmethod
    def create(storage: "StorageInterface") -> ResamplerInterface:
        """ResamplerService példány létrehozása.

        Args:
            storage: A tárolási interfész példány

        Returns:
            ResamplerInterface: A létrehozott ResamplerService példány
        """
        return ResamplerService(storage=storage)

    @classmethod
    def get_instance(cls) -> ResamplerInterface:
        """ResamplerService példány lekérdezése a DI konténerből.

        Returns:
            ResamplerInterface: A ResamplerService példány

        Raises:
            ComponentNotFoundError: Ha a komponens nem található a konténerben
        """
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
            instance = cls.create(storage=storage)
            container.register(component_name, instance)
            return instance
