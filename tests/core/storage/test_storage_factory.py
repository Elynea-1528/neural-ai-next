"""StorageFactory tesztek."""

from pathlib import Path

import pytest

from neural_ai.core.storage.exceptions import StorageError
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.implementations.storage_factory import StorageFactory
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


def test_default_storage_type() -> None:
    """Ellenőrzi az alapértelmezett storage típust."""
    storage = StorageFactory.get_storage()
    assert isinstance(storage, FileStorage)


def test_get_storage_without_params() -> None:
    """Ellenőrzi a storage lekérését paraméterek nélkül."""
    storage = StorageFactory.get_storage()
    assert isinstance(storage, StorageInterface)


def test_get_storage_with_params(tmp_path: Path) -> None:
    """Ellenőrzi a storage példányosítást paraméterekkel."""
    storage = StorageFactory.get_storage(base_path=str(tmp_path))
    assert isinstance(storage, FileStorage)


def test_get_unknown_storage_type() -> None:
    """Ellenőrzi ismeretlen storage típus kezelését."""
    with pytest.raises(StorageError):
        StorageFactory.get_storage(storage_type="unknown")


def test_storage_instances(tmp_path: Path) -> None:
    """Ellenőrzi, hogy különböző paraméterekkel különböző példányokat kapunk."""
    path1 = tmp_path / "path1"
    path2 = tmp_path / "path2"

    storage1 = StorageFactory.get_storage(base_path=str(path1))
    storage2 = StorageFactory.get_storage(base_path=str(path2))

    assert isinstance(storage1, FileStorage)
    assert isinstance(storage2, FileStorage)
    assert storage1 is not storage2  # Különböző példányok
