# YAMLConfigManager

Az YAMLConfigManager egy YAML fájlokat kezelő konfigurációkezelő implementáció, amely a `ConfigManagerInterface` interfészt valósítja meg.

## Áttekintés

Ez az osztály lehetővé teszi konfigurációs adatok YAML formátumban történő betöltését, mentését, lekérdezését és validálását. Támogatja a beágyazott struktúrákat, típusellenőrzést, séma alapú validációt és automatikus verziókezelést.

## Funkciók

- **Konfiguráció betöltése**: YAML fájlból történő adatbetöltés verzióellenőrzéssel
- **Konfiguráció mentése**: Adatok YAML formátumban történő mentése verzióinformációval
- **Érték lekérdezése**: Egyszerű és beágyazott értékek lekérdezése
- **Érték beállítása**: Konfigurációs értékek módosítása
- **Séma validáció**: Konfigurációs adatok validálása séma alapján
- **Verziókezelés**: Séma verziók ellenőrzése és kompatibilitás vizsgálata
- **Függőség injektálás**: Logger és Storage komponensek támogatása

## Osztálystruktúra

### ValidationContext

Belső adatosztály a validációs folyamat adatainak tárolására.

**Attribútumok:**
- `path` (str): Az aktuális konfigurációs útvonal
- `errors` (dict[str, str]): Validációs hibák gyűjteménye
- `value` (Any | None): Az ellenőrizendő érték
- `schema` (dict[str, Any]): A validációs séma

### YAMLConfigManager

Fő konfigurációkezelő osztály.

**Konstansok:**
- `_TYPE_MAP` (dict[str, type]): Típusleképezés a séma validáláshoz
- `_CURRENT_SCHEMA_VERSION` (str): A jelenlegi séma verziója

**Attribútumok:**
- `_config` (dict[str, Any]): A betöltött konfigurációs adatok
- `_filename` (str | None): Az aktuális konfigurációs fájl elérési útja
- `_logger` (LoggerInterface | None): Naplózó komponens
- `_storage` (StorageInterface | None): Tároló komponens

## Metódusok

### `__init__`

```python
def __init__(
    self,
    filename: str | None = None,
    logger: LoggerInterface | None = None,
    storage: StorageInterface | None = None,
) -> None
```

Inicializálja a YAML konfigurációkezelőt.

**Paraméterek:**
- `filename` (str | None): Konfigurációs fájl útvonala (opcionális)
- `logger` (LoggerInterface | None): Logger interfész a naplózásra (opcionális)
- `storage` (StorageInterface | None): Storage interfész a perzisztens tárolásra (opcionális)

### `get`

```python
def get(self, *keys: str, default: Any = None) -> Any
```

Érték lekérése a konfigurációból.

**Paraméterek:**
- `*keys` (str): A konfigurációs kulcsok hierarchiája
- `default` (Any): Alapértelmezett érték, ha a kulcs nem található

**Visszatérési érték:**
- A konfigurációs érték vagy az alapértelmezett érték

### `get_section`

```python
def get_section(self, section: str) -> dict[str, Any]
```

Teljes konfigurációs szekció lekérése.

**Paraméterek:**
- `section` (str): A szekció neve

**Visszatérési érték:**
- A szekció konfigurációs adatai

**Kivételek:**
- `KeyError`: Ha a szekció nem található

### `set`

```python
def set(self, *keys: str, value: Any) -> None
```

Érték beállítása a konfigurációban.

**Paraméterek:**
- `*keys` (str): A konfigurációs kulcsok hierarchiája
- `value` (Any): A beállítandó érték

**Kivételek:**
- `ValueError`: Ha nincs kulcs megadva vagy érvénytelen hierarchia

### `save`

```python
def save(self, filename: str | None = None) -> None
```

Aktuális konfiguráció mentése fájlba.

A konfiguráció mentésekor automatikusan hozzáadja a `_schema_version` mezőt a fájlhoz, hogy a jövőbeli betöltések kompatibilitást ellenőrizhessenek.

**Paraméterek:**
- `filename` (str | None): A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

**Kivételek:**
- `ValueError`: Ha nincs fájlnév megadva vagy mentési hiba történik

### `_get_current_schema_version`

```python
def _get_current_schema_version(self) -> str
```

Visszaadja a jelenlegi séma verzióját.

**Visszatérési érték:**
- str: A jelenlegi séma verziója

### `_check_schema_compatibility`

```python
def _check_schema_compatibility(self, loaded_version: str) -> bool
```

Ellenőrzi a betöltött séma kompatibilitását.

**Paraméterek:**
- `loaded_version` (str): A betöltött konfiguráció séma verziója

**Visszatérési érték:**
- bool: True ha kompatibilis, False egyébként

### `load`

```python
def load(self, filename: str) -> None
```

Konfiguráció betöltése fájlból.

A betöltés során ellenőrzi a séma verzió kompatibilitást, ha a fájl tartalmaz verzióinformációt. A verzióellenőrzés során figyelmeztetést naplóz, ha a betöltött verzió eltér a vártól.

**Paraméterek:**
- `filename` (str): A betöltendő fájl neve

**Kivételek:**
- `ConfigLoadError`: Ha a fájl nem található vagy betöltési hiba történik

### `validate`

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

Konfiguráció validálása séma alapján.

**Paraméterek:**
- `schema` (dict[str, Any]): A validációs séma definíció

**Visszatérési érték:**
- Tuple[bool, dict[str, str] | None]: (sikeres-e a validáció, hibák dictionary vagy None)

## Használati példa

### Alap inicializálás

