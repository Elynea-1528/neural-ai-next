# ConfigManagerInterface

## Áttekintés

Konfiguráció kezelő interfész.

## Interfész

### `ConfigManagerInterface`

Konfigurációkezelő interfész.

Ez az interfész definiálja a konfigurációkezelők által implementálandó metódusokat.

#### Absztrakt Metódusok

##### `__init__(filename)`

Inicializálja a konfigurációkezelőt.

**Paraméterek:**
- `filename`: Konfigurációs fájl útvonala (opcionális)

##### `get(*keys, default)`

Érték lekérése a konfigurációból.

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `default`: Alapértelmezett érték, ha a kulcs nem található

**Visszatérési érték:**
- `Any`: A konfigurációs érték vagy az alapértelmezett érték

##### `get_section(section)`

Teljes konfigurációs szekció lekérése.

**Paraméterek:**
- `section`: A szekció neve

**Visszatérési érték:**
- `dict[str, Any]`: A szekció konfigurációs adatai

##### `set(*keys, value)`

Érték beállítása a konfigurációban.

**Paraméterek:**
- `*keys`: A konfigurációs kulcsok hierarchiája
- `value`: A beállítandó érték

##### `save(filename)`

Konfiguráció mentése fájlba.

**Paraméterek:**
- `filename`: A mentési fájl neve (opcionális)

##### `load(filename)`

Konfiguráció betöltése fájlból.

**Paraméterek:**
- `filename`: A betöltendő fájl neve

##### `validate(schema)`

Konfiguráció validálása séma alapján.

**Paraméterek:**
- `schema`: A validáláshoz használt séma

**Visszatérési érték:**
- `tuple[bool, dict[str, str] | None]`: (érvényes-e, hibák szótára)

## Implementáció

Ez az interfész a következő osztályok által van implementálva:

- [`YAMLConfigManager`](../implementations/yaml_config_manager.md#yamlconfigmanager)

## Használati Példa

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface
from typing import Any

class JSONConfigManager(ConfigManagerInterface):
    """JSON konfigurációkezelő implementáció."""
    
    def __init__(self, filename: str | None = None):
        self._config: dict[str, Any] = {}
        self._filename = filename
        if filename:
            self.load(filename)
    
    def get(self, *keys: str, default: Any = None) -> Any:
        """Érték lekérése a konfigurációból."""
        current = self._config
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key)
            if current is None:
                return default
        return current
    
    def get_section(self, section: str) -> dict[str, Any]:
        """Teljes konfigurációs szekció lekérése."""
        if section not in self._config:
            raise KeyError(f"Konfigurációs szekció nem található: {section}")
        return self._config.get(section, {})
    
    def set(self, *keys: str, value: Any) -> None:
        """Érték beállítása a konfigurációban."""
        if not keys:
            raise ValueError("Legalább egy kulcsot meg kell adni")
        
        current = self._config
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                raise ValueError(f"Nem lehet beágyazott kulcsot beállítani: {key}")
            current = current[key]
        current[keys[-1]] = value
    
    def save(self, filename: str | None = None) -> None:
        """Konfiguráció mentése fájlba."""
        import json
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("Nincs fájlnév megadva")
        
        with open(save_filename, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def load(self, filename: str) -> None:
        """Konfiguráció betöltése fájlból."""
        import json
        with open(filename, 'r') as f:
            self._config = json.load(f)
        self._filename = filename
    
    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        """Konfiguráció validálása séma alapján."""
        errors = {}
        # Egyszerűsített validáció
        for key, expected_type in schema.items():
            value = self._config.get(key)
            if value is not None and not isinstance(value, expected_type):
                errors[key] = f"Várt típus: {expected_type.__name__}"
        
        return not bool(errors), errors if errors else None
```

## Metódus Részletek

### get(*keys, default)

A metódus lehetővé teszi a konfigurációban lévő értékek hierarchikus lekérdezését. A kulcsokat pontokkal elválasztva vagy külön argumentumokként lehet megadni.

**Példa:**
```python
# Hierarchikus kulcsok
value1 = config.get("database", "host", default="localhost")
value2 = config.get("database.host", default="localhost")
```

### get_section(section)

Egy teljes konfigurációs szekciót ad vissza dictionary formátumban. Hasznos, ha egy egész konfigurációs blokkra van szükség.

**Példa:**
```python
database_config = config.get_section("database")
host = database_config.get("host")
port = database_config.get("port")
```

### set(*keys, value)

Hierarchikus kulcsokkal lehet értékeket beállítani. Ha a köztes kulcsok nem léteznek, automatikusan létrehozza őket.

**Példa:**
```python
config.set("database", "host", "localhost")
config.set("database", "port", 5432)
```

### validate(schema)

A validációs séma egy dictionary, amely meghatározza az elvárt típusokat és egyéb korlátozásokat. A metódus visszaadja, hogy a validáció sikeres volt-e, és ha nem, akkor a hibákat is tartalmazó dictionary-t.

**Példa:**
```python
schema = {
    "database": dict,
    "logging": dict,
    "timeout": int
}

is_valid, errors = config.validate(schema)
if not is_valid:
    for key, error in errors.items():
        print(f"{key}: {error}")
```

## Kapcsolódó Dokumentáció

- [ConfigManagerFactoryInterface](factory_interface.md)
- [YAMLConfigManager](../implementations/yaml_config_manager.md)
- [Config Implementációk](../implementations/__init__.md)
- [Config Modul](../__init__.md)