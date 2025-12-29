# core/storage/factory.py

Storage factory implementáció a különböző tároló komponensek létrehozásához.

Ez a modul felelős a storage implementációk példányosításáért a factory
minta segítségével. Alapértelmezetten a FileStorage implementációt támogatja,
de további storage típusok is regisztrálhatók dinamikusan.

## Osztályok

### `StorageFactory`

Factory osztály storage komponensek létrehozásához.

    Ez az osztály felelős a különböző storage implementációk példányosításáért.
    Alapértelmezetten a FileStorage implementációt támogatja, de további
    storage típusok is regisztrálhatók.


## Függvények

### `register_storage`

Új storage típus regisztrálása a factory számára.

        Args:
            storage_type: A storage típus egyedi azonosítója (pl. "s3", "database").
            storage_class: A storage osztály, amely implementálja a StorageInterface-t.

        Raises:
            ValueError: Ha a storage_class nem implementálja a StorageInterface-t.

        Example:
            >>> from neural_ai.core.storage.interfaces import StorageInterface
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
            StorageError: Ha nem található a kért storage típus vagy a
                példányosítása sikertelen.

        Example:
            >>> storage = StorageFactory.get_storage("file", base_path="data")
            >>> storage.save_object({"key": "value"}, "config.json")
            >>> # Egyéni paraméterekkel
            >>> storage = StorageFactory.get_storage("file", base_path="data",
            ...                                       create_if_missing=True)


---

**Forrásfájl:** [`core/storage/factory.py`](../../../neural_ai/core/storage/factory.py)
