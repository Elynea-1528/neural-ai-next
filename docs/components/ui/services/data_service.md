# Data Service

## Áttekintés

Ez a dokumentáció a `neural_ai/ui/services/data_service.py` modult dokumentálja, amely az UI réteg adatkezelési szolgáltatását implementálja.

## Modul struktúra

```
neural_ai/ui/services/
├── data_service.py          # Fő implementáció
├── data_service_interface.py # Interfész (ABC)
└── __init__.py
```

## Fő osztály

### DataService

A `DataService` osztály implementálja a `DataServiceInterface` interfészt, és felelős az adatok kezeléséért a Big Data környezetben.

```python
class DataService(DataServiceInterface)
```

#### Konstruktor

```python
def __init__(self, bridge: "CoreBridgeInterface") -> None
```

**Paraméterek:**
- `bridge`: A backend bridge példány, amelyen keresztül elérjük a backend komponenseket (Bi5Downloader, ParquetStorage)

#### Adatforrások

Az osztály a következő adatforrásokat támogatja:

| ID | Név | Leírás | Formátum |
|---|---|---|---|
| `tick_data` | Tick Adatok | Valós idejű tick adatok | parquet |
| `ohlc_data` | OHLC Adatok | Nyitó, magas, alacsony, záró adatok | parquet |
| `market_data` | Piaci Adatok | Általános piaci adatok | parquet |

## Fő metódusok

### load_data

```python
def load_data(
    self, source: str, filters: dict[str, Any] | None = None, chunk_size: int = 10000
) -> Generator[list[dict[str, Any]], None, None]
```

Adatok aszinkron betöltése chunkokban.

**Paraméterek:**
- `source`: Az adatforrás azonosítója
- `filters`: Szűrőfeltételek (opcionális)
- `chunk_size`: A chunkok mérete (alapértelmezett: 10000)

**Visszatérési érték:**
- Generator, amely adat chunkokat ad vissza

### get_data_sources

```python
def get_data_sources(self) -> list[dict[str, str]]
```

Elérhető adatforrások lekérdezése.

**Visszatérési érték:**
- Az adatforrások listája részletes információkkal

### get_data_info

```python
def get_data_info(self, source: str) -> dict[str, Any]
```

Adatforrás információk lekérdezése.

**Paraméterek:**
- `source`: Az adatforrás azonosítója

**Visszatérési érték:**
- Metaadatok a forrásról (méret, rekordok, utolsó frissítés)

### apply_filters

```python
def apply_filters(
    self, data: list[dict[str, Any]], filters: dict[str, Any]
) -> list[dict[str, Any]]
```

Szűrők alkalmazása adatokra.

**Támogatott szűrők:**
- Egyszerű szűrés: `{"field": "value"}`
- Tartomány szűrés: `{"field": {"min": 10, "max": 100}}`

### export_data

```python
def export_data(self, data: list[dict[str, Any]], format: str, destination: str) -> bool
```

Adatok exportálása különböző formátumokba.

**Támogatott formátumok:**
- `parquet`
- `csv`
- `json`

### download_history

```python
async def download_history(self, symbol: str, start: datetime, end: datetime) -> dict[str, Any]
```

Történelmi adatok letöltése aszinkron módon a Dukascopy .bi5 formátumból.

**Paraméterek:**
- `symbol`: A szimbólum (pl. 'EURUSD')
- `start`: Kezdő dátum
- `end`: Záró dátum

**Visszatérési érték:**
- Letöltési eredmények metaadatai

### list_available_data

```python
def list_available_data(self, symbol: str | None = None) -> pd.DataFrame
```

Elérhető adatok listázása DataFrame formátumban.

**Fontos:** Ez a metódus csak a `tick_data` forrást listázza, ha vannak elérhető fájlok. Az `ohlc_data` és `market_data` források nem jelennek meg ghost sorokként.

**Rekord becslés:** `total_files * 3530` (óránkénti átlagos tick szám)

