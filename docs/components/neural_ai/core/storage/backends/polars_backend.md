# PolarsBackend

## Áttekintés

A `PolarsBackend` egy Polars alapú tárolási backend, amely a Parquet formátumot használja a gyors adatfeldolgozáshoz. Ez a backend AVX2 támogatással rendelkezik, ami jelentősen gyorsabb feldolgozást tesz lehetővé. Ideális választás modern CPU-khoz, ahol a teljesítmény a legfontosabb szempont.

## Osztály

```python
class PolarsBackend(StorageBackend)
```

## Főbb Jellemzők

- **AVX2 gyorsítás**: Jelentősen gyorsabb feldolgozás
- **Lazy import**: A polars és pyarrow csomagok csak akkor töltődnek be, amikor szükség van rájuk
- **Párhuzamos feldolgozás**: Többmagos processzorok hatékony kihasználása
- **Jobb memóriakezelés**: Hatékonyabb memóriahasználat
- **Chunkolás**: Nagy adathalmazok darabonkénti feldolgozása
- **Particionálás**: Dátum és szimbólum alapú particionálás

## Attribútumok

- `name`: 'polars'
- `supported_formats`: ['parquet']
- `is_async`: True

## Inicializálás

```python
def __init__(self) -> None
```

**Példa:**

```python
from neural_ai.core.storage.backends import PolarsBackend

# Backend létrehozása
backend = PolarsBackend()

print(f"Backend neve: {backend.name}")
print(f"Támogatott formátumok: {backend.supported_formats}")
print(f"Aszinkron támogatás: {backend.is_async}")
```

## Metódusok

### `write()`

DataFrame adatok írása Parquet formátumban.

```python
def write(
    self,
    data: Any,
    path: str,
    **kwargs: dict[str, Any]
) -> None
```

**Paraméterek:**
- `data`: A tárolandó Polars DataFrame
- `path`: A cél elérési út (.parquet kiterjesztéssel)
- `**kwargs`: További konfigurációs paraméterek
  - `compression`: Tömörítési algoritmus (alapértelmezett: 'snappy')
  - `partition_by`: Particionálási oszlopok listája
  - `schema`: Adatséma definíció

**Kivételek:**
- `ValueError`: Ha az adatok érvénytelenek vagy az elérési út hibás
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a tárolási művelet sikertelen

**Példák:**

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Alapvető írás
df = pl.DataFrame({
    "timestamp": pl.date_range("2023-01-01", "2023-01-02", "1h"),
    "value": range(25),
    "category": ["A", "B", "C"] * 8 + ["A"]
})
backend.write(df, "data.parquet")

# Tömörített írás
backend.write(df, "data_compressed.parquet", compression="snappy")

# Particionált írás
df_with_partitions = df.with_columns([
    pl.col("timestamp").dt.year().alias("year"),
    pl.col("timestamp").dt.month().alias("month")
])
backend.write(
    df_with_partitions,
    "partitioned_data.parquet",
    partition_by=["year", "month"]
)
```

### `read()`

DataFrame adatok olvasása Parquet fájlból.

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
- `pl.DataFrame`: A beolvasott Polars DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

**Példák:**

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Alapvető olvasás
df = backend.read("data.parquet")

# Csak bizonyos oszlopok betöltése
df = backend.read("data.parquet", columns=["timestamp", "value"])

# Partíciók szűrése
df = backend.read(
    "partitioned_data.parquet",
    filters=[("year", "=", 2023), ("month", "=", 1)]
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

**Kivételek:**
- `ValueError`: Ha az adatok sémája nem kompatibilis a meglévővel
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a hozzáfűzési művelet sikertelen

**Példák:**

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Új adatok létrehozása
new_data = pl.DataFrame({
    "timestamp": pl.date_range("2023-01-02", "2023-01-03", "1h"),
    "value": range(100, 125),
    "category": ["D", "E", "F"] * 8 + ["D"]
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
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

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
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

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

Biztosítja, hogy a polars csomag betöltődött.

```python
def _ensure_initialized(self) -> None
```

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
- `pl.DataFrame`: Az összes chunkból összefűzött DataFrame

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
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Nagy DataFrame létrehozása
large_df = pl.DataFrame({
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

### Tick Adatok Particionált Tárolása

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Tick adatok létrehozása
tick_data = pl.DataFrame({
    "timestamp": pl.date_range("2023-01-01", "2023-01-02", "1min"),
    "symbol": ["EURUSD"] * 1440,
    "bid": [1.0 + i * 0.0001 for i in range(1440)],
    "ask": [1.0002 + i * 0.0001 for i in range(1440)],
    "volume": [1000] * 1440
})

# Dátum oszlopok hozzáadása
tick_data = tick_data.with_columns([
    pl.col("timestamp").dt.year().alias("year"),
    pl.col("timestamp").dt.month().alias("month"),
    pl.col("timestamp").dt.day().alias("day")
])

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

### Párhuzamos Feldolgozás

```python
import polars as pl
import asyncio
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

