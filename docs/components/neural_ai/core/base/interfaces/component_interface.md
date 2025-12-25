# Component Interface - Core komponens interfészek

## Áttekintés

Ez a modul tartalmazza a core komponensekhez kapcsolódó interfészeket. Az interfészek definiálják a komponensek szerződését, és biztosítják a típusbiztonságot és a függőségi injektálás támogatását.

## Interfészek

### `CoreComponentsInterface`

**Hely:** [`neural_ai.core.base.interfaces.component_interface:17`](neural_ai/core/base/interfaces/component_interface.py:17)

Core komponensek interfész. Ez az interfész definiálja a core komponensek gyűjteményének alapvető funkcionalitását és hozzáférését.

Ez egy absztrakt osztály (ABC), amelyet minden core komponens gyűjtemény implementációjának meg kell valósítania.

#### Absztrakt metódusok

##### `config` property
Konfiguráció kezelő komponens.

**Visszatérési érték:** `ConfigManagerInterface | None` - A konfiguráció kezelő komponens vagy None

**Példa:**
```python
from neural_ai.core.base.interfaces.component_interface import CoreComponentsInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface

class MyComponents(CoreComponentsInterface):
    @property
    def config(self) -> ConfigManagerInterface | None:
        return self._config
```

##### `logger` property
Logger komponens.

**Visszatérési érték:** `LoggerInterface | None` - A logger komponens vagy None

##### `storage` property
Storage komponens.

**Visszatérési érték:** `StorageInterface | None` - A storage komponens vagy None

##### `has_config() -> bool`
Ellenőrzi, hogy van-e konfigurációs komponens.

**Visszatérési érték:** `bool` - True ha van konfigurációs komponens, különben False

**Példa:**
```python
if components.has_config():
    config = components.config
    value = config.get("setting")
```

##### `has_logger() -> bool`
Ellenőrzi, hogy van-e logger komponens.

**Visszatérési érték:** `bool` - True ha van logger komponens, különben False

##### `has_storage() -> bool`
Ellenőrzi, hogy van-e storage komponens.

**Visszatérési érték:** `bool` - True ha van storage komponens, különben False

##### `validate() -> bool`
Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e.

**Visszatérési érték:** `bool` - True ha minden komponens elérhető, különben False

**Példa:**
```python
from neural_ai.core.base.interfaces.component_interface import CoreComponentsInterface
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

class MyComponents(CoreComponentsInterface):
    def __init__(self):
        self._config: ConfigManagerInterface | None = None
        self._logger: LoggerInterface | None = None
        self._storage: StorageInterface | None = None
    
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

### `CoreComponentFactoryInterface`

**Hely:** [`neural_ai.core.base.interfaces.component_interface:91`](neural_ai/core/base/interfaces/component_interface.py:91)

Core komponens factory interfész. Ez az interfész definiálja a core komponensek létrehozásáért és inicializálásáért felelős factory osztály alapvető funkcionalitását.

Ez egy absztrakt osztály (ABC), amelyet minden core komponens factory implementációjának meg kell valósítania.

#### Absztrakt metódusok

##### `create_components(config_path, log_path, storage_path) -> CoreComponentsInterface` (static)
Core komponensek létrehozása és inicializálása.

**Paraméterek:**
- `config_path: str | None` - Konfiguráció útvonala (opcionális)
- `log_path: str | None` - Log fájl útvonala (opcionális)
- `storage_path: str | None` - Storage alap útvonal (opcionális)

**Visszatérési érték:** `CoreComponentsInterface` - Az inicializált komponensek

**Példa:**
```python
from neural_ai.core.base.interfaces.component_interface import (
    CoreComponentFactoryInterface,
    CoreComponentsInterface
)

class MyFactory(CoreComponentFactoryInterface):
    @staticmethod
    def create_components(
        config_path: str | None = None,
        log_path: str | None = None,
        storage_path: str | None = None,
    ) -> CoreComponentsInterface:
        # Implementáció
        components = MyComponents()
        # Inicializálás
        return components
```

##### `create_with_container(container) -> CoreComponentsInterface` (static)
Core komponensek létrehozása meglévő konténerből.

**Paraméterek:**
- `container: DIContainerInterface` - A dependency injection konténer

**Visszatérési érték:** `CoreComponentsInterface` - Az inicializált komponensek

**Példa:**
```python
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface

