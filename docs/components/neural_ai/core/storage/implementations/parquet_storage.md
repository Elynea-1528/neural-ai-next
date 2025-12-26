# ParquetStorageService

## Áttekintés

A `ParquetStorageService` egy particionált Parquet tároló szolgáltatás, amely a Tick adatok particionált Parquet formátumban történő tárolását és lekérdezését valósítja meg. A szolgáltatás hardver-gyorsítást detektál és automatikusan kiválasztja a legoptimálisabb backend-et (PolarsBackend AVX2 támogatással, vagy PandasBackend kompatibilitási módban).

## Osztály

```python
class ParquetStorageService(metaclass=SingletonMeta)
```

## Főbb Jellemzők

- **Particionált tárolás**: Dátum és szimbólum alapú particionálás
- **Hardver detekció**: Automatikus backend kiválasztás AVX2 támogatás alapján
- **Aszinkron műveletek**: Támogatja az aszinkron adatkezelést
- **Adatintegritás**: Checksum ellenőrzés és validáció
- **Singleton minta**: Csak egy példány létezik az alkalmazás élettartama alatt

## Inicializálás

```python
def __init__(
    self,
    base_path: str | Path | None = None,
    compression: str = "snappy",
    hardware: HardwareInterface | None = None
) -> None
```

**Paraméterek:**
- `base_path`: Az alapútvonal a tároláshoz (alapértelmezett: "/data/tick")
- `compression`: A tömörítési algoritmus (alapértelmezett: "snappy")
- `hardware`: A hardverképességek detektálásáért felelős interfész (opcionális)

**Attribútumok:**
- `BASE_PATH`: A tárolás alapútvonala
- `engine`: A Parquet engine ('fastparquet' vagy 'polars')
- `compression`: Tömörítési algoritmus ('snappy')
- `backend`: A kiválasztott tárolási backend

**Példa:**

```python
from neural_ai.core.storage import ParquetStorageService
from neural_ai.core.utils import HardwareFactory

# Alapértelmezett inicializálás
service = ParquetStorageService()

# Egyéni útvonallal
service = ParquetStorageService(base_path="/custom/tick/data")

# Egyéni tömörítéssel
service = ParquetStorageService(compression="gzip")

# Saját hardware interfésszel
hardware = HardwareFactory.get_hardware_interface()
service = ParquetStorageService(hardware=hardware)
```

## Backend Kiválasztás

A szolgáltatás automatikusan detektálja a hardver képességeket és kiválasztja a legoptimálisabb tárolási backend-et:

### PolarsBackend (AVX2 támogatással)
- **Előnyök**: Gyorsabb feldolgozás, jobb memóriakezelés
- **Használat**: Ha az AVX2 utasításkészlet elérhető

### PandasBackend (Kompatibilitási mód)
- **Előnyök**: Kompatibilis régebbi CPU-kkal
- **Használat**: Ha az AVX2 nem elérhető

**Példa a backend kiválasztásra:**

```python
service = ParquetStorageService()
print(f"Kiválasztott backend: {service.backend.name}")
print(f"Engine: {service.engine}")

# Kimenet példa:
# Kiválasztott backend: polars
# Engine: polars
# vagy
# Kiválasztott backend: pandas
# Engine: fastparquet
```

## Metódusok

### `store_tick_data()`

Tick adatok tárolása particionált Parquet formátumban.

```python
async def store_tick_data(
    self,
    symbol: str,
    data: Any,
    date: datetime
) -> None
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma (pl. 'EURUSD')
- `data`: A Tick adatokat tartalmazó DataFrame
- `date`: A dátum, ami alapján a particionálás történik

**Kivételek:**
- `ValueError`: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

**Szükséges Oszlopok:**
- `timestamp`: Időbélyeg
- `bid`: Bid ár
- `ask`: Ask ár

**Példa:**

```python
import polars as pl
from datetime import datetime

# Tick adatok létrehozása
data = pl.DataFrame({
    'timestamp': [datetime.now()],
    'bid': [1.1000],
    'ask': [1.1002],
    'volume': [1000],
    'source': ['jforex']
})

# Adatok tárolása
await service.store_tick_data('EURUSD', data, datetime.now())
```

### `read_tick_data()`

Tick adatok olvasása dátumtartományból.

```python
async def read_tick_data(
    self,
    symbol: str,
    start_date: datetime,
    end_date: datetime
) -> Any
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:**
- `Any`: A Tick adatokat tartalmazó DataFrame

**Példa:**

```python
from datetime import datetime, timedelta

# Dátumtartomány megadása
start = datetime(2023, 12, 1)
end = datetime(2023, 12, 31)

# Adatok betöltése
data = await service.read_tick_data('EURUSD', start, end)
print(f"Betöltött tickek száma: {len(data)}")

# Adatok feldolgozása
if len(data) > 0:
    print(f"Első tick: {data[0]['timestamp']}")
    print(f"Utolsó tick: {data[-1]['timestamp']}")
```

