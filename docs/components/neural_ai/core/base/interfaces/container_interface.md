# Container Interface

## Áttekintés

Dependency injection konténer interfészek.

Ez a modul tartalmazza a DI konténerhez és lusta betöltéshez kapcsolódó interfészeket.

## Interfészek

### `DIContainerInterface`

Dependency injection konténer interfész.

Ez az interfész definiálja a dependency injection konténer alapvető funkcionalitását, amely a komponensek közötti függőségek kezelését biztosítja.

#### Absztrakt Metódusok

##### `register_instance(interface, instance)`

Komponens példány regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a példányt regisztráljuk
- `instance`: A regisztrálandó példány

##### `register_factory(interface, factory)`

Factory függvény regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa, amihez a factory-t regisztráljuk
- `factory`: A factory függvény, ami létrehozza az implementációt

##### `resolve(interface)`

Függőség feloldása a konténerből.

**Paraméterek:**
- `interface`: Az interfész típusa, amit fel szeretnénk oldani

**Visszatérési érték:**
- `InterfaceT | None`: A regisztrált példány vagy None ha nem található

##### `register_lazy(component_name, factory_func)`

Lusta betöltésű komponens regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `factory_func`: A komponens létrehozásához használt factory függvény

**Kivételek:**
- `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

##### `get(component_name)`

Komponens példány lekérése (lusta betöltéssel).

**Paraméterek:**
- `component_name`: A lekérendő komponens neve

**Visszatérési érték:**
- `object`: A komponens példánya

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található

##### `clear()`

Konténer ürítése.

### `LazyComponentInterface`

Lusta betöltésű komponens interfész.

Ez az interfész definiálja a lusta (lazy) betöltésű komponensek alapvető funkcionalitását.

#### Absztrakt Metódusok

##### `get()`

Komponens példány lekérése (lusta betöltéssel).

**Visszatérési érték:**
- `object`: A komponens példánya

##### `is_loaded` property

Ellenőrzi, hogy a komponens betöltődött-e már.

**Visszatérési érték:**
- `bool`: True, ha a komponens már betöltődött, egyébként False

## Implementáció

Ezek az interfészek a következő osztályok által vannak implementálva:

- [`DIContainer`](../implementations/di_container.md#dicontainer)
- [`LazyComponent`](../implementations/di_container.md#lazycomponent)

## Használati Példák

### Alap konténer használat

```python
from neural_ai.core.base.interfaces import DIContainerInterface
from neural_ai.core.logger.interfaces import LoggerInterface
from neural_ai.core.logger.implementations import DefaultLogger

class MyContainer(DIContainerInterface):
    def __init__(self):
        self._instances = {}
        self._factories = {}
    
    def register_instance(self, interface, instance):
        self._instances[interface] = instance
    
    def register_factory(self, interface, factory):
        self._factories[interface] = factory
    
    def resolve(self, interface):
        if interface in self._instances:
            return self._instances[interface]
        if interface in self._factories:
            return self._factories[interface]()
        return None
    
    # ... egyéb metódusok implementációja
```

### Lusta betöltés használata

```python
from neural_ai.core.base.interfaces import LazyComponentInterface
import threading

class MyLazyComponent(LazyComponentInterface):
    def __init__(self, factory_func):
        self._factory_func = factory_func
        self._instance = None
        self._loaded = False
        self._lock = threading.RLock()
    
    def get(self):
        with self._lock:
            if not self._loaded:
                self._instance = self._factory_func()
                self._loaded = True
        return self._instance
    
    @property
    def is_loaded(self):
        return self._loaded
```

## Kapcsolódó Dokumentáció

- [Component Interface](component_interface.md)
- [Interfészek Modul](__init__.md)
- [DIContainer Implementáció](../implementations/di_container.md)
- [Base Modul](../__init__.md)