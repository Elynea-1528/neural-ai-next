"""FileStorage implementáció.

A modulban található:
    - FileStorage: Fájlrendszer alapú tárolási implementáció Parquet formátummal.
"""

import os
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypedDict, cast

from neural_ai.data.storage.exceptions import (
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError,
    StorageSerializationError,
)
from neural_ai.data.storage.interfaces.storage_interface import StorageInterface

if TYPE_CHECKING:
    import pandas as pd

    from neural_ai.core.config.interfaces.config_interface import ConfigInterface
    from neural_ai.core.events.interfaces.event_bus_interface import EventBusInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface
    from neural_ai.data.storage.backends.base import StorageBackend


class StorageConfig(TypedDict, total=False):
    """Tárolási konfiguráció."""

    base_path: str | Path
    compression: str
    engine: str


class FileStorage(StorageInterface):
    """Fájlrendszer alapú tárolási implementáció."""

    def __init__(
        self,
        logger: "LoggerInterface",
        config: "ConfigInterface | None" = None,
        event_bus: "EventBusInterface | None" = None,
        base_path: str | Path | None = None,
        hardware: "HardwareInterface | None" = None,
        **kwargs: Any,
    ) -> None:
        """Inicializálja a FileStorage példányt backend selectorral.

        Hardver detekció alapján kiválasztja a megfelelő tárolási backend-et.
        Ha AVX2 elérhető, PolarsBackend-et használ, különben PandasBackend-et.

        Args:
            logger: Logger interfész
            config: Konfiguráció interfész
            event_bus: Eseménybusz interfész
            base_path: Alap könyvtár útvonala
            hardware: Hardver interfész (opcionális)
            **kwargs: További paraméterek
        """
        self.logger = logger
        self.config = config
        self.event_bus = event_bus
        self.storage_config = cast(StorageConfig, config.get("storage") or {} if config else {})
        self._base_path = (
            Path(base_path) if base_path else Path(self.storage_config.get("base_path", "."))
        )

        # Dependency Injection a HardwareInterface-hez
        if hardware is None:
            from neural_ai.core.utils.factory import HardwareFactory

            self.hardware = HardwareFactory.get_hardware_interface()
        else:
            self.hardware = hardware

        # Backend kiválasztás
        self._select_backend()

        self._initialized = True

    def _select_backend(self) -> None:
        """Backend kiválasztása hardver detekció alapján.

        Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért
        a hardver képességek alapján. Külön metódusba van kiszervezve,
        hogy a tesztek könnyen mockolhassák.
        """
        if self.hardware.has_avx2():
            from neural_ai.data.storage.backends.polars_backend import PolarsBackend

            self.backend: StorageBackend = PolarsBackend(
                logger=self.logger, name="polars", supported_formats=["parquet"]
            )
            # Log a backend kiválasztáshoz
            self.logger.debug(
                f"Selected backend: {self.backend.name} (AVX2={self.hardware.has_avx2()})"
            )
            self.logger.info(
                "AVX2 support detected. Using PolarsBackend for accelerated data processing."
            )
        else:
            from neural_ai.data.storage.backends.pandas_backend import PandasBackend

            self.backend: StorageBackend = PandasBackend(
                logger=self.logger, name="pandas", supported_formats=["parquet"]
            )
            # Log a backend kiválasztáshoz
            self.logger.debug(
                f"Selected backend: {self.backend.name} (AVX2={self.hardware.has_avx2()})"
            )
            self.logger.warning(
                "Legacy CPU detected. Running in Compatibility Mode with PandasBackend."
            )

    def _check_disk_space(self, file_path: Path, required_bytes: int) -> None:
        """Ellenőrzi, hogy van-e elég lemezterület a művelethez.

        Args:
            file_path: A célfájl útvonala
            required_bytes: Szükséges bájtok száma a művelethez

        Raises:
            InsufficientDiskSpaceError: Ha nincs elég lemezterület
        """
        try:
            stat = os.statvfs(file_path.parent)
            free_bytes = stat.f_bavail * stat.f_frsize
            if free_bytes < required_bytes:
                raise StorageIOError(
                    f"Nincs elég lemezterület: {free_bytes / 1024 / 1024:.2f} MB elérhető, "
                    f"{required_bytes / 1024 / 1024:.2f} MB szükséges"
                )
        except OSError as e:
            raise StorageIOError(f"Nem sikerült ellenőrizni a lemezterületet: {e}") from e

    def _check_permissions(self, file_path: Path, check_write: bool = True) -> None:
        """Ellenőrzi a fájl/könyvtár jogosultságokat.

        Args:
            file_path: A célfájl útvonala
            check_write: Ha True, ellenőrzi az írási jogosultságot is

        Raises:
            PermissionDeniedError: Ha a jogosultságok nem megfelelőek
            StorageIOError: Ha az útvonal ellenőrzése sikertelen
        """
        try:
            if not file_path.parent.exists():
                raise StorageIOError(f"A szülő könyvtár nem létezik: {file_path.parent}")

            if check_write and not os.access(str(file_path.parent), os.W_OK):
                raise StorageIOError(f"Nincs írási jogosultság a könyvtárhoz: {file_path.parent}")

            if file_path.exists() and not os.access(str(file_path), os.R_OK):
                raise StorageIOError(f"Nincs olvasási jogosultság a fájlhoz: {file_path}")
        except OSError as e:
            raise StorageIOError(f"Nem sikerült ellenőrizni a jogosultságokat: {e}") from e

    def get_storage_info(self, directory: str | Path) -> dict[str, Any]:
        """Tárolási információk lekérdezése egy könyvtárhoz.

        Args:
            directory: Az ellenőrizendő könyvtár útvonala

        Returns:
            Dict[str, Any]: Tárolási információk, beleértve a teljes, használt és szabad területet

        Raises:
            StorageIOError: Ha nem lehet lekérdezni a tárolási információkat
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
            raise StorageIOError(f"Nem sikerült lekérdezni a tárolási információkat: {e}") from e

    def _get_full_path(self, path: str | Path) -> Path:
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
        df: "pd.DataFrame",
        path: str,
        fmt: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Menti a DataFrame objektumot Parquet formátumban.

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala (.parquet kiterjesztéssel)
            fmt: A mentés formátuma (csak 'parquet' támogatott)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem parquet
            StorageIOError: Ha a mentés sikertelen
        """
        full_path = self._get_full_path(path)

        # Csak Parquet támogatott
        if fmt is not None and fmt != "parquet":
            raise StorageFormatError("Csak Parquet formátum támogatott")

        # Ellenőrizzük a kiterjesztést
        if not full_path.suffix.lower() == ".parquet":
            raise StorageFormatError("A fájlnak .parquet kiterjesztéssel kell rendelkeznie")

        # Ellenőrizzük a jogosultságokat
        self._check_permissions(full_path, check_write=True)

        # Ellenőrizzük a lemezterületet (becsült méret alapján)
        try:
            estimated_size = df.memory_usage(deep=True).sum()
            self._check_disk_space(full_path, int(estimated_size * 1.1))
        except StorageIOError:
            raise
        except Exception as e:
            self.logger.warning(f"Nem sikerült becsülni a DataFrame méretét: {e}")

        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            # Backend-en keresztül mentjük
            self.backend.write(df, str(full_path), **kwargs)
            self.logger.info(f"DataFrame sikeresen mentve: {full_path}")
        except Exception as e:
            self.logger.error(f"Hiba a DataFrame mentése során: {full_path}")
            raise StorageIOError(f"Hiba a DataFrame mentése során: {str(e)}") from e

    def load_dataframe(
        self,
        path: str,
        fmt: str | None = None,
        **kwargs: Any,
    ) -> "pd.DataFrame":
        """Betölti a DataFrame objektumot Parquet formátumból.

        Args:
            path: A betöltendő fájl útvonala (.parquet kiterjesztéssel)
            fmt: A fájl formátuma (csak 'parquet' támogatott)
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            pd.DataFrame: A betöltött DataFrame

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem parquet
            StorageIOError: Ha a betöltés sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Csak Parquet támogatott
        if fmt is not None and fmt != "parquet":
            raise StorageFormatError("Csak Parquet formátum támogatott")

        # Ellenőrizzük a kiterjesztést
        if not full_path.suffix.lower() == ".parquet":
            raise StorageFormatError("A fájlnak .parquet kiterjesztéssel kell rendelkeznie")

        # Ellenőrizzük az olvasási jogosultságot
        self._check_permissions(full_path, check_write=False)

        try:
            # Backend-en keresztül töltjük be
            result = self.backend.read(str(full_path), **kwargs)
            self.logger.info(f"DataFrame sikeresen betöltve: {full_path}")
            return cast(pd.DataFrame, result)
        except Exception as e:
            self.logger.error(f"Hiba a DataFrame betöltése során: {full_path}")
            raise StorageIOError(f"Hiba a DataFrame betöltése során: {str(e)}") from e

    def save_object(
        self,
        obj: Any,
        path: str,
        fmt: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Menti a Python objektumot pickle formátumban.

        Args:
            obj: A mentendő objektum
            path: A mentés útvonala (.pkl kiterjesztéssel)
            fmt: A mentés formátuma (csak 'pkl' támogatott)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem pkl
            StorageSerializationError: Ha az objektum nem szerializálható
            StorageIOError: Ha a mentés sikertelen
        """
        full_path = self._get_full_path(path)

        # Csak pickle támogatott
        if fmt is not None and fmt != "pkl":
            raise StorageFormatError("Csak pickle formátum támogatott objektumokhoz")

        # Ellenőrizzük a kiterjesztést
        if not full_path.suffix.lower() == ".pkl":
            raise StorageFormatError("Az objektum fájlnak .pkl kiterjesztéssel kell rendelkeznie")

        # Ellenőrizzük a jogosultságokat
        self._check_permissions(full_path, check_write=True)

        # Ellenőrizzük a lemezterületet (becsült méret alapján)
        try:
            import sys

            estimated_size = sys.getsizeof(str(obj))
            self._check_disk_space(full_path, int(estimated_size * 1.1))
        except StorageIOError:
            raise
        except Exception as e:
            self.logger.warning(f"Nem sikerült becsülni az objektum méretét: {e}")

        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            import pickle

            with open(full_path, "wb") as f:
                pickle.dump(obj, f, **kwargs)
            self.logger.info(f"Objektum sikeresen mentve: {full_path}")
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
        """Betölti a Python objektumot pickle formátumból.

        Args:
            path: A betöltendő fájl útvonala (.pkl kiterjesztéssel)
            fmt: A fájl formátuma (csak 'pkl' támogatott)
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            Any: A betöltött objektum

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem pkl
            StorageSerializationError: Ha az objektum nem deszerializálható
            StorageIOError: Ha a betöltés sikertelen
        """
        full_path = self._get_full_path(path)
        if not full_path.exists():
            raise StorageNotFoundError(f"Fájl nem található: {full_path}")

        # Csak pickle támogatott
        if fmt is not None and fmt != "pkl":
            raise StorageFormatError("Csak pickle formátum támogatott objektumokhoz")

        # Ellenőrizzük a kiterjesztést
        if not full_path.suffix.lower() == ".pkl":
            raise StorageFormatError("Az objektum fájlnak .pkl kiterjesztéssel kell rendelkeznie")

        # Ellenőrizzük az olvasási jogosultságot
        self._check_permissions(full_path, check_write=False)

        try:
            import pickle

            with open(full_path, "rb") as f:
                result = pickle.load(f, **kwargs)
            self.logger.info(f"Objektum sikeresen betöltve: {full_path}")
            return result
        except (TypeError, ValueError) as e:
            self.logger.error(f"Szerializációs hiba az objektum betöltése során: {full_path}")
            raise StorageSerializationError(f"Az objektum nem deszerializálható: {str(e)}") from e
        except Exception as e:
            self.logger.error(f"Hiba az objektum betöltése során: {full_path}")
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
        try:
            if not full_path.exists():
                raise StorageNotFoundError(f"Fájl nem található: {full_path}")

            stat = full_path.stat()
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "is_file": full_path.is_file(),
                "is_dir": full_path.is_dir(),
            }
        except StorageNotFoundError:
            raise
        except OSError as e:
            raise StorageIOError(f"Hiba a metaadatok lekérése során: {str(e)}") from e
        except Exception as e:
            raise StorageIOError(f"Váratlan hiba a metaadatok lekérése során: {str(e)}") from e

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
