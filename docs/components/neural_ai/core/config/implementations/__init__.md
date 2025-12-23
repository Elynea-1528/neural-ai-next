# Konfigurációkezelő Implementációk (`neural_ai.core.config.implementations`)

## Áttekintés

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat, köztük a YAML alapú konfigurációkezelőt és a hozzá tartozó factory osztályt. A modul célja, hogy egységes és bővíthető interfészt nyújtson a konfigurációs fájlok kezeléséhez.

## Tartalom

### Exportált Komponensek

- **[`ConfigManagerFactory`](./config_manager_factory.md)**: Factory osztály konfigurációkezelők létrehozásához
- **[`YAMLConfigManager`](./yaml_config_manager.md)**: YAML fájlokat kezelő konfigurációkezelő implementáció
- **`__version__`**: A modul aktuális verziószáma (dinamikusan betöltve)
- **`SCHEMA_VERSION`**: A konfigurációs séma aktuális verziószáma

## Használat

### Alapvető Importálás

```python
from neural_ai.core.config.implementations import ConfigManagerFactory, YAMLConfigManager
```

### Gyors példa

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

# Konfigurációkezelő létrehozása
factory = ConfigManagerFactory()
config = factory.get_manager("config.yaml")

# Érték lekérése
database_host = config.get("database", "host")
log_level = config.get("logging", "level", default="INFO")

# Érték beállítása
config.set("database", "port", value=5432)

# Konfiguráció mentése
config.save()
```

### Factory használata különböző típusokhoz

```python
from neural_ai.core.config.implementations import ConfigManagerFactory

factory = ConfigManagerFactory()

# YAML fájl kezelése
yaml_config = factory.get_manager("config.yaml")

# Explicit típus megadása
yaml_config2 = factory.get_manager("config.yml", manager_type="yaml")

# Támogatott kiterjesztések lekérése
supported = factory.get_supported_extensions()
print(f"Támogatott formátumok: {supported}")
```

## Architektúra

### Osztálydiagram

```
ConfigManagerFactory
    ├── get_manager(filename, manager_type=None) -> ConfigManagerInterface
    ├── register_manager(extension, manager_class) -> None
    ├── get_supported_extensions() -> list[str]
    └── create_manager(manager_type, *args, **kwargs) -> ConfigManagerInterface

YAMLConfigManager implements ConfigManagerInterface
    ├── __init__(filename=None) -> None
    ├── get(*keys, default=None) -> Any
    ├── get_section(section) -> dict[str, Any]
    ├── set(*keys, value) -> None
    ├── save(filename=None) -> None
    ├── load(filename) -> None
    └── validate(schema) -> tuple[bool, dict[str, str] | None]
```

### Függőségek

- **Belső függőségek**:
  - `neural_ai.core.config.exceptions.ConfigLoadError`
  - `neural_ai.core.config.interfaces.ConfigManagerInterface`
  - `neural_ai.core.config.interfaces.FactoryInterface`

- **Külső függőségek**:
  - `yaml` (PyYAML csomag)

## Fejlesztés

### Új konfigurációs formátum hozzáadása

1. Hozz létre egy új osztályt, amely implementálja a `ConfigManagerInterface`-t
2. Regisztráld az új osztályt a `ConfigManagerFactory`-ban:

```python
from neural_ai.core.config.implementations import ConfigManagerFactory
from neural_ai.core.config.interfaces import ConfigManagerInterface

class JSONConfigManager(ConfigManagerInterface):
    # Implementáció...

# Regisztráció
ConfigManagerFactory.register_manager(".json", JSONConfigManager)
```

### Séma validáció

A `YAMLConfigManager` támogatja a konfigurációs adatok séma alapú validálását:

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

is_valid, errors = config.validate(schema)
if not is_valid:
    print(f"Validációs hibák: {errors}")
```

## Hibakezelés

A modul a következő kivételeket használja:

