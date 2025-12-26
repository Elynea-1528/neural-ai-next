# PandasBackend

## Áttekintés

A `PandasBackend` egy Pandas alapú tárolási backend, amely a FastParquet-et használja a DataFrame-ek tárolásához. Ez a backend kompatibilitási módban működik, és ideális régebbi CPU-khoz, ahol az AVX2 utasításkészlet nem elérhető.

## Osztály

```python
class PandasBackend(StorageBackend)
```

## Főbb Jellemzők

- **Lazy import**: A pandas és fastparquet csomagok csak akkor töltődnek be, amikor szükség van rájuk
- **FastParquet**: Hatékony Parquet tárolás
- **Chunkolás**: Nagy adathalmazok darabonkénti feldolgozása
- **Particionálás**: Dátum és szimbólum alapú particionálás
- **Kompatibilitás**: Működik régebbi hardveren is

## Attribútumok

- `name`: 'pandas'
- `supported_formats`: ['parquet']
- `is_async`: True

## Inicializálás

```python
def __init__(self) -> None
```

**Példa:**

```python
from neural_ai.core.storage.backends import PandasBackend

# Backend létrehozása
backend = PandasBackend()

print(f"Backend neve: {backend.name}")
print(f"Támogatott formátumok: {backend.supported_formats}")
print(f"Aszinkron támogatás: {backend.is_async}")
```

## Metódusok

### `write()`

DataFrame adatok írása Parquet formátumban FastParquet használatával.

```python
def write(
    self,
    data: Any,
    path: str,
    **kwargs: dict[str, Any]
) -> None
```

**Paraméterek:**
- `data`: A tárolandó Pandas DataFrame
- `path`: A cél elérési út (.parquet kiterjesztéssel)
- `**kwargs`: További konfigurációs paraméterek
  - `compression`: Tömörítési algoritmus (alapértelmezett: 'snappy')
  - `partition_by`: Particionálási oszlopok listája
  - `schema`: Adatséma definíció
  - `index`: Index mentése (alapértelmezett: False)

**Kivételek:**
- `ValueError`: Ha az adatok érvénytelenek vagy az elérési út hibás
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a tárolási művelet sikertelen

**Példák:**

```python
import pandas as pd
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Alapvető írás
df = pd.DataFrame({
    "timestamp": pd.date_range("2023-01-01", periods=100, freq="H"),
    "value": range(100),
    "category": ["A", "B", "C"] * 33 + ["A"]
})
backend.write(df, "data.parquet")

# Tömörített írás
backend.write(df, "data_compressed.parquet", compression="snappy")

# Particionált írás
df_with_partitions = df.copy()
df_with_partitions["year"] = df_with_partitions["timestamp"].dt.year
df_with_partitions["month"] = df_with_partitions["timestamp"].dt.month
backend.write(
    df_with_partitions,
    "partitioned_data.parquet",
    partition_by=["year", "month"]
)

# Index mentése
backend.write(df, "data_with_index.parquet", index=True)
```

### `read()`

DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

```python
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
- `pd.DataFrame`: A beolvasott Pandas DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

**Példák:**

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Alapvető olvasás
df = backend.read("data.parquet")

# Csak bizonyos oszlopok betöltése
df = backend.read("data.parquet", columns=["timestamp", "value"])

# Partíciók szűrése
df = backend.read(
    "partitioned_data.parquet",
    filters=[("year", "=", 2023), ("month", "=", 12)]
)

# Chunkoltan olvasás
df = backend.read("large_data.parquet", chunk_size=10000)
```

### `append()`

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

```python
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
  - `index`: Index mentése

**Kivételek:**
- `ValueError`: Ha az adatok sémája nem kompatibilis a meglévővel
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a hozzáfűzési művelet sikertelen

**Példák:**

```python
import pandas as pd
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Új adatok létrehozása
new_data = pd.DataFrame({
    "timestamp": pd.date_range("2023-01-02", periods=50, freq="H"),
    "value": range(100, 150),
    "category": ["D", "E", "F"] * 16 + ["D", "E"]
})

# Adatok hozzáfűzése
backend.append(new_data, "data.parquet")

# Sémavizsgálattal
backend.append(new_data, "data.parquet", schema_validation=True)
```

### `supports_format()`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

```python
def supports_format(self, format_name: str) -> bool
```

**Paraméterek:**
- `format_name`: A formátum neve (pl. 'parquet', 'csv')

**Visszatérési érték:**
- `bool`: True, ha a formátum támogatott, egyébként False

**Példa:**

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

print(f"Parquet támogatott: {backend.supports_format('parquet')}")
print(f"CSV támogatott: {backend.supports_format('csv')}")
```

