# Storage Komponens API Dokumentáció

## Interfészek

### ConfigManagerInterface

```python
class StorageInterface(ABC):
    """Adattárolás kezelő interfész."""

    @abstractmethod
    def save_dataframe(
        self,
        df: pd.DataFrame,
        path: Union[str, Path],
        format: str = "csv",
        **kwargs: Any,
    ) -> None:
        """DataFrame mentése."""
        pass

    @abstractmethod
    def load_dataframe(
        self,
        path: Union[str, Path],
        format: Optional[str] = None,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """DataFrame betöltése."""
        pass

    @abstractmethod
    def save_object(
        self,
        obj: Any,
        path: Union[str, Path],
        format: str = "json",
        **kwargs: Any,
    ) -> None:
        """Python objektum mentése."""
        pass

    @abstractmethod
    def load_object(
        self,
        path: Union[str, Path],
        format: Optional[str] = None,
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
    def list_dir(
        self, path: Union[str, Path], pattern: Optional[str] = None
    ) -> list[Path]:
        """Könyvtár tartalmának listázása."""
        pass
```

## Implementációk

### FileStorage

A fájlrendszer alapú storage implementáció.

```python
class FileStorage(StorageInterface):
    """Fájl alapú storage implementáció."""

    def __init__(self, base_path: Optional[Union[str, Path]] = None) -> None:
        """Storage inicializálása.

        Args:
            base_path: Alap könyvtár útvonal (None esetén az aktuális könyvtár)
        """
```

#### Metódusok

##### save_dataframe

```python
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: Union[str, Path],
    format: str = "csv",
    **kwargs: Any,
) -> None:
    """DataFrame mentése.

    Args:
        df: Mentendő DataFrame
        path: Mentési útvonal
        format: Fájl formátum (csv, json, excel)
        **kwargs: További formátum-specifikus paraméterek

    Raises:
        StorageFormatError: Ha a formátum nem támogatott
        StorageIOError: Ha a mentés sikertelen
    """
```

##### load_dataframe

```python
def load_dataframe(
    self,
    path: Union[str, Path],
    format: Optional[str] = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """DataFrame betöltése.

    Args:
        path: Betöltési útvonal
        format: Fájl formátum (ha None, akkor a kiterjesztésből)
        **kwargs: További formátum-specifikus paraméterek

    Returns:
        pd.DataFrame: A betöltött DataFrame

    Raises:
        StorageNotFoundError: Ha a fájl nem található
        StorageFormatError: Ha a formátum nem támogatott
        StorageIOError: Ha a betöltés sikertelen
    """
```

## Kivételek

### StorageError

```python
class StorageError(Exception):
    """Alap kivétel a storage műveletekhez."""

    def __init__(self, message: str, original_error: Optional[Exception] = None) -> None:
        super().__init__(message)
        self.original_error = original_error
```

### Specifikus kivételek

- `StorageFormatError`: Nem támogatott vagy érvénytelen formátum esetén
- `StorageNotFoundError`: Nem létező erőforrás esetén
- `StorageSerializationError`: Szerializációs hibák esetén
- `StorageIOError`: Egyéb I/O műveletek hibái esetén

## Konstansok és konfigurációk

### Támogatott formátumok

```python
_DATAFRAME_FORMATS = {
    "csv": ("read_csv", "to_csv"),
    "json": ("read_json", "to_json"),
    "excel": ("read_excel", "to_excel"),
}

_OBJECT_FORMATS = {"json"}