**Oszlopok:**
- `source_id`: Az adatforrás azonosítója
- `symbol`: A szimbólum
- `name`: Az adatforrás neve
- `description`: Leírás
- `format`: Az adatformátum
- `size_gb`: Méret GB-ban
- `records`: Rekordok száma (becsült)
- `last_updated`: Utolsó frissítés időpontja
- `available_dates`: Elérhető dátumok száma
- `total_files`: Összes fájl száma

### get_storage_path

```python
def get_storage_path(self) -> Path
```

Az adattárolási útvonal lekérdezése.

**Visszatérési érték:**
- Az adattárolási útvonal

### get_configured_symbols

```python
def get_configured_symbols(self) -> list[str]
```

Konfigurált szimbólumok lekérdezése.

**Visszatérési érték:**
- A konfigurált szimbólumok listája

## Big Data támogatás

A szolgáltatás a következő Big Data funkciókat támogatja:

1. **Chunkolás**: Az adatok kezelése felosztott chunkokban a `chunk_size` paraméterrel
2. **Aszinkronitás**: Az `async`/`await` kulcsszavak használata a hálózati műveletekhez
3. **Parquet formátum**: Hatékony oszlopalapú tárolás a fastparquet segítségével
4. **Statisztikák**: Tárolási statisztikák lekérdezése (méret, fájlok, dátumok)

## Használati példák

### Alapvető használat

```python
from neural_ai.ui.services.data_service import DataService
from neural_ai.ui.interfaces.core_bridge_interface import CoreBridgeInterface

# Bridge példányosítása (a factory-n keresztül)
bridge: CoreBridgeInterface = ...

# Data Service létrehozása
data_service = DataService(bridge)

# Adatforrások lekérdezése
sources = data_service.get_data_sources()

# Adatok betöltése chunkokban
for chunk in data_service.load_data("tick_data", chunk_size=5000):
    process(chunk)
```

### Szűrés alkalmazása

```python
filters = {
    "symbol": "EURUSD",
    "volume": {"min": 10, "max": 100}
}
filtered_data = data_service.apply_filters(data, filters)
```

### Exportálás

```python
success = data_service.export_data(
    data=my_data,
    format="parquet",
    destination="/path/to/export"
)
```

### Elérhető adatok listázása

```python
# Összes szimbólum
df = data_service.list_available_data()

# Egyetlen szimbólum
df = data_service.list_available_data(symbol="EURUSD")
```

## Architektúra

```
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  DataService                         │   │
│  │  ┌───────────────────────────────────────────────┐  │   │
│  │  │           DataServiceInterface                │  │   │
│  │  └───────────────────────────────────────────────┘  │   │
│  │                                                    │   │
│  │  Felelősség:                                       │   │
│  │  - Adatok betöltése és szűrése                    │   │
│  │  - Exportálás különböző formátumokba             │   │
│  │  - Történelmi adatok letöltése (.bi5)             │   │
│  │  - Elérhető adatok listázása                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                  CoreBridge                         │   │
│  │  (Dependency Injection a backend komponensekhez)    │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│              ┌─────────────┼─────────────┐                  │
│              ▼             ▼             ▼                  │
│      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐    │
│      │ Bi5Downloader│ │ParquetStorage│ │   Config     │    │
│      │ (.bi5 decode)│ │  (Parquet)   │ │             │    │
│      └──────────────┘ └──────────────┘ └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Tesztelés

A modul teszteléséhez használd a következő parancsot:

```bash
/home/elynea/miniconda3/envs/neural-ai-next/bin/pytest tests/ui/services/test_data_service.py -v
```

## Kapcsolódó dokumentáció

- [Architecture Standards](../../development/architecture_standards.md)
- [Task Tree](../../development/TASK_TREE.md)
- [Data Service Interface](../../../../neural_ai/ui/interfaces/data_service_interface.py)
- [Core Bridge Interface](../../../../neural_ai/ui/interfaces/core_bridge_interface.py)