class MyFactory(CoreComponentFactoryInterface):
    @staticmethod
    def create_with_container(
        container: DIContainerInterface
    ) -> CoreComponentsInterface:
        # Komponensek létrehozása a konténerből
        components = MyComponents()
        # Inicializálás
        return components
```

##### `create_minimal() -> CoreComponentsInterface` (static)
Minimális core komponens készlet létrehozása alapértelmezett beállításokkal.

**Visszatérési érték:** `CoreComponentsInterface` - Az alapértelmezett komponensek

**Példa:**
```python
class MyFactory(CoreComponentFactoryInterface):
    @staticmethod
    def create_minimal() -> CoreComponentsInterface:
        # Alapértelmezett komponensek létrehozása
        components = MyComponents()
        # Minimális inicializálás
        return components
```

## Teljes implementáció példa

```python
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from neural_ai.core.base.interfaces.component_interface import (
    CoreComponentsInterface,
    CoreComponentFactoryInterface
)
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface

if TYPE_CHECKING:
    from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
    from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
    from neural_ai.core.storage.interfaces.storage_interface import StorageInterface

# Komponens gyűjtemény implementáció
class MyCoreComponents(CoreComponentsInterface):
    def __init__(self, container: DIContainerInterface):
        self._container = container
    
    @property
    def config(self) -> "ConfigManagerInterface | None":
        from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
        return self._container.resolve(ConfigManagerInterface)
    
    @property
    def logger(self) -> "LoggerInterface | None":
        from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
        return self._container.resolve(LoggerInterface)
    
    @property
    def storage(self) -> "StorageInterface | None":
        from neural_ai.core.storage.interfaces.storage_interface import StorageInterface
        return self._container.resolve(StorageInterface)
    
    def has_config(self) -> bool:
        return self.config is not None
    
    def has_logger(self) -> bool:
        return self.logger is not None
    
    def has_storage(self) -> bool:
        return self.storage is not None
    
    def validate(self) -> bool:
        return all([self.has_config(), self.has_logger(), self.has_storage()])

# Factory implementáció
class MyCoreFactory(CoreComponentFactoryInterface):
    @staticmethod
    def create_components(
        config_path: str | None = None,
        log_path: str | None = None,
        storage_path: str | None = None,
    ) -> CoreComponentsInterface:
        from neural_ai.core.base.implementations.di_container import DIContainer
        container = DIContainer()
        # Komponensek regisztrálása
        return MyCoreComponents(container)
    
    @staticmethod
    def create_with_container(
        container: DIContainerInterface
    ) -> CoreComponentsInterface:
        return MyCoreComponents(container)
    
    @staticmethod
    def create_minimal() -> CoreComponentsInterface:
        from neural_ai.core.base.implementations.di_container import DIContainer
        container = DIContainer()
        return MyCoreComponents(container)
```

## Függőségek

- `abc.ABC` - Absztrakt osztályokhoz
- `abc.abstractmethod` - Absztrakt metódusokhoz
- `typing.TYPE_CHECKING` - Körkörös importok elkerüléséhez
- `neural_ai.core.base.interfaces.container_interface.DIContainerInterface`

## Jellemzők

- **Típusbiztonság:** Erős típusosság a `typing` modul használatával
- **Függőségi injektálás:** Teljes DI támogatás interfészek alapján
- **Tesztelhetőség:** Könnyű mockolás és tesztelés interfészek segítségével
- **Körkörös importok elkerülése:** `TYPE_CHECKING` használatával

## Implementációk

Ezek az interfészek a következő modulokban vannak implementálva:

- `CoreComponentsInterface` → [`neural_ai.core.base.implementations.component_bundle.CoreComponents`](neural_ai/core/base/implementations/component_bundle.md)
- `CoreComponentFactoryInterface` → [`neural_ai.core.base.factory.CoreComponentFactory`](neural_ai/core/base/factory.md)

## Kapcsolódó dokumentáció

- [Base Interfaces Init](neural_ai/core/base/interfaces/__init__.md) - Az interfészek exportáló modulja
- [Container Interface](neural_ai/core/base/interfaces/container_interface.md) - DI konténer interfész
- [Component Bundle](neural_ai/core/base/implementations/component_bundle.md) - Implementáció
- [Core Component Factory](neural_ai/core/base/factory.md) - Implementáció