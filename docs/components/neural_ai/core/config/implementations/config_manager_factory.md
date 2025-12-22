# ConfigManagerFactory

## Áttekintés

A `ConfigManagerFactory` osztály egy factory implementáció, amely konfiguráció kezelő objektumokat hoz létre különböző fájlformátumokhoz. Az osztály támogatja a dinamikus regisztrációt és a kiterjesztés alapú automatikus felismerést.

## Osztály

```python
class ConfigManagerFactory(ConfigManagerFactoryInterface)
```

## Metódusok

### `register_manager()`

Új konfiguráció kezelő típus regisztrálása.

```python
@classmethod
def register_manager(
    cls, 
    extension: str, 
    manager_class: type[ConfigManagerInterface]
) -> None
```

**Paraméterek:**
- `extension` (str): A kezelt fájl kiterjesztése (pl: ".yml")
- `manager_class` (type[ConfigManagerInterface]): A kezelő osztály

**Példa:**
```python
ConfigManagerFactory.register_manager(".json", JSONConfigManager)
```

---

### `get_manager()`

Megfelelő konfiguráció kezelő létrehozása fájlnév vagy explicit típus alapján.

```python
@classmethod
def get_manager(
    cls, 
    filename: str | Path, 
    manager_type: str | None = None
) -> ConfigManagerInterface
```

**Paraméterek:**
- `filename` (str | Path): Konfigurációs fájl neve
- `manager_type` (str | None): Kért kezelő típus (opcionális)

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő

**Kivételek:**
- `ConfigLoadError`: Ha nem található megfelelő kezelő

**Példák:**
```python
# Automatikus felismerés kiterjesztés alapján
manager = ConfigManagerFactory.get_manager("config.yml")

# Explicit típus megadása
manager = ConfigManagerFactory.get_manager("config", manager_type="yaml")
```

---

### `get_supported_extensions()`

Támogatott fájl kiterjesztések lekérése.

```python
@classmethod
def get_supported_extensions(cls) -> list[str]
```

**Visszatérési érték:**
- `list[str]`: A támogatott kiterjesztések listája

**Példa:**
```python
extensions = ConfigManagerFactory.get_supported_extensions()
# Visszaadja: [".yml", ".yaml"]
```

---

### `create_manager()`

Konfiguráció kezelő létrehozása típus alapján.

```python
@classmethod
def create_manager(
    cls, 
    manager_type: str, 
    *args: Any, 
    **kwargs: Any
) -> ConfigManagerInterface
```

**Paraméterek:**
- `manager_type` (str): A kért kezelő típus
- `*args`: Pozícionális paraméterek
- `**kwargs`: Kulcsszavas paraméterek

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott kezelő

**Kivételek:**
- `ConfigLoadError`: Ha nem található megfelelő kezelő

**Példa:**
```python
manager = ConfigManagerFactory.create_manager(
    "yaml", 
    filename="config.yml"
)
```

## Támogatott Formátumok

Alapértelmezett támogatás:
- `.yml` - YAML formátum
- `.yaml` - YAML formátum

## Használati Példák

### Alap Használat

```python
from pathlib import Path
from neural_ai.core.config.implementations.config_manager_factory import (
    ConfigManagerFactory
)

# 1. Automatikus kiterjesztés felismerés
manager = ConfigManagerFactory.get_manager("config.yml")

# 2. Explicit típus megadása
manager = ConfigManagerFactory.get_manager(
    "config", 
    manager_type="yaml"
)

# 3. Path objektum használata
path = Path("/path/to/config.yaml")
manager = ConfigManagerFactory.get_manager(path)
```

### Egyéni Manager Regisztrálása

```python
from neural_ai.core.config.interfaces.config_interface import (
    ConfigManagerInterface
)

class JSONConfigManager(ConfigManagerInterface):
    """JSON konfiguráció kezelő."""
    # Implementáció...

# Regisztrálás
ConfigManagerFactory.register_manager(".json", JSONConfigManager)

# Használat
manager = ConfigManagerFactory.get_manager("config.json")
```

### Támogatott Kiterjesztések Lekérdezése

```python
extensions = ConfigManagerFactory.get_supported_extensions()
print(f"Támogatott kiterjesztések: {extensions}")
# Kimenet: Támogatott kiterjesztések: ['.yml', '.yaml', '.json']
```

## Hibakezelés

A factory a következő esetekben dob `ConfigLoadError` kivételt:

1. **Ismeretlen típus:** Ha explicit módon megadott típus nincs regisztrálva
2. **Nem támogatott kiterjesztés:** Ha a fájlnév kiterjesztése nem ismert

**Példa hibakezelésre:**
```python
from neural_ai.core.config.exceptions import ConfigLoadError

try:
    manager = ConfigManagerFactory.get_manager("config.xyz")
except ConfigLoadError as e:
    print(f"Hiba történt: {e}")
    # Kimenet: Hiba történt: Nem található konfig kezelő...
```

## Implementáció Részletek

### Belső Szerkezet

```python
class ConfigManagerFactory(ConfigManagerFactoryInterface):
    _manager_types: dict[str, type[ConfigManagerInterface]] = {
        ".yml": YAMLConfigManager,
        ".yaml": YAMLConfigManager,
    }
```

A regisztrált manager típusok egy szótárban vannak tárolva, ahol a kulcs a fájl kiterjesztés, az érték pedig a megfelelő manager osztály.

### Alapértelmezett Viselkedés

- Ha a fájlnévnek nincs kiterjesztése, alapértelmezésként YAML kezelőt hoz létre
- A kiterjesztés-egyeztetés kis- és nagybetűérzéketlen

## Kapcsolódó Komponensek

- [`ConfigManagerInterface`](../interfaces/config_interface.md) - A konfiguráció kezelők interfésze
- [`ConfigManagerFactoryInterface`](../interfaces/factory_interface.md) - A factory interfész
- [`YAMLConfigManager`](yaml_config_manager.md) - YAML konfiguráció kezelő implementáció
- [`ConfigLoadError`](../exceptions.md) - Konfigurációs betöltési hiba

## Forráskód

- **Fájl:** [`neural_ai/core/config/implementations/config_manager_factory.py`](../../../../neural_ai/core/config/implementations/config_manager_factory.py)