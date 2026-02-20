# neural_ai/core/config/implementations/yaml_config_manager.py

YAML alapú konfigurációkezelő implementáció.

## Importok

```python
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Any
from typing import TypeVar
from typing import cast
import yaml
from pydantic import BaseModel
from pydantic import ValidationError
from neural_ai.core.config.exceptions import ConfigLoadError
# ... és még 11 import
```

## Konstansok

- **`T`**
: `TypeVar('T', bound=BaseModel)`


## Osztály: `ValidationContext`

Séma validációs kontextus.

Ez az osztály tartalmazza a validációs folyamat során szükséges adatokat.

## Osztály: `YAMLConfigManager(ConfigManagerInterface)`

YAML fájlokat kezelő konfigurációkezelő.

A konfigurációk mentésekor automatikusan hozzáadja a schema_version-t,
és betöltéskor ellenőrzi a kompatibilitást.

### Metódusok

#### `__init__()`

```python
def __init__(self, filename: str | None = None, logger: 'LoggerInterface | None' = None, storage: 'StorageInterface | None' = None) -> None
```

Inicializálja a YAML konfigurációkezelőt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: Konfigurációs fájl útvonala (opcionális)
- **`logger`** (`'LoggerInterface | None'`) = `None`: Logger interfész a naplózásra (opcionális)
- **`storage`** (`'StorageInterface | None'`) = `None`: Storage interfész a perzisztens tárolásra (opcionális)

**Visszatérési érték:**

- Típus: `None`

#### `_get_current_schema_version()`

```python
def _get_current_schema_version(self) -> str
```

Visszaadja a jelenlegi séma verzióját.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `str`
- str: A jelenlegi séma verziója

#### `_check_schema_compatibility()`

```python
def _check_schema_compatibility(self, loaded_version: str) -> bool
```

Ellenőrzi a betöltött séma kompatibilitását.

**Paraméterek:**

- **`self`**
- **`loaded_version`** (`str`): A betöltött konfiguráció séma verziója

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha kompatibilis, False egyébként

#### `_ensure_dict()`

```python
def _ensure_dict(data: Any) -> dict[str, Any]
```

Adatok dictionary típusának biztosítása.

**Paraméterek:**

- **`data`** (`Any`): Ellenőrizendő adatok

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- Dict[str, Any]: Az adatok dictionary formátumban

**Kivételek:**

- **`ConfigLoadError`**: Ha az adatok nem None és nem dictionary

#### `get()`

```python
def get(self) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `Any`
- A konfigurációs érték vagy az alapértelmezett érték

**Kivételek:**

- **`TypeError`**: Ha bármelyik kulcs nem string típusú

#### `get_system_config()`

```python
def get_system_config(self) -> SystemConfig
```

Rendszer konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `SystemConfig`
- SystemConfig: A rendszer konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen
- **`KeyError`**: Ha a 'system' szekció nem található

#### `get_storage_config()`

```python
def get_storage_config(self) -> StorageConfig
```

Tárolási konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `StorageConfig`
- StorageConfig: A tárolási konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. CSV storage)
- **`KeyError`**: Ha a 'storage' szekció nem található

#### `get_processors_config()`

```python
def get_processors_config(self) -> ProcessorsConfig
```

Processzorok konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `ProcessorsConfig`
- ProcessorsConfig: A processzorok konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. hibás timeframe)
- **`KeyError`**: Ha a 'processors' szekció nem található

#### `get_logging_config()`

```python
def get_logging_config(self) -> LoggingConfig
```

Naplózási konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `LoggingConfig`
- LoggingConfig: A naplózási konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. hibás log level)
- **`KeyError`**: Ha a 'logging' szekció nem található

#### `get_database_config()`

```python
def get_database_config(self) -> DatabaseConfig
```

Adatbázis konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `DatabaseConfig`
- DatabaseConfig: Az adatbázis konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. érvénytelen DB típus)
- **`KeyError`**: Ha a 'database' szekció nem található

#### `get_events_config()`

```python
def get_events_config(self) -> EventsConfig
```

Esemény rendszer konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `EventsConfig`
- EventsConfig: Az esemény rendszer konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. hibás port szám)
- **`KeyError`**: Ha az 'events' szekció nem található

#### `get_collectors_config()`

```python
def get_collectors_config(self) -> CollectorsConfig
```

Gyűjtők konfiguráció lekérése validálással.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `CollectorsConfig`
- CollectorsConfig: A gyűjtők konfigurációs adatai Pydantic modell formátumban.

**Kivételek:**

- **`ConfigValidationError`**: Ha a konfiguráció érvénytelen (pl. üres symbols lista)
- **`KeyError`**: Ha a 'collectors' szekció nem található

#### `get_validated_config()`

```python
def get_validated_config(self, key: str, schema: type[T]) -> T
```

Konfiguráció betöltés Pydantic validációval.

**Paraméterek:**

- **`self`**
- **`key`** (`str`): Konfiguráció kulcs (pl. "database", "logging")
- **`schema`** (`type[T]`): Pydantic BaseModel séma validációhoz

**Visszatérési érték:**

- Típus: `T`
- Validált Pydantic modell

**Kivételek:**

- **`ConfigValidationError`**: Ha a validáció sikertelen
- **`KeyError`**: Ha a kulcs nem található

#### `get_section()`

```python
def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**

