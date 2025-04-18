# Neural AI - Storage Komponens

## Áttekintés

A storage komponens felelős az adatok perzisztens tárolásáért és betöltéséért. Támogatja a DataFrame-ek és Python objektumok különböző formátumokban történő mentését és betöltését.

## Főbb funkciók

- DataFrame-ek mentése és betöltése (CSV, JSON)
- Python objektumok szerializálása (JSON)
- Hierarchikus fájlrendszer kezelés
- Metaadatok kezelése
- Fájl és könyvtár műveletek

## Telepítés

A komponens a Neural AI keretrendszer részeként települ. Külön telepítést nem igényel.

## Használat

### Alap használat

```python
from neural_ai.core.storage.implementations import FileStorage

# Storage példány létrehozása
storage = FileStorage("data")

# DataFrame mentése és betöltése
df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
storage.save_dataframe(df, "data.csv")
loaded_df = storage.load_dataframe("data.csv")

# Python objektum mentése és betöltése
obj = {"config": {"param1": 123, "param2": "value"}}
storage.save_object(obj, "config.json")
loaded_obj = storage.load_object("config.json")

# Fájl műveletek
storage.exists("data.csv")  # True
metadata = storage.get_metadata("data.csv")
storage.delete("old_data.csv")

# Könyvtár listázás
files = storage.list_dir(".")
csv_files = storage.list_dir(".", "*.csv")
```

### Támogatott formátumok

#### DataFrame formátumok
- CSV (.csv)
- JSON (.json)
- Excel (.xlsx) - opcionális, függ a pandas excel támogatástól

#### Objektum formátumok
- JSON (.json)

### Hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageFormatError,
    StorageNotFoundError,
    StorageSerializationError,
)

try:
    storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError:
    print("A fájl nem található")
except StorageFormatError:
    print("Nem támogatott formátum")
except StorageError as e:
    print(f"Egyéb storage hiba: {e}")
```

## API Dokumentáció

### FileStorage

```python
class FileStorage:
    """Fájl alapú storage implementáció."""

    def __init__(self, base_path: Optional[str] = None) -> None:
        """Storage inicializálása.

        Args:
            base_path: Alap könyvtár útvonal (None esetén az aktuális könyvtár)
        """

    def save_dataframe(self, df: pd.DataFrame, path: str, format: str = "csv", **kwargs) -> None:
        """DataFrame mentése.

        Args:
            df: A mentendő DataFrame
            path: Mentési útvonal
            format: Fájl formátum (csv, json, excel)
            **kwargs: További formátum-specifikus paraméterek
        """

    def load_dataframe(self, path: str, format: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """DataFrame betöltése.

        Args:
            path: Betöltési útvonal
            format: Fájl formátum (ha None, akkor a kiterjesztésből)
            **kwargs: További formátum-specifikus paraméterek

        Returns:
            pd.DataFrame: A betöltött DataFrame
        """
```

## Fejlesztői információk

### Új formátum hozzáadása

1. Bővítse a `_DATAFRAME_FORMATS` vagy `_OBJECT_FORMATS` konstansokat.
2. Implementálja a megfelelő mentési/betöltési logikát.
3. Frissítse a dokumentációt.
4. Írjon teszteket az új formátumhoz.

### Hibakezelési konvenciók

- `StorageFormatError`: Nem támogatott vagy érvénytelen formátum esetén
- `StorageNotFoundError`: Nem létező erőforrás esetén
- `StorageSerializationError`: Szerializációs hibák esetén
- `StorageIOError`: Egyéb I/O műveletek hibái esetén

## Tesztelés

```bash
pytest tests/core/storage/
```

## Közreműködés

1. Fork létrehozása
2. Feature branch létrehozása (`git checkout -b feature/új_formátum`)
3. Változtatások commit-olása (`git commit -am 'Új formátum: xyz'`)
4. Branch feltöltése (`git push origin feature/új_formátum`)
5. Pull Request nyitása

## Licensz

MIT License - lásd a LICENSE fájlt a részletekért.
