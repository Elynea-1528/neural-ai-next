# StorageInterface

## Áttekintés

A `StorageInterface` egy absztrakt interfész, amely definiálja a tárolási műveletek alapvető viselkedését. Minden konkrét tárolási implementációnak ezt az interfészt kell implementálnia.

## Absztrakt Osztály

```python
class StorageInterface(ABC)
```

## Absztrakt Metódusok

### `save_dataframe()`

DataFrame mentése a megadott útvonalra.

```python
@abstractmethod
def save_dataframe(
    self,
    df: pd.DataFrame,
    path: str,
    **kwargs: Mapping[str, Any]
) -> None
```

**Paraméterek:**
- `df`: A mentendő pandas DataFrame
- `path`: A célfájl elérési útja
- `**kwargs`: További formázási és mentési opciók

**Kivételek:**
- `StorageIOError`: Ha I/O hiba történik a mentés során
- `StorageFormatError`: Ha a kért formátum nem támogatott
- `StorageSerializationError`: Ha az adatok nem szerializálhatók

**Példa implementációra:**

```python
def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]) -> None:
    # Implementáció
    # 1. Ellenőrzések (formátum, jogosultságok)
    # 2. Adatok szerializálása
    # 3. Fájl írása
    # 4. Hibakezelés
    pass
```

### `load_dataframe()`

DataFrame betöltése a megadott útvonalról.

```python
@abstractmethod
def load_dataframe(
    self,
    path: str,
    **kwargs: Mapping[str, Any]
) -> pd.DataFrame
```

**Paraméterek:**
- `path`: A forrásfájl elérési útja
- `**kwargs`: További betöltési és formázási opciók

**Visszatérési érték:**
- `pd.DataFrame`: A betöltött pandas DataFrame

**Kivételek:**
- `StorageNotFoundError`: Ha a forrásfájl nem található
- `StorageFormatError`: Ha a fájl formátuma nem támogatott
- `StorageSerializationError`: Ha az adatok nem deszerializálhatók
- `StorageIOError`: Ha I/O hiba történik a betöltés során

**Példa implementációra:**

```python
def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
    # Implementáció
    # 1. Fájl létezésének ellenőrzése
    # 2. Formátum ellenőrzése
    # 3. Adatok betöltése
    # 4. Deszerializálás
    # 5. DataFrame visszaadása
    pass
```

### `save_object()`

Objektum mentése a megadott útvonalra.

```python
@abstractmethod
def save_object(
    self,
    obj: object,
    path: str,
    **kwargs: Mapping[str, Any]
) -> None
```

**Paraméterek:**
- `obj`: A mentendő objektum
- `path`: A célfájl elérési útja
- `**kwargs`: További szerializációs opciók

**Kivételek:**
- `StorageIOError`: Ha I/O hiba történik a mentés során
- `StorageFormatError`: Ha a kért formátum nem támogatott
- `StorageSerializationError`: Ha az objektum nem szerializálható

**Példa implementációra:**

```python
def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
    # Implementáció
    # 1. Objektum szerializálása
    # 2. Formátum ellenőrzése
    # 3. Fájl írása
    # 4. Hibakezelés
    pass
```

### `load_object()`

Objektum betöltése a megadott útvonalról.

```python
@abstractmethod
def load_object(
    self,
    path: str,
    **kwargs: Mapping[str, Any]
) -> object
```

**Paraméterek:**
- `path`: A forrásfájl elérési útja
- `**kwargs`: További deszerializációs opciók

**Visszatérési érték:**
- `object`: A betöltött objektum

**Kivételek:**
- `StorageNotFoundError`: Ha a forrásfájl nem található
- `StorageFormatError`: Ha a fájl formátuma nem támogatott
- `StorageSerializationError`: Ha az objektum nem deszerializálható
- `StorageIOError`: Ha I/O hiba történik a betöltés során

**Példa implementációra:**

```python
def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
    # Implementáció
    # 1. Fájl létezésének ellenőrzése
    # 2. Adatok betöltése
    # 3. Deszerializálás
    # 4. Objektum visszaadása
    pass
```

### `exists()`

Ellenőrzi, hogy az útvonal létezik-e.

```python
@abstractmethod
def exists(self, path: str) -> bool
```

