# Historical Data Collection - MT5 Collector

## Áttekintés

Ez a dokumentum ismerteti a historikus adatgyűjtés Python backend implementációját az MT5 Collector komponensben. A rendszer lehetővé teszi 25 évnyi historikus adat gyűjtését, tárolását és kezelését a MetaTrader 5 platformról.

## Architektúra

### Komponensek

#### 1. HistoricalJobStatus Enum
```python
class HistoricalJobStatus(Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
```

#### 2. HistoricalJob
Historikus adatgyűjtési feladat reprezentációja.

**Attribútumok:**
- `job_id`: Egyedi job azonosító
- `symbol`: Pénznem szimbólum (pl. EURUSD)
- `timeframe`: Időkeret (pl. M1, H1)
- `start_date`: Kezdő dátum (ISO formátumban)
- `end_date`: Végdátum (ISO formátumban)
- `batch_size`: Kötegenkénti napok száma
- `priority`: Prioritás (low, normal, high)
- `status`: Job státusz
- `progress`: Haladás százalékban
- `total_batches`: Összes köteg száma
- `completed_batches`: Elkészült kötegek száma
- `current_batch`: Jelenlegi köteg száma
- `errors`: Hibaüzenetek listája
- `warnings`: Figyelmeztetések listája
- `created_at`: Létrehozás időpontja
- `started_at`: Indulás időpontja
- `completed_at`: Befejezés időpontja
- `estimated_duration`: Becsült időtartam

#### 3. HistoricalDataManager
Fő historikus adatkezelő osztály.

**Felelősségek:**
- Historikus adatkérések kezelése
- Job követés és státusz kezelés
- Adatok fogadása és validálása
- Adathézagok azonosítása
- Data Warehouse-ba történő tárolás

## API Endpointok

### 1. Historikus adatgyűjtés indítása (új)

**Endpoint:** `POST /api/v1/historical/start`

Ez az endpoint háromféle módon használható: automatikus indítás, specifikus szimbólum indítása, vagy összes szimbólum indítása.

**Query Parameters:**
- `auto_start` (bool, opcionális): Automatikus indítás (hiányzó adatok detektálása és feltöltése). Alapértelmezett: `true`
- `symbol` (string, opcionális): Szimbólum (pl. "EURUSD")
- `timeframe` (string, opcionális): Időkeret (pl. "H1", "M15"). Alapértelmezett: "H1"
- `start_date` (string, opcionális): Kezdő dátum (YYYY-MM-DD)
- `end_date` (string, opcionális): Befejező dátum (YYYY-MM-DD)
- `batch_size` (int, opcionális): Kötegméret napokban. Alapértelmezett: `365`
- `priority` (string, opcionális): Prioritás ("normal", "high", "low"). Alapértelmezett: "normal"

**1. Automatikus indítás (ajánlott):**
```bash
curl -X POST "http://localhost:8000/api/v1/historical/start?auto_start=true"
```

**Response:**
```json
{
  "status": "success",
  "message": "Historical data collection started",
  "mode": "auto_start",
  "jobs_created": 5,
  "missing_data": [
    {
      "symbol": "EURUSD",
      "timeframe": "H1",
      "start_date": "2020-01-01",
      "end_date": "2023-12-31"
    }
  ]
}
```

**2. Specifikus szimbólum indítása:**
```bash
curl -X POST "http://localhost:8000/api/v1/historical/start?symbol=EURUSD&timeframe=H1&start_date=2023-01-01&end_date=2023-12-31&batch_size=365&priority=high"
```

**Response:**
```json
{
  "status": "success",
  "message": "Historical data job created",
  "job_id": "job_12345",
  "symbol": "EURUSD",
  "timeframe": "H1",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "batch_size": 365,
  "priority": "high"
}
```

**3. Összes szimbólum indítása:**
```bash
curl -X POST "http://localhost:8000/api/v1/historical/start?auto_start=false"
```

**Response:**
```json
{
  "status": "success",
  "message": "Historical collection started for all instruments",
  "total_jobs": 24,
  "instruments": ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
  "timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"]
}
```

### 2. Historikus adatkérés létrehozása (régi módszer)

**Endpoint:** `POST /api/v1/historical/request`

**Request Body:**
```json
{
  "symbol": "EURUSD",
  "timeframe": "M1",
  "start_date": "2000-01-01",
  "end_date": "2025-12-31",
  "batch_size": 365,
  "priority": "normal"
}
```

**Response:**
```json
{
  "job_id": "job_12345",
  "status": "queued",
  "estimated_duration": "2 hours",
  "total_batches": 26,
  "message": "Historical data collection job created"
}
```

### 2. Job státusz lekérdezése

**Endpoint:** `GET /api/v1/historical/status/{job_id}`

