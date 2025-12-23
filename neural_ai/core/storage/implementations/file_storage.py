"""FileStorage implementáció.

A modulban található:
    - FileStorage: Fájlrendszer alapú storage implementáció
"""

import json
import os
from collections.abc import Callable, Sequence
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, cast

import pandas as pd

from neural_ai.core.base.exceptions import (
    InsufficientDiskSpaceError,
    PermissionDeniedError,
    StorageWriteError,
)
from neural_ai.core.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface


class FileStorage(StorageInterface):
    """Fájlrendszer alapú storage implementáció."""

    def __init__(
        self, base_path: str | Path | None = None, logger: Optional["LoggerInterface"] = None
    ) -> None:
        """Inicializálja a FileStorage példányt.

        Args:
            base_path: Alap könyvtár útvonala
            logger: Logger példány (opcionális)
        """
        self._base_path = Path(base_path) if base_path else Path.cwd()
        self.logger: LoggerInterface | None = logger
        self._setup_format_handlers()

    def _setup_format_handlers(self) -> None:
        """Beállítja a formátum kezelőket."""

        def save_csv(df: pd.DataFrame, path: str, **kwargs: Any) -> None:
            kwargs.setdefault("index", False)  # Alapértelmezetten ne mentse az indexet
            # CSV esetén közvetlen mentés
            df.to_csv(path, **kwargs)

        def load_csv(path: str, **kwargs: Any) -> pd.DataFrame:
            return cast(pd.DataFrame, pd.read_csv(path, **kwargs))

        def save_excel(df: pd.DataFrame, path: str, **kwargs: Any) -> None:
            kwargs.setdefault("index", False)  # Alapértelmezetten ne mentse az indexet
            # Excel esetén közvetlen mentés
            df.to_excel(path, **kwargs)

        def load_excel(path: str, **kwargs: Any) -> pd.DataFrame:
            return cast(pd.DataFrame, pd.read_excel(path, **kwargs))

        def save_json(obj: Any, path: str, **kwargs: Any) -> None:
            # JSON esetén közvetlen mentés
            with open(path, "w", encoding="utf-8") as f:
                json.dump(obj, f, **kwargs)

        def load_json(path: str, **kwargs: Any) -> Any:
            with open(path, encoding="utf-8") as f:
                return json.load(f, **kwargs)

        self._DATAFRAME_FORMATS: dict[str, dict[str, Callable[..., Any]]] = {
            "csv": {
                "save": save_csv,
                "load": load_csv,
            },
            "excel": {
                "save": save_excel,
                "load": load_excel,
            },
        }

        self._OBJECT_FORMATS: dict[str, dict[str, Callable[..., Any]]] = {
            "json": {
                "save": save_json,
                "load": load_json,
            }
        }

    def _check_disk_space(self, file_path: Path, required_bytes: int) -> None:
        """Check if there's enough disk space for the operation.

        Args:
            file_path: The target file path
            required_bytes: Required bytes for the operation

        Raises:
            InsufficientDiskSpaceError: If there's not enough disk space
        """
        try:
            stat = os.statvfs(file_path.parent)
            free_bytes = stat.f_bavail * stat.f_frsize
            if free_bytes < required_bytes:
                raise InsufficientDiskSpaceError(
                    f"Insufficient disk space: {free_bytes / 1024 / 1024:.2f} MB available, "
                    f"{required_bytes / 1024 / 1024:.2f} MB required"
                )
        except OSError as e:
            raise StorageIOError(f"Failed to check disk space: {e}") from e

    def _check_permissions(self, file_path: Path, check_write: bool = True) -> None:
        """Check file/directory permissions.

        Args:
            file_path: The target file path
            check_write: Whether to check write permissions

        Raises:
            PermissionDeniedError: If permissions are insufficient
            StorageIOError: If path check fails
        """
        try:
            if not file_path.parent.exists():
                raise PermissionDeniedError(f"Parent directory does not exist: {file_path.parent}")

            if check_write and not os.access(file_path.parent, os.W_OK):
                raise PermissionDeniedError(
                    f"No write permission for directory: {file_path.parent}"
                )

            if file_path.exists() and not os.access(file_path, os.R_OK):
                raise PermissionDeniedError(f"No read permission for file: {file_path}")
        except OSError as e:
            raise StorageIOError(f"Failed to check permissions: {e}") from e

    def get_storage_info(self, directory: str | Path) -> dict[str, Any]:
        """Get storage information for a directory.

        Args:
            directory: The directory path to check

        Returns:
            Dict[str, Any]: Storage information including total, used, and free space

        Raises:
            StorageIOError: If unable to get storage information
        """
        try:
            directory = Path(directory)
            stat = os.statvfs(directory)

            return {
                "total_space_gb": (stat.f_blocks * stat.f_frsize) / 1024 / 1024 / 1024,
                "used_space_gb": ((stat.f_blocks - stat.f_bavail) * stat.f_frsize)
                / 1024
                / 1024
                / 1024,
                "free_space_gb": (stat.f_bavail * stat.f_frsize) / 1024 / 1024 / 1024,
                "free_space_percent": (stat.f_bavail / stat.f_blocks) * 100,
            }
        except OSError as e:
            raise StorageIOError(f"Failed to get storage info: {e}") from e

    def _get_full_path(self, path: str | Path) -> Path:
        """Teljes útvonal előállítása.

        Args:
            path: Relatív vagy abszolút útvonal

        Returns:
            Path: Teljes útvonal
        """
        path = Path(path)
        return path if path.is_absolute() else self._base_path / path

    def _atomic_write(
        self,
        file_path: Path,
        content: str | bytes | Any,
        mode: str = "w",
        fmt: str = "json",
        **kwargs: Any,
    ) -> None:
        """Atomi fájlírás temp fájllal és átnevezéssel.

        Args:
            file_path: A célfájl útvonala
            content: Az írandó tartalom (str, bytes, DataFrame, vagy bármilyen objektum)
            mode: Fájl mód ('w' vagy 'wb')
            fmt: Formátum ('json', 'csv', 'excel', stb.)
            **kwargs: További paraméterek a formátum-specifikus mentéshez

        Raises:
            StorageWriteError: Ha az írás sikertelen
            StorageFormatError: Ha a formátum nem támogatott
            InsufficientDiskSpaceError: Ha nincs elég lemezterület
            PermissionDeniedError: Ha nincs megfelelő jogosultság
        """
        # Check permissions first
        self._check_permissions(file_path, check_write=True)

        # Calculate required space
        if isinstance(content, str):
            content_bytes = len(content.encode("utf-8"))
        elif isinstance(content, bytes):
            content_bytes = len(content)
        else:
            # For non-string, non-bytes content (like DataFrames), use default size
            # since they are handled by format-specific savers
            content_bytes = 1024 * 1024  # 1MB default

        # Check disk space (add 10% buffer for filesystem overhead)
        self._check_disk_space(file_path, int(content_bytes * 1.1))

        temp_path = file_path.with_suffix(file_path.suffix + ".tmp")

        try:
            # DataFrame esetén
            if fmt in self._DATAFRAME_FORMATS:
                self._DATAFRAME_FORMATS[fmt]["save"](content, str(temp_path), **kwargs)
            # Objektum esetén
            elif fmt in self._OBJECT_FORMATS:
                self._OBJECT_FORMATS[fmt]["save"](content, str(temp_path), **kwargs)
            # Szöveg vagy bytes esetén
            else:
                with open(temp_path, mode, encoding="utf-8" if "b" not in mode else None) as f:
                    if isinstance(content, (str, bytes)):
                        f.write(content)
                    else:
                        json.dump(content, f, indent=2, ensure_ascii=False)
                    f.flush()
                    os.fsync(f.fileno())
        except OSError as e:
            if temp_path.exists():
                temp_path.unlink()
            raise StorageWriteError(f"Failed to write temporary file: {e}") from e

        try:
            os.replace(temp_path, file_path)
        except OSError as e:
            if temp_path.exists():
                temp_path.unlink()
            raise StorageWriteError(f"Failed to replace file: {e}") from e

    def save_dataframe(
        self,
        df: pd.DataFrame,
        path: str,
        fmt: str | None = None,
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
        except OSError as e:
            if self.logger:
                self.logger.error(f"IO hiba a DataFrame mentése során: {full_path}")
            raise StorageIOError(f"Hiba a DataFrame mentése során: {str(e)}") from e
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Váratlan hiba a DataFrame mentése során: {full_path}",
                )
            raise StorageIOError(f"Hiba a DataFrame mentése során: {str(e)}") from e

    def load_dataframe(
        self,
        path: str,
        fmt: str | None = None,
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
            PermissionDeniedError: Ha nincs olvasási jogosultság
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Check read permissions
        self._check_permissions(full_path, check_write=False)

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
            return cast(
                pd.DataFrame,
                self._DATAFRAME_FORMATS[fmt]["load"](str(full_path), **kwargs),
            )
        except OSError as e:
            if self.logger:
                self.logger.error(f"IO hiba a DataFrame betöltése során: {full_path}")
            raise StorageIOError(f"Hiba a DataFrame betöltése során: {str(e)}") from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Váratlan hiba a DataFrame betöltése során: {full_path}")
            raise StorageIOError(f"Hiba a DataFrame betöltése során: {str(e)}") from e

    def save_object(
        self,
        obj: Any,
        path: str,
        fmt: str | None = None,
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
        except Exception as e:
            raise StorageIOError(f"Hiba az objektum mentése során: {str(e)}") from e

    def load_object(
        self,
        path: str,
        fmt: str | None = None,
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
            PermissionDeniedError: Ha nincs olvasási jogosultság
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Check read permissions
        self._check_permissions(full_path, check_write=False)

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
            if self.logger:
                self.logger.error(f"JSON dekódolási hiba az objektum betöltése során: {full_path}")
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}") from e
        except (TypeError, ValueError) as e:
            if self.logger:
                self.logger.error(f"Szerializációs hiba az objektum betöltése során: {full_path}")
            raise StorageSerializationError(f"Az objektum nem deszerializálható: {str(e)}") from e
        except OSError as e:
            if self.logger:
                self.logger.error(f"IO hiba az objektum betöltése során: {full_path}")
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}") from e
        except Exception as e:
            if self.logger:
                self.logger.error(f"Váratlan hiba az objektum betöltése során: {full_path}")
            raise StorageIOError(f"Hiba az objektum betöltése során: {str(e)}") from e

    def exists(self, path: str) -> bool:
        """Ellenőrzi az útvonal létezését.

        Args:
            path: Az ellenőrizendő útvonal

        Returns:
            bool: True, ha létezik, False ha nem
        """
        return self._get_full_path(path).exists()

    def get_metadata(self, path: str) -> dict[str, Any]:
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
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        try:
            if full_path.is_file():
                full_path.unlink()
            else:
                full_path.rmdir()  # Csak üres könyvtárakat törlünk

        except Exception as e:
            raise StorageIOError(f"Hiba a törlés során: {str(e)}") from e

    def list_dir(
        self,
        path: str,
        pattern: str | None = None,
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
        except Exception as e:
            raise StorageIOError(f"Hiba a könyvtár listázása során: {str(e)}") from e
