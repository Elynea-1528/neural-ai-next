# DataService

## Áttekintés

A `DataService` osztály a Neural AI Next rendszer felhasználói felületének adatkezelési szolgáltatását biztosítja. Ez az osztály felelős a történelmi adatok letöltéséért, az elérhető adatok listázásáért, valamint az adatok szűréséért és exportálásáért.

## Architektúra

### Osztályhierarchia

```python
DataService(DataServiceInterface)
```

### Implementált Interfészek

- [`DataServiceInterface`](../../ui/interfaces/data_service_interface.md)

### Függőségek

- **CoreBridge**: A backend komponensek eléréséhez
- **IJForexDownloader**: Történelmi tick adatok letöltéséhez
- **StorageInterface**: Tárolt adatok lekérdezéséhez és kezeléséhez

## Metódusok

### `__init__`

```python
def __init__(self, bridge: CoreBridgeInterface) -> None
```

A DataService inicializálója.

**Paraméterek:**
- `bridge` (CoreBridgeInterface): A CoreBridge példány, amelyen keresztül a backend komponensek elérhetők

**Létrehozza:**
- A három alapvető adatforrást: `tick_data`, `ohlc_data`, `market_data`

---

### `get_data_sources`

```python
def get_data_sources(self) -> list[dict[str, object]]
```

Visszaadja az összes elérhető adatforrást.

**Visszatérési érték:**
- `list[dict[str, object]]`: Az adatforrások listája, minden forrás tartalmazza az `id`, `name`, `description`, és `format` mezőket

---

### `get_data_info`

```python
def get_data_info(self, source_id: str) -> dict[str, object]
```

Lekérdezi egy adott adatforrás részletes információit.

**Paraméterek:**
- `source_id` (str): Az adatforrás azonosítója

**Visszatérési érték:**
- `dict[str, object]`: A forrás információi, tartalmazza a `source`, `name`, `description`, `format`, `size`, `records`, és `last_updated` mezőket

**Kivételek:**
- `ValueError`: Ha az adatforrás nem ismerhető fel

---

### `apply_filters`

```python
def apply_filters(
    self,
    data: list[dict[str, object]],
    filters: dict[str, object]
) -> list[dict[str, object]]
```

Alkalmazza a megadott szűrőket az adatokra.

**Paraméterek:**
- `data` (list[dict[str, object]]): A szűrendő adatok listája
- `filters` (dict[str, object]): A szűrők szótára, amely tartalmazhat:
  - Egyszerű egyeztetést: `{"field": "value"}`
  - Tartományt: `{"field": {"min": value, "max": value}}`

**Visszatérési érték:**
- `list[dict[str, object]]`: A szűrt adatok listája

---

### `export_data`

```python
def export_data(
    self,
    data: list[dict[str, object]],
    format_type: str,
    file_path: str
) -> bool
```

Exportálja az adatokat a megadott formátumban.

**Paraméterek:**
- `data` (list[dict[str, object]]): Az exportálandó adatok
- `format_type` (str): A célformátum (`parquet`, `csv`, `json`)
- `file_path` (str): A célfájl elérési útja

**Visszatérési érték:**
- `bool`: `True`, ha az exportálás sikeres, `False`, ha az adatok üresek

**Kivételek:**
- `ValueError`: Ha a formátum nem támogatott

---

### `download_history`

```python
async def download_history(
    self,
    symbol: str,
    start: datetime,
    end: datetime
) -> dict[str, object]
```

Letölti a megadott szimbólum történelmi adatait a dátumtartományban.

**Paraméterek:**
- `symbol` (str): A pénzpár szimbóluma (pl. "EURUSD")
- `start` (datetime): A kezdő dátum
- `end` (datetime): A befejező dátum

**Visszatérési érték:**
- `dict[str, object]`: A letöltés eredménye, tartalmazza:
  - `symbol` (str): A letöltött szimbólum
  - `status` (str): A letöltés állapota (`downloaded`, `partial`, `failed`)
  - `records` (int): A letöltött rekordok száma
  - `size_mb` (float): A letöltött adatok mérete MB-ban
  - `format` (str): Az adatok formátuma (`parquet`)

**Kivételek:**
- `ValueError`: Ha a dátumtartomány érvénytelen (kezdő dátum későbbi, mint a befejező, vagy jövőbeli dátum)
- `RuntimeError`: Ha a Bi5Downloader komponens nem érhető el

**Aszinkron működés:**
- A metódus aszinkron, nem blokkolja a felhasználói felületet
- A letöltés naponkénti bontásban történik
- Minden napra külön hívja a `Bi5Downloader.download_tick_data` metódust

---

### `list_available_data`

```python
def list_available_data(
    self,
    symbol: str | None = None
) -> pd.DataFrame
```

Listázza az elérhető adatokat a tárhelyről.

**Paraméterek:**
- `symbol` (str | None): Opcionális szimbólumszűrő

