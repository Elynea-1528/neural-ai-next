# YAMLConfigManager

## Áttekintés

Az `YAMLConfigManager` egy YAML fájlokat kezelő konfigurációkezelő implementáció, amely a [`ConfigManagerInterface`](../interfaces/config_interface.md) interfészt valósítja meg. A konfigurációk mentésekor automatikusan hozzáadja a schema verziót, és betöltéskor ellenőrzi a kompatibilitást.

## Osztályok

### ValidationContext

Séma validációs kontextus, amely tartalmazza a validációs folyamat során szükséges adatokat.

**Attribútumok:**
- `path` (str): A validálandó konfigurációs útvonal
- `errors` (dict[str, str]): A validációs hibák gyűjtője
- `value` (Any | None): A validálandó érték
- `schema` (dict[str, Any]): A validációs séma definíció

### YAMLConfigManager

YAML fájlokat kezelő konfigurációkezelő osztály.

#### Inicializálás

```python
def __init__(
    self,
    filename: str | None = None,
    logger: LoggerInterface | None = None,
    storage: StorageInterface | None = None,
) -> None
```

**Paraméterek:**
- `filename`: Konfigurációs fájl útvonala (opcionális)
- `logger`: Logger interfész a naplózásra (opcionális)
- `storage`: Storage interfész a perzisztens tárolásra (opcionális)

#### Főbb metódusok

##### get()

Érték lekérése a konfigurációból.

```python
def get(self, *keys: str, default: Any = None) -> Any
```

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `default`: Alapértelmezett érték, ha a kulcs nem található

**Visszatérési érték:** A konfigurációs érték vagy az alapértelmezett érték

##### get_section()

Teljes konfigurációs szekció lekérése.

```python
def get_section(self, section: str) -> dict[str, Any]
```

**Paraméterek:**
- `section`: A szekció neve

**Visszatérési érték:** A szekció konfigurációs adatai

**Kivételek:**
- `KeyError`: Ha a szekció nem található

##### set()

Érték beállítása a konfigurációban.

```python
def set(self, *keys: str, value: Any) -> None
```

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `value`: A beállítandó érték

**Kivételek:**
- `ValueError`: Ha nincs kulcs megadva vagy érvénytelen hierarchia

##### save()

Aktuális konfiguráció mentése fájlba. A konfiguráció mentésekor automatikusan hozzáadja a `schema_version`-t.

```python
def save(self, filename: str | None = None) -> None
```

**Paraméterek:**
- `filename`: A mentési fájl neve (opcionális, alapértelmezett az eredeti fájlnév)

**Kivételek:**
- `ValueError`: Ha nincs fájlnév megadva vagy mentési hiba történik

##### load()

Konfiguráció betöltése fájlból. A betöltés során ellenőrzi a séma verzió kompatibilitást.

```python
def load(self, filename: str) -> None
```

**Paraméterek:**
- `filename`: A betöltendő fájl neve

**Kivételek:**
- `ConfigLoadError`: Ha a fájl nem található vagy betöltési hiba történik

##### load_directory()

Betölti az összes YAML fájlt egy mappából namespaced struktúrába. A fájlneveket (kiterjesztés nélkül) használja kulcsként, és a tartalmukat az adott kulcs alá tölti be. A `system.yaml` fájl tartalmát a gyökérbe is betölti.

```python
def load_directory(self, path: str) -> None
```

**Paraméterek:**
- `path`: A konfigurációs mappa útvonala

**Kivételek:**
- `ConfigLoadError`: Ha a mappa nem található vagy betöltési hiba történik

##### validate()

Konfiguráció validálása séma alapján.

```python
def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]
```

**Paraméterek:**
- `schema`: A validációs séma definíció

**Visszatérési érték:** (sikeres-e a validáció, hibák dictionary vagy None)

#### Validációs séma formátum

A validációs séma a következő mezőket támogatja:

- `type`: Az elvárt típus ("str", "int", "float", "bool", "list", "dict")
- `optional`: Logikai érték, ha True, a mező opcionális (alapértelmezett: False)
- `schema`: Beágyazott séma definíció (csak "dict" típusnál)
- `choices`: Elfogadható értékek listája
- `min`: Minimális érték (csak számoknál)
- `max`: Maximális érték (csak számoknál)

**Példa séma:**

```yaml
database:
  type: dict
  schema:
    host:
      type: str
    port:
      type: int
      min: 1
      max: 65535
    debug:
      type: bool
      optional: true
```

#### Belső metódusok

##### _validate_dict()

Rekurzív séma validációt végző belső metódus.

##### _validate_required()

Kötelező mező ellenőrzése.

##### _validate_type()

Típus ellenőrzése.

##### _validate_nested()

Beágyazott értékek validálása.

##### _validate_constraints()

Érték korlátok validálása (choices, range).

## Használati példa

```python
from neural_ai.core.config.factory import ConfigManagerFactory

# Konfigurációkezelő létrehozása
config_manager = ConfigManagerFactory.get_manager("config.yaml")

# Érték lekérése
host = config_manager.get("database", "host", default="localhost")
port = config_manager.get("database", "port", default=5432)

# Érték beállítása
config_manager.set("database", "timeout", 30)

# Konfiguráció mentése
config_manager.save()

# Validálás séma alapján
schema = {
    "database": {
        "type": "dict",
        "schema": {
            "host": {"type": "str"},
            "port": {"type": "int", "min": 1, "max": 65535}
        }
    }
}
is_valid, errors = config_manager.validate(schema)
```

## Jellemzők

- **Séma verziókezelés:** Automatikus verzió ellenőrzés betöltéskor
- **Típusos validáció:** Szigorú típus ellenőrzés séma alapján
- **Hierarchikus struktúra:** Támogatja a beágyazott konfigurációs struktúrákat
- **Mappa betöltés:** Egyszerre több YAML fájl betöltése namespaced struktúrába
- **Kompatibilitás:** Visszamenőleges kompatibilitás ellenőrzése

## Kapcsolódó dokumentáció

- [`ConfigManagerInterface`](../interfaces/config_interface.md) - Az interfész definíciója
- [`ConfigManagerFactory`](../factory.md) - Factory osztály a konfigurációkezelők létrehozásához
- [`ConfigLoadError`](../exceptions/config_error.md) - Konfigurációs betöltési hibák