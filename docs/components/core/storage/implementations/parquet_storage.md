# ParquetStorageService - Particionált Parquet tároló szolgáltatás

## Áttekintés

A `ParquetStorageService` egy particionált Parquet formátumú tároló szolgáltatás, amely a Neural AI Next rendszer Tick adatainak tárolásáért és lekérdezéséért felelős. A szolgáltatás dátum és szimbólum alapú particionálást használ a gyors lekérdezés érdekében.

## Főbb jellemzők

- **Hardver-gyorsítás detekció**: Automatikusan kiválasztja a legoptimálisabb backend-et
  - PolarsBackend: AVX2 támogatással gyorsabb feldolgozás
  - PandasBackend: Kompatibilitási mód régebbi CPU-khoz
- **Particionált tárolás**: Dátum és szimbólum alapú particionálás
- **Aszinkron műveletek**: Hatékony adatfeldolgozás nagy adathalmazokhoz
- **Integritás ellenőrzés**: Checksum számítás és adatintegritás ellenőrzése
- **Tömörítés**: Snappy tömörítés támogatása

## Architektúra

### Osztály szerkezet

```python
class ParquetStorageService(metaclass=SingletonMeta):
    """Particionált Parquet tároló szolgáltatás backend selectorral."""
    
    def __init__(
        self,
        base_path: str | Path | None = None,
        compression: str = "snappy",
        hardware: "HardwareInterface | None" = None,
    ) -> None
```

### Attribútumok

- `BASE_PATH`: A tárolás alapútvonala (alapértelmezett: `/data/tick`)
- `engine`: A Parquet engine ('fastparquet' vagy 'polars')
- `compression`: Tömörítési algoritmus ('snappy')
- `backend`: A kiválasztott tárolási backend

## Metódusok

### `__init__`

Inicializálja a ParquetStorageService-t backend selectorral.

**Paraméterek:**
- `base_path`: Az alapútvonal a tároláshoz (opcionális)
- `compression`: A tömörítési algoritmus (alapértelmezett: 'snappy')
- `hardware`: A hardverképességek detektálásáért felelős interfész (opcionális)

### `store_tick_data`

Tick adatok tárolása particionált Parquet formátumban.

```python
async def store_tick_data(
    self, 
    symbol: str, 
    data: "pd.DataFrame | pl.DataFrame", 
    date: datetime
) -> None
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `data`: A Tick adatokat tartalmazó DataFrame
- `date`: A dátum, ami alapján a particionálás történik

**Kivételek:**
- `ValueError`: Ha a DataFrame üres vagy nem tartalmazza a szükséges oszlopokat

### `read_tick_data`

Tick adatok olvasása dátumtartományból.

```python
async def read_tick_data(
    self, 
    symbol: str, 
    start_date: datetime, 
    end_date: datetime
) -> "pd.DataFrame | pl.DataFrame"
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `start_date`: A kezdő dátum
- `end_date`: A záró dátum

**Visszatérési érték:**
- A Tick adatokat tartalmazó DataFrame

### `get_available_dates`

Elérhető dátumok lekérdezése egy adott szimbólumhoz.

```python
async def get_available_dates(self, symbol: str) -> list[datetime]
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma

**Visszatérési érték:**
- Az elérhető dátumok listája

### `calculate_checksum`

Adatok checksum számítása integritás ellenőrzéshez.

```python
async def calculate_checksum(self, symbol: str, date: datetime) -> str
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- A checksum SHA256 hash

### `verify_data_integrity`

Adatintegritás ellenőrzése.

```python
async def verify_data_integrity(self, symbol: str, date: datetime) -> bool
```

**Paraméterek:**
- `symbol`: A pénzpár szimbóluma
- `date`: A dátum

**Visszatérési érték:**
- True ha az adatok integritása megfelelő, egyébként False

### `get_storage_stats`

Tárolási statisztikák lekérdezése.

```python
async def get_storage_stats(self, symbol: str | None = None) -> dict[str, Any]
```

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:**
- A statisztikákat tartalmazó dictionary

## Használati példák

### Inicializálás