```python
from neural_ai.core.config.implementations.yaml_config_manager import YAMLConfigManager

# Fájl nélküli inicializálás
manager = YAMLConfigManager()

# Fájllal történő inicializálás
manager = YAMLConfigManager(filename="config.yaml")
```

### Értékek lekérdezése

```python
# Egyszerű érték lekérdezése
host = manager.get("database", "host")

# Beágyazott érték lekérdezése
database_config = manager.get("database")

# Alapértelmezett érték használata
port = manager.get("database", "port", default=5432)

# Teljes szekció lekérdezése
database_section = manager.get_section("database")
```

### Értékek beállítása

```python
# Egyszerű érték beállítása
manager.set("key", value="value")

# Beágyazott érték beállítása
manager.set("database", "host", value="localhost")
manager.set("database", "port", value=5432)
```

### Konfiguráció mentése és betöltése

```python
# Konfiguráció betöltése
manager.load("config.yaml")

# Módosítások végrehajtása
manager.set("database", "host", value="new_host")

# Konfiguráció mentése
manager.save()

# Másik fájlba mentés
manager.save("backup_config.yaml")
```

### Séma validálás

```python
# Validációs séma definiálása
schema = {
    "database": {
        "type": "dict",
        "schema": {
            "host": {"type": "str"},
            "port": {"type": "int", "min": 1, "max": 65535},
            "username": {"type": "str", "optional": True}
        }
    },
    "logging": {
        "type": "dict",
        "schema": {
            "level": {
                "type": "str",
                "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]
            }
        }
    }
}

# Validálás végrehajtása
is_valid, errors = manager.validate(schema)

if not is_valid:
    print("Validációs hibák:", errors)
```

### Függőség injektálás

```python
from neural_ai.core.logger.implementations import DefaultLogger
from neural_ai.core.storage.implementations import FileStorage

# Logger és Storage komponensek injektálása
logger = DefaultLogger()
storage = FileStorage()

manager = YAMLConfigManager(
    filename="config.yaml",
    logger=logger,
    storage=storage
)
```

## Séma validáció

A séma validáció a következő típusokat támogatja:

### Alaptípusok

- `str`: Szöveges érték
- `int`: Egész szám
- `float`: Lebegőpontos szám
- `bool`: Logikai érték
- `list`: Lista
- `dict`: Szótár

### Validációs szabályok

- `type` (str): Az elvárt adattípus
- `optional` (bool): A mező opcionális (alapértelmezett: False)
- `choices` (list): Az elfogadható értékek listája
- `min` (int/float): Minimális érték (számokhoz)
- `max` (int/float): Maximális érték (számokhoz)
- `schema` (dict): Beágyazott séma (dict típushoz)

### Példa séma

```python
schema = {
    "database": {
        "type": "dict",
        "schema": {
            "host": {"type": "str"},
            "port": {"type": "int", "min": 1, "max": 65535},
            "ssl": {"type": "bool", "optional": True}
        }
    },
    "retry_count": {"type": "int", "min": 0, "max": 10},
    "log_level": {
        "type": "str",
        "choices": ["DEBUG", "INFO", "WARNING", "ERROR"]
    }
}
```

## Hibakezelés

Az osztály a következő kivételeket dobhatja:

- `ConfigLoadError`: Konfiguráció betöltési hibák
- `ValueError`: Érvénytelen paraméterek vagy műveletek
- `KeyError`: Nem létező konfigurációs szekció

## Függőségek

- `neural_ai.core.config.interfaces.ConfigManagerInterface`: Alapinterfész
- `neural_ai.core.config.exceptions.ConfigLoadError`: Kivétel osztály
- `neural_ai.core.logger.interfaces.LoggerInterface`: Naplózó interfész (opcionális)
- `neural_ai.core.storage.interfaces.StorageInterface`: Tároló interfész (opcionális)

## Verziókezelés

Az YAMLConfigManager automatikus verziókezelést valósít meg a konfigurációs séma kompatibilitásának biztosítására.

### Séma verzió követés

- **Mentéskor**: A rendszer automatikusan hozzáadja a `_schema_version` mezőt a mentett konfigurációhoz
- **Betöltéskor**: A rendszer ellenőrzi a betöltött verziót és figyelmeztet, ha eltérés van
- **Jelenlegi verzió**: `1.0` (a `_CURRENT_SCHEMA_VERSION` konstansban tárolva)

### Verzió kompatibilitás

A `_check_schema_compatibility` metódus kezeli a verzió kompatibilitást:
- Jelenleg csak a pontos verzió egyezést ellenőrzi
- Jövőbeli fejlesztés: verzió kompatibilitási mátrix implementálása

### Példa verziókezelésre

```python
# Konfiguráció mentése (automatikusan hozzáadja a verziót)
manager.save("config.yaml")

# A mentett fájl tartalmazni fogja:
# _schema_version: "1.0"
# database:
#   host: localhost
#   port: 5432

# Konfiguráció betöltése (verzióellenőrzéssel)
manager.load("config.yaml")
# Ha a verzió eltér, warning log jön
```

## Típusok

Az osztály szigorú típusellenőrzést használ a `mypy` kompatibilitás érdekében. Az `Any` típus használata minimalizálva van, és pontos típusokat használunk mindenhol.

## Thread Safety

Az osztály nem thread-safe. Több szál esetén külső szinkronizáció szükséges.

## Lásd még

- [`ConfigManagerInterface`](../interfaces/config_interface.md): Konfigurációkezelő interfész
- [`ConfigManagerFactory`](config_manager_factory.md): Konfigurációkezelő gyár
- [`ConfigLoadError`](../exceptions.md): Konfigurációs hibák