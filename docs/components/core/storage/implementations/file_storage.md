# core/storage/implementations/file_storage.py

FileStorage implementáció.

A modulban található:
    - FileStorage: Fájlrendszer alapú storage implementáció

## Osztályok

### `FileStorage`

Fájlrendszer alapú storage implementáció.


## Függvények

### `__init__`

Inicializálja a FileStorage példányt.

        Args:
            base_path: Alap könyvtár útvonala
            logger: Logger példány (opcionális)
            **kwargs: További paraméterek (pl. hardware), amiket figyelmen kívül hagyunk.

### `_setup_format_handlers`

Beállítja a formátum kezelőket.

### `save_csv`

Nincs docstring.

### `load_csv`

Nincs docstring.

### `save_excel`

Nincs docstring.

### `load_excel`

Nincs docstring.

### `save_json`

Nincs docstring.

### `load_json`

Nincs docstring.

### `_check_disk_space`

Check if there's enough disk space for the operation.

        Args:
            file_path: The target file path
            required_bytes: Required bytes for the operation

        Raises:
            InsufficientDiskSpaceError: If there's not enough disk space

### `_check_permissions`

Ellenőrzi a fájl/könyvtár jogosultságokat.

        Args:
            file_path: A célfájl útvonala
            check_write: Ha True, ellenőrzi az írási jogosultságot is

        Raises:
            PermissionDeniedError: Ha a jogosultságok nem megfelelőek
            StorageIOError: Ha az útvonal ellenőrzése sikertelen

### `get_storage_info`

Get storage information for a directory.

        Args:
            directory: The directory path to check

        Returns:
            Dict[str, Any]: Storage information including total, used, and free space

        Raises:
            StorageIOError: If unable to get storage information

### `_get_full_path`

Teljes útvonal előállítása.

        Args:
            path: Relatív vagy abszolút útvonal

        Returns:
            Path: Teljes útvonal

### `_atomic_write`

Atomi fájlírás temp fájllal és átnevezéssel.

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

### `save_dataframe`

Menti a DataFrame objektumot.

        Args:
            df: A mentendő DataFrame
            path: A mentés útvonala
            fmt: A mentés formátuma (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageIOError: Ha a mentés sikertelen
            InsufficientDiskSpaceError: Ha nincs elég lemezterület
            PermissionDeniedError: Ha nincs írási jogosultság

### `load_dataframe`

Betölti a DataFrame objektumot.

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

### `save_object`

Menti a Python objektumot.

        Args:
            obj: A mentendő objektum
            path: A mentés útvonala
            fmt: A mentés formátuma (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Raises:
            StorageFormatError: Ha a formátum nem támogatott
            StorageSerializationError: Ha az objektum nem szerializálható
            StorageIOError: Ha a mentés sikertelen
            InsufficientDiskSpaceError: Ha nincs elég lemezterület
            PermissionDeniedError: Ha nincs írási jogosultság

### `load_object`

Betölti a Python objektumot.

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

### `exists`

Ellenőrzi az útvonal létezését.

        Args:
            path: Az ellenőrizendő útvonal

        Returns:
            bool: True, ha létezik, False ha nem

### `get_metadata`

Lekéri a fájl vagy könyvtár metaadatait.

        Args:
            path: A fájl vagy könyvtár útvonala

        Returns:
            Dict[str, Any]: A metaadatok

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a lekérés sikertelen

### `delete`

Törli a megadott fájlt vagy könyvtárat.

        Args:
            path: A törlendő útvonal

        Raises:
            StorageNotFoundError: Ha a fájl nem található
            StorageIOError: Ha a törlés sikertelen

### `list_dir`

Listázza egy könyvtár tartalmát.

        Args:
            path: A könyvtár útvonala
            pattern: Szűrő minta a fájlnevekre

        Returns:
            Sequence[Path]: A könyvtár tartalma Path objektumokként

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található
            StorageIOError: Ha a listázás sikertelen


---

**Forrásfájl:** [`core/storage/implementations/file_storage.py`](../../../neural_ai/core/storage/implementations/file_storage.py)
