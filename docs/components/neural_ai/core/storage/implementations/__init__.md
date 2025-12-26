# Storage Implementációk

## Áttekintés

Ez a csomag a Storage komponens konkrét implementációit tartalmazza. Minden implementáció megvalósítja a [`StorageInterface`](../interfaces/storage_interface.md)-t, és a [`StorageFactory`](../factory.md) által használható.

## Elérhető Implementációk

### [`FileStorage`](file_storage.md)
Fájlrendszer alapú tárolási implementáció, amely támogatja a CSV, Excel és JSON formátumokat.

### [`ParquetStorageService`](parquet_storage.md)
Particionált Parquet tároló szolgáltatás Tick adatokhoz, hardver-gyorsítással és automatikus backend kiválasztással.

## Használat

### Alapvető Használat

```python
from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService

# FileStorage használata
file_storage = FileStorage(base_path="/data")
file_storage.save_dataframe(df, "data.csv")

# ParquetStorageService használata
parquet_service = ParquetStorageService()
await parquet_service.store_tick_data("EURUSD", tick_data, datetime.now())
```

### Factory Használata

```python
from neural_ai.core.storage import StorageFactory

# FileStorage létrehozása
file_storage = StorageFactory.get_storage("file", base_path="/data")

# ParquetStorageService létrehozása
parquet_service = StorageFactory.get_storage("parquet", base_path="/tick/data")
```

## Implementációk Összehasonlítása

| Jellemző | FileStorage | ParquetStorageService |
|----------|-------------|----------------------|
| **Cél** | Általános adattárolás | Tick adatok particionált tárolása |
| **Formátumok** | CSV, Excel, JSON | Parquet |
| **Particionálás** | Nem | Igen (dátum, szimbólum) |
| **Backend** | Nincs | Polars/Pandas (automatikus) |
| **Aszinkron** | Nem | Igen |
| **Hardver gyorsítás** | Nem | Igen (AVX2) |
| **Használati eset** | Konfigurációk, általános adatok | Nagy mennyiségű időbeli adat |

## Példák

### FileStorage Használata

```python
from neural_ai.core.storage.implementations import FileStorage
import pandas as pd

# Inicializálás
storage = FileStorage(base_path="/data")

# DataFrame mentése
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["Budapest", "Debrecen", "Szeged"]
})
storage.save_dataframe(df, "users.csv")

# Objektum mentése
config = {
    "database": {"host": "localhost", "port": 5432},
    "logging": {"level": "INFO"}
}
storage.save_object(config, "config.json")

# Adatok betöltése
loaded_df = storage.load_dataframe("users.csv")
loaded_config = storage.load_object("config.json")
```

### ParquetStorageService Használata

```python
import asyncio
import polars as pl
from datetime import datetime, timedelta
from neural_ai.core.storage.implementations import ParquetStorageService

async def main():
    # Inicializálás
    service = ParquetStorageService(base_path="/tick/data")
    
    # Tick adatok létrehozása
    tick_data = pl.DataFrame({
        "timestamp": pl.date_range("2023-12-25", "2023-12-26", "1min"),
        "bid": [1.0 + i * 0.0001 for i in range(1440)],
        "ask": [1.0002 + i * 0.0001 for i in range(1440)],
        "volume": [1000] * 1440,
        "source": ["jforex"] * 1440
    })
    
    # Adatok tárolása
    await service.store_tick_data("EURUSD", tick_data, datetime(2023, 12, 25))
    
    # Adatok betöltése
    start_date = datetime(2023, 12, 25)
    end_date = datetime(2023, 12, 26)
    loaded_data = await service.read_tick_data("EURUSD", start_date, end_date)
    
    print(f"Betöltött tickek: {len(loaded_data)}")
    
    # Integritás ellenőrzés
    is_valid = await service.verify_data_integrity("EURUSD", datetime(2023, 12, 25))
    print(f"Adatintegritás: {'OK' if is_valid else 'HIBÁS'}")

# Futtatás
asyncio.run(main())
```

### Kombinált Használat

```python
import asyncio
import pandas as pd
import polars as pl
from datetime import datetime
from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService

async def process_and_store_data():
    # Inicializálás
    file_storage = FileStorage(base_path="/data")
    parquet_service = ParquetStorageService(base_path="/tick/data")
    
    # Konfiguráció betöltése
    config = file_storage.load_object("config.json")
    
    # Tick adatok generálása
    tick_data = pl.DataFrame({
        "timestamp": pl.date_range("2023-12-25", "2023-12-26", "1min"),
        "bid": [1.0 + i * 0.0001 for i in range(1440)],
        "ask": [1.0002 + i * 0.0001 for i in range(1440)],
        "volume": [1000] * 1440
    })
    
    # Adatok tárolása Parquet-ban
    await parquet_service.store_tick_data("EURUSD", tick_data, datetime(2023, 12, 25))
    
    # Statisztikák mentése JSON-ban
    stats = {
        "symbol": "EURUSD",
        "date": "2023-12-25",
        "ticks": len(tick_data),
        "avg_bid": float(tick_data["bid"].mean()),
        "avg_ask": float(tick_data["ask"].mean())
    }
    file_storage.save_object(stats, "daily_stats.json")
    
    # Adatok betöltése és aggregálás
    start_date = datetime(2023, 12, 25)
    end_date = datetime(2023, 12, 26)
    loaded_data = await parquet_service.read_tick_data("EURUSD", start_date, end_date)
    
    # Aggregált adatok mentése CSV-ként
    aggregated_df = pd.DataFrame({
        "metric": ["min_bid", "max_bid", "avg_bid", "total_volume"],
        "value": [
            float(loaded_data["bid"].min()),
            float(loaded_data["bid"].max()),
            float(loaded_data["bid"].mean()),
            int(loaded_data["volume"].sum())
        ]
    })
    file_storage.save_dataframe(aggregated_df, "aggregated_stats.csv")

# Futtatás
asyncio.run(process_and_store_data())
```