**Response:**
```json
{
  "job_id": "job_12345",
  "status": "in_progress",
  "progress": {
    "completed_batches": 10,
    "total_batches": 26,
    "percentage": 38.46
  },
  "current_batch": {
    "batch_number": 11,
    "date_range": "2010-01-01 to 2010-12-31"
  },
  "errors": [],
  "warnings": [],
  "started_at": "2025-12-16T20:00:00Z",
  "estimated_completion": "2025-12-16T22:00:00Z"
}
```

### 3. Historikus adatok fogadása

**Endpoint:** `POST /api/v1/historical/collect`

**Request Body:**
```json
{
  "job_id": "job_12345",
  "batch_number": 1,
  "symbol": "EURUSD",
  "timeframe": "M1",
  "date_range": {
    "start": "2000-01-01",
    "end": "2000-12-31"
  },
  "bars": [
    {
      "time": 946684800,
      "open": 1.0100,
      "high": 1.0120,
      "low": 1.0090,
      "close": 1.0115,
      "volume": 1000
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "batch_number": 1,
  "bars_received": 525600,
  "bars_stored": 525600,
  "message": "Batch stored successfully"
}
```

### 4. Adathézagok azonosítása

**Endpoint:** `GET /api/v1/data/gaps`

**Query Parameters:**
- `symbol` (optional): Filter by symbol
- `timeframe` (optional): Filter by timeframe
- `start_date` (optional): Start of analysis period
- `end_date` (optional): End of analysis period

**Response:**
```json
{
  "analysis_period": {
    "start": "2000-01-01",
    "end": "2025-12-16"
  },
  "gaps": [
    {
      "symbol": "EURUSD",
      "timeframe": "M1",
      "start": "2020-03-15T10:30:00Z",
      "end": "2020-03-15T12:45:00Z",
      "duration_minutes": 135,
      "missing_bars": 135
    }
  ],
  "total_gaps": 15,
  "total_missing_bars": 2047
}
```

### 5. Adathézagok pótlása

**Endpoint:** `POST /api/v1/data/fill-gaps`

**Request Body:**
```json
{
  "symbol": "EURUSD",
  "timeframe": "M1",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Gap filling jobs created: 3",
  "job_ids": ["job_1", "job_2", "job_3"],
  "total_gaps": 3
}
```

## Adattárolás

### Mappa struktúra

```
data/
├── collectors/
│   └── mt5/
│       ├── historical_jobs.db          # SQLite adatbázis job-okhoz
│       ├── raw/                        # Nyers adatok
│       │   ├── ticks/
│       │   └── ohlcv/
│       └── invalid/                    # Érvénytelen adatok
│
└── warehouse/
    ├── historical/                     # 25 év historikus adat
    ├── update/                         # Inkrementális frissítések
    ├── realtime/                       # Valós idejű adatok
    └── validated/                      # Validált adatok
```

### Adatbázis séma

```sql
CREATE TABLE historical_jobs (
    job_id TEXT PRIMARY KEY,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    batch_size INTEGER NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    progress REAL NOT NULL,
    total_batches INTEGER NOT NULL,
    completed_batches INTEGER NOT NULL,
    current_batch INTEGER NOT NULL,
    errors TEXT,
    warnings TEXT,
    created_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    estimated_duration TEXT
);
```

## Használati példák

### Command Line Script

A [`scripts/start_historical_collection.py`](../../../scripts/start_historical_collection.py) script használatával parancssorból indítható a historikus adatgyűjtés.

**1. Automatikus indítás (hiányzó adatok feltöltése):**
```bash
python scripts/start_historical_collection.py --auto-start
```

**2. Összes szimbólum indítása:**
```bash
python scripts/start_historical_collection.py --all-instruments
```

**3. Specifikus szimbólum indítása:**
```bash
python scripts/start_historical_collection.py --symbol EURUSD --timeframe H1 --start-date 2023-01-01 --end-date 2023-12-31
```

**4. Testreszabott beállítások:**
```bash
python scripts/start_historical_collection.py --symbol GBPUSD --timeframe M15 --start-date 2022-01-01 --end-date 2024-12-31 --batch-size 180 --priority high
```

**Paraméterek:**
- `--auto-start`: Automatikus indítás (hiányzó adatok detektálása)
- `--all-instruments`: Összes szimbólum indítása
- `--symbol`: Szimbólum megadása
- `--timeframe`: Időkeret megadása
- `--start-date`: Kezdő dátum (YYYY-MM-DD)
- `--end-date`: Befejező dátum (YYYY-MM-DD)
- `--batch-size`: Kötegméret napokban (alapértelmezett: 365)
- `--priority`: Prioritás (normal, high, low)
- `--help`: Súgó megjelenítése

### Python kliens

