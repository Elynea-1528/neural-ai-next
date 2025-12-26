# Storage Backends

## Áttekintés

Ez a modul tartalmazza a tárolási backend-ek implementációit különböző DataFrame könyvtárakhoz (Polars, Pandas). A backend-ek a Parquet formátumot használják a hatékony adattároláshoz és támogatják a chunkolást és aszinkron műveleteket.

## Elérhető Backend-ek

### [`StorageBackend`](base.md)
Absztrakt alaposztály a tárolási backend-ek számára

### [`PandasBackend`](pandas_backend.md)
Pandas alapú tárolási backend FastParquet formátumhoz

### [`PolarsBackend`](polars_backend.md)
Polars alapú tárolási backend Parquet formátumhoz

## Típusok

### `DataFrameType`

```python
DataFrameType: TypeAlias = Any
```

A támogatott DataFrame típusok aliasa (Polars vagy Pandas).

## Backend Kiválasztás

### Hardver Alapú Automatikus Kiválasztás

A rendszer automatikusan kiválasztja a legoptimálisabb backend-et a hardver képességek alapján:

- **PolarsBackend**: Ha az AVX2 utasításkészlet elérhető (gyorsabb feldolgozás)
- **PandasBackend**: Ha az AVX2 nem elérhető (kompatibilitási mód)

### Kézi Választás

```python
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

# Kézi backend kiválasztás
if hardware.has_avx2():
    backend = PolarsBackend()
else:
    backend = PandasBackend()
```

## Támogatott Formátumok

### Parquet
- **Tömörítés**: Snappy, Gzip
- **Particionálás**: Dátum, szimbólum alapú
- **Chunkolás**: Nagy adathalmazok hatékony kezelése

## Használat

### Alapvető Használat

```python
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend
import pandas as pd

# Backend létrehozása
backend = PandasBackend()

# DataFrame írása
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
backend.write(df, "data.parquet", compression="snappy")

# DataFrame olvasása
loaded_df = backend.read("data.parquet")
```

### Backend Váltás

```python
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

# Polars backend (ajánlott)
polars_backend = PolarsBackend()
polars_backend.write(data, "data.parquet")

# Pandas backend (kompatibilitás)
pandas_backend = PandasBackend()
pandas_backend.write(data, "data.parquet")
```

### Particionált Tárolás

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Particionált írás
backend.write(
    df,
    "partitioned_data.parquet",
    compression="snappy",
    partition_by=["year", "month"]
)

# Particionált olvasás
df = backend.read(
    "partitioned_data.parquet",
    filters=[("year", "=", 2023), ("month", "=", 12)]
)
```

### Chunkolás

```python
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Nagy fájl chunkoltan történő olvasása
df = backend.read(
    "large_data.parquet",
    chunk_size=10000  # 10k sor per chunk
)

# Chunkok feldolgozása
for chunk in df:
    process_chunk(chunk)
```

## Teljesítmény Összehasonlítás

### PolarsBackend
- **Előnyök**:
  - Gyorsabb feldolgozás (AVX2 támogatás)
  - Jobb memóriakezelés
  - Párhuzamos feldolgozás
- **Használati eset**: Nagy adathalmazok, gyors lekérdezések

### PandasBackend
- **Előnyök**:
  - Kompatibilis régebbi hardverrel
  - Stabil működés
  - Széleskörű támogatás
- **Használati eset**: Kompatibilitás, kisebb adathalmazok

## Metódusok Összehasonlítása

### `write()`

```python
# PolarsBackend
polars_backend.write(
    data,
    path,
    compression="snappy",
    partition_by=["year", "month"]
)

# PandasBackend
pandas_backend.write(
    data,
    path,
    compression="snappy",
    partition_by=["year", "month"],
    index=False
)
```

### `read()`

```python
# PolarsBackend
df = polars_backend.read(
    path,
    columns=["col1", "col2"],
    filters=[("year", "=", 2023)],
    chunk_size=10000
)

# PandasBackend
df = pandas_backend.read(
    path,
    columns=["col1", "col2"],
    filters=[("year", "=", 2023)],
    chunk_size=10000
)
```

### `append()`

```python
# Mindkét backend hasonlóan működik
backend.append(new_data, "existing_data.parquet")
```

## Komplex Példák

### Adatok Migrálása Backend-ek Között

```python
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

def migrate_data(source_path: str, target_path: str):
    """Adatok migrálása Pandas-ról Polars backend-re."""
    
    # Forrás backend (Pandas)
    source_backend = PandasBackend()
    
    # Adatok betöltése
    data = source_backend.read(source_path)
    
    # Cél backend (Polars)
    target_backend = PolarsBackend()
    
    # Adatok mentése új backend-el
    target_backend.write(data, target_path, compression="snappy")
    
    print(f"Adatok migrálva: {source_path} -> {target_path}")
