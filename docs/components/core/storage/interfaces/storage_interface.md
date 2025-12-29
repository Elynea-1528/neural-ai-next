# core/storage/interfaces/storage_interface.py

Storage interfész modul.

Ez a modul definiálja a tárolási műveletek absztrakt interfészét,
amelyet minden konkrét tárolási implementációnak implementálnia kell.

## Osztályok

### `StorageInterface`

Absztrakt interfész tárolási műveletek definiálásához.

    Ez az interfész biztosítja a standardizált tárolási műveleteket
    DataFrame-ekkel és általános objektumokkal való munkavégzéshez.


## Függvények

### `save_dataframe`

DataFrame mentése a megadott útvonalra.

        Args:
            df: A mentendő pandas DataFrame.
            path: A célfájl elérési útja.
            **kwargs: További formázási és mentési opciók.

        Raises:
            StorageIOError: Ha I/O hiba történik a mentés során.
            StorageFormatError: Ha a kért formátum nem támogatott.
            StorageSerializationError: Ha az adatok nem szerializálhatók.

### `load_dataframe`

DataFrame betöltése a megadott útvonalról.

        Args:
            path: A forrásfájl elérési útja.
            **kwargs: További betöltési és formázási opciók.

        Returns:
            A betöltött pandas DataFrame.

        Raises:
            StorageNotFoundError: Ha a forrásfájl nem található.
            StorageFormatError: Ha a fájl formátuma nem támogatott.
            StorageSerializationError: Ha az adatok nem deszerializálhatók.
            StorageIOError: Ha I/O hiba történik a betöltés során.

### `save_object`

Objektum mentése a megadott útvonalra.

        Args:
            obj: A mentendő objektum.
            path: A célfájl elérési útja.
            **kwargs: További szerializációs opciók.

        Raises:
            StorageIOError: Ha I/O hiba történik a mentés során.
            StorageFormatError: Ha a kért formátum nem támogatott.
            StorageSerializationError: Ha az objektum nem szerializálható.

### `load_object`

Objektum betöltése a megadott útvonalról.

        Args:
            path: A forrásfájl elérési útja.
            **kwargs: További deszerializációs opciók.

        Returns:
            A betöltött objektum.

        Raises:
            StorageNotFoundError: Ha a forrásfájl nem található.
            StorageFormatError: Ha a fájl formátuma nem támogatott.
            StorageSerializationError: Ha az objektum nem deszerializálható.
            StorageIOError: Ha I/O hiba történik a betöltés során.

### `exists`

Ellenőrzi, hogy az útvonal létezik-e.

        Args:
            path: Az ellenőrizendő útvonal.

        Returns:
            True, ha az útvonal létezik, egyébként False.

### `get_metadata`

Fájl vagy könyvtár metaadatainak lekérdezése.

        Args:
            path: A cél útvonal.

        Returns:
            A metaadatok szótárba rendezve.

        Raises:
            StorageNotFoundError: Ha az útvonal nem található.
            StorageIOError: Ha a metaadatok lekérdezése sikertelen.

### `delete`

Fájl vagy könyvtár törlése.

        Args:
            path: A törlendő útvonal.

        Raises:
            StorageNotFoundError: Ha az útvonal nem található.
            StorageIOError: Ha a törlés sikertelen.

### `list_dir`

Könyvtár tartalmának listázása.

        Args:
            path: A könyvtár elérési útja.
            pattern: Opcionális glob minta a fájlnevek szűrésére.

        Returns:
            A könyvtárban található elemek Path objektumokként.

        Raises:
            StorageNotFoundError: Ha a könyvtár nem található.
            StorageIOError: Ha a listázás sikertelen.


---

**Forrásfájl:** [`core/storage/interfaces/storage_interface.py`](../../../neural_ai/core/storage/interfaces/storage_interface.py)
