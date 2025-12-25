# DI Container - Dependency Injection Konténer

## Áttekintés

Ez a modul egy egyszerű dependency injection (DI) konténer implementációt tartalmaz. A konténer kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását. Támogatja a lusta betöltést, singleton mintát és a komponensek életciklus kezelését.

## Osztályok

### `LazyComponent[T]`

**Hely:** [`neural_ai.core.base.implementations.di_container:16`](neural_ai/core/base/implementations/di_container.py:16)

Lusta betöltésű komponensek wrapper osztálya. Ez az osztály biztosítja a komponensek lusta (lazy) betöltését, ami azt jelenti, hogy a komponens csak akkor jön létre, amikor először használják.

#### Metódusok

##### `__init__(factory_func: Callable[[], T]) -> None`
Inicializálja a lusta komponenst.

**Paraméterek:**
- `factory_func`: A komponens létrehozásához használt factory függvény

##### `get() -> T`
Lekéri a komponens példányt (lusta betöltéssel).

**Visszatérési érték:** A komponens példánya

##### `is_loaded` property
Ellenőrzi, hogy a komponens betöltődött-e már.

**Visszatérési érték:** `bool` - True, ha a komponens már betöltődött, egyébként False

**Példa:**
```python
from neural_ai.core.base.implementations.di_container import LazyComponent

def create_expensive_service():
    print("Szolgáltatás létrehozása...")
    return ExpensiveService()

lazy_service = LazyComponent(create_expensive_service)
# A create_expensive_service még nem futott le

service = lazy_service.get()  # Most fut le: "Szolgáltatás létrehozása..."
# service egy ExpensiveService példány

service2 = lazy_service.get()  # Már nem fut le, ugyanazt a példányt adja vissza
```

### `DIContainer`

**Hely:** [`neural_ai.core.base.implementations.di_container:57`](neural_ai/core/base/implementations/di_container.py:57)

Egyszerű dependency injection konténer. A konténer kezeli a komponensek közötti függőségeket és biztosítja azok megfelelő inicializálását.

#### Attribútumok

- `_instances: dict[object, object]` - Regisztrált példányok tárolója
- `_factories: dict[object, Callable[[], object]]` - Factory függvények tárolója
- `_lazy_components: dict[str, LazyComponent[object]]` - Lusta komponensek tárolója
- `_logger: logging.Logger` - Logger példány

#### Metódusok

##### `__init__() -> None`
Konténer inicializálása.

##### `register_instance(interface: InterfaceT, instance: InterfaceT) -> None`
Példány regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa
- `instance`: Az interfészt megvalósító példány

**Példa:**
```python
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger

container = DIContainer()
logger = DefaultLogger(name="my_logger")
container.register_instance(LoggerInterface, logger)
```

##### `register_factory(interface: InterfaceT, factory: Callable[[], InterfaceT]) -> None`
Factory függvény regisztrálása a konténerben.

**Paraméterek:**
- `interface`: Az interfész típusa
- `factory`: Az interfész implementációját létrehozó factory függvény

**Példa:**
```python
def create_logger():
    return DefaultLogger(name="factory_logger")

container.register_factory(LoggerInterface, create_logger)
```

##### `resolve(interface: InterfaceT) -> InterfaceT | None`
Függőség feloldása a konténerből.

**Paraméterek:**
- `interface`: Az interfész típusa

**Visszatérési érték:** Az interfészhez tartozó példány vagy None

**Példa:**
```python
logger = container.resolve(LoggerInterface)
if logger:
    logger.info("Üzenet")
```

##### `register_lazy(component_name: str, factory_func: Callable[[], T]) -> None`
Lusta betöltésű komponens regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `factory_func`: A komponenst létrehozó függvény

**Kivételek:**
- `ValueError`: Ha a komponens név érvénytelen vagy a factory függvény nem hívható

**Példa:**
```python
def create_expensive_service():
    return ExpensiveService()

container.register_lazy("expensive_service", create_expensive_service)
```

##### `get(component_name: str) -> object`
Komponens példány lekérése (lusta betöltés támogatással).

**Paraméterek:**
- `component_name`: A lekérendő komponens neve

**Visszatérési érték:** A komponens példánya

**Kivételek:**
- `ComponentNotFoundError`: Ha a komponens nem található

**Példa:**
```python
service = container.get("expensive_service")
```

