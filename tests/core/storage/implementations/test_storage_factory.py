"""Tesztek a StorageFactory osztályhoz."""

from pathlib import Path

import pytest

from neural_ai.core.storage.exceptions import StorageError
from neural_ai.core.storage.factory import StorageFactory
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class TestStorageFactory:
    """StorageFactory osztály tesztesetei."""

    def setup_method(self) -> None:
        """Teszteset előkészítése."""
        # Tiszta állapot biztosítása minden teszt előtt
        StorageFactory._storage_types = {"file": FileStorage}

    def test_register_storage_success(self) -> None:
        """Sikeres storage regisztráció tesztelése."""

        # Előkészítés
        class MockStorage(StorageInterface):
            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:
                return {}

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

            def list_dir(self, path: str = "") -> list[str]:
                return []

        # Művelet
        StorageFactory.register_storage("mock", MockStorage)

        # Ellenőrzés
        assert "mock" in StorageFactory._storage_types
        assert StorageFactory._storage_types["mock"] is MockStorage

    def test_register_storage_invalid_class(self) -> None:
        """Érvénytelen storage osztály regisztrációjának tesztelése."""

        # Előkészítés
        class NotAStorage:
            pass

        # Művelet és ellenőrzés
        with pytest.raises(ValueError, match="nem implementálja a StorageInterface-t"):
            StorageFactory.register_storage("invalid", NotAStorage)

    def test_get_storage_default_file(self) -> None:
        """Alapértelmezett file storage lekérése."""
        # Művelet
        storage = StorageFactory.get_storage()

        # Ellenőrzés
        assert isinstance(storage, FileStorage)
        assert storage._base_path == Path.cwd()

    def test_get_storage_with_base_path(self, tmp_path: Path) -> None:
        """Storage lekérése egyéni base_path paraméterrel."""
        # Művelet
        storage = StorageFactory.get_storage(base_path=str(tmp_path))

        # Ellenőrzés
        assert isinstance(storage, FileStorage)
        assert storage._base_path == tmp_path

    def test_get_storage_with_kwargs(self, tmp_path: Path) -> None:
        """Storage lekérése további kwargs paraméterekkel."""
        # Művelet
        storage = StorageFactory.get_storage(base_path=str(tmp_path))

        # Ellenőrzés
        assert isinstance(storage, FileStorage)
        assert storage._base_path == tmp_path

    def test_get_storage_invalid_type(self) -> None:
        """Érvénytelen storage típus lekérése."""
        # Művelet és ellenőrzés
        with pytest.raises(StorageError, match="Ismeretlen storage típus"):
            StorageFactory.get_storage("nonexistent")

    def test_get_storage_instantiation_failure(self) -> None:
        """Storage példányosítási hiba tesztelése."""

        # Előkészítés
        class BadStorage(StorageInterface):
            def __init__(self, required_param: str):
                raise TypeError("Missing required parameter")

            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:
                return {}

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

            def list_dir(self, path: str = "") -> list[str]:
                return []

        StorageFactory.register_storage("bad", BadStorage)

        # Művelet és ellenőrzés
        with pytest.raises(StorageError, match="Nem sikerült létrehozni"):
            StorageFactory.get_storage("bad")

    def test_get_storage_unexpected_error(self) -> None:
        """Váratlan hiba tesztelése storage létrehozásakor."""

        # Előkészítés
        class FailingStorage(StorageInterface):
            def __init__(self, **kwargs: object):
                raise RuntimeError("Unexpected error")

            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:
                return {}

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

            def list_dir(self, path: str = "") -> list[str]:
                return []

        StorageFactory.register_storage("failing", FailingStorage)

        # Művelet és ellenőrzés
        with pytest.raises(StorageError, match="Váratlan hiba"):
            StorageFactory.get_storage("failing")

    def test_available_storage_types(self) -> None:
        """Elérhető storage típusok listázása."""
        # Ellenőrzés
        types = list(StorageFactory._storage_types.keys())
        assert "file" in types

    def test_storage_types_isolation(self) -> None:
        """Storage típusok elkülönítésének tesztelése."""
        # Ellenőrzés, hogy a setup_method visszaállítja az eredeti állapotot
        assert "mock" not in StorageFactory._storage_types
        assert StorageFactory._storage_types == {"file": FileStorage}