async def process_multiple_files(file_paths: list[str]):
    """Több fájl párhuzamos feldolgozása."""
    
    tasks = []
    for file_path in file_paths:
        task = asyncio.create_task(process_single_file(file_path))
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results

async def process_single_file(file_path: str):
    """Egyetlen fájl feldolgozása."""
    # Adatok betöltése
    df = backend.read(file_path)
    
    # Feldolgozás
    processed_df = df.filter(pl.col("value") > 100)
    
    # Eredmény mentése
    output_path = file_path.replace(".parquet", "_processed.parquet")
    backend.write(processed_df, output_path)
    
    return len(processed_df)

# Használat
file_paths = ["data1.parquet", "data2.parquet", "data3.parquet"]
results = asyncio.run(process_multiple_files(file_paths))
print(f"Feldolgozott sorok: {results}")
```

### Adatok Aggregálása

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Adatok betöltése
df = backend.read("tick_data.parquet")

# Aggregálás
summary = df.group_by("symbol").agg([
    pl.col("bid").min().alias("min_bid"),
    pl.col("bid").max().alias("max_bid"),
    pl.col("bid").mean().alias("avg_bid"),
    pl.col("volume").sum().alias("total_volume")
])

# Eredmény mentése
backend.write(summary, "tick_summary.parquet")

print("Aggregált adatok:")
print(summary)
```

### Komplex Szűrés és Transzformáció

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Adatok betöltése
df = backend.read("financial_data.parquet")

# Komplex szűrés
filtered_df = df.filter(
    (pl.col("timestamp").dt.year() == 2023) &
    (pl.col("symbol").is_in(["EURUSD", "GBPUSD"])) &
    (pl.col("volume") > 1000)
)

# Transzformáció
transformed_df = filtered_df.with_columns([
    # Spread számítás
    (pl.col("ask") - pl.col("bid")).alias("spread"),
    # Napi aggregáció
    pl.col("timestamp").dt.date().alias("date")
])

# Csoportosítás és aggregáció
daily_summary = transformed_df.group_by(["date", "symbol"]).agg([
    pl.col("spread").mean().alias("avg_spread"),
    pl.col("volume").sum().alias("daily_volume")
])

# Eredmény mentése
backend.write(daily_summary, "daily_summary.parquet")

print(f"Feldolgozott napok: {len(daily_summary)}")
```

## Teljesítmény Optimalizálás

### 1. Predikátum Pushdown

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Predikátum pushdown - a szűrés a betöltéskor történik
filtered_data = backend.read(
    "large_data.parquet",
    filters=[
        ("year", "=", 2023),
        ("month", "=", 12),
        ("value", ">", 1000)
    ]
)
```

### 2. Oszlop Pruning

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Csak szükséges oszlopok betöltése
essential_columns = ["timestamp", "value", "category"]
df = backend.read("data.parquet", columns=essential_columns)
```

### 3. Lazy Evaluation

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Lazy evaluation használata
lazy_df = pl.scan_parquet("data.parquet")

# Láncolt műveletek
result = (
    lazy_df
    .filter(pl.col("value") > 100)
    .group_by("category")
    .agg([
        pl.col("value").mean().alias("avg_value"),
        pl.col("value").count().alias("count")
    ])
    .collect()  # Végrehajtás
)

backend.write(result, "aggregated_data.parquet")
```

