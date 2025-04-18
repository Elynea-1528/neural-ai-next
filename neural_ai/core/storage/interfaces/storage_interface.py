"""Storage interfész definíció."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd


class StorageInterface(ABC):
    """Adattárolás kezelő interfész."""

    @abstractmethod
    def save_dataframe(
        self,
        df: pd.DataFrame,
        path: Union[str, Path],
        fmt: str = "parquet",
        **kwargs: Any,
    ) -> None:
        """Menti a megadott DataFrame-et."""
        pass

    @abstractmethod
    def load_dataframe(
        self,
        path: Union[str, Path],
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Betölti a megadott DataFrame-et."""
        pass

    @abstractmethod
    def save_object(
        self,
        obj: Any,
        path: Union[str, Path],
        fmt: str = "pickle",
        **kwargs: Any,
    ) -> None:
        """Python objektum mentése."""
        pass

    @abstractmethod
    def load_object(
        self,
        path: Union[str, Path],
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Python objektum betöltése."""
        pass

    @abstractmethod
    def exists(self, path: Union[str, Path]) -> bool:
        """Ellenőrzi, hogy létezik-e a megadott útvonal."""
        pass

    @abstractmethod
    def get_metadata(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Metaadatok lekérése."""
        pass

    @abstractmethod
    def delete(self, path: Union[str, Path]) -> None:
        """Fájl vagy könyvtár törlése."""
        pass

    @abstractmethod
    def list_dir(self, path: Union[str, Path], pattern: Optional[str] = None) -> list[Path]:
        """Könyvtár tartalmának listázása."""
        pass
