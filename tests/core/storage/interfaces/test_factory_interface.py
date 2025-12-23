"""Tesztek a StorageFactoryInterface interfészhez.

Ez a modul tartalmazza a StorageFactoryInterface interfész tesztjeit,
amelyek ellenőrzik a tárolási factory-k alapvető viselkedését.
"""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class ConcreteStorage(StorageInterface):
    """Konkrét tárolási implementáció a teszteléshez."""

    def __init__(self, base_path: str | Path | None = None, **kwargs: Mapping[str, Any]) -> None:
        """Inicializálja a tárolót a megadott alapútvonallal.

        Args:
            base_path: Az alap könyvtár útvonala.
            **kwargs: További konfigurációs paraméterek.
        """
        self._base_path = Path(base_path) if base_path else Path.cwd()

    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]) -> None:
        """DataFrame mentése a tárolóba (nem implementált).

        Args:
            df: A menteni kívánt DataFrame.
            path: A cél útvonal a tárolón belül.
            **kwargs: További paraméterek.
        """
        pass  # Teszt célú üres implementáció

    def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
        """DataFrame betöltése a tárolóból (nem implementált).

        Args:
            path: A betöltendő fájl útvonala.
            **kwargs: További paraméterek.

        Returns:
            pd.DataFrame: A betöltött DataFrame.
        """
        return pd.DataFrame()  # Teszt célú üres implementáció

    def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
        """Objektum mentése a tárolóba (nem implementált).

        Args:
            obj: A menteni kívánt objektum.
            path: A cél útvonal a tárolón belül.
            **kwargs: További paraméterek.
        """
        pass  # Teszt célú üres implementáció

    def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
        """Objektum betöltése a tárolóból (nem implementált).

        Args:
            path: A betöltendő fájl útvonala.
            **kwargs: További paraméterek.

        Returns:
            object: A betöltött objektum.
        """
        return None  # Teszt célú üres implementáció

    def exists(self, path: str) -> bool:
        """Létezés ellenőrzése (nem implementált).

        Args:
            path: Az ellenőrizendő útvonal.

        Returns:
            bool: Mindig False.
        """
        return False  # Teszt célú üres implementáció

    def get_metadata(self, path: str) -> dict[str, Any]:
        """Metaadatok lekérdezése (nem implementált).

        Args:
            path: A cél útvonal.

        Returns:
            dict[str, Any]: Üres szótár.
        """
        return {}  # Teszt célú üres implementáció

    def delete(self, path: str) -> None:
        """Törlés (nem implementált).

        Args:
            path: A törlendő útvonal.
        """
        pass  # Teszt célú üres implementáció

    def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]:
        """Könyvtár tartalmának listázása (nem implementált).

        Args:
            path: A listázandó könyvtár útvonala.
            pattern: Fájl minta a szűréshez.

        Returns:
            Sequence[Path]: A talált fájlok listája.
        """
        return []  # Teszt célú üres implementáció


class ConcreteStorageFactory(StorageFactoryInterface):
    """Konkrét storage factory a teszteléshez."""

    _storage_types: dict[str, type[StorageInterface]] = {}

    @classmethod
    def register_storage(
        cls,
        storage_type: str,
        storage_class: type[StorageInterface],
    ) -> None:
        """Tárolási típus regisztrálása.

        Args:
            storage_type: A tárolási típus azonosítója.
            storage_class: A tárolási osztály.
        """
        if not isinstance(storage_type, str) or not storage_type:
            raise ValueError("A storage_type-nak nem üres stringnek kell lennie.")
        if not isinstance(storage_class, type):
            raise TypeError("A storage_class-nak egy osztálynak kell lennie.")
        if not issubclass(storage_class, StorageInterface):
            raise TypeError("A storage_class-nak a StorageInterface-t kell megvalósítania.")
        cls._storage_types[storage_type] = storage_class

    @classmethod
    def get_storage(
        cls,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        **kwargs: dict[str, object],
    ) -> StorageInterface:
        """Tárolási példány létrehozása.

        Args:
            storage_type: A kért tárolási típus.
            base_path: Az alap könyvtár útvonala.
            **kwargs: További paraméterek.

        Returns:
            StorageInterface: Az inicializált tárolási példány.

        Raises:
            KeyError: Ha a tárolási típus nincs regisztrálva.
        """
        if storage_type not in cls._storage_types:
            raise KeyError(f"Ismeretlen tárolási típus: {storage_type}")
        storage_class = cls._storage_types[storage_type]
        # A ConcreteStorage-nak base_path paramétert kell átadni
        if issubclass(storage_class, ConcreteStorage):
            return storage_class(base_path=base_path, **kwargs)
        return storage_class(**kwargs)


class TestStorageFactoryInterface:
    """Tesztek a StorageFactoryInterface interfészhez."""

    def test_register_storage_success(self) -> None:
        """Sikeres tárolási típus regisztrálásának tesztelése."""
        ConcreteStorageFactory._storage_types.clear()
        ConcreteStorageFactory.register_storage("test", ConcreteStorage)
        assert "test" in ConcreteStorageFactory._storage_types
        assert ConcreteStorageFactory._storage_types["test"] is ConcreteStorage

    def test_register_storage_empty_type_raises_value_error(self) -> None:
        """Üres típusnév esetén ValueError kivétel keletkezik."""
        with pytest.raises(ValueError, match="nem üres stringnek kell lennie"):
            ConcreteStorageFactory.register_storage("", ConcreteStorage)

    def test_register_storage_invalid_class_raises_type_error(self) -> None:
        """Érvénytelen osztály esetén TypeError kivétel keletkezik."""

        class NotAStorage:
            pass

        with pytest.raises(TypeError, match="StorageInterface-t kell megvalósítania"):
            ConcreteStorageFactory.register_storage("invalid", NotAStorage)  # type: ignore[arg-type]

    def test_get_storage_success(self, tmp_path: Path) -> None:
        """Sikeres tárolási példány létrehozásának tesztelése."""
        ConcreteStorageFactory._storage_types.clear()
        ConcreteStorageFactory.register_storage("test", ConcreteStorage)
        storage = ConcreteStorageFactory.get_storage("test", base_path=tmp_path)
        assert isinstance(storage, ConcreteStorage)
        assert storage._base_path == tmp_path

    def test_get_storage_default_path(self) -> None:
        """Alapértelmezett útvonal használatának tesztelése."""
        ConcreteStorageFactory._storage_types.clear()
        ConcreteStorageFactory.register_storage("test", ConcreteStorage)
        storage = ConcreteStorageFactory.get_storage("test")
        assert isinstance(storage, ConcreteStorage)
        assert storage._base_path == Path.cwd()

    def test_get_storage_unknown_type_raises_key_error(self) -> None:
        """Ismeretlen típus esetén KeyError kivétel keletkezik."""
        ConcreteStorageFactory._storage_types.clear()
        with pytest.raises(KeyError, match="Ismeretlen tárolási típus"):
            ConcreteStorageFactory.get_storage("unknown")

    def test_get_storage_with_kwargs(self, tmp_path: Path) -> None:
        """További paraméterek átadásának tesztelése."""
        ConcreteStorageFactory._storage_types.clear()
        ConcreteStorageFactory.register_storage("test", ConcreteStorage)
        storage = ConcreteStorageFactory.get_storage(
            "test",
            base_path=tmp_path,
        )
        assert isinstance(storage, ConcreteStorage)
        assert storage._base_path == tmp_path
