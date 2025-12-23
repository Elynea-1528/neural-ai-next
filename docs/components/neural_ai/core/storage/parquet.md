# ParquetStorageService - Particionált Parquet Tároló

## 🎯 Áttekintés

A `ParquetStorageService` a Neural AI Next rendszer Big Data tároló komponense, amely particionált Parquet formátumban tárolja a Tick adatokat. A particionálás dátum és szimbólum alapú, ami lehetővé teszi a gyors és hatékony adatlekérdezést 25 évnyi Tick adatra.

## 📦 Jellemzők

### Főbb Képességek

- **Particionált Tárolás:** Dátum és szimbólum alapú particionálás (`/data/tick/EURUSD/tick/year=2023/month=12/day=23/`)
- **Aszinkron Műveletek:** Minden tárolási és olvasási művelet aszinkron
- **Adatintegritás:** Checksum ellenőrzés és validáció
- **Hatékony Lekérdezés:** Csak a szükséges partíciók betöltése
- **Tömörítés:** Snappy tömörítés a tárolási hely optimalizálásához
- **Több szimbólum támogatása:** EURUSD, GBPUSD, USDJPY, USDCHF, XAUUSD

### Technológiai Stack

- **Polars:** Gyors DataFrame feldolgozás
- **FastParquet:** Parquet fájlok kezelése
- **Loguru:** Strukturált naplózás
- **Asyncio:** Aszinkron műveletek

## 🏗️ Architektúra

### Partíciószerkezet

```
/data/tick/
├── EURUSD/
│   ├── tick/
│   │   ├── year=2023/
│   │   │   ├── month=12/
│   │   │   │   ├── day=01/
│   │   │   │   │   └── data.parquet
│   │   │   │   ├── day=02/
│   │   │   │   └── ...
│   │   │   └── year=2024/
│   │   └── ...
├── GBPUSD/
├── USDJPY/
├── USDCHF/
└── XAUUSD/
```

### Adatmodell

```python
class TickData(BaseModel):
    """Tick adat modell."""
    timestamp: datetime
    symbol: str
    bid: float
    ask: float
    volume: Optional[int] = None
    source: str  # 'jforex', 'mt5', 'ibkr'
    
    @property
    def spread(self) -> float:
        """Spread kiszámítása."""
        return self.ask - self.bid
    
    @property
    def mid_price(self) -> float:
        """Középár kiszámítása."""
        return (self.bid + self.ask) / 2
```

## 🔧 API Referencia

### Osztály: `ParquetStorageService`

#### Metódusok

##### `__init__()`

Inicializálja a ParquetStorageService-t.

```python
service = ParquetStorageService()
```

##### `store_tick_data(symbol: str, data: pl.DataFrame, date: datetime) -> None`

Tick adatok tárolása particionált Parquet formátumban.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma (pl. 'EURUSD')
- `data`: A Tick adatokat tartalmazó Polars DataFrame
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

await service.store_tick_data('EURUSD', data, datetime.now())
```

##### `read_tick_data(symbol: str, start_date: datetime, end_date: datetime) -> pl.DataFrame`

Tick adatok olvasása dátumtartományból.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:**
- A Tick adatokat tartalmazó Polars DataFrame

**Példa:**
```python
from datetime import datetime, timedelta

start = datetime(2023, 12, 1)
end = datetime(2023, 12, 31)

data = await service.read_tick_data('EURUSD', start, end)
print(f"Loaded {len(data)} ticks")
```

##### `get_available_dates(symbol: str) -> List[datetime]`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma

**Visszatérési érték:**
- Az elérhető dátumok listája

**Példa:**
```python
dates = await service.get_available_dates('EURUSD')
print(f"Available dates: {len(dates)}")
```

##### `calculate_checksum(symbol: str, date: datetime) -> str`

Adatok checksum számítása integritás ellenőrzéshez.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- A checksum SHA256 hash

**Példa:**
```python
checksum = await service.calculate_checksum('EURUSD', datetime.now())
print(f"Checksum: {checksum}")
```

##### `verify_data_integrity(symbol: str, date: datetime) -> bool`

Adatintegritás ellenőrzése.

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- `True` ha az adatok integritása megfelelő, egyébként `False`

**Példa:**
```python
is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
print(f"Data integrity: {is_valid}")
```

##### `get_storage_stats(symbol: Optional[str] = None) -> Dict[str, Any]`

Tárolási statisztikák lekérdezése.

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:**
- A statisztikákat tartalmazó dictionary

**Példa:**
```python
# Összes statisztika
stats = await service.get_storage_stats()
print(f"Total files: {stats['total_files']}")

# Csak egy szimbólum statisztikája
stats = await service.get_storage_stats('EURUSD')
```

## 🔍 Használati Példák

### 1. Alapvető Tárolás és Olvasás

```python
import asyncio
from datetime import datetime
import polars as pl
from neural_ai.core.storage.parquet import ParquetStorageService

