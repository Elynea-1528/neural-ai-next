# StorageFactoryInterface

## Áttekintés

A `StorageFactoryInterface` egy absztrakt interfész, amely egy gyártó (factory) mintát definiál a különböző tárolási megoldások létrehozásához. Ez az interfész lehetővé teszi a tárolási implementációk dinamikus regisztrálását és példányosítását.

## Absztrakt Osztály

```python
class StorageFactoryInterface(ABC)
```

## Absztrakt Metódusok

### `register_storage()`

Új tárolási típus regisztrálása a factory számára.

```python
@classmethod
@abstractmethod
def register_storage(
    cls,
    storage_type: str,
    storage_class: type[StorageInterface]
) -> None
```

**Paraméterek:**
- `storage_type`: A tárolási típus egyedi azonosítója (pl. 'file', 's3')
- `storage_class`: A tárolási osztály, amely megvalósítja a StorageInterface-t

**Kivételek:**
- `NotImplementedError`: Ha az alosztály nem valósítja meg ezt a metódust

**Példa implementációra:**

```python
@classmethod
def register_storage(
    cls,
    storage_type: str,
    storage_class: type[StorageInterface]
) -> None:
    # Implementáció
    # 1. Validáció (interfész ellenőrzése)
    # 2. Regisztráció a belső szótárban
    # 3. Hibakezelés
    pass
```

### `get_storage()`

Tárolási példány létrehozása a megadott típus alapján.

```python
@classmethod
@abstractmethod
def get_storage(
    cls,
    storage_type: str = "file",
    base_path: str | Path | None = None,
    **kwargs: dict[str, object]
) -> StorageInterface
```

**Paraméterek:**
- `storage_type`: A kért tárolási típus azonosítója. Alapértelmezett: 'file'
- `base_path`: Az alap könyvtár útvonala a fájl alapú tároláshoz
- `**kwargs`: További, a tárolási implementáció specifikus paraméterek

**Visszatérési érték:**
- `StorageInterface`: Egy inicializált tárolási példány

**Kivételek:**
- `NotImplementedError`: Ha az alosztály nem valósítja meg ezt a metódust
- `KeyError`: Ha a megadott tárolási típus nincs regisztrálva
- `ValueError`: Ha a megadott paraméterek érvénytelenek

**Példa implementációra:**

```python
@classmethod
def get_storage(
    cls,
    storage_type: str = "file",
    base_path: str | Path | None = None,
    **kwargs: dict[str, object]
) -> StorageInterface:
    # Implementáció
    # 1. Típus ellenőrzése
    # 2. Osztály lekérése
    # 3. Példányosítás
    # 4. Visszaadás
    pass
```

## Implementáció Példa

### Teljes Implementáció

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
from neural_ai.core.storage.interfaces.factory_interface import StorageFactoryInterface

if TYPE_CHECKING:
    from neural_ai.core.utils.interfaces.hardware_interface import HardwareInterface

class StorageFactory(StorageFactoryInterface):
    """Factory osztály storage komponensek létrehozásához."""
    
    _storage_types: dict[str, type[StorageInterface]] = {
        "file": FileStorage,
    }
    
    @classmethod
    def register_storage(
        cls,
        storage_type: str,
        storage_class: type[StorageInterface]
    ) -> None:
        """Új tárolási típus regisztrálása a factory számára.
        
        Args:
            storage_type: A tárolási típus egyedi azonosítója (pl. "s3", "database")
            storage_class: A tárolási osztály, amely implementálja a StorageInterface-t
        
        Raises:
            ValueError: Ha a storage_class nem implementálja a StorageInterface-t
        """
        if not issubclass(storage_class, StorageInterface):
            raise ValueError(
                f"A(z) {storage_class} nem implementálja a StorageInterface-t"
            )
        cls._storage_types[storage_type] = storage_class
    
    @classmethod
    def get_storage(
        cls,
        storage_type: str = "file",
        base_path: str | Path | None = None,
        hardware: "HardwareInterface | None" = None,
        **kwargs: object
    ) -> StorageInterface:
        """Tárolási példány létrehozása a megadott típus alapján.
        
        Args:
            storage_type: A kért tárolási típus azonosítója (alapértelmezett: "file")
            base_path: Alap könyvtár útvonal a file alapú tároláshoz
            hardware: A hardverképességek detektálásáért felelős interfész (opcionális)
            **kwargs: További paraméterek a storage osztály konstruktorának
        
        Returns:
            StorageInterface: Az inicializált tárolási példány
        
        Raises:
            StorageError: Ha nem található a kért tárolási típus vagy a
                példányosítása sikertelen
        """
        if storage_type not in cls._storage_types:
            raise StorageError(
                f"Ismeretlen storage típus: {storage_type}. "
                f"Elérhető típusok: {list(cls._storage_types.keys())}"
            )
        
        storage_class = cls._storage_types[storage_type]
        
        # A base_path hozzáadása a kwargs-hoz, ha meg van adva
        if base_path is not None:
            kwargs["base_path"] = base_path
        
        # A hardware hozzáadása a kwargs-hoz, ha meg van adva
        if hardware is not None:
            kwargs["hardware"] = hardware
        
        try:
            storage = storage_class(**kwargs)
            return storage
        except TypeError as e:
            raise StorageError(
                f"Nem sikerült létrehozni a storage példányt: {str(e)}"
            ) from e
        except Exception as e:
            raise StorageError(
                f"Váratlan hiba történt a storage példányosítása közben: {str(e)}"
            ) from e
