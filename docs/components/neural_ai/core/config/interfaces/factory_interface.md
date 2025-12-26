# ConfigManagerFactoryInterface

## Áttekintés

Konfiguráció kezelő factory interfész definíciója.

Ez az interfész egy gyártó (factory) mintát valósít meg a konfiguráció kezelők létrehozásához. Lehetővé teszi különböző konfigurációs formátumok kezelését és a kezelők dinamikus regisztrációját.

## Interfész

### `ConfigManagerFactoryInterface`

Konfiguráció kezelő factory interfész.

Ez az absztrakt osztály definiálja a konfiguráció kezelő gyártó alapvető műveleteit, beleértve a kezelők regisztrációját és létrehozását.

#### Absztrakt Osztálymetódusok

##### `register_manager(extension, manager_class)`

Új konfiguráció kezelő típus regisztrálása.

A metódus lehetővé teszi egy adott fájlkiterjesztéshez tartozó konfiguráció kezelő osztály regisztrációját. Ezt követően a gyár képes lesz automatikusan kiválasztani a megfelelő kezelőt a fájlnév alapján.

**Paraméterek:**
- `extension`: A kezelt fájl kiterjesztése (pl: ".yml", ".yaml", ".json")
- `manager_class`: A kezelő osztály, amely implementálja a ConfigManagerInterface-t

**Kivételek:**
- `ValueError`: Ha az extension vagy manager_class érvénytelen
- `TypeError`: Ha a manager_class nem megfelelő típusú

##### `get_manager(filename, manager_type)`

Megfelelő konfiguráció kezelő létrehozása fájlnév vagy típus alapján.

A metódus a fájlnév kiterjesztése alapján automatikusan kiválasztja a megfelelő kezelőt, vagy a megadott típus alapján hozza létre a kezelőt.

**Paraméterek:**
- `filename`: Konfigurációs fájl teljes neve (elérési úttal együtt)
- `manager_type`: Opcionális kezelő típus azonosító

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott konfiguráció kezelő példány

**Kivételek:**
- `ValueError`: Ha a fájlnév kiterjesztése nem regisztrált
- `KeyError`: Ha a megadott manager_type nem létezik
- `RuntimeError`: Ha a kezelő létrehozása sikertelen

##### `create_manager(manager_type, *args, **kwargs)`

Konfiguráció kezelő létrehozása típus alapján.

A metódus explicit típusmegadással hozza létre a konfiguráció kezelőt, lehetővé téve a paraméterek átadását a konstruktornak.

**Paraméterek:**
- `manager_type`: A kért kezelő típus azonosítója
- `*args`: Pozícionális argumentumok a kezelő konstruktorának
- `**kwargs`: Kulcsszavas argumentumok a kezelő konstruktorának

**Visszatérési érték:**
- `ConfigManagerInterface`: A létrehozott konfiguráció kezelő példány

**Kivételek:**
- `KeyError`: Ha a megadott manager_type nem létezik
- `TypeError`: Ha a paraméterek nem kompatibilisek a kezelő konstruktorával
- `RuntimeError`: Ha a kezelő létrehozása sikertelen

## Implementáció

Ez az interfész a következő osztály által van implementálva:

- [`ConfigManagerFactory`](../factory.md#configmanagerfactory)

## Használati Példa

### Egyéni konfigurációkezelő implementáció

```python
from neural_ai.core.config.interfaces import (
    ConfigManagerFactoryInterface,
    ConfigManagerInterface
)
from typing import Any
import json

class JSONConfigManager(ConfigManagerInterface):
    """JSON konfigurációkezelő implementáció."""
    
    def __init__(self, filename: str | None = None):
        self._config = {}
        self._filename = filename
        if filename:
            self.load(filename)
    
    def get(self, *keys: str, default: Any = None) -> Any:
        current = self._config
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key)
            if current is None:
                return default
        return current
    
    def get_section(self, section: str) -> dict[str, Any]:
        if section not in self._config:
            raise KeyError(f"Szekció nem található: {section}")
        return self._config.get(section, {})
    
    def set(self, *keys: str, value: Any) -> None:
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
        save_filename = filename or self._filename
        if not save_filename:
            raise ValueError("Nincs fájlnév megadva")
        
        with open(save_filename, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def load(self, filename: str) -> None:
        with open(filename, 'r') as f:
            self._config = json.load(f)
        self._filename = filename
    
    def validate(self, schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]:
        errors = {}
        for key, expected_type in schema.items():
            value = self._config.get(key)
            if value is not None and not isinstance(value, expected_type):
                errors[key] = f"Várt típus: {expected_type.__name__}"
        return not bool(errors), errors if errors else None

class CustomConfigFactory(ConfigManagerFactoryInterface):
    """Egyéni konfigurációkezelő gyár."""
    
    _managers: dict[str, type[ConfigManagerInterface]] = {}
    
    @classmethod
    def register_manager(
        cls,
        extension: str,
        manager_class: type[ConfigManagerInterface]
    ) -> None:
        """Új konfiguráció kezelő regisztrálása."""
        if not extension.startswith("."):
            extension = f".{extension}"
        
        if not isinstance(manager_class, type):
            raise TypeError("A kezelő osztálynak kell lennie")
        
        if not issubclass(manager_class, ConfigManagerInterface):
            raise TypeError("A kezelő osztálynak implementálnia kell a ConfigManagerInterface-t")
        
        cls._managers[extension] = manager_class
    
    @classmethod
    def get_manager(
        cls,
        filename: str,
        manager_type: str | None = None
    ) -> ConfigManagerInterface:
        """Konfiguráció kezelő létrehozása."""
        if manager_type:
            ext = f".{manager_type}" if not manager_type.startswith(".") else manager_type
            if ext in cls._managers:
                return cls._managers[ext](filename)
            raise KeyError(f"Ismeretlen kezelő típus: {manager_type}")
        
        from pathlib import Path
        ext = Path(filename).suffix.lower()
        if ext in cls._managers:
            return cls._managers[ext](filename)
        
        raise ValueError(f"Nem támogatott fájlkiterjesztés: {ext}")
    
    @classmethod
    def create_manager(
        cls,
        manager_type: str,
        *args: object,
        **kwargs: object
    ) -> ConfigManagerInterface:
        """Konfiguráció kezelő létrehozása típus alapján."""
        if not manager_type.startswith("."):
            manager_type = f".{manager_type}"
        
        if manager_type in cls._managers:
            return cls._managers[manager_type](*args, **kwargs)
        
        raise KeyError(f"Ismeretlen kezelő típus: {manager_type}")

# Használat
CustomConfigFactory.register_manager(".json", JSONConfigManager)
json_config = CustomConfigFactory.get_manager("config.json")
```

## Tervezési Minta

A `ConfigManagerFactoryInterface` a **Factory Method** tervezési mintát valósítja meg, amely:

1. **Lazítási elvet követ**: A konkrét osztályok létrehozását a leszármazott osztályokra bízza
2. **Bővíthetőséget biztosít**: Új konfigurációs formátumok egyszerűen hozzáadhatók
3. **Egységes interfészt nyújt**: Minden konfigurációkezelő ugyanazt az interfészt implementálja
4. **Dinamikus választást tesz lehetővé**: A fájlkiterjesztés alapján automatikusan kiválasztja a megfelelő kezelőt

## Kapcsolódó Dokumentáció

- [ConfigManagerInterface](config_interface.md)
- [ConfigManagerFactory](../factory.md)
- [Config Implementációk](../implementations/__init__.md)
- [Config Modul](../__init__.md)