## Bővíthetőség

### Egyéni Implementáció Hozzáadása

```python
from neural_ai.core.storage.interfaces import StorageInterface
from neural_ai.core.storage import StorageFactory
import pandas as pd

class CustomStorage(StorageInterface):
    """Egyéni tárolási implementáció."""
    
    def __init__(self, custom_param: str):
        self.custom_param = custom_param
    
    def save_dataframe(self, df: pd.DataFrame, path: str, **kwargs):
        # Egyéni implementáció
        pass
    
    def load_dataframe(self, path: str, **kwargs) -> pd.DataFrame:
        # Egyéni implementáció
        pass
    
    # További metódusok implementációja...

# Regisztrálás a factory-ban
StorageFactory.register_storage("custom", CustomStorage)

# Használat
custom_storage = StorageFactory.get_storage("custom", custom_param="value")
```

## Exportált Osztályok

A modul a következő osztályokat exportálja:

- `FileStorage`: Fájlrendszer alapú tároló
- `ParquetStorageService`: Particionált Parquet tároló szolgáltatás

## Best Practices

### 1. Megfelelő Implementáció Kiválasztása

```python
from neural_ai.core.storage.implementations import FileStorage, ParquetStorageService

def get_storage_implementation(data_type: str):
    """Visszaadja a megfelelő tárolási implementációt."""
    if data_type == "tick":
        return ParquetStorageService()
    elif data_type == "config":
        return FileStorage(base_path="/config")
    else:
        return FileStorage(base_path="/data")
```

### 2. Hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageNotFoundError,
    StorageIOError
)

try:
    storage.save_dataframe(df, "data.csv")
except StorageNotFoundError:
    # Fájl nem található
    storage.save_dataframe(df, "data.csv")
except StorageIOError as e:
    # IO hiba
    logger.error(f"IO hiba: {e}")
    raise
except StorageError as e:
    # Általános storage hiba
    logger.error(f"Storage hiba: {e}")
    raise
```

### 3. Aszinkron Használat

```python
import asyncio
from neural_ai.core.storage.implementations import ParquetStorageService

async def process_tick_data():
    service = ParquetStorageService()
    
    # Több szimbólum párhuzamos feldolgozása
    symbols = ["EURUSD", "GBPUSD", "USDJPY"]
    tasks = [
        service.read_tick_data(symbol, start_date, end_date)
        for symbol in symbols
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Futtatás
data = asyncio.run(process_tick_data())
```

### 4. Teljesítmény Optimalizálás

```python
from neural_ai.core.storage.implementations import ParquetStorageService
from neural_ai.core.utils import HardwareFactory

# Hardver alapú optimalizálás
hardware = HardwareFactory.get_hardware_interface()
service = ParquetStorageService(hardware=hardware)

# Backend információ
print(f"Kiválasztott backend: {service.backend.name}")
print(f"Engine: {service.engine}")
```

## Tesztelés

### Unit Tesztelés

```python
import unittest
from unittest.mock import Mock, patch
from neural_ai.core.storage.implementations import FileStorage

class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage(base_path="/test")
    
    def test_save_dataframe(self):
        import pandas as pd
        df = pd.DataFrame({"col": [1, 2, 3]})
        
        # Tesztelés
        self.storage.save_dataframe(df, "test.csv")
        
        # Ellenőrzés
        loaded_df = self.storage.load_dataframe("test.csv")
        self.assertEqual(len(loaded_df), 3)
    
    def test_load_nonexistent_file(self):
        with self.assertRaises(StorageNotFoundError):
            self.storage.load_dataframe("nonexistent.csv")
```

### Integration Tesztelés

```python
import asyncio
import polars as pl
from datetime import datetime
from neural_ai.core.storage.implementations import ParquetStorageService

async def test_parquet_storage():
    service = ParquetStorageService(base_path="/test/tick")
    
    # Tesztadatok
    test_data = pl.DataFrame({
        "timestamp": pl.date_range("2023-12-25", "2023-12-26", "1h"),
        "bid": [1.0] * 25,
        "ask": [1.0002] * 25,
        "volume": [1000] * 25
    })
    
    # Tárolás
    await service.store_tick_data("TEST", test_data, datetime(2023, 12, 25))
    
    # Betöltés
    loaded_data = await service.read_tick_data(
        "TEST",
        datetime(2023, 12, 25),
        datetime(2023, 12, 26)
    )
    
    # Ellenőrzés
    assert len(loaded_data) == 25
    assert "bid" in loaded_data.columns
    assert "ask" in loaded_data.columns
    
    # Integritás ellenőrzés
    is_valid = await service.verify_data_integrity("TEST", datetime(2023, 12, 25))
    assert is_valid
    
    print("Integration teszt sikeres!")

# Futtatás
asyncio.run(test_parquet_storage())