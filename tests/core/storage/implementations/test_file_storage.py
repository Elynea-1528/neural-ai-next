"""FileStorage tesztelése."""

import tempfile
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest

from neural_ai.core.base.exceptions import PermissionDeniedError
from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.core.storage.implementations.file_storage import FileStorage


class TestFileStorage:
    """FileStorage osztály tesztesetei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    @pytest.fixture
    def mock_logger(self) -> Mock:
        """Mock logger létrehozása."""
        return Mock()

    def test_init_with_default_path(self) -> None:
        """Teszteli az alapértelmezett útvonal használatát."""
        storage = FileStorage()
        assert storage._base_path == Path.cwd()

    def test_init_with_custom_path(self, temp_dir: Path) -> None:
        """Teszteli az egyéni útvonal használatát."""
        storage = FileStorage(base_path=temp_dir)
        assert storage._base_path == temp_dir

    def test_init_with_logger(self, temp_dir: Path, mock_logger: Mock) -> None:
        """Teszteli a logger injektálását."""
        storage = FileStorage(base_path=temp_dir, logger=mock_logger)
        assert storage.logger is mock_logger

    def test_save_and_load_dataframe_csv(self, storage: FileStorage) -> None:
        """Teszteli a DataFrame CSV mentését és betöltését."""
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        path = "test.csv"

        storage.save_dataframe(df, path)
        loaded_df = storage.load_dataframe(path)

        pd.testing.assert_frame_equal(df, loaded_df)

    def test_save_dataframe_invalid_format(self, storage: FileStorage) -> None:
        """Teszteli az érvénytelen formátum esetén dobott kivételt."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.invalid"

        with pytest.raises(StorageFormatError):
            storage.save_dataframe(df, path)

    def test_load_nonexistent_dataframe(self, storage: FileStorage) -> None:
        """Teszteli a nem létező fájl betöltésénél dobott kivételt."""
        with pytest.raises(StorageNotFoundError):
            storage.load_dataframe("nonexistent.csv")

    def test_save_and_load_object_json(self, storage: FileStorage) -> None:
        """Teszteli az objektum JSON mentését és betöltését."""
        obj = {"key": "value", "number": 42}
        path = "test.json"

        storage.save_object(obj, path)
        loaded_obj = storage.load_object(path)

        assert loaded_obj == obj

    def test_save_object_invalid_format(self, storage: FileStorage) -> None:
        """Teszteli az érvénytelen objektum formátum esetén dobott kivételt."""
        obj = {"key": "value"}
        path = "test.invalid"

        with pytest.raises(StorageFormatError):
            storage.save_object(obj, path)

    def test_load_nonexistent_object(self, storage: FileStorage) -> None:
        """Teszteli a nem létező objektum betöltésénél dobott kivételt."""
        with pytest.raises(StorageNotFoundError):
            storage.load_object("nonexistent.json")

    def test_exists_true(self, storage: FileStorage) -> None:
        """Teszteli a létező fájl ellenőrzését."""
        path = "test.json"
        storage.save_object("content", path)

        assert storage.exists(path) is True

    def test_exists_false(self, storage: FileStorage) -> None:
        """Teszteli a nem létező fájl ellenőrzését."""
        assert storage.exists("nonexistent.txt") is False

    def test_get_metadata(self, storage: FileStorage) -> None:
        """Teszteli a metaadatok lekérését."""
        path = "test.json"
        storage.save_object("content", path)

        metadata = storage.get_metadata(path)

        assert "size" in metadata
        assert "created" in metadata
        assert "modified" in metadata
        assert metadata["is_file"] is True
        assert metadata["is_dir"] is False

    def test_get_metadata_nonexistent(self, storage: FileStorage) -> None:
        """Teszteli a metaadatok lekérését nem létező fájl esetén."""
        with pytest.raises(StorageNotFoundError):
            storage.get_metadata("nonexistent.txt")

    def test_delete_file(self, storage: FileStorage) -> None:
        """Teszteli a fájl törlését."""
        path = "test.json"
        storage.save_object("content", path)

        storage.delete(path)

        assert storage.exists(path) is False

    def test_delete_nonexistent(self, storage: FileStorage) -> None:
        """Teszteli a nem létező fájl törlésénél dobott kivételt."""
        with pytest.raises(StorageNotFoundError):
            storage.delete("nonexistent.txt")

    def test_list_dir(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását."""
        storage.save_object("content1", "file1.json")
        storage.save_object("content2", "file2.json")

        files = storage.list_dir(".")

        filenames = [f.name for f in files]
        assert "file1.json" in filenames
        assert "file2.json" in filenames

    def test_list_dir_with_pattern(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását mintával."""
        storage.save_object("content1", "file1.json")
        storage.save_dataframe(pd.DataFrame({"a": [1, 2]}), "file2.csv")

        files = storage.list_dir(".", pattern="*.csv")

        filenames = [f.name for f in files]
        assert "file2.csv" in filenames
        assert "file1.json" not in filenames

    def test_list_nonexistent_dir(self, storage: FileStorage) -> None:
        """Teszteli a nem létező könyvtár listázásánál dobott kivételt."""
        with pytest.raises(StorageNotFoundError):
            storage.list_dir("nonexistent")

    def test_get_storage_info(self, storage: FileStorage) -> None:
        """Teszteli a tárhely információk lekérését."""
        info = storage.get_storage_info(".")

        assert "total_space_gb" in info
        assert "used_space_gb" in info
        assert "free_space_gb" in info
        assert "free_space_percent" in info

    def test_check_disk_space_with_logger(self, temp_dir: Path, mock_logger: Mock) -> None:
        """Teszteli a logger használatát hiba esetén."""
        storage = FileStorage(base_path=temp_dir, logger=mock_logger)
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"

        storage.save_dataframe(df, path)

        # A sikeres mentés után a loggernek nem kellene hívva lennie
        # Csak akkor hívódik, ha hiba történik
        assert not mock_logger.exception.called

    def test_serialization_error(self, storage: FileStorage) -> None:
        """Teszteli a szerializálási hibát."""

        # Olyan objektum, ami nem szerializálható JSON-ba
        class NonSerializable:
            pass

        obj = NonSerializable()
        path = "test.json"

        with pytest.raises(StorageSerializationError):
            storage.save_object(obj, path)

    def test_io_error_on_save(self, storage: FileStorage) -> None:
        """Teszteli az IO hibát mentéskor."""
        # Érvénytelen útvonal (gyökérkönyvtár, ami nem létezik)
        storage._base_path = Path("/nonexistent_root_directory_12345")

        # Linuxon a nem létező könyvtárba történő írás PermissionDeniedError-t dob
        # Ez a helyes működés, ezért mindkét kivételt elfogadjuk
        with pytest.raises((StorageIOError, PermissionDeniedError)):
            storage.save_object({"key": "value"}, "test.json")
