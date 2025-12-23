"""StorageInterface tesztelése.

Ez a modul tartalmazza a StorageInterface interfész tesztjeit,
ellenőrizve az összes absztrakt metódus helyes definícióját és működését.
"""

from collections.abc import Mapping
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pandas as pd
import pytest

from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class TestStorageInterface:
    """StorageInterface interfész tesztosztálya."""

    def test_interface_is_abstract(self) -> None:
        """Teszteli, hogy az interfész valóban absztrakt."""
        with pytest.raises(TypeError):
            StorageInterface()  # type: ignore

    def test_save_dataframe_signature(self) -> None:
        """Teszteli a save_dataframe metódus szignatúráját."""

        # Mock implementáció létrehozása
        class MockStorage(StorageInterface):
            def save_dataframe(
                self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]
            ) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
                return pd.DataFrame()

            def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
                pass

            def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
                return object()

            def exists(self, path: str) -> bool:
                return True

            def get_metadata(self, path: str) -> dict[str, Any]:
                return {}

            def delete(self, path: str) -> None:
                pass

            def list_dir(self, path: str, pattern: str | None = None) -> list[Path]:
                return []

        storage = MockStorage()
        df = pd.DataFrame({"test": [1, 2, 3]})

        # Metódus hívás ellenőrzése
        storage.save_dataframe(df, "test.csv")
        kwargs: dict[str, Any] = {"index": False, "header": True}
        storage.save_dataframe(df, "test.csv", **kwargs)

    def test_load_dataframe_signature(self) -> None:
        """Teszteli a load_dataframe metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)
        mock_storage.load_dataframe.return_value = pd.DataFrame()

        result = mock_storage.load_dataframe("test.csv")
        assert isinstance(result, pd.DataFrame)

    def test_save_object_signature(self) -> None:
        """Teszteli a save_object metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)

        test_object = {"key": "value", "number": 42}
        mock_storage.save_object(test_object, "test.pkl")

        mock_storage.save_object.assert_called_once()

    def test_load_object_signature(self) -> None:
        """Teszteli a load_object metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)
        test_object = {"key": "value"}
        mock_storage.load_object.return_value = test_object

        result = mock_storage.load_object("test.pkl")
        assert result == test_object

    def test_exists_signature(self) -> None:
        """Teszteli az exists metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)
        mock_storage.exists.return_value = True

        result = mock_storage.exists("test.txt")
        assert isinstance(result, bool)

    def test_get_metadata_signature(self) -> None:
        """Teszteli a get_metadata metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)
        mock_storage.get_metadata.return_value = {"size": 1024, "modified": "2025-01-01"}

        result = mock_storage.get_metadata("test.txt")
        assert isinstance(result, dict)

    def test_delete_signature(self) -> None:
        """Teszteli a delete metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)

        mock_storage.delete("test.txt")
        mock_storage.delete.assert_called_once_with("test.txt")

    def test_list_dir_signature(self) -> None:
        """Teszteli a list_dir metódus szignatúráját."""
        mock_storage = Mock(spec=StorageInterface)
        mock_storage.list_dir.return_value = [Path("file1.txt"), Path("file2.txt")]

        result = mock_storage.list_dir("/test")
        assert isinstance(result, list)

        # Pattern paraméter tesztelése
        result_with_pattern = mock_storage.list_dir("/test", pattern="*.txt")
        assert isinstance(result_with_pattern, list)

    def test_all_abstract_methods_defined(self) -> None:
        """Teszteli, hogy minden absztrakt metódus definiálva van."""

        class CompleteStorage(StorageInterface):
            """Teljes implementáció az összes absztrakt metódussal."""

            def save_dataframe(
                self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]
            ) -> None:
                """DataFrame mentése."""
                pass

            def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
                """DataFrame betöltése."""
                return pd.DataFrame()

            def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
                """Objektum mentése."""
                pass

            def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
                """Objektum betöltése."""
                return object()

            def exists(self, path: str) -> bool:
                """Létezés ellenőrzése."""
                return True

            def get_metadata(self, path: str) -> dict[str, Any]:
                """Metaadatok lekérdezése."""
                return {}

            def delete(self, path: str) -> None:
                """Törlés."""
                pass

            def list_dir(self, path: str, pattern: str | None = None) -> list[Path]:
                """Könyvtár listázása."""
                return []

        # Ha nem jön létre kivétel, akkor minden metódus definiálva van
        storage = CompleteStorage()
        assert isinstance(storage, StorageInterface)

    def test_missing_abstract_method_raises_error(self) -> None:
        """Teszteli, hogy hiányzó absztrakt metódus esetén hiba keletkezik."""

        class IncompleteStorage(StorageInterface):
            """Hiányos implementáció."""

            def save_dataframe(
                self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]
            ) -> None:
                pass

            # Hiányzik a load_dataframe és más metódusok

        with pytest.raises(TypeError) as exc_info:
            IncompleteStorage()  # type: ignore

        assert "abstract" in str(exc_info.value).lower()

    def test_type_hints_are_correct(self) -> None:
        """Teszteli a típusannotációk helyességét."""

        class TypedStorage(StorageInterface):
            """Típusosított implementáció."""

            def save_dataframe(
                self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]
            ) -> None:
                assert isinstance(df, pd.DataFrame)
                assert isinstance(path, str)

            def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
                assert isinstance(path, str)
                return pd.DataFrame()

            def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
                assert isinstance(path, str)

            def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
                assert isinstance(path, str)
                return {"test": "object"}

            def exists(self, path: str) -> bool:
                assert isinstance(path, str)
                return True

            def get_metadata(self, path: str) -> dict[str, Any]:
                assert isinstance(path, str)
                return {"size": 100}

            def delete(self, path: str) -> None:
                assert isinstance(path, str)

            def list_dir(self, path: str, pattern: str | None = None) -> list[Path]:
                assert isinstance(path, str)
                if pattern is not None:
                    assert isinstance(pattern, str)
                return []

        storage = TypedStorage()

        # Teszt hívások a típusellenőrzéshez
        df = pd.DataFrame({"col": [1, 2, 3]})
        storage.save_dataframe(df, "test.csv")
        result_df = storage.load_dataframe("test.csv")
        assert isinstance(result_df, pd.DataFrame)

        storage.save_object({"key": "value"}, "test.pkl")
        result_obj = storage.load_object("test.pkl")
        assert isinstance(result_obj, object)

        exists = storage.exists("test.txt")
        assert isinstance(exists, bool)

        metadata = storage.get_metadata("test.txt")
        assert isinstance(metadata, dict)

        storage.delete("test.txt")

        files = storage.list_dir("/test")
        assert isinstance(files, list)

        files_pattern = storage.list_dir("/test", pattern="*.txt")
        assert isinstance(files_pattern, list)