**Paraméterek:**
- `path`: Az ellenőrizendő útvonal

**Visszatérési érték:**
- `bool`: True, ha az útvonal létezik, egyébként False

**Példa implementációra:**

```python
def exists(self, path: str) -> bool:
    # Implementáció
    # 1. Útvonal ellenőrzése
    # 2. Létezés visszaadása
    pass
```

### `get_metadata()`

Fájl vagy könyvtár metaadatainak lekérdezése.

```python
@abstractmethod
def get_metadata(self, path: str) -> dict[str, Any]
```

**Paraméterek:**
- `path`: A cél útvonal

**Visszatérési érték:**
- `dict[str, Any]`: A metaadatok szótárba rendezve

**Kivételek:**
- `StorageNotFoundError`: Ha az útvonal nem található
- `StorageIOError`: Ha a metaadatok lekérdezése sikertelen

**Példa implementációra:**

```python
def get_metadata(self, path: str) -> dict[str, Any]:
    # Implementáció
    # 1. Fájl statisztikák lekérése
    # 2. Metaadatok összeállítása
    # 3. Szótár visszaadása
    pass
```

### `delete()`

Fájl vagy könyvtár törlése.

```python
@abstractmethod
def delete(self, path: str) -> None
```

**Paraméterek:**
- `path`: A törlendő útvonal

**Kivételek:**
- `StorageNotFoundError`: Ha az útvonal nem található
- `StorageIOError`: Ha a törlés sikertelen

**Példa implementációra:**

```python
def delete(self, path: str) -> None:
    # Implementáció
    # 1. Fájl létezésének ellenőrzése
    # 2. Törlés végrehajtása
    # 3. Hibakezelés
    pass
```

### `list_dir()`

Könyvtár tartalmának listázása.

```python
@abstractmethod
def list_dir(
    self,
    path: str,
    pattern: str | None = None
) -> Sequence[Path]
```

**Paraméterek:**
- `path`: A könyvtár elérési útja
- `pattern`: Opcionális glob minta a fájlnevek szűrésére

**Visszatérési érték:**
- `Sequence[Path]`: A könyvtárban található elemek Path objektumokként

**Kivételek:**
- `StorageNotFoundError`: Ha a könyvtár nem található
- `StorageIOError`: Ha a listázás sikertelen

**Példa implementációra:**

```python
def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]:
    # Implementáció
    # 1. Könyvtár létezésének ellenőrzése
    # 2. Tartalom listázása
    # 3. Szűrés (ha van pattern)
    # 4. Path objektumok visszaadása
    pass
```

## Implementáció Példa

### Teljes Implementáció

```python
from abc import ABC, abstractmethod
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any
import pandas as pd
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

class FileSystemStorage(StorageInterface):
    """Fájlrendszer alapú tárolási implementáció."""
    
    def __init__(self, base_path: str = "/data"):
        self.base_path = Path(base_path)
    
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs: Mapping[str, Any]) -> None:
        """DataFrame mentése."""
        full_path = self.base_path / path
        
        # Formátum meghatározása
        fmt = kwargs.get('format', path.split('.')[-1])
        
        if fmt == 'csv':
            df.to_csv(full_path, **kwargs)
        elif fmt == 'parquet':
            df.to_parquet(full_path, **kwargs)
        else:
            raise StorageFormatError(f"Unsupported format: {fmt}")
    
    def load_dataframe(self, path: str, **kwargs: Mapping[str, Any]) -> pd.DataFrame:
        """DataFrame betöltése."""
        full_path = self.base_path / path
        
        if not full_path.exists():
            raise StorageNotFoundError(f"File not found: {path}")
        
        fmt = kwargs.get('format', path.split('.')[-1])
        
        if fmt == 'csv':
            return pd.read_csv(full_path, **kwargs)
        elif fmt == 'parquet':
            return pd.read_parquet(full_path, **kwargs)
        else:
            raise StorageFormatError(f"Unsupported format: {fmt}")
    
    def save_object(self, obj: object, path: str, **kwargs: Mapping[str, Any]) -> None:
        """Objektum mentése."""
        import json
        full_path = self.base_path / path
        
        with open(full_path, 'w') as f:
            json.dump(obj, f, **kwargs)
    
    def load_object(self, path: str, **kwargs: Mapping[str, Any]) -> object:
        """Objektum betöltése."""
        import json
        full_path = self.base_path / path
        
        if not full_path.exists():
            raise StorageNotFoundError(f"File not found: {path}")
        
        with open(full_path, 'r') as f:
            return json.load(f, **kwargs)
    
    def exists(self, path: str) -> bool:
        """Ellenőrzi az útvonal létezését."""
        return (self.base_path / path).exists()
    
    def get_metadata(self, path: str) -> dict[str, Any]:
        """Metaadatok lekérdezése."""
        full_path = self.base_path / path
        
        if not full_path.exists():
            raise StorageNotFoundError(f"File not found: {path}")
        
        stat = full_path.stat()
        return {
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_file': full_path.is_file(),
            'is_dir': full_path.is_dir()
        }
    
    def delete(self, path: str) -> None:
        """Fájl törlése."""
        full_path = self.base_path / path
        
        if not full_path.exists():
            raise StorageNotFoundError(f"File not found: {path}")
        
        full_path.unlink()
    
    def list_dir(self, path: str, pattern: str | None = None) -> Sequence[Path]:
        """Könyvtár tartalmának listázása."""
        full_path = self.base_path / path
        
        if not full_path.exists():
            raise StorageNotFoundError(f"Directory not found: {path}")
        
        if not full_path.is_dir():
            raise StorageIOError(f"Not a directory: {path}")
        
        if pattern:
            return list(full_path.glob(pattern))
        else:
            return list(full_path.iterdir())
```

