# ParquetStorageService - Particionált Parquet tároló szolgáltatás

## Áttekintés

A `ParquetStorageService` egy fejlett, particionált Parquet tároló szolgáltatás, amely automatikusan detektálja a hardver képességeket és kiválasztja a legoptimálisabb tárolási backend-et a Neural AI Next rendszer számára.

## Főbb jellemzők

- **Hardver-gyorsítás detektálás**: Automatikusan észleli az AVX2 utasításkészlet támogatást
- **Backend selector**: Dinamikusan választja ki a legjobb backend-et (PolarsBackend vagy PandasBackend)
- **Particionált tárolás**: Dátum és szimbólum alapú particionálás a gyors lekérdezés érdekében
- **Aszinkron műveletek**: Támogatja az aszinkron adatolvasást és -írást
- **Adatintegritás ellenőrzés**: Checksum számítás és adatintegritás ellenőrzés

## Architektúra

### Backend Selector Mechanizmus

A szolgáltatás a következő logika alapján választja ki a tárolási backend-et:

1. **AVX2 támogatás esetén**: `PolarsBackend` használata gyorsabb feldolgozáshoz
2. **AVX2 hiánya esetén**: `PandasBackend` használata kompatibilitási módban

```python
if has_avx2():
    self.backend = PolarsBackend()
    self.engine = "polars"
    logger.info("AVX2 support detected. Using PolarsBackend for accelerated data processing.")
else:
    self.backend = PandasBackend()
    logger.warning("Legacy CPU detected. Running in Compatibility Mode with PandasBackend.")
```

### Osztályszerkezet

```python
class ParquetStorageService(StorageInterface, metaclass=SingletonMeta):
    BASE_PATH = Path("/data/tick")
    
    def __init__(self) -> None:
        self.engine = "fastparquet"
        self.compression = "snappy"
        self.backend: StorageBackend
        # ... backend kiválasztás
```

## Metódusok

### `__init__()`

Inicializálja a ParquetStorageService-t backend selectorral.

**Paraméterek**: Nincs

**Visszatérési érték**: `None`

### `store_tick_data(symbol: str, data: Any, date: datetime) -> None`

Tick adatok tárolása particionált Parquet formátumban.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma (pl. 'EURUSD')
- `data`: A Tick adatokat tartalmazó DataFrame
- `date`: A dátum, ami alapján a particionálás történik

**Kivételek:**
- `ValueError`: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

**Példa:**
```python
import polars as pl
from datetime import datetime

data = pl.DataFrame({
    'timestamp': [datetime.now()],
    'bid': [1.1000],
    'ask': [1.1002],
    'volume': [1000],
    'source': ['jforex']
})

service = ParquetStorageService()
await service.store_tick_data('EURUSD', data, datetime.now())
```

### `read_tick_data(symbol: str, start_date: datetime, end_date: datetime) -> Any`

Tick adatok olvasása dátumtartományból.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:** A Tick adatokat tartalmazó DataFrame

**Példa:**
```python
from datetime import datetime, timedelta

service = ParquetStorageService()
start = datetime(2023, 12, 1)
end = datetime(2023, 12, 31)

data = await service.read_tick_data('EURUSD', start, end)
print(f"Loaded {len(data)} ticks")
```

### `get_available_dates(symbol: str) -> list[datetime]`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma

**Visszatérési érték:** Az elérhető dátumok listája

### `calculate_checksum(symbol: str, date: datetime) -> str`

Adatok checksum számítása integritás ellenőrzéshez.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:** A checksum SHA256 hash

### `verify_data_integrity(symbol: str, date: datetime) -> bool`

Adatintegritás ellenőrzése.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:** `True` ha az adatok integritása megfelelő, egyébként `False`

### `get_storage_stats(symbol: str | None = None) -> dict[str, Any]`

Tárolási statisztikák lekérdezése.

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:** A statisztikákat tartalmazó dictionary

## Particionálási stratégia

A tárolás a következő mappaszerkezetet követi:

```
/data/tick/{SYMBOL}/tick/year={YEAR}/month={MONTH}/day={DAY}/data.parquet
```

**Példa:**
```
/data/tick/EURUSD/tick/year=2023/month=12/day=23/data.parquet
```

## Backend kompatibilitás

### PolarsBackend (AVX2 támogatással)

- **Előnyök**: Gyorsabb feldolgozás, jobb memóriakezelés
- **Használati feltétel**: AVX2 utasításkészlet támogatás

### PandasBackend (Kompatibilitási mód)

- **Előnyök**: Széles körű kompatibilitás, minden CPU-n fut
- **Használati feltétel**: Nincs speciális hardverkövetelmény

## Függőségek

- `neural_ai.core.base.interfaces.StorageInterface`
- `neural_ai.core.base.singleton.SingletonMeta`
- `neural_ai.core.utils.hardware.has_avx2`
- `neural_ai.core.storage.backends.polars_backend.PolarsBackend`
- `neural_ai.core.storage.backends.pandas_backend.PandasBackend`

## Verzió történet

- **2.0.0**: Backend selector implementáció, hardver-gyorsítás detektálás
- **1.0.0**: Alapvető Parquet tároló szolgáltatás

## Kapcsolódó dokumentáció

- [`neural_ai/core/storage/backends/base.md`](base.md) - Storage Backend alaposztály
- [`neural_ai/core/storage/backends/polars_backend.md`](backends/polars_backend.md) - PolarsBackend dokumentáció
- [`neural_ai/core/storage/backends/pandas_backend.md`](backends/pandas_backend.md) - PandasBackend dokumentáció
- [`neural_ai/core/utils/hardware.md`](../utils/hardware.md) - Hardver detekciós segédfunkciók