async def main():
    service = ParquetStorageService()
    
    # Minta adatok létrehozása
    data = pl.DataFrame({
        'timestamp': [datetime(2023, 12, 23, 10, i, 0) for i in range(10)],
        'bid': [1.1000 + i * 0.0001 for i in range(10)],
        'ask': [1.1002 + i * 0.0001 for i in range(10)],
        'volume': [1000 + i * 100 for i in range(10)],
        'source': ['jforex'] * 10
    })
    
    # Adatok tárolása
    await service.store_tick_data('EURUSD', data, datetime(2023, 12, 23))
    
    # Adatok olvasása
    result = await service.read_tick_data(
        'EURUSD',
        datetime(2023, 12, 23, 9, 0, 0),
        datetime(2023, 12, 23, 11, 0, 0)
    )
    
    print(f"Loaded {len(result)} ticks")

asyncio.run(main())
```

### 2. Nagy Adathalmaz Tárolása

```python
async def store_large_dataset():
    service = ParquetStorageService()
    
    # Nagy adathalmaz létrehozása (1M tick)
    timestamps = [datetime.now() + timedelta(seconds=i) for i in range(1_000_000)]
    bids = [1.1000 + i * 0.000001 for i in range(1_000_000)]
    asks = [b + 0.0002 for b in bids]
    
    data = pl.DataFrame({
        'timestamp': timestamps,
        'bid': bids,
        'ask': asks,
        'volume': [1000] * 1_000_000,
        'source': ['mt5'] * 1_000_000
    })
    
    # Tárolás
    await service.store_tick_data('EURUSD', data, datetime.now())
    
    # Statisztikák lekérdezése
    stats = await service.get_storage_stats('EURUSD')
    print(f"Files: {stats['symbols']['EURUSD']['files']}")
    print(f"Size: {stats['symbols']['EURUSD']['size_gb']:.2f} GB")

asyncio.run(store_large_dataset())
```

### 3. Adatintegritás Ellenőrzése

```python
async def verify_data():
    service = ParquetStorageService()
    symbol = 'EURUSD'
    date = datetime(2023, 12, 23)
    
    # Integritás ellenőrzése
    is_valid = await service.verify_data_integrity(symbol, date)
    
    if is_valid:
        print("Data integrity: OK")
        
        # Checksum lekérdezése
        checksum = await service.calculate_checksum(symbol, date)
        print(f"Checksum: {checksum}")
    else:
        print("Data integrity: FAILED")

asyncio.run(verify_data())
```

### 4. Több Szimbólum Kezelése

```python
async def manage_multiple_symbols():
    service = ParquetStorageService()
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF', 'XAUUSD']
    
    for symbol in symbols:
        # Minta adatok létrehozása
        data = pl.DataFrame({
            'timestamp': [datetime.now()],
            'bid': [1.0],  # Placeholder értékek
            'ask': [1.0002],
            'volume': [1000],
            'source': ['jforex']
        })
        
        # Tárolás
        await service.store_tick_data(symbol, data, datetime.now())
    
    # Összes statisztika
    stats = await service.get_storage_stats()
    print(f"Total files: {stats['total_files']}")
    print(f"Total size: {stats['total_size_gb']:.2f} GB")
    
    # Szimbólumonkénti bontás
    for symbol, symbol_stats in stats['symbols'].items():
        print(f"{symbol}: {symbol_stats['files']} files, {symbol_stats['size_gb']:.2f} GB")

asyncio.run(manage_multiple_symbols())
```

## 🧪 Tesztelés

### Tesztfuttatás

```bash
# ParquetStorageService tesztek futtatása
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/test_parquet.py -v

# Teljes coverage
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/core/storage/test_parquet.py --cov=neural_ai.core.storage.parquet --cov-report=html
```

### Főbb Tesztesetek

1. **Alapvető tárolás és olvasás**
2. **Üres DataFrame kezelése**
3. **Hiányzó oszlopok kezelése**
4. **Nem létező adatok olvasása**
5. **Elérhető dátumok lekérdezése**
6. **Checksum számítás**
7. **Adatintegritás ellenőrzés**
8. **Tárolási statisztikák**
9. **Dátum szerinti szűrés**
10. **Több szimbólum kezelése**

## 🔗 Kapcsolódó Dokumentumok

- [Adattárház Specifikáció](docs/planning/specs/04_data_warehouse.md)
- [Storage Interface](docs/components/neural_ai/core/storage/interfaces/storage_interface.md)
- [Storage Factory](docs/components/neural_ai/core/storage/implementations/storage_factory.md)
- [Fejlesztési Útmutató](docs/development/unified_development_guide.md)

## 📝 Jegyzetek

- A Parquet formátum lehetővé teszi a hatékony tömörítést és gyors lekérdezést
- A particionálás jelentősen javítja a lekérdezési teljesítményt
- Az aszinkron műveletek optimalizálják a nagy adathalmazok kezelését
- A checksum ellenőrzés biztosítja az adatok integritását
- A Polars DataFrame-ek gyorsabbak mint a Pandas DataFrame-ek nagy adathalmazokon