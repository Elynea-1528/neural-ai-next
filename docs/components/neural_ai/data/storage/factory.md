# neural_ai/data/storage/factory.py

Storage factory implementáció a különböző tároló komponensek létrehozásához.

Ez a modul felelős a storage implementációk példányosításáért a factory
minta segítségével. Alapértelmezetten a FileStorage és ParquetStorage implementációkat támogatja,
de további storage típusok is regisztrálhatók dinamikusan.

## Osztályok

### `StorageFactory`

Factory osztály storage komponensek létrehozásához.

    Ez az osztály felelős a különböző storage implementációk példányosításáért.
    Alapértelmezetten a FileStorage és ParquetStorage implementációkat támogatja,
    de további storage típusok is regisztrálhatók.

## Függvények

### `register_storage`

Új storage típus regisztrálása a factory számára.

        Args:
            storage_type: A storage típus egyedi azonosítója (pl. "s3", "database").
            storage_class: A storage osztály, amely implementálja a StorageInterface-t.

        Raises:
            ValueError: Ha a storage_class nem implementálja a StorageInterface-t.

        Example:
            >>> from neural_ai.data.storage.interfaces import StorageInterface
            >>> class S3Storage(StorageInterface):
            ...     pass
            >>> StorageFactory.register_storage("s3", S3Storage)

### `get_storage`

Storage példány létrehozása a megadott típus alapján.

        Args:
            storage_type: A kért storage típus azonosítója (alapértelmezett: "file").
            base_path: Alap könyvtár útvonal a file alapú tároláshoz.
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális).
            **kwargs: További paraméterek a storage osztály konstruktorának.

        Returns:
            StorageInterface: Az inicializált storage példány.

        Raises:
            ValueError: Ha nem található a kért storage típus vagy a
                példányosítása sikertelen.

        Example:
            >>> storage = StorageFactory.get_storage("parquet", base_path="data")
            >>> # Parquet storage használata
            >>> storage = StorageFactory.get_storage("file", base_path="data", create_if_missing=True)


---

**Forrásfájl:** [`neural_ai/data/storage/factory.py`](../../../neural_ai/data/storage/factory.py)