- **`ConfigLoadError`**: Konfigurációs fájl betöltési vagy feldolgozási hibák
- **`ValueError`**: Érvénytelen paraméterek vagy műveletek
- **`KeyError`**: Nem létező konfigurációs szekciók elérése

Példa hibakezelésre:

```python
from neural_ai.core.config.exceptions import ConfigLoadError
from neural_ai.core.config.implementations import ConfigManagerFactory

try:
    factory = ConfigManagerFactory()
    config = factory.get_manager("config.yaml")
    config.load("config.yaml")
except ConfigLoadError as e:
    print(f"Konfiguráció betöltése sikertelen: {e}")
except FileNotFoundError:
    print("A konfigurációs fájl nem található")
```

## Teljesítmény és Biztonság

### Teljesítmény

- **Lazy loading**: A konfigurációs fájlok csak akkor töltődnek be, amikor szükség van rájuk
- **Gyorsítótár**: A beolvasott konfigurációk memóriában vannak tárolva a gyors elérés érdekében
- **Hatékony keresés**: A beágyazott kulcsok hatékony keresése dictionary struktúrákban

### Biztonság

- **Safe load**: A YAML fájlok betöltése `yaml.safe_load()` használatával történik
- **Validáció**: Opcionális séma validáció a bemeneti adatok ellenőrzésére
- **Típusellenőrzés**: A beállított értékek típusának ellenőrzése validációs sémával

## Tesztelés

A modulhoz tartozó tesztek a `tests/core/config/implementations/` mappában találhatók:

- `test___init__.py`: Modul inicializálás és exportok tesztelése
- `test_config_manager_factory.py`: Factory osztály tesztelése
- `test_yaml_config_manager.py`: YAML kezelő tesztelése

Tesztek futtatása:

```bash
pytest tests/core/config/implementations/ -v
```

## Kapcsolódó Dokumentáció

- [Konfigurációkezelő Architektúra](../architecture.md)
- [Konfigurációs Interface](../interfaces/config_interface.md)
- [Factory Interface](../interfaces/factory_interface.md)
- [Hibakezelés](../exceptions.md)

## Verziókezelés

### Modul verziója

A modul verziószáma dinamikusan töltődik be a `pyproject.toml` fájlból:

```python
from neural_ai.core.config.implementations import __version__

print(f"Modul verziója: {__version__}")
```

### Konfigurációs séma verzió

A konfigurációs fájlokban használható a `schema_version` mező a séma verziójának
nyilvántartására. Ez lehetővé teszi a verziók közötti migrációkat és kompatibilitás-ellenőrzést.

```python
from neural_ai.core.config.implementations import SCHEMA_VERSION

# Aktuális séma verzió
print(f"Séma verzió: {SCHEMA_VERSION}")

# Konfiguráció betöltése és verzió ellenőrzése
config = factory.get_manager("config.yaml")
file_version = config.get("schema_version", default="1.0.0")

if file_version != SCHEMA_VERSION:
    print(f"Figyelem: A konfigurációs fájl verziója ({file_version}) eltér a támogatottól ({SCHEMA_VERSION})")
    # Verzió migráció végrehajtása...
```

### Verzió migrációs példa

```python
from neural_ai.core.config.implementations import ConfigManagerFactory, SCHEMA_VERSION

factory = ConfigManagerFactory()
config = factory.get_manager("config.yaml")

# Verzió ellenőrzése és migráció
current_version = config.get("schema_version", default="1.0.0")

if current_version == "1.0.0" and SCHEMA_VERSION == "1.1.0":
    # Migrációs lépések
    config.set("new_feature", "enabled", value=True)
    config.set("schema_version", value="1.1.0")
    config.save()
```

## Verziótörténet

- **v1.0.0** (2024-12-22): Kezdeti implementáció
  - YAML konfigurációkezelő
  - Factory pattern implementáció
  - Séma validáció támogatás
  - Dinamikus verzióbetöltés
  - Schema version kezelés