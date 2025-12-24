# PandasBackend

## Áttekintés

A `PandasBackend` egy tárolási backend implementáció, amely a Pandas DataFrame könyvtárat és a FastParquet engine-t használja a hatékony adattároláshoz. Ez a backend ideális választás, ha kompatibilitásra van szükség más Pandas alapú eszközökkel vagy ha a fejlesztők ismerik a Pandas API-t.

## Főbb Jellemzők

- **Alapkönyvtár**: Pandas
- **Parquet Engine**: FastParquet
- **Lazy Import**: A pandas és fastparquet csomagok csak akkor töltődnek be, amikor szükség van rájuk
- **Chunkolás**: Támogatja a nagy adathalmazok chunkolt feldolgozását
- **Particionálás**: Dátum és szimbólum alapú particionálás támogatása
- **Aszinkron Műveletek**: Minden művelet aszinkron módon végezhető

## Osztálydefiníció

```python
class PandasBackend(StorageBackend):
    """Pandas alapú tárolási backend FastParquet formátumhoz."""
    
    def __init__(self):
        """Inicializálja a PandasBackend példányt."""
        super().__init__(name="pandas", supported_formats=["parquet"], is_async=True)
        self._pandas_wrapper = PandasDataFrame()
        self._initialized = False
```

## Lazy Import Rendszer

A `PandasBackend` egyedi lazy import rendszert használ a `PandasDataFrame` wrapper osztályon keresztül:

```python
class PandasDataFrame:
    """Wrapper osztály a Pandas DataFrame köré lazy importtal."""
    
    def __init__(self):
        self._pandas = None
        self._fastparquet = None
    
    def _import_pandas(self):
        """Lazy import a pandas és fastparquet csomagok számára."""
        if self._pandas is None:
            import pandas as pd
            import fastparquet
            self._pandas = pd
            self._fastparquet = fastparquet
        return self._pandas, self._fastparquet
```

Ez a megoldás biztosítja, hogy a nehéz könyvtárak csak akkor töltődjenek be, amikor az első tárolási vagy olvasási műveletet végrehajtjuk.

## Metódusok

### `write(data: DataFrameType, path: str, **kwargs) -> None`

DataFrame adatok írása Parquet formátumban FastParquet használatával.

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

**Példa:**

```python
import pandas as pd
from datetime import datetime
from neural_ai.core.storage.backends import PandasBackend

# Backend létrehozása
backend = PandasBackend()

# Minta adatok
data = pd.DataFrame({
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

# Index mentésével
backend.write(data, "data/tick.parquet", index=True)
```

### `read(path: str, **kwargs) -> DataFrameType`

DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

**Paraméterek:**
- `path`: A forrás elérési út
- `**kwargs`: További konfigurációs paraméterek
  - `columns`: Csak ezen oszlopok betöltése
  - `filters`: Szűrők a partíciókra (pl. [('year', '=', 2023)])
  - `chunk_size`: Chunk méret chunkolás esetén

**Visszatérési érték:**
A beolvasott Pandas DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

**Példa:**

```python
from datetime import datetime
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

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
  - `index`: Index mentése

**Kivételek:**
- `ValueError`: Ha az adatok sémája nem kompatibilis a meglévővel
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a hozzáfűzési művelet sikertelen

**Példa:**

```python
import pandas as pd
from datetime import datetime
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()

