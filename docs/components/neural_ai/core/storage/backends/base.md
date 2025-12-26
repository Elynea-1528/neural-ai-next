# StorageBackend

## Áttekintés

A `StorageBackend` egy absztrakt alaposztály a tárolási backend-ek számára. Ez az osztály definiálja a kötelező interfészt, amelyet minden tárolási backend implementációjának támogatnia kell. A backend-ek felelősek a DataFrame-ek tárolásáért, olvasásáért és hozzáfűzéséért különböző formátumokban (elsősorban Parquet).

## Absztrakt Osztály

```python
class StorageBackend(ABC)
```

## Attribútumok

### `name`
A backend neve (pl. 'polars', 'pandas')

### `supported_formats`
A támogatott fájlformátumok listája

### `is_async`
Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket

## Konstruktor

```python
def __init__(
    self,
    name: str,
    supported_formats: list[str],
    is_async: bool = True
)
```

**Paraméterek:**
- `name`: A backend egyedi neve
- `supported_formats`: A támogatott fájlformátumok listája
- `is_async`: Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket

**Példa:**

```python
class MyBackend(StorageBackend):
    def __init__(self):
        super().__init__(
            name="my_backend",
            supported_formats=["parquet", "csv"],
            is_async=True
        )
```

## Absztrakt Metódusok

### `write()`

DataFrame adatok írása a megadott elérési útra.

```python
@abstractmethod
def write(
    self,
    data: Any,
    path: str,
    **kwargs: dict[str, Any]
) -> None
```

**Paraméterek:**
- `data`: A tárolandó DataFrame
- `path`: A cél elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `compression`: Tömörítési algoritmus (pl. 'snappy', 'gzip')
  - `partition_by`: Particionálási oszlopok listája
  - `schema`: Adatséma definíció

**Kivételek:**
- `ValueError`: Ha az adatok érvénytelenek vagy az elérési út hibás
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a tárolási művelet sikertelen

**Példa implementációra:**

```python
def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
    # Implementáció
    # 1. Adatok validálása
    # 2. Elérési út ellenőrzése
    # 3. Tömörítés beállítása
    # 4. Particionálás (ha szükséges)
    # 5. Írás végrehajtása
    pass
```

### `read()`

DataFrame adatok olvasása a megadott elérési útról.

```python
@abstractmethod
def read(
    self,
    path: str,
    **kwargs: dict[str, Any]
) -> Any
```

**Paraméterek:**
- `path`: A forrás elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `columns`: Csak ezen oszlopok betöltése
  - `filters`: Szűrők a partíciókra (pl. [('year', '=', 2023)])
  - `chunk_size`: Chunk méret chunkolás esetén

**Visszatérési érték:**
- `Any`: A beolvasott DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

**Példa implementációra:**

```python
def read(self, path: str, **kwargs: dict[str, Any]) -> Any:
    # Implementáció
    # 1. Fájl létezésének ellenőrzése
    # 2. Formátum ellenőrzése
    # 3. Oszlopok szűrése (ha van)
    # 4. Partíciók szűrése (ha van)
    # 5. Chunkolás (ha kérték)
    # 6. DataFrame visszaadása
    pass
```

### `append()`

DataFrame adatok hozzáfűzése egy meglévő fájlhoz.

```python
@abstractmethod
def append(
    self,
    data: Any,
    path: str,
    **kwargs: dict[str, Any]
) -> None
```

**Paraméterek:**
- `data`: A hozzáfűzendő DataFrame
- `path`: A cél elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `compression`: Tömörítési algoritmus
  - `schema_validation`: Sémavizsgálat engedélyezése

**Kivételek:**
- `ValueError`: Ha az adatok sémája nem kompatibilis a meglévővel
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a hozzáfűzési művelet sikertelen

**Példa implementációra:**

```python
def append(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
    # Implementáció
    # 1. Adatok validálása
    # 2. Létező fájl ellenőrzése
    # 3. Sémavizsgálat (ha kérték)
    # 4. Adatok összefűzése
    # 5. Újraírás
    pass
```

### `supports_format()`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

```python
@abstractmethod
def supports_format(self, format_name: str) -> bool
```

**Paraméterek:**
- `format_name`: A formátum neve (pl. 'parquet', 'csv')

**Visszatérési érték:**
- `bool`: True, ha a formátum támogatott, egyébként False

**Példa implementációra:**

```python
def supports_format(self, format_name: str) -> bool:
    return format_name.lower() in self.supported_formats
```

