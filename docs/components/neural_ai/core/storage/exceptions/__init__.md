# Storage Kivételek

## Áttekintés

Ez a modul a Storage komponens kivétel osztályait tartalmazza. A kivételek hierarchikus szerkezetűek, amelyek lehetővé teszik a részletes hibakezelést és a specifikus hibahelyzetek megkülönböztetését.

## Kivétel Hierarchia

```
Exception
└── StorageError
    ├── StorageFormatError
    ├── StorageSerializationError
    ├── StorageIOError
    ├── StorageNotFoundError
    └── StorageValidationError
```

## Kivétel Osztályok

### `StorageError`

Alap kivétel a storage műveletekhez.

```python
class StorageError(Exception):
    def __init__(self, message: str, original_error: Exception | None = None) -> None
```

**Paraméterek:**
- `message`: Hibaüzenet
- `original_error`: Eredeti kivétel, ha van

**Attribútumok:**
- `original_error`: Az eredeti kivétel objektum (opcionális)

**Példa:**

```python
try:
    storage.save_dataframe(df, "invalid/path/data.csv")
except StorageError as e:
    print(f"Hiba történt: {e}")
    if e.original_error:
        print(f"Eredeti hiba: {e.original_error}")
```

### `StorageFormatError`

Nem támogatott vagy érvénytelen formátum esetén dobott kivétel.

```python
class StorageFormatError(StorageError)
```

**Használati esetek:**
- Ismeretlen fájlformátum megadása
- Nem támogatott DataFrame formátum
- Érvénytelen konverziós paraméterek

**Példa:**

```python
try:
    storage.save_dataframe(df, "data.xyz")  # Ismeretlen kiterjesztés
except StorageFormatError as e:
    print(f"Formátum hiba: {e}")
```

### `StorageSerializationError`

Szerializációs vagy deszerializációs hiba esetén dobott kivétel.

```python
class StorageSerializationError(StorageError)
```

**Használati esetek:**
- Nem szerializálható objektum mentése
- Sérült JSON/CSV fájl betöltése
- Adatintegritási problémák

**Példa:**

```python
class NonSerializableClass:
    def __init__(self):
        self.file_handle = open("test.txt")

try:
    obj = NonSerializableClass()
    storage.save_object(obj, "object.json")
except StorageSerializationError as e:
    print(f"Szerializációs hiba: {e}")
```

### `StorageIOError`

I/O műveletek során fellépő hibák esetén dobott kivétel.

```python
class StorageIOError(StorageError)
```

**Használati esetek:**
- Lemezterület elfogyott
- Fájlrendszer hozzáférés megtagadva
- Hálózati hiba (távoli tárolók esetén)
- Olvasási/írási művelet sikertelen

**Példa:**

```python
try:
    # Próbáljunk írni egy csak olvasható könyvtárba
    storage.save_dataframe(df, "/readonly/data.csv")
except StorageIOError as e:
    print(f"IO hiba: {e}")
```

### `StorageNotFoundError`

Nem létező erőforrás esetén dobott kivétel.

```python
class StorageNotFoundError(StorageError)
```

**Használati esetek:**
- Nem létező fájl betöltése
- Hiányzó könyvtár elérése
- Törölt erőforrás használata

**Példa:**

```python
try:
    df = storage.load_dataframe("nonexistent.csv")
except StorageNotFoundError as e:
    print(f"Fájl nem található: {e}")
    # Kezeljük a hiányzó fájlt
    df = create_default_dataframe()
```

### `StorageValidationError`

Érvénytelen adat vagy paraméter esetén dobott kivétel.

```python
class StorageValidationError(StorageError)
```

**Használati esetek:**
- Érvénytelen útvonal formátum
- Hiányzó kötelező paraméterek
- Adatok érvényességének ellenőrzése során fellépő hiba

**Példa:**

```python
try:
    # Érvénytelen útvonal
    storage.save_dataframe(df, "")
except StorageValidationError as e:
    print(f"Validációs hiba: {e}")
```

## Használat

### Alapvető Hibakezelés

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageFormatError,
    StorageIOError,
    StorageNotFoundError
)

try:
    storage.save_dataframe(df, "data.csv")
except StorageNotFoundError:
    # Fájl nem található - létrehozzuk
    storage.save_dataframe(df, "data.csv")
except StorageIOError as e:
    # IO hiba - naplózzuk és dobjuk tovább
    logger.error(f"IO hiba: {e}")
    raise
except StorageError as e:
    # Általános storage hiba
    logger.error(f"Storage hiba: {e}")
```

### Részletes Hibaanalízis

```python
try:
    df = storage.load_dataframe("data.csv")
except StorageError as e:
    if isinstance(e, StorageNotFoundError):
        # Fájl nem létezik, hozzuk létre
        df = create_default_dataframe()
        storage.save_dataframe(df, "data.csv")
    elif isinstance(e, StorageFormatError):
        # Formátum probléma, próbáljuk meg konvertálni
        df = convert_from_legacy_format("data.csv")
    elif isinstance(e, StorageIOError):
        # IO probléma, próbáljuk meg újra
        time.sleep(1)
        df = storage.load_dataframe("data.csv")
    else:
        # Ismeretlen hiba
        raise
```

### Egyéni Hibaüzenetek

```python
from neural_ai.core.storage.exceptions import StorageError

def save_with_retry(storage, data, path, max_retries=3):
    for attempt in range(max_retries):
        try:
            storage.save_dataframe(data, path)
            return
        except StorageIOError as e:
            if attempt == max_retries - 1:
                raise StorageError(
                    f"Az adatok mentése sikertelen {max_retries} próbálkozás után",
                    original_error=e
                )
            time.sleep(2 ** attempt)  # Exponenciális backoff
```

## Exportált Kivételek

A modul a következő kivétel osztályokat exportálja:

- `StorageError`
- `StorageFormatError`
- `StorageSerializationError`
- `StorageIOError`
- `StorageNotFoundError`
- `StorageValidationError`

## Best Practices

1. **Specifikus kivételek használata**: Mindig próbáljunk meg a legspecifikusabb kivételt elkapni
2. **Eredeti hiba megőrzése**: Használjuk az `original_error` paramétert a hibák láncolásához
3. **Részletes hibaüzenetek**: Adjunk meg informatív hibaüzeneteket a hibakeresés megkönnyítéséhez
4. **Hiba visszajelzés**: Naplózzuk a hibákat a rendszer állapotának nyomon követéséhez