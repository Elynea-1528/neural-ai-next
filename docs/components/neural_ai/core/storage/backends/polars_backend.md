# PolarsBackend

## Áttekintés

A `PolarsBackend` egy tárolási backend implementáció, amely a Polars DataFrame könyvtárat és a PyArrow Parquet engine-t használja a hatékony adattároláshoz. Ez a backend ideális választás nagy adathalmazok esetén, mivel a Polars kiváló teljesítményt és memóriahatékonyságot nyújt.

## Főbb Jellemzők

- **Alapkönyvtár**: Polars
- **Parquet Engine**: PyArrow
- **Lazy Import**: A polars és pyarrow csomagok csak akkor töltődnek be, amikor szükség van rájuk
- **Chunkolás**: Támogatja a nagy adathalmazok chunkolt feldolgozását
- **Particionálás**: Dátum és szimbólum alapú particionálás támogatása
- **Aszinkron Műveletek**: Minden művelet aszinkron módon végezhető

## Osztálydefiníció

```python
class PolarsBackend(StorageBackend):
    """Polars alapú tárolási backend Parquet formátumhoz."""
    
    def __init__(self):
        """Inicializálja a PolarsBackend példányt."""
        super().__init__(name="polars", supported_formats=["parquet"], is_async=True)
        self._polars_wrapper = PolarsDataFrame()
        self._initialized = False
```

## Lazy Import Rendszer

A `PolarsBackend` egyedi lazy import rendszert használ a `PolarsDataFrame` wrapper osztályon keresztül:

```python
class PolarsDataFrame:
    """Wrapper osztály a Polars DataFrame köré lazy importtal."""
    
    def __init__(self):
        self._polars = None
        self._pyarrow = None
    
    def _import_polars(self):
        """Lazy import a polars és pyarrow csomagok számára."""
        if self._polars is None:
            import polars as pl
            import pyarrow as pa
            import pyarrow.parquet as pq
            self._polars = pl
            self._pyarrow = pa
            self._parquet = pq
        return self._polars, self._pyarrow, self._parquet
```

Ez a megoldás biztosítja, hogy a nehéz könyvtárak csak akkor töltődjenek be, amikor az első tárolási vagy olvasási műveletet végrehajtjuk.

## Metódusok

### `write(data: DataFrameType, path: str, **kwargs) -> None`

DataFrame adatok írása Parquet formátumban.

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

**Példa:**

```python
import polars as pl
from datetime import datetime
from neural_ai.core.storage.backends import PolarsBackend

# Backend létrehozása
backend = PolarsBackend()

# Minta adatok
data = pl.DataFrame({
    'timestamp': [datetime.now()],
    'symbol': ['EURUSD'],
    'bid': [1.1000],
    'ask': [1.1002],
    'volume': [1000],
    'source': ['jforex']
})

# Alapvető írás
backend.write(data, "data/tick.parquet")

# Tömörítéssel
backend.write(data, "data/tick.parquet", compression="snappy")

# Particionálva
backend.write(data, "data/tick.parquet", partition_by=["symbol", "year"])
```

### `read(path: str, **kwargs) -> DataFrameType`

DataFrame adatok olvasása Parquet fájlból.

**Paraméterek:**
- `path`: A forrás elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `columns`: Csak ezen oszlopok betöltése
  - `filters`: Szűrők a partíciókra (pl. [('year', '=', 2023)])
  - `chunk_size`: Chunk méret chunkolás esetén

**Visszatérési érték:**
A beolvasott Polars DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

**Példa:**

```python
from datetime import datetime
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Alapvető olvasás
data = backend.read("data/tick.parquet")

# Csak bizonyos oszlopok
data = backend.read("data/tick.parquet", columns=["timestamp", "bid", "ask"])

# Szűrés partíciókra
filters = [("year", "=", 2023), ("month", "=", 12)]
data = backend.read("data/tick.parquet", filters=filters)

# Chunkolás
data = backend.read("data/tick.parquet", chunk_size=10000)
```

