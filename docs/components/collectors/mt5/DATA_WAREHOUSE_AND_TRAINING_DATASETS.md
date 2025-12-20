# Data Warehouse és Training Dataset Implementáció

**Date:** 2025-12-16
**Version:** 1.0.0
**Status:** Implemented

---

## Áttekintés

Ez a dokumentum ismerteti a Data Warehouse Manager és Training Dataset Generator komponensek implementációját, amelyek optimalizálják az adattárolást és lehetővé teszik a különböző típusú tanulási adathalmazok automatikus generálását.

---

## Tartalomjegyzék

1. [Data Warehouse Manager](#data-warehouse-manager)
2. [Training Dataset Generator](#training-dataset-generator)
3. [CollectorStorage bővítés](#collectorstorage-bővítés)
4. [API Endpointok](#api-endpointok)
5. [Használati példák](#használati-példák)
6. [Tesztelés](#tesztelés)

---

## Data Warehouse Manager

### Bevezetés

A Data Warehouse Manager felelős a hierarchikus adatszervezésért és adatműveletekért. Létrehozza és kezeli a következő struktúrát:

```
data/
├── warehouse/
│   ├── historical/     # 25 év állandó adat
│   ├── update/         # 3-12 hónap, évente merge-elődik
│   ├── realtime/       # Jelenlegi 30 nap
│   └── validated/      # Minőségellenőrzött adatok
├── training/           # 4 adathalmaz típus
│   ├── retraining/     # 1 év, hetente frissül
│   ├── medium/         # 5 év, havonta frissül
│   ├── deep_learning/  # 25 év, évente frissül
│   └── validation/     # 6 hónap, soha nem kerül tanításba
└── metadata/           # Metadata fájlok
```

### Főbb funkciók

#### 1. Adatok mozgatása

```python
from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import DataWarehouseManager

warehouse_manager = DataWarehouseManager(base_path="data")

# Adatok mozgatása a különböző mappák között
result = warehouse_manager.move_data(
    source_path="warehouse/realtime",
    destination_path="warehouse/update",
    instrument="EURUSD",
    timeframe="M1"
)
```

#### 2. Update adatok merge-elése

```python
# Update mappa adatainak merge-elése a historical mappába
result = warehouse_manager.merge_update_to_historical(
    instrument="EURUSD",
    timeframe="M1"
)
```

#### 3. Adatok archiválása

```python
# Adatok archiválása
result = warehouse_manager.archive_data(
    source_path="warehouse/realtime",
    archive_name="archive_2025_01",
    instrument="EURUSD",
    timeframe="M1"
)
```

#### 4. Régi adatok törlése

```python
# Régi adatok törlése (30 napnál régebbi)
result = warehouse_manager.cleanup_old_data(
    source_path="warehouse/realtime",
    retention_days=30
)
```

#### 5. Statisztikák lekérdezése

```python
# Warehouse statisztikák lekérdezése
stats = warehouse_manager.get_warehouse_stats()
print(f"Total size: {stats['total_size_gb']:.2f} GB")
print(f"Total files: {stats['total_files']}")
```

#### 6. Adatintegritás ellenőrzése

```python
# Adatintegritás ellenőrzése
result = warehouse_manager.validate_data_integrity(
    instrument="EURUSD",
    timeframe="M1",
    location="warehouse/historical"
)

if result["is_valid"]:
    print("Data integrity: OK")
else:
    print(f"Issues found: {result['issues_found']}")
```

#### 7. Biztonsági mentés és visszaállítás

```python
# Biztonsági mentés
backup_result = warehouse_manager.backup_data(
    source_path="warehouse",
    backup_name="backup_2025_01",
    instruments=["EURUSD", "GBPUSD"],
    timeframes=["M1", "M5"]
)

# Visszaállítás
restore_result = warehouse_manager.restore_data(
    backup_name="backup_2025_01",
    target_path="warehouse/restored",
    instruments=["EURUSD"],
    timeframes=["M1"]
)
```

---

## Training Dataset Generator

### Bevezetés

A Training Dataset Generator felelős a különböző típusú tanulási adathalmazok generálásáért:

1. **Retraining Dataset**: 1 év, heti frissítés (gyors rátanuláshoz)
2. **Medium Dataset**: 5 év, havi frissítés (közepes tanuláshoz)
3. **Deep Learning Dataset**: 25 év, évi frissítés (mélytanuláshoz)
4. **Validation Dataset**: 6 hónap, soha nem kerül tanításba

### Főbb funkciók

#### 1. Adathalmaz generálása

```python
from neural_ai.collectors.mt5.implementations.training_dataset_generator import TrainingDatasetGenerator
from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import DataWarehouseManager

warehouse_manager = DataWarehouseManager(base_path="data")
training_generator = TrainingDatasetGenerator(warehouse_manager=warehouse_manager)

# Retraining adathalmaz generálása
result = training_generator.generate_dataset(
    dataset_type="retraining",
    symbols=["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
    timeframes=["M1", "M5", "M15", "H1", "H4", "D1"],
    end_date="2024-12-31",
    quality_threshold=0.95,
    output_format="parquet"
)

print(f"Dataset ID: {result['dataset_id']}")
print(f"Total records: {result['total_records']}")
```

#### 2. Adathalmaz állapotának lekérdezése

```python
# Adathalmaz állapotának lekérdezése
status = training_generator.get_dataset_status("dataset_retraining_2024_2025")

print(f"Status: {status['status']}")
print(f"Files: {status['files']}")
print(f"Size: {status['total_size_gb']:.2f} GB")
```

#### 3. Adathalmazok listázása

```python
# Összes adathalmaz listázása
all_datasets = training_generator.list_datasets()

# Adathalmazok listázása típus szerint
retraining_datasets = training_generator.list_datasets(dataset_type="retraining")
```

#### 4. Adathalmaz információk

```python
# Adathalmaz típusok információinak lekérdezése
info = training_generator.get_dataset_info()

print("Supported dataset types:")
for dataset_type, config in info["dataset_types"].items():
    print(f"  - {dataset_type}: {config['description']}")
```

---

## CollectorStorage bővítés

### Data Warehouse integráció

A CollectorStorage-t bővítettük Data Warehouse Manager integrációval:

```python
from neural_ai.collectors.mt5.implementations.storage.collector_storage import CollectorStorage

# CollectorStorage inicializálása Warehouse integrációval
storage = CollectorStorage(
    base_path="data",
    use_parquet=True,
    enable_warehouse_integration=True
)
```

### Új funkciók

#### 1. Automatikus adatszervezés

```python
# Validált adatok automatikus szervezése a warehouse-ba
result = storage.auto_organize_validated_data()
print(f"Organized {result['organized_count']} data sources")
```

#### 2. Warehouse karbantartás

```python
# Teljes warehouse karbantartás futtatása
result = storage.schedule_warehouse_maintenance()

# Eredmények ellenőrzése
print(f"Cleanup: {result['results']['cleanup_raw']['files_count']} files deleted")
print(f"Merge operations: {len([k for k in result['results'].keys() if k.startswith('merge_')])}")
```

#### 3. Warehouse statisztikák

```python
# Warehouse statisztikák lekérdezése
stats = storage.get_warehouse_stats()
print(f"Warehouse size: {stats['total_size_gb']:.2f} GB")
```

---

## API Endpointok

### Training Dataset Endpointok

#### 1. Adathalmaz generálása

```http
POST /api/v1/training/generate
Content-Type: application/json

{
  "dataset_type": "retraining",
  "symbols": ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
  "timeframes": ["M1", "M5", "M15", "H1", "H4", "D1"],
  "date_range": {
    "start": "2024-01-01",
    "end": "2024-12-31"
  },
  "quality_threshold": 0.95,
  "output_format": "parquet"
}
```

#### 2. Adathalmaz állapotának lekérdezése

```http
GET /api/v1/training/status/dataset_retraining_2024_2025
```

#### 3. Adathalmazok listázása

```http
GET /api/v1/training/datasets?dataset_type=retraining
```

#### 4. Adathalmaz információk

```http
GET /api/v1/training/info
```

### Data Warehouse Endpointok

#### 1. Warehouse statisztikák

```http
GET /api/v1/warehouse/stats
```

#### 2. Adatok szervezése

```http
POST /api/v1/warehouse/organize?instrument=EURUSD&timeframe=M1&data_type=validated
```

#### 3. Automatikus szervezés

```http
POST /api/v1/warehouse/auto-organize
```

#### 4. Update merge-elése

```http
POST /api/v1/warehouse/merge?instrument=EURUSD&timeframe=M1
```

#### 5. Warehouse karbantartás

```http
POST /api/v1/warehouse/maintenance
```

#### 6. Biztonsági mentés

```http
POST /api/v1/warehouse/backup?backup_name=backup_2025_01&instruments=EURUSD,GBPUSD&timeframes=M1,M5
```

#### 7. Integritás ellenőrzés

```http
GET /api/v1/warehouse/validate?instrument=EURUSD&timeframe=M1&location=warehouse/historical
```

---

## Használati példák

### 1. Teljes munkafolyamat

```python
from neural_ai.collectors.mt5.implementations.storage.data_warehouse_manager import DataWarehouseManager
from neural_ai.collectors.mt5.implementations.training_dataset_generator import TrainingDatasetGenerator

# 1. Inicializálás
warehouse_manager = DataWarehouseManager(base_path="data")
training_generator = TrainingDatasetGenerator(warehouse_manager=warehouse_manager)

# 2. Adatok szervezése a warehouse-ba
warehouse_manager.move_data(
    source_path="collectors/mt5/raw",
    destination_path="warehouse/validated",
    instrument="EURUSD",
    timeframe="M1"
)

# 3. Tanulási adathalmaz generálása
result = training_generator.generate_dataset(
    dataset_type="retraining",
    symbols=["EURUSD"],
    timeframes=["M1"],
    end_date="2024-12-31",
    quality_threshold=0.95
)

# 4. Adathalmaz állapotának ellenőrzése
status = training_generator.get_dataset_status(result["dataset_id"])
print(f"Dataset ready: {status['status'] == 'completed'}")
```

### 2. Heti karbantartási szkript

```python
import schedule
import time

def weekly_maintenance():
    """Heti warehouse karbantartás."""
    storage = CollectorStorage(base_path="data", enable_warehouse_integration=True)

    # 1. Régi adatok törlése
    storage.cleanup_old_raw_data(retention_days=30)

    # 2. Update adatok merge-elése
    for instrument in ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"]:
        for timeframe in ["M1", "M5", "M15", "H1", "H4", "D1"]:
            storage.merge_update_to_historical(instrument, timeframe)

    # 3. Validált adatok szervezése
    storage.auto_organize_validated_data()

    # 4. Tanulási adathalmazok frissítése
    training_generator = TrainingDatasetGenerator(
        warehouse_manager=storage.warehouse_manager
    )

    # Retraining adathalmaz frissítése
    training_generator.generate_dataset(
        dataset_type="retraining",
        symbols=["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
        timeframes=["M1", "M5", "M15", "H1", "H4", "D1"]
    )

# Heti futás beállítása
schedule.every().week.do(weekly_maintenance)

while True:
    schedule.run_pending()
    time.sleep(3600)  # 1 óra
```

### 3. Adathalmaz használata ML modellekhez

```python
import pandas as pd

# Retraining adathalmaz betöltése
retraining_data = pd.read_parquet("data/training/retraining/EURUSD/M1_retraining_2024_2025.parquet")

# Adatok előkészítése
X = retraining_data[['open', 'high', 'low', 'close', 'volume']]
y = retraining_data['close'].shift(-1)  # Következő időpontban záróár

# ML modell tanítása
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100)
model.fit(X[:-1], y[:-1])  # Utolsó rekordot kihagyjuk

# Validation adathalmaz betöltése
validation_data = pd.read_parquet("data/training/validation/EURUSD/M1_validation_2025_06_2025_12.parquet")

# Validálás
X_val = validation_data[['open', 'high', 'low', 'close', 'volume']]
y_val = validation_data['close'].shift(-1)

score = model.score(X_val[:-1], y_val[:-1])
print(f"Model score: {score:.4f}")
```

---

## Tesztelés

### Data Warehouse Manager tesztek

```bash
# Egyedi teszt futtatása
python -m pytest tests/test_data_warehouse_manager.py::TestDataWarehouseManager::test_initialization -v

# Összes teszt futtatása
python -m pytest tests/test_data_warehouse_manager.py -v

# Integrációs tesztek
python -m pytest tests/test_data_warehouse_manager.py::TestDataWarehouseManagerIntegration -v
```

### Training Dataset Generator tesztek

```bash
# Egyedi teszt futtatása
python -m pytest tests/test_training_dataset_generator.py::TestTrainingDatasetGenerator::test_generate_retraining_dataset -v

# Összes teszt futtatása
python -m pytest tests/test_training_dataset_generator.py -v

# Integrációs tesztek
python -m pytest tests/test_training_dataset_generator.py::TestTrainingDatasetGeneratorIntegration -v
```

### Tesztlefedettség

```bash
# Tesztlefedettség mérése
python -m pytest tests/ --cov=neural_ai.collectors.mt5.implementations.storage --cov=neural_ai.collectors.mt5.implementations.training_dataset_generator --cov-report=html
```

---

## Teljesítményoptimalizálás

### 1. Párhuzamos feldolgozás

```python
from concurrent.futures import ThreadPoolExecutor

def generate_datasets_parallel():
    """Több adathalmaz párhuzamos generálása."""
    dataset_configs = [
        ("retraining", ["EURUSD"], ["M1"]),
        ("medium", ["EURUSD"], ["M1"]),
        ("validation", ["EURUSD"], ["M1"])
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for dataset_type, symbols, timeframes in dataset_configs:
            future = executor.submit(
                training_generator.generate_dataset,
                dataset_type=dataset_type,
                symbols=symbols,
                timeframes=timeframes,
                end_date="2024-12-31"
            )
            futures.append(future)

        results = [f.result() for f in futures]

    return results
```

### 2. Adattömörítés

```python
# Parquet fájlok tömörítése
df.to_parquet(
    "data.parquet",
    engine='fastparquet',
    compression='snappy',  # Gyors és hatékony tömörítés
    index=False
)
```

### 3. Memóriakezelés

```python
# Nagy adathalmazok feldolgozása chunk-okban
def process_large_dataset(file_path, chunk_size=10000):
    """Nagy adathalmaz feldolgozása chunk-okban."""
    chunks = pd.read_parquet(file_path, chunksize=chunk_size)

    for chunk in chunks:
        # Feldolgozás
        processed_chunk = process_chunk(chunk)
        yield processed_chunk
```

---

## Hibaelhárítás

### 1. Adatintegritás problémák

```python
# Integritás ellenőrzés
result = warehouse_manager.validate_data_integrity(
    instrument="EURUSD",
    timeframe="M1",
    location="warehouse/historical"
)

if not result["is_valid"]:
    print("Issues found:")
    for issue in result["issues"]:
        print(f"  - {issue}")

    # Javítási javaslatok
    if "duplicate" in str(result["issues"]).lower():
        print("Suggested fix: Remove duplicates")
    if "null" in str(result["issues"]).lower():
        print("Suggested fix: Fill or remove null values")
```

### 2. Teljesítményproblémák

```python
# Teljesítmény profilozás
import cProfile
import pstats

def profile_dataset_generation():
    """Adathalmaz generálás profilozása."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Adathalmaz generálása
    result = training_generator.generate_dataset(
        dataset_type="retraining",
        symbols=["EURUSD"],
        timeframes=["M1"],
        end_date="2024-12-31"
    )

    profiler.disable()

    # Eredmények kiírása
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 leglassabb függvények
```

### 3. Tárolóproblémák

```python
# Tároló statisztikák ellenőrzése
stats = warehouse_manager.get_warehouse_stats()

if stats["total_size_gb"] > 100:
    print("Warning: Warehouse size exceeds 100GB")
    print("Consider archiving old data or increasing storage capacity")

# Automatikus archiválás
if stats["warehouse"]["realtime"]["size_gb"] > 10:
    warehouse_manager.archive_data(
        source_path="warehouse/realtime",
        archive_name=f"archive_{datetime.now().strftime('%Y_%m')}",
        instrument="EURUSD"
    )
```

---

## Biztonság

### 1. Adatbiztonsági mentések

```python
# Rendszeres biztonsági mentések
def daily_backup():
    """Napi biztonsági mentés."""
    warehouse_manager = DataWarehouseManager(base_path="data")

    backup_name = f"daily_backup_{datetime.now().strftime('%Y_%m_%d')}"

    result = warehouse_manager.backup_data(
        source_path="warehouse",
        backup_name=backup_name,
        instruments=["EURUSD", "GBPUSD", "USDJPY", "XAUUSD"],
        timeframes=["M1", "M5", "M15", "H1", "H4", "D1"]
    )

    print(f"Daily backup created: {backup_name}")
```

### 2. Hozzáférés-vezérlés

```python
# Bizalmas adathalmazok védelme
def protect_sensitive_datasets():
    """Érzékeny adathalmazok védelme."""
    import os

    sensitive_datasets = [
        "data/training/validation",
        "data/warehouse/historical"
    ]

    for dataset_path in sensitive_datasets:
        # Csak olvasási jogosultság beállítása
        os.chmod(dataset_path, 0o444)
```

---

## Következő lépések

### 1. Monitorozás implementálása

- [ ] Warehouse méret monitorozása
- [ ] Adathalmaz minőség metrikák
- [ ] Generálási idő nyomon követése
- [ ] Hibák és figyelmeztetések riasztása

### 2. További optimalizálások

- [ ] In-memory gyorsítótár implementálása
- [ ] Elosztott feldolgozás támogatása
- [ ] Real-time adatfrissítések
- [ ] Automatikus skálázás

### 3. Bővítmények

- [ ] További adatformátumok támogatása
- [ ] Speciális feature engineering
- [ ] Automatikus modell validáció
- [ ] Adatminőség javító algoritmusok

---

## Kapcsolódó dokumentáció

- [Data Collection Strategy Overhaul](plans/data_collection_strategy_overhaul.md)
- [Data Quality Framework](docs/components/collectors/mt5/DATA_QUALITY_FRAMEWORK.md)
- [Historical Data Collection](docs/components/collectors/mt5/HISTORICAL_DATA_COLLECTION.md)
- [MT5 Collector API](docs/components/collectors/mt5/api.md)

---

**Document Version:** 1.0.0
**Last Updated:** 2025-12-16
**Author:** Roo (AI Architect)
**Status:** Implemented
