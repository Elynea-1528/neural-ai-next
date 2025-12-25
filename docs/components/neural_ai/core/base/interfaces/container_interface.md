# Container Interface - DI konténer interfészek

## Áttekintés

Ez a modul tartalmazza a dependency injection konténerhez és lusta betöltéshez kapcsolódó interfészeket. Az interfészek definiálják a konténer és a lusta komponensek szerződését, és biztosítják a típusbiztonságot.

## Interfészek

### `DIContainerInterface`

**Hely:** [`neural_ai.core.base.interfaces.container_interface:14`](neural_ai/core/base/interfaces/container_interface.py:14)

Dependency injection konténer interfész. Ez az interfész definiálja a dependency injection konténer alapvető funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.

Ez egy absztrakt osztály (ABC), amelyet minden DI konténer implementációjának meg kell valósítania.

#### Absztrakt metódusok

##### `register_instance(interface: InterfaceT, instance: InterfaceT) -> None`
Komponens példány regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a példányt regisztráljuk
- `instance`: A regisztrálandó példány

**Példa:**
```python
from neural_ai.core.base.interfaces.container_interface import DIContainerInterface
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

class MyContainer(DIContainerInterface):
    def register_instance(self, interface, instance):
        self._instances[interface] = instance

container = MyContainer()
logger = DefaultLogger(name="my_logger")
container.register_instance(LoggerInterface, logger)
```

##### `register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`
Factory függvény regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a factory-t regisztráljuk
- `factory`: A factory függvény, ami létrehozza az implementációt

**Példa:**
```python
def create_logger():
    return DefaultLogger(name="factory_logger")

class MyContainer(DIContainerInterface):
    def register_factory(self, interface, factory):
        self._factories[interface] = factory

container.register_factory(LoggerInterface, create_logger)
```

##### `resolve(interface: InterfaceT) -> InterfaceT | None`
Függőség feloldása a konténerből.

**Paraméterek:**
- `interface`: Az interfész típusa, amit fel szeretnénk oldani

**Visszatérési érték:** A regisztrált példány vagy None ha nem található

**Példa:**
```python
class MyContainer(DIContainerInterface):
    def resolve(self, interface):
        return self._instances.get(interface)

logger = container.resolve(LoggerInterface)
if logger:
    logger.info("Üzenet")
```

##### `register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`
Lusta betöltésű komponens regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `factory_func`: A komponens létrehozásához használt factory függvény

**Kivételek:**
- `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

**Példa:**
```python
class MyContainer(DIContainerInterface):
    def register_lazy(self, component_name, factory_func):
        if not component_name:
            raise ValueError("Component name must be non-empty")
        if not callable(factory_func):
            raise ValueError("Factory function must be callable")
        self._lazy_components[component_name] = LazyComponent(factory_func)

def create_expensive_service():
    return ExpensiveService()

container.register_lazy("expensive_service", create_expensive_service)
```

##### `get(component_name: str) -> object`
Komponens példány lekérése (lusta betöltéssel).

**Paraméterek:**
- `component_name`: A lekérendő komponens neve

**Visszatérési érték:** A komponens példánya

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található

**Példa:**
```python
class MyContainer(DIContainerInterface):
    def get(self, component_name):
        if component_name in self._instances:
            return self._instances[component_name]
        if component_name in self._lazy_components:
            return self._lazy_components[component_name].get()
        raise ComponentNotFoundError(f"Component '{component_name}' not found")

service = container.get("expensive_service")
```

##### `clear() -> None`
Konténer ürítése. Eltávolítja az összes regisztrált példányt, factory-t és lusta komponenst.

**Példa:**
```python
class MyContainer(DIContainerInterface):
    def clear(self):
        self._instances.clear()
        self._factories.clear()
        self._lazy_components.clear()

container.clear()
```

### `LazyComponentInterface`

**Hely:** [`neural_ai.core.base.interfaces.container_interface:87`](neural_ai/core/base/interfaces/container_interface.py:87)

Lusta betöltésű komponens interfész. Ez az interfész definiálja a lusta (lazy) betöltésű komponensek alapvető funkcionalitását.

Ez egy absztrakt osztály (ABC), amelyet minden lusta komponens implementációjának meg kell valósítania.

#### Absztrakt metódusok

##### `get() -> object`
Komponens példány lekérése (lusta betöltéssel).

**Visszatérési érték:** A komponens példánya

**Példa:**
```python
from neural_ai.core.base.interfaces.container_interface import LazyComponentInterface

class MyLazyComponent(LazyComponentInterface):
    def __init__(self, factory_func):
        self._factory_func = factory_func
        self._instance = None
        self._loaded = False
    
    def get(self):
        if not self._loaded:
            self._instance = self._factory_func()
            self._loaded = True
        return self._instance

lazy_component = MyLazyComponent(create_expensive_service)
service = lazy_component.get()  # Most jön létre a példány
```

##### `is_loaded` property
Ellenőrzi, hogy a komponens betöltődött-e már.

**Visszatérési érték:** `bool` - True, ha a komponens már betöltődött, egyébként False

**Példa:**
```python
class MyLazyComponent(LazyComponentInterface):
    @property
    def is_loaded(self):
        return self._loaded

