"""Unit tesztek a neural_ai/__init__.py modulhoz.

Ez a teszt modul biztosítja a 100% statement és branch coverage-t
a neural_ai/__init__.py fájlhoz. Teszteli a verziókezelést, konstansokat,
és a logger inicializálását.
"""

from importlib import metadata
from unittest.mock import MagicMock, patch

import pytest


class TestVersionManagement:
    """Verziókezelés tesztelése."""

    def test_version_loaded_from_metadata_successfully(self) -> None:
        """Teszt: __version__ sikeresen betöltődik a metadata-ból."""
        # Arrange & Act
        with patch("neural_ai.metadata.version", return_value="2.5.3"):
            # Újra importáljuk a modult a mock-kal
            import importlib

            import neural_ai
            importlib.reload(neural_ai)

            # Assert
            assert isinstance(neural_ai.__version__, str)
            assert len(neural_ai.__version__) > 0

    def test_version_fallback_when_package_not_found(self) -> None:
        """Teszt: __version__ fallback értéket használ, ha a csomag nincs telepítve."""
        # Arrange
        with patch(
            "neural_ai.metadata.version",
            side_effect=metadata.PackageNotFoundError
        ):
            # Act
            import importlib

            import neural_ai
            importlib.reload(neural_ai)

            # Assert
            assert neural_ai.__version__ == "1.0.0"

    def test_version_is_final_constant(self) -> None:
        """Teszt: __version__ Final típusú konstans."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert hasattr(neural_ai, "__version__")
        # Final típus ellenőrzése az annotations-ben
        annotations = neural_ai.__annotations__
        assert "__version__" in annotations
        assert "Final" in str(annotations["__version__"])


class TestSchemaVersion:
    """Konfigurációs séma verzió tesztelése."""

    def test_schema_version_exists(self) -> None:
        """Teszt: __schema_version__ létezik."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert hasattr(neural_ai, "__schema_version__")

    def test_schema_version_value(self) -> None:
        """Teszt: __schema_version__ értéke '1.0'."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert neural_ai.__schema_version__ == "1.0"

    def test_schema_version_is_final_constant(self) -> None:
        """Teszt: __schema_version__ Final típusú konstans."""
        # Arrange & Act
        import neural_ai

        # Assert
        annotations = neural_ai.__annotations__
        assert "__schema_version__" in annotations
        assert "Final" in str(annotations["__schema_version__"])

    def test_schema_version_is_string(self) -> None:
        """Teszt: __schema_version__ string típusú."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert isinstance(neural_ai.__schema_version__, str)


class TestLoggerInitialization:
    """Logger inicializálás tesztelése."""

    @patch("neural_ai.LoggerFactory.get_logger")
    def test_logger_factory_called_on_import(
        self, mock_get_logger: MagicMock
    ) -> None:
        """Teszt: LoggerFactory.get_logger meghívódik az import során."""
        # Arrange
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Act
        import importlib

        import neural_ai
        importlib.reload(neural_ai)

        # Assert
        mock_get_logger.assert_called_once_with("neural_ai")

    @patch("neural_ai.LoggerFactory.get_logger")
    def test_logger_info_called_with_correct_parameters(
        self, mock_get_logger: MagicMock
    ) -> None:
        """Teszt: logger.info meghívódik a megfelelő paraméterekkel."""
        # Arrange
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Act
        import importlib

        import neural_ai
        importlib.reload(neural_ai)

        # Assert
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args

        # Ellenőrizzük az üzenetet
        assert "Neural-AI-Next modul inicializálva" in call_args[0][0]

        # Ellenőrizzük az extra paramétereket
        assert "extra" in call_args[1]
        extra = call_args[1]["extra"]
        assert "version" in extra
        assert "schema_version" in extra
        assert extra["schema_version"] == "1.0"


class TestPublicAPI:
    """Publikus API exportálás tesztelése."""

    def test_all_exports_version(self) -> None:
        """Teszt: __all__ tartalmazza a __version__-t."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert "__version__" in neural_ai.__all__

    def test_all_exports_schema_version(self) -> None:
        """Teszt: __all__ tartalmazza a __schema_version__-t."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert "__schema_version__" in neural_ai.__all__

    def test_all_is_final_list(self) -> None:
        """Teszt: __all__ Final[list[str]] típusú."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert isinstance(neural_ai.__all__, list)
        assert all(isinstance(item, str) for item in neural_ai.__all__)

        # Final típus ellenőrzése
        annotations = neural_ai.__annotations__
        assert "__all__" in annotations
        assert "Final" in str(annotations["__all__"])

    def test_all_contains_exactly_two_items(self) -> None:
        """Teszt: __all__ pontosan 2 elemet tartalmaz."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert len(neural_ai.__all__) == 2

    def test_exported_items_are_accessible(self) -> None:
        """Teszt: Az exportált elemek elérhetők a modulból."""
        # Arrange & Act
        import neural_ai

        # Assert
        for item in neural_ai.__all__:
            assert hasattr(neural_ai, item)


class TestModuleDocstring:
    """Modul docstring tesztelése."""

    def test_module_has_docstring(self) -> None:
        """Teszt: A modul rendelkezik docstring-gel."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert neural_ai.__doc__ is not None
        assert len(neural_ai.__doc__) > 0

    def test_docstring_contains_version_example(self) -> None:
        """Teszt: A docstring tartalmaz példát a verzió használatára."""
        # Arrange & Act
        import neural_ai

        # Assert
        assert neural_ai.__doc__ is not None and "neural_ai.__version__" in neural_ai.__doc__


class TestImportBehavior:
    """Import viselkedés tesztelése."""

    def test_module_imports_without_error(self) -> None:
        """Teszt: A modul hiba nélkül importálható."""
        # Arrange & Act & Assert
        try:
            import neural_ai
            assert neural_ai is not None
        except Exception as e:
            pytest.fail(f"Import sikertelen: {e}")

    def test_reimport_does_not_raise_error(self) -> None:
        """Teszt: A modul újraimportálása nem okoz hibát."""
        # Arrange & Act & Assert
        try:
            import importlib

            import neural_ai
            importlib.reload(neural_ai)
            assert neural_ai is not None
        except Exception as e:
            pytest.fail(f"Újraimportálás sikertelen: {e}")


class TestTypeAnnotations:
    """Típus annotációk tesztelése."""

    def test_version_has_correct_type_annotation(self) -> None:
        """Teszt: __version__ típus annotációja helyes."""
        # Arrange & Act
        import neural_ai

        # Assert
        annotations = neural_ai.__annotations__
        assert "__version__" in annotations
        assert "str" in str(annotations["__version__"])

    def test_schema_version_has_correct_type_annotation(self) -> None:
        """Teszt: __schema_version__ típus annotációja helyes."""
        # Arrange & Act
        import neural_ai

        # Assert
        annotations = neural_ai.__annotations__
        assert "__schema_version__" in annotations
        assert "str" in str(annotations["__schema_version__"])

    def test_all_has_correct_type_annotation(self) -> None:
        """Teszt: __all__ típus annotációja helyes."""
        # Arrange & Act
        import neural_ai

        # Assert
        annotations = neural_ai.__annotations__
        assert "__all__" in annotations
        assert "list" in str(annotations["__all__"])
