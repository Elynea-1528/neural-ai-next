# Base Interfaces - Alap interfészek

## Áttekintés

Ez a modul tartalmazza a Neural AI Next base komponens rendszerének összes interfészét és absztrakt osztályát. Az interfészek definiálják a komponensek szerződését, és biztosítják a típusbiztonságot és a függőségi injektálás támogatását.

## Exportált interfészek

### `DIContainerInterface`

**Hely:** [`neural_ai.core.base.interfaces.container_interface:14`](neural_ai/core/base/interfaces/container_interface.py:14)

Dependency injection konténer interfész. Ez az interfész definiálja a dependency injection konténer alapvető funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.

**Főbb metódusok:**
- `register_instance()` - Komponens példány regisztrálása
- `register_factory()` - Factory függvény regisztrálása
- `resolve()` - Függőség feloldása
- `register_lazy()` - Lusta betöltésű komponens regisztrálása
- `get()` - Komponens példány lekérése

### `LazyComponentInterface`

**Hely:** [`neural_ai.core.base.interfaces.container_interface:87`](neural_ai/core/base/interfaces/container_interface.py:87)

Lusta betöltésű komponens interfész. Ez az interfész definiálja a lusta (lazy) betöltésű komponensek alapvető funkcionalitását.

**Főbb metódusok:**
- `get()` - Komponens példány lekérése
- `is_loaded` property - Ellenőrzi, hogy a komponens betöltődött-e már

### `CoreComponentsInterface`

**Hely:** [`neural_ai.core.base.interfaces.component_interface:17`](neural_ai/core/base/interfaces/component_interface.py:17)

Core komponensek interfész. Ez az interfész definiálja a core komponensek gyűjteményének alapvető funkcionalitását és hozzáférését.

**Főbb metódusok:**
- `config` property - Konfiguráció kezelő komponens
- `logger` property - Logger komponens
- `storage` property - Storage komponens
- `has_config()` - Ellenőrzi, hogy van-e konfigurációs komponens
- `has_logger()` - Ellenőrzi, hogy van-e logger komponens
- `has_storage()` - Ellenőrzi, hogy van-e storage komponens
- `validate()` - Ellenőrzi, hogy minden szükséges komponens rendelkezésre áll-e

### `CoreComponentFactoryInterface`

**Hely:** [`neural_ai.core.base.interfaces.component_interface:91`](neural_ai/core/base/interfaces/component_interface.py:91)

Core komponens factory interfész. Ez az interfész definiálja a core komponensek létrehozásáért és inicializálásáért felelős factory osztály alapvető funkcionalitását.

**Főbb metódusok:**
- `create_components()` - Core komponensek létrehozása és inicializálása
- `create_with_container()` - Core komponensek létrehozása meglévő konténerből
- `create_minimal()` - Minimális core komponens készlet létrehozása

## Használati példa

### Interfész implementáció

```python
from abc import ABC, abstractmethod
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface

class MyDIContainer(DIContainerInterface):
    def register_instance(self, interface, instance):
        # Implementáció
        pass
    
    def register_factory(self, interface, factory):
        # Implementáció
        pass
    
    def resolve(self, interface):
        # Implementáció
        pass
    
    def register_lazy(self, component_name, factory_func):
        # Implementáció
        pass
    
    def get(self, component_name):
        # Implementáció
        pass
    
    def clear(self):
        # Implementáció
        pass
```

### Típusellenőrzés

```python
from typing import TYPE_CHECKING
from neural_ai.core.base.interfaces import (
    DIContainerInterface,
    CoreComponentsInterface
)

if TYPE_CHECKING:
    # Típusellenőrzéshez használható
    container: DIContainerInterface
    components: CoreComponentsInterface
```

### Factory implementáció

```python
from neural_ai.core.base.interfaces import CoreComponentFactoryInterface
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface

class MyComponentFactory(CoreComponentFactoryInterface):
    @staticmethod
    def create_components(config_path=None, log_path=None, storage_path=None):
        # Implementáció
        pass
    
    @staticmethod
    def create_with_container(container: DIContainerInterface):
        # Implementáció
        pass
    
    @staticmethod
    def create_minimal():
        # Implementáció
        pass
```

## Interfész hierarchia

```
DIContainerInterface
├── register_instance()
├── register_factory()
├── resolve()
├── register_lazy()
├── get()
└── clear()

LazyComponentInterface
├── get()
└── is_loaded property

CoreComponentsInterface
├── config property
├── logger property
├── storage property
├── has_config()
├── has_logger()
├── has_storage()
└── validate()

CoreComponentFactoryInterface
├── create_components()
├── create_with_container()
└── create_minimal()
```

## Jellemzők

- **Típusbiztonság:** Erős típusosság a `typing` modul használatával
- **Függőségi injektálás:** Teljes DI támogatás interfészek alapján
- **Lusta betöltés:** Támogatja a lusta betöltésű komponenseket
- **Tesztelhetőség:** Könnyű mockolás és tesztelés interfészek segítségével
- **Körkörös importok elkerülése:** `TYPE_CHECKING` használatával

## Implementációk

Ezek az interfészek a következő modulokban vannak implementálva:

- `DIContainerInterface` → [`neural_ai.core.base.implementations.di_container.DIContainer`](neural_ai/core/base/implementations/di_container.md)
- `LazyComponentInterface` → [`neural_ai.core.base.implementations.di_container.LazyComponent`](neural_ai/core/base/implementations/di_container.md)
- `CoreComponentsInterface` → [`neural_ai.core.base.implementations.component_bundle.CoreComponents`](neural_ai/core/base/implementations/component_bundle.md)
- `CoreComponentFactoryInterface` → [`neural_ai.core.base.factory.CoreComponentFactory`](neural_ai/core/base/factory.md)

## Kapcsolódó dokumentáció

- [Container Interface](neural_ai/core/base/interfaces/container_interface.md) - DI konténer interfész részletes leírása
- [Component Interface](neural_ai/core/base/interfaces/component_interface.md) - Core komponensek interfész részletes leírása
- [DI Container](neural_ai/core/base/implementations/di_container.md) - Implementáció
- [Component Bundle](neural_ai/core/base/implementations/component_bundle.md) - Implementáció