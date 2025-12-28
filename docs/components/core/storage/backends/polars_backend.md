# PolarsBackend

## Áttekintés

A `PolarsBackend` egy nagy teljesítményű tárolási backend, amely a Polars könyvtárat használja a DataFrame-ek gyors feldolgozásához és a PyArrow Parquet formátumot a hatékony tároláshoz. Ez a backend ideális nagy adatmennyiségek kezeléséhez, különösen AVX2 támogatással rendelkező hardveren.

## Osztály leírás

**Teljes név**: `neural_ai.core.storage.backends.polars_backend.PolarsBackend`

**Öröklődés**: `StorageBackend`

## Főbb jellemzők

- **Motor**: Polars + PyArrow
- **Támogatott formátumok**: Parquet
- **Aszinkron támogatás**: Igen
- **Lazy import**: A polars és pyarrow csak szükség esetén töltődik be
- **Chunkolás**: Támogatja a nagy fájlok darabolását
- **Particionálás**: Támogatja a particionált tárolást
- **Tömörítés**: Támogatja a Snappy, Gzip és egyéb tömörítési algoritmusokat
- **Sémavizsgálat**: Automatikus séma ellenőrzés hozzáfűzéskor

## Inicializálás

```python
from neural_ai.core.storage.backends.polars_backend import PolarsBackend

# Alap inicializálás
backend = PolarsBackend()

# A backend lazy importot használ, így a polars csak az első műveletkor töltődik be
```

**Attribútumok:**
- `name`: 'polars'
- `supported_formats`: ['parquet']
- `is_async`: True
- `_initialized`: A backend inicializáltsági állapota

## Metódusok

### `write()`

DataFrame adatok írása Parquet formátumban.

```python
def write(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None
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

Alap írás:
```python
import polars as pl

df = pl.DataFrame({'id': [1, 2, 3], 'name': ['a', 'b', 'c']})
backend.write(df, "data.parquet")
```

Tömörítéssel:
```python
backend.write(df, "data.parquet", compression='gzip')
```

Particionálva:
```python
backend.write(df, "data.parquet", partition_by=['category'])
```

### `read()`

DataFrame adatok olvasása Parquet fájlból.

```python
def read(self, path: str, **kwargs: dict[str, Any]) -> Any
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

Alap olvasás:
```python
df = backend.read("data.parquet")
```

Oszlopok szűrése:
```python
df = backend.read("data.parquet", columns=['id', 'name'])
```

Szűrőkkel:
```python
filters = [('year', '=', 2023), ('month', '=', 12)]
df = backend.read("data.parquet", filters=filters)
```

Chunkolás:
```python
df = backend.read("large_data.parquet", chunk_size=10000)
```

### `append()`

DataFrame adatok hozzáfűzése egy meglévő Parquet fájlhoz.

```python
def append(self, data: Any, path: str, **kwargs: dict[str, Any]) -> None
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

Alap hozzáfűzés:
```python
new_data = pl.DataFrame({'id': [4, 5], 'name': ['d', 'e']})
backend.append(new_data, "data.parquet")
```

Sémavizsgálattal:
```python
backend.append(new_data, "data.parquet", schema_validation=True)
```

### `get_info()`

Parquet fájl információinak lekérdezése.

```python
def get_info(self, path: str) -> dict[str, Any]
```

**Paraméterek:**
- `path`: Az elérési út

**Visszatérési érték:**
```python
{
    'size': 1024,              # Fájlméret bájtban
    'rows': 1000,              # Sorok száma
    'columns': ['id', 'name'], # Oszlopok listája
    'format': 'parquet',       # Formátum
    'created': datetime(...),  # Létrehozás dátuma
    'modified': datetime(...), # Módosítás dátuma
    'num_row_groups': 1,       # Row group-ok száma
    'compression': 'SNAPPY'    # Tömörítés típusa
}
```

**Kivételek:**
- `FileNotFoundError`: Ha a fájl nem létezik
- `RuntimeError`: Ha az információ lekérdezése sikertelen

**Példa:**
```python
info = backend.get_info("data.parquet")
print(f"Sorok: {info['rows']}, Méret: {info['size']} bájt")
```

### `supports_format()`

Ellenőrzi, hogy a backend támogatja-e a megadott formátumot.

```python
def supports_format(self, format_name: str) -> bool
```

**Példa:**
```python
assert backend.supports_format('parquet') == True
assert backend.supports_format('csv') == False
```

### `validate_data()`

Ellenőrzi, hogy az adatok érvényes DataFrame-e.

```python
def validate_data(self, data: Any) -> bool
```

**Példa:**
```python
df = pl.DataFrame({'id': [1, 2, 3]})
assert backend.validate_data(df) == True
assert backend.validate_data(None) == False
```

## Belső működés

### Lazy Import

A `PolarsBackend` lazy importot használ a teljesítmény optimalizálásához:

```python
class PolarsDataFrame:
    """Wrapper osztály a Polars DataFrame köré lazy importtal."""
    
    def _import_polars(self):
        """Lazy import a polars és pyarrow csomagok számára."""
        if self._polars is None:
            import polars as pl
            import pyarrow as pa
            import pyarrow.parquet as pq
            # ...
