# Data Service

## Áttekintés

A `DataService` osztály az adatkezelési szolgáltatást implementálja, amely az adatok betöltését, szűrését és kezelését végzi Big Data támogatással. Ez az osztály a UI rétegben található, és a CoreBridge-en keresztül éri el a backend komponenseket.

## Osztály

```python
class DataService(DataServiceInterface)
```

## Metódusok

### `__init__`

```python
def __init__(self, bridge: "CoreBridgeInterface") -> None
```

A Data Service inicializálása.

**Paraméterek:**
- `bridge`: A backend bridge példány, amelyen keresztül elérjük a backend komponenseket (Bi5Downloader, ParquetStorage)

### `load_data`

```python
def load_data(
    self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000
) -> Generator[list[dict[str, Any]], None, None]
```

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**
- `source`: Az adatforrás azonosítója
- `filters`: Szűrőfeltételek
- `chunk_size`: A chunkok mérete

**Visszatérési érték:**
- `Generator[list[dict[str, Any]], None, None]`: Adat chunkok

### `get_data_sources`

```python
def get_data_sources(self) -> list[dict[str, str]]
```

Elérhető adatforrások lekérdezése.

**Visszatérési érték:**
- `list[dict[str, str]]`: Az adatforrások listája

### `get_data_info`

```python
def get_data_info(self, source: str) -> dict[str, Any]
```

Adatforrás információk lekérdezése.

**Paraméterek:**
- `source`: Az adatforrás azonosítója

**Visszatérési érték:**
- `dict[str, Any]`: Az adatforrás metaadatai

### `apply_filters`

```python
def apply_filters(
    self, data: list[dict[str, Any]], filters: dict[str, Any]
) -> list[dict[str, Any]]
```

Szűrők alkalmazása adatokra.

**Paraméterek:**
- `data`: A szűrendő adatok
- `filters`: Az alkalmazandó szűrők

**Visszatérési érték:**
- `list[dict[str, Any]]`: A szűrt adatok

### `export_data`

```python
def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool
```

Adatok exportálása különböző formátumokba.

**Paraméterek:**
- `data`: Az exportálandó adatok
- `format`: A célformátum (parquet, csv, json)
- `destination`: A cél útvonal

**Visszatérési érték:**
- `bool`: True, ha sikeres az exportálás

### `download_history`

```python
async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]
```

Történelmi adatok letöltése aszinkron módon. Ez a metódus a CoreBridge-en keresztül eléri a Bi5Downloader-t, és valós adatletöltést végez a Dukascopy .bi5 formátumból.

**Paraméterek:**
- `symbol`: A szimbólum (pl. 'EURUSD')
- `start`: A kezdő dátum
- `end`: A záró dátum

**Visszatérési érték:**
- `dict[str, Any]`: A letöltött adatok metaadatai és az adatok

**Kivételek:**
- `ValueError`: Ha a dátumtartomány érvénytelen
- `RuntimeError`: Ha a letöltés sikertelen

### `list_available_data`

```python
def list_available_data(self, symbol: str | None = None) -> pd.DataFrame
```

Elérhető adatok listázása DataFrame formátumban. Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t, és valós adatokról állít össze listát.

**Paraméterek:**
- `symbol`: Opcionális szimbólum szűréshez

**Visszatérési érték:**
- `pd.DataFrame`: Az elérhető adatok DataFrame-je

### `get_storage_path`

```python
def get_storage_path(self) -> Path
```

Az adattárolási útvonal lekérdezése. Ez a metódus a CoreBridge-en keresztül eléri a ParquetStorage-t, és a tényleges tárolási útvonalat adja vissza.

**Visszatérési érték:**
- `Path`: Az adattárolási útvonal

**Kivételek:**
- `RuntimeError`: Ha a storage komponens nem érhető el

### `get_configured_symbols`

```python
def get_configured_symbols(self) -> list[str]
```

Konfigurált szimbólumok lekérdezése. A metódus eléri a konfigurációt a CoreBridge-en keresztül, és kiolvassa a JForex collectorhoz tartozó szimbólumokat. Ha a konfiguráció üres vagy hiba történik a lekérdezés során, akkor egy alapértelmezett szimbólumlistát ad vissza.

**Visszatérési érték:**
- `list[str]`: A konfigurált szimbólumok listája. Alapértelmezett esetben `["EURUSD"]`-t ad vissza, ha a konfigurációból nem sikerül lekérdezni a szimbólumokat.

**Példa:**
```python
data_service = DataService(bridge)
symbols = data_service.get_configured_symbols()
print(symbols)
# ['EURUSD', 'GBPUSD', 'USDJPY']
```

## Privát metódusok

### `_generate_mock_data`

```python
def _generate_mock_data(
    self, source: str, filters: dict[str, Any] | None = None
) -> list[dict[str, Any]]
```

Mock adatok generálása teszteléshez.

### `_get_storage_stats_async`

```python
async def _get_storage_stats_async(
    self, storage: "StorageInterface", symbol: str
) -> dict[str, Any]
```

Segédfüggvény a storage statisztikák aszinkron lekérdezéséhez.

## Adatforrások

A DataService a következő adatforrásokat támogatja:

- **tick_data**: Valós idejű tick adatok
- **ohlc_data**: Nyitó, magas, alacsony, záró adatok
- **market_data**: Általános piaci adatok

## Big Data támogatás

A DataService a következő Big Data funkciókat támogatja:

- **Chunkolás**: Nagy adatmennyiségek feldolgozása kisebb darabokban
- **Aszinkronitás**: Nem blokkoló műveletek
- **Parquet formátum**: Hatékony bináris adattárolás

## Függőségek

- `neural_ai.ui.interfaces.data_service_interface.DataServiceInterface`
- `neural_ai.core.storage.interfaces.storage_interface.StorageInterface`
- `neural_ai.ui.interfaces.core_bridge_interface.CoreBridgeInterface`
- `neural_ai.collectors.jforex.interfaces.downloader_interface.IJForexDownloader`

## Használat

```python
from neural_ai.ui.services.data_service import DataService
from neural_ai.ui.factory import UIFactory

# UI Factory inicializálása
factory = UIFactory()

# DataService példány létrehozása
data_service = factory.get_service("data")

# Adatforrások lekérdezése
sources = data_service.get_data_sources()

# Adatok betöltése
for chunk in data_service.load_data("tick_data"):
    process_chunk(chunk)

# Történelmi adatok letöltése
import asyncio
from datetime import datetime

async def download_data():
    result = await data_service.download_history(
        symbol="EURUSD",
        start=datetime(2024, 1, 1),
        end=datetime(2024, 1, 31)
    )
    print(f"Letöltött rekordok: {result['records']}")

asyncio.run(download_data())

# Konfigurált szimbólumok lekérdezése
symbols = data_service.get_configured_symbols()
print(f"Konfigurált szimbólumok: {symbols}")