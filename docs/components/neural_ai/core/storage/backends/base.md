# StorageBackend Absztrakt Osztály

## Áttekintés

A `StorageBackend` egy absztrakt alaposztály, amely definiálja a kötelező interfészt minden tárolási backend implementációhoz a Neural AI Next rendszerben. Ez az osztály biztosítja a konzisztenciát a különböző DataFrame könyvtárak (Polars, Pandas) implementációi között.

## Osztálydefiníció

```python
class StorageBackend(ABC):
    """Absztrakt alaposztály a tárolási backend-ek számára."""
    
    def __init__(self, name: str, supported_formats: list[str], is_async: bool = True):
        """Inicializálja a StorageBackend példányt."""
        self.name: str = name
        self.supported_formats: list[str] = supported_formats
        self.is_async: bool = is_async
```

## Attribútumok

### `name: str`
A backend egyedi neve (pl. 'polars', 'pandas').

### `supported_formats: list[str]`
A támogatott fájlformátumok listája (pl. ['parquet']).

### `is_async: bool`
Logikai érték, amely jelzi, hogy a backend támogatja-e az aszinkron műveleteket.

## Absztrakt Metódusok

### `write(data: DataFrameType, path: str, **kwargs) -> None`

DataFrame adatok írása a megadott elérési útra.

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

### `read(path: str, **kwargs) -> DataFrameType`

DataFrame adatok olvasása a megadott elérési útról.

**Paraméterek:**
- `path`: A forrás elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `columns`: Csak ezen oszlopok betöltése
  - `filters`: Szűrők a partíciókra (pl. [('year', '=', 2023)])
  - `chunk_size`: Chunk méret chunkolás esetén

**Visszatérési érték:**
A beolvasott DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

### `append(data: DataFrameType, path: str, **kwargs) -> None`

DataFrame adatok hozzáfűzése egy meglévő fájlhoz.

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

### `supports_format(format_name: str) -> bool`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

**Paraméterek:**
- `format_name`: A formátum neve (pl. 'parquet', 'csv')

**Visszatérési érték:**
True, ha a formátum támogatott, egyébként False

### `get_info(path: str) -> Dict[str, Any]`

Fájl információinak lekérdezése.

**Paraméterek:**
- `path`: Az elérési út

**Visszatérési érték:**
A fájl információit tartalmazó dictionary:
- `size`: Fájlméret bájtban
- `rows`: Sorok száma
- `columns`: Oszlopok listája
- `format`: Fájlformátum
- `created`: Létrehozás dátuma
- `modified`: Módosítás dátuma

**Kivételek:**
- `FileNotFoundError`: Ha a fájl nem létezik

## Konkrét Metódusok

### `validate_data(data: DataFrameType) -> bool`

DataFrame érvényességének ellenőrzése.

**Paraméterek:**
- `data`: Az ellenőrizendő DataFrame

**Visszatérési érték:**
True, ha a DataFrame érvényes, egyébként False

**Implementáció:**
```python
def validate_data(self, data: DataFrameType) -> bool:
    try:
        return len(data) >= 0 and len(data.columns()) > 0
    except Exception:
        return False
```

### `__repr__() -> str`

A backend szöveges reprezentációja.

**Visszatérési érték:**
A backend leíró string (pl. "PolarsBackend(name='polars', formats=['parquet'], async=True)")

## DataFrameType Protokoll

A backend-ek egy közös `DataFrameType` protokollt használnak a típusbiztosság érdekében:

```python
class DataFrameType(Protocol):
    """DataFrame protokoll, amely definiálja a kötelező DataFrame műveleteket."""
    
    def __len__(self) -> int:
        """DataFrame hosszának lekérdezése."""
        ...
    
    def columns(self) -> list[str]:
        """Oszlopok lekérdezése."""
        ...
    
    def shape(self) -> tuple[int, int]:
        """DataFrame alakjának lekérdezése."""
        ...
```

## Használati Példák

### Alapvető Használat

```python
from neural_ai.core.storage.backends import StorageBackend, PolarsBackend

# Backend példányosítása
backend: StorageBackend = PolarsBackend()

# Adatok írása
data = get_data()  # Valamilyen DataFrame
backend.write(data, "path/to/file.parquet")

# Adatok olvasása
loaded_data = backend.read("path/to/file.parquet")

# Adatok hozzáfűzése
new_data = get_new_data()
backend.append(new_data, "path/to/file.parquet")

# Fájl információk lekérdezése
info = backend.get_info("path/to/file.parquet")
print(f"File size: {info['size']} bytes")
print(f"Rows: {info['rows']}")
```

### Konfigurációs Opciók

```python
# Tömörítés beállítása
backend.write(data, path, compression="snappy")

# Particionálás
backend.write(data, path, partition_by=["year", "month", "symbol"])

# Oszlopok szűrése olvasáskor
data = backend.read(path, columns=["timestamp", "bid", "ask"])

# Partíciók szűrése
filters = [("year", "=", 2023), ("month", "=", 12)]
data = backend.read(path, filters=filters)

# Chunkolás
data = backend.read(path, chunk_size=10000)
```

### Formátum Támogatás Ellenőrzése

```python
# Ellenőrzés
if backend.supports_format("parquet"):
    print("Parquet formátum támogatott")
else:
    print("Parquet formátum nem támogatott")
```

## Fejlesztés

### Új Backend Implementálása

1. Hozz létre egy új osztályt, amely a `StorageBackend`-ből származik
2. Implementáld az összes absztrakt metódust
3. Használj lazy importot a nehéz könyvtárakhoz
4. Add hozzá az osztályt a `__init__.py`-hoz

**Példa:**

```python
from neural_ai.core.storage.backends.base import StorageBackend, DataFrameType
from typing import Any, Dict

class CustomBackend(StorageBackend):
    """Egyéni tárolási backend implementáció."""
    
    def __init__(self):
        super().__init__(name="custom", supported_formats=["parquet"])
        self._wrapper = None
    
    def _ensure_initialized(self):
        """Lazy import a könyvtárak számára."""
        if self._wrapper is None:
            import custom_library
            self._wrapper = custom_library
    
    def write(self, data: DataFrameType, path: str, **kwargs: Dict[str, Any]) -> None:
        self._ensure_initialized()
        # Implementáció
        pass
    
    def read(self, path: str, **kwargs: Dict[str, Any]) -> DataFrameType:
        self._ensure_initialized()
        # Implementáció
        pass
    
    def append(self, data: DataFrameType, path: str, **kwargs: Dict[str, Any]) -> None:
        self._ensure_initialized()
        # Implementáció
        pass
    
    def supports_format(self, format_name: str) -> bool:
        return format_name.lower() in self.supported_formats
    
    def get_info(self, path: str) -> Dict[str, Any]:
        self._ensure_initialized()
        # Implementáció
        pass
```

## Kapcsolódó Dokumentumok

- [Storage Backends Áttekintés](__init__.md)
- [Polars Backend](polars_backend.md)
- [Pandas Backend](pandas_backend.md)
- [Parquet Storage](../parquet.md)

## Jegyzetek

- A `StorageBackend` egy absztrakt osztály, nem példányosítható közvetlenül
- Minden leszármazott osztálynak implementálnia kell az összes absztrakt metódust
- A lazy import használata kötelező a nehéz könyvtárak esetén
- A `DataFrameType` protokoll biztosítja a típusbiztosságot különböző DataFrame implementációk esetén