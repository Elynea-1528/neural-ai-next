# Base Komponens Interfészek

## Áttekintés

A base komponens interfészei definiálják a rendszer alapvető szerződéseit és absztrakt osztályait. Ezek biztosítják a típusbiztonságot és a konzisztens API-t a különböző implementációk között.

## Főbb Interfészek

### DIContainerInterface

A dependency injection konténer alapvető interfésze.

#### Metódusok

- `register_instance(interface, instance)`: Komponens példány regisztrálása
- `register_factory(interface, factory)`: Factory függvény regisztrálása
- `resolve(interface)`: Függőség feloldása
- `register_lazy(component_name, factory_func)`: Lusta betöltésű komponens regisztrálása
- `get(component_name)`: Komponens példány lekérése
- `clear()`: Konténer ürítése

### CoreComponentsInterface

A core komponensek gyűjteményének interfésze.

#### Tulajdonságok

- `config`: Konfiguráció kezelő komponens (opcionális)
- `logger`: Logger komponens (opcionális)
- `storage`: Storage komponens (opcionális)

#### Metódusok

- `has_config()`: Konfigurációs komponens ellenőrzése
- `has_logger()`: Logger komponens ellenőrzése
- `has_storage()`: Storage komponens ellenőrzése
- `validate()`: Összes szükséges komponens ellenőrzése

### CoreComponentFactoryInterface

A core komponensek létrehozásáért felelős factory interfész.

#### Metódusok

- `create_components(config_path, log_path, storage_path)`: Teljes komponens készlet létrehozása
- `create_with_container(container)`: Komponensek létrehozása meglévő konténerből
- `create_minimal()`: Minimális komponens készlet létrehozása

### LazyComponentInterface

A lusta betöltésű komponensek interfésze.

#### Metódusok

- `get()`: Komponens példány lekérése (lusta betöltéssel)

#### Tulajdonságok

- `is_loaded`: Betöltöttség ellenőrzése

## Használat

```python
from neural_ai.core.base.interfaces import DIContainerInterface, CoreComponentsInterface

# Interfész alapú programozás
def create_components(container: DIContainerInterface) -> CoreComponentsInterface:
    # Implementáció a konténer használatával
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

