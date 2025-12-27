# Pandas Backend - Tárolási Backend Dokumentáció

## Áttekintés

A `PandasBackend` egy tárolási backend implementáció, amely a Pandas könyvtárat és a FastParquet-et használja DataFrame-ek hatékony tárolására Parquet formátumban. A backend támogatja a chunkolást, aszinkron műveleteket és a particionált tárolást.

## Osztályok

### PandasDataFrame

Wrapper osztály a Pandas DataFrame köré lazy importtal.

**Cél:** Biztosítja, hogy a pandas és fastparquet csomagok csak akkor töltődjön be, amikor az osztályt valóban használják.

#### Metódusok

- `_import_pandas() -> tuple[Any, Any]`: Lazy import a pandas és fastparquet csomagok számára
- `pd` (property): Pandas modul lekérdezése
- `fp` (property): FastParquet modul lekérdezése

### PandasBackend

Pandas alapú tárolási backend FastParquet formátumhoz.

**Öröklés:** `StorageBackend`

**Attribútumok:**
- `name: str = 'pandas'`
- `supported_formats: list[str] = ['parquet']`
- `is_async: bool = True`

#### Konstruktor

```python
def __init__(self) -> None
```

Inicializálja a PandasBackend példányt. A lazy import miatt a pandas és fastparquet csomagok csak akkor töltődnek be, amikor az első műveletet végrehajtjuk.

#### Publikus Metódusok

##### write()

```python
def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None
```

DataFrame adatok írása Parquet formátumban FastParquet használatával.

**Paraméterek:**
- `data: Any`: A tárolandó Pandas DataFrame
- `path: str`: A cél elérési út (.parquet kiterjesztéssel)
- `**kwargs: dict[str, Any]`: További konfigurációs paraméterek
  - `compression: str`: Tömörítési algoritmus (alapértelmezett: 'snappy')
  - `partition_by: list[str] | None`: Particionálási oszlopok listája
  - `index: bool`: Index mentése (alapértelmezett: False)

**Kivételek:**
- `ValueError`: Ha az adatok érvénytelenek vagy az elérési út hibás
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a tárolási művelet sikertelen

##### read()

```python
def read(self, path: str, **kwargs: dict[str, Any]) -> Any
```

DataFrame adatok olvasása Parquet fájlból FastParquet használatával.

**Paraméterek:**
- `path: str`: A forrás elérési út
- `**kwargs: dict[str, Any]`: További konfigurációs paraméterek
  - `columns: list[str] | None`: Csak ezen oszlopok betöltése
  - `filters: list[tuple[Any, ...]] | None`: Szűrők a partíciókra (pl. [('year', '=', 2023)])
  - `chunk_size: int | None`: Chunk méret chunkolás esetén

**Visszatérési érték:** A beolvasott Pandas DataFrame

**Kivételek:**
- `FileNotFoundError`: Ha a forrásfájl nem létezik
- `ValueError`: Ha a fájlformátum nem támogatott
- `RuntimeError`: Ha az olvasási művelet sikertelen

##### append()

```python
def append(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None
```

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

Ha a célfájl nem létezik, létrehozza azt. Ha létezik, hozzáfűzi az új adatokat a meglévőhöz.

**Paraméterek:**
- `data: Any`: A hozzáfűzendő DataFrame
- `path: str`: A cél elérési út
- `**kwargs: dict[str, Any]`: További konfigurációs paraméterek
  - `compression: str`: Tömörítési algoritmus
  - `schema_validation: bool`: Sémavizsgálat engedélyezése
  - `index: bool`: Index mentése

**Kivételek:**
- `ValueError`: Ha az adatok sémája nem kompatibilis a meglévővel
- `FileNotFoundError`: Ha a célkönyvtár nem létezik
- `RuntimeError`: Ha a hozzáfűzési művelet sikertelen

##### supports_format()

```python
def supports_format(self, format_name: str) -> bool
```

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

**Paraméterek:**
- `format_name: str`: A formátum neve (pl. 'parquet', 'csv')

**Visszatérési érték:** True, ha a formátum támogatott, egyébként False

##### get_info()

