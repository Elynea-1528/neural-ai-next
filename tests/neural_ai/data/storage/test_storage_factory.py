"""StorageFactory teszt modul.

Ez a modul tartalmazza a StorageFactory osztály tesztjeit.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from neural_ai.data.storage.exceptions import StorageError
from neural_ai.data.storage.factory import StorageFactory
from neural_ai.data.storage.implementations.file_storage import FileStorage
from neural_ai.data.storage.implementations.parquet_storage import ParquetStorageService
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface


class TestStorageFactory:
    """StorageFactory osztály tesztjei."""

    def setup_method(self) -> None:
        """Teszt metódus előtti beállítás - Singleton cache törlése."""
        from neural_ai.core.base.implementations.singleton import SingletonMeta

        SingletonMeta._instances.clear()  # pyright: ignore[reportPrivateUsage]

    def test_register_storage(self) -> None:
        """Teszteli a storage típus regisztrálását."""

        # Mock storage osztály létrehozása
        class MockStorage(StorageInterface):
            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:  # type: ignore[override]
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def list_dir(self, path: str) -> list[str]:  # type: ignore[override]
                return []

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

        mock_storage_class = MockStorage

        # Regisztráció
        StorageFactory.register_storage("mock", mock_storage_class)

        # Ellenőrzés
        assert "mock" in StorageFactory.get_registered_types()
        assert StorageFactory.get_registered_types()["mock"] is mock_storage_class

    def test_register_storage_invalid_class(self) -> None:
        """Teszteli a nem StorageInterface-t implementáló osztály regisztrálását."""

        # Olyan osztály, ami nem implementálja a StorageInterface-t
        class InvalidClass:
            pass

        # A regisztráció során nem történik ellenőrzés, ezért ez sikeres lesz
        # (a Python dinamikus természete miatt)
        StorageFactory.register_storage("invalid", InvalidClass)  # type: ignore[arg-type]
        assert "invalid" in StorageFactory.get_registered_types()

    def test_get_storage_file_type(self, tmp_path: Path) -> None:
        """Teszteli a file storage létrehozását."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"base_path": str(tmp_path)}
        storage = StorageFactory.get_storage(
            storage_type="file", base_path=str(tmp_path), config=mock_config
        )

        assert isinstance(storage, FileStorage)
        assert storage.base_path == tmp_path

    def test_get_storage_parquet_type(self, tmp_path: Path) -> None:
        """Teszteli a parquet storage létrehozását."""
        mock_config = MagicMock()
        mock_config.get_section.return_value = {"base_path": str(tmp_path)}
        mock_hardware: MagicMock = MagicMock()
        mock_hardware.has_avx2.return_value = True

        storage = StorageFactory.get_storage(
            storage_type="parquet",
            base_path=str(tmp_path),
            hardware=mock_hardware,
            config=mock_config,
        )

        assert isinstance(storage, ParquetStorageService)
        # A has_avx2 metódust többször is meghívhatják a backend kiválasztásakor
        assert mock_hardware.has_avx2.called

    def test_get_storage_with_kwargs(self, tmp_path: Path) -> None:
        """Teszteli a storage létrehozást további paraméterekkel."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"base_path": str(tmp_path)}
        storage = StorageFactory.get_storage(
            storage_type="file", base_path=str(tmp_path), create_if_missing=True, config=mock_config
        )

        assert isinstance(storage, FileStorage)

    def test_get_storage_invalid_config(self, tmp_path: Path) -> None:
        """Teszteli az érvénytelen konfigurációt (pl. tiltott storage típus)."""
        mock_config = MagicMock()
        # JSON storage használata tiltott a központi konfigurációban
        mock_config.get.return_value = {"type": "json", "base_path": str(tmp_path)}

        with pytest.raises(StorageError, match="Érvénytelen storage konfiguráció"):
            StorageFactory.get_storage(
                storage_type="file", base_path=str(tmp_path), config=mock_config
            )

    def test_get_storage_invalid_type(self) -> None:
        """Teszteli a nem létező storage típus lekérését."""
        with pytest.raises(StorageError, match="Ismeretlen storage típus"):
            StorageFactory.get_storage(storage_type="nonexistent")

    def test_get_storage_instantiation_failure(self, tmp_path: Path) -> None:
        """Teszteli a storage példányosítási hibát."""

        # Regisztráljunk egy olyan osztályt, ami hibát dob a konstruktorban
        class FailingStorage(StorageInterface):
            def __init__(self, **kwargs: object) -> None:
                raise TypeError("Test error")

            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:  # type: ignore[override]
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def list_dir(self, path: str) -> list[str]:  # type: ignore[override]
                return []

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

        StorageFactory.register_storage("failing", FailingStorage)

        mock_config = MagicMock()
        with pytest.raises(StorageError, match="Nem sikerült létrehozni a storage példányt"):
            StorageFactory.get_storage(
                storage_type="failing", base_path=str(tmp_path), config=mock_config
            )

    def test_get_storage_unexpected_error(self, tmp_path: Path) -> None:
        """Teszteli a váratlan hibát a storage létrehozásakor."""

        # Regisztráljunk egy olyan osztályt, ami váratlan hibát dob
        class UnexpectedErrorStorage(StorageInterface):
            def __init__(self, **kwargs: object) -> None:
                raise RuntimeError("Unexpected error")

            def save_object(self, obj: object, path: str, **kwargs: object) -> None:
                pass

            def load_object(self, path: str, **kwargs: object) -> object:
                return {}

            def save_dataframe(self, df: object, path: str, **kwargs: object) -> None:
                pass

            def load_dataframe(self, path: str, **kwargs: object) -> object:  # type: ignore[override]
                return {}

            def delete(self, path: str) -> None:
                pass

            def exists(self, path: str) -> bool:
                return True

            def list_dir(self, path: str) -> list[str]:  # type: ignore[override]
                return []

            def get_metadata(self, path: str) -> dict[str, object]:
                return {}

        StorageFactory.register_storage("unexpected", UnexpectedErrorStorage)

        mock_config = MagicMock()
        with pytest.raises(StorageError, match="Váratlan hiba"):
            StorageFactory.get_storage(
                storage_type="unexpected", base_path=str(tmp_path), config=mock_config
            )

    def test_get_storage_default_base_path(self) -> None:
        """Teszteli a storage létrehozást alapértelmezett útvonallal."""
        mock_config = MagicMock()
        mock_config.get.return_value = {}
        storage = StorageFactory.get_storage(storage_type="file", config=mock_config)

        assert isinstance(storage, FileStorage)
        # Alapértelmezett útvonal a FileStorage konstruktorában Path.cwd()

    def test_get_storage_with_hardware_none(self, tmp_path: Path) -> None:
        """Teszteli a storage létrehozást hardware=None paraméterrel."""
        mock_config = MagicMock()
        mock_config.get.return_value = {"base_path": str(tmp_path)}
        storage = StorageFactory.get_storage(
            storage_type="file", base_path=str(tmp_path), hardware=None, config=mock_config
        )

        assert isinstance(storage, FileStorage)
        assert storage.base_path == tmp_path

    def test_initial_storage_types(self) -> None:
        """Teszteli a kezdeti storage típusokat."""
        # Ellenőrizzük, hogy a kezdeti típusok jól lettek-e definiálva
        initial_types = {"file", "parquet"}
        assert initial_types.issubset(set(StorageFactory.get_registered_types().keys()))