### `get_info()`

Fájl információinak lekérdezése.

```python
@abstractmethod
def get_info(self, path: str) -> dict[str, Any]
```

**Paraméterek:**
- `path`: Az elérési út

**Visszatérési érték:**
- `dict[str, Any]`: A fájl információit tartalmazó dictionary:
  - `size`: Fájlméret bájtban
  - `rows`: Sorok száma
  - `columns`: Oszlopok listája
  - `format`: Fájlformátum
  - `created`: Létrehozás dátuma
  - `modified`: Módosítás dátuma

**Kivételek:**
- `FileNotFoundError`: Ha a fájl nem létezik

**Példa implementációra:**

```python
def get_info(self, path: str) -> dict[str, Any]:
    # Implementáció
    # 1. Fájl létezésének ellenőrzése
    # 2. Statisztikák lekérése
    # 3. Metaadatok összeállítása
    # 4. Szótár visszaadása
    pass
```

## Konkrét Metódusok

### `validate_data()`

DataFrame érvényességének ellenőrzése.

```python
def validate_data(self, data: Any) -> bool
```

**Paraméterek:**
- `data`: Az ellenőrizendő DataFrame

**Visszatérési érték:**
- `bool`: True, ha a DataFrame érvényes, egyébként False

**Példa:**

```python
backend = MyBackend()
df = pd.DataFrame({"col1": [1, 2, 3]})

if backend.validate_data(df):
    backend.write(df, "data.parquet")
else:
    raise ValueError("Érvénytelen DataFrame")
```

### `__repr__()`

A backend szöveges reprezentációja.

```python
def __repr__(self) -> str
```

**Visszatérési érték:**
- `str`: A backend szöveges reprezentációja

**Példa:**

```python
backend = MyBackend()
print(backend)
# Kimenet: MyBackend(name='my_backend', formats=['parquet'], async=True)
```

## Implementáció Példa

### Teljes Implementáció

```python
from abc import ABC, abstractmethod
from typing import Any
from neural_ai.core.storage.backends.base import StorageBackend

class CustomBackend(StorageBackend):
    """Egyéni tárolási backend implementáció."""
    
    def __init__(self):
        super().__init__(
            name="custom",
            supported_formats=["parquet", "csv"],
            is_async=True
        )
        self._initialized = False
    
    def _ensure_initialized(self):
        """Biztosítja, hogy a szükséges csomagok betöltődtek."""
        if not self._initialized:
            # Lazy import
            import some_library
            self._library = some_library
            self._initialized = True
    
    def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok írása."""
        self._ensure_initialized()
        
        try:
            # Ellenőrzések
            if not self.validate_data(data):
                raise ValueError("Érvénytelen DataFrame adatok")
            
            # Konfiguráció
            compression = kwargs.get("compression", "snappy")
            
            # Írás
            self._library.write_parquet(data, path, compression=compression)
            
        except Exception as e:
            raise RuntimeError(f"A tárolási művelet sikertelen: {str(e)}") from e
    
    def read(self, path: str, **kwargs: dict[str, Any]) -> Any:
        """DataFrame adatok olvasása."""
        self._ensure_initialized()
        
        try:
            # Konfiguráció
            columns = kwargs.get("columns", None)
            filters = kwargs.get("filters", None)
            
            # Olvasás
            df = self._library.read_parquet(
                path,
                columns=columns,
                filters=filters
            )
            
            return df
            
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az olvasási művelet sikertelen: {str(e)}") from e
    
    def append(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None:
        """DataFrame adatok hozzáfűzése."""
        self._ensure_initialized()
        
        try:
            # Ellenőrzések
            if not self.validate_data(data):
                raise ValueError("Érvénytelen DataFrame adatok")
            
            # Ha a fájl létezik, olvassuk ki
            if os.path.exists(path):
                existing_data = self.read(path)
                
                # Sémavizsgálat
                if kwargs.get("schema_validation", False):
                    if not self._validate_schema(existing_data, data):
                        raise ValueError("Az adatok sémája nem kompatibilis")
                
                # Összefűzés
                combined_data = self._library.concat([existing_data, data])
            else:
                combined_data = data
            
            # Újraírás
            self.write(combined_data, path, **kwargs)
            
        except (ValueError, FileNotFoundError):
            raise
        except Exception as e:
            raise RuntimeError(f"A hozzáfűzési művelet sikertelen: {str(e)}") from e
    
    def supports_format(self, format_name: str) -> bool:
        """Formátum támogatás ellenőrzése."""
        return format_name.lower() in self.supported_formats
    
    def get_info(self, path: str) -> dict[str, Any]:
        """Fájl információinak lekérdezése."""
        self._ensure_initialized()
        
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"A fájl nem található: {path}")
            
            # Statisztikák
            stat = os.stat(path)
            
            # Metaadatok
            metadata = self._library.read_metadata(path)
            
            return {
                "size": stat.st_size,
                "rows": metadata.num_rows,
                "columns": list(metadata.schema.names),
                "format": "parquet",
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
            }
            
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Az információ lekérdezése sikertelen: {str(e)}") from e
    
    def _validate_schema(self, existing: Any, new: Any) -> bool:
        """Séma kompatibilitás ellenőrzése."""
        try:
            existing_cols = set(existing.columns)
            new_cols = set(new.columns)
            return existing_cols.issubset(new_cols)
        except Exception:
            return False
```

