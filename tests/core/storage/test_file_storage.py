"""FileStorage tesztek."""

from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.core.storage.implementations.file_storage import FileStorage


@pytest.fixture
def test_storage(tmp_path: Path) -> FileStorage:
    """Létrehoz egy FileStorage példányt."""
    return FileStorage(base_path=tmp_path)


@pytest.fixture
def test_df() -> pd.DataFrame:
    """Létrehoz egy minta DataFrame-et."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
            "city": ["New York", "London", "Paris"],
        }
    )


@pytest.fixture
def test_obj() -> dict[str, Any]:
    """Létrehoz egy minta objektumot."""
    return {
        "string": "test",
        "number": 42,
        "list": [1, 2, 3],
        "nested": {"key": "value"},
    }


def test_save_load_dataframe_csv(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a DataFrame mentését és betöltését CSV formátumban."""
    path = "data.csv"
    test_storage.save_dataframe(test_df, path, fmt="csv", index=False)
    loaded_df = test_storage.load_dataframe(path, fmt="csv")
    pd.testing.assert_frame_equal(test_df, loaded_df)


def test_save_load_object_json(test_storage: FileStorage, test_obj: dict[str, Any]) -> None:
    """Teszteli az objektum mentését és betöltését JSON formátumban."""
    path = "data.json"
    test_storage.save_object(test_obj, path, fmt="json")
    loaded_obj = test_storage.load_object(path, fmt="json")
    assert loaded_obj == test_obj


def test_load_nonexistent_file(test_storage: FileStorage) -> None:
    """Teszteli a nem létező fájl betöltését."""
    with pytest.raises(StorageNotFoundError):
        test_storage.load_dataframe("nonexistent.csv")


def test_unsupported_dataframe_format(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a nem támogatott DataFrame formátum kezelését."""
    with pytest.raises(StorageFormatError):
        test_storage.save_dataframe(test_df, "data.xyz", fmt="xyz")


def test_unsupported_object_format(test_storage: FileStorage, test_obj: dict[str, Any]) -> None:
    """Teszteli a nem támogatott objektum formátum kezelését."""
    with pytest.raises(StorageFormatError):
        test_storage.save_object(test_obj, "data.xyz", fmt="xyz")


def test_invalid_json_object(test_storage: FileStorage) -> None:
    """Teszteli a nem JSON szerializálható objektum kezelését."""
    obj = {"func": lambda x: x}  # Függvények nem JSON szerializálhatók
    with pytest.raises(StorageSerializationError):
        test_storage.save_object(obj, "data.json", fmt="json")


def test_exists(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a fájl létezésének ellenőrzését."""
    path = "data.csv"
    assert not test_storage.exists(path)
    test_storage.save_dataframe(test_df, path, fmt="csv")
    assert test_storage.exists(path)


def test_get_metadata(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a metaadatok lekérését."""
    path = "data.csv"
    test_storage.save_dataframe(test_df, path, fmt="csv")
    metadata = test_storage.get_metadata(path)

    assert isinstance(metadata, dict)
    assert metadata["size"] > 0
    assert metadata["is_file"] is True
    assert metadata["is_dir"] is False


def test_delete_file(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a fájl törlését."""
    path = "data.csv"
    test_storage.save_dataframe(test_df, path, fmt="csv")
    assert test_storage.exists(path)
    test_storage.delete(path)
    assert not test_storage.exists(path)


def test_delete_nonexistent_file(test_storage: FileStorage) -> None:
    """Teszteli a nem létező fájl törlését."""
    with pytest.raises(StorageNotFoundError):
        test_storage.delete("nonexistent.csv")


def test_list_dir(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a könyvtár tartalmának listázását."""
    # Hozzunk létre néhány fájlt
    test_storage.save_dataframe(test_df, "data1.csv", fmt="csv")
    test_storage.save_dataframe(test_df, "data2.csv", fmt="csv")
    test_storage.save_dataframe(test_df, "other.txt", fmt="csv")

    # Listázás pattern nélkül
    files = test_storage.list_dir(".")
    assert len(files) == 3

    # Listázás pattern-nel
    csv_files = test_storage.list_dir(".", "*.csv")
    assert len(csv_files) == 2
    assert all(f.suffix == ".csv" for f in csv_files)


def test_list_dir_with_subdir(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli az alkönyvtárak listázását."""
    # Hozzunk létre alkönyvtár struktúrát
    test_storage.save_dataframe(test_df, "dir1/data1.csv", fmt="csv")
    test_storage.save_dataframe(test_df, "dir1/data2.csv", fmt="csv")
    test_storage.save_dataframe(test_df, "dir2/data3.csv", fmt="csv")

    # Listázzuk az alkönyvtárakat
    root_items = test_storage.list_dir(".")
    assert len(root_items) == 2
    assert all(p.is_dir() for p in root_items)

    # Listázzuk az egyik alkönyvtár tartalmát
    dir1_items = test_storage.list_dir("dir1")
    assert len(dir1_items) == 2
    assert all(p.is_file() for p in dir1_items)


def test_relative_and_absolute_paths(tmp_path: Path) -> None:
    """Teszteli a relatív és abszolút útvonalak kezelését."""
    storage = FileStorage(tmp_path)
    df = pd.DataFrame({"a": [1, 2, 3]})

    # Relatív útvonal
    storage.save_dataframe(df, "relative/path/data.csv", fmt="csv")
    assert (tmp_path / "relative/path/data.csv").exists()

    # Abszolút útvonal
    abs_path = tmp_path / "absolute/path/data.csv"
    storage.save_dataframe(df, abs_path, fmt="csv")
    assert abs_path.exists()


def test_automatic_format_detection(test_storage: FileStorage, test_df: pd.DataFrame) -> None:
    """Teszteli a formátum automatikus felismerését kiterjesztés alapján."""
    # Mentsük el a DataFrame-et explicit formátum megadással
    test_storage.save_dataframe(test_df, "data.csv", fmt="csv")

    # Töltsük be formátum megadása nélkül
    loaded_df = test_storage.load_dataframe("data.csv")
    pd.testing.assert_frame_equal(test_df, loaded_df)
