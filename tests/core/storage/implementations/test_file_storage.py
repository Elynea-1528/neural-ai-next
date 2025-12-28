"""FileStorage teszt modul.

Ez a modul tartalmazza a FileStorage osztály tesztjeit.
"""

import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from neural_ai.core.base.exceptions import (
    PermissionDeniedError,
)
from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
)
from neural_ai.core.storage.implementations.file_storage import FileStorage


class TestFileStorage:
    """FileStorage osztály tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Ideiglenes könyvtár létrehozása a tesztekhez."""
        tmpdir = tempfile.mkdtemp()
        yield Path(tmpdir)
        shutil.rmtree(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=str(temp_dir))

    @pytest.fixture
    def sample_dataframe(self) -> pd.DataFrame:
        """Minta DataFrame létrehozása."""
        return pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })

    @pytest.fixture
    def sample_object(self) -> dict[str, object]:
        """Minta Python objektum létrehozása."""
        return {
            'key': 'value',
            'number': 42,
            'nested': {'inner': 'data'}
        }

    def test_init_default_path(self) -> None:
        """Teszteli az alapértelmezett útvonal beállítását."""
        storage = FileStorage()
        assert storage._base_path == Path.cwd()

    def test_init_custom_path(self, temp_dir: Path) -> None:
        """Teszteli az egyéni útvonal beállítását."""
        storage = FileStorage(base_path=str(temp_dir))
        assert storage._base_path == temp_dir

    def test_init_with_logger(self, temp_dir: Path) -> None:
        """Teszteli a logger beállítását."""
        mock_logger: MagicMock = MagicMock()
        storage = FileStorage(base_path=str(temp_dir), logger=mock_logger)
        assert storage.logger is mock_logger

    def test_get_full_path_absolute(self, storage: FileStorage) -> None:
        """Teszteli az abszolút útvonal kezelését."""
        abs_path = Path("/absolute/path/file.txt")
        result = storage._get_full_path(abs_path)
        assert result == abs_path

    def test_get_full_path_relative(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a relatív útvonal kezelését."""
        rel_path = "relative/file.txt"
        result = storage._get_full_path(rel_path)
        assert result == temp_dir / rel_path

    def test_exists_true(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a létező fájl ellenőrzését."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        assert storage.exists("test.txt") is True

    def test_exists_false(self, storage: FileStorage) -> None:
        """Teszteli a nem létező fájl ellenőrzését."""
        assert storage.exists("nonexistent.txt") is False

    def test_save_dataframe_csv(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None:
        """Teszteli a DataFrame mentését CSV formátumban."""
        storage.save_dataframe(sample_dataframe, "test.csv")

        # Ellenőrizzük, hogy a fájl létrejött
        assert storage.exists("test.csv")

        # Betöltjük és ellenőrizzük az adatokat
        loaded = storage.load_dataframe("test.csv")
        assert len(loaded) == 3
        assert list(loaded.columns) == ['id', 'name', 'age']

    def test_save_dataframe_excel(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None:
        """Teszteli a DataFrame mentését Excel formátumban."""
        # Ellenőrizzük, hogy az openpyxl csomag telepítve van-e
        pytest.importorskip("openpyxl")

        storage.save_dataframe(sample_dataframe, "test.xlsx")

        # Ellenőrizzük, hogy a fájl létrejött
        assert storage.exists("test.xlsx")

        # Betöltjük és ellenőrizzük az adatokat
        loaded = storage.load_dataframe("test.xlsx")
        assert len(loaded) == 3

    def test_save_dataframe_invalid_format(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None:
        """Teszteli a DataFrame mentését érvénytelen formátumban."""
        with pytest.raises(StorageFormatError, match="Nem támogatott DataFrame formátum"):
            storage.save_dataframe(sample_dataframe, "test.invalid")

    def test_load_dataframe_not_found(self, storage: FileStorage) -> None:
        """Teszteli a DataFrame betöltését nem létező fájlból."""
        with pytest.raises(StorageNotFoundError, match="Fájl nem található"):
            storage.load_dataframe("nonexistent.csv")

    def test_save_object_json(self, storage: FileStorage, sample_object: dict[str, object]) -> None:
        """Teszteli a Python objektum mentését JSON formátumban."""
        storage.save_object(sample_object, "test.json")

        # Ellenőrizzük, hogy a fájl létrejött
        assert storage.exists("test.json")

        # Betöltjük és ellenőrizzük az adatokat
        loaded = storage.load_object("test.json")
        assert loaded == sample_object

    def test_save_object_invalid_format(self, storage: FileStorage, sample_object: dict[str, object]) -> None:
        """Teszteli a Python objektum mentését érvénytelen formátumban."""
        with pytest.raises(StorageFormatError, match="Nem támogatott objektum formátum"):
            storage.save_object(sample_object, "test.invalid")

    def test_load_object_not_found(self, storage: FileStorage) -> None:
        """Teszteli a Python objektum betöltését nem létező fájlból."""
        with pytest.raises(StorageNotFoundError, match="Fájl nem található"):
            storage.load_object("nonexistent.json")

    def test_load_object_invalid_json(self, storage: FileStorage) -> None:
        """Teszteli a Python objektum betöltését érvénytelen JSON fájlból."""
        # Hozzunk létre egy érvénytelen JSON fájlt
        invalid_json_path = storage._get_full_path("invalid.json")
        invalid_json_path.write_text("{invalid json}")

        with pytest.raises(StorageIOError):
            storage.load_object("invalid.json")

    def test_get_metadata_file(self, storage: FileStorage) -> None:
        """Teszteli a fájl metaadatok lekérdezését."""
        test_file = storage._get_full_path("meta_test.txt")
        test_file.write_text("test content")

        metadata = storage.get_metadata("meta_test.txt")

        assert metadata['size'] > 0
        assert metadata['is_file'] is True
        assert metadata['is_dir'] is False
        assert isinstance(metadata['created'], datetime)
        assert isinstance(metadata['modified'], datetime)

    def test_get_metadata_not_found(self, storage: FileStorage) -> None:
        """Teszteli a metaadatok lekérdezését nem létező fájlból."""
        with pytest.raises(StorageNotFoundError):
            storage.get_metadata("nonexistent.txt")

    def test_delete_file(self, storage: FileStorage) -> None:
        """Teszteli a fájl törlését."""
        test_file = storage._get_full_path("delete_test.txt")
        test_file.write_text("test")

        assert storage.exists("delete_test.txt")
        storage.delete("delete_test.txt")
        assert not storage.exists("delete_test.txt")

    def test_delete_not_found(self, storage: FileStorage) -> None:
        """Teszteli a nem létező fájl törlését."""
        with pytest.raises(StorageNotFoundError):
            storage.delete("nonexistent.txt")

    def test_list_dir(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását."""
        # Hozzunk létre néhány tesztfájlt
        (storage._get_full_path("dir1") / "file1.txt").parent.mkdir(parents=True, exist_ok=True)
        storage._get_full_path("dir1/file1.txt").write_text("test1")
        storage._get_full_path("dir1/file2.txt").write_text("test2")

        files = storage.list_dir("dir1")
        assert len(files) == 2
        filenames = [f.name for f in files]
        assert "file1.txt" in filenames
        assert "file2.txt" in filenames

    def test_list_dir_with_pattern(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását mintával."""
        # Hozzunk létre néhány tesztfájlt
        (storage._get_full_path("dir2") / "file1.txt").parent.mkdir(parents=True, exist_ok=True)
        storage._get_full_path("dir2/file1.txt").write_text("test1")
        storage._get_full_path("dir2/file2.csv").write_text("test2")

        txt_files = storage.list_dir("dir2", pattern="*.txt")
        assert len(txt_files) == 1
        assert txt_files[0].name == "file1.txt"

    def test_list_dir_not_found(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását nem létező könyvtárból."""
        with pytest.raises(StorageNotFoundError):
            storage.list_dir("nonexistent_dir")

    def test_check_permissions_read_only(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli az olvasási jogosultság ellenőrzését."""
        test_file = temp_dir / "readonly.txt"
        test_file.write_text("test")
        test_file.chmod(0o444)

        # Ez nem szabad, hogy hibát dobjon, csak írási jogosultság ellenőrzésénél
        try:
            storage._check_permissions(test_file, check_write=False)
        except PermissionDeniedError:
            pytest.fail("Unexpected PermissionDeniedError")

    def test_get_storage_info(self, storage: FileStorage) -> None:
        """Teszteli a tároló információk lekérdezését."""
        info = storage.get_storage_info(storage._base_path)

        assert 'total_space_gb' in info
        assert 'used_space_gb' in info
        assert 'free_space_gb' in info
        assert 'free_space_percent' in info
        assert isinstance(info['free_space_percent'], float)

    def test_atomic_write_json(self, storage: FileStorage, sample_object: dict[str, object]) -> None:
        """Teszteli az atomi írást JSON formátumban."""
        test_file = storage._get_full_path("atomic_test.json")
        storage._atomic_write(test_file, sample_object, fmt="json")

        # Ellenőrizzük, hogy a fájl létrejött
        assert test_file.exists()

        # Ellenőrizzük a tartalmat
        loaded = json.loads(test_file.read_text())
        assert loaded == sample_object

    def test_atomic_write_dataframe(self, storage: FileStorage, sample_dataframe: pd.DataFrame) -> None:
        """Teszteli az atomi írást DataFrame-mel."""
        test_file = storage._get_full_path("atomic_df.csv")
        storage._atomic_write(test_file, sample_dataframe, fmt="csv")

        # Ellenőrizzük, hogy a fájl létrejött
        assert test_file.exists()

        # Betöltjük és ellenőrizzük
        loaded = pd.read_csv(test_file)
        assert len(loaded) == 3

    def test_setup_format_handlers(self, storage: FileStorage) -> None:
        """Teszteli a formátum kezelők beállítását."""
        assert 'csv' in storage._DATAFRAME_FORMATS
        assert 'excel' in storage._DATAFRAME_FORMATS
        assert 'json' in storage._OBJECT_FORMATS

        # Ellenőrizzük, hogy a kezelők rendelkeznek save és load metódusokkal
        for fmt in storage._DATAFRAME_FORMATS:
            assert 'save' in storage._DATAFRAME_FORMATS[fmt]
            assert 'load' in storage._DATAFRAME_FORMATS[fmt]

        for fmt in storage._OBJECT_FORMATS:
            assert 'save' in storage._OBJECT_FORMATS[fmt]
            assert 'load' in storage._OBJECT_FORMATS[fmt]