## Best Practices

### 1. Tömörítés Beállítása

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Snappy tömörítés (gyors, közepes tömörítés)
backend.write(data, "data_snappy.parquet", compression="snappy")

# Gzip tömörítés (lassabb, jobb tömörítés)
backend.write(data, "data_gzip.parquet", compression="gzip")
```

### 2. Partíciók Használata

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Particionált mentés
backend.write(
    tick_data,
    "tick_data.parquet",
    partition_by=["year", "month", "day"]
)

# Partíciók szűrése
filtered_data = backend.read(
    "tick_data.parquet",
    filters=[("year", "=", 2023), ("month", "=", 12)]
)
```

### 3. Hibakezelés

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

### 4. Memóriakezelés

```python
import polars as pl
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Stream processing nagy adathalmazokhoz
lazy_df = pl.scan_parquet("large_data.parquet")

# Lazy aggregation
result = (
    lazy_df
    .group_by("category")
    .agg([
        pl.col("value").sum().alias("total")
    ])
    .collect(streaming=True)  # Stream mód
)

backend.write(result, "aggregated.parquet")
```

## Teljesítmény Összehasonlítás

### Polars vs Pandas

```python
import time
import pandas as pd
import polars as pl
from neural_ai.core.storage.backends import PandasBackend, PolarsBackend

# Nagy DataFrame létrehozása
size = 1_000_000
data = {
    "id": range(size),
    "value": [i * 2 for i in range(size)],
    "category": [f"cat_{i % 100}" for i in range(size)]
}

# Pandas DataFrame
pandas_df = pd.DataFrame(data)

# Polars DataFrame
polars_df = pl.DataFrame(data)

# Backend-ek
pandas_backend = PandasBackend()
polars_backend = PolarsBackend()

# Teljesítmény teszt
def benchmark_write(backend, df, path):
    start = time.time()
    backend.write(df, path)
    return time.time() - start

def benchmark_read(backend, path):
    start = time.time()
    df = backend.read(path)
    return time.time() - start

# Tesztelés
pandas_write_time = benchmark_write(pandas_backend, pandas_df, "pandas_test.parquet")
polars_write_time = benchmark_write(polars_backend, polars_df, "polars_test.parquet")

pandas_read_time = benchmark_read(pandas_backend, "pandas_test.parquet")
polars_read_time = benchmark_read(polars_backend, "polars_test.parquet")

print(f"Pandas írás: {pandas_write_time:.4f} másodperc")
print(f"Polars írás: {polars_write_time:.4f} másodperc")
print(f"Pandas olvasás: {pandas_read_time:.4f} másodperc")
print(f"Polars olvasás: {polars_read_time:.4f} másodperc")
```

## Kompatibilitás

A PolarsBackend a következő környezetekben működik:

- **CPU**: x86_64 CPU-k AVX2 támogatással
- **Operációs rendszer**: Linux, macOS, Windows
- **Python verzió**: 3.8+
- **Függőségek**: polars, pyarrow

Ez a backend ideális választás, ha:
- Modern hardver áll rendelkezésre
- A teljesítmény a legfontosabb szempont
- Nagy adathalmazokat kell feldolgozni
- Párhuzamos feldolgozásra van szükség

## AVX2 Támogatás Ellenőrzése

```python
from neural_ai.core.utils import HardwareFactory

hardware = HardwareFactory.get_hardware_interface()

if hardware.has_avx2():
    print("AVX2 támogatás: PolarsBackend használata")
    from neural_ai.core.storage.backends import PolarsBackend
    backend = PolarsBackend()
else:
    print("Nincs AVX2 támogatás: PandasBackend használata")
    from neural_ai.core.storage.backends import PandasBackend
    backend = PandasBackend()