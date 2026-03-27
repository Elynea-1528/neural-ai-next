"""Unit tesztek az ai_service modulhoz.

Ez a modul teszteli az AIService osztály funkcióit.
"""

from unittest.mock import MagicMock

import pytest

from neural_ai.ui.services.ai_service import AIService


class TestAIServiceInit:
    """Tesztek az AIService inicializálásához."""

    def test_init_creates_instance(self) -> None:
        """Ellenőrzi, hogy az AIService létrehozható."""
        # Arrange
        mock_logger = MagicMock()
        mock_config = {}
        mock_core = MagicMock()

        # Act
        service = AIService(
            logger=mock_logger,
            config=mock_config,
            core_components=mock_core,
        )

        # Assert
        assert service._logger == mock_logger  # type: ignore
        assert service._config == mock_config  # type: ignore
        assert service._core_components == mock_core  # type: ignore
        assert len(service._models) == 3  # type: ignore
        assert service._loaded_models == {}  # type: ignore
        assert service._training_jobs == {}  # type: ignore


class TestAIServiceGetAvailableModels:
    """Tesztek a get_available_models metódushoz."""

    def test_get_available_models_returns_list(self) -> None:
        """Ellenőrzi, hogy a modellek listáját adja vissza."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act
        result = service.get_available_models()

        # Assert
        assert isinstance(result, list)
        assert len(result) == 3
        assert all("id" in model for model in result)
        assert all("name" in model for model in result)
        assert all("description" in model for model in result)
        assert all("type" in model for model in result)
        assert all("status" in model for model in result)


class TestAIServiceLoadModel:
    """Tesztek a load_model metódushoz."""

    def test_load_model_raises_error_for_unknown_model(self) -> None:
        """Ellenőrzi, hogy hiba dobódik ismeretlen modellre."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Ismeretlen modell: unknown"):
            service.load_model("unknown")

    def test_load_model_raises_error_for_unavailable_model(self) -> None:
        """Ellenőrzi, hogy hiba dobódik nem elérhető modellre."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Modell nem elérhető: transformer_model"):
            service.load_model("transformer_model")

    def test_load_model_success(self) -> None:
        """Ellenőrzi, hogy a modell betöltése sikeres."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act
        result = service.load_model("hierarchical_v1")

        # Assert
        assert result is True
        assert "hierarchical_v1" in service._loaded_models  # type: ignore

    def test_load_model_with_config(self) -> None:
        """Ellenőrzi, hogy a modell betöltése konfigurációval működik."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        model_config = {"param1": "value1"}

        # Act
        result = service.load_model("hierarchical_v1", config=model_config)

        # Assert
        assert result is True
        assert service._loaded_models["hierarchical_v1"]["config"] == model_config  # type: ignore


class TestAIServiceRunInference:
    """Tesztek a run_inference metódushoz."""

    def test_run_inference_raises_error_for_unloaded_model(self) -> None:
        """Ellenőrzi, hogy hiba dobódik nem betöltött modellre."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Modell nincs betöltve: hierarchical_v1"):
            service.run_inference("hierarchical_v1", {})

    def test_run_inference_success(self) -> None:
        """Ellenőrzi, hogy az inferencia futtatása sikeres."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        service.load_model("hierarchical_v1")
        input_data = {"symbol": "EURUSD", "timeframe": "H1"}

        # Act
        result = service.run_inference("hierarchical_v1", input_data)

        # Assert
        assert "model_id" in result
        assert "prediction" in result
        assert "confidence" in result
        assert "timestamp" in result
        assert result["input_data"] == input_data


class TestAIServiceGetModelInfo:
    """Tesztek a get_model_info metódushoz."""

    def test_get_model_info_raises_error_for_unknown_model(self) -> None:
        """Ellenőrzi, hogy hiba dobódik ismeretlen modellre."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Ismeretlen modell: unknown"):
            service.get_model_info("unknown")

    def test_get_model_info_success(self) -> None:
        """Ellenőrzi, hogy a modell információk lekérdezése sikeres."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act
        result = service.get_model_info("hierarchical_v1")

        # Assert
        assert result["id"] == "hierarchical_v1"
        assert "name" in result
        assert "description" in result
        assert "type" in result
        assert "status" in result
        assert "parameters" in result
        assert "accuracy" in result
        assert "last_trained" in result


class TestAIServiceTrainModel:
    """Tesztek a train_model metódushoz."""

    def test_train_model_raises_error_for_unknown_model(self) -> None:
        """Ellenőrzi, hogy hiba dobódik ismeretlen modellre."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Ismeretlen modell: unknown"):
            service.train_model("unknown", [])

    def test_train_model_success(self) -> None:
        """Ellenőrzi, hogy a modell tanítása sikeres."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        training_data = [{"input": "data1"}, {"input": "data2"}]

        # Act
        result = service.train_model("hierarchical_v1", training_data)

        # Assert
        assert "training_id" in result
        assert result["model_id"] == "hierarchical_v1"
        assert result["status"] == "started"
        assert "message" in result

    def test_train_model_with_config(self) -> None:
        """Ellenőrzi, hogy a modell tanítása konfigurációval működik."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        training_data = [{"input": "data1"}]
        training_config = {"epochs": 100, "batch_size": 32}

        # Act
        result = service.train_model("hierarchical_v1", training_data, config=training_config)

        # Assert
        assert "training_id" in result
        training_id = result["training_id"]
        assert service._training_jobs[training_id]["config"] == training_config  # type: ignore


class TestAIServiceGetTrainingStatus:
    """Tesztek a get_training_status metódushoz."""

    def test_get_training_status_raises_error_for_unknown_training(self) -> None:
        """Ellenőrzi, hogy hiba dobódik ismeretlen tanításra."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Ismeretlen tanítás: unknown"):
            service.get_training_status("unknown")

    def test_get_training_status_success(self) -> None:
        """Ellenőrzi, hogy a tanítás állapotának lekérdezése sikeres."""
        # Arrange
        service = AIService(
            logger=MagicMock(),
            config={},
            core_components=MagicMock(),
        )
        training_data = [{"input": "data1"}]
        train_result = service.train_model("hierarchical_v1", training_data)
        training_id = train_result["training_id"]

        # Act
        result = service.get_training_status(training_id)

        # Assert
        assert result["training_id"] == training_id
        assert result["model_id"] == "hierarchical_v1"
        assert "status" in result
        assert "progress" in result
        assert "epoch" in result
        assert "loss" in result
        assert "started_at" in result
        assert "estimated_completion" in result
