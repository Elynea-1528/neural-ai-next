# Storage Komponens Használati Példák

## 1. Alap használat

### 1.1 Storage inicializálása

```python
from neural_ai.core.storage.implementations import FileStorage

# Alap könyvtárral
storage = FileStorage("data")

# Relatív útvonallal
storage = FileStorage("./data/processed")

# Abszolút útvonallal
storage = FileStorage("/path/to/data")
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

# CSV formátumban mentés
storage.save_dataframe(df, "users.csv")

# JSON formátumban mentés
storage.save_dataframe(df, "users.json", format="json")

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

storage.save_object(config, "model_config.json")

# Konfiguráció betöltése
loaded_config = storage.load_object("model_config.json")
```

## 2. Haladó használat

### 2.1 DataFrame mentési opciók

```python
# CSV mentés speciális elválasztóval
storage.save_dataframe(df, "data.csv", sep=";")

# Index nélküli mentés
storage.save_dataframe(df, "data.csv", index=False)

# Dátum formátum beállítása
storage.save_dataframe(df, "data.csv", date_format="%Y-%m-%d")

# Float formázás
storage.save_dataframe(df, "data.csv", float_format="%.2f")
```

### 2.2 DataFrame betöltési opciók

```python
# Specifikus oszlopok betöltése
df = storage.load_dataframe("data.csv", usecols=["id", "name"])

# Dátum parse-olás
df = storage.load_dataframe("data.csv", parse_dates=["created_at"])

# Egyéni NA értékek
df = storage.load_dataframe("data.csv", na_values=["N/A", "missing"])
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
storage.save_object(data, "data.json", indent=2)

# Egyéni dátum formátummal
storage.save_object(data, "data.json", default=str)
```

## 3. Fájlrendszer műveletek

### 3.1 Hierarchikus szervezés

```python
# Könyvtár struktúra létrehozása
storage.save_dataframe(train_df, "datasets/train/data.csv")
storage.save_dataframe(test_df, "datasets/test/data.csv")
storage.save_object(model_params, "models/baseline/params.json")

# Könyvtár listázás
all_files = storage.list_dir("datasets")
csv_files = storage.list_dir("datasets", "*.csv")
```

### 3.2 Metaadatok és ellenőrzések

```python
# Fájl létezés ellenőrzése
if storage.exists("models/baseline/params.json"):
    params = storage.load_object("models/baseline/params.json")

# Metaadatok lekérése
metadata = storage.get_metadata("datasets/train/data.csv")
print(f"File size: {metadata['size']} bytes")
print(f"Last modified: {metadata['modified']}")

# Fájl törlése
storage.delete("old_data.csv")
```

## 4. Hibakezelés

### 4.1 Alap hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageNotFoundError,
    StorageFormatError
)

try:
    df = storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError:
    print("File not found")
except StorageError as e:
    print(f"Storage error: {e}")
```

### 4.2 Formátum hibák kezelése

```python
try:
    # Nem támogatott formátum
    storage.save_dataframe(df, "data.xyz", format="xyz")
except StorageFormatError as e:
    print(f"Format error: {e}")

try:
    # Hibás JSON
    storage.load_object("invalid.json")
except StorageError as e:
    print(f"Error loading JSON: {e}")
```

## 5. Legjobb gyakorlatok

### 5.1 Kontextus menedzsment

```python
def process_data(storage: FileStorage, input_path: str, output_path: str) -> None:
    try:
        # Adatok betöltése
        df = storage.load_dataframe(input_path)

        # Feldolgozás
        processed_df = df.copy()
        processed_df["value"] = processed_df["value"] * 2

        # Eredmény mentése
        storage.save_dataframe(processed_df, output_path)

    except StorageError as e:
        print(f"Error processing data: {e}")
        raise
```

### 5.2 Konfigurációkezelés

```python
def load_config(storage: FileStorage, config_path: str) -> dict:
    """Konfiguráció betöltése alapértelmezett értékekkel."""
    defaults = {
        "batch_size": 32,
        "learning_rate": 0.001,
        "epochs": 100
    }

    try:
        config = storage.load_object(config_path)
        return {**defaults, **config}
    except StorageNotFoundError:
        print(f"Config not found at {config_path}, using defaults")
        return defaults