# Új adatok
new_data = pd.DataFrame({
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
from neural_ai.core.storage.backends import PandasBackend

backend = PandasBackend()
info = backend.get_info("data/tick.parquet")

print(f"File size: {info['size']} bytes")
print(f"Rows: {info['rows']}")
print(f"Columns: {info['columns']}")
print(f"Compression: {info['compression']}")
```

## Belső Segédfunkciók

### `_write_partitioned(df: DataFrameType, path: str, partition_by: list, compression: str, index: bool) -> None`

Particionált Parquet fájl írása.

**Paraméterek:**
- `df`: A tárolandó DataFrame
- `path`: A cél elérési út
- `partition_by`: Particionálási oszlopok listája
- `compression`: Tömörítési algoritmus
- `index`: Index mentése

### `_read_chunked(path: str, chunk_size: int, columns, filters) -> DataFrameType`

Chunkoltan olvassa a Parquet fájlt.

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
backend = PandasBackend()  # Itt még nem töltődik be a pandas

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
import pandas as pd
from datetime import datetime, timedelta
from neural_ai.core.storage.backends import PandasBackend

async def store_tick_data():
    backend = PandasBackend()
    
    # Tick adatok generálása
    timestamps = [datetime.now() + timedelta(seconds=i) for i in range(10000)]
    data = pd.DataFrame({
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
from neural_ai.core.storage.backends import PandasBackend

async def process_large_dataset():
    backend = PandasBackend()
    
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
from neural_ai.core.storage.backends import PandasBackend

async def manage_multiple_symbols():
    backend = PandasBackend()
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

### 4. Adatok Hozzáfűzése

```python
import pandas as pd
from datetime import datetime
from neural_ai.core.storage.backends import PandasBackend

async def append_tick_data():
    backend = PandasBackend()
    
    # Létező adatok ellenőrzése
    try:
        existing_data = await backend.read("data/tick.parquet")
        print(f"Existing rows: {len(existing_data)}")
    except FileNotFoundError:
        print("File does not exist, creating new one")
    
    # Új tick adatok
    new_ticks = pd.DataFrame({
        'timestamp': [datetime.now()],
        'symbol': ['EURUSD'],
        'bid': [1.1005],
        'ask': [1.1007],
        'volume': [2000],
        'source': ['ibkr']
    })
    
    # Hozzáfűzés sémavizsgálattal
    await backend.append(
        new_ticks,
        "data/tick.parquet",
        schema_validation=True,
        compression="snappy"
    )
    
    print("Tick adatok sikeresen hozzáfűzve")
```

## Összehasonlítás

### Pandas vs Polars

| Szempont | PandasBackend | PolarsBackend |
|----------|---------------|---------------|
| **Teljesítmény** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Memóriahatékonyság** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Chunkolás** | FastParquet alapú | PyArrow alapú |
| **Particionálás** | Igen | Igen |
| **Lazy Import** | Igen | Igen |
| **Aszinkron** | Igen | Igen |
| **Kompatibilitás** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### Előnyök

1. **Széles Körű Támogatás**: A Pandas a legnépszerűbb DataFrame könyvtár Pythonban
2. **Gazdag API**: Rengeteg beépített függvény adatmanipulációhoz
3. **Kompatibilitás**: Kompatibilis a legtöbb adattudományi eszközzel
4. **Jól Ismert**: A legtöbb fejlesztő ismeri a Pandas API-t

### Hátrányok

1. **Lassabb Teljesítmény**: A Polars-nál lassabb nagy adathalmazokon
2. **Nagyobb Memóriahasználat**: Több memóriát igényel mint a Polars
3. **Single-threaded**: Alapértelmezetten egy szálat használ

## Kapcsolódó Dokumentumok

- [Storage Backends Áttekintés](__init__.md)
- [Base Backend](base.md)
- [Polars Backend](polars_backend.md)
- [Parquet Storage](../parquet.md)

## Tesztelés

```bash
# PandasBackend tesztek futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_pandas_backend.py -v

# Teljes coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_pandas_backend.py --cov=neural_ai.core.storage.backends.pandas_backend --cov-report=html
```

## Jegyzetek

- A PandasBackend a legjobb választás, ha kompatibilitásra van szükség más Pandas alapú eszközökkel
- A lazy import biztosítja, hogy a nehéz könyvtárak csak akkor töltődjenek be, amikor szükség van rájuk
- A chunkolás lehetővé teszi a korlátlan méretű adathalmazok feldolgozását
- A particionálás jelentősen javítja a lekérdezési teljesítményt
- A FastParquet engine gyorsabb lehet mint a PyArrow bizonyos esetekben