# ConfigManagerFactory

## Áttekintés

Konfiguráció kezelő factory implementáció.

## Osztály

### `ConfigManagerFactory`

Factory osztály konfiguráció kezelők létrehozásához.

Ez az osztály a `ConfigManagerFactoryInterface` interfészt implementálja, és felelős a különböző típusú konfigurációkezelők létrehozásáért és regisztrálásáért.

#### Osztályszintű Attribútumok

- `_manager_types`: Szótár, amely a fájlkiterjesztéseket társítja a konfigurációkezelő osztályokhoz

#### Osztálymetódusok

##### `register_manager(extension, manager_class)`

Új konfiguráció kezelő típus regisztrálása.

**Paraméterek:**
- `extension`: A kezelt fájl kiterjesztése (pl: ".yml")
- `manager_class`: A kezelő osztály

**Visszatérési érték:**
- `None`

##### `get_manager(filename, manager_type)`

Megfelelő konfiguráció kezelő létrehozása.

A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

**Paraméterek:**
- `filename`: Konfigurációs fájl neve
- `manager_type`: Kért kezelő típus (opcionális)

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő

**Kivételek:**
- `ConfigLoadError`: Ha nem található megfelelő kezelő

##### `get_supported_extensions()`

Támogatott fájl kiterjesztések lekérése.

**Visszatérési érték:**
- `list[str]`: A támogatott kiterjesztések listája

##### `create_manager(manager_type, *args, **kwargs)`

Konfiguráció kezelő létrehozása típus alapján.

A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt, lehetővé téve a paraméterek átadását a konstruktornak.

**Paraméterek:**
- `manager_type`: A kért kezelő típus
- `*args`: Pozícionális paraméterek
- `**kwargs`: Kulcsszavas paraméterek

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő

**Kivételek:**
- `ConfigLoadError`: Ha nem található megfelelő kezelő

## Használati Példák

### Alap konfigurációkezelő létrehozása

```python
from neural_ai.core.config.factory import ConfigManagerFactory

# Fájlnév alapján automatikus kiválasztás
config_manager = ConfigManagerFactory.get_manager("config.yml")

# Explicit típusmegadás
yaml_manager = ConfigManagerFactory.get_manager("config.txt", manager_type="yaml")
```

### Egyéni kezelő regisztrálása

```python
from neural_ai.core.config.factory import ConfigManagerFactory
from neural_ai.core.config.interfaces import ConfigManagerInterface

class JSONConfigManager(ConfigManagerInterface):
    # Implementáció...
    pass

# Regisztrálás
ConfigManagerFactory.register_manager(".json", JSONConfigManager)

# Használat
json_config = ConfigManagerFactory.get_manager("config.json")
```

### Támogatott kiterjesztések lekérdezése

```python
from neural_ai.core.config.factory import ConfigManagerFactory

extensions = ConfigManagerFactory.get_supported_extensions()
print(f"Támogatott kiterjesztések: {extensions}")
# ['.yml', '.yaml']
```

### Kezelő létrehozása paraméterekkel

```python
from neural_ai.core.config.factory import ConfigManagerFactory

# YAML kezelő létrehozása egyéni paraméterekkel
config = ConfigManagerFactory.create_manager(
    "yaml",
    filename="config.yml",
    logger=my_logger,
    storage=my_storage
)
```

## Támogatott Formátumok

A factory alapértelmezés szerint a következő formátumokat támogatja:

- **.yml**: YAML konfigurációk (YAMLConfigManager)
- **.yaml**: YAML konfigurációk (YAMLConfigManager)

További formátumok regisztrálhatók a `register_manager` metódussal.

## Kapcsolódó Dokumentáció

- [Config Modul](__init__.md)
- [YAMLConfigManager](implementations/yaml_config_manager.md)
- [ConfigManagerInterface](interfaces/config_interface.md)
- [ConfigManagerFactoryInterface](interfaces/factory_interface.md)