### `append(data: DataFrameType, path: str, **kwargs) -> None`

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

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

**Példa:**

```python
import polars as pl
from datetime import datetime
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()

# Új adatok
new_data = pl.DataFrame({
    'timestamp': [datetime.now()],
    'symbol': ['EURUSD'],
    'bid': [1.1001],
    'ask': [1.1003],
    'volume': [1500],
    'source': ['mt5']
})

# Hozzáfűzés
backend.append(new_data, "data/tick.parquet")

# Sémavizsgálattal
backend.append(new_data, "data/tick.parquet", schema_validation=True)
```

### `get_info(path: str) -> Dict[str, Any]`

Parquet fájl információinak lekérdezése.

**Paraméterek:**
- `path`: Az elérési út

**Visszatérési érték:**
A fájl információit tartalmazó dictionary:
- `size`: Fájlméret bájtban
- `rows`: Sorok száma
- `columns`: Oszlopok listája
- `format`: 'parquet'
- `created`: Létrehozás dátuma
- `modified`: Módosítás dátuma
- `num_row_groups`: Row group-ok száma
- `compression`: Tömörítési algoritmus

**Példa:**

```python
from neural_ai.core.storage.backends import PolarsBackend

backend = PolarsBackend()
info = backend.get_info("data/tick.parquet")

print(f"File size: {info['size']} bytes")
print(f"Rows: {info['rows']}")
print(f"Columns: {info['columns']}")
print(f"Compression: {info['compression']}")
```

## Belső Segédfunkciók

### `_read_chunked(path: str, chunk_size: int, columns, filters) -> DataFrameType`

Chunkoltan olvassa a Parquet fájlt PyArrow segítségével.

**Paraméterek:**
- `path`: A forrás elérési út
- `chunk_size`: Egy chunk mérete sorokban
- `columns`: Csak ezen oszlopok betöltése
- `filters`: Szűrők a partíciókra

**Visszatérési érték:**
Az összes chunkból összefűzött DataFrame

### `_validate_schema(existing: DataFrameType, new: DataFrameType) -> bool`

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

**Paraméterek:**
- `existing`: A meglévő DataFrame
- `new`: Az új DataFrame

**Visszatérési érték:**
True, ha a sémák kompatibilisek, egyébként False

## Teljesítmény Optimalizálások

### 1. Lazy Import

A nehéz könyvtárak csak akkor töltődnek be, amikor szükség van rájuk:

```python
backend = PolarsBackend()  # Itt még nem töltődik be a polars

# Az első műveletkor töltődik be
backend.write(data, "file.parquet")  # Most töltődik be
```

### 2. Chunkolás

Nagy adathalmazok hatékony feldolgozása:

```python
# 1M sor chunkolása 10k-as darabokban
data = backend.read("large_file.parquet", chunk_size=10000)
```

### 3. Particionálás

Gyors lekérdezés partíciókra szűréssel:

```python
# Csak a 2023. decemberi adatok betöltése
filters = [("year", "=", 2023), ("month", "=", 12)]
data = backend.read("data/tick.parquet", filters=filters)
```

### 4. Oszlop Szűrés

Csak a szükséges oszlopok betöltése:

```python
# Csak időbélyeg és árak betöltése
data = backend.read("data/tick.parquet", columns=["timestamp", "bid", "ask"])
```

## Használati Példák

### 1. Tick Adatok Tárolása