```python
from neural_ai.core.storage.implementations.parquet_storage import ParquetStorageService
from datetime import datetime

# Alapértelmezett inicializálás
service = ParquetStorageService()

# Egyéni útvonallal
service = ParquetStorageService(base_path="/custom/path")
```

### Adatok tárolása

```python
import polars as pl
from datetime import datetime

# DataFrame létrehozása
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

### Adatok olvasása

```python
from datetime import datetime, timedelta

# Dátumtartomány megadása
start = datetime(2023, 12, 1)
end = datetime(2023, 12, 31)

# Adatok betöltése
data = await service.read_tick_data('EURUSD', start, end)
print(f"Loaded {len(data)} ticks")
```

### Statisztikák lekérdezése

```python
# Összes statisztika
stats = await service.get_storage_stats()
print(f"Total files: {stats['total_files']}")
print(f"Total size: {stats['total_size_gb']} GB")

# Szimbólum specifikus statisztika
stats = await service.get_storage_stats('EURUSD')
```

### Integritás ellenőrzés

```python
# Checksum számítás
checksum = await service.calculate_checksum('EURUSD', datetime.now())
print(f"Checksum: {checksum}")

# Adatintegritás ellenőrzése
is_valid = await service.verify_data_integrity('EURUSD', datetime.now())
print(f"Data integrity: {is_valid}")
```

## Particionálási stratégia

A tárolás a következő mappaszerkezetet követi:

```
BASE_PATH/
├── EURUSD/
│   └── tick/
│       └── year=2023/
│           └── month=12/
│               └── day=23/
│                   └── data.parquet
├── GBPUSD/
│   └── tick/
│       └── year=2023/
│           └── month=12/
│               └── day=23/
│                   └── data.parquet
```

Ez a struktúra lehetővé teszi:
- Gyors szűrést szimbólum szerint
- Hatékony dátumtartomány lekérdezéseket
- Automatikus adatbontást idő szerint

## Backend kiválasztás

A szolgáltatás automatikusan detektálja a hardver képességeket:

1. **AVX2 támogatás esetén**: PolarsBackend
   - Gyorsabb feldolgozás
   - Jobb memóriakezelés
   - Több szálon történő feldolgozás

2. **AVX2 támogatás hiányában**: PandasBackend
   - Kompatibilitási mód
   - Széleskörű támogatás
   - Megbízható működés

## Típusos támogatás

A szolgáltatás mind a Pandas, mind a Polars DataFrame-eket támogatja:

- **Tárolás**: Bármelyik DataFrame típust eltárolja
- **Olvasás**: A backend típusának megfelelő DataFrame-et ad vissza
- **Konverzió**: Automatikus konverzió a backend igényei szerint

## Hibakezelés

A szolgáltatás átfogó hibakezelést biztosít:

- **Érvényesség ellenőrzés**: DataFrame-ek ellenőrzése tárolás előtt
- **Oszlop ellenőrzés**: Kötelező oszlopok jelenlétének ellenőrzése
- **Integritás ellenőrzés**: Adatok rendezettségének ellenőrzése
- **Hiba naplózás**: Reszletes hibanaplózás structlog segítségével

## Teljesítmény optimalizálások

- **Aszinkron műveletek**: Párhuzamos fájlműveletek
- **Chunkolás**: Nagy adathalmazok feldolgozása
- **Tömörítés**: Snappy tömörítés a tárolási hely csökkentésére
- **Particionálás**: Gyors szűrés és lekérdezés
- **Hardver-gyorsítás**: AVX2 támogatás kihasználása

## Függőségek

- `pandas`: DataFrame kezelés
- `polars`: Gyorsabb DataFrame feldolgozás
- `structlog`: Naplózás
- `pathlib`: Fájlrendszer műveletek
- `asyncio`: Aszinkron műveletek
- `hashlib`: Checksum számítás

## Kapcsolódó komponensek

- [`StorageBackend`](../../backends/base.md): A tárolási backend-ek alapinterfésze
- [`PolarsBackend`](../../backends/polars_backend.md): Polars alapú backend implementáció
- [`PandasBackend`](../../backends/pandas_backend.md): Pandas alapú backend implementáció
- [`HardwareInterface`](../../../utils/interfaces/hardware_interface.md): Hardverképességek detektálása