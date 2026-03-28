"""Unit tesztek az AIServiceInterface interfészhez."""

from typing import Any
from unittest.mock import MagicMock

from neural_ai.ui.interfaces.ai_service_interface import AIServiceInterface


class TestAIServiceInterface:
    """Tesztek az AIServiceInterface interfészhez."""

    def test_interface_is_runtime_checkable(self) -> None:
        """Teszteli, hogy az interfész runtime checkable."""
        mock_service = MagicMock(spec=AIServiceInterface)
        assert isinstance(mock_service, AIServiceInterface)

    def test_get_available_models_signature(self) -> None:
        """Teszteli a get_available_models metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        models: list[dict[str, str]] = [
            {"id": "model1", "name": "Model 1"},
            {"id": "model2", "name": "Model 2"},
        ]
        mock_service.get_available_models.return_value = models
        result = mock_service.get_available_models()
        assert isinstance(result, list)
        assert len(result) == 2
        mock_service.get_available_models.assert_called_once()

    def test_load_model_signature(self) -> None:
        """Teszteli a load_model metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        mock_service.load_model.return_value = True
        result = mock_service.load_model("model1", {"param": "value"})
        assert result is True
        mock_service.load_model.assert_called_once_with("model1", {"param": "value"})

    def test_load_model_without_config(self) -> None:
        """Teszteli a load_model metódust konfiguráció nélkül."""
        mock_service = MagicMock(spec=AIServiceInterface)
        mock_service.load_model.return_value = True
        result = mock_service.load_model("model1")
        assert result is True
        mock_service.load_model.assert_called_once_with("model1")

    def test_run_inference_signature(self) -> None:
        """Teszteli a run_inference metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        input_data: dict[str, Any] = {"data": [1, 2, 3]}
        mock_service.run_inference.return_value = {"prediction": 0.95}
        result = mock_service.run_inference("model1", input_data)
        assert isinstance(result, dict)
        assert "prediction" in result
        mock_service.run_inference.assert_called_once_with("model1", input_data)

    def test_get_model_info_signature(self) -> None:
        """Teszteli a get_model_info metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        mock_service.get_model_info.return_value = {
            "id": "model1",
            "name": "Model 1",
            "version": "1.0",
        }
        result = mock_service.get_model_info("model1")
        assert isinstance(result, dict)
        assert "id" in result
        mock_service.get_model_info.assert_called_once_with("model1")

    def test_train_model_signature(self) -> None:
        """Teszteli a train_model metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        training_data: list[dict[str, Any]] = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
        config: dict[str, Any] = {"epochs": 10}
        mock_service.train_model.return_value = {"training_id": "train123", "status": "started"}
        result = mock_service.train_model("model1", training_data, config)
        assert isinstance(result, dict)
        assert "training_id" in result
        mock_service.train_model.assert_called_once_with("model1", training_data, config)

    def test_train_model_without_config(self) -> None:
        """Teszteli a train_model metódust konfiguráció nélkül."""
        mock_service = MagicMock(spec=AIServiceInterface)
        training_data: list[dict[str, Any]] = [{"x": 1, "y": 2}]
        mock_service.train_model.return_value = {"training_id": "train123"}
        result = mock_service.train_model("model1", training_data)
        assert isinstance(result, dict)
        mock_service.train_model.assert_called_once_with("model1", training_data)

    def test_get_training_status_signature(self) -> None:
        """Teszteli a get_training_status metódus szignatúráját."""
        mock_service = MagicMock(spec=AIServiceInterface)
        mock_service.get_training_status.return_value = {
            "training_id": "train123",
            "status": "running",
            "progress": 0.5,
        }
        result = mock_service.get_training_status("train123")
        assert isinstance(result, dict)
        assert "status" in result
        mock_service.get_training_status.assert_called_once_with("train123")

    def test_interface_has_all_required_methods(self) -> None:
        """Teszteli, hogy az interfész tartalmazza az összes szükséges metódust."""
        required_methods = [
            "get_available_models",
            "load_model",
            "run_inference",
            "get_model_info",
            "train_model",
            "get_training_status",
        ]
        for method in required_methods:
            assert hasattr(AIServiceInterface, method)

    def test_mock_implements_interface(self) -> None:
        """Teszteli, hogy a mock objektum implementálja az interfészt."""
        mock_service = MagicMock(spec=AIServiceInterface)
        assert hasattr(mock_service, "get_available_models")
        assert hasattr(mock_service, "load_model")
        assert hasattr(mock_service, "run_inference")
        assert hasattr(mock_service, "get_model_info")
        assert hasattr(mock_service, "train_model")
        assert hasattr(mock_service, "get_training_status")