```python
import requests

# 1. Historikus adatkérés létrehozása
response = requests.post(
    "http://localhost:8000/api/v1/historical/request",
    json={
        "symbol": "EURUSD",
        "timeframe": "M1",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "batch_size": 30,
        "priority": "high"
    }
)
job_id = response.json()["job_id"]

# 2. Státusz lekérdezése
status = requests.get(f"http://localhost:8000/api/v1/historical/status/{job_id}")
print(status.json())

# 3. Hézagok keresése
gaps = requests.get(
    "http://localhost:8000/api/v1/data/gaps",
    params={
        "symbol": "EURUSD",
        "timeframe": "M1",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
)
print(gaps.json())

# 4. Hézagok pótlása
fill_response = requests.post(
    "http://localhost:8000/api/v1/data/fill-gaps",
    json={
        "symbol": "EURUSD",
        "timeframe": "M1",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
)
print(fill_response.json())
```

### cURL parancsok

```bash
# Historikus adatkérés
curl -X POST http://localhost:8000/api/v1/historical/request \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "timeframe": "M1",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "batch_size": 365,
    "priority": "normal"
  }'

# Státusz lekérdezése
curl http://localhost:8000/api/v1/historical/status/job_12345

# Hézagok keresése
curl "http://localhost:8000/api/v1/data/gaps?symbol=EURUSD&timeframe=M1"

# Hézagok pótlása
curl -X POST http://localhost:8000/api/v1/data/fill-gaps \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "EURUSD",
    "timeframe": "M1"
  }'
```

## Hibakezelés

### Gyakori hibák

1. **Érvénytelen dátumtartomány**
   - Hiba: "Start date must be before end date"
   - Megoldás: Ellenőrizze a dátumokat

2. **Ismeretlen job ID**
   - Hiba: "Job not found"
   - Megoldás: Ellenőrizze a job_id-t

3. **Tárolási hiba**
   - Hiba: "Failed to store historical data"
   - Megoldás: Ellenőrizze a lemezterületet és engedélyeket

4. **Validációs hiba**
   - Hiba: "Invalid OHLCV bar"
   - Megoldás: Az érvénytelen adatok külön tárolásra kerülnek

### Hibajavítási stratégiák

1. **Automatikus újrapróbálkozás**: A rendszer automatikusan újrapróbálkozik átmeneti hibák esetén
2. **Hézagpótlás**: Az észlelt adathézagok automatikusan pótolhatók
3. **Manuális beavatkozás**: Kritikus hibák esetén a rendszer naplózza a hibát és értesíti a felhasználót

## Teljesítményoptimalizálás

### Tippek

1. **Kötegméret optimalizálása**: Használjon kisebb kötegeket nagyobb adatmennyiség esetén
2. **Prioritás beállítása**: Fontos adatokhoz használja a "high" prioritást
3. **Időzítés**: Tervezze meg a historikus adatgyűjtést alacsony forgalom idején
4. **Tárolás**: Ellenőrizze rendszeresen a lemezterületet

### Monitorozás

```bash
# Tárolási statisztikák
curl http://localhost:8000/api/v1/storage/stats

# Validációs jelentés
curl http://localhost:8000/api/v1/validation/report

# Hibajelentés
curl http://localhost:8000/api/v1/errors/report
```

## Fejlesztői információk

### Fájlok

- **Main implementation**: [`neural_ai/collectors/mt5/implementations/historical_data_manager.py`](../neural_ai/collectors/mt5/implementations/historical_data_manager.py)
- **Integration**: [`neural_ai/collectors/mt5/implementations/mt5_collector.py`](../neural_ai/collectors/mt5/implementations/mt5_collector.py)
- **Tests**: [`tests/test_historical_data_manager.py`](../../../tests/test_historical_data_manager.py)

### Függőségek

- `fastapi`: API keretrendszer
- `pydantic`: Adatvalidáció
- `pandas`: Adatfeldolgozás
- `fastparquet`: Parquet formátum támogatás
- `sqlite3`: Job követés

### Tesztelés

```bash
# Unit tesztek futtatása
python tests/test_historical_data_manager.py

# API tesztek
python -m pytest tests/ -v
```

## Verziótörténet

- **v1.0.0** (2025-12-16): Kezdeti implementáció
  - Historikus adatkérések kezelése
  - Job követés és státusz kezelés
  - Adatok fogadása és validálása
  - Adathézagok azonosítása
  - Data Warehouse-ba történő tárolás

## Kapcsolódó dokumentáció

- [Data Collection Strategy Overview](../../../plans/data_collection_strategy_overhaul.md)
- [MT5 Collector API](../mt5/api.md)
- [Data Warehouse Structure](../../storage/architecture.md)
- [MQL5 EA Historical Extension Spec](../../../plans/mql5_ea_historical_extension_spec.md)