```python
import polars as pl
from datetime import datetime, timedelta
from neural_ai.core.storage.backends import PolarsBackend

async def store_tick_data():
    backend = PolarsBackend()
    
    # Tick adatok generálása
    timestamps = [datetime.now() + timedelta(seconds=i) for i in range(10000)]
    data = pl.DataFrame({
        'timestamp': timestamps,
        'symbol': ['EURUSD'] * 10000,
        'bid': [1.1000 + i * 0.0001 for i in range(10000)],
        'ask': [1.1002 + i * 0.0001 for i in range(10000)],
        'volume': [1000] * 10000,
        'source': ['jforex'] * 10000
    })
    
    # Tárolás particionálva
    await backend.write(
        data,
        "data/tick/EURUSD/tick.parquet",
        partition_by=["year", "month"],
        compression="snappy"
    )
    
    print("Tick adatok sikeresen tárolva")
```

### 2. Nagy Adathalmaz Feldolgozása

```python
from neural_ai.core.storage.backends import PolarsBackend

async def process_large_dataset():
    backend = PolarsBackend()
    
    # Chunkoltan olvassuk az adatokat
    chunk_size = 50000
    data = await backend.read(
        "data/large_tick_data.parquet",
        chunk_size=chunk_size,
        columns=["timestamp", "bid", "ask"]
    )
    
    # Feldolgozás
    print(f"Loaded {len(data)} rows")
    
    # Statisztikák
    info = await backend.get_info("data/large_tick_data.parquet")
    print(f"File size: {info['size'] / 1024 / 1024:.2f} MB")
    print(f"Compression: {info['compression']}")
```

### 3. Több Szimbólum Kezelése

```python
from neural_ai.core.storage.backends import PolarsBackend

async def manage_multiple_symbols():
    backend = PolarsBackend()
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'XAUUSD']
    
    for symbol in symbols:
        # Adatok olvasása
        data = await backend.read(
            f"data/tick/{symbol}/tick.parquet",
            filters=[("year", "=", 2023)],
            columns=["timestamp", "bid", "ask"]
        )
        
        # Feldolgozás
        print(f"{symbol}: {len(data)} ticks loaded")
        
        # Statisztikák
        info = await backend.get_info(f"data/tick/{symbol}/tick.parquet")
        print(f"  Size: {info['size'] / 1024 / 1024:.2f} MB")
```

## Összehasonlítás

### Polars vs Pandas

| Szempont | PolarsBackend | PandasBackend |
|----------|---------------|---------------|
| **Teljesítmény** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Memóriahatékonyság** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Chunkolás** | PyArrow alapú | FastParquet alapú |
| **Particionálás** | Igen | Igen |
| **Lazy Import** | Igen | Igen |
| **Aszinkron** | Igen | Igen |

### Előnyök

1. **Kiváló Teljesítmény**: A Polars gyorsabb mint a Pandas nagy adathalmazokon
2. **Memóriahatékonyság**: Kevesebb memóriát használ
3. **Lazy Evaluation**: Több műveletet összevonhatunk egyetlen optimalizált végrehajtásba
4. **Többszálas Feldolgozás**: Automatikusan használja a CPU összes magját

### Hátrányok

1. **Kisebb Közösség**: A Pandas-nál kisebb a közösség és kevesebb a harmadik féltől származó eszköz
2. **Kompatibilitás**: Kevesebb eszközzel kompatibilis mint a Pandas

## Kapcsolódó Dokumentumok

- [Storage Backends Áttekintés](__init__.md)
- [Base Backend](base.md)
- [Pandas Backend](pandas_backend.md)
- [Parquet Storage](../parquet.md)

## Tesztelés

```bash
# PolarsBackend tesztek futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_polars_backend.py -v

# Teljes coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_polars_backend.py --cov=neural_ai.core.storage.backends.polars_backend --cov-report=html
```

## Jegyzetek

- A PolarsBackend a leggyorsabb választás nagy adathalmazok esetén
- A lazy import biztosítja, hogy a nehéz könyvtárak csak akkor töltődjenek be, amikor szükség van rájuk
- A chunkolás lehetővé teszi a korlátlan méretű adathalmazok feldolgozását
- A particionálás jelentősen javítja a lekérdezési teljesítményt