```

### Több Backend Használata Párhuzamosan

```python
import asyncio
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

async def process_with_multiple_backends(file_paths: list[str]):
    """Több fájl feldolgozása különböző backend-ekkel."""
    
    # Backend-ek létrehozása
    polars_backend = PolarsBackend()
    pandas_backend = PandasBackend()
    
    # Feldolgozási feladatok
    tasks = []
    
    for i, file_path in enumerate(file_paths):
        # Váltakozó backend kiválasztása
        backend = polars_backend if i % 2 == 0 else pandas_backend
        
        # Aszinkron feldolgozás
        task = asyncio.create_task(process_file(backend, file_path))
        tasks.append(task)
    
    # Várakozás az összes feladatra
    results = await asyncio.gather(*tasks)
    
    return results

async def process_file(backend, file_path: str):
    """Fájl feldolgozása adott backend-el."""
    data = backend.read(file_path)
    # Feldolgozás
    processed_data = process_data(data)
    return processed_data
```

### Backend Teljesítmény Tesztelés

```python
import time
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

def benchmark_backends(data, file_path: str):
    """Backend-ek teljesítményének összehasonlítása."""
    
    backends = {
        "Polars": PolarsBackend(),
        "Pandas": PandasBackend()
    }
    
    results = {}
    
    for name, backend in backends.items():
        # Írási sebesség
        start_time = time.time()
        backend.write(data, f"{name.lower()}_{file_path}")
        write_time = time.time() - start_time
        
        # Olvasási sebesség
        start_time = time.time()
        loaded_data = backend.read(f"{name.lower()}_{file_path}")
        read_time = time.time() - start_time
        
        results[name] = {
            "write_time": write_time,
            "read_time": read_time,
            "data_size": len(data)
        }
        
        print(f"{name} Backend:")
        print(f"  Írási idő: {write_time:.4f} másodperc")
        print(f"  Olvasási idő: {read_time:.4f} másodperc")
        print(f"  Adatméret: {len(data)} sor")
    
    return results
```

## Best Practices

### 1. Backend Kiválasztás

```python
from neural_ai.core.utils import HardwareFactory
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

def get_optimal_backend():
    """Optimális backend kiválasztása hardver alapján."""
    hardware = HardwareFactory.get_hardware_interface()
    
    if hardware.has_avx2():
        print("AVX2 támogatás: PolarsBackend használata")
        return PolarsBackend()
    else:
        print("Kompatibilitási mód: PandasBackend használata")
        return PandasBackend()
```

### 2. Tömörítés Beállítása

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Snappy tömörítés (gyors, közepes tömörítés)
backend.write(data, "data_snappy.parquet", compression="snappy")

# Gzip tömörítés (lassabb, jobb tömörítés)
backend.write(data, "data_gzip.parquet", compression="gzip")
```

### 3. Particionálás Használata

```python
from neural_ai.core.storage.backends import PolarsBackend
import polars as pl

backend = PolarsBackend()

# Adatok létrehozása particionáláshoz
df = pl.DataFrame({
    "timestamp": pl.date_range("2023-01-01", "2023-12-31", "1d"),
    "symbol": ["EURUSD"] * 365,
    "bid": [1.0] * 365,
    "ask": [1.0] * 365
})

# Dátum oszlopok hozzáadása
df = df.with_columns([
    pl.col("timestamp").dt.year().alias("year"),
    pl.col("timestamp").dt.month().alias("month"),
    pl.col("timestamp").dt.day().alias("day")
])

# Particionált mentés
backend.write(
    df,
    "tick_data.parquet",
    compression="snappy",
    partition_by=["year", "month", "day"]
)
```

### 4. Hibakezelés

```python
from neural_ai.core.storage.backends import PolarsBackend
from neural_ai.core.storage.exceptions import StorageError

backend = PolarsBackend()

try:
    # Adatok írása
    backend.write(data, "data.parquet")
    
    # Adatok olvasása
    loaded_data = backend.read("data.parquet")
    
except (ValueError, RuntimeError) as e:
    print(f"Hiba a backend művelet során: {e}")
    # Hibakezelés
```

## Exportált Osztályok

A modul a következő osztályokat exportálja:

- `DataFrameType`: DataFrame típus alias
- `StorageBackend`: Absztrakt alaposztály
- `PandasBackend`: Pandas implementáció
- `PolarsBackend`: Polars implementáció