print(lazy_component.is_loaded)  # False
service = lazy_component.get()
print(lazy_component.is_loaded)  # True
```

## Teljes implementáció példa

```python
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar, Generic
from neural_ai.core.base.interfaces.container_interface import (
    DIContainerInterface,
    LazyComponentInterface
)
from neural_ai.core.base.exceptions import ComponentNotFoundError

T = TypeVar('T')
InterfaceT = TypeVar('InterfaceT')

# Lusta komponens implementáció
class MyLazyComponent(LazyComponentInterface, Generic[T]):
    def __init__(self, factory_func: Callable[[], T]):
        self._factory_func = factory_func
        self._instance: T | None = None
        self._loaded = False
    
    def get(self) -> T:
        if not self._loaded:
            self._instance = self._factory_func()
            self._loaded = True
        return self._instance  # type: ignore
    
    @property
    def is_loaded(self) -> bool:
        return self._loaded

# DI konténer implementáció
class MyDIContainer(DIContainerInterface):
    def __init__(self):
        self._instances: dict[object, object] = {}
        self._factories: dict[object, Callable[[], object]] = {}
        self._lazy_components: dict[str, MyLazyComponent[object]] = {}
    
    def register_instance(self, interface: InterfaceT, instance: InterfaceT) -> None:
        self._instances[interface] = instance
    
    def register_factory(
        self,
        interface: InterfaceT,
        factory: Callable[[], InterfaceT]
    ) -> None:
        self._factories[interface] = factory
    
    def resolve(self, interface: InterfaceT) -> InterfaceT | None:
        if interface in self._instances:
            return self._instances[interface]  # type: ignore
        if interface in self._factories:
            factory = self._factories[interface]
            instance = factory()
            self._instances[interface] = instance
            return instance  # type: ignore
        return None
    
    def register_lazy(self, component_name: str, factory_func: Callable[[], T]) -> None:
        if not component_name:
            raise ValueError("Component name must be non-empty")
        if not callable(factory_func):
            raise ValueError("Factory function must be callable")
        self._lazy_components[component_name] = MyLazyComponent(factory_func)
    
    def get(self, component_name: str) -> object:
        if component_name in self._instances:
            return self._instances[component_name]
        if component_name in self._lazy_components:
            return self._lazy_components[component_name].get()
        raise ComponentNotFoundError(f"Component '{component_name}' not found")
    
    def clear(self) -> None:
        self._instances.clear()
        self._factories.clear()
        self._lazy_components.clear()
```

## Használati példa

```python
from neural_ai.core.base.interfaces.container_interface import (
    DIContainerInterface,
    LazyComponentInterface
)
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

# Konténer létrehozása
container = MyDIContainer()

# Példány regisztrálása
logger = DefaultLogger(name="app")
container.register_instance(LoggerInterface, logger)

# Factory regisztrálása
def create_config():
    return YamlConfigManager("config.yml")

container.register_factory(ConfigManagerInterface, create_config)

# Lusta komponens regisztrálása
def create_expensive_service():
    print("Drága szolgáltatás létrehozása...")
    return ExpensiveService()

container.register_lazy("expensive_service", create_expensive_service)

# Komponensek lekérése
logger = container.resolve(LoggerInterface)
config = container.resolve(ConfigManagerInterface)
service = container.get("expensive_service")  # Most jön létre
```

## Függőségek

- `abc.ABC` - Absztrakt osztályokhoz
- `abc.abstractmethod` - Absztrakt metódusokhoz
- `collections.abc.Callable` - Függvény típusokhoz
- `typing.TypeVar` - Generikus típusokhoz

## Jellemzők

- **Típusbiztonság:** Erős típusosság generikus típusokkal
- **Függőségi injektálás:** Teljes DI támogatás interfészek alapján
- **Lusta betöltés:** Támogatja a lusta betöltésű komponenseket
- **Tesztelhetőség:** Könnyű mockolás és tesztelés interfészek segítségével

## Implementációk

Ezek az interfészek a következő modulokban vannak implementálva:

- `DIContainerInterface` → [`neural_ai.core.base.implementations.di_container.DIContainer`](neural_ai/core/base/implementations/di_container.md)
- `LazyComponentInterface` → [`neural_ai.core.base.implementations.di_container.LazyComponent`](neural_ai/core/base/implementations/di_container.md)

## Kapcsolódó dokumentáció

- [Base Interfaces Init](neural_ai/core/base/interfaces/__init__.md) - Az interfészek exportáló modulja
- [Component Interface](neural_ai/core/base/interfaces/component_interface.md) - Core komponensek interfész
- [DI Container](neural_ai/core/base/implementations/di_container.md) - Implementáció
- [Lazy Loader](neural_ai/core/base/implementations/lazy_loader.md) - Lusta betöltés implementáció