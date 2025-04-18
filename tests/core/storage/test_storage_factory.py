"""Storage factory tesztek."""

from pathlib import Path
from typing import Any, Optional

import pytest

from neural_ai.core.storage.exceptions import StorageError
from neural_ai.core.storage.implementations.file_storage import FileStorage
from neural_ai.core.storage.implementations.storage_factory import StorageFactory
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class MockStorage(StorageInterface):
    """Mock storage implementáció teszteléshez."""

    def __init__(self, base_path: Optional[Path] = None, **kwargs: Any) -> None:
        """Mock storage inicializálása."""
        self.base_path = base_path
        self.kwargs = kwargs

    def save_dataframe(self, *args: Any, **kwargs: Any) -> None:
        """Mock implementáció."""
        pass

    def load_dataframe(self, *args: Any, **kwargs: Any) -> Any:
        """Mock implementáció."""
        pass

    def save_object(self, *args: Any, **kwargs: Any) -> None:
        """Mock implementáció."""
        pass

    def load_object(self, *args: Any, **kwargs: Any) -> Any:
        """Mock implementáció."""
        pass

    def exists(self, *args: Any, **kwargs: Any) -> bool:
        """Mock implementáció."""
        return True

    def get_metadata(self, *args: Any, **kwargs: Any) -> Any:
        """Mock implementáció."""
        return {}

    def delete(self, *args: Any, **kwargs: Any) -> None:
        """Mock implementáció."""
        pass

    def list_dir(self, *args: Any, **kwargs: Any) -> list[Path]:
        """Mock implementáció."""
        return []


def test_default_storage_type() -> None:
    """Teszteli az alapértelmezett storage típus (file) működését."""
    storage = StorageFactory.get_storage()
    assert isinstance(storage, FileStorage)


def test_register_and_get_storage() -> None:
    """Teszteli új storage típus regisztrálását és lekérését."""
    StorageFactory.register_storage("mock", MockStorage)
    storage = StorageFactory.get_storage("mock", base_path=Path("test"))

    assert isinstance(storage, MockStorage)
    assert storage.base_path == Path("test")


def test_get_storage_with_kwargs() -> None:
    """Teszteli a storage létrehozását további paraméterekkel."""
    StorageFactory.register_storage("mock", MockStorage)
    storage = StorageFactory.get_storage("mock", base_path=Path("test"), extra_param=True)

    assert isinstance(storage, MockStorage)
    assert storage.base_path == Path("test")
    assert storage.kwargs["extra_param"] is True


def test_get_unknown_storage_type() -> None:
    """Teszteli nem létező storage típus lekérését."""
    with pytest.raises(StorageError) as exc:
        StorageFactory.get_storage("unknown")

    assert "Ismeretlen storage típus" in str(exc.value)
    assert "unknown" in str(exc.value)


@pytest.fixture
def mock_storage_class() -> type[StorageInterface]:
    """Mock storage osztály fixture."""

    class TestStorage(StorageInterface):
        def __init__(self, base_path: Optional[Path] = None, **kwargs: Any) -> None:
            pass

        def save_dataframe(self, *args: Any, **kwargs: Any) -> None:
            pass

        def load_dataframe(self, *args: Any, **kwargs: Any) -> Any:
            pass

        def save_object(self, *args: Any, **kwargs: Any) -> None:
            pass

        def load_object(self, *args: Any, **kwargs: Any) -> Any:
            pass

        def exists(self, *args: Any, **kwargs: Any) -> bool:
            return True

        def get_metadata(self, *args: Any, **kwargs: Any) -> Any:
            return {}

        def delete(self, *args: Any, **kwargs: Any) -> None:
            pass

        def list_dir(self, *args: Any, **kwargs: Any) -> list[Path]:
            return []

    return TestStorage


def test_storage_type_overwrite(mock_storage_class: type[StorageInterface]) -> None:
    """Teszteli storage típus felülírását."""
    StorageFactory.register_storage("file", mock_storage_class)
    storage = StorageFactory.get_storage("file")
    assert isinstance(storage, mock_storage_class)