### Használat

```python
# Storage létrehozása
storage = FileSystemStorage(base_path="/data")

# DataFrame mentése
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
storage.save_dataframe(df, "test.csv")

# DataFrame betöltése
loaded_df = storage.load_dataframe("test.csv")

# Objektum mentése
config = {"key": "value"}
storage.save_object(config, "config.json")

# Objektum betöltése
loaded_config = storage.load_object("config.json")

# Metaadatok lekérdezése
metadata = storage.get_metadata("test.csv")
print(f"File size: {metadata['size']} bytes")

# Könyvtár listázása
files = storage.list_dir(".", pattern="*.csv")
for file in files:
    print(file)
```

## Best Practices

### 1. Hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageNotFoundError,
    StorageIOError
)

def safe_save(storage: StorageInterface, data, path: str):
    try:
        if isinstance(data, pd.DataFrame):
            storage.save_dataframe(data, path)
        else:
            storage.save_object(data, path)
    except StorageNotFoundError:
        # Kezeljük a nem létező útvonalat
        storage.save_object(data, path + ".backup")
    except StorageIOError as e:
        # Naplózzuk az IO hibát
        logger.error(f"IO error: {e}")
        raise
    except StorageError as e:
        # Általános storage hiba
        logger.error(f"Storage error: {e}")
        raise
```

### 2. Típusjelzés

```python
from typing import Protocol
from neural_ai.core.storage.interfaces import StorageInterface

class DataProcessor:
    def __init__(self, storage: StorageInterface):
        self.storage = storage
    
    def process_and_save(self, data: pd.DataFrame, path: str):
        # Feldolgozás
        processed_data = self.process(data)
        
        # Mentés
        self.storage.save_dataframe(processed_data, path)
    
    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        # Feldolgozási logika
        pass
```

### 3. Tesztelés

```python
import unittest
from unittest.mock import Mock, patch
from neural_ai.core.storage.interfaces import StorageInterface

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.mock_storage = Mock(spec=StorageInterface)
        self.processor = DataProcessor(self.mock_storage)
    
    def test_process_and_save(self):
        # Tesztadatok
        test_data = pd.DataFrame({"col": [1, 2, 3]})
        
        # Metódus hívása
        self.processor.process_and_save(test_data, "test.csv")
        
        # Ellenőrzés
        self.mock_storage.save_dataframe.assert_called_once()
```

## Implementációs Tippek

1. **Kötelező metódusok**: Minden absztrakt metódust implementáljunk
2. **Hibakezelés**: Kezeljük a lehetséges kivételeket
3. **Dokumentáció**: Dokumentáljuk a paramétereket és visszatérési értékeket
4. **Típusjelzés**: Használjunk pontos típusjelzéseket
5. **Tesztelés**: Írjunk teszteket az implementációhoz