##### `get_lazy_components() -> dict[str, bool]`
Visszaadja az összes lusta komponens állapotát.

**Visszatérési érték:** Szótár, ahol a kulcsok a komponens nevek, az értékek pedig azt jelzik, hogy a komponens betöltődött-e már

**Példa:**
```python
lazy_status = container.get_lazy_components()
for name, loaded in lazy_status.items():
    print(f"{name}: {'loaded' if loaded else 'not loaded'}")
```

##### `preload_components(component_names: list[str]) -> None`
Előre betölti a megadott komponenseket.

**Paraméterek:**
- `component_names`: A betöltendő komponensek neveinek listája

**Példa:**
```python
container.preload_components(["expensive_service", "database_connection"])
```

##### `clear() -> None`
Kiüríti a konténert. Eltávolítja az összes regisztrált példányt, factory-t és lusta komponenst.

**Példa:**
```python
container.clear()
```

##### `register(component_name: str, instance: object) -> None`
Komponens példány regisztrálása.

**Paraméterek:**
- `component_name`: A komponens neve
- `instance`: A regisztrálandó példány

**Kivételek:**
- `ValueError`: Ha a component_name érvénytelen vagy az instance None
- `SingletonViolationError`: Ha a singleton minta megsértésre kerül

##### `get_memory_usage() -> dict[str, int | dict[str, int]]`
Memóriahasználati statisztikák lekérése.

**Visszatérési érték:** Szótár a memóriahasználati adatokkal:
- `total_instances`: A regisztrált példányok száma
- `lazy_components`: A lusta komponensek száma
- `loaded_lazy_components`: A betöltött lusta komponensek száma
- `instance_sizes`: Az egyes példányok mérete

**Példa:**
```python
stats = container.get_memory_usage()
print(f"Összes példány: {stats['total_instances']}")
print(f"Példány méretek: {stats['instance_sizes']}")
```

## Használati példa

```python
from neural_ai.core.base.implementations.di_container import DIContainer
from neural_ai.core.logger.interfaces.logger_interface import LoggerInterface
from neural_ai.core.logger.implementations.default_logger import DefaultLogger
from neural_ai.core.config.interfaces.config_interface import ConfigManagerInterface
from neural_ai.core.config.implementations.yaml_config_manager import YamlConfigManager

# Konténer létrehozása
container = DIContainer()

# Példány regisztrálása
logger = DefaultLogger(name="app")
container.register_instance(LoggerInterface, logger)

# Factory regisztrálása
def create_config():
    return YamlConfigManager("config.yml")

container.register_factory(ConfigManagerInterface, create_config)

# Lusta komponens regisztrálása
def create_expensive_service():
    return ExpensiveService()

container.register_lazy("expensive_service", create_expensive_service)

# Komponensek lekérése
logger = container.resolve(LoggerInterface)
config = container.resolve(ConfigManagerInterface)
service = container.get("expensive_service")

# Memóriahasználat ellenőrzése
stats = container.get_memory_usage()
print(stats)
```

## Singleton Pattern ellenőrzés

A konténer automatikusan ellenőrzi a singleton mintát:

- Figyelmeztet, ha egy példánynak nincs `_initialized` flag-je
- Figyelmeztet, ha egy osztálynak nincs `_instance` osztályváltozója
- Kivételt dob, ha egy komponenst többször próbálnak regisztrálni különböző példányokkal

## Függőségek

- `logging` - Naplózás
- `threading` - Szálbiztosság
- `warnings` - Figyelmeztetések
- `neural_ai.core.base.exceptions.ComponentNotFoundError`
- `neural_ai.core.base.exceptions.SingletonViolationError`

## Jellemzők

- **Dependency Injection:** Teljes DI támogatás interfészek alapján
- **Lazy Loading:** Lustabetöltés támogatása drága erőforrásokhoz
- **Singleton Pattern:** Automatikus singleton ellenőrzés és betartatás
- **Szálbiztosság:** Biztonságos használat többszálú környezetben
- **Memóriamonitoring:** Beépített memóriahasználati statisztikák
- **Type Safety:** Generikus típusokkal erős típusosság

## Kapcsolódó dokumentáció

- [Core Component Factory](neural_ai/core/base/factory.md)
- [Component Bundle](neural_ai/core/base/implementations/component_bundle.md)
- [Lazy Loader](neural_ai/core/base/implementations/lazy_loader.md)