## Használat

### Alapvető Használat

```python
from neural_ai.core.storage.backends.base import StorageBackend
import pandas as pd

# Backend létrehozása
backend = CustomBackend()

# Adatok írása
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
backend.write(df, "data.parquet", compression="snappy")

# Adatok olvasása
loaded_df = backend.read("data.parquet")

# Adatok hozzáfűzése
new_data = pd.DataFrame({"col1": [4, 5], "col2": ["d", "e"]})
backend.append(new_data, "data.parquet")

# Fájl információk
info = backend.get_info("data.parquet")
print(f"Méret: {info['size']} bájt")
print(f"Sorok: {info['rows']}")
print(f"Oszlopok: {info['columns']}")
```

### Formátum Ellenőrzés

```python
from neural_ai.core.storage.backends.base import StorageBackend

backend = CustomBackend()

# Formátum támogatás ellenőrzése
print(f"Parquet támogatott: {backend.supports_format('parquet')}")
print(f"CSV támogatott: {backend.supports_format('csv')}")
print(f"JSON támogatott: {backend.supports_format('json')}")
```

### Adatok Validálása

```python
from neural_ai.core.storage.backends.base import StorageBackend
import pandas as pd

backend = CustomBackend()

# Érvényes DataFrame
valid_df = pd.DataFrame({"col1": [1, 2, 3]})
print(f"Érvényes adatok: {backend.validate_data(valid_df)}")

# Érvénytelen DataFrame
invalid_df = None
print(f"Érvénytelen adatok: {backend.validate_data(invalid_df)}")

# Üres DataFrame
empty_df = pd.DataFrame()
print(f"Üres adatok: {backend.validate_data(empty_df)}")
```

## Best Practices

### 1. Lazy Import

```python
class EfficientBackend(StorageBackend):
    def __init__(self):
        super().__init__("efficient", ["parquet"], True)
        self._library = None
    
    def _ensure_initialized(self):
        if self._library is None:
            # Csak akkor töltődik be, ha valóban használjuk
            import heavy_library
            self._library = heavy_library
```

### 2. Hibakezelés

```python
from neural_ai.core.storage.backends.base import StorageBackend

class SafeBackend(StorageBackend):
    def write(self, data, path, **kwargs):
        try:
            # Validáció
            if not self.validate_data(data):
                raise ValueError("Érvénytelen adatok")
            
            # Művelet
            self._write_internal(data, path, **kwargs)
            
        except ValueError:
            raise
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Írási hiba: {str(e)}") from e
```

### 3. Sémavizsgálat

```python
from neural_ai.core.storage.backends.base import StorageBackend

class SchemaValidationBackend(StorageBackend):
    def append(self, data, path, **kwargs):
        # Sémavizsgálat engedélyezése
        if kwargs.get("schema_validation", False):
            if not self._validate_schema(existing_data, data):
                raise ValueError("Séma inkompatibilitás")
        
        # Hozzáfűzés
        super().append(data, path, **kwargs)
```

## Implementációs Tippek

1. **Absztrakt metódusok**: Minden absztrakt metódust implementáljunk
2. **Validáció**: Használjuk a `validate_data()` metódust
3. **Hibakezelés**: Kezeljük a lehetséges kivételeket
4. **Lazy import**: Használjunk lazy importot a nehéz csomagokhoz
5. **Dokumentáció**: Dokumentáljuk a paramétereket és visszatérési értékeket
6. **Tesztelés**: Írjunk teszteket az implementációhoz