```

## Használat

### Alapvető Használat

```python
from neural_ai.core.storage import StorageFactory

# Alapértelmezett file storage létrehozása
storage = StorageFactory.get_storage("file", base_path="data")

# DataFrame mentése
import pandas as pd
df = pd.DataFrame({"col1": [1, 2, 3]})
storage.save_dataframe(df, "test.csv")
```

### Egyéni Tárolási Típus Regisztrálása

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.interfaces import StorageInterface
import pandas as pd

class S3Storage(StorageInterface):
    """S3 tárolási implementáció."""
    
    def __init__(self, bucket: str, region: str = "us-east-1"):
        self.bucket = bucket
        self.region = region
    
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs):
        # S3 implementáció
        pass
    
    def load_dataframe(self, path: str, **kwargs) -> pd.DataFrame:
        # S3 implementáció
        pass
    
    # További metódusok implementációja...

# Regisztrálás
StorageFactory.register_storage("s3", S3Storage)

# Használat
s3_storage = StorageFactory.get_storage("s3", bucket="my-bucket")
```

### Paraméterek Átadása

```python
from neural_ai.core.storage import StorageFactory

# File storage egyéni paraméterekkel
file_storage = StorageFactory.get_storage(
    "file",
    base_path="/custom/path",
    create_if_missing=True,
    auto_create_dirs=True
)

# Database storage paraméterekkel
db_storage = StorageFactory.get_storage(
    "database",
    host="localhost",
    port=5432,
    user="admin",
    password="secret"
)
```

## Bővíthetőség

### Új Tárolási Megoldások Hozzáadása

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.interfaces import StorageInterface
import pandas as pd
import boto3

class S3Storage(StorageInterface):
    """AWS S3 tárolási implementáció."""
    
    def __init__(self, bucket: str, region: str = "us-east-1", **kwargs):
        self.bucket = bucket
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region, **kwargs)
    
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs):
        import io
        buffer = io.BytesIO()
        df.to_parquet(buffer, **kwargs)
        buffer.seek(0)
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=buffer
        )
    
    def load_dataframe(self, path: str, **kwargs) -> pd.DataFrame:
        import io
        response = self.s3_client.get_object(Bucket=self.bucket, Key=path)
        buffer = io.BytesIO(response['Body'].read())
        return pd.read_parquet(buffer, **kwargs)
    
    # További metódusok...

# Regisztrálás
StorageFactory.register_storage("s3", S3Storage)

# Használat
s3_storage = StorageFactory.get_storage(
    "s3",
    bucket="my-data-bucket",
    region="eu-west-1"
)
```

### Cloud Storage Implementáció

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.interfaces import StorageInterface
import pandas as pd
from google.cloud import storage

class GCSStorage(StorageInterface):
    """Google Cloud Storage implementáció."""
    
    def __init__(self, bucket_name: str, project: str = None, **kwargs):
        self.bucket_name = bucket_name
        self.client = storage.Client(project=project, **kwargs)
        self.bucket = self.client.bucket(bucket_name)
    
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs):
        import io
        buffer = io.BytesIO()
        df.to_parquet(buffer, **kwargs)
        buffer.seek(0)
        blob = self.bucket.blob(path)
        blob.upload_from_file(buffer, rewind=True)
    
    def load_dataframe(self, path: str, **kwargs) -> pd.DataFrame:
        import io
        blob = self.bucket.blob(path)
        buffer = io.BytesIO()
        blob.download_to_file(buffer)
        buffer.seek(0)
        return pd.read_parquet(buffer, **kwargs)
    
    # További metódusok...

# Regisztrálás
StorageFactory.register_storage("gcs", GCSStorage)

# Használat
gcs_storage = StorageFactory.get_storage(
    "gcs",
    bucket_name="my-gcs-bucket",
    project="my-project"
)
```