```python
def get_info(self, path: str) -> dict[str, Any]
```

Parquet fájl információinak lekérdezése.

**Paraméterek:**
- `path: str`: Az elérési út

**Visszatérési érték:** A fájl információit tartalmazó dictionary:
- `size: int`: Fájlméret bájtban
- `rows: int`: Sorok száma
- `columns: list[str]`: Oszlopok listája
- `format: str`: 'parquet'
- `created: datetime`: Létrehozás dátuma
- `modified: datetime`: Módosítás dátuma
- `num_row_groups: int`: Row group-ok száma
- `compression: str`: Tömörítési algoritmus

**Kivételek:**
- `FileNotFoundError`: Ha a fájl nem létezik
- `RuntimeError`: Ha az információ lekérdezése sikertelen

#### Védett Metódusok

##### _ensure_initialized()

```python
def _ensure_initialized(self) -> None
```

Biztosítja, hogy a pandas csomag betöltődött.

##### _write_partitioned()

```python
def _write_partitioned(
    self, 
    df: Any, 
    path: str, 
    partition_by: list[str], 
    compression: str, 
    index: bool
) -> None
```

Particionált Parquet fájl írása.

**Paraméterek:**
- `df: Any`: A tárolandó DataFrame
- `path: str`: A cél elérési út
- `partition_by: list[str]`: Particionálási oszlopok listája
- `compression: str`: Tömörítési algoritmus
- `index: bool`: Index mentése

##### _read_chunked()

```python
def _read_chunked(
    self, 
    path: str, 
    chunk_size: int, 
    columns: list[str] | None, 
    filters: list[tuple[Any, ...]] | None
) -> Any
```

Chunkoltan olvassa a Parquet fájlt.

**Paraméterek:**
- `path: str`: A forrás elérési út
- `chunk_size: int`: Egy chunk mérete sorokban
- `columns: list[str] | None`: Csak ezen oszlopok betöltése
- `filters: list[tuple[Any, ...]] | None`: Szűrők a partíciókra

**Visszatérési érték:** Az összes chunkból összefűzött DataFrame

##### _validate_schema()

```python
def _validate_schema(self, existing: Any, new: Any) -> bool
```

Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e.

**Paraméterek:**
- `existing: Any`: A meglévő DataFrame
- `new: Any`: Az új DataFrame

**Visszatérési érték:** True, ha a sémák kompatibilisek, egyébként False

## Használati Példa

```python
from neural_ai.core.storage.backends.pandas_backend import PandasBackend
import pandas as pd

# Backend létrehozása
backend = PandasBackend()

# DataFrame létrehozása
df = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})

# Írás
backend.write(df, '/path/to/data.parquet', compression='snappy')

# Olvasás
df_read = backend.read('/path/to/data.parquet', columns=['id', 'name'])

# Hozzáfűzés
df_new = pd.DataFrame({
    'id': [4, 5],
    'name': ['David', 'Eve'],
    'age': [28, 32]
})
backend.append(df_new, '/path/to/data.parquet')

# Információ lekérdezése
info = backend.get_info('/path/to/data.parquet')
print(f"Rows: {info['rows']}, Columns: {info['columns']}")
```

## Jellemzők

- **Lazy Import:** A pandas és fastparquet csomagok csak akkor töltődnek be, amikor szükség van rájuk
- **Particionálás:** Támogatja a particionált tárolást oszlopok alapján
- **Chunkolás:** Nagy fájlok esetén lehetőség van chunkolásra
- **Tömörítés:** Támogatja a Snappy, Gzip és egyéb tömörítési algoritmusokat
- **Sémavizsgálat:** Opcionális sémavizsgálat hozzáfűzéskor
- **Metaadatok:** Kiterjesztett metaadat lekérdezés

## Függőségek

- `pandas`: DataFrame kezelés
- `fastparquet`: Parquet fájlformátum támogatás

## Lásd még

- [`StorageBackend`](base.md): Az absztrakt alaposztály
- [`PolarsBackend`](polars_backend.md): Alternatív backend Polars-szal
- [`ParquetStorage`](../implementations/parquet_storage.md): Magas szintű Parquet tároló