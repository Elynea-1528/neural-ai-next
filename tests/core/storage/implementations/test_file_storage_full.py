"""FileStorage komprehenszív tesztjei - hibakezelés és edge case-ek.

Ez a modul tartalmazza a FileStorage teljes tesztlefedettségét,
beleértve a PermissionError, InsufficientDiskSpaceError és 
StorageFormatError kezelését.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from neural_ai.core.base.exceptions import (
    InsufficientDiskSpaceError,
    PermissionDeniedError,
)
from neural_ai.core.base.exceptions import StorageWriteError
from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageSerializationError,
)
from neural_ai.core.storage.implementations.file_storage import FileStorage


class TestFileStoragePermissionErrors:
    """PermissionError tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_check_permissions_read_denied(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az olvasási jogosultság ellenőrzését."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("test")
        
        # Mockoljuk az os.access-t hogy olvasás tiltva
        with patch("os.access", return_value=False):
            with pytest.raises(PermissionDeniedError, match="No read permission"):
                storage._check_permissions(test_file, check_write=False)

    def test_check_permissions_write_denied(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az írási jogosultság ellenőrzését."""
        test_file = temp_dir / "test.txt"
        
        # Mockoljuk az os.access-t hogy írás tiltva
        with patch("os.access", return_value=False):
            with pytest.raises(PermissionDeniedError, match="No write permission"):
                storage._check_permissions(test_file, check_write=True)

    def test_check_permissions_parent_not_exists(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a szülőkönyvtár nem létezését."""
        test_file = temp_dir / "nonexistent" / "test.txt"
        
        with pytest.raises(PermissionDeniedError, match="does not exist"):
            storage._check_permissions(test_file, check_write=True)

    def test_save_dataframe_permission_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a DataFrame mentését jogosultsági hiba esetén."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        
        # Mockoljuk az os.access-t hogy írás tiltva
        with patch("os.access", return_value=False):
            with pytest.raises(PermissionDeniedError):
                storage.save_dataframe(df, path)

    def test_load_dataframe_permission_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a DataFrame betöltését jogosultsági hiba esetén."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        storage.save_dataframe(df, path)
        
        # Mockoljuk az os.access-t hogy olvasás tiltva
        with patch("os.access", side_effect=lambda p, m: m != os.W_OK):
            with pytest.raises(PermissionDeniedError):
                storage.load_dataframe(path)

    def test_save_object_permission_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az objektum mentését jogosultsági hiba esetén."""
        obj = {"key": "value"}
        path = "test.json"
        
        # Mockoljuk az os.access-t hogy írás tiltva
        with patch("os.access", return_value=False):
            with pytest.raises(PermissionDeniedError):
                storage.save_object(obj, path)

    def test_load_object_permission_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az objektum betöltését jogosultsági hiba esetén."""
        obj = {"key": "value"}
        path = "test.json"
        storage.save_object(obj, path)
        
        # Mockoljuk az os.access-t hogy olvasás tiltva
        with patch("os.access", side_effect=lambda p, m: m != os.W_OK):
            with pytest.raises(PermissionDeniedError):
                storage.load_object(path)


class TestFileStorageDiskSpaceErrors:
    """InsufficientDiskSpaceError tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_check_disk_space_insufficient(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a lemezterület ellenőrzését elégtelen terület esetén."""
        test_file = temp_dir / "test.txt"
        
        # Mockoljuk az os.statvfs-t hogy kevés helyet mutasson
        mock_stat = Mock()
        mock_stat.f_bavail = 100  # Kevesebb mint a szükséges
        mock_stat.f_frsize = 1024
        
        with patch("os.statvfs", return_value=mock_stat):
            with pytest.raises(InsufficientDiskSpaceError, match="Insufficient disk space"):
                storage._check_disk_space(test_file, required_bytes=1024 * 200)

    def test_check_disk_space_os_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a lemezterület ellenőrzését OS hiba esetén."""
        test_file = temp_dir / "test.txt"
        
        # Mockoljuk az os.statvfs-t hogy OSError-t dobjon
        with patch("os.statvfs", side_effect=OSError("Disk error")):
            with pytest.raises(StorageIOError, match="Failed to check disk space"):
                storage._check_disk_space(test_file, required_bytes=1024)

    def test_save_dataframe_insufficient_space(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a DataFrame mentését elégtelen lemezterület esetén."""
        df = pd.DataFrame({"a": list(range(1000))})  # Nagyobb DataFrame
        path = "test.csv"
        
        # Mockoljuk az os.statvfs-t hogy kevés helyet mutasson
        mock_stat = Mock()
        mock_stat.f_bavail = 1
        mock_stat.f_frsize = 1024
        
        with patch("os.statvfs", return_value=mock_stat):
            with pytest.raises(InsufficientDiskSpaceError):
                storage.save_dataframe(df, path)

    def test_save_object_insufficient_space(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az objektum mentését elégtelen lemezterület esetén."""
        obj = {"data": "x" * 10000}  # Nagy objektum
        path = "test.json"
        
        # Mockoljuk az os.statvfs-t hogy kevés helyet mutasson
        mock_stat = Mock()
        mock_stat.f_bavail = 1
        mock_stat.f_frsize = 1024
        
        with patch("os.statvfs", return_value=mock_stat):
            with pytest.raises(InsufficientDiskSpaceError):
                storage.save_object(obj, path)


class TestFileStorageFormatErrors:
    """StorageFormatError tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_save_dataframe_unsupported_format(self, storage: FileStorage):
        """Teszteli a DataFrame mentését nem támogatott formátumban."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.xyz"  # Ismeretlen kiterjesztés
        
        with pytest.raises(StorageFormatError, match="Nem támogatott DataFrame formátum"):
            storage.save_dataframe(df, path)

    def test_save_dataframe_no_extension(self, storage: FileStorage):
        """Teszteli a DataFrame mentését kiterjesztés nélküli fájlba."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test"  # Nincs kiterjesztés
        
        with pytest.raises(StorageFormatError, match="Nem sikerült meghatározni"):
            storage.save_dataframe(df, path)

    def test_load_dataframe_unsupported_format(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a DataFrame betöltését nem támogatott formátumból."""
        path = "test.xyz"  # Ismeretlen kiterjesztés
        (temp_dir / path).write_text("dummy")
        
        with pytest.raises(StorageFormatError, match="Nem támogatott DataFrame formátum"):
            storage.load_dataframe(path)

    def test_save_object_unsupported_format(self, storage: FileStorage):
        """Teszteli az objektum mentését nem támogatott formátumban."""
        obj = {"key": "value"}
        path = "test.xyz"  # Ismeretlen kiterjesztés
        
        with pytest.raises(StorageFormatError, match="Nem támogatott objektum formátum"):
            storage.save_object(obj, path)

    def test_load_object_unsupported_format(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az objektum betöltését nem támogatott formátumból."""
        path = "test.xyz"  # Ismeretlen kiterjesztés
        (temp_dir / path).write_text("dummy")
        
        with pytest.raises(StorageFormatError, match="Nem támogatott objektum formátum"):
            storage.load_object(path)

    def test_atomic_write_unsupported_format(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az atomi írást nem támogatott formátumban."""
        test_file = temp_dir / "test.xyz"
        
        with pytest.raises(StorageFormatError):
            storage._atomic_write(test_file, "content", fmt="xyz")


class TestFileStorageSerializationErrors:
    """StorageSerializationError tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_save_object_non_serializable(self, storage: FileStorage):
        """Teszteli a nem szerializálható objektum mentését."""
        
        class NonSerializable:
            pass
        
        obj = NonSerializable()
        path = "test.json"
        
        with pytest.raises(StorageSerializationError, match="nem szerializálható"):
            storage.save_object(obj, path)

    def test_load_object_invalid_json(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az érvénytelen JSON betöltését."""
        path = "test.json"
        (temp_dir / path).write_text("invalid json content")
        
        with pytest.raises(StorageIOError):
            storage.load_object(path)


class TestFileStorageIOErrors:
    """StorageIOError tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_save_dataframe_io_error(self, storage: FileStorage):
        """Teszteli az IO hibát DataFrame mentésekor."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        
        # Mockoljuk a to_csv-t hogy IOError-t dobjon
        with patch("pandas.DataFrame.to_csv", side_effect=OSError("IO Error")):
            with pytest.raises(StorageIOError, match="Hiba a DataFrame mentése"):
                storage.save_dataframe(df, path)

    def test_load_dataframe_io_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az IO hibát DataFrame betöltésekor."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        storage.save_dataframe(df, path)
        
        # Mockoljuk a read_csv-t hogy IOError-t dobjon
        with patch("pandas.read_csv", side_effect=OSError("IO Error")):
            with pytest.raises(StorageIOError, match="Hiba a DataFrame betöltése"):
                storage.load_dataframe(path)

    def test_get_storage_info_io_error(self, storage: FileStorage):
        """Teszteli a tárhely információk lekérését IO hiba esetén."""
        # Mockoljuk az os.statvfs-t hogy OSError-t dobjon
        with patch("os.statvfs", side_effect=OSError("Disk error")):
            with pytest.raises(StorageIOError, match="Failed to get storage info"):
                storage.get_storage_info(".")

    def test_get_metadata_io_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a metaadatok lekérését IO hiba esetén."""
        path = "test.json"
        storage.save_object({"key": "value"}, path)
        
        # Mockoljuk a stat-ot hogy Exception-t dobjon
        with patch.object(Path, "stat", side_effect=Exception("Stat error")):
            with pytest.raises(StorageIOError, match="Hiba a metaadatok lekérése"):
                storage.get_metadata(path)

    def test_delete_io_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a törlést IO hiba esetén."""
        path = "test.json"
        storage.save_object({"key": "value"}, path)
        
        # Mockoljuk az unlink-et hogy Exception-t dobjon
        with patch.object(Path, "unlink", side_effect=Exception("Delete error")):
            with pytest.raises(StorageIOError, match="Hiba a törlés"):
                storage.delete(path)

    def test_list_dir_io_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a könyvtár listázást IO hiba esetén."""
        storage.save_object({"key": "value"}, "test.json")
        
        # Mockoljuk a glob-ot hogy Exception-t dobjon
        with patch.object(Path, "glob", side_effect=Exception("Glob error")):
            with pytest.raises(StorageIOError, match="Hiba a könyvtár listázása"):
                storage.list_dir(".")


class TestFileStorageEdgeCases:
    """Edge case tesztjei."""

    @pytest.fixture
    def temp_dir(self) -> Path:
        """Átmeneti könyvtár létrehozása."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def storage(self, temp_dir: Path) -> FileStorage:
        """FileStorage példány létrehozása."""
        return FileStorage(base_path=temp_dir)

    def test_atomic_write_temp_file_cleanup(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az atomi írás temp fájl takarítását."""
        test_file = temp_dir / "test.json"
        
        # Mockoljuk a json.dump-t hogy hibát dobjon
        with patch("json.dump", side_effect=OSError("Write error")):
            try:
                storage._atomic_write(test_file, {"key": "value"})
            except StorageWriteError:
                pass
        
        # A temp fájlnak nem szabadna léteznie
        temp_file = temp_dir / "test.json.tmp"
        assert not temp_file.exists()

    def test_atomic_write_replace_error(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az atomi írás replace hibáját."""
        test_file = temp_dir / "test.json"
        temp_file = temp_dir / "test.json.tmp"
        temp_file.write_text("temp content")
        
        # Mockoljuk az os.replace-t hogy hibát dobjon
        with patch("os.replace", side_effect=OSError("Replace error")):
            with pytest.raises(StorageWriteError, match="Failed to replace file"):
                storage._atomic_write(test_file, {"key": "value"})
        
        # A temp fájlnak el kell tűnnie
        assert not temp_file.exists()

    def test_save_dataframe_exception_handling(self, storage: FileStorage):
        """Teszteli a DataFrame mentés kivételkezelését."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        
        # Mockoljuk a mkdir-t hogy Exception-t dobjon
        with patch.object(Path, "mkdir", side_effect=Exception("Mkdir error")):
            with pytest.raises(StorageIOError, match="Hiba a DataFrame mentése"):
                storage.save_dataframe(df, path)

    def test_load_dataframe_exception_handling(self, storage: FileStorage, temp_dir: Path):
        """Teszteli a DataFrame betöltés kivételkezelését."""
        df = pd.DataFrame({"a": [1, 2, 3]})
        path = "test.csv"
        storage.save_dataframe(df, path)
        
        # Mockoljuk a read_csv-t hogy Exception-t dobjon
        with patch("pandas.read_csv", side_effect=Exception("Read error")):
            with pytest.raises(StorageIOError, match="Hiba a DataFrame betöltése"):
                storage.load_dataframe(path)

    def test_save_object_exception_handling(self, storage: FileStorage):
        """Teszteli az objektum mentés kivételkezelését."""
        obj = {"key": "value"}
        path = "test.json"
        
        # Mockoljuk a mkdir-t hogy Exception-t dobjon
        with patch.object(Path, "mkdir", side_effect=Exception("Mkdir error")):
            with pytest.raises(StorageIOError, match="Hiba az objektum mentése"):
                storage.save_object(obj, path)

    def test_load_object_exception_handling(self, storage: FileStorage, temp_dir: Path):
        """Teszteli az objektum betöltés kivételkezelését."""
        obj = {"key": "value"}
        path = "test.json"
        storage.save_object(obj, path)
        
        # Mockoljuk a json.load-t hogy Exception-t dobjon
        with patch("json.load", side_effect=Exception("Load error")):
            with pytest.raises(StorageIOError, match="Hiba az objektum betöltése"):
                storage.load_object(path)