### `get_info()`

Parquet fájl információinak lekérdezése.

```python
def get_info(self, path: str) -> dict[str, Any]
```

**Paraméterek:**
- `path`: Az elérési út

**Visszatérési érték:**
- `dict[str, Any]`: A fájl információit tartalmazó dictionary:
  - `size`: Fájlméret bájtban
  - `rows`: Sorok száma
  - `columns`: Oszlopok listája
  - `format`: 'parquet'
  - `created`: Létrehozás dátuma
  - `modified`: Módosítás dátuma
  - `num_row_groups`: Row group-ok száma
  - `compression`: Tömörítési algoritmus

**Kivételek:**
- `FileNotFoundError`: Ha a fájl nem található

**Példa:**

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Fájl információk lekérdezése
info = backend.get_info("data.parquet")

print(f"Fájlméret: {info['size']} bájt")
print(f"Sorok száma: {info['rows']}")
print(f"Oszlopok: {info['columns']}")
print(f"Tömörítés: {info['compression']}")
print(f"Row group-ok: {info['num_row_groups']}")
```

## Belső Metódusok

### `_ensure_initialized()`

Biztosítja, hogy a pandas csomag betöltődött.

```python
def _ensure_initialized(self) -> None
```

### `_write_partitioned()`

Particionált Parquet fájl írása.

```python
def _write_partitioned(
    self,
    df: Any,
    path: str,
    partition_by: list,
    compression: str,
    index: bool
) -> None
```

**Paraméterek:**
- `df`: A tárolandó DataFrame
- `path`: A cél elérési út
- `partition_by`: Particionálási oszlopok listája
- `compression`: Tömörítési algoritmus
- `index`: Index mentése

### `_read_chunked()`

Chunkoltan olvassa a Parquet fájlt.

```python
def _read_chunked(
    self,
    path: str,
    chunk_size: int,
    columns: list | None,
    filters: list | None
) -> Any
```

**Paraméterek:**
- `path`: A forrás elérési út
- `chunk_size`: Egy chunk mérete sorokban
- `columns`: Csak ezen oszlopok betöltése
- `filters`: Szűrők a partíciókra

**Visszatérési érték:**
- `pd.DataFrame`: Az összes chunkból összefűzött DataFrame

### `_validate_schema()`

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

```python
def _validate_schema(self, existing: Any, new: Any) -> bool
```

**Paraméterek:**
- `existing`: A meglévő DataFrame
- `new`: Az új DataFrame

**Visszatérési érték:**
- `bool`: True, ha a sémák kompatibilisek, egyébként False

## Komplex Példák

### Nagy Adathalmazok Feldolgozása

```python
import pandas as pd
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Nagy DataFrame létrehozása
large_df = pd.DataFrame({
    "id": range(1_000_000),
    "value": [i * 2 for i in range(1_000_000)],
    "category": [f"cat_{i % 100}" for i in range(1_000_000)]
})

# Írás tömörítéssel
print("Adatok írása...")
backend.write(large_df, "large_data.parquet", compression="snappy")

# Chunkoltan olvasás
print("Adatok olvasása chunkoltan...")
chunked_df = backend.read("large_data.parquet", chunk_size=50000)

# Chunkok feldolgozása
total_rows = 0
for chunk in [chunked_df]:  # Egyszerűsített példa
    total_rows += len(chunk)
    print(f"Feldolgozott chunk: {len(chunk)} sor")

print(f"Összesen feldolgozott sorok: {total_rows}")
```

### Particionált Adatok Kezelése

```python
import pandas as pd
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Tick adatok létrehozása
tick_data = pd.DataFrame({
    "timestamp": pd.date_range("2023-01-01", periods=10000, freq="1min"),
    "symbol": ["EURUSD"] * 5000 + ["GBPUSD"] * 5000,
    "bid": [1.0 + i * 0.0001 for i in range(10000)],
    "ask": [1.0002 + i * 0.0001 for i in range(10000)],
    "volume": [1000] * 10000
})

# Dátum oszlopok hozzáadása
tick_data["year"] = tick_data["timestamp"].dt.year
tick_data["month"] = tick_data["timestamp"].dt.month
tick_data["day"] = tick_data["timestamp"].dt.day

