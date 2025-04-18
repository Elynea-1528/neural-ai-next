# Storage Komponens Architektúra

## Áttekintés

A storage komponens egy moduláris, interfész alapú rendszer, amely különböző típusú adatok perzisztens tárolását és betöltését biztosítja. Az architektúra lehetővé teszi különböző storage implementációk létrehozását és egyszerű integrációját.

## Architektúrális diagram

```
+-------------------+
|  StorageInterface |
+-------------------+
         ^
         |
    +-----------+
    | FileStorage|
    +-----------+

+------------------+     +------------------+     +------------------+
|    DataFrame     |     |  Python Objects  |     |   File System   |
|    Operations    |     |   Serialization  |     |   Operations    |
+------------------+     +------------------+     +------------------+
         ^                       ^                        ^
         |                       |                        |
         +---------------+-------+------------------------+
                        |
                  +-----------+
                  |FileStorage|
                  +-----------+
```

## Komponens rétegek

### 1. Interfész réteg

```python
StorageInterface
├── DataFrame műveletek
├── Objektum műveletek
└── Fájlrendszer műveletek
```

Ez a réteg definiálja a komponens publikus API-ját és biztosítja a különböző implementációk konzisztenciáját.

### 2. Implementációs réteg

```python
FileStorage
├── DataFrame kezelés
│   ├── CSV formátum
│   ├── JSON formátum
│   └── Excel formátum
├── Objektum kezelés
│   └── JSON formátum
└── Fájlrendszer műveletek
    ├── Útvonal kezelés
    ├── Metaadatok
    └── Könyvtár műveletek
```

Ez a réteg tartalmazza a konkrét implementációkat a különböző storage típusokhoz.

### 3. Kivételkezelési réteg

```python
StorageError
├── StorageFormatError
├── StorageNotFoundError
├── StorageSerializationError
└── StorageIOError
```

Specifikus kivételosztályok a különböző hibatípusok kezeléséhez.

## Adatfolyam

### DataFrame mentése

```
Client -> StorageInterface.save_dataframe()
  -> FileStorage.save_dataframe()
    -> Format validation
    -> Path resolution
    -> DataFrame serialization
      -> File system write
```

### Objektum betöltése

```
Client -> StorageInterface.load_object()
  -> FileStorage.load_object()
    -> Path resolution
    -> Format detection
    -> File system read
      -> Object deserialization
```

## Integrációs pontok

### 1. Pandas integráció

- DataFrame I/O műveletek
- Formátum specifikus paraméterek
- Automatikus index kezelés

### 2. Fájlrendszer integráció

- Útvonal kezelés (pathlib)
- Könyvtár műveletek
- Metaadatok lekérése

### 3. Szerializáció

- JSON formátum
- Típus konverziók
- Hibakezelés

## Biztonsági szempontok

### 1. Útvonal validáció

```python
def _get_full_path(self, path: Union[str, Path]) -> Path:
    path = Path(path)
    return path if path.is_absolute() else self._base_path / path
```

### 2. Hibakezelés

```python
try:
    # Storage művelet
except Exception as e:
    raise StorageError("Művelet sikertelen", e)
```

### 3. Jogosultságok

- Fájl műveletek előtti ellenőrzés
- Megfelelő kivételek dobása

## Teljesítmény szempontok

### 1. Memóriahasználat

- Nagy fájlok chunked feldolgozása
- Metaadatok lusta betöltése

### 2. I/O optimalizáció

- Buffer használat
- Batch műveletek

## Monitorozás és diagnosztika

### 1. Loggolás

- Művelet kezdete/vége
- Hibák részletes naplózása
- Teljesítmény metrikák

### 2. Metrikák

- I/O műveletek száma
- Feldolgozott adatmennyiség
- Hibaarány

## Továbbfejlesztési lehetőségek

### 1. Új storage típusok

- S3Storage
- GCSStorage
- SQLStorage

### 2. További formátumok

- Parquet
- HDF5
- Feather

### 3. Optimalizációk

- Aszinkron műveletek
- Caching
- Párhuzamos feldolgozás
