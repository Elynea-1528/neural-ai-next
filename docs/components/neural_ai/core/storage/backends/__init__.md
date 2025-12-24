# Storage Backends Modul

## Áttekintés

A Storage Backends modul a Neural AI Next rendszer tárolási rétegének bővíthető alapja. Különböző DataFrame könyvtárakhoz (Polars, Pandas) nyújt implementációkat, amelyek a Parquet formátumot használják a hatékony adattároláshoz.

## Főbb Jellemzők

### Támogatott Backend-ek

- **PolarsBackend**: Polars DataFrame-ekhez, PyArrow Parquet használatával
- **PandasBackend**: Pandas DataFrame-ekhez, FastParquet használatával

### Közös Funkcionalitás

- **Parquet Formátum**: Mindkét backend a Parquet formátumot használja optimalizált tároláshoz
- **Lazy Import**: A nehéz könyvtárak csak akkor töltődnek be, amikor szükség van rájuk
- **Chunkolás**: Nagy adathalmazok hatékony feldolgozása
- **Particionálás**: Dátum és szimbólum alapú particionálás támogatása
- **Aszinkron Műveletek**: Mindkét backend támogatja az aszinkron műveleteket

## Architektúra

### Osztálydiagram

```
StorageBackend (Absztrakt)
├── PolarsBackend
│   ├── _polars_wrapper: PolarsDataFrame
│   ├── write()
│   ├── read()
│   ├── append()
│   └── get_info()
└── PandasBackend
    ├── _pandas_wrapper: PandasDataFrame
    ├── write()
    ├── read()
    ├── append()
    └── get_info()
```

### DataFrameType Protokoll

A backend-ek egy közös `DataFrameType` protokollt használnak, amely garantálja a kompatibilitást:

```python
class DataFrameType(Protocol):
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

## Használat

### Alapvető Példa

```python
from neural_ai.core.storage.backends import PolarsBackend, PandasBackend

# Polars backend használata
polars_backend = PolarsBackend()
polars_backend.write(data, "path/to/file.parquet")

# Pandas backend használata
pandas_backend = PandasBackend()
pandas_backend.write(data, "path/to/file.parquet")
```

### Konfigurációs Opciók

#### Írási Opciók

```python
# Tömörítés beállítása
backend.write(data, path, compression="snappy")

# Particionálás
backend.write(data, path, partition_by=["year", "month"])

# Index mentése (Pandas)
backend.write(data, path, index=True)
```

#### Olvasási Opciók

```python
# Csak bizonyos oszlopok betöltése
data = backend.read(path, columns=["timestamp", "bid", "ask"])

# Szűrés partíciókra
filters = [("year", "=", 2023), ("month", "=", 12)]
data = backend.read(path, filters=filters)

# Chunkolás
data = backend.read(path, chunk_size=10000)
```

## Backend Összehasonlítás

| Funkció | PolarsBackend | PandasBackend |
|---------|---------------|---------------|
| Alapkönyvtár | Polars | Pandas |
| Parquet Engine | PyArrow | FastParquet |
| Teljesítmény | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Memóriahatékonyság | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Chunkolás Támogatás | Igen | Igen |
| Particionálás | Igen | Igen |
| Lazy Import | Igen | Igen |

## Fejlesztés

### Új Backend Hozzáadása

1. Hozz létre egy új osztályt, amely a `StorageBackend`-ből származik
2. Implementáld az összes absztrakt metódust
3. Használj lazy importot a nehéz könyvtárakhoz
4. Add hozzá az osztályt a `__init__.py`-hoz
5. Írj teszteket a új backend-hez

### Példa Új Backend-re

```python
class CustomBackend(StorageBackend):
    def __init__(self):
        super().__init__(name="custom", supported_formats=["parquet"])
        self._wrapper = CustomDataFrame()
    
    def write(self, data: DataFrameType, path: str, **kwargs) -> None:
        # Implementáció
        pass
    
    def read(self, path: str, **kwargs) -> DataFrameType:
        # Implementáció
        pass
    
    # További metódusok...
```

## Kapcsolódó Dokumentumok

- [Base Backend](base.md) - Az absztrakt alaposztály részletes leírása
- [Polars Backend](polars_backend.md) - A Polars implementáció dokumentációja
- [Pandas Backend](pandas_backend.md) - A Pandas implementáció dokumentációja
- [Parquet Storage](../parquet.md) - A magas szintű Parquet tároló szolgáltatás
- [Storage Interface](../interfaces/storage_interface.md) - A tárolási interfész

## Tesztelés

A backend-ek tesztelése:

```bash
# Összes backend tesztje
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/ -v

# Csak Polars backend
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_polars_backend.py -v

# Csak Pandas backend
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/backends/test_pandas_backend.py -v
```

## Jegyzetek

- A backend-ek lazy importot használnak, így a nehéz könyvtárak csak akkor töltődnek be, amikor szükség van rájuk
- Mindkét backend támogatja a particionált tárolást, ami jelentősen javítja a lekérdezési teljesítményt
- A Polars backend általában gyorsabb és memóriahatékonyabb nagy adathalmazokon
- A Pandas backend jobb választás, ha kompatibilitásra van szükség más Pandas alapú eszközökkel