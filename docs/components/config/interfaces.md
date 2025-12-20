# Config Komponens Interfészek

## Áttekintés

A config komponens interfészei definiálják a konfigurációkezelő rendszer alapvető szerződéseit és absztrakt osztályait. Ezek biztosítják a típusbiztonságot és a konzisztens API-t a különböző konfigurációkezelő implementációk között.

## Főbb Interfészek

### ConfigManagerInterface

A konfigurációkezelők alapvető interfésze.

#### Metódusok

- `__init__(filename: str | None = None) -> None`: Inicializálja a konfigurációkezelőt
- `get(*keys: str, default: Any = None) -> Any`: Érték lekérése a konfigurációból
- `get_section(section: str) -> dict[str, Any]`: Teljes konfigurációs szekció lekérése
- `set(*keys: str, value: Any) -> None`: Érték beállítása a konfigurációban
- `save(filename: str | None = None) -> None`: Konfiguráció mentése fájlba
- `load(filename: str) -> None`: Konfiguráció betöltése fájlból
- `validate(schema: dict[str, Any]) -> tuple[bool, dict[str, str] | None]`: Konfiguráció validálása séma alapján

### ConfigManagerFactoryInterface

A konfigurációkezelők létrehozásáért felelős factory interfész.

#### Metódusok

- `register_manager(extension: str, manager_class: type[ConfigManagerInterface]) -> None`: Új konfiguráció kezelő típus regisztrálása
- `get_manager(filename: str, manager_type: str | None = None) -> ConfigManagerInterface`: Megfelelő konfiguráció kezelő létrehozása
- `create_manager(manager_type: str, *args: Any, **kwargs: Any) -> ConfigManagerInterface`: Konfiguráció kezelő létrehozása típus alapján

## Használat

```python
from neural_ai.core.config.interfaces import ConfigManagerInterface, ConfigManagerFactoryInterface

# Interfész alapú programozás
def create_config_manager(factory: ConfigManagerFactoryInterface) -> ConfigManagerInterface:
    # Implementáció a factory használatával
    pass
```

## Típusbiztonság

Minden interfész teljes típusannotációval rendelkezik, biztosítva a fordítási idejű típusellenőrzést és az IDE támogatást.

## Kiterjesztés

Új interfészek hozzáadásakor mindig kövesse ezeket az irányelveket:

1. Használjon ABC (Abstract Base Class) alapot
2. Definiálja az összes absztrakt metódust
3. Adjon hozzá teljes típusannotációt
4. Írjon Google style docstring-et
5. Frissítse ezt a dokumentációt

## Kapcsolódó Dokumentáció

- [API Referencia](api.md)
- [Architektúra](architecture.md)
- [Fejlesztési Útmutató](development_checklist.md)
