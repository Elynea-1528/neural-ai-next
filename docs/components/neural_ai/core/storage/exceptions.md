# Storage Kivételek (`neural_ai.core.storage.exceptions`)

Ez a modul a Storage komponens által használt kivételosztályokat definiálja. A kivételek egy hierarchiát alkotnak, amelyek lehetővé teszik a hibák pontosabb kezelését és diagnosztizálását.

## Osztályok

### `StorageError`

Az összes storage kivétel alaposztálya.

**Leírás:**
Egy általános kivétel, amely a storage műveletek során fellépő hibákat csomagolja be. Tartalmazhat egy opcionális eredeti kivételt is a hibakeresés megkönnyítésére.

**Inicializálás:**
- `message` (`str`): Az emberi olvashatóságot szolgáló hibaüzenet.
- `original_error` (`Exception | None`, opcionális): Az a kivétel, amely a hiba kiváltásáért felelős. Alapértelmezett értéke `None`.

**Attribútumok:**
- `original_error`: Az eredeti kivétel referenciája, ha van.

**Használat:**
```python
try:
    storage.save("key", {"data": "value"})
except ValueError as e:
    raise StorageError("Nem sikerült elmenteni az adatot", e)
```

---

### `StorageFormatError`

Nem támogatott vagy érvénytelen formátum esetén dobott kivétel.

**Leírás:**
A `StorageError` leszármazottja. Akkor használatos, amikor a rendszer olyan adatot vagy formátumot próbál feldolgozni, amelyet nem támogat vagy érvénytelen.

**Használat:**
```python
if not data_format.startswith("json"):
    raise StorageFormatError(f"A(z) '{data_format}' formátum nem támogatott.")
```

---

### `StorageSerializationError`

Szerializációs vagy deszerializációs hiba esetén dobott kivétel.

**Leírás:**
A `StorageError` leszármazottja. Akkor dobódik, ha az adatok JSON-né (vagy más formátummá) való átalakítása vagy onnan való visszaalakítása sikertelen.

**Használat:**
```python
import json

try:
    serialized_data = json.dumps(complex_object)
except TypeError as e:
    raise StorageSerializationError("Az objektumot nem sikerült szerializálni.", e)
```

---

### `StorageIOError`

I/O (Input/Output) műveletek során fellépő hibák esetén dobott kivétel.

**Leírás:**
A `StorageError` leszármazottja. Fájlrendszerbeli hibák, írási/olvasási problémák esetén használatos.

**Használat:**
```python
try:
    with open(file_path, 'w') as f:
        f.write(data)
except OSError as e:
    raise StorageIOError(f"A(z) '{file_path}' fájlba írás sikertelen.", e)
```

---

### `StorageNotFoundError`

Nem létező erőforrás elérésekor dobott kivétel.

**Leírás:**
A `StorageError` leszármazottja. Akkor dobódik, amikor egy adott kulccsal, fájllal vagy más erőforrással kapcsolatos műveletet próbálnak végrehajtani, de az nem található.

**Használat:**
```python
if not os.path.exists(file_path):
    raise StorageNotFoundError(f"A(z) '{file_path}' fájl nem található.")
```

---

### `StorageValidationError`

Érvénytelen adat vagy paraméter esetén dobott kivétel.

**Leírás:**
A `StorageError` leszármazottja. Akkor használatos, amikor a tárolandó adatok vagy a művelet paraméterei nem felelnek meg a várt kritériumoknak (pl. séma validáció).

**Használat:**
```python
if not isinstance(data, dict):
    raise StorageValidationError("A tárolandó adatnak szótárnak kell lennie.")
```

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

## Hibakezelés

A kivételek használatának legjobb gyakorlata, hogy a lehető legkonkrétabb kivételt kapd el.

```python
from neural_ai.core.storage.exceptions import (
    StorageError,
    StorageNotFoundError,
    StorageIOError,
)

try:
    data = storage.load("user_profile_123")
except StorageNotFoundError:
    # Kezeld a nem található erőforrás esetét
    data = create_default_user_profile()
except StorageIOError as e:
    # Naplózd az I/O hibát
    logger.error(f"Storage I/O hiba: {e.original_error}")
except StorageError as e:
    # Általános storage hiba
    logger.error(f"Ismeretlen storage hiba: {e}")