### `get_available_dates()`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

```python
async def get_available_dates(self, symbol: str) -> list[datetime]
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma

**Visszatérési érték:**
- `list[datetime]`: Az elérhető dátumok listája

**Példa:**

```python
# Elérhető dátumok lekérdezése
dates = await service.get_available_dates('EURUSD')
print(f"Elérhető dátumok száma: {len(dates)}")

# Dátumok kiírása
for date in dates[:10]:  # Első 10 dátum
    print(date.strftime("%Y-%m-%d"))
```

### `calculate_checksum()`

Adatok checksum számítása integritás ellenőrzéshez.

```python
async def calculate_checksum(
    self,
    symbol: str,
    date: datetime
) -> str
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- `str`: A checksum SHA256 hash

**Példa:**

```python
from datetime import datetime

# Checksum számítása
checksum = await service.calculate_checksum('EURUSD', datetime.now())
print(f"Checksum: {checksum}")

# Checksum ellenőrzése
expected_checksum = "abc123..."
if checksum == expected_checksum:
    print("Az adatok integritása megfelelő")
else:
    print("Az adatok sérültek lehetnek")
```

### `verify_data_integrity()`

Adatintegritás ellenőrzése.

```python
async def verify_data_integrity(
    self,
    symbol: str,
    date: datetime
) -> bool
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- `bool`: True ha az adatok integritása megfelelő, egyébként False

**Ellenőrzések:**
- Fájl létezés
- Nem üres DataFrame
- Szükséges oszlopok jelenléte
- Időbélyeg szerinti rendezés

**Példa:**

```python
from datetime import datetime

# Integritás ellenőrzése
is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
print(f"Adatintegritás: {'OK' if is_valid else 'HIBÁS'}")

# Több dátum ellenőrzése
dates = await service.get_available_dates('EURUSD')
for date in dates:
    is_valid = await service.verify_data_integrity('EURUSD', date)
    if not is_valid:
        print(f"Hibás adatok: {date}")
```

### `get_storage_stats()`

Tárolási statisztikák lekérdezése.

```python
async def get_storage_stats(
    self,
    symbol: str | None = None
) -> dict[str, Any]
```

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:**
- `dict[str, Any]`: A statisztikákat tartalmazó dictionary

**Statisztikák:**
- `total_files`: Összes fájl száma
- `total_size_gb`: Összes méret GB-ban
- `symbols`: Szimbólumonkénti statisztikák

**Példa:**

```python
# Összes statisztika
stats = await service.get_storage_stats()
print(f"Összes fájl: {stats['total_files']}")
print(f"Összes méret: {stats['total_size_gb']:.2f} GB")

# Szimbólumonkénti statisztikák
for symbol, symbol_stats in stats['symbols'].items():
    print(f"{symbol}: {symbol_stats['files']} fájl, {symbol_stats['size_gb']:.2f} GB")

# Egy szimbólum statisztikája
eurusd_stats = await service.get_storage_stats('EURUSD')
print(f"EURUSD fájlok: {eurusd_stats['total_files']}")
```

## Belső Metódusok

### `_select_backend()`

Backend kiválasztása hardver detekció alapján.

```python
def _select_backend(self) -> None
```

Ez a metódus felelős a megfelelő tárolási backend kiválasztásáért a hardver képességek alapján. Külön metódusba van kiszervezve, hogy a tesztek könnyen mockolhassák.

### `_get_path()`

Elérési út generálása a megadott szimbólumhoz és dátumhoz.

```python
def _get_path(self, symbol: str, date: datetime) -> Path
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- `Path`: A teljes elérési út a Parquet fájlhoz

**Útvonal formátum:**
```
{BASE_PATH}/{SYMBOL}/tick/year={YEAR}/month={MONTH}/day={DAY}/data.parquet
```

**Példa:**
```python
date = datetime(2023, 12, 23)
path = service._get_path('EURUSD', date)
# /data/tick/EURUSD/tick/year=2023/month=12/day=23/data.parquet
```

### `_read_parquet_async()`

Aszinkron Parquet olvasás.

```python
async def _read_parquet_async(self, path: Path) -> Any
```

### `_concat_dataframes()`

DataFrame-ek összefűzése a backend típusának megfelelően.

```python
def _concat_dataframes(self, dfs: list[Any]) -> Any
```

### `_filter_by_timestamp()`

DataFrame szűrése időbélyeg alapján.

```python
def _filter_by_timestamp(
    self,
    data: Any,
    start_date: datetime,
    end_date: datetime
) -> Any
```

## Komplex Példák

### Több szimbólum adatainak kezelése

```python
from datetime import datetime, timedelta

symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
start_date = datetime(2023, 12, 1)
end_date = datetime(2023, 12, 31)

# Adatok betöltése minden szimbólumhoz
for symbol in symbols:
    print(f"Betöltés: {symbol}")
    data = await service.read_tick_data(symbol, start_date, end_date)
    print(f"  Tickek száma: {len(data)}")
    
    # Integritás ellenőrzés
    dates = await service.get_available_dates(symbol)
    valid_count = 0
    for date in dates:
        if await service.verify_data_integrity(symbol, date):
            valid_count += 1
    print(f"  Érvényes napok: {valid_count}/{len(dates)}")
```

