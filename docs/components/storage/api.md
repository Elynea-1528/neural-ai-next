# Storage Komponens API Dokumentáció

## Interfészek

### StorageInterface

```python
class StorageInterface(ABC):
    """Storage interfész osztály."""

    @abstractmethod
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Any) -> None:
        """Végrehajt egy DataFrame mentési műveletet.

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageIOError: Ha a mentés sikertelen
            StorageSerializationError: Ha az adatok nem szerializálhatók
        """

    @abstractmethod
    def load_dataframe(self, path: str, **kwargs: Any) -> pd.DataFrame:
        """Betölt egy DataFrame objektumot a megadott útvonalon.

        Args:
            path: A betöltendő fájl útvonala
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            pd.DataFrame: A betöltött DataFrame

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az adatok nem deszerializálhatók
            StorageIOError: Ha a betöltés sikertelen
        """

    @abstractmethod
    def save_object(self, obj: Any, path: str, **kwargs: Any) -> None:
        """Végrehajt egy objektum mentési műveletet.

        Args:
            obj: A mentendő objektum
            path: A mentés útvonala
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem szerializálható
            StorageIOError: Ha a mentés sikertelen
        """

    @abstractmethod
    def load_object(self, path: str, **kwargs: Any) -> Any:
        """Betölt egy objektumot a megadott útvonalon.

        Args:
            path: A betöltendő fájl útvonala
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            Any: A betöltött objektum

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem deszerializálható
            StorageIOError: Ha a betöltés sikertelen
        """

    @abstractmethod
    def exists(self, path: str) -> bool:
        """Ellenőrzi egy útvonal létezését.

        Args:
            path: Az ellenőrizendő útvonal

        Returns:
            bool: True, ha létezik, False ha nem
        """

    @abstractmethod
    def get_metadata(self, path: str) -> Dict[str, Any]:
        """Lekéri egy fájl vagy könyvtár metaadatait.

        Args:
            path: A fájl vagy könyvtár útvonala

        Returns:
            Dict[str, Any]: A metaadatok

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a lekérés sikertelen
        """

    @abstractmethod
    def delete(self, path: str) -> None:
        """Törli a megadott fájlt vagy könyvtárat.

        Args:
            path: A törlendő útvonal

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a törlés sikertelen
        """

    @abstractmethod
    def list_dir(self, path: str, pattern: Optional[str] = None) -> Sequence[Path]:
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
```

## Implementációk

### FileStorage

A fájlrendszer alapú storage implementáció.

```python
class FileStorage(StorageInterface):
    """Fájlrendszer alapú storage implementáció."""

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        """Inicializálja a FileStorage példányt.

        Args:
            base_path: Alap könyvtár útvonala (None esetén az aktuális könyvtár)
        """

    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Any) -> None:
        """DataFrame mentése.

        A formátum automatikusan felismerésre kerül a fájl kiterjesztése alapján.
        Az index alapértelmezetten nem kerül mentésre, de felülírható a kwargs-ban.

        Támogatott formátumok:
        - .csv: CSV fájl (pandas to_csv)
        - .xlsx: Excel fájl (pandas to_excel)

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala
            **kwargs: További pandas mentési paraméterek (pl. index=True)
        """
```

## Kivételek

### StorageError

```python
class StorageError(Exception):
    """Alap kivétel osztály a storage műveletekhez."""

    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error
```

### Specifikus kivételek

- `StorageFormatError`: Nem támogatott vagy érvénytelen formátum esetén
- `StorageNotFoundError`: Nem létező erőforrás esetén
- `StorageSerializationError`: Szerializációs hibák esetén
- `StorageIOError`: Egyéb I/O műveletek hibái esetén
