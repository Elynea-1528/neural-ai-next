"""Storage interfész tesztelése."""

import inspect
from pathlib import Path
from typing import Any, Dict, Sequence

import pandas as pd

from neural_ai.core.storage.exceptions import StorageError
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class TestStorageInterface:
    """StorageInterface tesztek."""

    def test_is_abstract(self) -> None:
        """Teszteli, hogy az osztály absztrakt-e."""
        assert inspect.isabstract(StorageInterface)

    def test_abstract_methods(self) -> None:
        """Ellenőrzi az absztrakt metódusokat."""
        # Absztrakt metódusok lekérése
        abstract_methods = {
            name
            for name, method in inspect.getmembers(StorageInterface)
            if (
                getattr(method, "__isabstractmethod__", False)
                and isinstance(method, property) is False
            )
        }

        expected_methods = {
            "save_dataframe",
            "load_dataframe",
            "save_object",
            "load_object",
            "exists",
            "get_metadata",
            "delete",
            "list_dir",
        }

        assert abstract_methods == expected_methods

    def test_method_signatures(self) -> None:
        """Ellenőrzi a metódusok szignatúráit."""
        save_df_sig = inspect.signature(StorageInterface.save_dataframe)
        assert list(save_df_sig.parameters.keys()) == ["self", "df", "path", "kwargs"]
        assert save_df_sig.parameters["kwargs"].kind == inspect.Parameter.VAR_KEYWORD
        assert save_df_sig.return_annotation is None

        load_df_sig = inspect.signature(StorageInterface.load_dataframe)
        assert list(load_df_sig.parameters.keys()) == ["self", "path", "kwargs"]
        assert load_df_sig.parameters["kwargs"].kind == inspect.Parameter.VAR_KEYWORD
        assert load_df_sig.return_annotation == pd.DataFrame

        list_dir_sig = inspect.signature(StorageInterface.list_dir)
        assert list(list_dir_sig.parameters.keys()) == ["self", "path", "pattern"]
        assert list_dir_sig.parameters["pattern"].default is None
        assert list_dir_sig.return_annotation == Sequence[Path]

    def test_method_annotations(self) -> None:
        """Ellenőrzi a metódusok típusannotációit."""

        def get_return_annotation(method: Any) -> Any:
            return inspect.signature(method).return_annotation

        assert get_return_annotation(StorageInterface.save_dataframe) is None
        assert get_return_annotation(StorageInterface.load_dataframe) == pd.DataFrame
        assert get_return_annotation(StorageInterface.save_object) is None
        assert get_return_annotation(StorageInterface.load_object) == Any
        assert get_return_annotation(StorageInterface.exists) == bool
        assert get_return_annotation(StorageInterface.get_metadata) == Dict[str, Any]
        assert get_return_annotation(StorageInterface.delete) is None
        assert get_return_annotation(StorageInterface.list_dir) == Sequence[Path]

    def test_storage_error(self) -> None:
        """Ellenőrzi a StorageError kivételt."""
        assert issubclass(StorageError, Exception)
