# Storage Modul

## Áttekintés

A Storage modul felelős az adattárolásért és -kezelésért a rendszerben. Támogatja a különböző tárolási backend-eket (Pandas, Polars) és formátumokat (Parquet, CSV, Excel, JSON) a hatékony adatkezelés érdekében.

## Architektúra

A modul követi az architektúra szabványokat:

- **Interfaces**: [`storage_interface.py`](../../../neural_ai/core/storage/interfaces/storage_interface.py), [`factory_interface.py`](../../../neural_ai/core/storage/interfaces/factory_interface.py)
- **Implementations**: [`file_storage.py`](../../../neural_ai/core/storage/implementations/file_storage.py), [`parquet_storage.py`](../../../neural_ai/core/storage/implementations/parquet_storage.py)
- **Backends**: [`pandas_backend.py`](../../../neural_ai/core/storage/backends/pandas_backend.py), [`polars_backend.py`](../../../neural_ai/core/storage/backends/polars_backend.py)
- **Factory**: [`factory.py`](../../../neural_ai/core/storage/factory.py)
- **Exceptions**: [`exceptions`](../../../neural_ai/core/storage/exceptions/)

## Fő komponensek

### StorageFactory

A [`StorageFactory`](factory.md) felelős a különböző storage implementációk létrehozásáért a factory minta segítségével.

### FileStorage

A [`FileStorage`](implementations/file_storage.md) fájlrendszer alapú tárolást biztosít, támogatva a CSV, Excel és JSON formátumokat.

### ParquetStorageService

A [`ParquetStorageService`](implementations/parquet_storage.md) speciális Parquet formátumú tárolást nyújt, automatikusan kiválasztva a legjobb backend-et (Pandas vagy Polars) a hardver képességek alapján.

### Storage Backend-ek

- [`PandasBackend`](backends/pandas_backend.md): Pandas alapú Parquet tárolás
- [`PolarsBackend`](backends/polars_backend.md): Polars alapú gyorsított Parquet tárolás (AVX2 támogatással)

## Használati példák

### Alap storage létrehozása

```python
from neural_ai.core.storage.factory import StorageFactory

# File storage létrehozása
file_storage = StorageFactory.get_storage("file", base_path="data")

# Parquet storage létrehozása
parquet_storage = StorageFactory.get_storage("parquet", base_path="data")
```

### Adatok mentése és betöltése

```python
import pandas as pd

# DataFrame mentése
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
file_storage.save_dataframe(df, "test.csv")

# DataFrame betöltése
loaded_df = file_storage.load_dataframe("test.csv")
```

### Objektumok mentése

```python
# Python objektum mentése
data = {'key': 'value', 'number': 42}
file_storage.save_object(data, "config.json")

# Objektum betöltése
loaded_data = file_storage.load_object("config.json")
```

## Tesztelés

A modul átfogó tesztelésen esik át:

- **Unit tesztek**: [`tests/core/storage/`](../../../tests/core/storage/)
  - [`test_factory.py`](../../../tests/core/storage/test_factory.py) - StorageFactory tesztjei
  - [`implementations/test_file_storage.py`](../../../tests/core/storage/implementations/test_file_storage.py) - FileStorage tesztjei
  - [`implementations/test_parquet_storage.py`](../../../tests/core/storage/implementations/test_parquet_storage.py) - ParquetStorageService tesztjei
  - [`backends/test_pandas_backend.py`](../../../tests/core/storage/backends/test_pandas_backend.py) - PandasBackend tesztjei
  - [`backends/test_polars_backend.py`](../../../tests/core/storage/backends/test_polars_backend.py) - PolarsBackend tesztjei

## Jellemzők

- **Támogatott formátumok**: Parquet, CSV, Excel, JSON
- **Backend auto-detection**: Automatikus backend kiválasztás hardver képességek alapján
- **Lazy loading**: A nehéz könyvtárak (polars, pyarrow) csak szükség esetén töltődnek be
- **Tömörítés**: Támogatja a Snappy, Gzip és egyéb tömörítési algoritmusokat
- **Particionálás**: Támogatja a particionált tárolást dátum és egyéb kritériumok alapján
- **Adatintegritás**: Checksum ellenőrzés és validáció

## Függőségek

- `pandas`: DataFrame kezelés
- `polars`: Gyorsított DataFrame kezelés (opcionális, AVX2 támogatással)
- `pyarrow`: Parquet formátum támogatás
- `fastparquet`: Alternatív Parquet backend
- `openpyxl`: Excel formátum támogatás