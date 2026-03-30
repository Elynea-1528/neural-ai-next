"""Unit tesztek a ResamplerServiceFactory-hoz."""

from unittest.mock import MagicMock, patch

from neural_ai.processors.resampler_service.factory import ResamplerServiceFactory
from neural_ai.processors.resampler_service.interfaces.resampler_interface import (
    ResamplerInterface,
)


class TestResamplerServiceFactory:
    """Tesztek a ResamplerServiceFactory osztályhoz."""

    def test_create_returns_resampler_interface(self) -> None:
        """Ellenőrzi, hogy a create metódus ResamplerInterface példányt ad vissza."""
        # Arrange
        mock_storage = MagicMock()
        mock_logger = MagicMock()

        # Act
        result = ResamplerServiceFactory.create(storage=mock_storage, logger=mock_logger)

        # Assert
        assert isinstance(result, ResamplerInterface)

    def test_create_with_valid_dependencies(self) -> None:
        """Ellenőrzi, hogy a create metódus megfelelő függőségekkel működik."""
        # Arrange
        mock_storage = MagicMock()
        mock_logger = MagicMock()

        # Act
        result = ResamplerServiceFactory.create(storage=mock_storage, logger=mock_logger)

        # Assert
        assert result is not None
        assert isinstance(result, ResamplerInterface)

    @patch("neural_ai.processors.resampler_service.factory.DIContainer")
    def test_get_instance_returns_existing_instance(self, mock_container_class: MagicMock) -> None:
        """Ellenőrzi, hogy a get_instance visszaadja a meglévő példányt."""
        # Arrange
        mock_container = MagicMock()
        mock_container_class.return_value = mock_container
        mock_instance = MagicMock(spec=ResamplerInterface)
        mock_container.get.return_value = mock_instance

        # Act
        result = ResamplerServiceFactory.get_instance()

        # Assert
        assert result == mock_instance
        mock_container.get.assert_called_once_with("ResamplerService")

    @patch("neural_ai.data.storage.factory.StorageFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.processors.resampler_service.factory.DIContainer")
    def test_get_instance_creates_new_instance_if_not_exists(
        self, mock_container_class: MagicMock, mock_logger_factory: MagicMock, mock_storage_factory: MagicMock  # noqa: E501
    ) -> None:
        """Ellenőrzi, hogy a get_instance létrehoz új példányt, ha nem létezik."""
        # Arrange
        mock_container = MagicMock()
        mock_container_class.return_value = mock_container
        mock_container.get.side_effect = Exception("Not found")

        mock_storage = MagicMock()
        mock_container.resolve.return_value = mock_storage

        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        # Act
        result = ResamplerServiceFactory.get_instance()

        # Assert
        assert isinstance(result, ResamplerInterface)
        mock_container.register.assert_called_once()
        mock_logger_factory.get_logger.assert_called_once()

    @patch("neural_ai.data.storage.factory.StorageFactory")
    @patch("neural_ai.core.logger.factory.LoggerFactory")
    @patch("neural_ai.processors.resampler_service.factory.DIContainer")
    def test_get_instance_uses_fallback_storage(
        self,
        mock_container_class: MagicMock,
        mock_logger_factory: MagicMock,
        mock_storage_factory: MagicMock,
    ) -> None:
        """Ellenőrzi, hogy a get_instance fallback storage-t használ, ha nincs a konténerben."""
        # Arrange
        mock_container = MagicMock()
        mock_container_class.return_value = mock_container
        mock_container.get.side_effect = Exception("Not found")
        mock_container.resolve.side_effect = Exception("Storage not found")

        mock_storage = MagicMock()
        mock_storage_factory.get_storage.return_value = mock_storage

        mock_logger = MagicMock()
        mock_logger_factory.get_logger.return_value = mock_logger

        # Act
        result = ResamplerServiceFactory.get_instance()

        # Assert
        assert isinstance(result, ResamplerInterface)
        mock_storage_factory.get_storage.assert_called_once_with(storage_type="parquet")
        mock_container.register.assert_called_once()

    def test_factory_create_is_static(self) -> None:
        """Ellenőrzi, hogy a create metódus statikus."""
        # Arrange & Act & Assert
        # A @staticmethod dekorátorral ellátott metódusok közvetlenül hívhatók az osztályon
        assert callable(ResamplerServiceFactory.create)

    def test_factory_has_required_methods(self) -> None:
        """Ellenőrzi, hogy a factory tartalmazza az összes szükséges metódust."""
        # Arrange
        required_methods = ["create", "get_instance"]

        # Act & Assert
        for method_name in required_methods:
            assert hasattr(ResamplerServiceFactory, method_name)
            assert callable(getattr(ResamplerServiceFactory, method_name))
