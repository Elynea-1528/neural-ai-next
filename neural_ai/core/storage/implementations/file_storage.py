"""FileStorage implementáció.

A modulban található:
    - FileStorage: Fájlrendszer alapú storage implementáció
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Sequence, Union

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
    """Fájlrendszer alapú storage implementáció."""

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        """Inicializálja a FileStorage példányt.

        Args:
            base_path: Alap könyvtár útvonala
        """
        self._base_path = Path(base_path) if base_path else Path.cwd()
        self._setup_format_handlers()

    def _setup_format_handlers(self) -> None:
        """Beállítja a formátum kezelőket."""

        def save_csv(df: pd.DataFrame, path: str, **kwargs: Any) -> None:
            kwargs.setdefault("index", False)  # Alapértelmezetten ne mentse az indexet
            df.to_csv(path, **kwargs)

        def load_csv(path: str, **kwargs: Any) -> pd.DataFrame:
            return pd.read_csv(path, **kwargs)

        def save_excel(df: pd.DataFrame, path: str, **kwargs: Any) -> None:
            kwargs.setdefault("index", False)  # Alapértelmezetten ne mentse az indexet
            df.to_excel(path, **kwargs)

        def load_excel(path: str, **kwargs: Any) -> pd.DataFrame:
            return pd.read_excel(path, **kwargs)

        def save_json(obj: Any, path: str, **kwargs: Any) -> None:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f, **kwargs)

        def load_json(path: str, **kwargs: Any) -> Any:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f, **kwargs)

        self._DATAFRAME_FORMATS: Dict[str, Dict[str, Callable]] = {
            "csv": {
                "save": save_csv,
                "load": load_csv,
            },
            "excel": {
                "save": save_excel,
                "load": load_excel,
            },
        }

        self._OBJECT_FORMATS: Dict[str, Dict[str, Callable]] = {
            "json": {
                "save": save_json,
                "load": load_json,
            }
        }

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
        path: str,
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Menti a DataFrame objektumot.

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala
            fmt: A mentés formátuma (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageIOError: Ha a mentés sikertelen
        """
        full_path = self._get_full_path(path)

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
            full_path.parent.mkdir(parents=True, exist_ok=True)
            self._DATAFRAME_FORMATS[fmt]["save"](df, str(full_path), **kwargs)
        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a DataFrame mentése során: {str(e)}") from e

    def load_dataframe(
        self,
        path: str,
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Betölti a DataFrame objektumot.

        Args:
            path: A betöltendő fájl útvonala
            fmt: A fájl formátuma (ha None, akkor a kiterjesztésből)
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
            return self._DATAFRAME_FORMATS[fmt]["load"](str(full_path), **kwargs)
        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a DataFrame betöltése során: {str(e)}") from e

    def save_object(
        self,
        obj: Any,
        path: str,
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Menti a Python objektumot.

        Args:
            obj: A mentendő objektum
            path: A mentés útvonala
            fmt: A mentés formátuma (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem szerializálható
            StorageIOError: Ha a mentés sikertelen
        """
        full_path = self._get_full_path(path)

        if fmt is None:
            fmt = full_path.suffix.lower().lstrip(".")
            if not fmt:
                raise StorageFormatError("Nem sikerült meghatározni a fájl formátumát")

        if fmt not in self._OBJECT_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott objektum formátum: {fmt}. "
                f"Támogatott formátumok: {list(self._OBJECT_FORMATS.keys())}"
            )

        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            self._OBJECT_FORMATS[fmt]["save"](obj, str(full_path), **kwargs)
        except (TypeError, ValueError) as e:
            raise StorageSerializationError(f"Az objektum nem szerializálható: {str(e)}") from e
        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba az objektum mentése során: {str(e)}") from e

    def load_object(
        self,
        path: str,
        fmt: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        """Betölti a Python objektumot.

        Args:
            path: A betöltendő fájl útvonala
            fmt: A fájl formátuma (ha None, akkor a kiterjesztésből)
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

        if fmt is None:
            fmt = full_path.suffix.lower().lstrip(".")
            if not fmt:
                raise StorageFormatError("Nem sikerült meghatározni a fájl formátumát")

        if fmt not in self._OBJECT_FORMATS:
            raise StorageFormatError(
                f"Nem támogatott objektum formátum: {fmt}. "
                f"Támogatott formátumok: {list(self._OBJECT_FORMATS.keys())}"
            )

        try:
            return self._OBJECT_FORMATS[fmt]["load"](str(full_path), **kwargs)
        except json.JSONDecodeError as e:
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}") from e
        except (TypeError, ValueError) as e:
            raise StorageSerializationError(f"Az objektum nem deszerializálható: {str(e)}") from e
        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}") from e

    def exists(self, path: str) -> bool:
        """Ellenőrzi az útvonal létezését.

        Args:
            path: Az ellenőrizendő útvonal

        Returns:
            bool: True, ha létezik, False ha nem
        """
        return self._get_full_path(path).exists()

    def get_metadata(self, path: str) -> Dict[str, Any]:
        """Lekéri a fájl vagy könyvtár metaadatait.

        Args:
            path: A fájl vagy könyvtár útvonala

        Returns:
            Dict[str, Any]: A metaadatok

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a lekérés sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        try:
            stat = full_path.stat()
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "is_file": full_path.is_file(),
                "is_dir": full_path.is_dir(),
            }
        except Exception as e:
            raise StorageIOError(f"Hiba a metaadatok lekérése során: {str(e)}") from e

    def delete(self, path: str) -> None:
        """Törli a megadott fájlt vagy könyvtárat.

        Args:
            path: A törlendő útvonal

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
            raise StorageIOError(f"Hiba a törlés során: {str(e)}") from e

    def list_dir(
        self,
        path: str,
        pattern: Optional[str] = None,
    ) -> Sequence[Path]:
        """Listázza egy könyvtár tartalmát.

        Args:
            path: A könyvtár útvonala
            pattern: Szűrő minta a fájlnevekre

        Returns:
            Sequence[Path]: A könyvtár tartalma Path objektumokként

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található
            StorageIOError: Ha a listázás sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Könyvtár nem található: {full_path}")
        if not full_path.is_dir():
            raise StorageIOError(f"Az útvonal nem könyvtár: {full_path}")

        try:
            pattern = pattern or "*"
            return list(full_path.glob(pattern))
        except StorageError:
            raise
        except Exception as e:
            raise StorageIOError(f"Hiba a könyvtár listázása során: {str(e)}") from e
