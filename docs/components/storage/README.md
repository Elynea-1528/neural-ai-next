# Neural AI - Storage Komponens

## Áttekintés

A Storage komponens a Neural AI Next rendszer adattárolási rétege. Felelős a különböző típusú adatok perzisztens tárolásáért és betöltéséért, támogatva a DataFrame-ek és Python objektumok különböző formátumokban történő kezelését.

## Főbb funkciók

- DataFrame-ek mentése és betöltése (CSV, JSON, Excel)
- Python objektumok szerializációja
- Hierarchikus fájlrendszer kezelés
- Metaadatok kezelése
- Automatikus formátum felismerés
- Path objektum támogatás
- Biztonságos fájlműveletek
- Típusbiztos műveletek

## Telepítés és függőségek

A komponens a Neural AI keretrendszer részeként települ.

### Függőségek
- pandas: DataFrame műveletek
- pyyaml: YAML fájl támogatás (opcionális)
- openpyxl: Excel támogatás (opcionális)

## Használat

### 1. Alap használat

```python
from neural_ai.core.storage.implementations import FileStorage

# Storage inicializálása
storage = FileStorage("data")

# DataFrame műveletek
df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
storage.save_dataframe(df, "data.csv")
loaded_df = storage.load_dataframe("data.csv")

# Objektum műveletek
config = {"param1": 123, "param2": "value"}
storage.save_object(config, "config.json")
loaded_config = storage.load_object("config.json")
```

### 2. Haladó DataFrame műveletek

```python
# CSV mentés speciális beállításokkal
storage.save_dataframe(df, "data.csv",
    index=False,
    sep=";",
    date_format="%Y-%m-%d",
    float_format="%.2f"
)

# DataFrame betöltés szűréssel
df = storage.load_dataframe("data.csv",
    usecols=["id", "name"],
    parse_dates=["created_at"],
    dtype={"id": int}
)
```

### 3. Fájlrendszer műveletek

```python
# Fájl és könyvtár műveletek
files = storage.list_dir("data")
csv_files = storage.list_dir("data", "*.csv")

if storage.exists("old_data.csv"):
    storage.delete("old_data.csv")

metadata = storage.get_metadata("data.csv")
```

## Architektúra

A komponens felépítése:

```
neural_ai/core/storage/
├── interfaces/
│   ├── storage_interface.py   # Alap storage interfész
│   └── factory_interface.py   # Factory interfész
├── implementations/
│   ├── file_storage.py       # Fájl alapú implementáció
│   └── storage_factory.py    # Storage factory
└── exceptions.py            # Storage kivételek
```

### Főbb osztályok

1. **StorageInterface**
   - Adattárolási műveletek definiálása
   - DataFrame és objektum műveletek
   - Fájlrendszer műveletek

2. **FileStorage**
   - Fájl alapú implementáció
   - Formátum kezelés
   - Biztonságos fájlműveletek

3. **StorageFactory**
   - Storage példányok létrehozása
   - Konfiguráció kezelés
   - Alapértelmezett implementáció választás

## API gyorsreferencia

```python
# Storage inicializálás
storage = FileStorage("data")

# DataFrame műveletek
storage.save_dataframe(df, "path.csv", **kwargs)
df = storage.load_dataframe("path.csv", **kwargs)

# Objektum műveletek
storage.save_object(obj, "path.json")
obj = storage.load_object("path.json")

# Fájlrendszer műveletek
storage.exists("path")
storage.delete("path")
files = storage.list_dir("path", "*.csv")
meta = storage.get_metadata("path")
```

## Fejlesztői információk

### Új formátum támogatás hozzáadása

1. Bővítse a támogatott formátumok listáját
2. Implementálja a mentési és betöltési logikát
3. Adjon hozzá formátum-specifikus validációt
4. Írjon teszteket az új formátumhoz

### Hibakezelési konvenciók

```python
from neural_ai.core.storage.exceptions import (
    StorageError,             # Alap kivétel
    StorageNotFoundError,     # Nem létező erőforrás
    StorageFormatError,       # Formátum hiba
    StorageIOError,          # I/O műveleti hiba
    StorageValidationError   # Validációs hiba
)
```

## Tesztelés

```bash
# Unit tesztek futtatása
pytest tests/core/storage/

# Lefedettség ellenőrzése
pytest --cov=neural_ai.core.storage tests/core/storage/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_formátum`)
3. Változtatások commit-olása (`git commit -am 'Új formátum: xyz'`)
4. Branch feltöltése (`git push origin feature/új_formátum`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.

## További dokumentáció

- [API Dokumentáció](api.md)
- [Architektúra leírás](architecture.md)
- [Tervezési specifikáció](design_spec.md)
- [Példák](examples.md)
- [Fejlesztési checklist](development_checklist.md)
