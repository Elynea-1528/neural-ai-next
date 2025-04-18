"""Fájl alapú storage implementáció."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd

from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface


class FileStorage(StorageInterface):
    """Fájl alapú storage implementáció.

    A komponens fájlrendszer alapú tárolást biztosít DataFrame-ek és Python
    objektumok számára különböző formátumokban.

    Args:
        base_path: Alap könyvtár útvonal (None esetén az aktuális könyvtár)
        **kwargs: További paraméterek (jövőbeli használatra)
    """

    _DATAFRAME_FORMATS = {
        "csv": ("read_csv", "to_csv"),
        "json": ("read_json", "to_json"),
        "excel": ("read_excel", "to_excel"),
    }

    _OBJECT_FORMATS = {"json"}

    def __init__(self, base_path: Optional[Union[str, Path]] = None, **kwargs: Any) -> None:
        """Storage inicializálása."""
        self._base_path = Path(base_path) if base_path else Path.cwd()

    def _get_full_path(self, path: Union[str, Path]) -> Path:
        """Teljes útvonal előállítása.

        Args:
            path: Relatív vagy abszolút útvonal

        Returns:
            Path: Teljes útvonal
        """
        path = Path(path)
        return path if path.is_absolute() else self._base_path / path

    def save_dataframe(
        self,
        df: pd.DataFrame,
        path: Union[str, Path],
        fmt: str = "csv",
        **kwargs: Any,
    ) -> None:
        """Menti a megadott DataFrame-et.

        Args:
            df: Mentendő DataFrame
            path: Mentési útvonal
            fmt: Fájl formátum (csv, json, excel)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageIOError: Ha a mentés sikertelen
        """
        if fmt not in self._DATAFRAME_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott DataFrame formátum: {fmt}. "
                f"Támogatott formátumok: {list(self._DATAFRAME_FORMATS.keys())}"
            )

        try:
            full_path = self._get_full_path(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)

            _, save_method = self._DATAFRAME_FORMATS[fmt]
            save_func = getattr(df, save_method)

            # CSV esetén mindig mentjük az indexet is
            if fmt == "csv" and "index" not in kwargs:
                kwargs["index"] = False

            save_func(full_path, **kwargs)

        except Exception as e:
            raise StorageIOError(f"Hiba a DataFrame mentése során: {str(e)}", e) from e

    def load_dataframe(
        self,
        path: Union[str, Path],
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Betölti a megadott DataFrame-et.

        Args:
            path: Betöltési útvonal
            fmt: Fájl formátum (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            pd.DataFrame: A betöltött DataFrame

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageIOError: Ha a betöltés sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Ha nincs megadva formátum, próbáljuk kitalálni a kiterjesztésből
        if fmt is None:
            fmt = full_path.suffix.lower().lstrip(".")
            if not fmt:
                raise StorageFormatError("Nem sikerült meghatározni a fájl formátumát")

        if fmt not in self._DATAFRAME_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott DataFrame formátum: {fmt}. "
                f"Támogatott formátumok: {list(self._DATAFRAME_FORMATS.keys())}"
            )

        try:
            load_method, _ = self._DATAFRAME_FORMATS[fmt]
            load_func = getattr(pd, load_method)

            # CSV esetén mindig kezeljük az indexet
            if fmt == "csv" and "index_col" not in kwargs:
                kwargs["index_col"] = False

            return load_func(full_path, **kwargs)

        except Exception as e:
            raise StorageIOError(f"Hiba a DataFrame betöltése során: {str(e)}", e) from e

    def save_object(
        self,
        obj: Any,
        path: Union[str, Path],
        fmt: str = "json",
        **kwargs: Any,
    ) -> None:
        """Python objektum mentése.

        Args:
            obj: Mentendő objektum
            path: Mentési útvonal
            fmt: Fájl formátum (jelenleg csak json támogatott)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem szerializálható
            StorageIOError: Ha a mentés sikertelen
        """
        if fmt not in self._OBJECT_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott objektum formátum: {fmt}. "
                f"Támogatott formátumok: {self._OBJECT_FORMATS}"
            )

        try:
            full_path = self._get_full_path(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)

            if fmt == "json":
                with open(full_path, "w", encoding="utf-8") as f:
                    json.dump(obj, f, **kwargs)

        except (TypeError, ValueError) as e:
            raise StorageSerializationError(f"Az objektum nem szerializálható: {str(e)}", e) from e
        except Exception as e:
            raise StorageIOError(f"Hiba az objektum mentése során: {str(e)}", e) from e

    def load_object(
        self,
        path: Union[str, Path],
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Python objektum betöltése.

        Args:
            path: Betöltési útvonal
            fmt: Fájl formátum (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            Any: A betöltött objektum

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem deszerializálható
            StorageIOError: Ha a betöltés sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Ha nincs megadva formátum, próbáljuk kitalálni a kiterjesztésből
        if fmt is None:
            fmt = full_path.suffix.lower().lstrip(".")
            if not fmt:
                raise StorageFormatError("Nem sikerült meghatározni a fájl formátumát")

        if fmt not in self._OBJECT_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott objektum formátum: {fmt}. "
                f"Támogatott formátumok: {self._OBJECT_FORMATS}"
            )

        try:
            if fmt == "json":
                with open(full_path, "r", encoding="utf-8") as f:
                    return json.load(f, **kwargs)

            raise StorageFormatError(f"Ismeretlen formátum: {fmt}")

        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}", e) from e

    def exists(self, path: Union[str, Path]) -> bool:
        """Ellenőrzi, hogy létezik-e a megadott útvonal.

        Args:
            path: Ellenőrizendő útvonal

        Returns:
            bool: True ha létezik, False ha nem
        """
        return self._get_full_path(path).exists()

    def get_metadata(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Metaadatok lekérése.

        Args:
            path: Fájl útvonala

        Returns:
            Dict[str, Any]: Metaadatok (méret, módosítási idő, stb.)

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a metaadatok nem elérhetőek
        """
        try:
            full_path = self._get_full_path(path)
            if not full_path.exists():
                raise StorageNotFoundError(f"Fájl nem található: {full_path}")

            stat = os.stat(full_path)
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "is_file": full_path.is_file(),
                "is_dir": full_path.is_dir(),
            }

        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a metaadatok lekérése során: {str(e)}", e) from e

    def delete(self, path: Union[str, Path]) -> None:
        """Fájl vagy könyvtár törlése.

        Args:
            path: Törlendő útvonal

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a törlés sikertelen
        """
        try:
            full_path = self._get_full_path(path)
            if not full_path.exists():
                raise StorageNotFoundError(f"Fájl nem található: {full_path}")

            if full_path.is_file():
                full_path.unlink()
            else:
                full_path.rmdir()  # Csak üres könyvtárakat törlünk

        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a törlés során: {str(e)}", e) from e

    def list_dir(self, path: Union[str, Path], pattern: Optional[str] = None) -> list[Path]:
        """Könyvtár tartalmának listázása.

        Args:
            path: Könyvtár útvonala
            pattern: Opcionális glob minta a szűréshez

        Returns:
            list[Path]: A talált fájlok és könyvtárak listája

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található
            StorageIOError: Ha a listázás sikertelen
        """
        try:
            full_path = self._get_full_path(path)
            if not full_path.exists():
                raise StorageNotFoundError(f"Könyvtár nem található: {full_path}")
            if not full_path.is_dir():
                raise StorageIOError(f"Nem könyvtár: {full_path}")

            if pattern:
                return list(full_path.glob(pattern))
            return list(full_path.iterdir())

        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a könyvtár listázása során: {str(e)}", e) from e
