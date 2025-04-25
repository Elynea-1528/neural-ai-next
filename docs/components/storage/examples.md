# Storage Komponens Használati Példák

## 1. Alap használat

### 1.1 Storage inicializálása

```python
from pathlib import Path
from neural_ai.core.storage.implementations import FileStorage

# Alap könyvtárral
storage = FileStorage("data")

# Relatív útvonallal
storage = FileStorage("./data/processed")

# Abszolút útvonallal
storage = FileStorage("/path/to/data")

# Path objektummal
storage = FileStorage(Path("data/processed"))
```

### 1.2 DataFrame műveletek

```python
import pandas as pd

# DataFrame létrehozása
df = pd.DataFrame({
    "id": range(1, 4),
    "name": ["Alice", "Bob", "Charlie"],
    "value": [10.5, 20.0, 15.7]
})

# Automatikus formátum felismerés kiterjesztés alapján
storage.save_dataframe(df, "users.csv")  # CSV formátum
storage.save_dataframe(df, "users.json")  # JSON formátum
storage.save_dataframe(df, "users.xlsx")  # Excel formátum

# Index kezelés
storage.save_dataframe(df, "users_with_index.csv", index=True)
storage.save_dataframe(df, "users_no_index.csv", index=False)  # Alapértelmezett

# DataFrame betöltése
users_df = storage.load_dataframe("users.csv")
```

### 1.3 Python objektumok kezelése

```python
# Konfiguráció mentése
config = {
    "model_params": {
        "layers": [64, 32, 16],
        "activation": "relu",
        "dropout": 0.2
    },
    "training": {
        "epochs": 100,
        "batch_size": 32,
        "learning_rate": 0.001
    }
}

# JSON formátum automatikus felismerése
storage.save_object(config, "model_config.json")

# Konfiguráció betöltése
loaded_config = storage.load_object("model_config.json")
```

## 2. Haladó használat

### 2.1 DataFrame mentési opciók

```python
# CSV mentés speciális elválasztóval
storage.save_dataframe(df, "data.csv", sep=";")

# Float formázás és idexelés
storage.save_dataframe(df, "data.csv",
    float_format="%.2f",
    index=True,
    index_label="row_id"
)

# Dátum formátum beállítása
storage.save_dataframe(df, "data.csv",
    date_format="%Y-%m-%d",
    encoding="utf-8"
)
```

### 2.2 DataFrame betöltési opciók

```python
# Specifikus oszlopok betöltése
df = storage.load_dataframe("data.csv", usecols=["id", "name"])

# Dátum parse-olás
df = storage.load_dataframe("data.csv",
    parse_dates=["created_at"],
    date_parser=lambda x: pd.to_datetime(x, utc=True)
)

# Egyéni NA értékek és típusok
df = storage.load_dataframe("data.csv",
    na_values=["N/A", "missing"],
    dtype={"id": int, "value": float}
)
```

### 2.3 JSON szerializáció testreszabása

```python
from datetime import datetime

# Egyéni adatok mentése
data = {
    "timestamp": datetime.now(),
    "values": [1, 2, 3],
    "active": True
}

# JSON mentés formázással
storage.save_object(data, "data.json",
    indent=2,
    default=str  # datetime szerializáció
)

# JSON betöltés parse-olással
loaded = storage.load_object("data.json",
    parse_float=decimal.Decimal  # pontos lebegőpontos számok
)
```

## 3. Fájlrendszer műveletek

### 3.1 Hierarchikus szervezés

```python
# Könyvtár struktúra létrehozása
storage.save_dataframe(train_df, "datasets/train/data.csv")
storage.save_dataframe(test_df, "datasets/test/data.csv")
storage.save_object(model_params, "models/baseline/params.json")

# Könyvtár listázás Path objektumokkal
dataset_paths = storage.list_dir("datasets")
for path in dataset_paths:
    print(f"Found file: {path.name}")
    if path.suffix == '.csv':
        df = storage.load_dataframe(str(path))

# Szűrés mintával
csv_paths = storage.list_dir("datasets", pattern="*.csv")
json_paths = storage.list_dir("models", pattern="*.json")
```

### 3.2 Metaadatok és ellenőrzések

```python
# Fájl létezés ellenőrzése
if storage.exists("models/baseline/params.json"):
    params = storage.load_object("models/baseline/params.json")

# Metaadatok lekérése
metadata = storage.get_metadata("datasets/train/data.csv")
print(f"File size: {metadata['size']} bytes")
print(f"Created: {metadata['created']}")
print(f"Last modified: {metadata['modified']}")
print(f"Last accessed: {metadata['accessed']}")
print(f"Is file: {metadata['is_file']}")
print(f"Is directory: {metadata['is_dir']}")

# Fájl törlése
storage.delete("old_data.csv")
```

## 4. Hibakezelés

### 4.1 Alap hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageNotFoundError,
    StorageFormatError,
    StorageSerializationError,
    StorageIOError
)

try:
    df = storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError as e:
    print(f"File not found: {e}")
except StorageFormatError as e:
    print(f"Invalid format: {e}")
except StorageSerializationError as e:
    print(f"Data error: {e}")
except StorageIOError as e:
    print(f"I/O error: {e}")
except StorageError as e:
    print(f"General storage error: {e}")
```

### 4.2 Részletes hibakezelés

```python
try:
    # Hibás JSON fájl betöltése
    storage.load_object("invalid.json")
except StorageSerializationError as e:
    print(f"JSON parsing error: {e}")
    if e.original_error:  # Az eredeti kivétel elérése
        print(f"Original error: {e.original_error}")

# Nem létező könyvtár listázása
try:
    paths = storage.list_dir("nonexistent_dir")
except StorageNotFoundError as e:
    print(f"Directory not found: {e}")
```

## 5. Legjobb gyakorlatok

### 5.1 Típusbiztos használat

```python
from typing import Dict, Any
from pathlib import Path

def process_data(storage: FileStorage, input_path: str, output_path: str) -> None:
    """DataFrame feldolgozása hibakezeleléssel."""
    try:
        df = storage.load_dataframe(input_path)

        # Feldolgozás
        processed_df = df.copy()
        processed_df["value"] = processed_df["value"] * 2

        # Eredmény mentése index nélkül
        storage.save_dataframe(
            processed_df,
            output_path,
            index=False,
            float_format="%.3f"
        )

    except StorageError as e:
        print(f"Error processing data: {e}")
        raise
```

### 5.2 Konfigurációkezelés

```python
def load_config(
    storage: FileStorage,
    config_path: str,
    defaults: Dict[str, Any]
) -> Dict[str, Any]:
    """Konfiguráció betöltése alapértelmezett értékekkel."""
    try:
        config = storage.load_object(config_path)
        return {**defaults, **config}
    except StorageNotFoundError:
        print(f"Config not found at {config_path}, using defaults")
        return defaults.copy()
    except StorageError as e:
        print(f"Error loading config: {e}")
        return defaults.copy()