**Visszatérési érték:**
- `pd.DataFrame`: Egy DataFrame, amely tartalmazza:
  - `source_id` (str): Az adatforrás azonosítója
  - `symbol` (str): A pénzpár szimbóluma
  - `name` (str): Az adatforrás neve
  - `size_gb` (float): Az adatok mérete GB-ban
  - `records` (int): A rekordok száma
  - `last_updated` (datetime): Az utolsó frissítés ideje

**Kivételek:**
- `RuntimeError`: Ha a Storage komponens nem érhető el

---

### `get_storage_path`

```python
def get_storage_path(self) -> Path
```

Visszaadja a tárhely alapértelmezett útvonalát.

**Visszatérési érték:**
- `Path`: A tárhely útvonala

**Kivételek:**
- `RuntimeError`: Ha a Storage komponens nem érhető el

---

### `load_data`

```python
def load_data(
    self,
    source: str,
    chunk_size: int = 1000,
    filters: dict[str, object] | None = None
) -> Iterator[list[dict[str, object]]]
```

Betölti az adatokat chunk-okban a megadott forrásból.

**Paraméterek:**
- `source` (str): Az adatforrás azonosítója
- `chunk_size` (int): A chunk-ok mérete (alapértelmezett: 1000)
- `filters` (dict[str, object] | None): Opcionális szűrők

**Visszatérési érték:**
- `Iterator[list[dict[str, object]]]`: Egy iterator, amely adat-chunk-okat ad vissza

**Kivételek:**
- `ValueError`: Ha az adatforrás nem ismerhető fel

---

### `_get_storage_stats_async` (Protected)

```python
async def _get_storage_stats_async(
    self,
    storage: object,
    symbol: str
) -> dict[str, object]
```

Helper metódus a tárhely statisztikák aszinkron lekérdezéséhez.

**Paraméterek:**
- `storage` (object): A storage komponens
- `symbol` (str): A szimbólum

**Visszatérési érték:**
- `dict[str, object]`: A statisztikák, tartalmazza a `total_files`, `size_gb`, `available_dates` mezőket

**Fallback logika:**
- Ha a storage nem támogatja a `get_storage_stats` metódust, alapértelmezett értékekkel tér vissza
- Hibák esetén szintén alapértelmezett értékekkel tér vissza

---

## Használati példák

### Történelmi adatok letöltése

```python
from datetime import datetime
from neural_ai.ui.services.data_service import DataService

# DataService példányosítása
data_service = DataService(core_bridge)

# Adatok letöltése
async def download_data():
    result = await data_service.download_history(
        symbol="EURUSD",
        start=datetime(2026, 1, 1),
        end=datetime(2026, 1, 3)
    )
    print(f"Letöltve: {result['records']} rekord")

# Aszinkron hívás
import asyncio
asyncio.run(download_data())
```

### Elérhető adatok listázása

```python
# Összes elérhető adat
df = data_service.list_available_data()
print(df)

# Csak egy szimbólum adatai
df_eurusd = data_service.list_available_data("EURUSD")
print(df_eurusd)
```

### Adatok szűrése

```python
# Alapvető szűrés
data = [
    {"id": 1, "name": "test1", "value": 100},
    {"id": 2, "name": "test2", "value": 200},
]
filters = {"name": "test1"}
filtered = data_service.apply_filters(data, filters)

# Tartomány szűrése
filters = {"value": {"min": 150, "max": 250}}
filtered = data_service.apply_filters(data, filters)
```

### Adatok exportálása

```python
# Parquet formátumban
success = data_service.export_data(
    data,
    format_type="parquet",
    file_path="/tmp/data.parquet"
)
```

## Adatforrások

A DataService három alapvető adatforrást kezel:

1. **tick_data**: Tick adatok nagy felbontásban
2. **ohlc_data**: OHLC (Open-High-Low-Close) adatok
3. **market_data**: Piaci adatok és meta-információk

## Típusok és Formátumok

- **Tárolási formátum**: Parquet (Big Data optimalizált)
- **Adatforrás formátum**: Bi5 (JForex natív formátuma)
- **Export formátumok**: Parquet, CSV, JSON

## Hibakezelés

A DataService átfogó hibakezelést biztosít:

- **Érvénytelen adatforrás**: `ValueError` kivétel
- **Érvénytelen dátumtartomány**: `ValueError` kivétel
- **Hiányzó komponens**: `RuntimeError` kivétel
- **Nem támogatott formátum**: `ValueError` kivétel

## Teljesítményoptimalizálás

- **Chunk-olás**: Nagy adatmennyiségek feldolgozása kisebb egységekben
- **Aszinkron működés**: UI nem blokkolása hosszú műveletek során
- **Big Data támogatás**: Parquet formátum és particionálás

## Kapcsolódó dokumentáció

- [DataServiceInterface](../../ui/interfaces/data_service_interface.md)
- [CoreBridgeInterface](../../ui/interfaces/core_bridge_interface.md)
- [IJForexDownloader](../../collectors/jforex/interfaces/downloader_interface.md)
- [StorageInterface](../../core/storage/interfaces/storage_interface.md)