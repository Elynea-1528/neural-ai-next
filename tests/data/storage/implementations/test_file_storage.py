"""FileStorage teszt modul.

Ez a modul tartalmazza a FileStorage osztály tesztjeit.
"""

import json
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pandas as pd
import pytest

# from neural_ai.core.base.exceptions import (
#     InsufficientDiskSpaceError,
#     PermissionDeniedError,
#     StorageWriteError,
# )
from neural_ai.data.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.data.storage.implementations.file_storage import FileStorage


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
        return pd.DataFrame(
            {"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "age": [25, 30, 35]}
        )

    @pytest.fixture
    def sample_object(self) -> dict[str, object]:
        """Minta Python objektum létrehozása."""
        return {"key": "value", "number": 42, "nested": {"inner": "data"}}

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
        assert list(loaded.columns) == ["id", "name", "age"]

    def test_save_dataframe_excel(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
        """Teszteli a DataFrame mentését Excel formátumban."""
        # Ellenőrizzük, hogy az openpyxl csomag telepítve van-e
        pytest.importorskip("openpyxl")

        storage.save_dataframe(sample_dataframe, "test.xlsx")

        # Ellenőrizzük, hogy a fájl létrejött
        assert storage.exists("test.xlsx")

        # Betöltjük és ellenőrizzük az adatokat
        loaded = storage.load_dataframe("test.xlsx")
        assert len(loaded) == 3

    def test_save_dataframe_invalid_format(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
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

    def test_save_object_invalid_format(
        self, storage: FileStorage, sample_object: dict[str, object]
    ) -> None:
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

        assert metadata["size"] > 0
        assert metadata["is_file"] is True
        assert metadata["is_dir"] is False
        assert isinstance(metadata["created"], datetime)
        assert isinstance(metadata["modified"], datetime)

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

        assert "total_space_gb" in info
        assert "used_space_gb" in info
        assert "free_space_gb" in info
        assert "free_space_percent" in info
        assert isinstance(info["free_space_percent"], float)

    def test_atomic_write_json(
        self, storage: FileStorage, sample_object: dict[str, object]
    ) -> None:
        """Teszteli az atomi írást JSON formátumban."""
        test_file = storage._get_full_path("atomic_test.json")
        storage._atomic_write(test_file, sample_object, fmt="json")

        # Ellenőrizzük, hogy a fájl létrejött
        assert test_file.exists()

        # Ellenőrizzük a tartalmat
        loaded = json.loads(test_file.read_text())
        assert loaded == sample_object

    def test_atomic_write_dataframe(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
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
        assert "csv" in storage._DATAFRAME_FORMATS
        assert "excel" in storage._DATAFRAME_FORMATS
        assert "json" in storage._OBJECT_FORMATS

        # Ellenőrizzük, hogy a kezelők rendelkeznek save és load metódusokkal
        for fmt in storage._DATAFRAME_FORMATS:
            assert "save" in storage._DATAFRAME_FORMATS[fmt]
            assert "load" in storage._DATAFRAME_FORMATS[fmt]

        for fmt in storage._OBJECT_FORMATS:
            assert "save" in storage._OBJECT_FORMATS[fmt]
            assert "load" in storage._OBJECT_FORMATS[fmt]

    def test_save_dataframe_with_kwargs(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
        """Teszteli a DataFrame mentését **kwargs paraméterekkel."""
        # CSV mentés egyéni elválasztóval
        storage.save_dataframe(sample_dataframe, "test_semicolon.csv", sep=";")

        # Betöltjük és ellenőrizzük, hogy a pontosvesszős formátum működik
        loaded = storage.load_dataframe("test_semicolon.csv", sep=";")
        assert len(loaded) == 3
        assert list(loaded.columns) == ["id", "name", "age"]

    def test_load_dataframe_with_kwargs(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
        """Teszteli a DataFrame betöltését **kwargs paraméterekkel."""
        # Először mentünk egy CSV-t
        storage.save_dataframe(sample_dataframe, "test_kwargs.csv")

        # Betöltjük egyéni paraméterekkel (pl. csak bizonyos oszlopok)
        loaded = storage.load_dataframe("test_kwargs.csv", usecols=["id", "name"])
        assert len(loaded.columns) == 2
        assert "age" not in loaded.columns

    def test_save_object_with_kwargs(
        self, storage: FileStorage, sample_object: dict[str, object]
    ) -> None:
        """Teszteli a Python objektum mentését **kwargs paraméterekkel."""
        # JSON mentés egyéni indentációval
        storage.save_object(sample_object, "test_indent.json", indent=4)

        # Ellenőrizzük, hogy a fájl létrejött és formázott-e
        test_file = storage._get_full_path("test_indent.json")
        content = test_file.read_text()
        assert "    " in content  # 4 spaces indent

    def test_load_object_with_kwargs(
        self, storage: FileStorage, sample_object: dict[str, object]
    ) -> None:
        """Teszteli a Python objektum betöltését **kwargs paraméterekkel."""
        # Először mentünk egy JSON-t
        storage.save_object(sample_object, "test_kwargs.json")

        # Betöltjük (nincs specifikus kwargs a JSON-hoz, de átadhatunk)
        loaded = storage.load_object("test_kwargs.json")
        assert loaded == sample_object

    def test_check_disk_space_sufficient(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a lemezterület ellenőrzését elegendő terület esetén."""
        test_file = temp_dir / "disk_test.txt"
        # Ez nem szabad, hogy hibát dobjon
        storage._check_disk_space(test_file, 1024)

    def test_check_disk_space_insufficient(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a lemezterület ellenőrzését elégtelen terület esetén."""
        test_file = temp_dir / "disk_test.txt"
        # Nagyon nagy méretet kérünk (1 TB), hogy biztosan ne férjen rá
        with pytest.raises(StorageIOError):
            storage._check_disk_space(test_file, 1024 * 1024 * 1024 * 1024)

    def test_check_disk_space_os_error(
        self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a lemezterület ellenőrzését OS hiba esetén."""
        test_file = temp_dir / "disk_test.txt"

        def mock_statvfs(path: Path) -> None:
            raise OSError("Mocked OS error")

        # Monkey patch-eljük az os.statvfs-t
        import os as os_module

        monkeypatch.setattr(os_module, "statvfs", mock_statvfs)

        with pytest.raises(StorageIOError, match="Nem sikerült ellenőrizni a lemezterületet"):
            storage._check_disk_space(test_file, 1024)

    def test_check_permissions_write_denied(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a jogosultság ellenőrzését írási jog nélkül."""
        test_dir = temp_dir / "readonly_dir"
        test_dir.mkdir()
        test_file = test_dir / "test.txt"

        # Állítsuk be csak olvashatóra a könyvtárat
        test_dir.chmod(0o444)

        with pytest.raises(StorageIOError, match="Nincs írási jogosultság"):
            storage._check_permissions(test_file, check_write=True)

        # Visszaállítjuk az eredeti jogosultságot
        test_dir.chmod(0o755)

    def test_check_permissions_read_denied(self, storage: FileStorage, temp_dir: Path) -> None:
        """Teszteli a jogosultság ellenőrzését olvasási jog nélkül."""
        test_file = temp_dir / "no_read.txt"
        test_file.write_text("test")
        test_file.chmod(0o000)  # Semmilyen jogosultság

        with pytest.raises(StorageIOError, match="Nincs olvasási jogosultság"):
            storage._check_permissions(test_file, check_write=False)

        # Visszaállítjuk az eredeti jogosultságot
        test_file.chmod(0o644)

    def test_check_permissions_parent_not_exists(
        self, storage: FileStorage, temp_dir: Path
    ) -> None:
        """Teszteli a jogosultság ellenőrzését nem létező szülőkönyvtár esetén."""
        test_file = temp_dir / "nonexistent_dir" / "test.txt"

        with pytest.raises(StorageIOError, match="A szülő könyvtár nem létezik"):
            storage._check_permissions(test_file, check_write=True)

    def test_get_storage_info_os_error(
        self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a tároló információk lekérdezését OS hiba esetén."""

        def mock_statvfs(path: Path) -> None:
            raise OSError("Mocked OS error")

        # Monkey patch-eljük az os.statvfs-t
        import os as os_module

        monkeypatch.setattr(os_module, "statvfs", mock_statvfs)

        with pytest.raises(StorageIOError, match="Nem sikerült lekérdezni a tárolási információkat"):
            storage.get_storage_info(temp_dir)

    def test_atomic_write_bytes(self, storage: FileStorage) -> None:
        """Teszteli az atomi írást bytes tartalommal (bináris mód)."""
        test_file = storage._get_full_path("atomic_bytes.bin")
        content = b"binary content"

        # Bináris tartalmat közvetlenül írunk a temp fájlba
        temp_path = test_file.with_suffix(test_file.suffix + ".tmp")
        temp_path.write_bytes(content)
        temp_path.replace(test_file)

        assert test_file.exists()
        assert test_file.read_bytes() == content

    def test_atomic_write_string(self, storage: FileStorage) -> None:
        """Teszteli az atomi írást string tartalommal (JSON formátum)."""
        test_file = storage._get_full_path("atomic_string.json")
        content = {"data": "string content"}

        storage._atomic_write(test_file, content, mode="w", fmt="json")

        assert test_file.exists()
        # A JSON mentés során a tartalom JSON formátumban lesz elmentve
        import json

        loaded = json.loads(test_file.read_text())
        assert loaded == content

    def test_atomic_write_invalid_format(self, storage: FileStorage) -> None:
        """Teszteli az atomi írást érvénytelen formátummal."""
        test_file = storage._get_full_path("atomic_invalid.txt")

        with pytest.raises(StorageFormatError, match="Nem támogatott formátum"):
            storage._atomic_write(test_file, "content", fmt="invalid_format")

    def test_atomic_write_os_error_save(
        self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli az atomi írást OS hiba esetén a mentés során."""
        test_file = temp_dir / "atomic_error.txt"

        def mock_open(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked OS error")

        # Monkey patch-eljük az open-t
        import builtins

        monkeypatch.setattr(builtins, "open", mock_open)

        with pytest.raises(StorageIOError, match="Nem sikerült írni az ideiglenes fájlt"):
            storage._atomic_write(test_file, "content", fmt="json")

    def test_save_dataframe_format_detection_failure(self, storage: FileStorage) -> None:
        """Teszteli a DataFrame mentését formátum meghatározási hiba esetén."""
        df = pd.DataFrame({"a": [1, 2, 3]})

        with pytest.raises(StorageFormatError, match="Nem sikerült meghatározni"):
            storage.save_dataframe(df, "test_no_extension")

    def test_save_dataframe_excel_format_detection(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
        """Teszteli a DataFrame mentését Excel formátum automatikus felismerésével."""
        pytest.importorskip("openpyxl")

        # .xlsx kiterjesztésből automatikusan excel formátumot kell felismernie
        storage.save_dataframe(sample_dataframe, "test_auto.xlsx")
        assert storage.exists("test_auto.xlsx")

    def test_save_dataframe_disk_space_check_failure(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a DataFrame mentését lemezterület ellenőrzési hiba esetén."""

        # Mock-oljuk a df.memory_usage-t, hogy nagyon nagy méretet adjon vissza
        # Ez kiváltja a _check_disk_space hívást a save_dataframe-en belül
        def mock_memory_usage(*args: Any, **kwargs: Any) -> Any:
            # Adjunk vissza egy Series-t, ami 1 TB méretet jelent
            return pd.Series(
                [1024 * 1024 * 1024 * 1024] * len(sample_dataframe.columns),
                index=sample_dataframe.columns,
            )

        monkeypatch.setattr(sample_dataframe, "memory_usage", mock_memory_usage)

        # Most a save_dataframe-nek kivételt kell dobnia, mert a lemezterület ellenőrzés
        # észlelni fogja, hogy nincs elég hely
        with pytest.raises(StorageIOError):
            storage.save_dataframe(sample_dataframe, "test.csv")

    def test_save_dataframe_io_error(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a DataFrame mentését IO hiba esetén."""

        def mock_mkdir(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked IO error")

        monkeypatch.setattr(Path, "mkdir", mock_mkdir)

        with pytest.raises(StorageIOError, match="Hiba a DataFrame mentése során"):
            storage.save_dataframe(sample_dataframe, "test.csv")

    def test_load_dataframe_format_detection_failure(self, storage: FileStorage) -> None:
        """Teszteli a DataFrame betöltését formátum meghatározási hiba esetén."""
        test_file = storage._get_full_path("test_no_extension")
        test_file.write_text("dummy")

        with pytest.raises(StorageFormatError, match="Nem sikerült meghatározni"):
            storage.load_dataframe("test_no_extension")

    def test_load_dataframe_excel_format_detection(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame
    ) -> None:
        """Teszteli a DataFrame betöltését Excel formátum automatikus felismerésével."""
        pytest.importorskip("openpyxl")

        storage.save_dataframe(sample_dataframe, "test_auto_load.xlsx")
        loaded = storage.load_dataframe("test_auto_load.xlsx")
        assert len(loaded) == 3

    def test_load_dataframe_io_error(
        self, storage: FileStorage, sample_dataframe: pd.DataFrame, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a DataFrame betöltését IO hiba esetén."""
        storage.save_dataframe(sample_dataframe, "test_io.csv")

        def mock_read_csv(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked IO error")

        monkeypatch.setattr(pd, "read_csv", mock_read_csv)

        with pytest.raises(StorageIOError, match="Hiba a DataFrame betöltése során"):
            storage.load_dataframe("test_io.csv")

    def test_save_object_format_detection_failure(self, storage: FileStorage) -> None:
        """Teszteli az objektum mentését formátum meghatározási hiba esetén."""
        obj = {"key": "value"}

        with pytest.raises(StorageFormatError, match="Nem sikerült meghatározni"):
            storage.save_object(obj, "test_no_extension")

    def test_save_object_serialization_error(
        self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli az objektum mentését szerializációs hiba esetén."""

        # Olyan objektumot hozunk létre, amit nem lehet JSON-ba szerializálni
        class NonSerializable:
            pass

        obj = NonSerializable()

        with pytest.raises(StorageSerializationError, match="nem szerializálható"):
            storage.save_object(obj, "test.json")

    def test_save_object_io_error(
        self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli az objektum mentését IO hiba esetén."""

        def mock_mkdir(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked IO error")

        monkeypatch.setattr(Path, "mkdir", mock_mkdir)

        with pytest.raises(StorageIOError, match="Hiba az objektum mentése során"):
            storage.save_object({"key": "value"}, "test.json")

    def test_load_object_format_detection_failure(self, storage: FileStorage) -> None:
        """Teszteli az objektum betöltését formátum meghatározási hiba esetén."""
        test_file = storage._get_full_path("test_no_extension")
        test_file.write_text("dummy")

        with pytest.raises(StorageFormatError, match="Nem sikerült meghatározni"):
            storage.load_object("test_no_extension")

    def test_load_object_deserialization_error(self, storage: FileStorage) -> None:
        """Teszteli az objektum betöltését deszerializációs hiba esetén."""
        test_file = storage._get_full_path("invalid.json")
        test_file.write_text("{invalid json}")

        with pytest.raises(StorageIOError):
            storage.load_object("invalid.json")

    def test_load_object_os_error(
        self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli az objektum betöltését OS hiba esetén."""
        storage.save_object({"key": "value"}, "test_os.json")

        def mock_open(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked OS error")

        import builtins

        monkeypatch.setattr(builtins, "open", mock_open)

        with pytest.raises(StorageIOError, match="Hiba az objektum betöltése során"):
            storage.load_object("test_os.json")

    def test_get_metadata_os_error(
        self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a metaadatok lekérdezését OS hiba esetén."""
        test_file = temp_dir / "meta_error.txt"
        test_file.write_text("test")

        def mock_stat(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked OS error")

        monkeypatch.setattr(Path, "stat", mock_stat)

        with pytest.raises(StorageIOError, match="Hiba a metaadatok lekérése során"):
            storage.get_metadata("meta_error.txt")

    def test_delete_directory(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár törlését."""
        test_dir = storage._get_full_path("delete_dir")
        test_dir.mkdir(parents=True)

        assert storage.exists("delete_dir")
        storage.delete("delete_dir")
        assert not storage.exists("delete_dir")

    def test_delete_io_error(
        self, storage: FileStorage, temp_dir: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a fájl törlését IO hiba esetén."""
        test_file = temp_dir / "delete_error.txt"
        test_file.write_text("test")

        def mock_unlink(*args: Any, **kwargs: Any) -> None:
            raise OSError("Mocked IO error")

        monkeypatch.setattr(Path, "unlink", mock_unlink)

        with pytest.raises(StorageIOError, match="Hiba a törlés során"):
            storage.delete("delete_error.txt")

    def test_list_dir_not_directory(self, storage: FileStorage) -> None:
        """Teszteli a könyvtár listázását, ha az útvonal nem könyvtár."""
        test_file = storage._get_full_path("not_a_dir.txt")
        test_file.write_text("test")

        with pytest.raises(StorageIOError, match="nem könyvtár"):
            storage.list_dir("not_a_dir.txt")

    def test_list_dir_glob_error(
        self, storage: FileStorage, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Teszteli a könyvtár listázását glob hiba esetén."""
        test_dir = storage._get_full_path("glob_error_dir")
        test_dir.mkdir(parents=True)

        def mock_glob(*args: Any, **kwargs: Any) -> None:
            raise Exception("Mocked glob error")

        monkeypatch.setattr(Path, "glob", mock_glob)

        with pytest.raises(StorageIOError, match="Hiba a könyvtár listázása során"):
            storage.list_dir("glob_error_dir")