### Adatok mentése és ellenőrzése

```python
import polars as pl
from datetime import datetime

# Tick adatok generálása
def generate_tick_data(symbol: str, date: datetime, count: int = 1000):
    timestamps = [date + timedelta(seconds=i) for i in range(count)]
    return pl.DataFrame({
        'timestamp': timestamps,
        'bid': [1.1000 + i * 0.0001 for i in range(count)],
        'ask': [1.1002 + i * 0.0001 for i in range(count)],
        'volume': [1000] * count,
        'source': ['jforex'] * count
    })

# Adatok mentése
symbol = 'EURUSD'
date = datetime(2023, 12, 25)
data = generate_tick_data(symbol, date)

print("Adatok mentése...")
await service.store_tick_data(symbol, data, date)

# Ellenőrzés
print("Integritás ellenőrzése...")
is_valid = await service.verify_data_integrity(symbol, date)
print(f"Integritás: {'OK' if is_valid else 'HIBÁS'}")

# Checksum ellenőrzés
checksum = await service.calculate_checksum(symbol, date)
print(f"Checksum: {checksum}")
```

### Statisztikák és monitoring

```python
from datetime import datetime

# Teljes tárolási statisztika
stats = await service.get_storage_stats()
print("=== Tárolási Statisztikák ===")
print(f"Összes fájl: {stats['total_files']}")
print(f"Összes méret: {stats['total_size_gb']:.2f} GB")
print()

# Szimbólumonkénti részletek
print("=== Szimbólumonkénti Statisztikák ===")
for symbol, symbol_stats in sorted(stats['symbols'].items()):
    print(f"{symbol}:")
    print(f"  Fájlok: {symbol_stats['files']}")
    print(f"  Méret: {symbol_stats['size_gb']:.2f} GB")

# Elérhető dátumok ellenőrzése
symbol = 'EURUSD'
dates = await service.get_available_dates(symbol)
if dates:
    print(f"\n{symbol} elérhető dátumai:")
    print(f"  Első dátum: {dates[0].strftime('%Y-%m-%d')}")
    print(f"  Utolsó dátum: {dates[-1].strftime('%Y-%m-%d')}")
    print(f"  Összes nap: {len(dates)}")
else:
    print(f"\n{symbol} esetén nincsenek elérhető dátumok")
```

### Batch műveletek

```python
import asyncio
from datetime import datetime, timedelta

# Több dátum adatainak egyszerre történő ellenőrzése
async def batch_verify_integrity(symbol: str, dates: list[datetime]):
    tasks = [
        service.verify_data_integrity(symbol, date)
        for date in dates
    ]
    results = await asyncio.gather(*tasks)
    
    valid_count = sum(results)
    total_count = len(results)
    
    print(f"Érvényes adatok: {valid_count}/{total_count}")
    return results

# Használat
symbol = 'EURUSD'
dates = await service.get_available_dates(symbol)
if dates:
    # Utolsó 7 nap ellenőrzése
    recent_dates = dates[-7:]
    results = await batch_verify_integrity(symbol, recent_dates)
    
    # Hibás dátumok listázása
    invalid_dates = [
        date for date, is_valid in zip(recent_dates, results) if not is_valid
    ]
    if invalid_dates:
        print("Hibás dátumok:")
        for date in invalid_dates:
            print(f"  {date.strftime('%Y-%m-%d')}")
```

## Best Practices

1. **Aszinkron használat**: Mindig használjuk az aszinkron metódusokat
2. **Integritás ellenőrzés**: Ellenőrizzük az adatok integritását mentés után
3. **Dátumtartomány**: Használjunk pontos dátumtartományt a `read_tick_data`-hoz
4. **Backend figyelés**: Monitorozzuk a backend teljesítményét
5. **Statisztikák**: Rendszeresen ellenőrizzük a tárolási statisztikákat
6. **Checksum**: Használjuk a checksum ellenőrzést kritikus adatok esetén

## Teljesítmény Optimalizálás

### PolarsBackend (ajánlott)
- **Előnyök**: 
  - Gyorsabb feldolgozás
  - Jobb memóriakezelés
  - AVX2 gyorsítás
- **Használat**: Automatikusan kiválasztódik, ha az AVX2 elérhető

### PandasBackend (kompatibilitás)
- **Előnyök**: 
  - Kompatibilis régebbi hardverrel
  - Stabil működés
- **Használat**: Automatikusan kiválasztódik, ha az AVX2 nem elérhető

### Tömörítés
- **Snappy** (alapértelmezett): Gyors tömörítés, jó arány
- **Gzip**: Jobb tömörítési arány, lassabb feldolgozás