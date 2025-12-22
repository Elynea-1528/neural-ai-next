# Konfigurációkezelő Implementációk (`neural_ai.core.config.implementations`)

## Áttekintés

Ez a modul tartalmazza a különböző konfigurációkezelő implementációkat, köztük a YAML alapú konfigurációkezelőt és a hozzá tartozó factory osztályt. A modul célja, hogy egységes és bővíthető interfészt nyújtson a konfigurációs fájlok kezeléséhez.

## Tartalom

### Exportált Osztályok

- **[`ConfigManagerFactory`](./config_manager_factory.md)**: Factory osztály konfigurációkezelők létrehozásához
- **[`YAMLConfigManager`](./yaml_config_manager.md)**: YAML fájlokat kezelő konfigurációkezelő implementáció

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

## Verziótörténet

- **v1.0.0** (2024-12-22): Kezdeti implementáció
  - YAML konfigurációkezelő
  - Factory pattern implementáció
  - Séma validáció támogatás