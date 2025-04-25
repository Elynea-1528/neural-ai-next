"""FileStorage tesztek."""

# pylint: disable=redefined-outer-name

import os
from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd
import pytest

from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
)
from neural_ai.core.storage.implementations.file_storage import FileStorage


@pytest.fixture
def storage() -> FileStorage:
    """Létrehoz egy FileStorage példányt."""
    return FileStorage()


@pytest.fixture
def test_dir(tmp_path: Path) -> Path:
    """Teszt könyvtár fixture."""
    return tmp_path


def _create_files(test_dir: Path, files: list[str]) -> None:
    """Segédfüggvény tesztfájlok létrehozásához."""
    for file in files:
        (test_dir / file).touch()


def test_save_load_dataframe_csv_with_options(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli DataFrame mentését és betöltését CSV formátumban speciális opciókkal."""
    df = pd.DataFrame({"index": [1, 2, 3], "col": ["a,b", "c;d", "e|f"]})
    path = test_dir / "test.csv"
    storage.save_dataframe(df, str(path), index=True, sep="|")
    loaded_df = storage.load_dataframe(str(path), sep="|", index_col=0)
    pd.testing.assert_frame_equal(df, loaded_df)


def test_save_load_dataframe_with_format_guess(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli DataFrame formátum automatikus felismerését."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    path = test_dir / "test.csv"
    storage.save_dataframe(df, str(path))
    loaded_df = storage.load_dataframe(str(path), fmt=None)  # Automatikus felismerés
    pd.testing.assert_frame_equal(df, loaded_df)


def test_save_load_object_json_with_options(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli JSON mentést és betöltést formázási opciókkal."""
    data = {"list": [1, 2, 3], "nested": {"key": "value"}}
    path = test_dir / "test.json"
    storage.save_object(data, str(path), indent=2)
    loaded_data = storage.load_object(str(path))
    assert data == loaded_data

    # Ellenőrizzük a formázást
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "  " in content  # Van behúzás


def test_load_object_unknown_format(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli ismeretlen formátumú objektum betöltését."""
    path = test_dir / "test.unknown"
    path.touch()
    with pytest.raises(StorageFormatError, match="Nem támogatott objektum formátum: unknown"):
        storage.load_object(str(path))


def test_get_metadata_non_existent_file(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli metaadat lekérését nem létező fájlra."""
    path = test_dir / "nonexistent.txt"
    with pytest.raises(StorageNotFoundError, match="Fájl nem található"):
        storage.get_metadata(str(path))


def test_delete_non_empty_dir_error(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem üres könyvtár törlését."""
    subdir = test_dir / "non_empty_dir"
    subdir.mkdir()
    (subdir / "file.txt").touch()

    with pytest.raises(StorageIOError, match="Directory not empty"):
        storage.delete(str(subdir))


def test_save_load_dataframe_csv(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli DataFrame mentését és betöltését CSV formátumban."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    path = test_dir / "test.csv"
    storage.save_dataframe(df, str(path))
    loaded_df = storage.load_dataframe(str(path))
    pd.testing.assert_frame_equal(df, loaded_df)


@pytest.mark.skip(reason="openpyxl package not installed")
def test_save_load_dataframe_excel(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli DataFrame mentését és betöltését Excel formátumban."""
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    path = test_dir / "test.xlsx"
    storage.save_dataframe(df, str(path), fmt="excel")
    loaded_df = storage.load_dataframe(str(path), fmt="excel")
    pd.testing.assert_frame_equal(df, loaded_df)


def test_save_load_object_json(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli objektum mentését és betöltését JSON formátumban."""
    data = {"key": "value", "number": 42}
    path = test_dir / "test.json"
    storage.save_object(data, str(path))
    loaded_data = storage.load_object(str(path))
    assert data == loaded_data


def test_load_nonexistent_file(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem létező fájl betöltését."""
    path = test_dir / "nonexistent.csv"
    with pytest.raises(StorageNotFoundError, match="Fájl nem található"):
        storage.load_dataframe(str(path))


def test_unsupported_dataframe_format(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem támogatott DataFrame formátum kezelését."""
    df = pd.DataFrame({"a": [1, 2, 3]})
    path = test_dir / "test.xyz"
    with pytest.raises(StorageFormatError, match="Nem támogatott DataFrame formátum"):
        storage.save_dataframe(df, str(path), fmt="xyz")


def test_unsupported_object_format(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem támogatott objektum formátum kezelését."""
    data = {"key": "value"}
    path = test_dir / "test.xyz"
    with pytest.raises(StorageFormatError, match="Nem támogatott objektum formátum"):
        storage.save_object(data, str(path), fmt="xyz")


def test_invalid_json_object(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli érvénytelen JSON objektum kezelését."""
    path = test_dir / "test.json"
    with open(path, "w", encoding="utf-8") as f:
        f.write("invalid json")
    with pytest.raises(StorageIOError, match="Hiba az objektum betöltése során"):
        storage.load_object(str(path))


def test_exists(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli a fájl létezés ellenőrzését."""
    path = test_dir / "test.txt"
    path.touch()
    assert storage.exists(str(path))
    assert not storage.exists(str(test_dir / "nonexistent.txt"))


def test_get_metadata(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli a metaadatok lekérését."""
    path = test_dir / "test.txt"
    content = "test content"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    metadata = storage.get_metadata(str(path))
    assert isinstance(metadata, Dict)
    assert metadata["size"] == len(content)
    assert isinstance(metadata["created"], datetime)
    assert isinstance(metadata["modified"], datetime)
    assert isinstance(metadata["accessed"], datetime)
    assert metadata["is_file"] is True
    assert metadata["is_dir"] is False


def test_get_dir_metadata(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli könyvtár metaadatainak lekérését."""
    subdir = test_dir / "subdir"
    subdir.mkdir()

    metadata = storage.get_metadata(str(subdir))
    assert isinstance(metadata, Dict)
    assert metadata["is_file"] is False
    assert metadata["is_dir"] is True


def test_delete_file(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli fájl törlését."""
    path = test_dir / "test.txt"
    path.touch()
    assert path.exists()
    storage.delete(str(path))
    assert not path.exists()


def test_delete_empty_dir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli üres könyvtár törlését."""
    subdir = test_dir / "empty_dir"
    subdir.mkdir()
    assert subdir.exists()
    storage.delete(str(subdir))
    assert not subdir.exists()


def test_delete_non_empty_dir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem üres könyvtár törlését."""
    subdir = test_dir / "non_empty_dir"
    subdir.mkdir()
    (subdir / "file.txt").touch()

    with pytest.raises(StorageIOError):
        storage.delete(str(subdir))


def test_delete_nonexistent_file(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem létező fájl törlését."""
    path = test_dir / "nonexistent.txt"
    with pytest.raises(StorageNotFoundError, match="Fájl nem található"):
        storage.delete(str(path))


def test_list_dir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli könyvtár tartalmának listázását."""
    files = ["file1.txt", "file2.txt"]
    _create_files(test_dir, files)
    listed_files = storage.list_dir(str(test_dir))
    assert set(f.name for f in listed_files) == set(files)


def test_list_dir_with_pattern(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli könyvtár tartalmának listázását mintával."""
    files = ["test1.txt", "test2.txt", "other.txt"]
    _create_files(test_dir, files)
    listed_files = storage.list_dir(str(test_dir), pattern="test*.txt")
    assert set(f.name for f in listed_files) == {"test1.txt", "test2.txt"}


def test_list_dir_with_subdir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli könyvtár tartalmának listázását alkönyvtárakkal."""
    files = ["file1.txt", "file2.txt"]
    subdir = test_dir / "subdir"
    subdir.mkdir()
    (subdir / "file3.txt").touch()
    _create_files(test_dir, files)
    listed_files = storage.list_dir(str(test_dir))
    assert set(f.name for f in listed_files) == set(files + ["subdir"])


def test_list_nonexistent_dir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli nem létező könyvtár listázását."""
    nonexistent = test_dir / "nonexistent"
    with pytest.raises(StorageNotFoundError):
        storage.list_dir(str(nonexistent))


def test_list_file_as_dir(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli fájl listázását könyvtárként."""
    path = test_dir / "file.txt"
    path.touch()
    with pytest.raises(StorageIOError):
        storage.list_dir(str(path))


@pytest.mark.skip(reason="relative path handling not implemented")
def test_relative_and_absolute_paths(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli relatív és abszolút útvonalak kezelését."""
    rel_path = "test.txt"
    abs_path = str(test_dir / rel_path)
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write("test")
    assert storage.exists(abs_path)
    os.chdir(str(test_dir))
    assert storage.exists(rel_path)


def test_automatic_format_detection(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli a fájlformátum automatikus felismerését."""
    # JSON formátum
    data = {"key": "value"}
    json_path = test_dir / "test.json"
    storage.save_object(data, str(json_path))

    # CSV formátum
    df = pd.DataFrame({"col": [1, 2, 3]})
    csv_path = test_dir / "test.csv"
    storage.save_dataframe(df, str(csv_path))

    assert json_path.exists()
    assert csv_path.exists()


def test_complex_dataframe_types(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli komplex DataFrame típusok kezelését."""
    data = {
        "int": [1, 2, 3],
        "float": [1.1, 2.2, 3.3],
        "str": ["a", "b", "c"],
        "bool": [True, False, True],
        "date": pd.date_range("2020-01-01", periods=3),
    }
    df = pd.DataFrame(data)
    path = test_dir / "complex.csv"
    storage.save_dataframe(df, str(path))
    loaded_df = storage.load_dataframe(str(path), parse_dates=["date"])
    pd.testing.assert_frame_equal(df, loaded_df)


def test_unicode_handling(storage: FileStorage, test_dir: Path) -> None:
    """Teszteli Unicode karakterek kezelését."""
    text_data = {"english": "hello", "hungarian": "áéíóöőúüű", "chinese": "你好", "emoji": "👋🌍"}
    path = test_dir / "unicode.json"
    storage.save_object(text_data, str(path))
    loaded_data = storage.load_object(str(path))
    assert text_data == loaded_data