## Hibakezelés

### Alapvető Hibakezelés

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.exceptions import StorageError

try:
    storage = StorageFactory.get_storage("unknown_type")
except StorageError as e:
    print(f"Storage hiba: {e}")
    # Kezeljük a hibát
```

### Reszilens Használat

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.exceptions import StorageError

def create_storage_with_fallback(storage_type: str, fallback_type: str = "file", **kwargs):
    """Storage létrehozása fallback-kel."""
    try:
        return StorageFactory.get_storage(storage_type, **kwargs)
    except StorageError:
        print(f"Warning: {storage_type} not available, using {fallback_type}")
        return StorageFactory.get_storage(fallback_type, **kwargs)

# Használat
storage = create_storage_with_fallback("s3", bucket="my-bucket")
```

## Tesztelés

### Mock Factory

```python
import unittest
from unittest.mock import Mock, patch
from neural_ai.core.storage import StorageFactory
from neural_ai.core.storage.interfaces import StorageInterface

class TestStorageFactory(unittest.TestCase):
    def setUp(self):
        # Mock storage osztály
        self.mock_storage_class = Mock(spec=StorageInterface)
        
    def test_register_and_get_storage(self):
        # Regisztráció
        StorageFactory.register_storage("test", self.mock_storage_class)
        
        # Lekérés
        storage = StorageFactory.get_storage("test")
        
        # Ellenőrzés
        self.assertIsInstance(storage, Mock)
        
    def test_get_unknown_storage_type(self):
        # Ismeretlen típus lekérése
        with self.assertRaises(StorageError):
            StorageFactory.get_storage("unknown")
```

## Best Practices

### 1. Interfész Ellenőrzés

```python
from neural_ai.core.storage.interfaces import StorageInterface

def register_custom_storage(storage_type: str, storage_class):
    """Biztonságos regisztráció interfész ellenőrzéssel."""
    if not issubclass(storage_class, StorageInterface):
        raise ValueError(f"{storage_class} must implement StorageInterface")
    
    StorageFactory.register_storage(storage_type, storage_class)
```

### 2. Paraméter Validáció

```python
from neural_ai.core.storage import StorageFactory
from pathlib import Path

def create_file_storage(base_path: str) -> StorageInterface:
    """File storage létrehozása validációval."""
    path = Path(base_path)
    
    if not path.exists():
        raise ValueError(f"Base path does not exist: {base_path}")
    
    if not path.is_dir():
        raise ValueError(f"Base path is not a directory: {base_path}")
    
    return StorageFactory.get_storage("file", base_path=base_path)
```

### 3. Konfigurációból Töltés

```python
from neural_ai.core.storage import StorageFactory
from neural_ai.core.config import ConfigManagerInterface

def create_storage_from_config(config: ConfigManagerInterface) -> StorageInterface:
    """Storage létrehozása konfigurációból."""
    storage_type = config.get("storage.type", default="file")
    base_path = config.get("storage.base_path", default=None)
    
    kwargs = {}
    if storage_type == "s3":
        kwargs["bucket"] = config.get("storage.s3.bucket")
        kwargs["region"] = config.get("storage.s3.region", default="us-east-1")
    elif storage_type == "database":
        kwargs["host"] = config.get("storage.database.host")
        kwargs["port"] = config.get("storage.database.port", default=5432)
        kwargs["user"] = config.get("storage.database.user")
        kwargs["password"] = config.get("storage.database.password")
    
    return StorageFactory.get_storage(storage_type, base_path=base_path, **kwargs)
```

## Implementációs Tippek

1. **Interfész implementáció**: Mindig ellenőrizzük, hogy a regisztrált osztály implementálja-e a StorageInterface-t
2. **Paraméterek átadása**: Gondoskodjunk a paraméterek helyes átadásáról a konstruktornak
3. **Hibakezelés**: Kezeljük a lehetséges kivételeket a példányosítás során
4. **Dinamikus regisztráció**: Lehetővé tegyük a tárolási típusok futási időben történő regisztrálását
5. **Bővíthetőség**: Tervezzük meg a factory-t úgy, hogy könnyen bővíthető legyen új tárolási típusokkal