# Particionált mentés
print("Particionált adatok mentése...")
backend.write(
    tick_data,
    "tick_data.parquet",
    compression="snappy",
    partition_by=["year", "month", "day"]
)

# Partíciók szűrése
print("Adatok szűrése...")
filtered_data = backend.read(
    "tick_data.parquet",
    filters=[
        ("year", "=", 2023),
        ("month", "=", 1),
        ("day", "=", 1)
    ]
)

print(f"Szűrt adatok: {len(filtered_data)} sor")
```

### Adatok Hozzáfűzése és Frissítése

```python
import pandas as pd
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Kezdeti adatok
initial_data = pd.DataFrame({
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35]
})

# Mentés
backend.write(initial_data, "users.parquet")
print("Kezdeti adatok mentve")

# Új adatok hozzáadása
new_users = pd.DataFrame({
    "id": [4, 5],
    "name": ["David", "Eve"],
    "age": [28, 32]
})

# Hozzáfűzés sémavizsgálattal
backend.append(new_users, "users.parquet", schema_validation=True)
print("Új felhasználók hozzáadva")

# Összes adat betöltése
all_users = backend.read("users.parquet")
print(f"Összes felhasználó: {len(all_users)}")
print(all_users)
```

### Fájl Információk és Statisztikák

```python
from neural_ai.core.storage.backends import PandasBackend
import os

backend = PandasBackend()

# Több fájl információinak lekérdezése
files = ["data1.parquet", "data2.parquet", "data3.parquet"]

total_size = 0
total_rows = 0

for file in files:
    if os.path.exists(file):
        info = backend.get_info(file)
        total_size += info['size']
        total_rows += info['rows']
        
        print(f"\n{file}:")
        print(f"  Méret: {info['size'] / 1024 / 1024:.2f} MB")
        print(f"  Sorok: {info['rows']}")
        print(f"  Oszlopok: {len(info['columns'])}")
        print(f"  Tömörítés: {info['compression']}")

print(f"\nÖsszesített statisztikák:")
print(f"  Összes méret: {total_size / 1024 / 1024:.2f} MB")
print(f"  Összes sor: {total_rows}")
```

## Best Practices

### 1. Tömörítés Használata

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Snappy tömörítés (gyors, közepes tömörítés)
backend.write(data, "data_snappy.parquet", compression="snappy")

# Gzip tömörítés (lassabb, jobb tömörítés)
backend.write(data, "data_gzip.parquet", compression="gzip")
```

### 2. Index Kezelése

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Index mentése (ha szükséges)
backend.write(df_with_index, "data_with_index.parquet", index=True)

# Index nélküli mentés (ajánlott)
backend.write(df, "data.parquet", index=False)
```

### 3. Sémavizsgálat

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Hozzáfűzés sémavizsgálattal
backend.append(new_data, "existing_data.parquet", schema_validation=True)
```

### 4. Hibakezelés

```python
from neural_ai.core.storage.backends import PandasBackend
from neural_ai.core.storage.exceptions import StorageError

backend = PandasBackend()

try:
    # Adatok írása
    backend.write(data, "data.parquet")
    
    # Adatok olvasása
    loaded_data = backend.read("data.parquet")
    
except (ValueError, RuntimeError) as e:
    print(f"Hiba a backend művelet során: {e}")
    # Hibakezelés
```

## Teljesítmény Optimalizálás

### 1. Chunk Méret Beállítása

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Optimális chunk méret nagy adathalmazokhoz
chunked_data = backend.read("large_data.parquet", chunk_size=50000)
```

### 2. Oszlop Szűrés

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Csak szükséges oszlopok betöltése
essential_columns = ["timestamp", "value", "category"]
df = backend.read("data.parquet", columns=essential_columns)
```

### 3. Partíciók Használata

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Partíciók szűrése a gyors lekérdezéshez
filtered_data = backend.read(
    "partitioned_data.parquet",
    filters=[("year", "=", 2023), ("month", "=", 12)]
)
```

## Kompatibilitás

A PandasBackend a következő környezetekben működik:

- **CPU**: Minden x86_64 és ARM CPU
- **Operációs rendszer**: Linux, macOS, Windows
- **Python verzió**: 3.8+
- **Függőségek**: pandas, fastparquet

Ez a backend ideális választás, ha:
- Régebbi hardveren kell működnie
- Kompatibilitásra van szükség
- Stabil és jól ismert könyvtárat preferálunk