```

Ez biztosítja, hogy a nehéz könyvtárak csak akkor töltődjenek be, amikor valóban szükség van rájuk.

### Inicializálás ellenőrzés

Minden művelet előtt ellenőrzi az inicializáltságot:

```python
def _ensure_initialized(self):
    """Biztosítja, hogy a polars csomag betöltődött."""
    if not self._initialized:
        self._polars_wrapper._import_polars()
        self._initialized = True
```

### Chunkolás

A `_read_chunked()` metódus lehetővé teszi nagy fájlok hatékony feldolgozását:

```python
def _read_chunked(
    self, path: str, chunk_size: int, columns: list | None, filters: list | None
) -> Any:
    # PyArrow segítségével chunkolás
    parquet_file = self._polars_wrapper.pq.ParquetFile(path)
    
    chunks = []
    for batch in parquet_file.iter_batches(batch_size=chunk_size, columns=columns):
        chunks.append(self._polars_wrapper.pl.from_arrow(batch))
    
    # Összefűzés
    return self._polars_wrapper.pl.concat(chunks)
```

### Sémavizsgálat

A `_validate_schema()` metódus ellenőrzi a sémakompatibilitást:

```python
def _validate_schema(self, existing: Any, new: Any) -> bool:
    """Ellenőrzi, hogy a két DataFrame sémája kompatibilis-e."""
    # Az új adatoknak tartalmazniuk kell az összes meglévő oszlopot
    return existing_cols.issubset(new_cols)
```

## Teljesítmény optimalizációk

### AVX2 támogatás

A PolarsBackend kihasználja az AVX2 utasításkészletet a gyorsabb adatfeldolgozáshoz:

- Automatikus detektálás a `ParquetStorageService`-en keresztül
- Akár 10x-es sebességnövekedés nagy adatmennyiségeknél
- Vektorizált műveletek a modern CPU-kon

### Memóriakezelés

- **Zero-copy**: A PyArrow lehetővé teszi a zero-copy műveleteket
- **Streaming**: Nagy fájlok feldolgozása korlátozott memóriával
- **Garbage collection**: Hatékony memóriafelszabadítás

## Hibakezelés

A backend robusztus hibakezelést valósít meg:

### Érvényesítések

- DataFrame érvényesség ellenőrzése
- Fájlformátum ellenőrzése (.parquet kiterjesztés)
- Sémakompatibilitás ellenőrzése hozzáfűzéskor
- Célkönyvtár létezésének ellenőrzése

### Kivételek

- `ValueError`: Érvénytelen adatok vagy paraméterek
- `FileNotFoundError`: Fájl nem található
- `RuntimeError`: Egyéb futási idejű hibák

## Használati esetek

### Nagy adatmennyiségek feldolgozása

```python
# Több GB-os fájl feldolgozása chunkokban
chunk_size = 100000
df = backend.read("huge_dataset.parquet", chunk_size=chunk_size)

# Feldolgozás
processed_data = process_large_dataset(df)
```

### Idősoros adatok kezelése

```python
# Particionált tárolás dátum szerint
backend.write(tick_data, "tick_data.parquet", partition_by=['date'])

# Adott időszak betöltése
filters = [('date', '>=', '2023-01-01'), ('date', '<=', '2023-12-31')]
df = backend.read("tick_data.parquet", filters=filters)
```

### Adatgyűjtés és hozzáfűzés

```python
# Kezdeti adatok
initial_data = pl.DataFrame({'timestamp': [...], 'value': [...]})
backend.write(initial_data, "timeseries.parquet")

# Új adatok hozzáfűzése
new_data = collect_new_data()
backend.append(new_data, "timeseries.parquet", schema_validation=True)
```

## Tesztelés

A `PolarsBackend`-et a [`tests/core/storage/backends/test_polars_backend.py`](../../../tests/core/storage/backends/test_polars_backend.py) teszteli, amely lefedi:

- Alapvető írási és olvasási műveletek
- Tömörítés és particionálás
- Sémavizsgálat és validáció
- Chunkolás és szűrés
- Hibakezelés és érvényesítés
- Lazy import funkcionalitás