- **`self`**
- **`section`** (`str`): A szekció neve

**Visszatérési érték:**

- Típus: `dict[str, Any]`
- A szekció konfigurációs adatai

**Kivételek:**

- **`KeyError`**: Ha a szekció nem található

#### `set()`

```python
def set(self) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**

- **`self`**

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha nincs kulcs megadva vagy érvénytelen hierarchia

#### `save()`

```python
def save(self, filename: str | None = None) -> None
```

Aktuális konfiguráció mentése fájlba. A konfiguráció mentésekor automatikusan hozzáadja a schema_version-t, hogy a jövőbeli betöltések kompatibilitást ellenőrizhessenek.

**Paraméterek:**

- **`self`**
- **`filename`** (`str | None`) = `None`: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ValueError`**: Ha nincs fájlnév megadva vagy mentési hiba történik

#### `load()`

```python
def load(self, filename: str) -> None
```

Konfiguráció betöltése fájlból. A betöltés során ellenőrzi a séma verzió kompatibilitást, ha a fájl tartalmaz verzióinformációt.

**Paraméterek:**

- **`self`**
- **`filename`** (`str`): A betöltendő fájl neve

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ConfigLoadError`**: Ha a fájl nem található vagy betöltési hiba történik

#### `validate()`

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**

- **`self`**
- **`schema`** (`dict[str, Any]`): A validációs séma definíció

**Visszatérési érték:**

- Típus: `tuple[bool, dict[str, str] | None]`
- Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

#### `_validate_dict()`

```python
def _validate_dict(self, ctx: ValidationContext) -> None
```

Rekurzív séma validáció.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus a konfigurációs adatokkal

**Visszatérési érték:**

- Típus: `None`

#### `_validate_required()`

```python
def _validate_required(self, ctx: ValidationContext) -> bool
```

Kötelező mező ellenőrzése.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha a mező érvényes, False ha hiányzik

#### `_validate_type()`

```python
def _validate_type(self, ctx: ValidationContext) -> bool
```

Típus ellenőrzése.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `bool`
- bool: True ha a típus érvényes, False ha nem

#### `_validate_nested()`

```python
def _validate_nested(self, ctx: ValidationContext) -> None
```

Beágyazott értékek validálása.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `None`

#### `_validate_constraints()`

```python
def _validate_constraints(self, ctx: ValidationContext) -> None
```

Érték korlátok validálása.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `None`

#### `_validate_choices()`

```python
def _validate_choices(self, ctx: ValidationContext) -> None
```

Választható értékek validálása.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `None`

#### `_validate_range()`

```python
def _validate_range(self, ctx: ValidationContext) -> None
```

Érték tartományának validálása.

**Paraméterek:**

- **`self`**
- **`ctx`** (`ValidationContext`): Validációs kontextus

**Visszatérési érték:**

- Típus: `None`

#### `load_directory()`

```python
def load_directory(self, path: str) -> None
```

Betölti az összes YAML fájlt egy mappából namespaced struktúrába. A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat az adott kulcs alá tölti be. A 'system.yaml' fájl tartalmát a gyökérbe is betölti az app_name, debug stb. elérhetősége érdekében.

**Paraméterek:**

- **`self`**
- **`path`** (`str`): A konfigurációs mappa útvonala

**Visszatérési érték:**

- Típus: `None`

**Kivételek:**

- **`ConfigLoadError`**: Ha a mappa nem található vagy betöltési hiba történik

---

**Forrásfájl:** [`neural_ai/core/config/implementations/yaml_config_manager.py`](../../neural_ai/core/config/implementations/yaml_config_manager.py)
