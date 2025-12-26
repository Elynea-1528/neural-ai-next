# Component Interface

## Áttekintés

Core komponens interfészek.

Ez a modul tartalmazza a core komponensekhez kapcsolódó interfészeket.

## Interfészek

### `CoreComponentsInterface`

Core komponensek interfész.

Ez az interfész definiálja a core komponensek gyűjteményének alapvető funkcionalitását és hozzáférését.

#### Absztrakt Metódusok

##### `config` property

Konfiguráció kezelő komponens.

**Visszatérési érték:**
- `ConfigManagerInterface | None`: A konfiguráció kezelő komponens vagy None

##### `logger` property

Logger komponens.

**Visszatérési érték:**
- `LoggerInterface | None`: A logger komponens vagy None

##### `storage` property

Storage komponens.

**Visszatérési érték:**
- `StorageInterface | None`: A storage komponens vagy None

##### `has_config()`

Ellenőrzi, hogy van-e konfigurációs komponens.

**Visszatérési érték:**
- `bool`: True ha van konfigurációs komponens, különben False

##### `has_logger()`

Ellenőrzi, hogy van-e logger komponens.

**Visszatérési érték:**
- `bool`: True ha van logger komponens, különben False

##### `has_storage()`

Ellenőrzi, hogy van-e storage komponens.

**Visszatérési érték:**
- `bool`: True ha van storage komponens, különben False

##### `validate()`

Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

**Visszatérési érték:**
- `bool`: True ha minden komponens elérhető, különben False

### `CoreComponentFactoryInterface`

Core komponens factory interfész.

Ez az interfész definiálja a core komponensek létrehozásáért és inicializálásáért felelős factory osztály alapvető funkcionalitását.

#### Absztrakt Metódusok

##### `create_components(config_path, log_path, storage_path)`

Core komponensek létrehozása és inicializálása.

**Paraméterek:**
- `config_path`: Konfiguráció útvonala (opcionális)
- `log_path`: Log fájl útvonala (opcionális)
- `storage_path`: Storage alap útvonal (opcionális)

**Visszatérési érték:**
- `CoreComponentsInterface`: Az inicializált komponensek

##### `create_with_container(container)`

Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container`: A dependency injection konténer

**Visszatérési érték:**
- `CoreComponentsInterface`: Az inicializált komponensek

##### `create_minimal()`

Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:**
- `CoreComponentsInterface`: Az alapértelmezett komponensek

## Implementáció

Ezek az interfészek a következő osztályok által vannak implementálva:

- [`CoreComponents`](../implementations/component_bundle.md#corecomponents)
- [`CoreComponentFactory`](../factory.md)

## Használati Példa

```python
from neural_ai.core.base.interfaces import CoreComponentsInterface
from neural_ai.core.config.interfaces import ConfigManagerInterface
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.storage.interfaces import StorageInterface

class MyCustomComponents(CoreComponentsInterface):
    def __init__(self, config, logger, storage):
        self._config = config
        self._logger = logger
        self._storage = storage
    
    @property
    def config(self) -> ConfigManagerInterface | None:
        return self._config
    
    @property
    def logger(self) -> LoggerInterface | None:
        return self._logger
    
    @property
    def storage(self) -> StorageInterface | None:
        return self._storage
    
    def has_config(self) -> bool:
        return self._config is not None
    
    def has_logger(self) -> bool:
        return self._logger is not None
    
    def has_storage(self) -> bool:
        return self._storage is not None
    
    def validate(self) -> bool:
        return all([self.has_config(), self.has_logger(), self.has_storage()])
```

## Kapcsolódó Dokumentáció

- [Container Interface](container_interface.md)
- [Interfészek Modul](__init__.md)
- [Base Modul](../__init__.md)